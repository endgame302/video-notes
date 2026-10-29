# Contributing to video-notes

Thanks for helping. Bug reports, test videos, documentation fixes and code are all welcome.
By taking part you agree to follow the [code of conduct](CODE_OF_CONDUCT.md).

## Ways to help

- **Report a bug**: use the [bug report form](https://github.com/endgame302/video-notes/issues/new?template=bug-report.yml).
  Include the agent, OS, the command, and the `warnings` and `counts` from `frames.json`.
- **Propose a test video**: the benchmark is short of several kinds of video. See the
  [issues labelled `benchmark`](https://github.com/endgame302/video-notes/issues?q=label%3Abenchmark)
  and the [test video form](https://github.com/endgame302/video-notes/issues/new?template=test-video.yml).
- **Suggest a feature**: use the [feature request form](https://github.com/endgame302/video-notes/issues/new?template=feature-request.yml).
- **Run it on macOS or Linux**: the scripts have only been run end to end on Windows so far, so a
  report from either is useful even when everything works.

## Repository layout

```
skills/video-notes/                 the skill: this folder is what gets installed
  SKILL.md                          the procedure the agent follows
  requirements.txt                  Python packages
  scripts/frames.py                 screenshot capture (step 4)
  scripts/cloud_frames.py           runs frames.py on Kaggle (download here, process there)
  scripts/check_deps.py             checks the machine, prints install commands per OS
  references/frames.md              frames.py reference, read by the agent when needed
  assets/example-page/              page builder and template from the first run, to reuse
.claude-plugin/                     Claude Code plugin and marketplace manifests
.github/                            CI workflow, issue forms, pull request template
bench/                              benchmark: hand labels, scorer, labelling tool (not installed)
notebooks/gpu_ocr_benchmark.ipynb   OCR-mode comparison to run by hand on Colab or Kaggle
docs/                               install guide, benchmark, OCR and cloud findings, troubleshooting
```

Only `skills/video-notes/` is installed into agents. Keep anything the agent needs at run time
inside it, and anything for people developing the skill outside it.

## Development setup

Install the tools in [docs/install.md](docs/install.md#set-up-the-tools-once-per-machine), then:

```bash
git clone https://github.com/endgame302/video-notes.git
cd video-notes
python3 -m pip install -r skills/video-notes/requirements.txt
python3 skills/video-notes/scripts/check_deps.py
```

To use your working copy as the installed skill, link `skills/video-notes` into your agent's
skills folder (see [docs/install.md](docs/install.md#by-hand-any-agent-any-os)).

## Checks

CI runs on every push and pull request (`.github/workflows/ci.yml`). Run the same checks locally:

```bash
python3 .github/scripts/check_repo.py                      # skill spec, manifests, notebooks, scripts
python3 skills/video-notes/scripts/check_deps.py           # tools present
```

If you change `frames.py`, also run it on a real video and, for anything that changes which
frames are kept, score it on the benchmark.

## Changing what frames.py keeps

The thresholds in `frames.py` were tuned on the four hand-labelled test videos. A change that
affects which frames are kept needs before-and-after scores:

1. Download the test videos and run `frames.py` as in [bench/README.md](bench/README.md).
2. Score the current code with `python3 bench/score.py <work dir>`.
3. Make the change, run again into another folder (`--out`), and score that.
4. Put both sets of scores in the pull request. A change shouldn't lower coverage on any video
   without a good reason, and should say what it costs in frames to review.

The manifest's `gate` and `ocr.tile_tokens` fields let you try talking-head and rescue rules on
saved runs without OCR.

## Style

- Python: standard library first, then the packages in `requirements.txt`; no new dependency
  without a reason in the pull request. Scripts must work on Windows, macOS and Linux: use
  `pathlib`, read subprocess output as UTF-8, and don't assume a shell.
- `SKILL.md` must stay valid under the [Agent Skills spec](https://agentskills.io/specification)
  and agent-neutral: no tool names or placeholders specific to one agent.
- Docs: short, plain sentences; numbers with what they were measured on.

## Pull requests

1. Branch from `main` (`fix/…`, `feat/…`, `docs/…`).
2. Keep each pull request to one change, with a clear title in the imperative ("Add …", "Fix …").
3. Add an entry under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md).
4. Fill in the pull request template, including how you tested.

## Releases

Versions follow [Semantic Versioning](https://semver.org/). To release: move the `Unreleased`
entries into a new version section in `CHANGELOG.md`, bump `version` in
`.claude-plugin/plugin.json` and in the `metadata` of `skills/video-notes/SKILL.md`, merge, then
tag `vX.Y.Z` on `main` and publish a GitHub Release with that section as its notes.
