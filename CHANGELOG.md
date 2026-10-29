# Changelog

## Unreleased

- **Benchmark gaps tracked as issues**: `docs/benchmark.md` has a table of which kinds of video
  the test set covers; each missing kind is a GitHub issue labelled `benchmark`, and
  `.github/ISSUE_TEMPLATE/test-video.yml` is a form for proposing a test video.

## 1.1.0 (2026-10-29): installable anywhere

- **Standard Agent Skills layout**: the skill now lives in `skills/video-notes/` (with
  `scripts/`, `references/`, `assets/`), so `npx skills add endgame302/video-notes` installs it
  into Claude Code, Codex, Kimi, Gemini CLI, Cursor, OpenCode, Copilot and other agents.
- **Claude Code plugin**: `.claude-plugin/plugin.json` and `marketplace.json`, so
  `/plugin install video-notes --marketplace endgame302/video-notes` works.
- **Agent-neutral `SKILL.md`**: no Claude-only tools or placeholders; publishing falls back to
  writing `notes.html`; independent checks fall back to a separate self-check pass.
- **Cross-OS**: `scripts/check_deps.py` checks a machine and prints install commands for
  Windows, macOS, and Debian/Fedora/Arch/openSUSE; `frames.py` tries CUDA, then any GPU decoder
  ffmpeg finds, then the CPU, and reports a missing face model or video clearly. The
  machine-specific environment notes are gone.
- `frames.py` reference moved to `skills/video-notes/references/frames.md` so installed copies
  carry it. README rewritten around installing, per agent and per OS.

## 1.0.0 (2026-10-29)

- **Screenshot capture is now a script**, `scripts/frames.py`, replacing scene detection plus a
  frame every 15 s. One full-resolution frame per second, batched OCR, talking-head drop with a
  persistence rule, dedup, review sheets of dropped talking-head frames, a list of stretches
  with no screenshot, and a manifest that accounts for every frame. Catches 72–100% of
  on-screen states on the four test videos, against 7–41% before.
- **Downloads 1080p**, not 720p: at 720p text on pages behind a presenter is lost (72% → 62%).
- **Captions pin the language**, preferring the creator's subtitles, then the original-language
  auto-captions; `en.*` could pick a machine translation.
- **Benchmark added**: hand labels for four videos (`bench/labels/`), `bench/score.py`,
  `bench/label_sheets.py`, and `docs/benchmark.md`.
- README, a `frames.py` reference, `requirements.txt`.

## 0.1.0 (2026-10-28)

- First version of the skill, with the page builder and template from the first run
  (`reference/`).
