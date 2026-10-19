# -*- coding: utf-8 -*-
"""Burned-in Egyptian-Arabic captions, exactly the voiceover script. One line, 3-4 words, rounded #262626 box, y 1357-1433, x within 140-940.
Current word white, spoken silver, upcoming graphite. Arabic words in Cairo SemiBold (the one font exception), Latin words (Axiom, AI, APIs, DM) in DM Sans 500.
Word timing is ESTIMATED from the voiceover (timing.json)."""
import math, os, re
from PIL import Image, ImageDraw, ImageFont
from brand import *
import timeline as T
from lib import S, HERE
Y0, CY = 1340, 1395
_f = {}
def F(kind, sz):
    k = (kind, sz)
    if k not in _f:
        if kind == 'ar': _f[k] = ImageFont.truetype(os.path.join(HERE, 'fonts', 'cairo-arabic-600-normal.woff'), sz*S, layout_engine=ImageFont.Layout.RAQM)
        else: _f[k] = ImageFont.truetype(os.path.join(HERE, 'fonts', FONTS['dm5']), int(sz*0.9*S))
    return _f[k]
def runs(tok):
    out = []
    for part in tok.split(' '): out.append(('lat' if re.search('[A-Za-z]', part) else 'ar', part))
    return out                                   # reading order (first run is rightmost)
def meas(kind, sz, s): f = F('ar' if kind == 'ar' else 'lat', sz); return (f.getlength(s, direction='rtl', language='ar') if kind == 'ar' else f.getlength(s))/S
def tok_w(tok, sz):
    rs = runs(tok); sp = F('ar', sz).getlength(' ')/S
    return sum(meas(k, sz, s) for k, s in rs)+sp*(len(rs)-1), sp
CHUNKS = []                                     # (t0, t1, [(token, t0, t1)])
for key in ('S1','S2','S3','S4','S5','S6','S7','S8','S9','S10'):
    ws = T.WT[key]; n = len(ws); k = math.ceil(n/4); base, extra = divmod(n, k); p = 0; sent = []
    for c in range(k):
        m = base+(1 if c < extra else 0); sent.append(ws[p:p+m]); p += m
    for c, ch in enumerate(sent):
        t0 = ch[0][1]
        t1 = sent[c+1][0][1] if c+1 < len(sent) and sent[c+1][0][1]-ch[-1][2] < 0.4 else ch[-1][2]+0.12
        if c+1 == len(sent): t1 = ch[-1][2]+0.12
        CHUNKS.append((t0, t1, [(x[0], x[1], x[2]) for x in ch]))
def layout(toks):
    sz = 46
    while True:
        ws = [tok_w(t, sz)[0] for t in toks]; sp = F('ar', sz).getlength(' ')/S; tot = sum(ws)+sp*(len(ws)-1)
        if tot+88 <= 800: return sz, ws, sp, tot
        sz -= 2
def box_for(toks): sz, ws, sp, tot = layout(toks); return (540-(tot+88)/2, 1357, 540+(tot+88)/2, 1433)
def draw(bg, t):
    ch = next((c for c in CHUNKS if c[0]-0.05 <= t < c[1]), None)
    if ch is None: return
    t0, t1, words = ch; toks = [w[0] for w in words]; sz, ws, sp, tot = layout(toks)
    cur = max([j for j, w in enumerate(words) if w[1]-0.03 <= t] or [0])
    lay = Image.new('L', (FW*2, 110*2), 0); msk = Image.new('L', (FW*2, 110*2), 0); d = ImageDraw.Draw(lay); m = ImageDraw.Draw(msk)
    bx0, by0, bx1, by1 = box_for(toks); r = [bx0*2, (by0-Y0)*2, bx1*2, (by1-Y0)*2]
    d.rounded_rectangle(r, radius=38*2, fill=CHARCOAL); m.rounded_rectangle(r, radius=38*2, fill=255)
    x = 540+tot/2; base = (CY-Y0)*2+14*2           # RTL: first word on the right
    for j, tok in enumerate(toks):
        col = WHITE if j == cur else SILVER if j < cur else GRAPHITE
        for kind, s in runs(tok):
            wd = meas(kind, sz, s); x -= wd
            if kind == 'ar': d.text((x*2, base), s, font=F('ar', sz), fill=col, anchor='ls', direction='rtl', language='ar')
            else: d.text((x*2, base), s, font=F('lat', sz), fill=col, anchor='ls')
            x -= sp
        x += sp-sp                                 # (spacing already applied per run)
    bg.paste(lay.reduce(2), (0, Y0), msk.reduce(2))
if __name__ == '__main__':
    bx = [box_for([w[0] for w in c[2]]) for c in CHUNKS]
    print('chunks', len(CHUNKS), 'words/chunk', sorted({len(c[2]) for c in CHUNKS}), 'box x', min(b[0] for b in bx), max(b[2] for b in bx), 'y 1357-1433')
