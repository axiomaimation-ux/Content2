"""Safe-zone, palette, static-frame and stray-mark check (content layer only; captions checked separately)."""
import numpy as np, render as R, timeline as T, captions as C
from brand import *
xs0, ys0, xs1, ys1, bad, worst = 9999, 9999, 0, 0, 0, None
prev = None; static = 0; maxstatic = 0
for i in range(0, int(T.TOTAL*10)):
    t = i/10; a = np.array(R.content(t)) > 30
    if t >= 21.0 and t < 22.3: pass
    ys, xs = np.nonzero(a)
    if len(xs) == 0: continue
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    if R.scene_of(t) != 'S6': xs0, ys0, xs1, ys1 = min(xs0, x0), min(ys0, y0), max(xs1, x1), max(ys1, y1)
    if R.scene_of(t) != 'S6': bad += int(a[1175:, 945:].sum() > 0)
print('content bbox (excl. white block S6) x', xs0, xs1, 'y', ys0, ys1, '| safe x 35-1045, y 220-1470 | frames touching button column:', bad)
# caption box extents
bx = [(540-(sum(C.tok_w(w[0]) for w in c[2])+C.SP*(len(c[2])-1)+88)/2) for c in C.CHUNKS]
print('caption box: min x', round(min(bx)), 'max right', round(540+(540-min(bx))), '| y 1357-1433 (limit 1470) | first caption at', round(C.CHUNKS[0][0], 2))
# palette on stable frames
pal = np.array([0, 38, 85, 191, 255])
for tt in (7.0, 14.0, 30.0, 39.8):
    im = np.array(R.frame(tt).convert('L')).ravel()
    print('palette', tt, round(float((np.abs(im[:, None]-pal[None]) <= 6).any(1).mean())*100, 2), '%')
# motion: max run of identical consecutive frames (content+bg)
last = None; run = 0; mx = 0
for i in range(0, int(T.TOTAL*30), 1):
    f = np.array(R.frame(i/30, caps=False).convert('L'), dtype=np.int16)[220:1470:4, ::4]
    c = np.array(R.content(i/30))[220:1470:4, ::4].astype(np.int16)
    if last is not None and np.abs(c-last).max() < 3: run += 1; mx = max(mx, run)
    else: run = 0
    last = c
print('longest static content run (frames):', mx+1, '=', round((mx+1)/30, 2), 's')
