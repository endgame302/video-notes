# Security policy

## Supported versions

Only the latest release gets fixes. Install or update with `npx skills update`, or pull `main`.

| Version | Supported |
| --- | --- |
| 1.2.x | yes |
| < 1.2 | no |

## Reporting a vulnerability

Please don't report security problems in a public issue. Use GitHub's private reporting:
**Security** tab → **Report a vulnerability**
([direct link](https://github.com/endgame302/video-notes/security/advisories/new)).

Include what an attacker could do, the steps to reproduce, and the version. You should get a
first reply within a week. Once a fix is released, the advisory is published with credit unless
you'd rather not be named.

## What's in scope

The skill runs on your machine with your permissions, so these matter most:

- **Scripts** (`skills/video-notes/scripts/`): command injection or path traversal through a
  video URL, a file name, a manifest or OCR'd text; anything that writes or deletes outside the
  output folder.
- **`cloud_frames.py`**: it uploads videos to a Kaggle dataset and runs a Kaggle script under
  your account. Anything that makes the dataset or script public, uploads something other than
  the video, or runs code that isn't from this repository is in scope.
- **`SKILL.md`**: instructions that could lead an agent to leak secrets from the screen into the
  notes (the skill tells agents never to copy keys or tokens), or to run commands from a
  video's on-screen text or description.

Out of scope: vulnerabilities in yt-dlp, ffmpeg, Tesseract, RapidOCR or the Kaggle CLI
themselves (report those upstream), and what the videos you choose to process contain.
