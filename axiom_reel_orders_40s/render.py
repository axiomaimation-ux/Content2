import sys, subprocess, time, numpy as np
from multiprocessing import Pool
from PIL import Image, ImageChops, ImageDraw
from brand import *
import timeline as T, lib, captions
from scenes import SCENE_FN
CX, CY = SAFE_CENTER

def build_bg():
    S2 = 2; H = FH+LOOP; im = Image.new('L', (FW*S2, H*S2), 0); d = ImageDraw.Draw(im)
    for j in range(-1, H//GRID+2):
        for i in range(-1, FW//GRID+2):
            x, y = (i*GRID+30)*S2, (j*GRID+30)*S2
            if i % 4 == 0 and j % 4 == 0:
                d.line([(x-7*S2, y), (x+7*S2, y)], fill=GRAPHITE, width=3); d.line([(x, y-7*S2), (x, y+7*S2)], fill=GRAPHITE, width=3)
            else: d.ellipse([x-2.2*S2, y-2.2*S2, x+2.2*S2, y+2.2*S2], fill=CHARCOAL)
    return im
BG = build_bg()
def bg_frame(t):
    off = int(round((DRIFT*t) % LOOP*2)); return BG.crop((0, off, FW*2, off+FH*2)).reduce(2)
def scene_of(tg):
    for n, s, e in T.SCENES:
        if s <= tg < e: return n
    return T.SCENES[-1][0]
def scene_img(name, tg):
    """Scene content on a full-frame black layer, scaled by the scene's K about the safe-zone centre (540, 845)."""
    c = lib.Cv(); SCENE_FN[name](c, tg-T.START[name]); K = SCENE_K[name]
    if K == 1.0: return c.im.reduce(2) if False else c.im.resize((FW, FH), Image.LANCZOS)
    cw, ch = round(FW*K), round(FH*K); out = Image.new('L', (FW, FH), 0)
    out.paste(c.im.resize((cw, ch), Image.LANCZOS), (round(CX*(1-K)), round(CY*(1-K)))); return out
def content(tg):
    tg = min(max(tg, 0), T.TOTAL-1e-6)
    for tc in T.TRANS:
        if abs(tg-tc) < T.TD/2:
            prev = [n for n, s, e in T.SCENES if abs(e-tc) < 1e-6][0]; nxt = [n for n, s, e in T.SCENES if abs(s-tc) < 1e-6][0]
            return Image.blend(scene_img(prev, tg), scene_img(nxt, tg), (tg-(tc-T.TD/2))/T.TD)
    return scene_img(scene_of(tg), tg)
def frame(tg, caps=True):
    bg = bg_frame(tg); cont = content(tg)
    out = ImageChops.lighter(bg, cont)
    if scene_of(min(max(tg, 0), T.TOTAL-1e-6)) == 'S6':          # white block keeps the dot grid: dots/plus marks in Silver on white
        b = np.array(bg) > 0; o = np.array(out); o[(o == 255) & b] = SILVER; out = Image.fromarray(o)
    if caps: captions.draw(out, tg)
    return out
def _f(i): return frame(i/FPS).convert('RGB').tobytes()
def render(out, nproc=2):
    n = round(T.TOTAL*FPS)
    cmd = ['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{FW}x{FH}','-r',str(FPS),'-i','-',
           '-c:v','libx264','-preset','veryfast','-crf','16','-profile:v','high','-pix_fmt','yuv420p','-movflags','+faststart',out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time()
    with Pool(nproc) as pool:
        for i, b in enumerate(pool.imap(_f, range(n), chunksize=4)):
            p.stdin.write(b)
            if i % 150 == 0: print(i, f'{time.time()-t0:.0f}s', flush=True)
    p.stdin.close(); p.wait(); print('done', f'{time.time()-t0:.0f}s')
if __name__ == '__main__':
    if sys.argv[1] == 'test':
        t0 = time.time()
        for tt in map(float, sys.argv[2:]): frame(tt).save(f'/tmp/f_{tt:05.2f}.png')
        print('per frame', (time.time()-t0)/len(sys.argv[2:]))
    else: render(sys.argv[2])
