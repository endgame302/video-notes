"""Score frames.py output against the hand labels in bench/labels/.

usage: score.py <work_dir> [<video_id> ...] [--manifest REL]

<work_dir>/<id>/video.mp4 is a downloaded test video and <work_dir>/<id>/frames/frames.json its
frames.py manifest (pass --manifest to score another file relative to <work_dir>/<id>/, e.g. a
run made with --out). With no ids, every labelled video found in <work_dir> is scored.

Each label is one on-screen state (a slide, a page, an overlay) with a start and end time.
A state counts as covered when any kept frame falls inside it, within TOL seconds.
Times are contact-sheet seconds unless the label has "real_time": true. A 1-fps tile numbered
k shows real time k + 0.5, so a state seen on tiles s..e is on screen during real [s, e + 1].
"""
import json, sys
from pathlib import Path

TOL = 0.25
LABELS = Path(__file__).parent / "labels"

args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
manifest = "frames/frames.json"
if "--manifest" in args:
    i = args.index("--manifest")
    manifest = args[i + 1]
    del args[i:i + 2]
work, ids = Path(args[0]), args[1:] or sorted(p.stem for p in LABELS.glob("*.json"))

def hit(s, t):
    end = s["end"] if s.get("real_time") else s["end"] + 1
    return s["start"] - TOL <= t <= end + TOL

total_cov = total = 0
for vid in ids:
    m = work / vid / manifest
    if not m.exists():
        print(f"{vid:12s} no manifest at {m}")
        continue
    labels = json.loads((LABELS / f"{vid}.json").read_text(encoding="utf-8"))
    kept = json.loads(m.read_text(encoding="utf-8"))["kept"]
    times = [x["t"] if isinstance(x, dict) else x for x in kept]
    covered = [s for s in labels if any(hit(s, t) for t in times)]
    useful = [t for t in times if any(hit(s, t) for s in labels)]
    short = [s for s in labels if s["end"] - s["start"] <= 2]
    total_cov, total = total_cov + len(covered), total + len(labels)
    print(f"{vid:12s} coverage {len(covered):3d}/{len(labels):3d} = {100 * len(covered) / len(labels):3.0f}%"
          f"  short {sum(s in covered for s in short):2d}/{len(short):2d}  review {len(times):4d}"
          f"  off-target {len(times) - len(useful):3d}"
          f"  missed: {' '.join(str(s['id']) for s in labels if s not in covered)}")
if total:
    print(f"{'all':12s} coverage {total_cov:3d}/{total:3d} = {100 * total_cov / total:3.0f}%")
