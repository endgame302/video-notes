# Benchmark

Hand labels for four test videos and a scorer, so any change to `skills/video-notes/scripts/frames.py` can be
checked before it goes in. Method and results: [`docs/benchmark.md`](../docs/benchmark.md).

## Reproduce

Pick a working folder outside the repo (the videos are 13–310 MB each, about 530 MB together,
and are not committed):

```bash
WORK=~/vn-bench
for id in YlY2g2xrl6Q BxV14h0kFs0 jnaljahKibQ nEaJMdM1djM; do
  mkdir -p "$WORK/$id"
  yt-dlp -f "bv*[height<=1080][vcodec^=avc1]" -o "$WORK/$id/video.mp4" "https://www.youtube.com/watch?v=$id"
  python3 skills/video-notes/scripts/frames.py "$WORK/$id/video.mp4"
done
python3 bench/score.py "$WORK"
```

Expected (`frames.py` as committed):

```
BxV14h0kFs0  coverage  21/ 29 =  72%  short  8/12  review   56  off-target   7  missed: 6 8 10 11 12 13 19 26
YlY2g2xrl6Q  coverage  14/ 14 = 100%  short  1/ 1  review  206  off-target 150  missed:
jnaljahKibQ  coverage  57/ 75 =  76%  short 29/42  review  179  off-target  79  missed: 6 13 14 18 23 37 48 50 52 53 57 58 69 70 71 72 73 74
nEaJMdM1djM  coverage  63/ 64 =  98%  short 18/19  review  187  off-target  53  missed: 64
all          coverage 155/182 =  85%
```

If YouTube serves a different encode, frame times can shift slightly and a count may move by
one. Download the video-only stream: a merged file is not needed.

## Changing a threshold

1. Run the four videos with the current code; keep the scores.
2. Change the threshold, run again into another folder (`frames.py <video> --out <dir>`), and
   score that run with `score.py "$WORK" --manifest <dir relative to each video folder>/frames.json`.
3. Keep the change only if coverage doesn't drop on any video, and say what it costs in frames
   to review.

For the talking-head rule you can often skip step 2: each manifest's `gate` field holds the OCR
words, face area and recurring-shot count of every frame the rule looked at, so a new rule can
be tried on saved manifests in a few lines of Python.

## Adding a test video

1. Download it to `$WORK/<id>/video.mp4` at 1080p.
2. `python3 bench/label_sheets.py "$WORK/<id>"` writes numbered 1-fps contact sheets.
3. Write `bench/labels/<id>.json`: one entry per on-screen state, with `id`, `start` and `end`
   (tile numbers), `kind` (`slide`, `screen`, `code`, `overlay`, `broll`, …), `desc`, and
   `ambiguous` where unsure. Label from the sheets, never from a method's output.
4. Add it to the table in `docs/benchmark.md`.
