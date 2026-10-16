"""Contact sheet with the Reels safe-zone overlay (CHECK ONLY, never in the delivered video).
usage: python3 sheet.py out.png t1 t2 ...   (add --raw to skip overlay)"""
import sys, time
from PIL import Image, ImageDraw
import render as R

args = sys.argv[1:]
raw = "--raw" in args
args = [a for a in args if a != "--raw"]
times = [float(x) for x in args[1:]]
t0 = time.time()
ims = []
for t in times:
    im = R.frame_img(int(round(t * 30))).convert("RGB")
    if not raw:
        d = ImageDraw.Draw(im)
        d.rectangle([35, 220, 1045, 1470], outline=(255, 0, 255), width=3)
        d.rectangle([945, 1175, 1045, 1470], outline=(0, 255, 255), width=3)
    ims.append(im.resize((324, 576)))
print("sec/frame", (time.time() - t0) / len(ims))
cols = 6; rows = (len(ims) + cols - 1) // cols
sh = Image.new("RGB", (cols * 334, rows * 600), (30, 30, 30))
d = ImageDraw.Draw(sh)
for k, (im, t) in enumerate(zip(ims, times)):
    x = (k % cols) * 334 + 5; y = (k // cols) * 600 + 5
    sh.paste(im, (x, y)); d.text((x + 4, y + 580), f"{t:.2f}s", fill=(255, 255, 0))
sh.save(args[0])
