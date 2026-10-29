# Changelog

## 2026-10-29

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
- README, `docs/frames.md`, `requirements.txt`.

## 2026-10-28

- First version of the skill, with the page builder and template from the first run
  (`reference/`).
