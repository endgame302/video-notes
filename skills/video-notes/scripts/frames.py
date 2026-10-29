"""Screenshot candidates for video-notes, step 4: one frame per second, OCR, talking-head
drop, dedup, and a manifest that accounts for every frame.

usage: frames.py <video> [--out DIR] [--per-frame-ocr] [--keep-all] [--ocr tesseract|rapidocr|hybrid]

Writes into DIR (default: <video dir>/frames):
  t0000123.0.jpg ...   kept frames, named by their real time in seconds
  kept_000.jpg ...     contact sheets of the kept frames, with timestamps
  heads_000.jpg ...    contact sheets of DROPPED talking-head frames: glance at these, since an
                       overlay that OCR can't read (logo, stylised title) is dropped with the heads
  frames.json          manifest: every sampled frame's time, outcome and reason, the kept list
                       with OCR words, head-only stretches with no screenshot, timings, warnings
Exits non-zero (and says why) if frames go missing or the outcome counts don't balance.

Works on Windows, macOS and Linux. Needs ffmpeg/ffprobe and Tesseract (on PATH, or $TESSERACT),
and the packages in ../requirements.txt; check_deps.py (next to this file) checks all of it.

Measured on four hand-labelled videos (see ../references/frames.md, and bench/ in the repository,
https://github.com/endgame302/video-notes). The head-rule thresholds below were tuned on two
talking-head videos only; re-score with bench/score.py before changing them.
"""
import json, os, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import imagehash
import numpy as np
from PIL import Image

# $TESSERACT, else tesseract on PATH, else the default Windows install location
TESS = (os.environ.get("TESSERACT") or shutil.which("tesseract")
        or r"C:\Program Files\Tesseract-OCR\tesseract.exe")
if not Path(TESS).exists() and not shutil.which(TESS):
    sys.exit("frames.py: Tesseract not found; install it or set TESSERACT to its path")
CASCADE = Path(cv2.data.haarcascades if hasattr(cv2, "data") else ".") / "haarcascade_frontalface_default.xml"
if not hasattr(cv2, "CascadeClassifier"):
    sys.exit(f"frames.py: OpenCV {cv2.__version__} has no face detector (OpenCV 5 removed it); "
             'pip install "opencv-python<5"')
if not CASCADE.is_file():
    sys.exit("frames.py: OpenCV's face model is missing (some distro OpenCV packages omit it); "
             'pip install "opencv-python<5"')
TESS_ENV = {**os.environ, "OMP_THREAD_LIMIT": "1"}   # parallel processes; no inner threading
PROCS = max(1, min(6, os.cpu_count() or 1))
# popcount of uint64 hash differences; np.bitwise_count needs numpy 2, so fall back to a table
if hasattr(np, "bitwise_count"):
    popcount = np.bitwise_count
else:
    _BITS = np.array([bin(i).count("1") for i in range(256)], np.uint8)
    popcount = lambda a: _BITS[a.view(np.uint8)].reshape(*a.shape, 8).sum(-1)
PIX = 20             # grey-level change that counts as "changed"
FACE_MIN = 0.015     # face box area / frame area for a frame to count as showing the host
HEAD_WORDS = 8       # a head frame with this many OCR words is kept regardless
TILE_W, COLS, ROWS = 384, 6, 5

args = sys.argv[1:]
if not args or args[0].startswith("-"):
    sys.exit(__doc__)
vid = Path(args[0])
if not vid.is_file():
    sys.exit(f"frames.py: no such video: {vid}")
out = Path(args[args.index("--out") + 1]) if "--out" in args else vid.parent / "frames"
per_frame_ocr = "--per-frame-ocr" in args
keep_all = "--keep-all" in args
# experimental: tesseract (default) | rapidocr (deep-learning OCR for every frame; needs a GPU to
# be quick) | hybrid (Tesseract, plus RapidOCR on the head review tiles to rescue overlays)
ocr_mode = args[args.index("--ocr") + 1] if "--ocr" in args else "tesseract"
if ocr_mode not in ("tesseract", "rapidocr", "hybrid"):
    sys.exit("frames.py: --ocr must be tesseract, rapidocr or hybrid")
out.mkdir(parents=True, exist_ok=True)
for f in list(out.glob("f_*.jpg")) + list(out.glob("t*.jpg")) + list(out.glob("*_[0-9][0-9][0-9].jpg")):
    f.unlink()
warnings, secs = [], {}
t0 = time.time()

def fail(msg):
    sys.exit(f"frames.py: {msg}")

# ---- 0. probe, and check there is room for every sampled frame ----
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                "stream=avg_frame_rate,width,height:format=duration", "-of", "json", str(vid)],
                               capture_output=True, text=True, encoding="utf-8", errors="replace").stdout or "{}")
if not pr.get("streams") or "format" not in pr:
    fail(f"ffprobe found no video stream in {vid}")
st = pr["streams"][0]
num, den = (int(x) for x in st["avg_frame_rate"].split("/"))
fps, width, height = num / den, st["width"], st["height"]
duration = float(pr["format"]["duration"])
step = max(1, round(fps))
interval = step / fps
if height < 1000:
    warnings.append(f"{width}x{height}: below 1080p. Text on pages shown behind the host is unreadable "
                    f"at reduced size, so those frames get dropped as talking heads; download 1080p.")
# ~210 KB per 1080p frame at -q:v 2 (measured), scaled by pixel count, plus margin
need = duration / interval * 0.21e6 * (width * height) / (1920 * 1080) * 1.2 + 0.5e9
free = shutil.disk_usage(out).free
if free < need:
    fail(f"needs ~{need / 1e9:.1f} GB free in {out} for {duration / interval:.0f} frames, has {free / 1e9:.1f} GB")

# ---- 1. decode one frame per second at full resolution, with each frame's real time ----
def decode(hw):
    p = subprocess.run(["ffmpeg", "-hide_banner", "-y"] + hw + ["-i", str(vid), "-vf",
                        f"select='not(mod(n,{step}))',showinfo", "-fps_mode", "passthrough", "-q:v", "2",
                        str(out / "f_%06d.jpg")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p, [float(m) for m in re.findall(r"pts_time:([\d.]+)", p.stderr)], sorted(out.glob("f_*.jpg"))

# CUDA first (fastest where present), then whatever GPU decoder ffmpeg finds (VideoToolbox on
# macOS, VA-API on Linux, D3D11 on Windows), then the CPU
for hw in (["-hwaccel", "cuda"], ["-hwaccel", "auto"], []):
    p, pts, files = decode(hw)
    if p.returncode == 0 and files and len(files) == len(pts):
        break
    for f in files:
        f.unlink()
if not hw:
    warnings.append("GPU decode unavailable; decoded on the CPU")
if p.returncode or not files:
    fail("ffmpeg could not decode the video: " + p.stderr[-300:])
if len(files) != len(pts):
    fail(f"{len(files)} frames written but {len(pts)} timestamps reported")
gaps = [(a, b) for a, b in zip(pts, pts[1:]) if b - a > 2 * interval]
if gaps:
    fail(f"decode skipped frames: {len(gaps)} gaps, first {gaps[0][0]:.1f}-{gaps[0][1]:.1f} s")
if (len(pts) - 1) * interval < duration - 3 * interval:
    fail(f"decode stopped early at {pts[-1]:.1f} s of {duration:.1f} s")
N = len(files)
T = [round(t, 2) for t in pts]
secs["decode"] = round(time.time() - t0, 1)

# ---- 2. skip frames identical to the last inspected one (a held slide is OCR'd once) ----
# Compared against the last INSPECTED frame, so a slow build still accumulates into a change.
t1 = time.time()
same, last, last_th = {}, None, None
for j, f in enumerate(files):
    th = cv2.imread(str(f), cv2.IMREAD_REDUCED_GRAYSCALE_4)
    if last_th is not None and th.shape == last_th.shape:
        d = cv2.absdiff(th, last_th) > PIX
        h6, w8 = d.shape[0] // 6, d.shape[1] // 8
        if d.mean() < 0.002 and d[:6 * h6, :8 * w8].reshape(6, h6, 8, w8).mean(axis=(1, 3)).max() < 0.01:
            same[j] = last
            continue
    last, last_th = j, th
todo = [j for j in range(N) if j not in same]

_tl = threading.local()
def look(j):
    # one classifier per thread: a CascadeClassifier shared across threads returns wrong boxes
    if not hasattr(_tl, "cc"):
        _tl.cc = cv2.CascadeClassifier(str(CASCADE))
    img = cv2.imread(str(files[j]), cv2.IMREAD_GRAYSCALE)
    small = cv2.resize(img, (640, 360))
    faces = _tl.cc.detectMultiScale(small, 1.2, 5, minSize=(24, 24))
    h = imagehash.phash(Image.fromarray(img))
    return max((w * h_ for *_, w, h_ in faces), default=0) / (640 * 360), h.hash.flatten()

with ThreadPoolExecutor(PROCS) as ex:
    looks = dict(zip(todo, ex.map(look, todo)))
face = {j: looks[j][0] for j in todo}
bits = {j: looks[j][1] for j in todo}
secs["skip_face_hash"] = round(time.time() - t1, 1)

# ---- 3. OCR every inspected frame at full resolution ----
# Batched: a few Tesseract processes each read a list of images, so start-up and model load are
# paid once per batch (OCR step 21-42% faster; identical outcomes to per-frame on all 2,649
# frames of the four test videos).
t2 = time.time()
grab_words = lambda s: set(re.findall(r"[a-z]{3,}", s.lower()))
def ocr_one(j):
    p = subprocess.run([TESS, str(files[j]), "stdout", "--psm", "3"], capture_output=True, text=True,
                       encoding="utf-8", errors="ignore", env=TESS_ENV)
    return j, grab_words(p.stdout)

fallbacks = 0
def ocr_chunk(ci, chunk):
    global fallbacks
    lst = out / f"ocr_list_{ci}.txt"
    lst.write_text("\n".join(str(files[j].resolve()) for j in chunk), encoding="utf-8")
    p = subprocess.run([TESS, str(lst), "stdout", "--psm", "3", "tsv"], capture_output=True, text=True,
                       encoding="utf-8", errors="ignore", env=TESS_ENV)
    found, pages = {j: set() for j in chunk}, set()
    for row in p.stdout.splitlines()[1:]:
        col = row.split("\t")
        if len(col) != 12:
            continue
        pages.add(int(col[1]))
        if col[0] == "5":
            found[chunk[int(col[1]) - 1]] |= grab_words(col[11])
    # an unreadable image stops Tesseract there, and every later frame would silently get no
    # words (and look like a talking head): check the exit code and page count, else redo singly
    if p.returncode or pages != set(range(1, len(chunk) + 1)):
        fallbacks += 1
        found = dict(map(ocr_one, chunk))
    return found

rapid, rapid_device = None, None
def rapid_engine():
    """RapidOCR on the best device here: CUDA through PyTorch (e.g. Colab), DirectML on Windows,
    else CPU. RapidOCR's docs advise against its onnxruntime-gpu path, so CUDA goes through torch."""
    global rapid, rapid_device
    if rapid is not None:
        return rapid
    try:
        from rapidocr import RapidOCR
    except ImportError:
        fail("--ocr rapidocr/hybrid needs RapidOCR: pip install rapidocr onnxruntime")
    try:
        import torch
        if torch.cuda.is_available():
            from rapidocr import EngineType
            p = {f"{k}.engine_type": EngineType.TORCH for k in ("Det", "Cls", "Rec")}
            p["EngineConfig.torch.use_cuda"] = True
            rapid, rapid_device = RapidOCR(params=p), "torch-cuda:" + torch.cuda.get_device_name(0)
            return rapid
    except ImportError:
        pass
    try:
        import onnxruntime as ort
        if "DmlExecutionProvider" in ort.get_available_providers():
            rapid, rapid_device = RapidOCR(params={"EngineConfig.onnxruntime.use_dml": True}), "onnx-directml"
            return rapid
    except ImportError:
        pass
    rapid, rapid_device = RapidOCR(), "onnx-cpu"
    warnings.append("RapidOCR is running on the CPU: about 5 s per frame")
    return rapid

def rapid_text(j):
    r = rapid_engine()(str(files[j]), use_cls=False)
    return " ".join(r.txts or [])

words = {}
if ocr_mode == "rapidocr":
    for j in todo:
        words[j] = grab_words(rapid_text(j))
elif per_frame_ocr:
    with ThreadPoolExecutor(PROCS) as ex:
        words = dict(ex.map(ocr_one, todo))
else:
    chunks = [todo[i:i + 40] for i in range(0, len(todo), 40)]
    with ThreadPoolExecutor(PROCS) as ex:
        for r in ex.map(ocr_chunk, range(len(chunks)), chunks):
            words.update(r)
    for f in out.glob("ocr_list_*.txt"):
        f.unlink()
if fallbacks:
    warnings.append(f"{fallbacks} OCR batches failed and were redone frame by frame")
secs["ocr"] = round(time.time() - t2, 1)

# ---- 4. talking-head drop ----
# A face frame that looks like frames >30 s away is the host's recurring shot. It is dropped
# when it has little text AND that text doesn't persist: OCR noise on a face changes frame to
# frame, a caption or a page behind the host repeats (Bookfox captions read 6-9 words, a zoomed
# Twitter header in Tom Scott 3, so a word count alone drops them).
t3 = time.time()
cand = [j for j in todo if face[j] > FACE_MIN]
recur = {}
if cand:
    B = np.packbits(np.array([bits[j] for j in cand]), axis=1).view(np.uint64).ravel()
    tc = np.array([T[j] for j in cand])
    for i, j in enumerate(cand):
        dist = popcount(B ^ B[i])
        recur[j] = int(((dist <= 14) & (np.abs(tc - T[j]) > 30)).sum())
gate = [j for j in cand if recur[j] >= 2]

def words_at(o):
    return words[same.get(o, o)]
def persists(j):
    return any(len(words[j] & words_at(o)) >= 2
               for o in range(max(0, j - 4), min(N, j + 5)) if o != j and abs(T[o] - T[j]) <= 2.5)
head = {j for j in gate if len(words[j]) < HEAD_WORDS and not persists(j)}

# ---- 5. dedup what's left: text overlap for text frames, pHash for the rest ----
def ham(a, b):
    return int(np.count_nonzero(bits[a] != bits[b]))
fate, kept = {}, []
for j in range(N):
    if j in same:
        fate[j] = f"unchanged-from {T[same[j]]}"
        continue
    if j in head:
        fate[j] = "head"
        continue
    ws, dup = words[j], None
    for i, o in enumerate(kept):
        wo = words[o]
        if len(ws) >= 6 and len(wo) >= 6:
            if i == len(kept) - 1 and len(wo - ws) <= 0.1 * len(wo):   # builds on the previous frame
                fate[o] = f"superseded by {T[j]}"
                kept[i] = j
                dup = "superseded"
                break
            if len(ws & wo) / len(ws | wo) > 0.85:
                dup = f"text dup of {T[o]}"
                break
        elif len(ws) < 6 and len(wo) < 6 and ham(j, o) <= 6:
            dup = f"phash dup of {T[o]}"
            break
    if dup is None:
        kept.append(j)
        fate[j] = "kept"
    elif dup != "superseded":
        fate[j] = dup
    else:
        fate[j] = "kept"
kept.sort()

# ---- 6. head review tiles: each new look of the host shot, plus frames that jump visibly from
# the second before (an overlay appearing). Grows with distinct looks, not with video length.
# Tom Scott: 77 tiles from 506 head frames, all 5 OCR-unreadable overlays among them.
tiles = []
for j in sorted(head):
    near = min((ham(j, o) for o in tiles), default=99)
    prev = j - 1 if j > 0 else None
    jump = prev is not None and ham(j, same.get(prev, prev)) > 8
    if near > 10 or (jump and near > 6):
        tiles.append(j)

# hybrid: read the review tiles with RapidOCR, which reads stylised overlays Tesseract can't.
# A tile with 2+ tokens (letters or digits, 2+ characters: "200 OK", "Web 2.0") is kept.
rescued = []
if ocr_mode == "hybrid" and tiles:
    t4 = time.time()
    for j in tiles:
        txt = rapid_text(j)
        if len(re.findall(r"[a-z0-9][a-z0-9.]+", txt.lower())) >= 2:
            rescued.append(j)
            words[j] = words[j] | grab_words(txt)
    for j in rescued:
        head.discard(j)
        tiles.remove(j)
        fate[j] = "kept (rescued by rapidocr)"
        kept.append(j)
    kept.sort()
    secs["rescue"] = round(time.time() - t4, 1)

# stretches with no screenshot: consecutive head frames (an unchanged copy of a head counts)
eff_head = [j in head or same.get(j) in head for j in range(N)]
stretches, s = [], None
for j in range(N + 1):
    if j < N and eff_head[j]:
        s = j if s is None else s
    elif s is not None:
        a, b = T[s], T[j - 1] + interval
        if b - a >= 5:
            stretches.append({"start": a, "end": round(b, 2), "reason": "talking head",
                              "review_tiles": [T[t] for t in tiles if s <= t < j]})
        s = None
secs["filter"] = round(time.time() - t3, 1)

# ---- 7. contact sheets, then delete every frame not kept ----
def sheets(idx, prefix):
    names, per = [], COLS * ROWS
    for n0 in range(0, len(idx), per):
        cells = []
        for j in idx[n0:n0 + per]:
            img = cv2.imread(str(files[j]))
            img = cv2.resize(img, (TILE_W, TILE_W * img.shape[0] // img.shape[1]))
            m, sec = divmod(int(T[j]), 60)
            cv2.rectangle(img, (0, 0), (110, 26), (0, 0, 0), -1)
            cv2.putText(img, f"{m}:{sec:02d} ({T[j]:.0f}s)" if m < 60 else f"{T[j]:.0f}s", (4, 19),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cells.append(img)
        blank = np.zeros_like(cells[0])
        cells += [blank] * (per - len(cells))
        rows = [np.hstack(cells[r * COLS:(r + 1) * COLS]) for r in range(ROWS)]
        rows = [r for r in rows if r.any()] or rows[:1]
        name = f"{prefix}_{n0 // per:03d}.jpg"
        cv2.imwrite(str(out / name), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
        names.append(name)
    return names

kept_sheets, head_sheets = sheets(kept, "kept"), sheets(tiles, "heads")
kept_files = {}
for j in kept:
    name = f"t{T[j]:07.1f}.jpg"
    files[j].replace(out / name) if not keep_all else shutil.copy(files[j], out / name)
    kept_files[j] = name
if not keep_all:
    for j, f in enumerate(files):
        if j not in kept_files:
            f.unlink(missing_ok=True)
secs["total"] = round(time.time() - t0, 1)

# ---- contract: every sampled frame has exactly one outcome, and the counts balance ----
outcome = {j: fate[j].split(" ")[0] for j in range(N)}
counts = {k: sum(v == k for v in outcome.values()) for k in sorted(set(outcome.values()))}
if len(fate) != N or sum(counts.values()) != N or counts.get("kept", 0) != len(kept):
    fail(f"outcome counts don't balance: {counts}, {N} frames, {len(kept)} kept")

manifest = {
    "video": str(vid), "duration": round(duration, 2), "fps": round(fps, 3), "size": [width, height],
    "interval": round(interval, 4), "sampled": N,
    "kept": [{"t": T[j], "file": kept_files[j], "words": sorted(words[j])} for j in kept],
    "kept_sheets": kept_sheets,
    "head_review": {"sheets": head_sheets, "tiles": [T[j] for j in tiles], "dropped": len(head)},
    "no_screenshot": stretches,
    "counts": counts,
    "frames": {T[j]: {"outcome": fate[j], **({"words": len(words[j]), "face": round(face[j], 4)}
                                             if j in words else {})} for j in range(N)},
    # per gated frame: OCR words, face area, matching shots >30 s away (tune the head rule offline)
    "gate": {T[j]: [sorted(words[j]), round(face[j], 4), recur[j]] for j in gate},
    "ocr": {"engine": ocr_mode, "device": rapid_device,
            "mode": "rapidocr" if ocr_mode == "rapidocr" else ("per-frame" if per_frame_ocr else "batched"),
            "frames": len(todo), "failed_batches": fallbacks, "rescued": [T[j] for j in rescued]},
    "secs": secs, "warnings": warnings,
}
(out / "frames.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
print(json.dumps({"sampled": N, "kept": len(kept), "counts": counts, "head_tiles": len(tiles),
                  "ocr": ocr_mode, "device": rapid_device, "rescued": len(rescued),
                  "no_screenshot_stretches": len(stretches), "secs": secs, "warnings": warnings}))
