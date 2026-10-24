import sys
from PIL import Image, ImageDraw
import render as R
from brand import *
def sheet(times, out, cols=6, sc=3):
    w, h = FW//sc, FH//sc; rows = (len(times)+cols-1)//cols
    S = Image.new('RGB', (cols*w, rows*(h+16)), (20, 20, 20)); d = ImageDraw.Draw(S)
    for i, t in enumerate(times):
        im = R.frame(t); im = im.convert('RGB'); o = ImageDraw.Draw(im)
        o.rectangle([35, 220, 1045, 1470], outline=(255, 60, 60), width=4)          # safe zone (check only)
        o.rectangle([945, 1175, 1045, 1470], outline=(255, 200, 0), width=4)         # button column
        x, y = (i % cols)*w, (i//cols)*(h+16); S.paste(im.resize((w, h)), (x, y+16)); d.text((x+4, y+2), f'{t:.2f}s', fill=(255, 255, 255))
    S.save(out)
if __name__ == '__main__':
    sheet([float(x) for x in sys.argv[2:]], sys.argv[1])
