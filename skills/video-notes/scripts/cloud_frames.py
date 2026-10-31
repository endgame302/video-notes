"""Run frames.py on Kaggle instead of this machine, with no browser and no manual steps.

usage: cloud_frames.py <youtube-url | video-file> [--out DIR] [--keep-video] [--ocr MODE] [--gpu] [--branch NAME]

YouTube blocks downloads from cloud machines, so the video is downloaded HERE (1080p, video
only), uploaded to a private Kaggle dataset, processed by frames.py in a private Kaggle script,
and the resulting frames/ folder is downloaded to --out (default: ./frames, or frames/ next to a
local video file). A downloaded video is deleted afterwards unless --keep-video.

Default: --ocr hybrid on Kaggle's 4-core CPU machine (Tesseract for every frame, RapidOCR on the
talking-head review tiles, ~5 s a tile; measured best: Tom Scott 72% -> 90% of on-screen states).
--gpu runs on Kaggle's T4 instead, which has fewer CPU cores but reads tiles in under a second.
--ocr tesseract skips RapidOCR; --ocr rapidocr reads every frame with it (experimental: it broke
dedup on a coding screencast; use it with --gpu).

One-time setup:
  1. A Kaggle account with a verified phone number (needed for internet in scripts).
  2. pip install kaggle   and sign in once:  kaggle auth login
     (or put an API token from kaggle.com/settings/api in ~/.kaggle/access_token).
Then every run is one command. The same dataset and script slugs are reused each time
(vn-frames-input, vn-frames-runner), so nothing piles up in the account.
"""
import atexit, json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

REPO = "https://github.com/endgame302/video-notes.git"
DATASET_SLUG, KERNEL_SLUG = "vn-frames-input", "vn-frames-runner"

args = sys.argv[1:]
if not args or args[0].startswith("-"):
    sys.exit(__doc__)
def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default
def fail(msg):
    sys.exit(f"cloud_frames.py: {msg}")
source, keep_video = args[0], "--keep-video" in args
ocr_mode, branch = opt("--ocr", "hybrid"), opt("--branch", "main")
gpu = "--gpu" in args and ocr_mode != "tesseract"   # Tesseract alone gains nothing from the GPU
if ocr_mode not in ("tesseract", "hybrid", "rapidocr"):
    fail("--ocr must be tesseract, hybrid or rapidocr")
if ocr_mode == "rapidocr" and not gpu:
    print("note: --ocr rapidocr on the CPU takes about 5 s per frame", flush=True)

KAGGLE = shutil.which("kaggle")
if not KAGGLE:
    fail("the Kaggle CLI is missing: pip install kaggle, then run: kaggle auth login")

def kaggle(*a, check=True):
    p = subprocess.run([KAGGLE, *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and p.returncode:
        fail(f"kaggle {' '.join(a[:2])} failed: {(p.stderr or p.stdout).strip()[-400:]}")
    return p

# ---- who am I? (the slugs live under the signed-in account) ----
p = kaggle("config", "view", check=False)
m = re.search(r"username:\s*(\S+)", p.stdout)
user = m.group(1) if m and m.group(1) != "None" else None
if not user:
    fail("not signed in to Kaggle: run  kaggle auth login  once (or set KAGGLE_API_TOKEN)")
dataset, kernel = f"{user}/{DATASET_SLUG}", f"{user}/{KERNEL_SLUG}"
t0 = time.time()

# ---- 1. the video, downloaded here: YouTube blocks most cloud IPs ----
stage = Path(tempfile.mkdtemp(prefix="vn-cloud-"))
atexit.register(shutil.rmtree, stage, True)          # never leave a staged video behind, even on failure
data_dir = stage / "data"
data_dir.mkdir()
video = data_dir / "video.mp4"
if Path(source).is_file():
    try:
        os.link(source, video)                      # same drive: no extra disk space
    except OSError:
        if shutil.disk_usage(stage).free < Path(source).stat().st_size * 1.1 + 2e8:
            fail(f"not enough free space in {stage} to stage {source}")
        shutil.copy(source, video)
    out = Path(opt("--out", Path(source).parent / "frames"))
    keep_video = True          # never delete a file the user gave us
else:
    ytdlp = shutil.which("yt-dlp") or fail("yt-dlp not found")
    info = json.loads(subprocess.run([ytdlp, "-j", "-f", "bv*[height<=1080][vcodec^=avc1]/bv*[height<=1080]", source],
                                     capture_output=True, text=True).stdout or "{}")
    size = info.get("filesize") or info.get("filesize_approx") or 0
    if size and shutil.disk_usage(stage).free < size * 1.1 + 2e8:
        fail(f"needs ~{size / 1e9:.1f} GB free in {stage} for the download")
    print(f"downloading {info.get('title', source)} ({size / 1e6:.0f} MB) ...", flush=True)
    subprocess.run([ytdlp, "-q", "--no-warnings", "-f", "bv*[height<=1080][vcodec^=avc1]/bv*[height<=1080]",
                    "-o", str(video), source], check=True)
    out = Path(opt("--out", Path.cwd() / "frames"))

# ---- 2. upload as a private dataset (one slug, overwritten each run) ----
(data_dir / "dataset-metadata.json").write_text(json.dumps(
    {"title": DATASET_SLUG, "id": dataset, "licenses": [{"name": "unknown"}]}), encoding="utf-8")
print(f"uploading {video.stat().st_size / 1e6:.0f} MB to private dataset {dataset} ...", flush=True)
exists = kaggle("datasets", "status", dataset, check=False).returncode == 0
if exists:
    kaggle("datasets", "version", "-p", str(data_dir), "-m", f"video for {source}"[:90], "-d")
else:
    kaggle("datasets", "create", "-p", str(data_dir))
# Wait until THIS upload is live: "ready" alone can still describe the previous version, and a
# script started then finds no video at all. So also wait for video.mp4 at exactly our size.
want = video.stat().st_size
time.sleep(15)
for _ in range(180):
    st = kaggle("datasets", "status", dataset, check=False).stdout.strip().lower()
    if "error" in st:
        fail(f"dataset processing failed: {st}")
    files = kaggle("datasets", "files", dataset, check=False).stdout
    if "ready" in st and re.search(rf"video\.mp4\s+{want}\s", files):
        break
    time.sleep(10)
else:
    fail("the uploaded video still isn't live on Kaggle after 30 minutes")

# ---- 3. run frames.py in a private Kaggle script ----
kdir = stage / "kernel"
kdir.mkdir()
ocr_pkgs = ' "rapidocr" "onnxruntime"' if ocr_mode != "tesseract" else ""
(kdir / "run.py").write_text(f'''import glob, subprocess, sys
sh = lambda c: subprocess.run(c, shell=True, check=True)
sh("apt-get -qq update > /dev/null && apt-get -qq install -y tesseract-ocr > /dev/null")
sh('pip -q install imagehash "opencv-python>=4.8,<5"{ocr_pkgs}')
sh("git clone -q --depth 1 -b {branch} {REPO} /kaggle/temp/vn")
import time
for _ in range(30):                     # the dataset mount can lag a little behind the start
    found = sorted(glob.glob("/kaggle/input/**/video.mp4", recursive=True))
    if found:
        break
    time.sleep(10)
else:
    sh("find /kaggle/input -maxdepth 4 | head -50")
    raise SystemExit("no video.mp4 under /kaggle/input")
vid = found[0]
cmd = [sys.executable, "/kaggle/temp/vn/skills/video-notes/scripts/frames.py", vid, "--out", "/kaggle/working/frames"]
if "{ocr_mode}" != "tesseract":
    cmd += ["--ocr", "{ocr_mode}"]
subprocess.run(cmd, check=True)
''', encoding="utf-8")
(kdir / "kernel-metadata.json").write_text(json.dumps({
    "id": kernel, "title": KERNEL_SLUG, "code_file": "run.py", "language": "python", "kernel_type": "script",
    "is_private": "true", "enable_gpu": "true" if gpu else "false", "machine_shape": "NvidiaTeslaT4" if gpu else "",
    "enable_internet": "true", "dataset_sources": [dataset],
    "competition_sources": [], "kernel_sources": [], "model_sources": []}), encoding="utf-8")
print(f"running frames.py on Kaggle ({kernel}, {'T4 GPU' if gpu else 'CPU'}, ocr={ocr_mode}) ...", flush=True)
kaggle("kernels", "push", "-p", str(kdir))
time.sleep(20)
state = ""
for _ in range(1440):                                   # up to 12 h, Kaggle's own limit
    state = kaggle("kernels", "status", kernel, check=False).stdout.strip().lower()
    if any(s in state for s in ("complete", "error", "cancel")):
        break
    time.sleep(30)
print(f"Kaggle run finished: {state}", flush=True)

# ---- 4. fetch the frames/ folder ----
fetched = stage / "output"
kaggle("kernels", "output", kernel, "-p", str(fetched), "-o", check=False)
manifest = next(fetched.rglob("frames.json"), None)
if not manifest:
    logs = sorted(fetched.glob("*.log"))
    tail = logs[0].read_text(encoding="utf-8", errors="replace")[-1500:] if logs else "(no log)"
    fail(f"no frames.json came back (status: {state}). Kaggle log tail:\n{tail}")
if out.exists():
    shutil.rmtree(out)
shutil.copytree(manifest.parent, out)
if keep_video and not Path(source).is_file():          # a URL download the user wants to keep
    shutil.move(str(video), out.parent / "video.mp4")
shutil.rmtree(stage, ignore_errors=True)            # the staged copy; a file the user gave stays put
m = json.loads((out / "frames.json").read_text(encoding="utf-8"))
print(json.dumps({"out": str(out), "kept": len(m["kept"]), "counts": m["counts"], "secs_on_kaggle": m["secs"],
                  "total_minutes": round((time.time() - t0) / 60, 1), "warnings": m["warnings"]}))
