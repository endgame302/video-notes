"""Numbered 1-fps contact sheets for hand-labelling a new test video.

usage: label_sheets.py <video_dir>     (expects <video_dir>/video.mp4)

Writes <video_dir>/sheet_000.jpg ... (5 x 6 tiles, each stamped m:ss) from 1-fps frames in
<video_dir>/lab/. Independent of frames.py on purpose: labels made from these sheets must not
depend on the method being scored. Tile k shows real time k + 0.5 s; see score.py.
"""
import subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

d = Path(sys.argv[1])
lab = d / "lab"
lab.mkdir(exist_ok=True)
if not any(lab.glob("f_*.jpg")):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(d / "video.mp4"),
                    "-vf", "fps=1,scale=384:216", "-q:v", "4", str(lab / "f_%05d.jpg")], check=True)
frames = sorted(lab.glob("f_*.jpg"))   # f_00001 = t 0 s (fps filter starts at 0)
try:
    font = ImageFont.truetype("arialbd.ttf", 22)
except OSError:
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
C, R = 5, 6
for s in range(0, len(frames), C * R):
    sheet = Image.new("RGB", (C * 384, R * 216), "black")
    for j, f in enumerate(frames[s:s + C * R]):
        t = int(f.stem[2:]) - 1
        x, y = (j % C) * 384, (j // C) * 216
        sheet.paste(Image.open(f), (x, y))
        ImageDraw.Draw(sheet).text((x + 4, y + 2), f"{t // 60}:{t % 60:02d}", fill="yellow", font=font,
                                   stroke_width=2, stroke_fill="black")
    sheet.save(d / f"sheet_{s // (C * R):03d}.jpg", quality=80)
print(d.name, len(frames), "frames,", (len(frames) + C * R - 1) // (C * R), "sheets")
