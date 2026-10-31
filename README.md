# video-notes

[![CI](https://github.com/endgame302/video-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/endgame302/video-notes/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/endgame302/video-notes)](https://github.com/endgame302/video-notes/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1)](https://agentskills.io)

An [Agent Skill](https://agentskills.io) that turns a video (YouTube or anything
[yt-dlp](https://github.com/yt-dlp/yt-dlp) can download) into complete study notes: a designed
HTML page with learning goals, checked screenshots, diagrams that fit the content, a cheat sheet
verified against the source, and an optional self-test. You can learn what the video teaches,
and do what it shows, without watching it.

Works with Claude Code, Codex, Kimi Code, Gemini CLI, Cursor, OpenCode, GitHub Copilot and other
agents that support Agent Skills, on Windows, macOS and Linux.

## Quick start

```bash
npx skills add endgame302/video-notes      # install into your agents
```

Install ffmpeg, Tesseract and yt-dlp ([commands for your OS](docs/install.md#set-up-the-tools-once-per-machine)),
then the Python packages and the checker:

```bash
python3 -m pip install -r ~/.claude/skills/video-notes/requirements.txt   # or wherever it was installed
python3 ~/.claude/skills/video-notes/scripts/check_deps.py
```

Then ask your agent: *"Make study notes for https://www.youtube.com/watch?v=…"*

## Features

- **Learning goals and a details table**: what you'll be able to do, each goal linked to the
  section that teaches it.
- **Notes in the video's own order**: every explanation, example, correction and warning, with
  timestamp links and a tag on each claim (shown working, claimed, opinion, sponsor content).
- **Checked screenshots**: captured by [`frames.py`](skills/video-notes/references/frames.md),
  viewed at full size, cropped and annotated.
- **Diagrams chosen by the shape of the content**: a video map, plus concept maps, flowcharts or
  before/after views only where the content has that shape.
- **A cheat sheet** of every command, setting and URL, checked against the docs the video uses.
- **An optional quiz**, and a check by a reader who sees only the notes.
- **Capture in the cloud**: [`cloud_frames.py`](#capture-on-kaggle) runs the heavy step on
  Kaggle's free GPU, hands-off.

## Installation

| How | Command |
| --- | --- |
| Any agent ([skills CLI](https://github.com/vercel-labs/skills)) | `npx skills add endgame302/video-notes` |
| Claude Code plugin | `/plugin install video-notes --marketplace endgame302/video-notes` |
| Codex | `$skill-installer install the skill at https://github.com/endgame302/video-notes/tree/main/skills/video-notes` |
| By hand | copy `skills/video-notes/` into your agent's skills folder |

Per-agent folders, Windows commands, agents without skill support and the tool setup:
[docs/install.md](docs/install.md).

## Usage

| Agent | Call it with |
| --- | --- |
| Claude Code | `/video-notes <url>` (plugin: `/video-notes:video-notes <url>`) |
| Codex | `$video-notes <url>`, or pick it from `/skills` |
| Kimi Code CLI | `/skill:video-notes <url>` |
| Others | ask for "study notes for <url>" |

| Option | Effect |
| --- | --- |
| `--quiz` / `--no-quiz` | include or skip the self-test without being asked |
| `--audio` | also transcribe the audio with faster-whisper and attribute speakers |
| "add the quiz", "run the audio pass" | on notes already made: add just that |

Agents that can publish pages (such as Claude with Artifacts) give you a link; others write
`notes.html` with an `img/` folder and tell you the path. The screenshot step takes 11–23 minutes
per hour of video on a 4-core laptop.

### Capture on Kaggle

```bash
pip install kaggle && kaggle auth login            # once
python3 skills/video-notes/scripts/cloud_frames.py "https://www.youtube.com/watch?v=..."
```

The video downloads on your machine (YouTube blocks cloud machines), goes to a private Kaggle
dataset, is processed by a private Kaggle script on its CPU machine (`--gpu` for its T4), and
`frames/` comes back: about 15–18 minutes for an 11–17-minute video with other jobs running. Details: [references/frames.md](skills/video-notes/references/frames.md#running-on-kaggle-cloud_framespy).

## How it works

[`skills/video-notes/SKILL.md`](skills/video-notes/SKILL.md) is the procedure the agent follows:

1. **Raw material**: the 1080p video, the creator's captions (never a machine translation), the
   metadata, and every repo or doc the video uses.
2. **Details and goals**, then **notes** in the video's order, with on-screen text read by OCR
   and commands checked against the sources.
3. **Screenshots**: `frames.py` samples one frame per second, skips unchanged frames, drops the
   presenter's talking-head shot, removes duplicates, and accounts for every frame.
4. **Visuals and the page**: light and dark themes, contents sidebar, inline SVG diagrams.
5. **Independent checks**: a fresh reader tries every learning goal from the notes alone.

## Results

Screenshot capture on seven labelled test videos (422 on-screen states; the last three were
labelled by Claude agents, see [docs/benchmark.md](docs/benchmark.md#webcam-overlay-videos)):

| Video | Kind | Default | `--ocr hybrid` |
| --- | --- | --- | --- |
| Bro Code, "List comprehensions" | coding screencast | 100% | 100% |
| Tom Scott, "This Video Has … Views" | talking head + pages | 72% | **90%** |
| Bookfox, "9 sentence shapes" | talking head + captions | 76% | 76% |
| Fireship, "Did the AI bubble just pop?" | fast-cut news | 98% | 98% |
| Nick Saraev, "Claude Code Marketing Full Course" (20 min) | screen recording + webcam | 97% | 97% |
| Cole Medin, "Make the PERFECT Videos with Claude Code" | screen recording + webcam | 95% | 95% |
| Better Stack, "This 164MB Speech Model Might Replace Whisper..." | edited tutorial | 78% | 79% |

Bro Code and Fireship have no presenter on camera, so hybrid mode changes nothing there. The
previous method (scene detection plus a frame every 15 s) caught 7–41%. Method and
findings: [docs/benchmark.md](docs/benchmark.md); OCR engines and GPUs:
[docs/ocr-and-cloud.md](docs/ocr-and-cloud.md).

## Documentation

| | |
| --- | --- |
| [docs/install.md](docs/install.md) | every install route, per-agent folders, tools per OS |
| [skills/video-notes/references/frames.md](skills/video-notes/references/frames.md) | `frames.py` and `cloud_frames.py`: options, outputs, each stage, thresholds |
| [docs/benchmark.md](docs/benchmark.md) | the test set, scoring, results, coverage gaps |
| [docs/ocr-and-cloud.md](docs/ocr-and-cloud.md) | OCR engines, GPU speeds, Colab vs Kaggle |
| [docs/troubleshooting.md](docs/troubleshooting.md) | error messages and fixes |
| [CHANGELOG.md](CHANGELOG.md) | what changed in each release |

## Limitations

- **Tuned on little data**: the talking-head thresholds come from two videos; the test set's
  gaps are [tracked as issues](https://github.com/endgame302/video-notes/issues?q=label%3Abenchmark).
- **Some overlays are missed**: stylised titles over a presenter that no OCR reads end up only on
  the review sheets; builds keep only their last stage; look-alike title cards can merge.
- **1080p needed**: at 720p text behind a presenter becomes unreadable (72% → 62%).
- **Disk**: about 210 KB per sampled frame while capture runs (≈2.3 GB for 3 hours).
- **Tested on Windows**: the macOS and Linux code paths haven't been run on those systems yet.

## Contributing

Bug reports, test videos and pull requests are welcome; see [CONTRIBUTING.md](CONTRIBUTING.md).
Please follow the [code of conduct](CODE_OF_CONDUCT.md), and report security issues as described
in [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE). The test videos belong to their creators and are not part of this repository;
`bench/labels/` only describes what appears on screen and when.
