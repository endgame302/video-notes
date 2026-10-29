# OCR engines, GPUs and cloud runs

What was tried to make screenshot capture more accurate and to run it off the user's machine,
and what was measured. Coverage is scored with `bench/score.py` against the hand labels (see
[`benchmark.md`](benchmark.md)).

## Coverage by OCR mode

| Video | Tesseract (default) | `--ocr hybrid` | `--ocr rapidocr` |
| --- | --- | --- | --- |
| Tom Scott (talking head + pages) | 72%, 56 frames | **90%, 70 frames** | 83%, 45 frames |
| Bookfox (talking head + captions) | 76%, 179 frames | 76%, 193 frames | 80%, 194 frames |
| Bro Code (coding screencast) | 100%, 206 frames | same as Tesseract | **36%**, 16 frames |
| Fireship (fast-cut news) | 98%, 187 frames | same as Tesseract | 95%, 164 frames |

Hybrid and RapidOCR runs were on Kaggle's T4; Tesseract on the i5-10300H. Kaggle's Tesseract
(5.3) gives the same coverage as the local one (5.4) with a few frames a second apart.

- **Hybrid** keeps Tesseract for every frame and runs RapidOCR only on the talking-head review
  tiles. On Tom Scott it caught the overlays Tesseract reads as nothing ("screen-scrapers",
  "200 OK", "Web 2.0", "Yahoo Pipes", a reCAPTCHA box). Videos with no host on camera have no
  tiles, so it changes nothing there.
- **Background text** in the host's shot nearly sank it: Bookfox has a sign that RapidOCR
  misreads differently on each tile ("boivs", "beyys", "bciys", "buokhure"). Without a filter,
  hybrid added 42 off-target frames; ignoring tokens on 3+ tiles cut that to 28; also treating
  near spellings with the same first letter (similarity ≥ 0.7) as the same token cut it to 14,
  with no loss on Tom Scott. The rule was tuned offline on the saved `ocr.tile_tokens`.
- **Full RapidOCR** reads every menu and panel of a code editor, so consecutive code steps
  share most of their words and the dedup (tuned on Tesseract's output) merges them. It stays
  experimental.

## Text accuracy

On 16 frames of a long course video whose text was checked by eye, RapidOCR read 43 of 44
strings and Tesseract 39 (measured in a separate session, `C:\vn_yulW\bench\compare_ab.py`).
Running RapidOCR on only the ~50 screenshots used in a set of notes took about 54 s on the GTX
1650. The skill uses it for text copied into the notes when it's installed.

## Speed

| | Seconds per frame |
| --- | --- |
| Tesseract, 6 processes, i5-10300H | 0.08–0.29 (more text, slower) |
| Tesseract, Colab (2 vCPUs) | about 1.0 |
| RapidOCR, GTX 1650 (DirectML) | 0.67 |
| RapidOCR, Colab T4 (CUDA via PyTorch) | 0.60–0.68 |
| RapidOCR, Kaggle T4 | 0.23 (light text) – 0.6 (coding screen) |
| RapidOCR, any CPU | about 4.6 |

RapidOCR's time grows with the amount of text (it reads line by line); another session saw
0.5 s on a light screen and 4 s on a dense dashboard with the same GPU. On Colab the GPU sat
mostly idle: preprocessing on its 2 slow cores was the bottleneck, which is why Kaggle's T4,
on a stronger CPU, was about 3× faster. RapidOCR's own docs advise against its onnxruntime-gpu
path, so CUDA goes through PyTorch.

## Where to run it

| | Your machine | Colab | Kaggle |
| --- | --- | --- | --- |
| Downloads from YouTube | yes | blocked on most machines | blocked (not tried directly; same cloud problem) |
| Hands-off | yes | no: needs a browser session every time | **yes, through the official CLI** |
| CPU | 4 cores / 8 threads | 2 vCPUs | 4 cores (CPU session), fewer with a GPU |
| GPU | GTX 1650 | T4 (free, one session at a time) | T4 (free, 30 h a week) |

Colab was tried first and abandoned: no API for headless runs, a page that lost its connection to
a running notebook, one GPU session at a time, and YouTube blocking its downloads on most
machines. `scripts/cloud_frames.py` uses Kaggle instead: download here, upload a private dataset,
run a private script, fetch `frames/`. Three bugs found on the way: Kaggle reported the dataset
ready before the new version was attached (it now waits for `video.mp4` at the uploaded size); a
local video was copied before upload (now hard-linked); a failed run left the copy behind (now
always removed).

`notebooks/gpu_ocr_benchmark.ipynb` runs the OCR-mode comparison on Colab or Kaggle by hand.
