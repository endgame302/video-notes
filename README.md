# video-notes

A [Claude Code](https://claude.com/claude-code) skill that turns a video (YouTube or anything
[yt-dlp](https://github.com/yt-dlp/yt-dlp) can download) into complete study notes: a designed
HTML page with learning goals, checked screenshots, diagrams that fit the content, a cheat sheet
verified against the source, and an optional self-test. The goal is that you can learn what the
video teaches, and do what it shows, without watching it.

```
/video-notes https://www.youtube.com/watch?v=...            # notes, asks whether to add a quiz
/video-notes https://www.youtube.com/watch?v=... --quiz     # notes + self-test
/video-notes https://www.youtube.com/watch?v=... --audio    # also re-transcribe with Whisper
```

## What you get

- **A details table and learning goals**: creator, length, tools and resources shown, and 3–6
  "you'll be able to…" goals, each linked to the section that teaches it.
- **Notes in the video's own order**: every explanation, worked example, correction and warning,
  with timestamp links back into the video and a tag on each claim (shown working, claimed,
  opinion, sponsor content, version-specific).
- **Screenshots that were looked at**: chosen from frames captured by `scripts/frames.py`,
  checked at full size, cropped and annotated.
- **Diagrams picked by the shape of the content**: a video map and at least one diagram of the
  main thing taught, plus concept maps, flowcharts, before/after and so on only when the content
  has that shape.
- **A cheat sheet** of every command, setting and URL, checked against the docs and repos the
  video uses.
- **An optional quiz** (`--quiz`), and a check by an agent that sees only the notes.

The full procedure is in [`SKILL.md`](SKILL.md); that file is what Claude follows.

## Requirements

| Tool | Used for | Notes |
| --- | --- | --- |
| Claude Code | runs the skill | |
| Python 3.10+ | `frames.py`, page build | packages in [`requirements.txt`](requirements.txt); `frames.py` needs numpy ≥ 2.0 |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | video, captions, metadata | |
| [ffmpeg](https://ffmpeg.org/) + ffprobe | frame capture | an NVIDIA GPU (CUDA) is used if present, else the CPU |
| [Tesseract](https://github.com/tesseract-ocr/tesseract) 5 with English data | on-screen text | found via `$TESSERACT`, then `PATH`, then `C:\Program Files\Tesseract-OCR\` |
| faster-whisper | only with `--audio` | install when first needed |

## Install

```bash
git clone https://github.com/endgame302/video-notes.git ~/.claude/skills/video-notes
pip install -r ~/.claude/skills/video-notes/requirements.txt
```

Then install yt-dlp, ffmpeg and Tesseract, and check they run:

```bash
yt-dlp --version && ffmpeg -version | head -1 && tesseract --version | head -1
```

`SKILL.md` ends with **Environment notes** written for the author's Windows machine (where
yt-dlp lives, the `python3` shim). Edit that section to match yours; the rest of the skill is
machine-independent.

## Usage

In Claude Code, paste a video link and ask for notes, or run:

| Command | What it does |
| --- | --- |
| `/video-notes <url>` | builds the notes; asks once whether to include a quiz |
| `/video-notes <url> --quiz` / `--no-quiz` | skips the question |
| `/video-notes <url> --audio` | also transcribes the audio with faster-whisper and attributes speakers |
| "add the quiz" (on notes already made) | adds only the quiz |
| "run the audio pass" (on notes already made) | runs only the audio pass and fixes what it changes |

The result is published as a page and Claude gives you the link. Expect the screenshot step
alone to take 11–23 minutes per hour of video (see below); writing and checking the notes is
on top of that.

## How it works

1. **Raw material**: the 1080p video, the creator's subtitles (or the original-language
   auto-captions, never a machine translation), the info JSON, and every repo or doc the video
   opens or links.
2. **Details and goals**: the details table, learning goals and a one-paragraph summary.
3. **Notes** in the video's order, with on-screen text OCR'd and commands checked against the
   fetched sources.
4. **Screenshots**: `scripts/frames.py` captures candidates; each one used is viewed at full
   size first.
5. **Visuals** chosen by content shape, one colour scheme across the page.
6. **The page**: light and dark themes, a contents sidebar, part banners with "watch from here"
   links, inline SVG diagrams.
7. **Checks by something other than the writer**: a fresh agent tries every learning goal from
   the notes alone; commands are checked against the docs; every transcript chunk must map to a
   section; every screenshot and diagram is viewed.

## Screenshot capture: `scripts/frames.py`

The mechanical part of step 4 is a script, so every run captures frames the same way.

```bash
python scripts/frames.py path/to/video.mp4            # writes path/to/frames/
```

It samples **one full-resolution frame per second**, skips frames identical to the last one,
OCRs the rest in batches, drops the presenter's recurring talking-head shot (unless text stays
on screen over it), removes duplicates, and writes a manifest that accounts for every frame.
Dropped talking-head frames are not just discarded: one tile per distinct look goes on a review
sheet, because a logo or stylised title that OCR can't read gets dropped with the heads.

On four hand-labelled test videos (182 on-screen states):

| Video | Kind | States caught | Frames to review | Run time |
| --- | --- | --- | --- | --- |
| Bro Code, "List comprehensions" | coding screencast | 14/14 (100%) | 206 | 3.9 min for 10.3 min |
| Tom Scott, "This Video Has … Views" | talking head + pages | 21/29 (72%) | 56 | 2.7 min for 10.7 min |
| Bookfox, "9 sentence shapes" | talking head + captions | 57/75 (76%) | 179 | 4.0 min for 17.8 min |
| Fireship, "Did the AI bubble just pop?" | fast-cut news | 63/64 (98%) | 187 | 1.0 min for 5.4 min |

The previous method (scene detection plus a frame every 15 s) caught 7%, 41% and 39% of the
states on the first three. Details: [`docs/frames.md`](docs/frames.md) (how it works, outputs,
manifest fields, thresholds, errors) and [`docs/benchmark.md`](docs/benchmark.md) (test set,
scoring, results, what was learned).

## Repository layout

```
SKILL.md                    the procedure Claude follows
scripts/frames.py           screenshot capture (step 4)
reference/build_page.py     page builder from the first run (structure and helpers to reuse)
reference/page_template.html  its template: CSS tokens, layout, quiz, lightbox, SVG diagrams
bench/labels/*.json         hand labels: every on-screen state in the four test videos
bench/score.py              scores a frames.py run against the labels
bench/label_sheets.py       contact sheets for labelling a new test video
bench/README.md             how to reproduce the benchmark
docs/frames.md              frames.py reference
docs/benchmark.md           benchmark method, results and findings
```

## Limitations

- **Tuned on little data.** The talking-head thresholds were tuned on two talking-head videos.
  Re-score with `bench/score.py` before changing them, and add labelled videos when you can.
- **OCR-blind overlays.** Stylised titles, logos and lower-thirds over a presenter are dropped
  as talking head. Most show up on the `heads_*.jpg` review sheets, but not all.
- **Builds keep only the last stage.** When text grows on screen (a sentence built up word by
  word), only the finished stage is kept.
- **Look-alike cards merge.** Numbered title cards on one template, with little text, can be
  merged as duplicates of each other.
- **1080p needed.** At 720p, text on pages shown behind a presenter becomes unreadable, and
  those frames are dropped (measured 72% → 62%). `frames.py` warns below 1080p.
- **CPU OCR is the bottleneck.** About 35–70 minutes of capture for a 3-hour video.
- **Disk.** About 210 KB per sampled 1080p frame while it runs (≈2.3 GB for 3 hours); it
  checks free space first and deletes every frame it doesn't keep.
- **Developed on Windows** (Git Bash, an NVIDIA GTX 1650). The scripts avoid Windows-only
  paths, but haven't been run on macOS or Linux.

## Troubleshooting

| Message from `frames.py` | Meaning and fix |
| --- | --- |
| `Tesseract not found` | install Tesseract, or set `TESSERACT` to the executable |
| `needs ~N GB free` | free disk space or pass `--out` to another drive |
| `GPU decode failed; decoded on the CPU` (warning) | no CUDA ffmpeg; slower but correct |
| `decode skipped frames` / `decode stopped early` | a damaged or partial download; download again |
| `N OCR batches failed and were redone frame by frame` (warning) | an unreadable frame image; results are still complete |
| `below 1080p` (warning) | download the 1080p stream |
| `outcome counts don't balance` | a bug in `frames.py`; please report it with the manifest |

## License

[MIT](LICENSE). The test videos themselves belong to their creators and are not part of
this repository; `bench/labels/` only describes what appears on screen and when.
