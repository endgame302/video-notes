"""Check that this machine can run the video-notes skill, and say how to fix what's missing.

usage: check_deps.py [--json]

Checks Python, the Python packages in ../requirements.txt, ffmpeg/ffprobe, Tesseract with English
data, and yt-dlp, then prints install commands for this OS (Windows, macOS, or a Linux family).
Exits 0 when everything required is present, 1 otherwise. --json prints the result for agents.
"""
import importlib, json, os, platform, re, shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQS = HERE.parent / "requirements.txt"
results = []   # (name, ok, required, detail)

def add(name, ok, detail, required=True):
    results.append({"name": name, "ok": bool(ok), "required": required, "detail": detail})

def run(cmd):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=30)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except (OSError, subprocess.TimeoutExpired) as e:
        return -1, str(e)

# ---- Python and packages ----
add("python>=3.10", sys.version_info >= (3, 10), platform.python_version())
for mod, label, need in (("numpy", "numpy>=2.0", "2.0"), ("cv2", "opencv-python", None),
                         ("imagehash", "ImageHash", None), ("PIL", "Pillow", None)):
    try:
        m = importlib.import_module(mod)
        ver = getattr(m, "__version__", "?")
        ok = True
        if need:
            ok = tuple(int(x) for x in re.findall(r"\d+", ver)[:2]) >= tuple(int(x) for x in need.split("."))
        detail = ver
        if mod == "cv2":
            cascade = Path(getattr(getattr(m, "data", None), "haarcascades", ".")) / "haarcascade_frontalface_default.xml"
            if not hasattr(m, "CascadeClassifier"):
                ok, detail = False, f"{ver}: OpenCV 5 removed the face detector; pip install \"opencv-python<5\""
            elif not cascade.is_file():
                ok, detail = False, f"{ver}, but its face model is missing (use pip's opencv-python, not a distro build)"
        add(label, ok, detail)
    except ImportError:
        add(label, False, "not installed")
try:
    importlib.import_module("markdown")
    add("Markdown", True, "installed", required=False)
except ImportError:
    add("Markdown", False, "not installed (only for assets/example-page/build_page.py)", required=False)
try:
    importlib.import_module("faster_whisper")
    add("faster-whisper", True, "installed", required=False)
except ImportError:
    add("faster-whisper", False, "not installed (only for --audio)", required=False)

# ---- command-line tools ----
for tool in ("ffmpeg", "ffprobe"):
    path = shutil.which(tool)
    code, outp = run([tool, "-version"]) if path else (-1, "")
    add(tool, code == 0, outp.splitlines()[0][:70] if code == 0 else "not found on PATH")
if shutil.which("ffmpeg"):
    _, hw = run(["ffmpeg", "-hide_banner", "-hwaccels"])
    accels = [l.strip() for l in hw.splitlines()[1:] if l.strip()]
    add("GPU decoding", bool(accels), ", ".join(accels) or "none (CPU decoding works, slower)", required=False)

tess = os.environ.get("TESSERACT") or shutil.which("tesseract")
if not tess and platform.system() == "Windows":
    default = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
    tess = str(default) if default.exists() else None
if tess:
    code, outp = run([tess, "--version"])
    _, langs = run([tess, "--list-langs"])
    has_eng = "eng" in langs.split()
    major = re.search(r"tesseract v?(\d+)", outp, re.I)
    ok = code == 0 and has_eng and major and int(major.group(1)) >= 4
    detail = (outp.splitlines()[0] if outp else "?") + ("" if has_eng else ", but no English data (eng)")
    add("tesseract", ok, detail)
else:
    add("tesseract", False, "not found on PATH (or set TESSERACT to its path)")

ytdlp = shutil.which("yt-dlp")
code, outp = run([ytdlp, "--version"]) if ytdlp else (-1, "")
add("yt-dlp", code == 0, outp.strip()[:30] if code == 0 else "not found on PATH")

# ---- install hints for this OS ----
def os_family():
    s = platform.system()
    if s == "Windows":
        return "windows"
    if s == "Darwin":
        return "macos"
    if s == "Linux":
        info = {}
        try:
            for line in Path("/etc/os-release").read_text().splitlines():
                k, _, v = line.partition("=")
                info[k] = v.strip('"').lower()
        except OSError:
            pass
        ids = (info.get("ID", "") + " " + info.get("ID_LIKE", "")).split()
        for fam, keys in (("debian", ("debian", "ubuntu")), ("fedora", ("fedora", "rhel", "centos")),
                          ("arch", ("arch",)), ("suse", ("suse", "opensuse"))):
            if any(k in ids for k in keys):
                return fam
        return "linux"
    return s.lower() or "unknown"

HINTS = {
    "windows": {
        "ffmpeg": "winget install --id Gyan.FFmpeg -e",
        "tesseract": "winget install --id UB-Mannheim.TesseractOCR -e   (installs to C:\\Program Files\\Tesseract-OCR, found automatically)",
        "yt-dlp": "winget install --id yt-dlp.yt-dlp -e",
    },
    "macos": {
        "ffmpeg": "brew install ffmpeg",
        "tesseract": "brew install tesseract",
        "yt-dlp": "brew install yt-dlp",
    },
    "debian": {
        "ffmpeg": "sudo apt install ffmpeg",
        "tesseract": "sudo apt install tesseract-ocr tesseract-ocr-eng",
        "yt-dlp": "python3 -m pip install --user -U yt-dlp   (the apt package is often too old for YouTube)",
    },
    "fedora": {
        "ffmpeg": "enable RPM Fusion, then: sudo dnf install ffmpeg   (Fedora's ffmpeg-free may lack H.264)",
        "tesseract": "sudo dnf install tesseract tesseract-langpack-eng",
        "yt-dlp": "sudo dnf install yt-dlp   (or python3 -m pip install --user -U yt-dlp)",
    },
    "arch": {
        "ffmpeg": "sudo pacman -S ffmpeg",
        "tesseract": "sudo pacman -S tesseract tesseract-data-eng",
        "yt-dlp": "sudo pacman -S yt-dlp",
    },
    "suse": {
        "ffmpeg": "sudo zypper install ffmpeg   (full codecs need the Packman repository)",
        "tesseract": "sudo zypper install tesseract-ocr tesseract-ocr-traineddata-english",
        "yt-dlp": "sudo zypper install yt-dlp   (or python3 -m pip install --user -U yt-dlp)",
    },
}
fam = os_family()
hints = HINTS.get(fam, {"ffmpeg": "install ffmpeg (https://ffmpeg.org/download.html)",
                        "tesseract": "install Tesseract 5 with English data (https://tesseract-ocr.github.io/tessdoc/Installation.html)",
                        "yt-dlp": "python3 -m pip install --user -U yt-dlp"})
pip_cmd = f'"{sys.executable}" -m pip install -r "{REQS}"'
fixes = []
for r in results:
    if r["ok"] or not r["required"]:
        continue
    key = "ffmpeg" if r["name"] in ("ffmpeg", "ffprobe") else r["name"]
    if key in hints:
        fixes.append(hints[key])
    elif r["name"] == "python>=3.10":
        fixes.append("install Python 3.10 or newer (https://www.python.org/downloads/)")
    elif pip_cmd not in fixes:
        fixes.append(pip_cmd)
fixes = list(dict.fromkeys(fixes))
ok = all(r["ok"] for r in results if r["required"])

if "--json" in sys.argv:
    print(json.dumps({"ok": ok, "os": fam, "checks": results, "fix": fixes}, indent=1))
else:
    print(f"video-notes dependency check ({platform.system()} {platform.release()}, {fam})\n")
    for r in results:
        mark = "ok " if r["ok"] else ("MISSING" if r["required"] else "-  ")
        print(f"  {mark:8s} {r['name']:16s} {r['detail']}")
    if fixes:
        print("\nTo fix:")
        for f in fixes:
            print(f"  {f}")
    print("\nAll required tools present." if ok else "\nSome required tools are missing.")
sys.exit(0 if ok else 1)
