import sys, subprocess, time, numpy as np
from PIL import Image, ImageChops, ImageDraw
from brand import *
import timeline as T, lib, captions
from scenes import SCENE_FN

K = CONTENT_SCALE; CX, CY = SAFE_CENTER
CW, CH_ = round(FW*K), round(FH*K); OX, OY = round(CX*(1-K)), round(CY*(1-K))   # content layer size and paste origin

def build_bg():
    """2x supersampled dot grid, tall enough to loop every 240 px (4 cells)."""
    S2 = 2; H = FH+LOOP; im = Image.new('L', (FW*S2, H*S2), 0); d = ImageDraw.Draw(im)
    for j in range(-1, H//GRID+2):
        for i in range(-1, FW//GRID+2):
            x, y = (i*GRID+30)*S2, (j*GRID+30)*S2
            if i % 4 == 0 and j % 4 == 0:   # "+" mark, graphite, ~14 px, 1.5 px stroke
                d.line([(x-7*S2, y), (x+7*S2, y)], fill=GRAPHITE, width=3); d.line([(x, y-7*S2), (x, y+7*S2)], fill=GRAPHITE, width=3)
            else: d.ellipse([x-2.2*S2, y-2.2*S2, x+2.2*S2, y+2.2*S2], fill=CHARCOAL)
    return im
BG = build_bg()
def bg_frame(t):
    off = int(round((DRIFT*t) % LOOP*2)); return BG.crop((0, off, FW*2, off+FH*2)).reduce(2)

def scene_img(name, tl):
    c = lib.Cv(); SCENE_FN[name](c, tl); return c.im.resize((CW, CH_), Image.LANCZOS)

def content(tg):
    tg = min(max(tg, 0), T.TOTAL-1e-6)
    for tc in T.TRANS:
        if abs(tg-tc) < T.TD/2:
            prev = [n for n, s, d in T.SCENES if s+d == tc][0]; nxt = [n for n, s, d in T.SCENES if s == tc][0]
            w = (tg-(tc-T.TD/2))/T.TD
            return Image.blend(scene_img(prev, T.DUR[prev]+(tg-tc)), scene_img(nxt, max(0, tg-tc)), w)
    for n, s, d in T.SCENES:
        if s <= tg < s+d: return scene_img(n, tg-s)

def frame(tg):
    bg = bg_frame(tg); cont = content(tg); box = (OX, OY, OX+CW, OY+CH_)
    bg.paste(ImageChops.lighter(bg.crop(box), cont), box); captions.draw(bg, tg); return bg, cont

def render(out, f0=0, f1=None):
    f1 = f1 or round(T.TOTAL*FPS)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time()
    for f in range(f0, f1):
        im, _ = frame(f/FPS); p.stdin.write(im.convert('RGB').tobytes())
        if f % 60 == 0: print(f, f'{time.time()-t0:.0f}s', flush=True)
    p.stdin.close(); p.wait(); print('done', time.time()-t0)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'test':
        times = [float(x) for x in sys.argv[2:]]; t0 = time.time()
        for tt in times:
            im, _ = frame(tt); im.save(f'/tmp/f_{tt:05.2f}.png')
        print('per frame', (time.time()-t0)/len(times))
    elif mode == 'video': render(sys.argv[2] if len(sys.argv) > 2 else 'video_silent.mp4')
