import math, random, os
from PIL import Image, ImageDraw, ImageFont
from brand import *
S = 2                                   # 2x supersampling
WH, SIL, GRA, CH, BK = WHITE, SILVER, GRAPHITE, CHARCOAL, BLACK
HERE = os.path.dirname(os.path.abspath(__file__))
_fc = {}
def font(n, sz):
    k = (n, sz)
    if k not in _fc: _fc[k] = ImageFont.truetype(os.path.join(HERE, 'fonts', FONTS[n]), int(round(sz*S)))
    return _fc[k]
def cl(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def ap(t, t0, d): return cl((t-t0)/d)
def eo(x): return 1-(1-x)**3
def eio(x): return x*x*(3-2*x)
def lerp(a, b, x): return a+(b-a)*x
def g(v, a=1.0): return int(round(cl(v*a, 0, 255)))
def tw(fn, sz, s, track=0): return font(fn, sz).getlength(s)/S + track*max(0, len(s)-1)

class Cv:
    def __init__(s):
        s.im = Image.new('L', (FW*S, FH*S), 0); s.d = ImageDraw.Draw(s.im)
    def rect(s, x0, y0, x1, y1, fill=None, line=None, r=0, w=2):
        s.d.rounded_rectangle([x0*S, y0*S, x1*S, y1*S], radius=r*S, fill=fill, outline=line, width=max(1, int(w*S)))
    def ell(s, cx, cy, rx, ry=None, fill=None, line=None, w=2):
        ry = rx if ry is None else ry
        s.d.ellipse([(cx-rx)*S, (cy-ry)*S, (cx+rx)*S, (cy+ry)*S], fill=fill, outline=line, width=max(1, int(w*S)))
    def ln(s, pts, fill, w=2):
        s.d.line([(x*S, y*S) for x, y in pts], fill=fill, width=max(1, int(w*S)), joint='curve')
    def poly(s, pts, fill): s.d.polygon([(x*S, y*S) for x, y in pts], fill=fill)
    def arc(s, cx, cy, r, a0, a1, fill, w=2):
        s.d.arc([(cx-r)*S, (cy-r)*S, (cx+r)*S, (cy+r)*S], a0, a1, fill=fill, width=max(1, int(w*S)))
    def tx(s, x, y, t, fn, sz, fill, anc='lm', track=0):
        f = font(fn, sz)
        if track == 0:
            s.d.text((x*S, y*S), t, font=f, fill=fill, anchor=anc); return
        w = tw(fn, sz, t, track); h = anc[0]
        x0 = x if h == 'l' else x-w/2 if h == 'm' else x-w
        for ch in t:
            s.d.text((x0*S, y*S), ch, font=f, fill=fill, anchor='l'+anc[1]); x0 += f.getlength(ch)/S+track

def wrap(txt, fn='sg6', sz=58, maxw=940):
    out, cur = [], ''
    for w in txt.split():
        n = (cur+' '+w).strip()
        if tw(fn, sz, n) <= maxw: cur = n
        else: out.append(cur); cur = w
    return out+[cur]

def appear(t, t0, d=0.35, floor=0.0):
    a = max(floor, eo(ap(t, t0, d))); return a, (1-a)*18

def head(c, t, items):
    for i, (t0, t1, lab, txt) in enumerate(items):
        if t < t0-0.16: continue
        ain = (0.55+0.45*eo(ap(t, t0, 0.4))) if i == 0 else eo(ap(t, t0-0.15, 0.3))
        aout = 1-ap(t, t1-0.15, 0.15) if i < len(items)-1 else 1.0
        a = min(ain, aout)
        if a <= 0.01: continue
        dy = (1-eo(ap(t, t0, 0.4)))*14 if i > 0 else 0
        if lab: c.tx(70, 262+dy, lab, 'dm5', 30, g(SIL, a), 'lm', track=6)
        for k, l in enumerate(wrap(txt)): c.tx(70, 332+dy+k*68, l, 'sg6', 58, g(WH, a), 'lm')

def card(c, x0, y0, x1, y1, a=1, hi=0, fw=0, r=16):
    c.rect(x0, y0, x1, y1, fill=g(lerp(CH, WH, fw), a), line=g(lerp(GRA, WH, max(hi, fw)), a), r=r, w=2)
def block(c, cx, cy, w, h, label, hi=0, fw=0, a=1, sz=30):
    card(c, cx-w/2, cy-h/2, cx+w/2, cy+h/2, a, hi, fw)
    c.tx(cx, cy, label, 'dm5', sz, g(lerp(lerp(GRA, WH, hi), BK, fw), a), 'mm', track=3)
def bubble(c, x0, y0, w, h, txt, kind, a=1, sz=30):
    if kind == 'out':
        c.rect(x0, y0, x0+w, y0+h, fill=g(WH, a), r=h/2); col = 0
    else:
        c.rect(x0, y0, x0+w, y0+h, fill=g(CH, a), line=g(GRA, a), r=h/2, w=2); col = g(SIL, a)
    c.tx(x0+h*0.55, y0+h/2, txt, 'dm5', sz, col)

# ---- icons ----
def person(c, cx, cy, s, col):
    c.ell(cx, cy-s*0.28, s*0.2, fill=col)
    c.d.pieslice([(cx-s*0.38)*S, (cy+s*0.02)*S, (cx+s*0.38)*S, (cy+s*0.78)*S], 180, 360, fill=col)
def clock(c, cx, cy, r, m, col, w=3):
    c.ell(cx, cy, r, line=col, w=w)
    for i in range(12):
        a = math.radians(i*30)
        c.ln([(cx+math.sin(a)*r*0.82, cy-math.cos(a)*r*0.82), (cx+math.sin(a)*r*0.93, cy-math.cos(a)*r*0.93)], col, w*0.7)
    a = math.radians(m); c.ln([(cx, cy), (cx+math.sin(a)*r*0.75, cy-math.cos(a)*r*0.75)], col, w)
    a = math.radians(m/12); c.ln([(cx, cy), (cx+math.sin(a)*r*0.45, cy-math.cos(a)*r*0.45)], col, w*1.3)
    c.ell(cx, cy, w*1.4, fill=col)
def check(c, cx, cy, s, col, w=5): c.ln([(cx-s*0.5, cy), (cx-s*0.12, cy+s*0.4), (cx+s*0.55, cy-s*0.4)], col, w)
def cross(c, cx, cy, s, col, w=5):
    c.ln([(cx-s/2, cy-s/2), (cx+s/2, cy+s/2)], col, w); c.ln([(cx-s/2, cy+s/2), (cx+s/2, cy-s/2)], col, w)
def cart(c, cx, cy, s, col, w=4):
    c.ln([(cx-s*.55, cy-s*.45), (cx-s*.35, cy-s*.45), (cx-s*.15, cy+s*.2), (cx+s*.4, cy+s*.2), (cx+s*.5, cy-s*.25), (cx-s*.28, cy-s*.25)], col, w)
    c.ell(cx-s*.08, cy+s*.42, s*.07, fill=col); c.ell(cx+s*.32, cy+s*.42, s*.07, fill=col)
def gear(c, cx, cy, r, col):
    pts = []
    for i in range(8):
        b = i*45
        for da, rr in ((-18, .78), (-10, 1), (10, 1), (18, .78)):
            a = math.radians(b+da); pts.append((cx+math.cos(a)*r*rr, cy+math.sin(a)*r*rr))
    c.poly(pts, col); c.ell(cx, cy, r*0.38, fill=BK)
def chat_icon(c, cx, cy, s, col):
    c.rect(cx-s/2, cy-s*.4, cx+s/2, cy+s*.25, line=col, r=s*.18, w=3)
    c.poly([(cx-s*.25, cy+s*.2), (cx-s*.35, cy+s*.5), (cx-s*.05, cy+s*.2)], col)
def browser_icon(c, cx, cy, s, col):
    c.rect(cx-s/2, cy-s*.4, cx+s/2, cy+s*.4, line=col, r=s*.1, w=3)
    c.ln([(cx-s/2, cy-s*.15), (cx+s/2, cy-s*.15)], col, 3); c.ell(cx-s*.33, cy-s*.27, 2.5, fill=col)
def cyl(c, cx, cy, w, h, cols):
    ry = h*0.13; x0, x1 = cx-w/2, cx+w/2; top = cy-h/2+ry; bot = cy+h/2-ry
    c.ell(cx, top, w/2, ry, line=cols[0], w=3)
    c.ln([(x0, top), (x0, bot)], cols[0], 3); c.ln([(x1, top), (x1, bot)], cols[0], 3)
    ys = [top+(bot-top)*k/3 for k in (1, 2, 3)]
    for k, y in enumerate(ys):
        c.d.arc([x0*S, (y-ry)*S, x1*S, (y+ry)*S], 0, 180, fill=cols[k], width=int(3*S))
def sparkle_ring(c, cx, cy, r0, r1, p, col=SIL, w=3):
    if 0 < p < 1:
        r = lerp(r0, r1, eo(p)); c.ell(cx, cy, r, line=g(col, 1-p), w=w)

def bolt(c, p0, p1, t, prog, a=1.0, amp=22):
    """Electricity from p0 to p1; prog 0..1.6 (head arrives at 1.0, tail gone at 1.6)."""
    if prog <= 0 or prog >= 1.6: return
    x0, y0 = p0; x1, y1 = p1; L = math.hypot(x1-x0, y1-y0)
    ux, uy = (x1-x0)/L, (y1-y0)/L; nx, ny = -uy, ux
    head_s = min(prog, 1.0); tail_s = max(0.0, prog-0.6)
    n = max(3, int(L*(head_s-tail_s)/24))
    seed = int(t*15)*7919 + int(x0+y0)
    for bi, (w, col, am) in enumerate(((6, WH, amp), (3, SIL, amp*1.3))):
        rng = random.Random(seed+bi*101); pts = []
        for k in range(n+1):
            s_ = lerp(tail_s, head_s, k/n); off = 0 if k in (0, n) else (rng.random()-.5)*2*am
            pts.append((x0+ux*L*s_+nx*off, y0+uy*L*s_+ny*off))
        c.ln(pts, g(col, a), w)
    hx, hy = x0+ux*L*head_s, y0+uy*L*head_s
    if prog < 1.0: c.ell(hx, hy, 9, fill=g(WH, a))
    if 1.0 <= prog < 1.4:
        rng = random.Random(seed)
        for _ in range(5):
            ang = rng.random()*6.283; l0, l1 = 10+rng.random()*8, 22+rng.random()*16
            c.ln([(x1+math.cos(ang)*l0, y1+math.sin(ang)*l0), (x1+math.cos(ang)*l1, y1+math.sin(ang)*l1)], g(SIL, a), 3)
