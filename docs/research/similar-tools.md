# Research: similar video-to-notes tools

Issue 24, researched 2026-10-30. Stars and push dates come from the GitHub API on that day. I read
docs and source but ran none of these tools, so the only measured comparison is the existing
claude-video row in [`docs/benchmark.md`](../benchmark.md).

## Short answer

Keep the approach. Nothing found replaces `frames.py`, and no other tool I read publishes a
measure of how much on-screen content it catches. Reuse ideas rather than code.

## Comparison

| Tool | Kind, licence, activity | How it picks frames | How it reads on-screen text | Output |
| --- | --- | --- | --- | --- |
| **video-notes** (this repo) | Skill, MIT | 1 fps, then removes duplicates | Tesseract/RapidOCR, plus the agent viewing frames | HTML page, cheat sheet, independent checks |
| [claude-video](https://github.com/bradautomates/claude-video) | Skill, MIT, 19.6k stars, Sep 2026 | [Default](https://raw.githubusercontent.com/bradautomates/claude-video/main/CHANGELOG.md): [ffmpeg scene > 0.20, thinned evenly to 100, 512 px wide](https://github.com/bradautomates/claude-video/blob/main/skills/watch/scripts/frames.py); or sends the video to Gemini | Model vision; no OCR | Answer to a question, not notes |
| [video-to-skill](https://github.com/Paldom/video-to-skill) | Skills, MIT, 1 star, Oct 2026 | [Scene threshold fitted to a frame budget](https://github.com/Paldom/video-to-skill/blob/main/skills/video-keyframes/SKILL.md); interval sampling across gaps over 2 min | Tesseract as an index; the agent reads the image | `note.md` |
| [tldw](https://github.com/Joy9001/tldw) | Skill, MIT, 1 star, Oct 2026 | Ranked ffmpeg scene changes, 9 to a contact sheet | Model vision | `note.md`, including study notes |
| [video-to-article](https://github.com/grimseal/video-to-article) | Skill, MIT, 0 stars, Oct 2026 | [Contact sheet tile every 4 s, then `probe` compares moments](https://github.com/grimseal/video-to-article/blob/main/SKILL.md) | Model vision | Article, HTML page, clips |
| [yt-extract](https://github.com/muckybuzzwoo/claude-code-youtube-extract) | Plugin, Apache-2.0, 6 stars | Optional: scene detection, minimum gap, cap, or one per chapter | None stated; 4 keyframes for the summary | Markdown |
| [video-fetcher-to-markdown](https://github.com/JimmySadek/video-fetcher-to-markdown) | Skill, MIT, 518 stars, Oct 2026 | Contact sheet, only for videos up to 3 min | None stated | Obsidian Markdown, mostly transcript |
| [summarize](https://github.com/steipete/summarize) | CLI and extension, MIT, 6.8k stars, Oct 2026 | [Scene 0.3, 2 s gap, 6 slides](https://github.com/steipete/summarize/blob/main/docs/commands/slides.md) by default | Optional Tesseract | Summary with slides |
| [BiliNote](https://github.com/JefferyHcool/BiliNote) | App, MIT, 7.7k stars, Sep 2026 | [Fixed interval (6 s when screenshots are on)](https://github.com/JefferyHcool/BiliNote/blob/master/backend/app/services/note.py), tiled into grids; removes only [byte-identical frames](https://github.com/JefferyHcool/BiliNote/blob/master/backend/app/utils/video_reader.py) | Model vision; no OCR | Markdown; the [LLM writes a screenshot marker](https://github.com/JefferyHcool/BiliNote/blob/master/backend/app/gpt/prompt.py) and the time is cut afterwards |
| [lecture_transcriber](https://github.com/lautarograc/lecture_transcriber) | CLI, MIT, 0 stars | Scene 0.4 | Tesseract; no LLM at all | Markdown, SRT |
| [lecture2notes](https://github.com/HHousen/lecture2notes) | Research code, AGPL-3.0, 67 stars, Jul 2026 | CNN slide classifier, perspective crop, clustering | OCR with slide structure analysis | HTML, Markdown |
| [Gemini API](https://ai.google.dev/gemini-api/docs/video-understanding) | Paid and free API | Direct video: 1 fps in static mode (default); agentic mode picks its own | Model vision; higher resolution advised for fine text | Text, no images |
| [Gemini Notebook](https://support.google.com/notebooklm/answer/16215270?hl=en) (formerly NotebookLM) | Product | None | Captions only, for YouTube | Study guides, Q&A |
| [Glasp](https://glasp.co/youtube-summary) | Product, from $15/month | None stated | Transcript only as described | Summary |
| [BibiGPT](https://bibigpt.co/features/ai-video-summary-visual-content) | Product | Claims frame analysis; method undisclosed | Undisclosed | Illustrated article |
| [Azure Video Indexer](https://learn.microsoft.com/en-us/azure/azure-video-indexer/video-indexer-overview) | Cloud API, 2,400 free trial minutes | Shots and stable keyframes | OCR | Structured insights, not notes |
| [TwelveLabs Pegasus](https://www.twelvelabs.io/pegasus) | Cloud API, 2-hour limit | Direct video | Vendor claims native reading, no OCR model | Text |
| [Otter](https://help.otter.ai/hc/en-us/articles/5093321813911-Automated-Slide-Capture-Overview) | Product, live meetings only | Unique slides and screen shares | Chat over screenshots; method unstated | Transcript with slides |
| [Panopto](https://www.panopto.com/features/video-search/) | Product | Not applicable (search) | Vendor says OCR plus speech index | Timestamped search |

## Facts worth pulling out

- **Direct video is a real alternative for reading, but not for screenshots.** Gemini
  [samples at 1 fps by default](https://ai.google.dev/gemini-api/docs/video-understanding), the same
  rate as `frames.py`, at about 100 tokens per second at low resolution and 300 at high. Google warns
  that this sampling can miss quick scene changes. YouTube URLs are a free preview, public videos
  only, 8 hours a day on the free tier. Input on `gemini-3.8-flash` is
  [$0.75 per million tokens until the end of 2026, then $1.50](https://ai.google.dev/gemini-api/docs/pricing).
- **claude-video's Gemini engine** [asks for on-screen text or code and separates what is seen from
  what is heard](https://github.com/bradautomates/claude-video/blob/main/skills/watch/scripts/gemini.py).
  Its [SKILL.md](https://github.com/bradautomates/claude-video/blob/main/skills/watch/SKILL.md)
  recommends that engine and treats frames, captions and titles as untrusted.
- **Fixed scene thresholds are a known weak point.** video-to-skill says a full slide change on a
  plain light deck scores about 0.03, so common thresholds catch nothing. tldw makes the same
  argument for small UI changes.
- **At least one peer treats OCR as this skill does.** video-to-skill calls it
  ["a search index, not a source"](https://github.com/Paldom/video-to-skill/blob/main/skills/video-notes/SKILL.md)
  and lets the image win on conflict; `frames.py`'s manifest words are likewise only for picking frames.
- **Published evaluation is thin.** claude-video's README gives speech-transcription speed and memory
  only, and tldw's gives processing times. I found no on-screen coverage figure for any tool.
  video-to-skill's and video-to-article's skills describe no independent reader or check of commands
  against sources.

## Inferences (mine, not sourced)

1. **Sampling looks right.** On the four videos scored against both, the repo measured `frames.py`
   at 72–100% where scene-based methods scored 7–67%, and video-to-skill's 0.03 figure offers a
   plausible reason. No peer's source challenges this, but nobody else has measured it either.
2. **Peers have one real advantage: bounded review cost.** They cap frames (claude-video 100,
   summarize 6) or fit a budget, while `frames.py` kept 408 frames on the course stretch. The price of
   a cap is coverage, which is exactly what these peers don't measure.
3. **Direct video can't replace `frames.py`,** because the notes need checked screenshots and Gemini
   returns text. It could add a second reader for `no_screenshot` stretches and overlays OCR misses.
   Rough cost: one hour at low resolution is about 360,000 tokens, or about $0.27 of input at today's
   price, plus output. It requires an API key and sends the video to Google, so it should stay opt-in.
4. **The skill's distinct value is the output and its checks, not capture alone.** The largest peer,
   claude-video, answers questions rather than writing notes, and the closest peers in intent have
   one star or none.

## What this means for the decision

**Is the current approach right?** Yes, though the evidence is this repo's own benchmark.

**What can be reused?** Nothing as a dependency. `lecture2notes` is AGPL, so its code should not go
into this MIT skill. MIT peers could be copied with notice, but I found no component better than what
exists. These ideas could each be an issue:

| Gap in this skill | Idea | From |
| --- | --- | --- |
| Mid-animation frames kept as settled; build stages lost | Compare candidate moments, take the latest complete one | video-to-article `probe` |
| Up to 408 frames to review | Per-shot digest of OCR, speech span and motion, read before opening images | video-to-skill `timeline.json` |
| No stated path when a video has no captions; Whisper only with `--audio` | Fall back to local transcription; give a transcript quality verdict | claude-video, video-to-skill, tldw |
| SKILL.md takes only a URL, though `frames.py` takes a path | Accept local files | claude-video, tldw, video-to-skill, video-to-article |
| SKILL.md doesn't say captions, on-screen text and fetched repos are untrusted | State it, as claude-video does | claude-video |
| Motion that a still can't show | Short inline clips | video-to-article |
| Full capture on speech-only videos | Classify the genre first and skip frames | video-to-skill |

## Open questions and what I couldn't verify

- **Which claude-video version was scored?** `docs/benchmark.md` doesn't record it, and v0.3.0
  (2026-09-25) changed uniform sampling. Its Gemini engine and uncapped `token-burner` preset are
  unscored; `token-burner` would be the fairer test of scene detection.
- **How well does direct video read on-screen text?** Untested. `bench/score.py` scores kept frames,
  so Gemini would need a different method, such as scoring a timestamped list of states it reports.
- **Undisclosed methods:** BibiGPT, NoteGPT, Otter and Panopto don't say how they choose frames or
  read text. Pegasus and BibiGPT capabilities are vendor claims.
- **Not verified from primary sources:**
  - Lilys AI: it appears to include screenshots, but I found only Lilys-hosted notes and third parties.
  - Mindgrasp: third-party reviews only.
  - Eightify: its site blocked my fetch and the indexed pages look years old.
  - NoteGPT: [pricing](https://notegpt.io/pricing) is confirmed ($9.99–$99/month billed monthly), but
    on-screen handling is not.
  - slidecap and notepipe: seen only in search results, so left out.
  - TwelveLabs: its pages disagree on price, so none is quoted.
- **Depth varies.** I checked claude-video's and BiliNote's constants directly in source. Most other
  rows rest on READMEs or SKILL.md files, read through a fetch tool that summarizes pages, and tldw's
  ranking method isn't documented there.
