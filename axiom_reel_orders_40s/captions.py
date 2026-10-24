# -*- coding: utf-8 -*-
"""Burned-in Egyptian-Arabic captions = exactly the voiceover words, from shot 2 on (shot 1 carries the headline instead).
One fixed place: #262626 rounded box, y 1357-1433, x within 135-945. Cairo SemiBold 54 px (Arabic), DM Sans 500 (Latin words).
Current word white, other words silver (never graphite). Timing ESTIMATED from the voiceover (timing.json)."""
import os, re
from PIL import Image, ImageDraw, ImageFont
from brand import *
import timeline as T
from lib import S, HERE
Y0, CY = 1340, 1395
SZ = 54; MAXW = 720                        # box = text + 88 px, so box <= 808 px (x 136-944)
_f = {}
def F(kind, sz=SZ):
    k = (kind, sz)
    if k not in _f:
        if kind == 'ar': _f[k] = ImageFont.truetype(os.path.join(HERE, 'fonts', 'cairo-arabic-600-normal.woff'), sz*S, layout_engine=ImageFont.Layout.RAQM)
        else: _f[k] = ImageFont.truetype(os.path.join(HERE, 'fonts', FONTS['dm5']), int(sz*0.9*S))
    return _f[k]
def runs(tok): return [('lat' if re.search('[A-Za-z]', p) else 'ar', p) for p in tok.split(' ')]
def meas(kind, s): f = F(kind); return (f.getlength(s, direction='rtl', language='ar') if kind == 'ar' else f.getlength(s))/S
SP = F('ar').getlength(' ')/S
def tok_w(tok): rs = runs(tok); return sum(meas(k, s) for k, s in rs)+SP*(len(rs)-1)
def chunk(ws):
    out, cur = [], []
    for x in ws:
        n = cur+[x]; tot = sum(tok_w(y[0]) for y in n)+SP*(len(n)-1)
        if cur and (tot > MAXW or len(n) > 4): out.append(cur); cur = [x]
        else: cur = n
    return out+[cur]
CHUNKS = []                                 # (t0, t1, [(token, t0, t1)])
for key in T.CAP_KEYS:
    ws = [tuple(x) for x in T.WT[key]]; sent = chunk(ws)
    for c, ch in enumerate(sent):
        t0 = ch[0][1]
        t1 = sent[c+1][0][1] if c+1 < len(sent) and sent[c+1][0][1]-ch[-1][2] < 0.4 else ch[-1][2]+0.12
        if c+1 == len(sent): t1 = ch[-1][2]+0.12
        CHUNKS.append((t0, t1, ch))
CHUNKS.sort(key=lambda c: c[0])
def draw(bg, t):
    ch = next((c for c in CHUNKS if c[0]-0.05 <= t < c[1]), None)
    if ch is None: return
    t0, t1, words = ch; toks = [w[0] for w in words]; ws = [tok_w(x) for x in toks]; tot = sum(ws)+SP*(len(ws)-1)
    cur = max([j for j, w in enumerate(words) if w[1]-0.03 <= t] or [0])
    lay = Image.new('L', (FW*2, 110*2), 0); msk = Image.new('L', (FW*2, 110*2), 0); d = ImageDraw.Draw(lay); m = ImageDraw.Draw(msk)
    bx0, bx1 = 540-(tot+88)/2, 540+(tot+88)/2; r = [bx0*2, (1357-Y0)*2, bx1*2, (1433-Y0)*2]
    d.rounded_rectangle(r, radius=38*2, fill=CHARCOAL); m.rounded_rectangle(r, radius=38*2, fill=255)
    x = 540+tot/2; base = (CY-Y0)*2+15*2
    for j, tok in enumerate(toks):
        col = WHITE if j == cur else SILVER
        for kind, s in runs(tok):
            wd = meas(kind, s); x -= wd
            if kind == 'ar': d.text((x*2, base), s, font=F('ar'), fill=col, anchor='ls', direction='rtl', language='ar')
            else: d.text((x*2, base), s, font=F('lat'), fill=col, anchor='ls')
            x -= SP
    bg.paste(lay.reduce(2), (0, Y0), msk.reduce(2))
if __name__ == '__main__':
    bx = [(540-(sum(tok_w(w[0]) for w in c[2])+SP*(len(c[2])-1)+88)/2) for c in CHUNKS]
    print('chunks', len(CHUNKS), 'words/chunk', sorted({len(c[2]) for c in CHUNKS}), 'min box x', round(min(bx)), '| first caption at', CHUNKS[0][0])
