# Research: models that take video directly

Issue 25. Checked 2026-10-30. Claims are marked **Fact** (from the linked source) or **Inference**
(my reasoning).

## Bottom line

**Inference:** keep local frame capture as the default. Direct video is cheap enough to test as an
optional second reader, but only Kimi Code and Gemini CLI have a confirmed built-in path, both too
small for a 30-minute video. I found no published test of character-level reading through direct
video. And the skill's screenshots need local frames anyway.

## Models and limits

**Fact**, except where noted. Not exhaustive.

| Model | Length | Files | Sampling | Audio |
| --- | --- | --- | --- | --- |
| [Gemini](https://ai.google.dev/gemini-api/docs/video-understanding) (current models) | 3 h at default resolution, 1 h at high (1M context) | Files API, inline, public YouTube URL | 1 fps, settable; opt-in agentic mode | Yes |
| [Qwen 3.5–3.8](https://www.alibabacloud.com/help/en/model-studio/vision) | 2 h | 2 GB by URL | 2 fps default, 0.1–10 | Not understood |
| [Nova 2 Lite](https://docs.aws.amazon.com/nova/latest/nova2-userguide/using-multimodal-models.html) | Under 1 h advised | 1 GB (S3) | 1 fps to 16 min, then 960 frames total; squashed to 672×672 | Not processed |
| [Pegasus 1.6](https://docs.twelvelabs.io/docs/concepts/models/pegasus/pegasus-1-6) | 2 h per analysis | 10 GB, up to 5184×2160 | Not stated | Not checked |
| [Kimi K3, K3.1 Pro, K2.6, K2.7 Code](https://platform.kimi.ai/docs/guide/use-kimi-vision-model) | Not stated | [100 MiB](https://platform.kimi.ai/docs/api/files), FHD or less | Key frames, rate not stated | Not stated |

- **No video:** [Claude](https://platform.claude.com/docs/en/build-with-claude/vision) (the vision
  page never mentions it) and [GPT-6 models](https://developers.openai.com/api/docs/models) (text and
  image input).
- **Also accept video, not costed:** Seed 2.0 ([tested natively](https://arxiv.org/abs/2606.02522));
  [GLM-5.3-Flash](https://docs.z.ai/guides/vlm/glm-5.3-flash), from a search snippet.
- **Gemini at high resolution** is [Google's advice](https://ai.google.dev/gemini-api/docs/media-resolution)
  for dense text and small details.

**Conflicts in Google's docs, all updated this month:** tokens per frame are 66 and 258 on the video
page but 70 and 280 on the media-resolution page. The paid File API limit is 20 GB on the video page
but [2 GB per file](https://ai.google.dev/gemini-api/docs/files) on the Files page.

## Cost

**Fact:** the input and output rates (USD per 1M tokens) below. **Inference:** the arithmetic.

Cost = input tokens × input rate + output tokens × output rate. I assumed 10K output tokens for 30
minutes and 60K for 3 hours, an arbitrary guess that leaves out thinking tokens, which are billed as
output. Gemini uses Google's rounded rates: about 100 tokens/s by default, about 300 at high, audio
included. So 1,800 s and 10,800 s give the counts shown.

| Model and setting | Rates | 30 min | 3 h |
| --- | --- | --- | --- |
| [Gemini 3.8 Flash](https://ai.google.dev/gemini-api/docs/pricing), default | $0.75 / $3.75 | 180K in: **$0.17** | 1.08M in: **$1.04** |
| Gemini 3.8 Flash, high | same | 540K in: **$0.44** | 3.24M in: **$2.66** |
| [Gemini 3.5 Flash-Lite](https://ai.google.dev/gemini-api/docs/pricing), default | $0.30 / $2.50 | 180K in: **$0.08** | 1.08M in: **$0.47** |
| Gemini 3.5 Flash-Lite, high | same | 540K in: **$0.19** | 3.24M in: **$1.12** |
| [Nova 2 Lite](https://aws.amazon.com/blogs/machine-learning/pair-nova-2-lite-with-claude-for-cost-optimized-document-processing/) | $0.30 / $2.50 | 518,400 in: **$0.18** (276,480: **$0.11**) | 276,480 in: **$0.23** |
| [Qwen 3.7 Plus](https://www.alibabacloud.com/help/en/model-studio/model-pricing) | $0.40 / $1.60 | 65,536 in: **$0.04** | 2 × 65,536 in: **$0.15** |
| [Pegasus 1.6](https://www.twelvelabs.io/overage), input only | $1.75 per hour | 0.5 h: **$0.88** | 3 h: **$5.25** |

Worked example: 540K × $0.75 + 10K × $3.75 = $0.405 + $0.0375 = $0.44.

- **Gemini 3.8 Flash doubles on 2027-01-01:** $0.35 and $2.07 at default, $0.89 and $5.31 at high. Its
  row doesn't say video costs the same as text; I assumed so.
- **3 h at high doesn't fit one request:** 3.24M ÷ 1M means at least 4. 3 h at default is 1.08M, just
  over 1M, although Google says 3 hours works.
- **YouTube URLs** are in preview at no charge, and may change. I couldn't confirm whether that covers
  tokens or only the feature.
- **Agentic mode:** the pricing page claims up to 88% fewer input tokens on long video, but the model loads
  only what it judges necessary, against this skill's "miss nothing" rule.
- **Nova's rate** comes from an AWS blog; the pricing tables didn't load. Its docs contradict themselves:
  prose says 960 frames past 16 minutes, the table says 1,800 at 30. If the prose holds, 3 h is one frame
  per 11.25 s.
- **Qwen** is a promotional rate and uses Alibaba's reference code; I couldn't confirm the server enforces
  it. The default budget is 65,536 tokens per video with up to 2,000 frames: about 67,000 pixels per frame,
  roughly 345×194 at 16:9. The 2-hour limit means 3 h takes 2 requests.
- **Kimi K3** is [$3/$15](https://www.kimi.ai/resources/kimi-k3-pricing), but tokens per video are
  unpublished, so no estimate is possible.

**Fact, for comparison:** local capture has no API charge and takes
[11–23 minutes per hour](../../skills/video-notes/SKILL.md) on a 4-core laptop. A 1080p frame costs
[2,691 visual tokens](https://platform.claude.com/docs/en/build-with-claude/vision) on recent Claude,
against 280 at Gemini high.

**Inference:** token units differ by vendor, but the gap suggests far more compressed frames. I found no
stated pixel size for Gemini's.

## Reading on-screen text

**I found no published evidence on small text, code or short overlays read through direct video at
character level, and nothing on tutorial-length screen recordings.** The nearest work (**Fact**):

- **[MME-VideoOCR](https://arxiv.org/abs/2505.21333)** (v3, August 2026; 1,464 videos, tested Gemini 2.5,
  now limited to past users):
  - Gemini 2.5 Pro led at 73.7%: 83.0% on text recognition, 44% on long videos.
  - Most models got up to 64 frames. The paper doesn't say if Gemini got native video.
  - Higher resolution helped the three open models tested.
  - Models "correct" visible misspellings, for example "togther" to "together".
  - No small-text result. Code appears only inside a broader reasoning task.
- **[Moment-Video](https://arxiv.org/abs/2606.02522)** (October 2026) is the only test I found that clearly
  uses native video interfaces, on Gemini 3.x and Seed 2.0. It tests brief events, not text:
  - On GUI recordings, Gemini 3.1 Pro got 27.5% at 1 fps and 34.9% at 8 fps. Humans scored 84.3% on a sample
    of the whole benchmark.
  - In an audited subset, 1 fps hit about 55% of event intervals and 8 fps 93–99%. Errors persisted even
    when all were hit.
  - Gemini 3.1 Pro fell to 4.76% on videos beyond 3 minutes. The authors call that bucket small and
    indicative only.
- **[ClearText-Video](https://arxiv.org/abs/2608.28784)** (August 2026) covers signs, not screens. OCR text
  alone scored 23.3% against 51.2% for a model seeing the video, which favours direct video, though it
  measures question answering rather than transcription.
- **[VideoDB OCR benchmark](https://github.com/video-db/ocr-benchmark):** frames, not direct video, with some
  React and CSS tutorials. Gemini 1.5 Pro got 76.1%, RapidOCR 57.0%.
- **Vendors:** Nova's guide lists small text as a limitation. Google warns of missed detail with rapid scene
  changes.

**Inference:** none of this compares with [this repo's figures](../benchmark.md), which score capture of
on-screen states rather than text read. Repairing misspellings is a specific risk for commands, flags and
code, which the cheat sheet must copy exactly.

## Can the agents use it?

| Agent | Direct video (**Fact**) | Source |
| --- | --- | --- |
| Claude Code | No. Read covers images, PDFs and notebooks; a feature request was auto-closed as inactive | [Tools](https://code.claude.com/docs/en/tools-reference), [#80865](https://github.com/anthropics/claude-code/issues/80865) |
| Codex | Not mentioned; images only | [CLI](https://learn.chatgpt.com/docs/codex/cli) |
| Kimi Code | **Yes.** 100 MB per file; media past 20 MB per conversation is dropped | [Guide](https://www.kimi.com/code/docs/en/kimi-code-cli/guides/interaction.html), [source](https://github.com/MoonshotAI/kimi-cli/blob/main/src/kimi_cli/tools/file/read_media.py) |
| Gemini CLI | **In code, not docs.** read_file sends video inline, 20 MB cap. No free tier; not optimized for Gemini 4+ | [fileUtils](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/utils/fileUtils.ts), [constants](https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/utils/constants.ts), [README](https://github.com/google-gemini/gemini-cli) |
| Cursor | **Unclear.** Notes show attachments and a video-review subagent; in September staff said chat video was in internal testing | [Notes](https://cursor.com/docs/release-notes), [forum](https://forum.cursor.com/t/pass-native-video-to-gemini-flash-in-agent-chat/171007) |
| OpenCode | Not in the read tool. Model metadata can declare video; no route to the model verified | [read.ts](https://github.com/anomalyco/opencode/blob/dev/packages/core/src/tool/plugin/read.ts), [models.dev](https://github.com/anomalyco/models.dev) |
| GitHub Copilot | No; images and PDFs in the CLI | [CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview) |

Gemini CLI's free and personal users moved to Antigravity CLI, whose
[prompt box takes MP4, MOV, WebM and AVI](https://www.antigravity.google/docs/cli/prompting) by paste. It
isn't on the README's list.

**Inference:** at an assumed 2 Mbps for 1080p H.264, 30 min is 2 Mb/s × 1,800 s ÷ 8 = 450 MB and 3 h is
2.7 GB. So 20 MB is about 80 s, and 100 MiB about 7 minutes. Built-in routes would need heavy downscaling or
splitting, and downscaling is what [the benchmark](../benchmark.md) found loses text. Any agent could
run a script that calls an API, as `cloud_frames.py` does with Kaggle, but that needs a key and sends the
video to the vendor. Content on Gemini's free tier is
[used to improve Google's products](https://ai.google.dev/gemini-api/docs/pricing).

## What this means for the decision

**Inference:**

- **Local capture stays.** The skill embeds cropped, checked screenshots, which models don't return. Direct
  video could only replace the reading step.
- **No sampling advantage.** Gemini defaults to 1 fps, as does `frames.py`, which keeps full 1080p frames.
  Better Stack has 90 of 105 states at 2 s or less.
- **The real appeal:** under a dollar for 30 minutes, audio included on Gemini, none of the local compute, and
  no download for public YouTube videos.
- **Next step:** if anything, test Gemini at high as a second reader that flags overlays and build stages
  `frames.py` drops, with its output checked against real frames.

## Open questions for an experiment

1. **Coverage:** how many states does Gemini list on the seven labelled videos, at default and high, scored
   with `bench/score.py`?
2. **Character accuracy:** how does it do against RapidOCR's 43 of 44 checked strings, plus code, flags and
   deliberate misspellings?
3. **Timestamps:** are they accurate enough to pull the right frame?
4. **Completeness:** does one long pass list everything, or must long videos be chunked?
5. **Sampling:** does higher fps recover short states, and at what cost?
6. **Real billing:** what are actual token counts, agentic-mode costs and YouTube URL charges, and which
   stream resolution do URLs read?

## Couldn't verify

- Bedrock's Nova and Pegasus price tables, and Kimi's first-party per-model table.
- Whether Gemini got native video in MME-VideoOCR or ClearText-Video.
- Cursor's current behaviour, Seed and GLM limits, and Pegasus 1.6 sampling and output rate.
- [A code-extraction study](https://www.mdpi.com/2227-7390/12/7/1036) returned HTTP 403; unread.
