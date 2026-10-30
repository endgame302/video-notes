# Benchmark: screenshot capture

How `frames.py` was chosen and checked: four videos, every on-screen state labelled by hand,
and each capture method scored on how many of those states it catches. Two screen recordings
with a webcam overlay were added later (see [Webcam-overlay videos](#webcam-overlay-videos)),
then an edited tutorial (see [Edited tutorial](#edited-tutorial)).

## Test set

| ID | Video | Channel | Length | Kind | States |
| --- | --- | --- | --- | --- | --- |
| `YlY2g2xrl6Q` | Learn Python LIST COMPREHENSIONS in 10 minutes! | Bro Code | 10.3 min | coding screencast | 14 |
| `BxV14h0kFs0` | This Video Has … Views | Tom Scott | 10.7 min | talking head with pages and overlays | 29 |
| `jnaljahKibQ` | If you learn these 9 sentence shapes… | Bookfox | 17.8 min | talking head with caption cards | 75 |
| `nEaJMdM1djM` | Did the AI bubble just pop? | Fireship | 5.4 min | fast-cut news montage | 64 |
| `yulWjh3rq28-5000` | Claude Code Marketing Full Course, 1:23:20–1:43:20 | Nick Saraev | 20.0 min | screen recording, webcam at the right edge | 78 |
| `Ya51a1EJPZk` | Make the PERFECT Videos with Claude Code (Full Workflow) | Cole Medin | 15.2 min | screen recording, webcam bottom right | 57 |
| `eskgvQYchd0` | This 164MB Speech Model Might Replace Whisper... | Better Stack | 9.5 min | edited tutorial: animated slides, page zooms, terminal beside presenter | 105 |

All were downloaded at 1080p H.264. `yulWjh3rq28-5000` is a 20-minute stretch of a 6-hour video,
cut without re-encoding from 5000 s (see [`bench/README.md`](../bench/README.md)).

## Labels and scoring

Each video was cut into 1-fps contact sheets (`bench/label_sheets.py`), independent of every
method being scored, and every distinct on-screen state (a slide, a page, an overlay, a code
screen at a new step) was written down with its first and last tile. Labels are in
`bench/labels/<id>.json`:

```json
{"id": 6, "start": 71, "end": 74, "kind": "overlay", "ambiguous": false,
 "desc": "Text overlay 'screen-scrapers' over talking head"}
```

`start`/`end` are tile numbers; a tile numbered k shows real time k + 0.5 s, so the state is
on screen during real [start, end + 1]. Labels with `"real_time": true` (Fireship, labelled
from exact frames) are in real seconds already.

`bench/score.py` reports, per video:

- **coverage**: states with at least one kept frame inside them (± 0.25 s);
- **short**: the same, for states lasting 2 s or less (the hardest);
- **review**: kept frames, i.e. what a person or Claude then has to look through;
- **off-target**: kept frames inside no labelled state (intro shots, transitions);
- **missed**: the IDs of states not caught.

## Results

States caught:

| Method | Bro Code | Tom Scott | Bookfox | Fireship |
| --- | --- | --- | --- | --- |
| Previous skill: scene detection + a frame every 15 s | 7% | 41% | 39% | — |
| claude-video (third-party tool, balanced preset) | 7% | 28% | 37% | 67% |
| v2: segment on still-pixel change, pick the settled frame | 79% | 48% | 73% | 97% |
| 1 fps, before the face gate | 100% | 69% | 72% | 98% |
| **`frames.py`** | **100%** | **72%** | **76%** | **98%** |

Frames to review with `frames.py`: 206, 56, 179 and 187. Overall it catches 155 of the 182
labelled states (85%).

Still missed, by cause (from each frame's recorded outcome):

| Cause | States | Notes |
| --- | --- | --- |
| **Intermediate stages of a build** (`superseded`) | Bookfox 48, 69, 70, 72, 73, 74 | A sentence that grows on screen: only the finished stage is kept. Right for slides that build up; wrong when each stage is taught. |
| **Overlay over the presenter that OCR can't read** (`head`) | Tom Scott 6, 8, 10, 12, 13; Bookfox 6, 14, 18, 23, 71 | All of Tom Scott's and Bookfox 71 are on the `heads_*.jpg` review sheets; Bookfox's other four lower-thirds are not. |
| **Look-alike cards with little text** (`phash dup`) | Bookfox 13, 37, 52, 53, 57, 58; Tom Scott 11, 19, 26 | Numbered title cards on one template ("#03 The Short Sentence", "#05 …") and chapter cards merge with each other; Tom Scott 19 is on a review tile. |
| **Near-identical text** (`text dup`) | Bookfox 50 | A quote and its rewritten version. |
| **A real repeat** (`phash dup`) | Fireship 64 | The end card repeats state 48: merging it is correct. |

The first and third rows are where the next gains are: keep each build stage that stays on
screen for a few seconds, and compare short-text cards by their words before their look.

### Webcam-overlay videos

Scored with `frames.py` at `ec890df` (unchanged since), default Tesseract mode, run on Kaggle
(Linux, T4 session). `--ocr hybrid` kept exactly the same frames on both.

| | Course stretch (`yulWjh3rq28-5000`) | Cole Medin (`Ya51a1EJPZk`) |
| --- | --- | --- |
| States caught | 76/78 (97%) | 54/57 (95%) |
| Short states caught | 24/26 | 21/23 |
| Frames to review | 408 | 191 |
| Kept frames in no state | 92 | 52 |
| Frames skipped as unchanged | 0 of 1,201 | 10 of 913 |
| Missed | 3, 39 | 34, 46, 47 |

Coverage is not the problem on these videos; cost is. The webcam changes every second, so the
unchanged-frame test almost never fires: every frame is OCR'd, and the course stretch keeps a
frame for every 3 seconds of video. Masking the webcam before the comparison is the obvious
next step, and these two videos can now show whether it costs coverage.

The misses: course 3 and 39 are one-second states (a reply still growing, an open dropdown)
superseded by the next frame; Cole Medin 46 and 47 are build stages of an animated list
(the `superseded` row above). Cole Medin 34 is a labelling ambiguity, not a clean miss: the
same diagram view first appears in a fast scroll at 286, which the labels treat as
unsettled; `frames.py` kept 286 and counted 456–474 as its text duplicate.

These two were labelled differently from the first four. A Claude agent drafted the labels
from the contact sheets only; a second agent, also working only from the sheets, reviewed
them against fixed rules (a state must be settled and readable; a scroll starts a new state
only when most of the content is new; a return to an earlier screen is not a new state;
typing and streaming text are not states; readable popups and menus are); then a sample of
14 changes was checked against the tiles. No person has checked them yet; the 18 states
marked `ambiguous` are the place to start.

### Edited tutorial

Better Stack's video cuts between a full-screen presenter, animated slides that build a stage
at a time, web pages it zooms into, and a terminal beside the presenter. Its zooms are into
pages inside motion graphics; none is into a screen recording, so that part of the kind is
still uncovered. Scored with `frames.py` at `d53d573`: default Tesseract mode on Windows, and
hybrid on Kaggle (Linux, T4).

| | Default | `--ocr hybrid` |
| --- | --- | --- |
| States caught | 82/105 (78%) | 83/105 (79%) |
| Short states caught | 67/90 | 68/90 |
| Frames to review | 145 | 145 |
| Kept frames in no state | 49 | 47 |
| Frames skipped as unchanged | 35 of 568 | 35 of 568 |

Most states here are short: 90 of the 105 last 2 s or less, because the slides build quickly.
The 23 default-mode misses, by cause:

| Cause | States | Notes |
| --- | --- | --- |
| **Intermediate stages of a build** (`superseded`) | 17, 29, 52, 53, 56, 73, 75, 81, 90, 93, 94, 95, 96, 100 | The same row as the first four videos, and the largest here: each card or row added to a slide is merged into the finished slide. |
| **Look-alike slides** (`phash dup`) | 14, 16, 25, 41, 92 | Mostly dark, so a small change barely moves the hash. |
| **Overlay over the presenter** (`head`) | 12, 33, 34, 103 | Hybrid mode recovers 12, the "7x SMALLER" thumbnail. The animated subscribe button stays lost. |

Two costs that the coverage number doesn't show:

- **Mid-animation frames are kept as if settled.** A bar or number still counting up reads as
  new text. At 38 s `frames.py` kept a bar reading 764 MB, then dropped state 14, the settled
  178 MB, as its look-alike. Frames at 212 s (4.47), 297 s (25.8x) and 300 s (70.1x) also show values
  the slide never settles on, and all count as on target because the score only checks the time.
  These frames need a person to reject them.
- **A zoom looks like new content.** The comparison table is kept at 207, 208 and 209 s while
  the page zooms, the behaviour the issue predicted.

Labelled the same way as the webcam videos: one Claude agent drafted from the contact sheets
only, and a second, also from the sheets only, reviewed against the same rules, plus one for
animation (a value still counting up is not a state) and one for zooms (a zoom is a new state
only if it makes unreadable text readable, and is then `ambiguous`). The review resolved 46
draft `ambiguous` flags down to 3. A third pass checked 15 tiles behind the review's changes
and found no errors, then restored one state the review removed: the first-run log held for
16 s at 130–145, now state 37 and `ambiguous`. That pass ran before scoring, but by a session
that had already seen `frames.py`'s output on this video. No person has checked these labels
yet; the 4 states marked `ambiguous` are the place to start.

## What was learned

In the order it was found:

1. **Sampling beats segmenting.** Every attempt to pick "the right frame" per segment missed
   short overlays; sampling every second and removing duplicates afterwards caught the most on
   every video, at the cost of more frames to review.
2. **A shared face detector is not thread-safe.** One OpenCV `CascadeClassifier` used by six
   threads returned wrong boxes for 395 of 639 frames, and about 49 frames flipped between
   "head" and "not head" on every run. That made an unrelated change (batched OCR) look like it
   cost coverage. One detector per thread made runs identical.
3. **Downscaled OCR drops pages behind the presenter.** A "quick" OCR at 960 px was meant to
   make the talking-head check cheap. On Tom Scott, web pages shown behind him read as 0–7 words
   instead of 14–78, and were dropped (coverage 69% → 55%). 1280 and 1440 px lost some too;
   only full resolution kept them all.
4. **Word count is the wrong test for a talking head; persistence is the right one.** Real
   captions read 6–9 words and a Twitter header 3; OCR noise on a face is a few garbage words
   that change every frame. Keeping text that repeats within 2.5 s recovered six states and kept
   no extra talking-head frames on Tom Scott.
5. **Batched OCR is safe and faster, with a guard.** Batches gave identical words to one process
   per frame, and identical outcomes on all 2,649 frames, 21–42% faster. But an unreadable image
   makes Tesseract stop mid-batch and the rest of the batch gets no words, so the exit code and
   page count are checked.
6. **720p isn't enough.** Tom Scott at 720p: 62% instead of 72%. The skill downloads 1080p.
7. **Disk fills fast.** Full-resolution frames are about 210 KB each; two benchmark runs failed
   on a full disk before `frames.py` got its free-space check.

## Coverage by kind of video

| Kind of video | In the test set |
| --- | --- |
| Coding screencast, no webcam | Bro Code |
| Talking head with pages and overlays | Tom Scott |
| Talking head with caption cards | Bookfox |
| Fast-cut news montage | Fireship |
| Screen recording with a webcam overlay | Nick Saraev course (20-min stretch), Cole Medin |
| Burned-in subtitles | not yet |
| Webcam in another place (left, top, round, moving) | not yet |
| Light-mode coding screencast with small fonts | not yet |
| Edited tutorial with zooms into the screen | Partly: Better Stack (zooms into web pages, not a screen recording) |
| Slide lecture with animated builds | not yet |
| Scrolling pages, docs or chat logs | not yet |
| Whiteboard and handwriting | not yet |
| Ads and kinetic typography | not yet |
| Two-person podcast or interview | not yet |
| 720p or heavily compressed upload | not yet |
| Non-English or mixed scripts | not yet |
| Dark-mode dashboards and terminals | not yet |

### Known gaps

Each "not yet" row is a GitHub issue labelled
[`benchmark`](https://github.com/endgame302/video-notes/issues?q=is%3Aissue+label%3Abenchmark),
saying what the kind tests and why it matters; propose another with the **Test video** issue
form. The webcam-overlay videos showed that a webcam defeats the unchanged-frame test (it
skipped 33 of 21,769 frames on the full 6-hour course), which costs OCR time and frames to
review rather than coverage.

## Reproducing

See [`bench/README.md`](../bench/README.md).
