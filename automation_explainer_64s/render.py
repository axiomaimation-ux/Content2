"""64 s AXIOM Reel: how automation works (Arabic captions, imagined scenes).
Content is drawn on a 2x layer at full-frame coordinates (only rows YO..YEND kept), scaled by K about the
Reels safe-zone centre (540, 845), composited with a lighter blend over the dot-grid background."""
import math, random, subprocess, sys, os
import numpy as np
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont, ImageChops
import brand as B
import timeline as T

W, H, S = 1080, 1920, 2
FPS = T.FPS
NFR = int(round(T.DUR * FPS))
K = 0.85
CX0, CY0 = 540, 845
YO, YEND = 100, 1590                  # pre-scale rows kept in the content layer
LW, LH = W * S, (YEND - YO) * S

# ---------- helpers ----------
_fonts = {}
def font(key, size):
    k = (key, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(B.FONT[key], int(round(size * S)))
    return _fonts[k]

def X(v): return int(round(v * S))
def Y(v): return int(round((v - YO) * S))
def clamp(x): return max(0.0, min(1.0, x))
def prog(t, t0, dur): return clamp((t - t0) / dur)
def ease_out(u): return 1 - (1 - u) ** 3
def ease_io(u): return 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2
def lerp(a, b, u): return a + (b - a) * u
def dim(c, a): return B.dim(c, a)
def mix(a, b, u): return B.mix(a, b, u)
def pt(x, y): return (X(x), Y(y))

def line(d, pts, c, w):
    d.line([pt(x, y) for x, y in pts], fill=c, width=max(1, X(w)), joint="curve")
def circ(d, cx, cy, r, fill=None, outline=None, w=2):
    d.ellipse([X(cx - r), Y(cy - r), X(cx + r), Y(cy + r)], fill=fill, outline=outline, width=X(w))
def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, w=2):
    d.rounded_rectangle([X(x0), Y(y0), X(x1), Y(y1)], radius=X(r), fill=fill, outline=outline, width=X(w))
def arc(d, x0, y0, x1, y1, a0, a1, c, w):
    d.arc([X(x0), Y(y0), X(x1), Y(y1)], a0, a1, fill=c, width=max(1, X(w)))
def poly(d, pts, fill):
    d.polygon([pt(x, y) for x, y in pts], fill=fill)

def text(d, x, y, s, fk, size, c, anchor="ls", track=0, rtl=False):
    f = font(fk, size)
    kw = dict(direction="rtl", language="ar") if rtl else {}
    if track:
        widths = [d.textlength(ch, font=f) for ch in s]
        total = sum(widths) + X(track) * (len(s) - 1)
        px = X(x) - (total / 2 if anchor == "ms" else (total if anchor == "rs" else 0))
        for ch, wd in zip(s, widths):
            d.text((px, Y(y)), ch, font=f, fill=c, anchor="ls")
            px += wd + X(track)
        return
    d.text((X(x), Y(y)), s, font=f, fill=c, anchor=anchor, **kw)

def new():
    img = Image.new("RGB", (LW, LH), B.BLACK)
    return img, ImageDraw.Draw(img)

def poly_prog(pts, p):
    """Points of the polyline up to fraction p of its length."""
    segs = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(segs); target = p * total
    out = [pts[0]]; acc = 0
    for i, sl in enumerate(segs):
        if acc + sl >= target:
            u = (target - acc) / sl if sl else 0
            out.append((lerp(pts[i][0], pts[i + 1][0], u), lerp(pts[i][1], pts[i + 1][1], u)))
            return out
        out.append(pts[i + 1]); acc += sl
    return out

def path_point(pts, f):
    segs = [math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
    total = sum(segs); target = clamp(f) * total; acc = 0
    for i, sl in enumerate(segs):
        if acc + sl >= target or i == len(segs) - 1:
            u = (target - acc) / sl if sl else 0
            x = lerp(pts[i][0], pts[i + 1][0], u); y = lerp(pts[i][1], pts[i + 1][1], u)
            return (x, y), ((pts[i + 1][0] - pts[i][0]) / sl, (pts[i + 1][1] - pts[i][1]) / sl)
        acc += sl
    return pts[-1], (0, 1)

def path_len(pts):
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))

def bolt_path(d, pts, lo, hi, seed, amp=26, w=6, col=B.WHITE):
    rng = random.Random(seed)
    n = max(3, int(path_len(pts) * (hi - lo) / 22) + 2)
    out = []
    for k in range(n):
        f = lo + (hi - lo) * k / (n - 1)
        p, (tx, ty) = path_point(pts, f)
        off = rng.uniform(-1, 1) * amp * math.sin(math.pi * clamp(f)) if 0 < k < n - 1 else 0
        out.append((p[0] - ty * off, p[1] + tx * off))
    line(d, out, col, w)

def zap(d, pts, t, start, dur, seed):
    """Electricity along a path, with head dot, tail and sparks on arrival."""
    u = (t - start) / dur
    if 0 < u < 1.6:
        lo, hi = max(0.0, u - .6), min(1.0, u)
        if hi - lo > 0.02:
            sd = seed + int(t * 15)
            bolt_path(d, pts, lo, hi, sd, 26, 6, B.WHITE)
            bolt_path(d, pts, lo, hi, sd + 7, 42, 3, B.SILVER)
        if u < 1:
            p, _ = path_point(pts, u)
            circ(d, p[0], p[1], 7, fill=B.WHITE)
    tau = t - (start + dur)
    if 0 <= tau < .2:
        g = ease_out(tau / .2)
        x, y = pts[-1]
        for k in range(6):
            a = math.radians(-170 + k * 32)
            r0, r1 = 8 + 4 * g, 14 + 22 * g
            line(d, [(x + r0 * math.cos(a), y + r0 * math.sin(a)), (x + r1 * math.cos(a), y + r1 * math.sin(a))],
                 dim(B.SILVER, 1 - tau / .2), 3)

# ---------- background: precise dot grid, drifting up 18 px/s, loops every 240 px (400 frames) ----------
GRID = 60
_PH = 400                 # frames per loop: 240 px / (18 px/s / 30 fps)
_tile5 = None
_bgc = {}

def _make_tile5():
    f = 5
    img = Image.new("L", (W * f, 240 * f), 0)
    d = ImageDraw.Draw(img)
    for j in range(4):
        y = (30 + 60 * j) * f
        for i in range(18):
            x = (30 + 60 * i) * f
            if j == 0 and i % 4 == 0:
                d.line([(x - 7 * f, y), (x + 7 * f, y)], fill=B.GRAPHITE[0], width=8)
                d.line([(x, y - 7 * f), (x, y + 7 * f)], fill=B.GRAPHITE[0], width=8)
            else:
                r = 2.2 * f
                d.ellipse([x - r, y - r, x + r, y + r], fill=B.CHARCOAL[0])
    return np.asarray(img, dtype=np.float32)

def bg_tile(k):
    global _tile5
    k %= _PH
    if k not in _bgc:
        if _tile5 is None:
            _tile5 = _make_tile5()
        sh = 3 * k                                   # 0.6 px per frame = 3 rows at 5x
        t = np.roll(_tile5, -sh, axis=0)
        t = t.reshape(240, 5, W, 5).mean(axis=(1, 3))
        _bgc[k] = np.clip(np.rint(t), 0, 255).astype(np.uint8)
    return _bgc[k]

def background(i):
    t = bg_tile(i)
    full = np.tile(t, (8, 1))[:H]
    return Image.fromarray(full, "L").convert("RGB")

# ---------- icons (shapes only) ----------
def icon(d, kind, cx, cy, c, rot=0.0, sc=1.0):
    if kind == "trigger":
        circ(d, cx, cy, 34 * sc, outline=c, w=4)
        poly(d, [(cx - 9 * sc, cy - 15 * sc), (cx - 9 * sc, cy + 15 * sc), (cx + 16 * sc, cy)], c)
    elif kind == "gear":
        circ(d, cx, cy, 17 * sc, outline=c, w=4)
        for k in range(8):
            a = math.radians(k * 45 + rot)
            line(d, [(cx + 25 * sc * math.cos(a), cy + 25 * sc * math.sin(a)),
                     (cx + 36 * sc * math.cos(a), cy + 36 * sc * math.sin(a))], c, 6)
    elif kind == "check":
        line(d, [(cx - 28 * sc, cy + 2 * sc), (cx - 9 * sc, cy + 20 * sc), (cx + 28 * sc, cy - 20 * sc)], c, 7)
    elif kind == "cart":
        line(d, [(cx - 36, cy - 28), (cx - 24, cy - 28), (cx - 14, cy + 12), (cx + 26, cy + 12)], c, 4)
        line(d, [(cx - 21, cy - 16), (cx + 34, cy - 16), (cx + 28, cy + 4), (cx - 15, cy + 4)], c, 4)
        circ(d, cx - 8, cy + 28, 5, fill=c); circ(d, cx + 20, cy + 28, 5, fill=c)
    elif kind == "grid":
        rrect(d, cx - 32, cy - 32, cx + 32, cy + 32, 8, outline=c, w=4)
        line(d, [(cx - 32, cy - 10), (cx + 32, cy - 10)], c, 3)
        line(d, [(cx - 32, cy + 10), (cx + 32, cy + 10)], c, 3)
        line(d, [(cx - 6, cy - 32), (cx - 6, cy + 32)], c, 3)
    elif kind == "bell":
        arc(d, cx - 22, cy - 36, cx + 22, cy + 8, 180, 360, c, 4)
        line(d, [(cx - 22, cy - 14), (cx - 30, cy + 18)], c, 4)
        line(d, [(cx + 22, cy - 14), (cx + 30, cy + 18)], c, 4)
        line(d, [(cx - 34, cy + 18), (cx + 34, cy + 18)], c, 4)
        arc(d, cx - 8, cy + 22, cx + 8, cy + 38, 0, 180, c, 4)
    elif kind == "plus":
        line(d, [(cx - 26 * sc, cy), (cx + 26 * sc, cy)], c, 7)
        line(d, [(cx, cy - 26 * sc), (cx, cy + 26 * sc)], c, 7)

def check_prog(d, cx, cy, sc, c, p, w=7):
    pts = [(cx - 28 * sc, cy + 2 * sc), (cx - 9 * sc, cy + 20 * sc), (cx + 28 * sc, cy - 20 * sc)]
    if p > 0:
        line(d, poly_prog(pts, p), c, w)

def human(d, cx, cy, sc, c, w=6):
    circ(d, cx, cy - 46 * sc, 36 * sc, outline=c, w=w)
    arc(d, cx - 70 * sc, cy + 2 * sc, cx + 70 * sc, cy + 142 * sc, 180, 360, c, w)

def chipicon(d, cx, cy, size, c, label_c, fill=None, w=4, label=True):
    h = size / 2
    rrect(d, cx - h, cy - h, cx + h, cy + h, 22, fill=fill, outline=c, w=w)
    for k in (-1, 0, 1):
        o = k * size * .26
        line(d, [(cx + o, cy - h), (cx + o, cy - h - 18)], c, 4)
        line(d, [(cx + o, cy + h), (cx + o, cy + h + 18)], c, 4)
        line(d, [(cx - h, cy + o), (cx - h - 18, cy + o)], c, 4)
        line(d, [(cx + h, cy + o), (cx + h + 18, cy + o)], c, 4)
    if label:
        text(d, cx, cy + size * .17, "AI", "sg700", size * .5, label_c, "ms")

def star(d, cx, cy, r, fill=None, outline=None, w=4):
    pts = []
    for k in range(10):
        a = math.radians(-90 + k * 36)
        rr = r if k % 2 == 0 else r * .45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    if fill:
        poly(d, pts, fill)
    if outline:
        line(d, pts + [pts[0]], outline, w)

def ring_pulse(d, cx, cy, r0, r1, tau, dur, w=2):
    if 0 <= tau < dur:
        g = ease_out(tau / dur)
        circ(d, cx, cy, lerp(r0, r1, g), outline=dim(B.WHITE, 1 - tau / dur), w=w)

def rrect_pulse(d, x0, y0, x1, y1, r, exp, tau, dur):
    if 0 <= tau < dur:
        g = ease_out(tau / dur) * exp
        rrect(d, x0 - g, y0 - g, x1 + g, y1 + g, r + g, outline=dim(B.WHITE, 1 - tau / dur), w=2)

def appear(t, t0, dur=.35, base=.35):
    return base + (1 - base) * ease_out(prog(t, t0, dur))

def block(d, x0, y0, x1, y1, role, num, kind, e, lvl, f=0.0, rot=0.0, h_small=False):
    fill = dim(mix(B.CHARCOAL, B.WHITE, f), e)
    border = dim(mix(B.GRAPHITE, B.WHITE, lvl), e)
    rrect(d, x0, y0, x1, y1, 28, fill=fill, outline=border, w=2)
    main = dim(mix(mix(B.SILVER, B.WHITE, lvl), B.BLACK, f), e)
    sub = dim(mix(mix(B.GRAPHITE, B.SILVER, lvl), B.BLACK, f), e)
    mid = (y0 + y1) / 2
    sc = .8 if h_small else 1.0
    icon(d, kind, x0 + 100 * (.85 if h_small else 1), mid, main, rot, sc)
    tx = x0 + (165 if h_small else 190)
    if h_small:
        text(d, tx, mid + 18, role, "sg600", 52, main)
    else:
        text(d, tx, mid - 30, f"0{num}", "dm500", 30, sub, track=5)
        text(d, tx, mid + 38, role, "sg600", 64, main)

# =============== scenes (pure functions of absolute time t) ===============
def scene_title(t):
    img, d = new()
    cx, cy, R = 540, 660, 190
    a = appear(t, 0.0, .3)
    p = ease_io(prog(t, *T.TI_RING))
    bb = (X(cx - R), Y(cy - R), X(cx + R), Y(cy + R))
    d.ellipse(bb, outline=dim(B.GRAPHITE, a), width=X(2))
    if p > 0:
        if p >= .999: d.ellipse(bb, outline=B.SILVER, width=X(2))
        else: d.arc(bb, -90, -90 + 360 * p, fill=B.SILVER, width=X(2))
    # orbiting dot
    th = math.radians(-90) + 2 * math.pi * 1.3 * ease_io(prog(t, 0.1, 1.9))
    circ(d, cx + R * math.cos(th), cy + R * math.sin(th), 12, fill=dim(B.WHITE, a))
    circ(d, cx, cy, 34, outline=dim(B.WHITE, a), w=4)
    poly(d, [(cx - 9, cy - 15), (cx - 9, cy + 15), (cx + 16, cy)], dim(B.WHITE, a))
    a2 = appear(t, T.TI_TITLE, .4, base=.0)
    if a2 > 0:
        text(d, 540, 1030 + 24 * (1 - ease_out(prog(t, T.TI_TITLE, .4))), "أتمتة ببساطة", "ar700", 128,
             dim(B.WHITE, a2), "ms", rtl=True)
    return img

ROW_TOP, ROW_H, ROW_STEP = 505, 140, 164

def scene_repeat(t):
    img, d = new()
    # power icon (trigger) on top
    lit = ease_out(prog(t, T.RP_POWER, .25))
    pa = appear(t, T.RP_ROWIN, .4)
    icon(d, "trigger", 540, 420, dim(mix(B.GRAPHITE, B.WHITE, lit), pa))
    ring_pulse(d, 540, 420, 40, 78, t - T.RP_POWER, .5)
    # rows
    for i in range(4):
        e = appear(t, T.RP_ROWIN + .08 * i, .4)
        slide = 30 * (1 - ease_out(prog(t, T.RP_ROWIN + .08 * i, .45)))
        y0 = ROW_TOP + i * ROW_STEP + slide
        rrect(d, 140, y0, 940, y0 + ROW_H, 24, fill=dim(B.CHARCOAL, e), outline=dim(B.GRAPHITE, e), w=2)
        circ(d, 205, y0 + ROW_H / 2, 16, outline=dim(B.GRAPHITE, e), w=3)
        line(d, [(260, y0 + 52), (560, y0 + 52)], dim(B.SILVER, e), 8)
        line(d, [(260, y0 + 90), (430, y0 + 90)], dim(B.GRAPHITE, e), 8)
        # checkbox state
        cx_, cy_ = 840, y0 + ROW_H / 2
        on1 = T.RP_TAPS[i]; auto1 = T.RP_AUTO[0][i]; auto2 = T.RP_AUTO[1][i]
        if t >= auto2: ck = ease_out(prog(t, auto2, .15)); how = "auto"
        elif t >= T.RP_RESET2: ck = 1 - ease_out(prog(t, T.RP_RESET2, .15)); how = "auto"
        elif t >= auto1: ck = ease_out(prog(t, auto1, .15)); how = "auto"
        elif t >= T.RP_RESET: ck = 1 - ease_out(prog(t, T.RP_RESET, .2)); how = "man"
        elif t >= on1: ck = ease_out(prog(t, on1, .15)); how = "man"
        else: ck = 0.0; how = "man"
        boxc = dim(mix(B.GRAPHITE, B.WHITE if how == "auto" else B.SILVER, ck), e)
        rrect(d, cx_ - 34, cy_ - 34, cx_ + 34, cy_ + 34, 12, fill=dim(B.WHITE, ck * e) if how == "auto" else None,
              outline=boxc, w=3)
        if ck > 0:
            check_prog(d, cx_, cy_, .7, B.BLACK if how == "auto" else dim(B.SILVER, e), ck, 6)
    # tapper (manual phase only)
    ta = ease_out(prog(t, 2.15, .25)) * (1 - ease_out(prog(t, 4.35, .3)))
    if ta > 0:
        taps = T.RP_TAPS
        yc = [ROW_TOP + i * ROW_STEP + ROW_H / 2 for i in range(4)]
        pos = (900, yc[0] - 70)
        if t < taps[0] - .3: pos = (900, yc[0] - 70)
        for i in range(4):
            a0 = taps[i] - .3
            if t >= a0:
                src = (900, yc[0] - 70) if i == 0 else (840, yc[i - 1])
                dst = (840, yc[i])
                pos = (lerp(src[0], dst[0], ease_io(prog(t, a0, .3))), lerp(src[1], dst[1], ease_io(prog(t, a0, .3))))
        press = 1.0
        for tp in taps:
            if tp <= t < tp + .15: press = 1 - .3 * math.sin(math.pi * (t - tp) / .15)
        circ(d, pos[0], pos[1], 24 * press, outline=dim(B.SILVER, max(ta, .0)), w=3)
        circ(d, pos[0], pos[1], 5, fill=dim(B.SILVER, ta))
    # label
    la = ease_out(prog(t, T.RP_LABEL, .4))
    if la > 0:
        text(d, 540, 1262 + 20 * (1 - la), "تلقائياً", "ar700", 92, dim(B.WHITE, la), "ms", rtl=True)
    return img

HUM = (540, 600)
CARD = (290, 940, 790, 1120)

def scene_ai(t):
    img, d = new()
    # result card
    e = appear(t, 7.0, .3)
    x0, y0, x1, y1 = CARD
    rrect(d, x0, y0, x1, y1, 28, fill=dim(B.CHARCOAL, e), outline=dim(B.GRAPHITE, e), w=2)
    line(d, [(x0 + 150, y0 + 66), (x1 - 50, y0 + 66)], dim(B.SILVER, e), 8)
    line(d, [(x0 + 150, y0 + 108), (x1 - 150, y0 + 108)], dim(B.GRAPHITE, e), 8)
    ccx, ccy = x0 + 80, (y0 + y1) / 2
    # check state: drawn at CHECK1, cleared at RESET, drawn again at CHECK2
    if t < T.AI_RESET:
        cp = prog(t, T.AI_CHECK1, .3); cc = B.WHITE; ca = 1.0
    elif t < T.AI_CHECK2:
        cp = 1.0; cc = B.WHITE; ca = 1 - ease_out(prog(t, T.AI_RESET, .25))
    else:
        cp = prog(t, T.AI_CHECK2, .3); cc = B.WHITE; ca = 1.0
    circ(d, ccx, ccy, 40, outline=dim(B.GRAPHITE, e), w=3)
    if cp > 0 and ca > 0:
        check_prog(d, ccx, ccy, .85, dim(cc, ca), ease_out(cp), 7)
    rrect_pulse(d, x0, y0, x1, y1, 28, 22, t - T.AI_RING, .5)
    # connecting line
    line(d, [(540, 790), (540, y0)], dim(B.GRAPHITE, e), 3)
    # human (phase 1)
    hx, hy = HUM
    ho = 1 - ease_out(prog(t, *T.AI_OUT))
    if ho > 0:
        ha = appear(t, 7.0, .4) * ho
        shift = -30 * (1 - ho)
        human(d, hx + shift, hy, 1.15, dim(B.WHITE, ha), 6)
    # AI chip (phase 2)
    cprog = ease_out(prog(t, *T.AI_CHIP))
    if cprog > 0:
        ca2 = cprog
        chipicon(d, hx, hy + 55 + 30 * (1 - cprog), 190, dim(B.WHITE, ca2), dim(B.WHITE, ca2),
                 fill=dim(B.CHARCOAL, ca2))
    # energy pulses
    for (s, dur) in (T.AI_P1, T.AI_P2):
        zap(d, [(540, 790), (540, y0)], t, s, dur, int(s * 100))
    return img

TH_TOP, TH_BH, TH_GAP = 400, 190, 160
def th_y(i): return TH_TOP + i * (TH_BH + TH_GAP)
ROLES = ["TRIGGER", "PROCESS", "ACTION"]
KINDS = ["trigger", "gear", "check"]

def scene_three(t):
    img, d = new()
    for j in range(2):
        wp = ease_out(prog(t, T.TH_WIRE[j], .4))
        ya, yb = th_y(j) + TH_BH, th_y(j + 1)
        lit = ease_out(prog(t, T.TH_HI[j + 1], .25))
        if wp > 0:
            line(d, [(540, ya), (540, lerp(ya, yb, wp))], mix(B.GRAPHITE, B.SILVER, lit), 3)
    for i in range(3):
        e = appear(t, T.TH_BLOCK[i], .4)
        sl = 36 * (1 - ease_out(prog(t, T.TH_BLOCK[i], .45)))
        hi = T.TH_HI[i]
        lvl = ease_out(prog(t, hi, .25))
        if i < 2:
            lvl *= 1 - .5 * ease_out(prog(t, T.TH_HI[i + 1], .25))
        rot = 40 * max(0.0, t - hi) if i == 1 else 0.0
        y0 = th_y(i) + sl
        block(d, 140, y0, 940, y0 + TH_BH, ROLES[i], i + 1, KINDS[i], e, lvl, 0.0, rot)
        ring_pulse(d, 240, y0 + TH_BH / 2, 38, 78, t - hi, .5)
    return img

def scene_flow(t):
    img, d = new()
    act = [T.FL_PRE[0], T.FL_B1[0] + T.FL_B1[1], T.FL_B2[0] + T.FL_B2[1]]
    for j in range(2):
        ya, yb = th_y(j) + TH_BH, th_y(j + 1)
        lit = ease_out(prog(t, act[j + 1], .2))
        line(d, [(540, ya), (540, yb)], mix(B.GRAPHITE, B.SILVER, lit), 3)
    for i in range(3):
        base = .75 if t < 24.0 else 1.0
        lvl = ease_out(prog(t, act[i], .2)) * (1.0 if i == 2 else 1.0)
        if i == 0:
            lvl = ease_out(prog(t, T.FL_PRE[0], .25))
        fill = ease_out(prog(t, T.FL_FILL, .3)) if i == 2 else 0.0
        rot = 140 * max(0.0, t - act[1]) if i == 1 and t > act[1] else 0.0
        block(d, 140, th_y(i), 940, th_y(i) + TH_BH, ROLES[i], i + 1, KINDS[i], 1.0, lvl, fill, rot)
    # trigger idle pulses
    for pt_ in T.FL_PRE:
        ring_pulse(d, 240, th_y(0) + TH_BH / 2, 38, 78, t - pt_, .5)
    zap(d, [(540, th_y(0) + TH_BH), (540, th_y(1))], t, T.FL_B1[0], T.FL_B1[1], 1000)
    zap(d, [(540, th_y(1) + TH_BH), (540, th_y(2))], t, T.FL_B2[0], T.FL_B2[1], 2000)
    for rt in T.FL_RINGS:
        rrect_pulse(d, 140, th_y(2), 940, th_y(2) + TH_BH, 28, 26, t - rt, .5)
    return img

# ---- website -> sheet + notification ----
WEB = (190, 535, 890, 755)
SHEET = (110, 935, 510, 1155)
NOTIF = (570, 935, 970, 1155)
P_SHEET = [(540, 755), (540, 845), (310, 845), (310, 935)]
P_NOTIF = [(540, 755), (540, 845), (770, 845), (770, 935)]

def scene_site(t):
    img, d = new()
    e = appear(t, 35.0, .4)
    x0, y0, x1, y1 = WEB
    rrect(d, x0, y0, x1, y1, 28, fill=dim(B.CHARCOAL, e), outline=dim(B.GRAPHITE, e), w=2)
    pulse = 1.0
    icon(d, "cart", 270, 615, dim(B.SILVER, e))
    text(d, 340, 612, "WEBSITE", "dm500", 30, dim(B.SILVER, e), track=5)
    # order chip
    orders = T.SI_ORDER
    on = 0.0
    if t >= orders[1]: on = ease_out(prog(t, orders[1], .25))
    elif t >= T.SI_ORDER_RESET: on = 1 - ease_out(prog(t, T.SI_ORDER_RESET, .25))
    elif t >= orders[0]: on = ease_out(prog(t, orders[0], .25))
    cx0, cy0, cx1, cy1 = 340, 665, 600, 730
    rrect(d, cx0, cy0, cx1, cy1, 20, fill=dim(B.WHITE, on) if on > 0 else None, outline=dim(mix(B.GRAPHITE, B.WHITE, on), e), w=2)
    text(d, 470 - 12, cy0 + 43, "ORDER", "dm500", 30, mix(dim(B.GRAPHITE, e), B.BLACK, on) if on > .5 else dim(mix(B.GRAPHITE, B.SILVER, on), e), "ms", track=4)
    if on > 0:
        check_prog(d, 572, 697, .32, B.BLACK, 1.0, 4)
    # wires
    for P_ in (P_SHEET, P_NOTIF):
        line(d, P_, dim(B.GRAPHITE, e), 3)
    # sheet card
    sx0, sy0, sx1, sy1 = SHEET
    rrect(d, sx0, sy0, sx1, sy1, 28, fill=dim(B.CHARCOAL, e), outline=dim(B.GRAPHITE, e), w=2)
    icon(d, "grid", 175, 1015, dim(B.SILVER, e), 0, .8)
    text(d, 225, 1010, "GOOGLE SHEET", "dm500", 30, dim(B.SILVER, e), track=2)
    for r in range(3):
        yy = 1070 + r * 30
        rrect(d, 140, yy, 480, yy + 16, 8, outline=dim(B.GRAPHITE, e), w=2)
        w1 = prog(t, T.SI_ROWS[0][r], .25); w2 = prog(t, T.SI_ROWS[1][r], .25)
        if t >= T.SI_ROWS[1][r]: fillp = w2
        elif t >= T.SI_ROWS_RESET: fillp = 1 - prog(t, T.SI_ROWS_RESET, .25)
        else: fillp = w1
        if fillp > 0:
            rrect(d, 142, yy + 2, 142 + (336 * ease_out(fillp)), yy + 14, 6, fill=dim(B.SILVER, e))
    # notification card
    nx0, ny0, nx1, ny1 = NOTIF
    rrect(d, nx0, ny0, nx1, ny1, 28, fill=dim(B.CHARCOAL, e), outline=dim(B.GRAPHITE, e), w=2)
    icon(d, "bell", 645, 1015, dim(B.SILVER, e), 0, .8)
    text(d, 695, 1010, "NOTIFICATION", "dm500", 30, dim(B.SILVER, e), track=2)
    badge = 0.0
    if t >= T.SI_BELL[1]: badge = ease_out(prog(t, T.SI_BELL[1], .2))
    elif t >= T.SI_BELL_RESET: badge = 1 - ease_out(prog(t, T.SI_BELL_RESET, .2))
    elif t >= T.SI_BELL[0]: badge = ease_out(prog(t, T.SI_BELL[0], .2))
    if badge > 0:
        circ(d, 668, 984, 10 * badge, fill=B.WHITE)
        for yy, w_ in ((1075, 340), (1105, 230)):
            line(d, [(600, yy), (600 + w_ * badge, yy)], dim(B.SILVER if yy == 1075 else B.GRAPHITE, e), 8)
    for bt in T.SI_BELL:
        tau = t - (bt + .05)
        if 0 <= tau < .6:
            g = ease_out(tau / .6); al = 1 - tau / .6
            for k, rr in enumerate((46, 62)):
                r_ = rr + 14 * g
                arc(d, 645 - r_, 1015 - r_, 645 + r_, 1015 + r_, -50 - 0, 50, dim(B.SILVER, al * (1 - .3 * k)), 3)
                arc(d, 645 - r_, 1015 - r_, 645 + r_, 1015 + r_, 130, 230, dim(B.SILVER, al * (1 - .3 * k)), 3)
    for (s, dur) in T.SI_BOLT:
        zap(d, P_SHEET, t, s, dur, 3000 + int(s))
        zap(d, P_NOTIF, t, s, dur, 4000 + int(s))
    return img

def scene_toggle(t):
    img, d = new()
    e = appear(t, 43.0, .3)
    cx, cy = 540, 720
    flip = ease_io(prog(t, *T.TG_FLIP))
    x0, y0, x1, y1 = cx - 190, cy - 95, cx + 190, cy + 95
    rrect(d, x0, y0, x1, y1, 95, fill=mix(B.CHARCOAL, B.WHITE, flip) if t >= 43.7 else dim(B.CHARCOAL, e),
          outline=dim(mix(B.GRAPHITE, B.WHITE, flip), e), w=3)
    kx = lerp(x0 + 95, x1 - 95, flip)
    circ(d, kx, cy, 70, fill=mix(B.SILVER, B.BLACK, flip) if flip > .5 else dim(B.SILVER, e))
    rrect_pulse(d, x0, y0, x1, y1, 95, 34, t - T.TG_RING, .6)
    la = ease_out(prog(t, T.TG_LABEL, .4))
    if la > 0:
        text(d, 540, 1040 + 20 * (1 - la), "تلقائياً", "ar700", 132, dim(B.WHITE, la), "ms", rtl=True)
    return img

def scene_chat(t):
    img, d = new()
    e = appear(t, 46.0, .35)
    cx0, cy0, cx1, cy1 = 160, 420, 920, 1230
    rrect(d, cx0, cy0, cx1, cy1, 32, outline=dim(B.GRAPHITE, e), w=2)
    text(d, 200, 505, "WHATSAPP", "dm500", 30, dim(B.SILVER, e), track=6)
    chipicon(d, 835, 490, 52, dim(B.WHITE, e), dim(B.WHITE, e), w=3, label=False)
    text(d, 835, 504, "AI", "sg700", 26, dim(B.WHITE, e), "ms")
    line(d, [(200, 545), (880, 545)], dim(B.GRAPHITE, e), 2)
    bub = [  # (x0, y0, x1, y1, who, bars)
        (200, 580, 640, 705, "ai", (320, 240)),
        (440, 730, 880, 810, "me", (300,)),
        (200, 840, 640, 965, "ai", (300, 200)),
        (600, 990, 880, 1065, "me", (180,)),
    ]
    for i, (x0, y0, x1, y1, who, bars) in enumerate(bub):
        tb = T.CH_BUB[i]
        u = ease_out(prog(t, tb, .3))
        # typing dots before AI bubbles
        if who == "ai":
            k = 0 if i == 0 else 1
            ds, de = T.CH_DOTS[k]
            if ds <= t < de:
                for q in range(3):
                    ph = math.sin((t - ds) * 9 - q * .9)
                    circ(d, 230 + q * 30, (y0 + y1) / 2, 7 + 2 * ph, fill=B.SILVER)
        if u <= 0: continue
        yy = lerp(y0 + 22, y0, u)
        if who == "ai":
            rrect(d, x0, yy, x1, yy + (y1 - y0), 24, fill=dim(B.CHARCOAL, u), outline=dim(B.GRAPHITE, u), w=2)
            col = dim(B.SILVER, u)
        else:
            rrect(d, x0, yy, x1, yy + (y1 - y0), 24, outline=dim(B.WHITE, u), w=2)
            col = dim(B.WHITE, u)
        for n_, bw in enumerate(bars):
            line(d, [(x0 + 30, yy + 38 + n_ * 36), (x0 + 30 + bw, yy + 38 + n_ * 36)], col, 8)
    # order confirmation strip
    sx0, sy0, sx1, sy1 = 200, 1100, 880, 1190
    f = ease_out(prog(t, T.CH_ORDER, .3))
    rrect(d, sx0, sy0, sx1, sy1, 24, fill=dim(mix(B.CHARCOAL, B.WHITE, f), e), outline=dim(mix(B.GRAPHITE, B.WHITE, f), e), w=2)
    text(d, 235, 1157, "ORDER", "dm500", 30, mix(dim(B.SILVER, e), B.BLACK, f), track=6)
    cc = (835, 1145)
    circ(d, cc[0], cc[1], 28, outline=mix(dim(B.GRAPHITE, e), B.BLACK, f), w=3)
    check_prog(d, cc[0], cc[1], .6, B.BLACK, ease_out(prog(t, T.CH_ORDER + .1, .3)), 5)
    rrect_pulse(d, sx0, sy0, sx1, sy1, 24, 20, t - (T.CH_ORDER + .05), .5)
    return img

# ---- summary ----
SU_TOP, SU_BH, SU_GAP = 510, 130, 140
def su_y(i): return SU_TOP + i * (SU_BH + SU_GAP)

def stage_chain(t):
    img, d = new()
    cycles = T.SU_CYCLES
    for j in range(2):
        line(d, [(540, su_y(j) + SU_BH), (540, su_y(j + 1))], B.GRAPHITE, 3)
    # activation state: last cycle start <= t
    cyc = [c for c in cycles if c <= t]
    c0 = cyc[-1] if cyc else None
    lv = [0.0, 0.0, 0.0]
    fl = 0.0
    if c0 is not None:
        lv[0] = ease_out(prog(t, c0 - .0, .1))
        lv[1] = ease_out(prog(t, c0 + .24, .1))
        lv[2] = ease_out(prog(t, c0 + .58, .1))
        fl = lv[2]
        # decay of the previous cycle's lit state is implicit: reset at the new cycle start
        if t - c0 > .9:
            k = ease_out(prog(t, c0 + .9, .3))
            lv = [v * (1 - k) for v in lv]; fl = fl * (1 - k)
    else:
        lv = [0.0, 0.0, 0.0]
    for i in range(3):
        rot = 120 * t if i == 1 else 0.0
        block(d, 240, su_y(i), 840, su_y(i) + SU_BH, ROLES[i], i + 1, KINDS[i], 1.0, lv[i], fl * 1.0 if i == 2 else 0.0, rot, h_small=True)
    for c in cycles:
        zap(d, [(540, su_y(0) + SU_BH), (540, su_y(1))], t, c, .24, 7000 + int(c * 10))
        zap(d, [(540, su_y(1) + SU_BH), (540, su_y(2))], t, c + .34, .24, 8000 + int(c * 10))
    return img

CH_X0, CH_Y0, CH_X1, CH_Y1 = 200, 560, 880, 1010
CH_PTS = [(200, 1010), (320, 940), (420, 965), (540, 830), (650, 780), (760, 660), (880, 560)]
def stage_chart(t):
    img, d = new()
    line(d, [(CH_X0, CH_Y0 - 20), (CH_X0, CH_Y1 + 20), (CH_X1 + 20, CH_Y1 + 20)], B.GRAPHITE, 3)
    text(d, CH_X1 + 20, CH_Y0 - 70, "إنتاجية", "ar600", 52, B.SILVER, "rs", rtl=True)
    p = ease_io(prog(t, *T.SU_CHART))
    if p > 0:
        pts = poly_prog(CH_PTS, p)
        line(d, pts, B.WHITE, 6)
        circ(d, pts[-1][0], pts[-1][1], 12, fill=B.WHITE)
    ring_pulse(d, CH_PTS[-1][0], CH_PTS[-1][1], 14, 44, t - T.SU_CHART_RING, .5)
    return img

def stage_human(t):
    img, d = new()
    a = appear(t, T.SU_HUMAN, .35, base=.0)
    human(d, 540, 760, 1.9, dim(B.WHITE, a), 7)
    p = ease_io(prog(t, *T.SU_HRING))
    bb = (X(540 - 250), Y(740 - 250), X(540 + 250), Y(740 + 250))
    if p > 0:
        d.arc(bb, -90, -90 + 360 * p, fill=B.SILVER, width=X(2))
    sa = ease_out(prog(t, T.SU_STAR, .3))
    if sa > 0:
        star(d, 780, 520, 48 * (.6 + .4 * sa), fill=dim(B.WHITE, sa))
        ring_pulse(d, 780, 520, 50, 82, t - T.SU_STAR, .5)
    return img

def scene_summary(t):
    ia = 1 - ease_out(prog(t, *T.SU_A_FADE))
    ib_in = ease_out(prog(t, T.SU_A_FADE[0] + .1, .3))
    ib_out = 1 - ease_out(prog(t, *T.SU_B_FADE))
    ib = ib_in * ib_out
    ic = ease_out(prog(t, T.SU_B_FADE[0] + .1, .3))
    img = None
    def add(img, layer, a):
        if a <= 0: return img
        layer = Image.eval(layer, lambda v: int(v * a)) if a < 1 else layer
        return layer if img is None else ImageChops.lighter(img, layer)
    if ia > 0: img = add(img, stage_chain(t), ia)
    if ib > 0: img = add(img, stage_chart(t), ib)
    if ic > 0: img = add(img, stage_human(t), ic)
    if img is None: img = stage_chain(t)
    return img

def scene_follow(t):
    img, d = new()
    a = appear(t, T.FO_PLUS, .3)
    cx, cy, R = 540, 700, 92
    f = ease_out(prog(t, T.FO_FILL, .25))
    circ(d, cx, cy, R, fill=mix(B.BLACK, B.WHITE, f) if f > 0 else None, outline=dim(mix(B.WHITE, B.WHITE, f), a), w=4)
    if f < .5:
        icon(d, "plus", cx, cy, dim(B.WHITE, a * (1 - 2 * f)), 0, 1.0)
    else:
        check_prog(d, cx, cy, 1.1, B.BLACK, ease_out(prog(t, T.FO_FILL + .1, .3)), 9)
    ring_pulse(d, cx, cy, R, R + 120, t - T.FO_RING, .7)
    la = ease_out(prog(t, T.FO_LABEL, .4))
    if la > 0:
        text(d, 540, 1040 + 20 * (1 - la), "فولو", "ar700", 150, dim(B.WHITE, la), "ms", rtl=True)
    return img

SCENE_FN = {"title": scene_title, "repeat": scene_repeat, "ai": scene_ai, "three": scene_three,
            "flow": scene_flow, "site": scene_site, "toggle": scene_toggle, "chat": scene_chat,
            "summary": scene_summary, "follow": scene_follow}

def scene_at(t):
    for name, a, b in T.SCENES:
        if a <= t < b: return name
    return T.SCENES[-1][0]

def content_layer(t):
    """Black layer with the scene(s); crossfade (0.25 s) only at the 3 budgeted transitions."""
    for x in T.XF:
        if x - T.XFD / 2 <= t <= x + T.XFD / 2:
            na = scene_at(x - 1e-3); nb = scene_at(x + 1e-3)
            u = ease_io(prog(t, x - T.XFD / 2, T.XFD))
            return Image.blend(SCENE_FN[na](t), SCENE_FN[nb](t), u)
    return SCENE_FN[scene_at(t)](t)

# ---------- captions (1 line, max 3 words, inside the safe zone) ----------
_CHUNKS = None
CAP_Y = 1350            # box centre (unscaled); box 1290..1410, inside y 220..1470, x 135..945
CAP_MAXW = 800

def _word_w(f_ar, f_la, parts):
    ws = []
    for p in parts:
        if p.isascii():
            ws.append((p, f_la, f_la.getlength(p)))
        else:
            ws.append((p, f_ar, f_ar.getlength(p, direction="rtl", language="ar")))
    return ws

def caption_layer(t):
    """Returns (rgb, mask) at 1x for the caption box region, or None. Region = full width x 140 rows."""
    global _CHUNKS
    if _CHUNKS is None: _CHUNKS = T.caption_chunks()
    cur = None
    for ch in _CHUNKS:
        if ch[0] <= t < ch[1]: cur = ch; break
    if cur is None: return None
    t0, t1, toks, spans = cur
    size = 58
    while True:
        f_ar = ImageFont.truetype(B.FONT["ar600"], size * S)
        f_la = ImageFont.truetype(B.FONT["dm500"], size * S)
        items = []
        for tk in toks:
            parts = _word_w(f_ar, f_la, tk[::-1])     # visual left->right inside a token
            w = sum(p[2] for p in parts) + (14 * S) * (len(parts) - 1)
            items.append((parts, w))
        gap = 30 * S
        total = sum(w for _, w in items) + gap * (len(items) - 1)
        if total <= (CAP_MAXW - 90) * S or size <= 40: break
        size -= 2
    bw = total + 90 * S
    reg_h = 140 * S
    rgb = Image.new("RGB", (W * S, reg_h), B.BLACK)
    mask = Image.new("L", (W * S, reg_h), 0)
    d = ImageDraw.Draw(rgb); dm = ImageDraw.Draw(mask)
    bx0 = (W * S - bw) / 2; by0 = 10 * S; by1 = 130 * S
    d.rounded_rectangle([bx0, by0, bx0 + bw, by1], radius=60 * S, fill=B.CHARCOAL)
    dm.rounded_rectangle([bx0, by0, bx0 + bw, by1], radius=60 * S, fill=255)
    # current token index
    idx = len(toks) - 1
    for k, (a, b) in enumerate(spans):
        if t < b: idx = k; break
    # visual order: first token in reading order is rightmost
    x = bx0 + 45 * S
    base = (by0 + by1) / 2 + size * S * .30
    for k in range(len(items) - 1, -1, -1):
        parts, w = items[k]
        col = B.WHITE if k == idx else (B.SILVER if k < idx else B.GRAPHITE)
        px = x
        for (s, f, wd) in parts:
            if s.isascii():
                d.text((px, base), s, font=f, fill=col, anchor="ls")
            else:
                d.text((px, base), s, font=f, fill=col, anchor="ls", direction="rtl", language="ar")
            px += wd + 14 * S
        x += w + gap
    return rgb.reduce(S), mask.reduce(S)

CAP_REG_Y = CAP_Y - 70      # region top at 1x

# ---------- composition ----------
SC_Y0 = int(round(CY0 + (YO - CY0) * K))            # 212: scaled top of the kept rows
SC_X0 = int(round(CX0 + (0 - CX0) * K))             # 81
SC_W = int(round(LW * K)); SC_H = int(round(LH * K)) // 2 * 2

def frame_img(i):
    t = i / FPS
    layer = content_layer(t)
    small = layer.resize((SC_W, SC_H), Image.LANCZOS).reduce(S)
    canvas = Image.new("RGB", (W, H), B.BLACK)
    canvas.paste(small, (SC_X0, SC_Y0))
    frame = ImageChops.lighter(background(i), canvas)
    cap = caption_layer(t)
    if cap is not None:
        rgb, mask = cap
        frame.paste(rgb, (0, CAP_REG_Y), mask)
    return frame

def frame_bytes(i):
    return frame_img(i).tobytes()

if __name__ == "__main__":
    out, wav = sys.argv[1], sys.argv[2]
    for k in range(_PH): bg_tile(k)       # precompute before forking
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", str(T.DUR), out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count() or 2) as pool:
        for n, b in enumerate(pool.imap(frame_bytes, range(NFR), chunksize=4)):
            p.stdin.write(b)
            if n % 120 == 0: print("frame", n, flush=True)
    p.stdin.close(); p.wait()
    print("done", out)
