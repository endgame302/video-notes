# Tool scouting

A **sweep** finds what exists today for one part of the skill. A model's knowledge stops months before the day it runs, so a list from memory misses whatever has shipped since. Indra OCR (created 2026-10-13) was missed that way: an OCR answer on 2026-10-29 came from memory, and the owner found Indra by chance. A plain star-sorted search shows only the old incumbents; a search filtered by creation date put Indra third.

## Steps

1. **Pick the part** from the table below, and note its last sweep date. Done when the sweep window is fixed: since the last sweep, or the last 6 months if there was none.
2. **Search every channel** for that window:
   - GitHub, 2-3 wordings of the job: `gh search repos <terms> --created ">=<window start>" --sort stars --limit 30`.
   - Each known vendor's org, newest first: `gh repo list <org> --limit 50 --json name,createdAt`.
   - Hugging Face: trending and newest models for the task.
   - PyPI: new packages for the same terms.
   - The area's current benchmark leaderboards: who is new near the top.

   Done when every channel has been searched, each with its window recorded.
3. **Profile each candidate:** what it does, licence (code and weights apart), Windows support, hardware and size, and its headline claims together with the data they were measured on. Claims measured on other data (document pages, not video frames) stay marked as such.
4. **Record the sweep:** update the part's row below with the date and a link to the findings, and list each candidate worth a test with the one throwaway test on our own frames or videos that would settle it. Add any new vendor to the row.

## Parts of the skill

| Part | Current choice | Vendors to check | Last swept |
| --- | --- | --- | --- |
| OCR | Tesseract 5; RapidOCR (PaddleOCR models) | tesseract-ocr, PaddlePaddle, RapidAI, datalab-to | 2026-11-07, GitHub only: Indra tested on our frames ([#30](https://github.com/endgame302/video-notes/issues/30)); Xiaomi-OCR-0 and OXR found, not reviewed |
| Frame sampling and dedup | ffmpeg at 1 fps, perceptual hash, OCR-text diff (`frames.py`) | | never |
| Captions and transcription | YouTube captions; faster-whisper large-v3 for `--audio` | SYSTRAN | never |
| Models that take video directly | none used | | 2026-10-30 ([#25](https://github.com/endgame302/video-notes/issues/25)) |
| Similar video-to-notes tools | | | 2026-10-30 ([#24](https://github.com/endgame302/video-notes/issues/24)) |
| Judge for note quality | Sonnet 5.5 | | never |
| Download | yt-dlp | | never |
