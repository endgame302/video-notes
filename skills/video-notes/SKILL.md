---
name: video-notes
description: Turn a video (YouTube or any yt-dlp URL) into complete study notes as a designed HTML page, with learning goals, checked screenshots, diagrams chosen to fit the content, a cheat sheet verified against the source, and an optional self-test, so the user can learn it and do what it teaches without watching. Use when the user shares a video link and asks for notes, a study guide or a write-up of a tutorial, or says "add the quiz" or "run the audio pass" on notes already made. Flags --audio, --quiz, --no-quiz.
license: MIT
compatibility: Needs Python 3.10+, ffmpeg, Tesseract 5 and yt-dlp, plus internet access. Windows, macOS and Linux; run scripts/check_deps.py to check a machine.
metadata:
  author: endgame302
  version: "1.2.0"
  repository: https://github.com/endgame302/video-notes
---

# Video notes

Input: a video URL, plus any of the flags below. If no URL was given, ask for it in one line and stop.

The user will use this page to learn everything the video teaches, and to do what it teaches, from the notes alone. It must miss nothing.

**Paths.** `scripts/`, `references/` and `assets/` below are inside this skill's folder (the folder holding this file). Run scripts by their full path, with `python3` (on Windows `python3` or `python`, whichever exists).

## Flags

- `--audio`: run the audio pass (step 1b). Without this flag, never run it and don't ask about it.
- `--quiz` / `--no-quiz`: include or skip the self-test quiz without asking.
- Later requests on notes already made: "add the quiz" runs only the [QUIZ] steps; "run the audio pass" runs only step 1b and fixes the names and attributions it changes. Update the page; don't redo anything else.

## 0. Before starting

- Run `python3 scripts/check_deps.py` once. If it reports something missing, show the user its install commands for their OS and stop until it passes; don't improvise around a missing tool.
- Work in a fresh folder outside the user's project (a temp or scratch directory).
- If no quiz flag was given, ask the user once (with your question tool if you have one): "Include a self-test quiz?" Options: "No (default)" / "Yes, add the quiz". No answer or no: build without it. Steps marked [QUIZ] run only when asked.

## 1. Start from the raw material, not a summary

- Download the video with yt-dlp at 1080p, never 4K or 1440p (`-f "bv*[height<=1080]"`; prefer avc1/H.264, which decodes fast). Don't drop to 720p: step 4's OCR can't read pages shown behind a presenter at 720p and drops them as talking heads (measured: 72% → 62% of on-screen states caught). Also get the info JSON (chapters, description, links, channel, upload date, view and subscriber counts). If video and audio don't merge, use the video-only stream for frames (and the audio stream for step 1b when `--audio` is set).
- Captions: pin the language, never `en.*` or `all`, which can pick a machine translation. Creator subtitles first: `--write-subs --sub-langs "en,en-US,en-GB"`. If there are none, auto-captions of the spoken language: `--write-auto-subs --sub-langs "en-orig"` (the `-orig` track is the real transcription; plain `en` on a video spoken in another language is a translation). For a video not in English, use the info JSON's `language` in place of `en`. Say in the details table which track was used.
- Fetch the resources the video uses: every repo, doc or README it opens on screen or links. For commands and config these are the source; the screen is a copy that may be out of date.
- Clean the captions into a timestamped transcript (about 30-second chunks) and read all of it.
- Auto-captions mangle names: correct every product, tool and skill name against what's on screen and in the fetched sources.

## 1b. Audio pass (only with `--audio`)

- Transcribe with faster-whisper (large-v3; install it with pip the first time, on a GPU if there is one), passing names from the title, description and on-screen text as hints. Wherever it disagrees with the captions, check the screen; mark any word still uncertain.
- If more than one person speaks, attribute every point to its speaker.

## 2. Open with the video's details and what you'll be able to do

- A details table: Creator (with channel link) · Subscribers (as of today) · Uploaded · Length · Topic · Tools shown · Resources/repos · Captions (creator's or auto) · Level / audience · Date watched (today) · Rating ("Not rated yet") · Status ("Notes done"). Leave out any row the video doesn't answer; never guess.
- 3–6 learning goals taken from the video, each starting with a verb ("Install…", "Configure…", "Explain why…"), each linked to the section that teaches it.
- One paragraph on what the video teaches, then the description's useful links.

## 3. Write the notes in the video's own order

- Group the chapters into a few parts, each part and section with a timestamp link back to the video.
- Cover everything taught: explanations, definitions, every worked example in full, the speaker's corrections, warnings, asides and opinions with their reasons.
- Tag how solid each claim is: shown working, claimed, opinion, sponsor content, or version/date-specific ("as of <upload date>"). Never present a claim or an ad as a demonstrated fact.
- Give every failure in the demo (errors, bugs found, wrong turns) a marked "What broke and the fix" box.
- Copy what's shown on screen (slides, code, commands, config, tables) as real text, read with OCR, upscaled and cropped where small. Use RapidOCR if it's installed (`pip install rapidocr onnxruntime`): it read 43 of 44 checked strings where Tesseract read 39, and running it on just the chosen screenshots takes about a minute per video. Otherwise Tesseract. Check every command and config against the fetched source; where the video and the current docs differ, show both and say which is current.
- Tables for facts that compare or repeat; prose only for reasoning. Short, plain sentences.
- Never copy a secret shown on screen (API keys, tokens); pick another frame or use a placeholder.

## 4. Screenshots, and check every one

- Run `python3 scripts/frames.py <video>`. Don't write your own ffmpeg sampling instead. It takes one full-resolution frame per second, skips frames identical to the last one, OCRs the rest, drops the presenter's recurring talking-head shot (unless it carries text that stays on screen), removes duplicates, and writes everything to `frames/` next to the video:
  - `t0000123.0.jpg`: the kept frames, named by their real time in seconds (from the decoder, so no seek drift).
  - `kept_*.jpg`: contact sheets of the kept frames with timestamps. Pick screenshots from these.
  - `heads_*.jpg`: contact sheets of DROPPED talking-head frames, one tile per distinct look. Always glance at them: an overlay OCR can't read (a logo, a stylised title, a "200 OK" badge) is dropped with the heads and only shows up here. To use one, rerun with `--keep-all`, or grab that second with `ffmpeg -i video.mp4 -ss <t> -frames:v 1 out.jpg` (`-ss` after `-i` decodes to the exact time).
  - `frames.json`: the manifest: every sampled frame's time, outcome and reason; the kept frames with their OCR words; `no_screenshot` stretches (talking head only, with their review tiles); timings; warnings.
- Add `--ocr hybrid` when RapidOCR is installed and the video has a presenter on camera: RapidOCR then reads the dropped talking-head tiles and keeps the ones carrying an overlay Tesseract can't read (measured: Tom Scott 72% → 90% of on-screen states caught, Bookfox unchanged, screencasts unaffected). It's quick on a GPU (DirectML on Windows, CUDA elsewhere) and takes a few minutes on a CPU. Don't use `--ocr rapidocr` (every frame): it merged distinct code steps on a coding screencast.
- To run capture on Kaggle instead of this machine (the user has run `pip install kaggle` and `kaggle auth login` once): `python3 scripts/cloud_frames.py <url>`. It downloads here (YouTube blocks cloud machines), uploads to a private Kaggle dataset, runs hybrid mode on Kaggle's CPU machine (`--gpu` for its T4) and brings `frames/` back, with no browser. About 15–18 minutes for an 11–17-minute video with other jobs running, mostly upload and setup. Use it when the user asks, or when this machine is short of disk or time; it still needs disk for the download itself.
- If it exits with an error (frames missing, decode stopped early, counts that don't balance, not enough disk), fix the cause and rerun; don't fall back to improvised sampling. Read its `warnings` (for example a video below 1080p).
- Where the speaker refers to something visual inside a `no_screenshot` stretch and no review tile shows it, say "no screenshot of this" in the notes rather than skipping it silently.
- The OCR words in the manifest are only for picking frames. For text you copy into the notes, OCR the chosen frame again, upscaled and cropped (step 3).
- Cost: about 210 KB of disk per sampled 1080p frame while it runs (≈2.3 GB for a 3-hour video; it checks free space first and deletes every frame it doesn't keep). Time: 11–23 minutes per hour of video (measured; text-dense coding screencasts are the slowest), so roughly 35–70 minutes for 3 hours; Tesseract OCR on the CPU is most of it. Run it in the background for long videos if you can.
- LOOK at the full-resolution frame before using it and confirm it shows what its caption says.
- Crop to the part that matters, dropping the webcam overlay where possible. Place it where it's discussed, with a caption.
- Details of every output field, stage and threshold, and of the OCR modes and cloud runs: `references/frames.md`. The thresholds were tuned on two talking-head videos; don't change them without re-scoring on the benchmark in the skill's repository (`bench/` at the repository URL above).

## 5. Visuals: pick by the shape of the content

Always include:

- A video map at the top: the parts on a timeline to scale, with each part's length.
- An "In 30 seconds" box opening each part (3–4 bullets); the speaker's key lessons as callouts.
- Annotated screenshots: numbered markers or boxes on the part that matters, explained in the caption.
- A cheat-sheet card at the end: every command, setting, config and URL, grouped by task, checked against the source. (Skip only if the video has none.)
- Glossary hovers: key terms with a dotted underline showing the definition on hover/tap, plus a short glossary.
- At least one diagram of the main thing taught or built: a sequence diagram or an architecture stack, whichever fits.

Add others ONLY when the content has that shape. Never add a type just to have it:

| Content shape | Visual |
| --- | --- |
| ideas that link to each other | concept map |
| steps that branch, loop or decide | flowchart / decision tree |
| "which one do I use when?" | decision tree |
| a change and what it fixes | before / after, side by side |
| a long live demo or session | session timeline of what happened |
| items judged on two qualities | 2x2, placed only as roughly as stated |
| real numbers to compare or over time | bar or line chart (never invented data) |
| a long process to learn step by step | click-through step diagram |
| memorable one-liners | quote cards |
| facts compared across several items | table |

This list isn't closed: if the content has another shape (a map for places or routes, a family or org tree, a circuit, a floor plan, a math graph or geometry figure, a chemical structure, a music staff, an anatomy diagram, a board position, a cycle), use the visual an expert in that field would draw. The same rules apply.

Rules for every visual:

- One strong visual per section over several weak ones. If a screenshot already shows the shape clearly, annotate it instead of redrawing it.
- Each diagram's title states its point, not its topic. ONE colour scheme with fixed meanings across all diagrams and part banners, with a colour key.
- Only facts from the video go in a visual: no invented numbers, steps or positions.
- [QUIZ] A "Test yourself" checklist ending each part, built from the quiz in step 7, answers hidden until clicked, each with the timestamp it comes from.

## 6. Deliver it as an HTML page

- Its own typefaces, light and dark themes, colour-coded part banners with "watch from here" timestamp buttons, a sticky contents sidebar (a drop-down on phones), screenshots that enlarge on click, and claim tags shown as small labels.
- Diagrams as inline SVG that adapt to dark mode. Images next to the page in an `img/` folder (or embedded, if the page must be a single file).
- [QUIZ] Tick boxes remembered in the browser, with a progress count in the sidebar and header.
- If the user also wants an editable copy, write the doc first and build the page from it.
- Deliver: if your environment can publish pages (for example Claude Artifacts), publish it, following that tool's page rules, and give the user the link. Otherwise write `notes.html` (with its `img/` folder) in the working folder, give the user the full path, and open it in their browser if you can.
- `assets/example-page/` holds the page from the first run (`build_page.py` built `page_template.html` from a doc's Markdown export): part banners, contents sidebar, quiz with saved ticks, lightbox, four inline-SVG diagrams. Reuse its structure, CSS tokens and helpers; rewrite the hero text and diagrams for each video, since they are specific to that one.

## 7. Check it with something other than you or the user

If you can start a sub-agent, use a fresh one for checks 1 and 6, given only what each check allows. If you can't, do them yourself in a separate pass, reading only what the check allows, and tell the user they were self-checked.

1. Cold-reader test: with ONLY the notes (no video, no transcript), try each learning goal. Hands-on tutorial: follow the cheat sheet in a clean sandbox where that's safe. Conceptual video: explain each goal, and check the explanation against the transcript. Pass = every goal reached from the notes alone. Fail = any "I'd need the video" moment; fix the notes and test again.
2. Source check: every command and config matches the fetched docs, or the difference is shown and explained.
3. Coverage audit: every transcript chunk maps to a section, every spoken number appears, every chapter has a timestamped section.
4. Screenshot audit: every screenshot viewed at full size, matching its caption, annotations on the right spot.
5. Visual check: each rendered diagram viewed once: nothing overlapping or cut off, colours match the key, each type fits its content.
6. [QUIZ] Independent quiz: from only the transcript, write 20 questions spread across the video; then answer them using only the notes. At least 95% correct. Fix any gap a missed question shows, and tell the user the score.

Tell the user what passed, what failed and was fixed, and what you couldn't verify.

## Tool notes

- yt-dlp, ffmpeg, ffprobe and Tesseract must be on PATH (or set `TESSERACT` to Tesseract's path). `scripts/check_deps.py` prints install commands for Windows, macOS and Linux.
- ffmpeg uses a GPU decoder when one works (CUDA, VideoToolbox, VA-API, D3D11) and falls back to the CPU.
- When running ffmpeg's `showinfo` yourself for timestamps, don't pass `-loglevel error` (it hides them).
