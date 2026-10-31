# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Two benchmark test videos with a webcam overlay (#3): a 20-minute stretch of Nick Saraev's
  "Claude Code Marketing Full Course" (78 states) and Cole Medin's "Make the PERFECT Videos with
  Claude Code" (57 states). `frames.py` catches 97% and 95%, but the webcam stops the
  unchanged-frame skip, so every frame is OCR'd. Labelled by Claude agents from the contact
  sheets and reviewed against written rules; not yet checked by a person.
- A benchmark test video of an edited tutorial (#7): Better Stack's "This 164MB Speech Model
  Might Replace Whisper..." (105 states). `frames.py` catches 78%, or 79% with `--ocr hybrid`.
  Most misses are slide build stages, and it keeps some frames mid-animation. Its zooms are into
  web pages, not a screen recording. Labelled and reviewed by Claude agents; not yet checked by
  a person.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` (Contributor Covenant 2.1), `SECURITY.md`, a pull
  request template, and bug-report and feature-request issue forms.
- CI (`.github/workflows/ci.yml`): checks `SKILL.md` against the Agent Skills spec, the plugin
  manifests, notebooks and stray control characters, compiles every script, and runs
  `frames.py` and `check_deps.py` on a generated test video.
- `docs/install.md` and `docs/troubleshooting.md`.
- `CLAUDE.md` and `docs/agents/` for coding agents: the GitHub issue tracker, the five triage
  labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), and
  how to read domain docs.

### Changed

- `cloud_frames.py` now runs on Kaggle's CPU machine by default, which has more cores, since
  hybrid mode's RapidOCR reads only the review tiles. `--gpu` selects the T4 and replaces `--cpu`.
  The CPU default hasn't been timed end to end yet.
- README restructured to the usual shape (badges, quick start, features, install, usage,
  results, docs, contributing); the detail moved into `docs/`.
- This changelog now follows Keep a Changelog, with git tags and GitHub Releases for each
  version.

## [1.2.0] - 2026-10-30

### Added

- `frames.py --ocr hybrid`: Tesseract for every frame, plus RapidOCR on the talking-head review
  tiles, keeping tiles with overlays Tesseract can't read. Background text repeated across
  tiles, matched by near spelling, is ignored. Tom Scott 72% → 90% of states, Bookfox unchanged
  (+14 frames), screencasts unaffected.
- `frames.py --ocr rapidocr` (experimental): RapidOCR for every frame. It broke dedup on a coding
  screencast (100% → 36%).
- `scripts/cloud_frames.py`: runs capture on Kaggle's free T4 with no browser. Downloads on this
  machine (YouTube blocks cloud IPs), uploads a private dataset, runs a private script, fetches
  `frames/`. One-time setup: `pip install kaggle`, `kaggle auth login`.
- RapidOCR for text copied into the notes when installed (43/44 checked strings against
  Tesseract's 39/44).
- Benchmark gaps tracked as GitHub issues labelled `benchmark`, a coverage table in
  `docs/benchmark.md`, and an issue form for proposing a test video.
- `docs/ocr-and-cloud.md` (what was measured, including what didn't work: Colab, full RapidOCR)
  and `notebooks/gpu_ocr_benchmark.ipynb`.

### Changed

- numpy 2 is no longer required.

### Fixed

- OpenCV 5 removed the face detector `frames.py` uses: `requirements.txt` now pins
  `opencv-python<5`, and `frames.py` and `check_deps.py` say what to install.

## [1.1.0] - 2026-10-29

### Added

- Claude Code plugin and marketplace manifests (`.claude-plugin/`), so
  `/plugin install video-notes --marketplace endgame302/video-notes` works.
- `scripts/check_deps.py`: checks a machine and prints install commands for Windows, macOS, and
  Debian, Fedora, Arch and openSUSE.

### Changed

- Standard Agent Skills layout: the skill lives in `skills/video-notes/` (with `scripts/`,
  `references/`, `assets/`), so `npx skills add endgame302/video-notes` installs it into Claude
  Code, Codex, Kimi, Gemini CLI, Cursor, OpenCode, Copilot and other agents.
- `SKILL.md` is agent-neutral: no Claude-only tools or placeholders; publishing falls back to
  writing `notes.html`; independent checks fall back to a separate self-check pass.
- `frames.py` tries CUDA, then any GPU decoder ffmpeg finds, then the CPU, and reports a missing
  face model or video clearly.
- The `frames.py` reference moved to `skills/video-notes/references/frames.md`, so installed
  copies carry it. README rewritten around installing, per agent and per OS.

### Removed

- The environment notes specific to the author's machine.

## [1.0.0] - 2026-10-29

### Added

- `scripts/frames.py` for screenshot capture, replacing scene detection plus a frame every 15 s:
  one full-resolution frame per second, batched OCR, talking-head drop with a persistence rule,
  dedup, review sheets of dropped talking-head frames, stretches with no screenshot, and a
  manifest that accounts for every frame. 72–100% of on-screen states caught on the four test
  videos, against 7–41% before.
- Benchmark: hand labels for four videos (`bench/labels/`), `bench/score.py`,
  `bench/label_sheets.py` and `docs/benchmark.md`.
- README, a `frames.py` reference, `requirements.txt`, MIT license.

### Changed

- Downloads 1080p, not 720p: at 720p text on pages behind a presenter is lost (72% → 62%).

### Fixed

- Captions pin the language, preferring the creator's subtitles, then the original-language
  auto-captions; `en.*` could pick a machine translation.

## 0.1.0 - 2026-10-28

### Added

- First version of the skill, with the page builder and template from the first run. Never
  published as a release.

[Unreleased]: https://github.com/endgame302/video-notes/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/endgame302/video-notes/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/endgame302/video-notes/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/endgame302/video-notes/releases/tag/v1.0.0
