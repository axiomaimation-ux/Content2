"""Safe-zone + palette check. Content layer bbox at 10 fps must sit inside x 35-1045, y 220-1470 (after the 0.85 scale); right button column x 945-1045 y>=1175 must stay empty."""
import numpy as np, render as R, timeline as T
from brand import *
xs0, ys0, xs1, ys1, bad = 9999, 9999, 0, 0, 0
for i in range(0, int(T.TOTAL*10)):
    a = np.array(R.content(i/10)) > 30; ys, xs = np.nonzero(a)
    if len(xs) == 0: continue
    x0, x1, y0, y1 = xs.min()+R.OX, xs.max()+R.OX, ys.min()+R.OY, ys.max()+R.OY
    xs0, ys0, xs1, ys1 = min(xs0, x0), min(ys0, y0), max(xs1, x1), max(ys1, y1)
    col = a[(1175-R.OY):, (945-R.OX):]; bad += int(col.sum()>0)
print('content bbox x', xs0, xs1, 'y', ys0, ys1, '| safe x 35-1045 y 220-1470 | frames touching button column:', bad)
im = np.array(R.frame(21.0).convert('L')).ravel(); pal = np.array([0, 38, 85, 191, 255])
print('palette: share of pixels within 6 levels of the 5 values', round(float((np.abs(im[:, None]-pal[None]) <= 6).any(1).mean())*100, 2), '%')
