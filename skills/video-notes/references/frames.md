# `frames.py` reference

Screenshot candidates for step 4 of the skill. One frame per second, OCR, talking-head drop,
dedup, review sheets, and a manifest that accounts for every frame.

```
python3 scripts/frames.py <video> [--out DIR] [--per-frame-ocr] [--keep-all]
```

Paths are relative to the skill folder. The benchmark figures below come from `bench/` in the
repository (https://github.com/endgame302/video-notes), which isn't installed with the skill.

| Option | Effect |
| --- | --- |
| `--out DIR` | write here instead of `<video dir>/frames` |
| `--per-frame-ocr` | one Tesseract process per frame instead of batches (slower, identical results; for checking) |
| `--keep-all` | keep every sampled frame on disk (debugging; uses the full ≈210 KB per frame) |

Environment: `TESSERACT` overrides where Tesseract is found (else `PATH`, else
`C:\Program Files\Tesseract-OCR\tesseract.exe`).

## Outputs

| File | Contents |
| --- | --- |
| `t0000123.0.jpg` | each kept frame, full resolution, named by its real time in seconds |
| `kept_000.jpg` … | contact sheets of the kept frames (6 × 5 tiles, stamped `m:ss (s)`) |
| `heads_000.jpg` … | contact sheets of **dropped** talking-head frames, one tile per distinct look |
| `frames.json` | the manifest (below) |

Every other sampled frame is deleted at the end unless `--keep-all` is given.

### `frames.json`

| Field | Meaning |
| --- | --- |
| `video`, `duration`, `fps`, `size`, `interval`, `sampled` | the input, and how many frames were sampled at what spacing |
| `kept[]` | `{t, file, words}` for each kept frame; `words` is the OCR word set (3+ letters, lower case), good for picking frames, not for quoting |
| `kept_sheets` | the `kept_*.jpg` file names |
| `head_review` | `sheets`, the `tiles` (times) shown on them, and how many frames were `dropped` as heads |
| `no_screenshot[]` | `{start, end, reason, review_tiles}`: stretches of 5 s or more that are talking head only |
| `counts` | frames per outcome; they always sum to `sampled` |
| `frames{t}` | every sampled frame: `outcome`, plus `words` (count) and `face` (area) if it was inspected |
| `gate{t}` | for each frame the head rule looked at: `[words, face area, matching shots > 30 s away]`, for tuning offline |
| `ocr` | `mode`, frames OCR'd, `failed_batches` |
| `secs` | time per stage |
| `warnings` | e.g. below 1080p, GPU decode failed, OCR batches redone |

Outcomes, one per sampled frame:

| Outcome | Meaning |
| --- | --- |
| `kept` | a screenshot candidate |
| `unchanged-from T` | identical to the frame at T, not inspected |
| `head` | the presenter's recurring shot with no lasting text |
| `superseded by T` | text that the next kept frame builds on (a slide mid-build) |
| `text dup of T` | the same text as a kept frame |
| `phash dup of T` | looks the same as a kept frame (little or no text) |

## How it decides

### 1. Sample one frame per second, at full resolution

ffmpeg decodes the whole video once (on the GPU when it can) and keeps every
`round(fps)`-th frame, recording each frame's presentation time from `showinfo`. Times come
from the decoder, so a frame is never "seeked to" and can't land seconds away from where it was
asked for. Errors stop the run: frame and timestamp counts differ, a gap over 2 intervals,
or decoding ending more than 3 intervals before the end.

*Why not scene detection?* Screen recordings change by scrolling and typing, which aren't scene
cuts; the earlier method of scene detection plus a frame every 15 s caught 7–41% of states.
*Why not segment-and-pick?* A smarter segmenter (v2) caught 48–97% but missed short overlays;
sampling every second and deduplicating afterwards caught more on every video.

### 2. Skip frames that haven't changed

Each frame is compared at quarter size with the last frame that was **inspected** (not the
previous frame, so a slow build still adds up to a change). Under 0.2% of pixels changed and no
cell of an 8 × 6 grid over 1% means unchanged.

### 3. Face and look

Each inspected frame gets a frontal-face detection (OpenCV Haar cascade at 640 × 360) and a
64-bit perceptual hash. Each worker thread has its own detector: one detector shared across
threads returned wrong boxes for about 60% of frames, which made results differ between runs.

### 4. OCR at full resolution, in batches

Tesseract (`--psm 3`) reads every inspected frame. Six processes each take a list of 40
images and return TSV, so start-up and model load are paid once per batch: 21–42% faster than
one process per frame, with identical outcomes on all 2,649 test frames. If Tesseract exits
with an error or returns the wrong number of pages (an unreadable image stops it, and every
later frame in the batch would silently get no words), that batch is redone frame by frame.

*Why full resolution?* Pages shown behind a presenter have small text. Downscaled to 960, 1280
or 1440 px wide, some of them read as zero words and are dropped as talking heads.

### 5. Talking-head drop

A frame is a **head candidate** when its largest face covers more than 1.5% of the frame and
it looks like (hash distance ≤ 14) at least two other face frames more than 30 s away: the
host's shot comes back, a portrait on a slide doesn't. A candidate is **dropped** only if

- it has fewer than 8 OCR words, **and**
- its text doesn't persist: no frame within 2.5 s shares 2 or more of its words.

OCR noise on a face changes from frame to frame; a caption or a page behind the presenter
repeats. A word count alone dropped real captions (6–9 words on Bookfox) and a zoomed Twitter
header (3 words on Tom Scott).

### 6. Deduplicate

In time order, each remaining frame is compared with the frames kept so far:

- both have 6+ words: if the newest kept frame's words are almost all (≥ 90%) in this frame,
  this frame **supersedes** it (a build finishing); else word overlap (Jaccard) over 0.85 is a
  **text dup**;
- both have under 6 words: hash distance ≤ 6 is a **phash dup**.

### 7. Review tiles and no-screenshot stretches

From the dropped head frames, a tile is shown when the frame looks unlike every tile so far
(hash distance > 10: a new shot), or jumps from the second before (> 8) and isn't close to any
tile (> 6): something appeared. This grows with the number of distinct looks, not the video's
length: 75 tiles from 506 head frames on Tom Scott, with all five OCR-unreadable overlays on
them.

Known gaps (see the benchmark): the supersede rule keeps only a build's last stage, short-text
cards that share a template merge on look, and some lower-thirds over a presenter don't get a
tile.

Runs of head frames lasting 5 s or more are listed in `no_screenshot`, with the tiles that
fall inside them, so the notes can say "no screenshot of this" instead of skipping silently.

### 8. Contract

Before writing the manifest it checks that every sampled frame has exactly one outcome and
that the counts sum to the number sampled; otherwise it exits with an error.

## Thresholds

| Constant | Value | What it controls | Tuned on |
| --- | --- | --- | --- |
| `PIX` | 20 | grey-level change that counts as changed | |
| unchanged test | < 0.2% overall, < 1% per cell | skipping identical frames | all four |
| `FACE_MIN` | 0.015 | face area for a head candidate | Tom Scott, Bookfox |
| recurring shot | ≤ 14 hash bits, ≥ 2 frames, > 30 s apart | the host's shot | Tom Scott, Bookfox |
| `HEAD_WORDS` | 8 | words that always keep a head frame | Tom Scott, Bookfox |
| persistence | ≥ 2 shared words within 2.5 s | caption or page over the host | Tom Scott, Bookfox |
| dedup | Jaccard > 0.85; supersede ≤ 10% missing; hash ≤ 6 | duplicates | all four |
| review tiles | new look > 10, jump > 8 and > 6 from tiles | head review sheet | Tom Scott |

The talking-head and review-tile values were tuned on two videos. To change one: edit it, run
`frames.py` on the test videos, and compare with `bench/score.py` (see
[`bench/README.md`](https://github.com/endgame302/video-notes/blob/main/bench/README.md)). The `gate` field lets you try rules on a saved
manifest without running OCR again.

## Performance

Measured on an Intel Core i5-10300H (4 cores) with a GTX 1650, batched OCR:

| Video | Length | Decode | Skip/face/hash | OCR | Total |
| --- | --- | --- | --- | --- | --- |
| Bro Code | 10.3 min | 91 s | 8 s | 134 s | 235 s |
| Tom Scott | 10.7 min | 85 s | 24 s | 53 s | 164 s |
| Bookfox | 17.8 min | 90 s | 36 s | 111 s | 240 s |
| Fireship | 5.4 min | 15 s | 5 s | 38 s | 60 s |

That is 11–23 minutes per hour of video, text-dense screencasts being the slowest. Peak disk
use is about 210 KB per sampled 1080p frame (scaled by pixel count); the script estimates it,
adds 20% and 0.5 GB, and stops if there isn't room.
