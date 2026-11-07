# Tool sweep, November 2026

Issue [#42](https://github.com/endgame302/video-notes/issues/42). Swept on 2026-11-08 with the method in
[`docs/agents/tool-scouting.md`](../agents/tool-scouting.md). Every finding below comes from a search made
on that day. Nothing comes from model memory. I read READMEs, model cards, release notes and API data. I ran
none of these tools and installed nothing.

Earlier research covered similar tools ([#24](https://github.com/endgame302/video-notes/issues/24)) and
direct-video models ([#25](https://github.com/endgame302/video-notes/issues/25)). Those notes live on the
throwaway branches `research/similar-tools` and `research/direct-video-models`. This sweep adds to them.

## Short answer

1. **OCR.** The best lead is the one already installed. RapidOCR 3.9 and later run PP-OCRv6, which has
   `tiny`, `small` and `medium` tiers. The Indra comparison already used RapidOCR 3.10, so it measured the
   `small` tier. Nobody has measured `tiny` (faster) or `medium` (more accurate) on our frames. The new
   one-billion-parameter OCR language models (Xiaomi-OCR-0, MiniCPM-OCR 1.0, OvisOCR2, TeleOCR, Unlimited-OCR 2)
   all report scores on document pages, not video frames. One of them is worth a test on code screens, where
   Indra fails.
2. **Frame sampling and dedup.** Nothing new beats `frames.py`'s sampling. One tool, claude-real-video,
   has a dedup design worth testing: a sliding window plus a "settled" detector. Nobody publishes a coverage
   number, so only our own benchmark can settle it.
3. **Captions and transcription.** faster-whisper's last release is from 2025-10-31, though its main branch is
   active. A new small model, granite-speech-5.0-470m-turboctc, is Apache-2.0 and runs from GGUF on CPU.
   Worth one test on `--audio` runs.
4. **Direct-video models.** Nothing since 2026-10-30 changes #25. Gemini Omni 1.2 Flash is video generation,
   not video reading. One search result said otherwise, and Google's changelog shows it is wrong.
5. **Similar tools.** About a dozen new or missed tools. The closest in method are claude-real-video (2,295
   stars), lecture-to-notes and watchless. None reports coverage of on-screen content.
6. **Note-quality judge.** A new paper shows LLM judges miss omissions (a fact left out of a note), at
   near-chance. That is the failure our judge most needs to catch. A new class of small "decision models"
   (Jev, Mica, Liquid's d1-omni-600M) answers yes/no with a probability and could check single claims
   cheaply.
7. **Download.** yt-dlp 2026.10.26 needs Python 3.11 or newer for the pip route, and its README says full
   YouTube support needs `yt-dlp-ejs` plus a JavaScript runtime. Our install notes and `check_deps.py` mention
   neither. One cheap check on this machine settles whether it matters.

## Channels searched and their windows

Today is 2026-11-08. "6 months" means 2026-05-08 to 2026-11-08.

| Part | Window | Why |
| --- | --- | --- |
| OCR | 6 months (GitHub, Hugging Face, PyPI, leaderboards, directories, papers) | The 2026-11-07 sweep covered GitHub only. I re-ran GitHub over the full 6 months, since it is cheap and the other channels had never been swept. |
| Frame sampling and dedup | 6 months | never swept |
| Captions and transcription | 6 months | never swept |
| Models that take video directly | 2026-10-30 to 2026-11-08 | last swept 2026-10-30 |
| Similar video-to-notes tools | 2026-10-30 to 2026-11-08, plus older tools that #24 missed | last swept 2026-10-30 |
| Note-quality judge | 6 months | never swept |
| Download | 6 months | never swept |

| Channel | What I searched | Window | Notes |
| --- | --- | --- | --- |
| GitHub search | `gh search repos <terms> --created ">=<start>" --sort stars`, 2 to 9 wordings per part | per part, above | Wordings are in each part. |
| Vendor orgs | `gh repo list`: tesseract-ocr, PaddlePaddle, RapidAI, datalab-to, SYSTRAN, yt-dlp, QwenLM, MoonshotAI, google-gemini, OpenGVLab. Hugging Face authors by newest: Qwen, moonshotai, google, openbmb, nvidia, LiquidAI, microsoft, tencent, allenai, internlm, ByteDance-Seed | per part | PaddlePaddle's org list shows no new OCR repo. PaddleOCR itself shipped v3.7.0 (PP-OCRv6) on 2026-06-11. |
| Hugging Face models | API: search and `pipeline_tag`, sorted by newest, likes and trending | per part | |
| PyPI | The PyPI search page failed to load for my fetch tool. I used web search limited to pypi.org, then the PyPI JSON API to check each name | 6 months | Weak channel. Names found only through search results. |
| Leaderboards | OmniDocBench (GitHub page), olmOCR-Bench (GitHub page). The Open ASR Leaderboard Space renders with JavaScript, so I could not read its table. I used model cards that quote it instead. | as of 2026-11-08 | |
| GitHunt | Week view (Nov 2 to Nov 8, top 30), month view (top 240 loaded), year view (only 30 entries loaded) | week, month, year | I filtered by keyword in the page. Nothing for OCR, ASR or notes in the week view. The month view shows Indra and MiniCPM-OCR, already known. The year view shows nothing relevant. |
| Trendshift | Home page ranking, top 25 | 2026-11-08 | No OCR, speech, video-notes or downloader repos. |
| OSS Insight | Collections list (102 collections) and trending page | 2026-11-08 | No collection for OCR, speech, video or documents. Its trending page says star rankings are paused because data since mid-2025 was under-captured. Nothing usable. |
| HackerGit | Search with `sort=new&from=2026` for: ocr, video notes, keyframes, transcription, whisper, yt-dlp, scene detection, video understanding, llm judge | 2026 only, newest first | Little. Found Scriptorium (lectures to Obsidian notes, shown on HN 2026-11-03) and Scan-to-vector (scanned pages to PDF). No OCR, ASR or downloader tool. |
| Hugging Face papers | Trending page, plus paper search for 7 wordings | 2026-05-08 to 2026-11-08 | Found Unlimited OCR, the Xiaomi-OCR-0 report, PolyOCR, Hawkeye, MURMUR, a tutorial-video agent paper and a judge-omission paper. |

---

## 1. OCR

Current choice: Tesseract 5 and RapidOCR. Last tested: Indra (87% of known strings, against RapidOCR's 89%,
about 8x faster, weak on code characters). See the
[#30 comment](https://github.com/endgame302/video-notes/issues/30#issuecomment-6710202417).

GitHub wordings: `OCR`; `text recognition vision language model`; `document parsing OCR`; `screen text extraction
screenshot OCR`; `ocr onnx cpu`; `screen recording code ocr`; `video ocr subtitles frames`.

**Every score below was measured on document pages, scene text or photos. None was measured on video
frames, and none on code screens.** Treat every headline number as a hint about the model, not about our
frames.

| Candidate | Created | Licence (code / weights) | Windows, hardware, size | Headline claim and the data it was measured on |
| --- | --- | --- | --- | --- |
| **PP-OCRv6** (PaddleOCR 3.7.0, RapidOCR 3.9+) | 2026-06-11 | Apache-2.0 / Apache-2.0 | ONNX, CPU. Tiers: tiny 1.5M, small 7.7M, medium 34.5M parameters. RapidOCR 3.10 lists all three in [`default_models.yaml`](https://github.com/RapidAI/RapidOCR/blob/main/python/rapidocr/default_models.yaml) and uses `small` by default. | Vendor release note: medium is +4.6% detection and +5.1% recognition over PP-OCRv5 server, and "5.2x" faster on CPU with OpenVINO. Vendor's own benchmark, document and industrial text. |
| **Xiaomi-OCR-0** | 2026-09-28 | Apache-2.0 / Apache-2.0 | 0.87B parameters. Runs on SGLang or vLLM (GPU) or experimentally on Ollama (community GGUF, about 1.8 GB). Windows not stated. | 95.24 on Real5-OmniDocBench (rank 1 on that page), 96.83 on OmniDocBench v1.6 (rank 2). Document pages. Its README says scene text and irregular layouts need whole-page mode. |
| **MiniCPM-OCR 1.0** (OpenBMB) | 2026-10-21 (weights); SDK 1.0.4 on PyPI | Apache-2.0 / Apache-2.0 | 1.3B parameters. Two stages: a layout model (PaddlePaddle/PaddleX) plus the recogniser on vLLM, SGLang, llama.cpp or Ollama. Official Docker image needs Linux, NVIDIA GPU, CUDA 12.9. | 93.68 on Real5-OmniDocBench, 54.7 on OCRBench v2, 1.2 pages per second. Document pages. |
| **MiniCPM-OCR Jev** | 2026-10-23 | Apache-2.0 / Apache-2.0 | 2B parameters | Scores whether an OCR result is right, 0 to 1. AUROC 93.6 on JevOCRBench (document regions). Not an OCR engine. See part 6. |
| **OvisOCR2** (ATH-MaaS) | 2026-07-13 | Apache-2.0 / Apache-2.0 (card) | 0.85B parameters. GGUF builds exist. | Rank 3 on OmniDocBench v1.6 (96.47). Document pages. Not read further. |
| **TeleOCR** (XingChen-AGI) | 2026-08-14 | Apache-2.0 / Apache-2.0 (card) | 1.4B parameters. GGUF builds exist. | Rank 2 on OmniDocBench v1.6 (96.91). Document pages. Not read further. |
| **OXR-1.0** (SoMarkAI) | 2026-10-05 | Apache-2.0 plus extra terms: [no commercial use](https://github.com/SoMarkAI/OXR/blob/main/LICENSE) above USD 2M in funding or revenue; personal use exempt. / same | 1.3B parameters. README asks for an NVIDIA GPU with 24 GB at minimum, and Docker. | Rank 1 on OmniDocBench v1.6 (97.03), olmOCR-Bench and DocParsingBench. Document pages. |
| **Unlimited-OCR / 2** (Baidu) | 2026-06-18 / 2026-10-26 | MIT / MIT | 3.3B parameters. Tested on an 80 GB A800. Community GGUF and MLX builds exist. | Built for hundred-page documents. On the OmniDocBench leaderboard. Document pages. |
| **Surya OCR 2.5** (Datalab) | 2026-10-25 | Apache-2.0 / OpenRAIL | 0.69B parameters | 90+ languages, layout, tables. I did not read its scores. |
| **LightOnOCR-3** | 2026-10-06 | Apache-2.0 / Apache-2.0 (card) | 0.8B and 4B | Not read further. |
| **RapidOCRLite** (RapidAI) | 2026-10-14 | Apache-2.0 / not stated | "Smaller, faster" RapidOCR. 25 stars. | README has no accuracy table that I read. |
| **openocr-mlt** | 2026-11-06 (PyPI) | not stated on PyPI | ONNX. "Tested on Linux x86_64." | Multilingual (ScriptMoE). No English accuracy claim read. |
| Indra (already tested) | 2026-10-13 | Apache-2.0 / modified OpenRAIL-M | 1M parameters, CPU | See #30. |

Also found in the Hugging Face and leaderboard channels but not profiled, because they are document parsers
with no small-text or code angle: PaddleOCR-VL-1.6 (2026-05-27), MinerU2.5-Pro (2026-05-20), jina-ocr-v1,
PolyOCR (paper 2609.37712), MonkeyOCRv2. Models before the window (Chandra OCR 2 and Qianfan-OCR in March,
GLM-OCR in January) are outside it and not reviewed.

**Closest thing to our case.** [Hawkeye](https://huggingface.co/papers/2610.41254) (paper, 2026-10-30)
fine-tunes a vision-language model on 8,398 blurry frames taken from 1,699 real video sequences, and says it
beats larger models on text 20 pixels or smaller. It is the only claim here measured on video-derived frames.
The frames are egocentric (smart glasses), not screen recordings. I found no released weights.

### Worth a throwaway test

| # | Candidate | The one test |
| --- | --- | --- |
| 1 | **RapidOCR 3.10, PP-OCRv6 `tiny` and `medium`** (the `small` row already exists) | Re-run the 240-frame set from #30 with `tiny`, `small` and `medium` on the same machine. Record strings read (loose and strict, same 92 strings) and seconds per frame. It settles whether `tiny` gets near Indra's speed with RapidOCR's code accuracy, or `medium` beats `small` on code. No new dependency. |
| 2 | **Xiaomi-OCR-0** (smallest of the new language-model readers, GGUF or SGLang) | Run the 22 known strings from the code screencast (run 5) and its frames on Kaggle's T4. Record strings read and seconds per frame. It settles whether a language-model reader gets code characters right where Indra drops underscores and swaps digits, and whether it is fast enough to matter. This is the longest shot: document benchmarks say nothing about monospace text. |
| 3 | **MiniCPM-OCR Jev** as a post-check on any engine's output | Score the frames where Indra and RapidOCR disagree (strict mismatches) and see if the score separates the wrong reads. Only worth doing after test 1 or 2 shows two engines are needed. Low priority. |

### Rejected

- **OXR-1.0.** Best document score, but it needs a 24 GB GPU and Docker, and the licence adds a funding limit. We have a T4 (16 GB) and a laptop.
- **Unlimited-OCR 2.** 3.3B parameters, built for hundred-page documents. Our job is one frame at a time.
- **MiniCPM-OCR 1.0.** Two stages, wants PaddlePaddle plus a GPU server, and its Docker image is Linux only. Layout detection is for documents. Heavy for the question test 2 asks more cheaply.
- **OvisOCR2, TeleOCR, LightOnOCR-3, Surya 2.5.** Same class as Xiaomi-OCR-0 with no extra reason to prefer them. Test 2 can swap one in if Xiaomi-OCR-0 shows promise.
- **jina-ocr-v1.** Licence is CC-BY-NC-4.0, which blocks use in a published skill.
- **nano-ocr.** A 4.8M-parameter reader for single cropped words, scored on word images.
- **openocr-mlt.** Multilingual, tested on Linux only, no English claim.
- **RapidOCRLite.** 25 stars, no table. Test 1's `tiny` tier asks the same question with the full project.
- **Tesseract 5.5.4** (2026-10-28) and **PaddleOCR 3.7.0.** Updates to incumbents. Tesseract is already the weakest strict reader in #30.

---

## 2. Frame sampling and dedup

Current choice: ffmpeg at 1 fps, perceptual hash and OCR-text diff (`frames.py`).

GitHub wordings (window 6 months): `video keyframe extraction`; `slide extraction video lecture`; `scene detection
video`; `frame deduplication perceptual hash video`; `video frames screencast dedup`; `extract unique frames video
ffmpeg`; `keyframes video`; `scene change detect`; `duplicate frames`; `tutorial video frames`. Most returned
nothing above 15 stars. The useful finds came from the similar-tools wordings in part 5.

| Candidate | Created | Licence | Windows, hardware | What it does and what it claims |
| --- | --- | --- | --- | --- |
| **claude-real-video** (`crv`) | 2026-06-30 | MIT | Windows, macOS, Linux. Python 3.10+, ffmpeg. No models to download for frames. | Scene change plus a 1 s floor. Dedup compares against the last N kept frames (default 4), so a shot seen before a cutaway is not sent again. A "settled-local" detector and a third "action channel" catch small moving subjects. Options: `--adaptive` for slow changes, `--text-anchors` forces frames at caption times, `--frame-width 1600` for small text. Claim: "26 of 58 frames" on a 58 s clip, and a synthetic repro for small fast subjects. Its README says perceptual hashes go blind on flat colours. The only timing is a 3-minute 640x360 clip on a Mac. No coverage score against labelled states. |
| **watchless** | 2026-07-11 | MIT | Not stated | For slides: ffmpeg keyframes, then local SSIM on a fixed slide region. Other video types use no visual comparison. |
| **lecture-to-notes** | 2026-08-02 | MIT | Tested on Windows 11, RTX 3070 Ti | Frames plus perceptual dedup, cheap OCR triage, semantic dedup, then Surya OCR on canonical slides. |
| **TASKER** (VG-GUI-TASKER, ECCV 2026) | 2026-06-22 | not stated | Needs a multi-image vision model for the search | Keyframe search as graph search driven by a model. Measured on VideoQA and GUI-tutorial agent tasks, not on coverage of on-screen states. |
| **LoHi** (paper 2610.04318) | 2026-10-03 | paper | | Finding: dense low-resolution sampling beats sparse native-resolution at equal token budgets, and hour-long video is dominated by decoding time. About model input, not our capture. |
| PySceneDetect 0.7.2 | release 2026-10-12 | not checked | | Maintenance releases (0.7.1 on 2026-07-22). Release notes not read. |

### Worth a throwaway test

| # | Candidate | The one test |
| --- | --- | --- |
| 1 | **crv's dedup design** (sliding window of 4 kept frames, settled-local detector) | Run crv's frame step on the labelled coding screencast and the screencast with a webcam overlay, then score both with `bench/score.py` beside `frames.py`. Record coverage of labelled states and frames kept. It settles whether a sliding window plus a pixel-based gate keeps states that `frames.py` merges (the "full RapidOCR merges code steps" failure in `docs/ocr-and-cloud.md`). Run it on Kaggle. |
| 2 | **`--text-anchors` idea** | Count labelled states that start within 1 s of a caption cue, using the existing labels and the downloaded captions. No tool needed. It settles whether forcing a frame at each cue would recover states that `frames.py` skips. |

### Rejected

- **TASKER.** One model call per segment. Built to answer questions, not to capture every state.
- **watchless.** Visual comparison only for fixed-slide-area decks, which `frames.py` already handles.
- **lecture-to-notes.** Its dedup stages (perceptual, then semantic) match what `frames.py` already does. Its other idea, cheap OCR first and high-quality OCR only on survivors, is worth noting against part 1 test 1.
- **PySceneDetect.** Scene thresholds, which #24 found weak on light slides (a full slide change scores about 0.03).
- **Other GitHub hits** (ComfyUI keyframe nodes, annotation tools, Figma screenshot extraction): not video-to-notes.

---

## 3. Captions and transcription

Current choice: YouTube captions; faster-whisper large-v3 for `--audio`. Vendor: SYSTRAN.

GitHub wordings (window 6 months): `speech to text`; `whisper transcription`; `speech recognition model`; `ASR`;
`faster than whisper transcribe`; `transcribe youtube captions`. Hugging Face: `pipeline_tag=automatic-speech-recognition`
sorted by trending, newest and likes.

**State of faster-whisper.** Last release v1.2.1 on 2025-10-31, so `pip install faster-whisper` gives a
year-old build. The main branch is active: commits on 2026-11-06, 2026-11-02 and 2026-10-16. Two open
issues to know: `multilingual=True` silently returns translated text unless
`condition_on_previous_text=False` (2026-08-16), and the Silero VAD call mutates its input (2026-11-02).
CTranslate2 shipped v4.8.5 on 2026-11-02.

| Candidate | Created | Licence (code / weights) | Windows, hardware, size | Headline claim and data |
| --- | --- | --- | --- | --- |
| **granite-speech-5.0-470m-turboctc** (IBM) | 2026-08-04 | Apache-2.0 / Apache-2.0 | 473M parameters. Non-autoregressive. GGUF through transcribe.cpp on CPU, Vulkan or CUDA, no Python at runtime. 8 languages. | English WER 5.51%, averaged over 9 short-form English test sets of the Open ASR Leaderboard (card, unofficial). Short clips, not tutorials. The card does not compare with Whisper. Word timestamps not stated. |
| **granite-speech-5.0-2b** | 2026-10-07 | Apache-2.0 / Apache-2.0 | 2.3B parameters. GGUF Q8_0 via llama.cpp. The card says lower bit depths lose accuracy past one minute of audio. | Open ASR Leaderboard results as of 2026-10-21 (short-form English), plus a noisy-speech leaderboard. |
| **VibeVoice-ASR-BitNet** (Microsoft) | 2026-07-24 | MIT / MIT | 0.32B parameters, 1.58 GB. CPU, "real time with 3+ threads" on AVX2. 7 languages. | Card's own WER table. Not read in full. |
| **transcribe.cpp** (handy-computer) | 2026-04-07 | MIT | ggml runtime for 16+ model families, 2,143 stars. | A runtime, not a model. Would host the two Granite models. |
| **OpenASR** (QuintinShaw) | 2026-07-02 | Apache-2.0 (each model keeps its own licence) | Rust CLI, Windows x64 desktop app, local OpenAI-compatible API. One runtime for Whisper, Qwen3-ASR, Parakeet, Granite and others. Pre-v1. | Word-level timestamps in JSON. No accuracy claims. |
| **Nemotron-3.5-Transcribe-30B-A4B** (NVIDIA) | 2026-10-07 | OpenMDW-1.1 / OpenMDW-1.1 | 34B parameters (4.3B active), GPU. Up to one hour of audio, word timestamps, 40 languages. | Open ASR Leaderboard results captured 2026-10-12. 3,091 likes. |
| **Confucius4-R2T2** (Youdao) | 2026-09-10 | other / other | 2B parameters, built for real-time | Not read. |
| **Phonon-2.5** (Fermion) | 2026-10-22 | cc-by-4.0 | Not read | Not read. |
| **MURMUR** (paper 2606.01483) | 2026-05-31 | paper | | Finding: for long-form audio, intermediate chunk sizes balance accuracy and speed. Relevant to how we chunk. |

Before the window and so not reviewed: Qwen3-ASR (January), Cohere Transcribe (March).

### Worth a throwaway test

| # | Candidate | The one test |
| --- | --- | --- |
| 1 | **granite-speech-5.0-470m-turboctc** through transcribe.cpp | Transcribe one 10-minute tutorial on this laptop's CPU with faster-whisper large-v3 and with this model. Score both against a hand-checked list of about 40 technical terms, commands and numbers from the video. Record real-time factor. It settles whether a model about one-fifth the size reads technical speech as well, which would shorten `--audio` runs. |
| 2 | **faster-whisper main branch** against v1.2.1 | Run the same 10 minutes on both. It settles whether the year of fixes changes our transcripts. Low cost. |

### Rejected

- **Nemotron-3.5-Transcribe-30B-A4B.** 34B parameters and a GPU. Far outside a laptop skill.
- **granite-speech-5.0-2b.** Bigger than the 470M model, same family. Test 1 comes first.
- **VibeVoice-ASR-BitNet.** CPU-friendly, but only 7 languages and a BitNet runtime I did not check on Windows. Add to test 1 only if Granite fails.
- **OpenASR.** A runtime and desktop app with no accuracy claim. It could run test 1, but that is a convenience, not a finding.
- **Confucius4-R2T2, Phonon-2.5.** Not read, no sign of a lead.
- **Other GitHub hits.** Dictation apps (Mac-only or push-to-talk), meeting recorders, text-to-speech models, language-specific models. Wrong job.
- **YouTube captions.** No new tool for the caption half: yt-dlp already fetches them.

---

## 4. Models that take video directly

Window 2026-10-30 to 2026-11-08. Existing notes: `docs/research/direct-video-models.md` on `origin/research/direct-video-models`.

GitHub wordings: `video understanding`; `video LLM`; `video question answering`; `long video`. Hugging Face:
`video-text-to-text` and `any-to-any` models created since 2026-10-20. Hugging Face authors by newest: listed above.
API source: the Google AI Studio changelog.

- **Gemini API changes.** On 2026-11-05 video parts gained `mediaProcessing` (`STATIC` or `AGENTIC`), and tools
  can return video to the model. On 2026-10-27 a Gemini API CLI (beta) arrived. On 2026-11-02 Google said
  gemini-2.5-pro and gemini-2.5-flash route to newer models on 2026-12-01.
  [Changelog](https://aistudio.google.com/docs/changelog). The `STATIC` and `AGENTIC` choice is the one #25
  already recorded.
- **Gemini Omni 1.2 Flash** (GA 2026-11-05) is "up to 15-second video generation and conversational editing".
  It does not read long video. A web search summary said it extends the video input window. The changelog
  does not say that. Ignore that claim.
- **Claude.** The Claude vision page lists images only. It never mentions video.
- **LFM3-Omni-2B** (Liquid AI, created 2026-10-21, just before the window and missed by #25). Takes text, images,
  video with or without sound, and audio. Samples video at 2 fps, 32K-token context, LFM Open License v1.0.
  On-device size (2B). The 32K limit means a few minutes at most.
- **NativeCodec-4B** (created 2026-10-31): a codec-based video model, weights gated. Not reviewable.
- **Kimi K3.1 Pro** (2026-11-02, about 2.78T parameters, licence "other"): already in #25.
- **Mage-VL-Cowork** (Microsoft, 2026-10-30): a computer-use model on screenshots, not video.
- **Paper.** *Can LLM agents learn by watching tutorial videos?* (2611.01460, 2026-11-01) builds a
  "tutorialbook" memory from tutorial videos. Closest in aim to this skill. I read only the abstract.

### Worth a throwaway test

None new. #25's suggestion stands (Gemini at high resolution as a second reader for overlays and build stages).
That test still needs an API key and would send video to Google.

### Rejected

- **LFM3-Omni-2B.** 32K context at 2 fps covers a few minutes of video, and nothing says it reads small text.
- **Gemini Omni 1.2 Flash, Genie 4.** Generation, not reading.
- **NativeCodec, Mage-VL-Cowork, Kimi K3.1 Pro.** Gated, wrong job, or too large.

---

## 5. Similar video-to-notes tools

Window 2026-10-30 to 2026-11-08, plus older tools that #24 did not list and this search found. #24 is
at `origin/research/similar-tools`. It calls itself non-exhaustive.

GitHub wordings (window 2026-10-30): `video notes`; `video to notes`; `youtube notes`; `video study notes`; `video to
markdown`; `tutorial video skill`; `watch video agent skill`; `video screenshots notes`; `lecture notes video`.
For older tools I used the wordings in part 2 over 6 months.

I read each README. None publishes a coverage number for on-screen content.

| Tool | Created | Licence, stars | Windows | What it does |
| --- | --- | --- | --- | --- |
| **claude-real-video** | 2026-06-30 | MIT, 2,295 | yes | Frames with dedup, plus transcript. See part 2. A paid Pro edition adds on-screen text. |
| **lecture-to-notes** | 2026-08-02 | MIT, 116 | tested on Windows 11 | Whisper, frames, perceptual and semantic dedup, Surya OCR, a local vision model, synced HTML viewer. |
| **watchless** | 2026-07-11 | MIT, 146 | not stated | Keyframe-led visual documents. Comparison only for slides. |
| **Watch2Skill** | 2026-11-05 | source-available ("other"), 0 | CI covers Windows | Evidence-first: the agent reads the whole transcript and contact sheets, then runs `validate`. Says sampled frames may miss events. |
| **watch-skill** (codevcn) | 2026-11-04 | MIT, 0 | Windows installer and exe | Frames, transcripts, OCR with timestamps. CLI, MCP, REST. Verification contracts. |
| **video-course-notes** | 2026-11-01 | MIT, 1 | yes | HTML study notes from course video. Its `check_note.py --strict` gate checks structure anchors, per-image decoding and mobile viewport. Warns that fluent but numerically wrong notes are the most dangerous failure when speech recognition is weak. |
| **course-video-notes** | 2026-11-04 | MIT, 1 | not stated | Frames, OCR (RapidOCR, Apple Vision, Tesseract), speech to text. Review notes as PDF. Mentions OCR misreading stylised titles. |
| **video-to-lecture-notes** | 2026-10-30 | MIT, 2 | yes | One frame per 10 s, picks the readable board per minute. Chalkboard lectures. |
| **video-to-pdf** | 2026-10-31 | MIT, 1 | not stated | PDF and slides from lecture video with reviewed screenshots. |
| **Scriptorium** | 2026-11-03 | not read | not stated | Lectures into Obsidian notes and flashcards (shown on Hacker News). |
| TAL (paper 2611.01460) | 2026-11-01 | paper | | Agents learn from tutorial videos into a memory. Abstract only. |

### Worth a throwaway test

| # | Candidate | The one test |
| --- | --- | --- |
| 1 | **A publish gate like `check_note.py --strict`** | Not a tool test. Compare its checks (every image decodes, structural anchors, mobile viewport) with our existing checks and list what we lack. It settles whether we have a gap. Reading only. |

### Rejected

None of these tools replaces ours: none reports coverage, and the closest in intent have 0 to 2 stars. The
ideas worth keeping are the sliding-window dedup (part 2) and the publish gate above.

---

## 6. Note-quality judge

Current choice: Sonnet 5.5.

GitHub wordings (window 6 months): `llm-as-a-judge`; `llm judge evaluation`; `rubric grading llm`; `summary faithfulness
hallucination detection`; `grounded note verification citations`; `evaluate agent skill output`. Hugging Face model
searches: `judge`, `reward-model`, `hallucination`, `faithfulness`, `grader`. Papers: judge and summarisation
wordings. I found no judge leaderboard that fits notes.

**The finding that matters.** [*LLM Judges Verify Presence, Not Absence*](https://huggingface.co/papers/2608.31016)
(2026-08-31) tested eight judge designs on 500 note pairs with a known single error. Judges separated the flawed
note from its clean twin at 0.79 to 0.94 on added or altered content, but 0.50 to 0.63 on omissions (0.5 is
a coin flip). Wording changes and voting did not fix it. The data is clinical notes read against a transcript.
Omission is also our main risk: a skipped screenshot or a dropped command. The paper does not test Sonnet 5.5.

| Candidate | Created | Licence | Windows, hardware | What it does and claims |
| --- | --- | --- | --- | --- |
| **d1-omni-600M** (Liquid AI) | 2026-10-05 | LFM Open License v1.0 | 587M parameters, CPU or GPU, `transformers` 5.15+ | Decision model: you send a state (text, images, up to 30 s of speech) and named questions. It returns a probability per option, with no text generated. Context 16,384 tokens, but only 896 tokens of text when images are used. |
| **Mica** (akivet) | 2026-09-25 | Apache-2.0 | 4B, CUDA or llama.cpp, one GPU | Same kind of model for long inputs. Claims the same answer 97.3% of the time when options are shuffled. Author's own claim. |
| **von** (wfzyx) | 2026-09-18 | Apache-2.0 | 395M encoder, CPU | Archived 2026-10-19. The README points to d1-omni-600M. |
| **MiniCPM-OCR Jev** | 2026-10-23 | Apache-2.0 | 2B | Scores whether an OCR result is correct. AUROC 93.6 on document regions. |
| **TypeSafe Jev** | 2026-09 | hosted API | hosted | The model that started the decision-model class. Cap is 32k tokens per state. Not open. |
| **agent-claimcheck** | 2026-09-28 | Apache-2.0 | Python | Checks an agent's claims against tool outputs: `verified`, `false_success`, `unverifiable`. Rules first, then a classifier. Measured on its own 300-trace benchmark. |
| **attest** | 2026-06-19 | Apache-2.0 | Python | Same idea: grade each claim against what tools returned. |

### Worth a throwaway test

| # | Candidate | The one test |
| --- | --- | --- |
| 1 | **Our own judge on omissions** (no new tool) | Take two finished notes. Delete a known, checkable fact from each (a command, a screenshot caption, a number) in 10 places. Ask the Sonnet 5.5 judge to review each note against the transcript and frames, as the skill does today. Count how many deletions it flags. It settles whether our judge has the blind spot the paper found. |
| 2 | **d1-omni-600M** as a per-claim check | Ask it "does this text appear in this frame?" for 50 cheat-sheet lines, half true and half altered by one character, against the matching frame. Record accuracy and calibration. It settles whether a small local model can verify single claims. Unlikely to read dense small text; the 896-token text limit with images is a warning. |

### Rejected

- **TypeSafe Jev.** Hosted, closed, and a text-only 32k cap.
- **Mica.** 4B on a GPU, no sign it beats d1-omni-600M for our job.
- **von.** Archived by its author.
- **MiniCPM-OCR Jev.** Judges OCR output only. It belongs to part 1 test 3.
- **agent-claimcheck and attest.** They check an agent's claims against tool logs. Our claims are checked against sources and frames, not tool traces.
- **Hugging Face judge and reward models.** Domain-specific (legal, clinical, math, safety), no note-quality or screenshot use.

---

## 7. Download

Current choice: yt-dlp. Vendor: yt-dlp.

GitHub wordings (window 6 months): `youtube downloader`; `video downloader`; `yt-dlp alternative`; `download youtube video
cli`; `youtube po token`; `youtube bot detection bypass download`. The hits are wrappers and GUIs around
yt-dlp. None is an alternative engine. Triangle-Downloader (Chrome extension, no yt-dlp, GPL-3.0, 100 stars)
captures the player stream and is browser-only.

yt-dlp in the window: 5 releases. Latest is 2026.10.26.

- **Python 3.10 support removed** in 2026.10.26. The pip route now needs Python 3.11 or newer. Our `docs/install.md`
  and `SKILL.md` say "Python 3.10+". The winget route (a standalone exe) is not affected.
- **Official Windows binaries now need Windows 10 or later.**
- **Security.** 2026.10.21 says old executables are open to man-in-the-middle attacks through a `certifi` flaw and
  advises downloading the new release by hand rather than using the self-updater (`-U`). 2026.10.26 finishes the fix.
- **JavaScript runtime.** The [README](https://github.com/yt-dlp/yt-dlp#dependencies) says `yt-dlp-ejs` plus a
  JavaScript runtime are "required for full YouTube support". Only deno is enabled by default. Node, bun and
  QuickJS need `--js-runtimes`. `docs/install.md` and `check_deps.py` do not mention this.
- **YouTube clients** in 2026.08.19: added `visionos` and `web_embedded` fallbacks, removed `android_vr` from defaults.

### Worth a throwaway test

| # | Candidate | The one test |
| --- | --- | --- |
| 1 | **Our download step on this machine** | Run `yt-dlp -v -F <public video URL>` with the current winget build. Read whether it warns about a missing JavaScript runtime and whether the 1080p avc1 formats in `SKILL.md`'s format string still appear. Then run the same with `--js-runtimes node` (the skill installer needs Node 22, so it is likely present). It settles whether our download is silently limited. |

### Rejected

- **All wrapper and GUI repos** (Downvid, yt-dlp-gui-v2, Prism and others). They call yt-dlp.
- **Triangle-Downloader.** Browser-only extension.
- **A yt-dlp alternative.** None found in the window.

---

## Ranked tests

1. **RapidOCR PP-OCRv6 `tiny` and `medium`** on the 240-frame set from #30. Free, no new dependency, and it
   could close the speed gap with Indra while keeping RapidOCR's code accuracy.
2. **Our download step** with `yt-dlp -v -F`, with and without a JavaScript runtime. One command. If it shows
   a warning, every run is affected.
3. **Xiaomi-OCR-0** on the code screencast's frames, on Kaggle. The one place a new OCR reader could beat both
   Indra and RapidOCR.
4. **crv's sliding-window dedup** scored with `bench/score.py` on the two screencasts.
5. **Judge omission test** on our own Sonnet 5.5 judge with 10 deleted facts per note.
6. **granite-speech-5.0-470m-turboctc** against faster-whisper large-v3 on one 10-minute tutorial.
7. **d1-omni-600M** per-claim check on 50 cheat-sheet lines.

## What I could not check

- PyPI search did not load, so PyPI coverage rests on web search results and per-name JSON lookups.
- The Open ASR Leaderboard table needs JavaScript. I used model cards that quote it.
- GitHunt's year view loaded only 30 entries.
- I read only abstracts for the papers, and not the full model cards for OvisOCR2, TeleOCR, LightOnOCR-3,
  Surya 2.5, Phonon-2.5 and Confucius4-R2T2.
- No tool here was run. Every number above is the vendor's or the author's own, on the data named.
