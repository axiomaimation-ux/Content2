"""Safe-zone check on every 0.1 s: bounding box of all content (after scaling) must sit inside the safe zone
and keep out of the right-hand button column (x 945-1045, y 1175-1470). The overlay is for checking only."""
import numpy as np
import render as R, timeline as T
from brand import *
x_lo, x_hi = SAFE['side'], FW-SAFE['side']; y_lo, y_hi = SAFE['top'], FH-SAFE['bottom']
worst = dict(l=9999, r=0, t=9999, b=0); bad = []; corner = 0
for k in range(int(T.TOTAL*10)):
    t = k/10; im = R.content(t); m = im.point(lambda v: 255 if v > 8 else 0); bb = m.getbbox()
    if not bb: continue
    l, tp, r, b = bb[0]+R.OX, bb[1]+R.OY, bb[2]+R.OX, bb[3]+R.OY
    worst['l'] = min(worst['l'], l); worst['r'] = max(worst['r'], r); worst['t'] = min(worst['t'], tp); worst['b'] = max(worst['b'], b)
    if l < x_lo or r > x_hi or tp < y_lo or b > y_hi: bad.append((t, bb))
    a = np.asarray(m)[1175-R.OY:1470-R.OY, 945-R.OX:1045-R.OX]
    if a.any(): corner += 1; bad.append((t, 'corner'))
print('extent l,t,r,b =', worst['l'], worst['t'], worst['r'], worst['b'], '| safe =', x_lo, y_lo, x_hi, y_hi)
print('violations:', len(bad), bad[:5])
