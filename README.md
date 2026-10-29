# video-notes

An [Agent Skill](https://agentskills.io) that turns a video (YouTube or anything
[yt-dlp](https://github.com/yt-dlp/yt-dlp) can download) into complete study notes: a designed
HTML page with learning goals, checked screenshots, diagrams that fit the content, a cheat sheet
verified against the source, and an optional self-test. The goal is that you can learn what the
video teaches, and do what it shows, without watching it.

Works with any agent that supports Agent Skills (Claude Code, Codex, Kimi Code, Gemini CLI,
Cursor, OpenCode, GitHub Copilot and others) on Windows, macOS and Linux.

```bash
npx skills add endgame302/video-notes
```

Then ask your agent: *"Make study notes for https://www.youtube.com/watch?v=…"*

## Contents

- [Install](#install)
- [Set up the tools](#set-up-the-tools-once-per-machine)
- [Usage](#usage)
- [What you get](#what-you-get)
- [How it works](#how-it-works)
- [Screenshot capture](#screenshot-capture-framespy)
- [Repository layout](#repository-layout)
- [Limitations](#limitations)
- [Troubleshooting](#troubleshooting)

## Install

### Any agent: the skills CLI (recommended)

```bash
npx skills add endgame302/video-notes
```

[`skills`](https://github.com/vercel-labs/skills) finds the agents installed on your machine and
asks which to install into. It needs Node.js 22.20 or newer and works on Windows, macOS and Linux.

| Option | Effect |
| --- | --- |
| `-g` | install for your user (all projects) instead of the current project |
| `-a <agent>` | pick the agent: `claude-code`, `codex`, `kimi-code-cli`, `gemini-cli`, `cursor`, `opencode`, `github-copilot`, `windsurf`, `goose`, `cline`, `roo`, `qwen-code`, … |
| `npx skills update` | update installed skills later |

Examples: `npx skills add endgame302/video-notes -g -a claude-code`,
`npx skills add endgame302/video-notes -g -a codex`.

### Claude Code: as a plugin

Inside Claude Code (2.1.275 or later):

```
/plugin install video-notes --marketplace endgame302/video-notes
```

Or in two steps, which works on older versions too:

```
/plugin marketplace add endgame302/video-notes
/plugin install video-notes@endgame302
```

Installed as a plugin, the skill is called `/video-notes:video-notes`; installed with the
skills CLI or by hand, it's `/video-notes`. Either way Claude also uses it on its own when you
ask for notes on a video.

### Codex

Use the skills CLI (`-a codex`), or ask Codex's built-in installer:

```
$skill-installer install the skill at https://github.com/endgame302/video-notes/tree/main/skills/video-notes
```

Codex reads skills from `~/.agents/skills/` (all projects) and `.agents/skills/` (one repo).

### By hand: any agent, any OS

A skill is just a folder. Copy `skills/video-notes/` from this repository into your agent's
skills folder.

macOS and Linux:

```bash
git clone https://github.com/endgame302/video-notes.git
mkdir -p ~/.agents/skills
cp -r video-notes/skills/video-notes ~/.agents/skills/
```

Windows (PowerShell):

```powershell
git clone https://github.com/endgame302/video-notes.git
New-Item -ItemType Directory -Force "$HOME\.agents\skills" | Out-Null
Copy-Item -Recurse video-notes\skills\video-notes "$HOME\.agents\skills\"
```

Replace `~/.agents/skills` with your agent's folder:

| Agent | All projects | One project |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `.claude/skills/` |
| Codex | `~/.agents/skills/` | `.agents/skills/` |
| Kimi Code CLI | `~/.kimi-code/skills/` or `~/.agents/skills/` | `.kimi-code/skills/` or `.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.agents/skills/` |
| Cursor | `~/.cursor/skills/` | `.agents/skills/` |
| OpenCode | `~/.config/opencode/skills/` | `.agents/skills/` |
| GitHub Copilot | `~/.copilot/skills/` | `.agents/skills/` |
| Others | see the [skills CLI agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md) | |

To keep it updated with `git pull`, link the folder instead of copying it
(`ln -s "$PWD/video-notes/skills/video-notes" ~/.agents/skills/video-notes` on macOS/Linux;
`New-Item -ItemType Junction -Path "$HOME\.agents\skills\video-notes" -Target "$PWD\video-notes\skills\video-notes"` on Windows).

### Agents without skill support

Any agent that can read files and run shell commands, including local-model agents, can follow
the skill as plain instructions:

> Read `<path>/skills/video-notes/SKILL.md` and follow it to make study notes for
> https://www.youtube.com/watch?v=…

The skill asks for independent checks by a fresh sub-agent; an agent that can't start one does
them itself and says so.

## Set up the tools (once per machine)

The skill runs Python scripts and three command-line tools. Install them, then let the skill's
checker confirm:

| | Windows | macOS | Debian / Ubuntu | Fedora | Arch |
| --- | --- | --- | --- | --- | --- |
| ffmpeg | `winget install --id Gyan.FFmpeg -e` | `brew install ffmpeg` | `sudo apt install ffmpeg` | `sudo dnf install ffmpeg` (RPM Fusion) | `sudo pacman -S ffmpeg` |
| Tesseract | `winget install --id UB-Mannheim.TesseractOCR -e` | `brew install tesseract` | `sudo apt install tesseract-ocr tesseract-ocr-eng` | `sudo dnf install tesseract tesseract-langpack-eng` | `sudo pacman -S tesseract tesseract-data-eng` |
| yt-dlp | `winget install --id yt-dlp.yt-dlp -e` | `brew install yt-dlp` | `python3 -m pip install --user -U yt-dlp` | `sudo dnf install yt-dlp` | `sudo pacman -S yt-dlp` |

Python 3.10 or newer, then the packages (from the skill folder your installer created, such as
`~/.claude/skills/video-notes` or `~/.agents/skills/video-notes`):

```bash
python3 -m pip install -r <skill folder>/requirements.txt
python3 <skill folder>/scripts/check_deps.py
```

On Windows use `python` if `python3` isn't found. `check_deps.py` lists anything missing with the
install command for your OS (it detects Windows, macOS, and Debian, Fedora, Arch and openSUSE
families), and exits non-zero until everything required is there. Your agent runs it first, too.

Notes:

- On Windows the Tesseract installer doesn't add itself to `PATH`; the scripts find it in
  `C:\Program Files\Tesseract-OCR\` anyway. Elsewhere, set `TESSERACT` to its path if it isn't
  on `PATH`.
- Use pip's `opencv-python`, not a distro OpenCV package: some omit the face model the scripts
  need, and `check_deps.py` says so.
- A GPU speeds up decoding (CUDA, VideoToolbox, VA-API or D3D11, whichever ffmpeg supports) but
  isn't required.
- `faster-whisper` is only needed for `--audio`; the agent installs it the first time.

## Usage

Ask in plain words, or call the skill by name:

| Agent | Call it with |
| --- | --- |
| Claude Code | `/video-notes <url>` (plugin: `/video-notes:video-notes <url>`) |
| Codex | `$video-notes <url>`, or pick it from `/skills` |
| Kimi Code CLI | `/skill:video-notes <url>` |
| Others | ask for "study notes for <url>"; the agent picks the skill from its description |

Options, as flags or in words:

| Option | Effect |
| --- | --- |
| `--quiz` / `--no-quiz` | include or skip the self-test without being asked |
| `--audio` | also transcribe the audio with faster-whisper and attribute speakers |
| "add the quiz" | on notes already made: adds only the quiz |
| "run the audio pass" | on notes already made: runs only the audio pass |

Where the page ends up: agents that can publish pages (such as Claude with Artifacts) give you a
link; others write `notes.html` and an `img/` folder in a working folder and tell you the path.

Expect the screenshot step alone to take 11–23 minutes per hour of video; writing and checking
the notes is on top of that.

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
- **An optional quiz**, and a check by a reader who sees only the notes.

## How it works

The full procedure is [`skills/video-notes/SKILL.md`](skills/video-notes/SKILL.md); that file is
what the agent follows.

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
7. **Checks by something other than the writer**: a fresh reader tries every learning goal from
   the notes alone; commands are checked against the docs; every transcript chunk must map to a
   section; every screenshot and diagram is viewed.

## Screenshot capture: `frames.py`

The mechanical part of step 4 is a script, so every agent captures frames the same way:

```bash
python3 skills/video-notes/scripts/frames.py path/to/video.mp4      # writes path/to/frames/
```

It samples **one full-resolution frame per second**, skips frames identical to the last one,
OCRs the rest in batches, drops the presenter's recurring talking-head shot (unless text stays
on screen over it), removes duplicates, and writes a manifest that accounts for every frame.
Dropped talking-head frames go on a review sheet, one tile per distinct look, because a logo or
stylised title that OCR can't read gets dropped with the heads.

On four hand-labelled test videos (182 on-screen states):

| Video | Kind | States caught | Frames to review | Run time |
| --- | --- | --- | --- | --- |
| Bro Code, "List comprehensions" | coding screencast | 14/14 (100%) | 206 | 3.9 min for 10.3 min |
| Tom Scott, "This Video Has … Views" | talking head + pages | 21/29 (72%) | 56 | 2.7 min for 10.7 min |
| Bookfox, "9 sentence shapes" | talking head + captions | 57/75 (76%) | 179 | 4.0 min for 17.8 min |
| Fireship, "Did the AI bubble just pop?" | fast-cut news | 63/64 (98%) | 187 | 1.0 min for 5.4 min |

The previous method (scene detection plus a frame every 15 s) caught 7%, 41% and 39% of the
states on the first three. Details:
[`references/frames.md`](skills/video-notes/references/frames.md) (outputs, manifest fields,
each stage, thresholds, errors) and [`docs/benchmark.md`](docs/benchmark.md) (test set,
scoring, results, what was learned).

## Repository layout

```
skills/video-notes/                 the skill: this folder is what gets installed
  SKILL.md                          the procedure the agent follows
  requirements.txt                  Python packages
  scripts/frames.py                 screenshot capture (step 4)
  scripts/check_deps.py             checks the machine, prints install commands per OS
  references/frames.md              frames.py reference, read by the agent when needed
  assets/example-page/              page builder and template from the first run, to reuse
.claude-plugin/                     Claude Code plugin and marketplace manifests
bench/                              benchmark: hand labels, scorer, labelling tool (not installed)
docs/benchmark.md                   benchmark method, results and findings
```

## Limitations

- **Tuned on little data.** The talking-head thresholds were tuned on two talking-head videos.
  Re-score with [`bench/`](bench/README.md) before changing them, and add labelled videos when
  you can.
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
- **Tested on Windows.** The scripts were run end to end on Windows 10 (Python 3.13, GTX 1650).
  The macOS and Linux paths (GPU decoder fallback, install hints, path handling) are written for
  those systems but haven't yet been run on them; reports welcome.

## Troubleshooting

| Message | Meaning and fix |
| --- | --- |
| `check_deps.py`: `MISSING …` | run the install command it prints for your OS |
| `Tesseract not found` | install Tesseract, or set `TESSERACT` to the executable |
| `OpenCV's face model is missing` | `pip install opencv-python` (not a distro OpenCV package) |
| `needs ~N GB free` | free disk space, or pass `--out` to a folder on another drive |
| `GPU decode unavailable; decoded on the CPU` (warning) | no working GPU decoder; slower but correct |
| `decode skipped frames` / `decode stopped early` | a damaged or partial download; download again |
| `N OCR batches failed and were redone frame by frame` (warning) | an unreadable frame image; results are still complete |
| `below 1080p` (warning) | download the 1080p stream |
| `outcome counts don't balance` | a bug in `frames.py`; please open an issue with the manifest |
| The agent doesn't see the skill | check the folder is `<skills dir>/video-notes/SKILL.md` (not nested one level deeper) and restart the agent |

## License

[MIT](LICENSE). The test videos belong to their creators and are not part of this repository;
`bench/labels/` only describes what appears on screen and when.
