# Installing video-notes

The skill is the folder [`skills/video-notes/`](../skills/video-notes). Install it with the
skills CLI, as a Claude Code plugin, with an agent's own installer, or by copying the folder.
Then install the tools it runs (below).

## Any agent: the skills CLI (recommended)

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

## Claude Code: as a plugin

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

## Codex

Use the skills CLI (`-a codex`), or ask Codex's built-in installer:

```
$skill-installer install the skill at https://github.com/endgame302/video-notes/tree/main/skills/video-notes
```

Codex reads skills from `~/.agents/skills/` (all projects) and `.agents/skills/` (one repo).

## By hand: any agent, any OS

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

## Agents without skill support

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

Optional extras:

| Package | Adds |
| --- | --- |
| `rapidocr onnxruntime` (`onnxruntime-directml` for a GPU on Windows) | `frames.py --ocr hybrid`, and more accurate text in the notes |
| `kaggle` (then `kaggle auth login` once) | `scripts/cloud_frames.py`: capture on Kaggle's free machines |
| `faster-whisper` | the `--audio` pass; the agent installs it the first time |

Notes:

- On Windows the Tesseract installer doesn't add itself to `PATH`; the scripts find it in
  `C:\Program Files\Tesseract-OCR\` anyway. Elsewhere, set `TESSERACT` to its path if it isn't
  on `PATH`.
- Use pip's `opencv-python` 4.x, not OpenCV 5 or a distro package: OpenCV 5 removed the face
  detector the scripts use, and some distro builds omit its model. `check_deps.py` says so.
- A GPU speeds up decoding (CUDA, VideoToolbox, VA-API or D3D11, whichever ffmpeg supports) but
  isn't required.

Problems: see [troubleshooting](troubleshooting.md).
