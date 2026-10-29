# Troubleshooting

| Message or symptom | Meaning and fix |
| --- | --- |
| `check_deps.py`: `MISSING …` | run the install command it prints for your OS |
| `Tesseract not found` | install Tesseract, or set `TESSERACT` to the executable |
| `OpenCV ... has no face detector` / `face model is missing` | `pip install "opencv-python<5"`: OpenCV 5 removed the face detector, and some distro builds omit its model |
| `needs ~N GB free` | free disk space, or pass `--out` to a folder on another drive |
| `GPU decode unavailable; decoded on the CPU` (warning) | no working GPU decoder; slower but correct |
| `decode skipped frames` / `decode stopped early` | a damaged or partial download; download again |
| `N OCR batches failed and were redone frame by frame` (warning) | an unreadable frame image; results are still complete |
| `below 1080p` (warning) | download the 1080p stream |
| `RapidOCR is running on the CPU` (warning) | `--ocr hybrid` without a GPU: correct, a few minutes slower |
| `--ocr rapidocr/hybrid needs RapidOCR` | `pip install rapidocr onnxruntime`, or drop `--ocr` |
| `outcome counts don't balance` | a bug in `frames.py`; please [open a bug report](https://github.com/endgame302/video-notes/issues/new?template=bug-report.yml) with the manifest |
| The agent doesn't see the skill | check the folder is `<skills dir>/video-notes/SKILL.md` (not nested one level deeper) and restart the agent |

## `cloud_frames.py` (Kaggle)

| Message | Meaning and fix |
| --- | --- |
| `the Kaggle CLI is missing` | `pip install kaggle` |
| `not signed in to Kaggle` | run `kaggle auth login` once and approve in the browser |
| `dataset processing failed` / `still isn't live on Kaggle` | Kaggle is slow or rejected the upload; run again |
| `no frames.json came back` | the Kaggle script failed; the message ends with its log. Internet in Kaggle scripts needs a phone-verified account |
| YouTube: `Sign in to confirm you're not a bot` | only seen on cloud machines; `cloud_frames.py` downloads on your machine for this reason |
