import math, random
from lib import *
import timeline as T
def lw(sc, key, i, side=0): return T.L(sc, key, i, side)

# ---------- helpers ----------
def gear_o(c, cx, cy, r, rot, col, w=5, teeth=12, fill=False, hole=None):
    pts = []
    for i in range(teeth):
        b = rot+i*360/teeth
        for da, rr in ((-9, .8), (-6, 1), (6, 1), (9, .8)):
            a = math.radians(b+da); pts.append((cx+math.cos(a)*r*rr, cy+math.sin(a)*r*rr))
    if fill: c.poly(pts, col)
    else: c.ln(pts+[pts[0]], col, w)
    if hole is not None: c.ell(cx, cy, r*.38, fill=hole)
def tri_warn(c, cx, cy, s, col, w=5):
    c.ln([(cx, cy-s*.55), (cx+s*.6, cy+s*.45), (cx-s*.6, cy+s*.45), (cx, cy-s*.55)], col, w)
    c.ln([(cx, cy-s*.15), (cx, cy+s*.15)], col, w); c.ell(cx, cy+s*.3, w*.55, fill=col)
def dashed_rect(c, x0, y0, x1, y1, frac, col, w=3, dash=22, gap=16):
    P = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]; tot = 2*((x1-x0)+(y1-y0)); lim = tot*frac; run = 0
    for k in range(4):
        (ax, ay), (bx, by) = P[k], P[k+1]; L_ = math.hypot(bx-ax, by-ay); s = 0
        while s < L_ and run < lim:
            e = min(s+dash, L_, s+(lim-run)); 
            c.ln([(ax+(bx-ax)*s/L_, ay+(by-ay)*s/L_), (ax+(bx-ax)*e/L_, ay+(by-ay)*e/L_)], col, w); run += dash+gap; s += dash+gap
def dots_on(c, p0, p1, t, a=1, n=2, spd=1.2, rev=False):
    for k in range(n):
        u = (t*spd+k/n) % 1; u = 1-u if rev else u
        c.ell(lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u), 7, fill=g(WH, a))
def draw_line(c, p0, p1, p, col, w=3):
    if p > 0: c.ln([p0, (lerp(p0[0], p1[0], p), lerp(p0[1], p1[1], p))], col, w)
def tick_box(c, cx, cy, s, p):
    c.rect(cx-s/2, cy-s/2, cx+s/2, cy+s/2, fill=g(WH, p) if p > .5 else None, line=g(lerp(GRA, WH, p)), r=8, w=3)
    if p > .5: check(c, cx, cy, s*.6, 0, 5)
def mini_pulse(c, cx, cy, r0, r1, t, t0, d=0.6, w=3): sparkle_ring(c, cx, cy, r0, r1, (t-t0)/d, SIL, w)

# ---------- A  hook ----------
def sA(c, t):
    head(c, t, [(0, 2.2, 'AUTOMATION', 'Why choose Axiom for automation?')])
    a = 0.55+0.45*eo(ap(t, 0, 0.4)); t6 = lw('A', 'S1', 5)
    rot = t*35+90*max(0, t-t6+0.3)
    gear_o(c, 540, 930, 200, rot, g(WH, a), 5); c.ell(540, 930, 150, line=g(GRA, a), w=3)
    c.tx(540, 945, '?', 'sg7', 280, g(WH, a), 'mm')
    mini_pulse(c, 540, 930, 215, 330, t, lw('A', 'S1', 2), 0.7); mini_pulse(c, 540, 930, 215, 330, t, t6, 0.7)

# ---------- B  meeting ----------
def bub_bars(c, x0, y0, w, h, a, side):
    c.rect(x0, y0, x0+w, y0+h, fill=g(CH, a), line=g(GRA, a), r=34, w=2)
    for k, ww in enumerate((0.7, 0.5, 0.6)):
        c.rect(x0+36, y0+24+k*26, x0+36+(w-72)*ww, y0+36+k*26, fill=g(SIL if side else GRA, a), r=6)
def sB(c, t):
    head(c, t, [(0, 3.5, 'STEP 01', 'First, a meeting to understand your business')])
    ts, tb, te = lw('B', 'S2', 3), lw('B', 'S2', 8), lw('B', 'S2', 9)
    for cx, lab, k in ((220, 'YOU', 0), (860, 'US', 1)):
        a, dy = appear(t, 0.12*k, 0.35, 0.5); person(c, cx, 800+dy, 150, g(SIL, a)); c.tx(cx, 925+dy, lab, 'dm5', 30, g(WH, a), 'mm', track=6)
    a, dy = appear(t, lw('B', 'S2', 0), 0.3)
    if a > 0: bub_bars(c, 100-(1-a)*30, 540, 330, 110, a, 0)
    a, dy = appear(t, lw('B', 'S2', 2), 0.3)
    if a > 0: bub_bars(c, 650+(1-a)*30, 580, 330, 110, a, 1)
    p = eo(ap(t, ts, 0.55)); draw_line(c, (330, 830), (750, 830), p, g(WH), 4)
    if 0 < p < 1: c.ell(lerp(330, 750, p), 830, 9, fill=g(WH))
    mini_pulse(c, 540, 830, 18, 70, t, ts+0.5)
    pb = ap(t, tb, 0.4)
    if pb > 0:
        draw_line(c, (240, 900), (430, 1030), eo(ap(t, tb+.1, .45)), g(GRA), 3); draw_line(c, (840, 900), (650, 1030), eo(ap(t, tb+.1, .45)), g(GRA), 3)
        a, dy = appear(t, tb, 0.35); card(c, 370, 1010+dy, 710, 1240+dy, a, hi=ap(t, te, .3))
        c.poly([(425, 1090+dy), (655, 1090+dy), (680, 1130+dy), (400, 1130+dy)], g(SIL, a))
        for xx in (460, 505, 550, 595): c.ln([(xx, 1092+dy), (xx-8, 1128+dy)], 0, 3)
        c.rect(430, 1130+dy, 650, 1190+dy, line=g(SIL, a), r=4, w=3); c.rect(520, 1150+dy, 560, 1190+dy, line=g(SIL, a), r=3, w=3)
        c.tx(540, 1290+dy, 'YOUR BUSINESS', 'dm5', 30, g(SIL, a), 'mm', track=5)
        if t >= te: check(c, 540, 1050, 40, g(WH, ap(t, te, .25)), 6)

# ---------- C  analyze ----------
def sC(c, t):
    head(c, t, [(0, 4.1, 'STEP 02', 'Analyze the problem, define exactly what to do')])
    t0, tp, td = lw('C', 'S3', 0), lw('C', 'S3', 3), lw('C', 'S3', 4)
    ys = [590+98*k for k in range(4)]
    for k in range(4):
        a, dy = appear(t, 0.1*k, 0.35, 0.5); flag = k == 2 and t >= tp
        hi = eio(ap(t, tp, .3)) if k == 2 else 0
        card(c, 90, ys[k]+dy, 990, ys[k]+76+dy, a, hi); c.ell(145, ys[k]+38+dy, 18, line=g(lerp(GRA, WH, hi), a), w=3)
        c.rect(200, ys[k]+31+dy, 200+(300, 420, 360, 260)[k], ys[k]+45+dy, fill=g(lerp(GRA, WH, hi*.6), a), r=7)
        if flag: tri_warn(c, 915, ys[k]+38, 52, g(WH, ap(t, tp, .25)), 5)
    mp = eio(ap(t, t0, max(.2, tp-t0)))
    if t < tp+0.9:
        my = lerp(ys[0]+38, ys[2]+38, mp); fadem = 1-ap(t, tp+.3, .5); mx = 770
        if fadem > 0:
            c.ell(mx, my, 46, line=g(WH, fadem), w=5); c.ln([(mx+33, my+33), (mx+72, my+72)], g(WH, fadem), 8)
    a, dy = appear(t, td, 0.35)
    if a > 0:
        card(c, 90, 1040+dy, 990, 1350+dy, a)
        for k, ww in enumerate((420, 520, 360)):
            tk = lw('C', 'S3', 7+k); p = eo(ap(t, tk, .3)); yy = 1105+k*100+dy
            tick_box(c, 160, yy, 46, p); c.rect(220, yy-8, 220+ww, yy+8, fill=g(lerp(GRA, SIL, p), a), r=8)

# ---------- D  system ----------
def sD(c, t):
    head(c, t, [(0, lw('D', 'S4', 11)-.1, 'STEP 03', 'A complete system, custom-built for your business'),
                (lw('D', 'S4', 11)-.1, lw('D', 'S4', 14)-.1, 'STEP 03', 'From the very first workflow'),
                (lw('D', 'S4', 14)-.1, 8, 'STEP 03', 'To the AI and APIs we connect')])
    th, tb = lw('D', 'S4', 2), lw('D', 'S4', 8); tdone = lw('D', 'S4', 18)+.1
    done = eio(ap(t, tdone, .3))
    fr = 0.3+0.67*ap(t, 0, tb+.3)
    dashed_rect(c, 110, 580, 970, 1300, 1 if done > 0 else fr, g(lerp(GRA, WH, done)), 3)
    nx = (230, 540, 850); NY = 960
    # workflow nodes
    for k in range(3):
        a, dy = appear(t, lw('D', 'S4', 4+k), 0.35)
        lit = eio(ap(t, (lw('D', 'S4', 11), lw('D', 'S4', 11)+.5, lw('D', 'S4', 12)+.5)[k], .2))
        if a > 0:
            c.ell(nx[k], NY+dy, 54, fill=g(lerp(CH, WH, lit if k == 2 else lit), a), line=g(lerp(GRA, WH, lit), a), w=3)
            c.tx(nx[k], NY+dy, '0%d' % (k+1), 'sg6', 42, g(lerp(SIL, BK, lit), a), 'mm')
            if k < 2: c.ln([(nx[k]+54, NY), (nx[k+1]-54, NY)], g(GRA, a), 3)
    bolt(c, (nx[0]+54, NY), (nx[1]-54, NY), t, (t-lw('D', 'S4', 11))/0.5, 1, 14)
    bolt(c, (nx[1]+54, NY), (nx[2]-54, NY), t, (t-lw('D', 'S4', 12))/0.5, 1, 14)
    # AI block
    ta = lw('D', 'S4', 14); a, dy = appear(t, ta, .35)
    if a > 0:
        lit = eio(ap(t, ta+.5, .25)); card(c, 390, 680+dy, 690, 800+dy, a, lit)
        c.tx(540, 740+dy, 'AI', 'sg7', 60, g(lerp(SIL, WH, lit), a), 'mm', track=4)
        bolt(c, (540, 800), (540, NY-54), t, (t-ta)/0.5, 1, 14)
    # API cards
    tp = lw('D', 'S4', 15)
    for k in range(3):
        a, dy = appear(t, tp+0.12*k, .35)
        if a > 0:
            lit = eio(ap(t, tp+.5+.12*k, .25)); cx = (230, 540, 850)[k]
            card(c, cx-100, 1150+dy, cx+100, 1240+dy, a, lit, 0, 14)
            c.tx(cx, 1195+dy, 'API', 'dm5', 34, g(lerp(GRA, WH, lit), a), 'mm', track=6)
            bolt(c, (cx, NY+54), (cx, 1150), t, (t-tp-0.12*k)/0.5, 1, 12)
    if t > tdone: mini_pulse(c, 540, 940, 300, 400, t, tdone, .8)

# ---------- E  solve ----------
def sE(c, t):
    head(c, t, [(0, 3.0, 'GOAL', 'Solving the problem in the best way possible')])
    ts, te = lw('E', 'S5', 4), lw('E', 'S5', 6)
    A_ = 170*(1-eio(ap(t, ts, 0.9))); N = 260; pts = []
    for i in range(N+1):
        u = i/N; pts.append((130+820*u+A_*0.5*math.sin(2*math.pi*6*u+t*1.5), 900+A_*math.sin(2*math.pi*4.5*u+1.2+t*1.2)*math.sin(math.pi*u)**0.6))
    a = 0.55+0.45*eo(ap(t, 0, .4)); c.ln(pts, g(WH, a), 5)
    c.ell(130, 900, 12, fill=g(WH, a)); done = eio(ap(t, te, .3))
    c.ell(950, 900, 40, fill=g(WH, done) if done > .5 else None, line=g(lerp(GRA, WH, done), a), w=4)
    if done > .5: check(c, 950, 900, 36, 0, 6)
    c.tx(130, 1130, 'THE PROBLEM', 'dm5', 30, g(SIL, a), 'lm', track=5); c.tx(950, 1130, 'THE BEST WAY', 'dm5', 30, g(lerp(GRA, WH, done), a), 'rm', track=5)
    mini_pulse(c, 950, 900, 45, 110, t, te)

# ---------- F  not alone ----------
def box_icon(c, cx, cy, s, col, w=4):
    c.rect(cx-s/2, cy-s/2, cx+s/2, cy+s/2, line=col, r=4, w=w); c.ln([(cx-s/2, cy-s*.1), (cx+s/2, cy-s*.1)], col, w); c.ln([(cx, cy-s/2), (cx, cy-s*.1)], col, w)
def sF(c, t):
    head(c, t, [(0, 5.1, 'THE DIFFERENCE', "We won't hand it over and leave you alone")])
    t5, t6, t9, t11 = lw('F', 'S6', 5), lw('F', 'S6', 6), lw('F', 'S6', 9), lw('F', 'S6', 11)
    a, dy = appear(t, 0, .35, 0.55); person(c, 230, 900, 170, g(SIL, a)); c.tx(230, 1040, 'YOU', 'dm5', 30, g(WH, a), 'mm', track=6)
    card(c, 740, 790, 960, 1010, a); gear_o(c, 850, 900, 70, t*30, g(WH, a), fill=True, hole=g(CH, a)); c.tx(850, 1040, 'US', 'dm5', 30, g(WH, a), 'mm', track=6)
    # hand-off attempt blocked
    px = ap(t, t6, 0.9)
    if px > 0 and t < t6+1.4:
        x = lerp(700, 540, eo(px)); fa = 1-ap(t, t6+.7, .5)
        box_icon(c, x, 900, 64, g(SIL, fa)); c.ln([(710, 900), (340, 900)], g(GRA, fa*.7), 2)
    xa = eio(ap(t, t5, .25))
    if xa > 0 and t < t9: cross(c, 540, 900, 110*xa, g(WH), 9)
    lk = eo(ap(t, t9, .5)); draw_line(c, (330, 900), (730, 900), lk, g(WH), 4)
    if lk >= 1:
        dots_on(c, (330, 900), (730, 900), t, 1, 2, .9); dots_on(c, (330, 900), (730, 900), t+.3, 0.0, 1)
    mini_pulse(c, 230, 880, 100, 170, t, t11, .7); mini_pulse(c, 850, 900, 120, 190, t, t11, .7)

# ---------- G  monthly + technical ----------
def sG(c, t):
    tsw = T.w('S8', 0)[0]-T.START['G']-0.1
    head(c, t, [(0, tsw, 'MONTHLY PLAN', 'Monthly plan, operation and costs included'), (tsw, 10, 'WE HANDLE', 'The technical side')])
    d1 = 1-ap(t, tsw-.3, .35)
    if d1 > 0:
        a, dy = appear(t, 0, .35, .55); a *= d1; card(c, 150, 590, 930, 990, a); c.tx(190, 628, 'MONTH', 'dm5', 26, g(GRA, a), 'lm', track=6)
        t5, t6 = lw('G', 'S7', 5), lw('G', 'S7', 7)
        for k in range(28):
            col, row = k % 7, k//7; fk = ap(t, t5+(t6-t5)*k/28, .2)
            x0 = 195+col*100; y0 = 665+row*80
            c.rect(x0, y0, x0+90, y0+60, fill=g(lerp(CH, SIL, fk*.55), a), line=g(lerp(GRA, SIL, fk), a), r=8, w=2)
        for r_, (i, lab) in enumerate(((8, 'OPERATION'), (10, 'RUNNING COSTS'))):
            tk = lw('G', 'S7', i); aa, dy = appear(t, tk, .35); aa *= d1
            if aa > 0:
                y = 1030+r_*105+dy; card(c, 150, y, 930, y+82, aa, eio(ap(t, tk+.35, .25)))
                c.tx(190, y+41, lab, 'dm5', 30, g(WH, aa), 'lm', track=5); c.tx(830, y+41, 'INCLUDED', 'dm5', 26, g(SIL, aa), 'rm', track=4)
                if t > tk+.35: check(c, 885, y+41, 30, g(WH, ap(t, tk+.35, .2)*aa), 5)
    a2 = ap(t, tsw+.1, .3)
    if a2 > 0:
        tiles = [(5, 'CODE', 0, 0), (6, 'APIs', 1, 0), (8, 'MAINTENANCE', 0, 1), (9, 'SUPPORT', 1, 1)]
        for idx, lab, cx_, cy_ in tiles:
            tt = lw('G', 'S8', idx); x0 = 130+cx_*430; y0 = 620+cy_*290
            aa, dy = appear(t, tsw+.2+.08*(cy_*2+cx_), .35); lit = eio(ap(t, tt, .25))
            if aa <= 0: continue
            card(c, x0, y0+dy, x0+390, y0+240+dy, aa, lit); cx, cy = x0+195, y0+95+dy; col = g(lerp(GRA, WH, lit), aa)
            if lab == 'CODE': c.ln([(cx-30, cy-34), (cx-70, cy), (cx-30, cy+34)], col, 7); c.ln([(cx+30, cy-34), (cx+70, cy), (cx+30, cy+34)], col, 7); c.ln([(cx+12, cy-40), (cx-12, cy+40)], col, 6)
            elif lab == 'APIs':
                c.rect(cx-74, cy-26, cx-20, cy+26, line=col, r=6, w=5); c.rect(cx+20, cy-26, cx+74, cy+26, line=col, r=6, w=5)
                c.ln([(cx-20, cy-12), (cx+20, cy-12)], col, 5); c.ln([(cx-20, cy+12), (cx+20, cy+12)], col, 5)
            elif lab == 'MAINTENANCE': gear_o(c, cx, cy, 46, t*40*lit, col, 5)
            else: chat_icon(c, cx, cy, 100, col); [c.ell(cx-22+k*22, cy-6, 4, fill=col) for k in range(3)]
            c.tx(x0+195, y0+196+dy, lab, 'dm5', 30, g(lerp(SIL, WH, lit), aa), 'mm', track=5)
            mini_pulse(c, x0+195, y0+120, 150, 230, t, tt, .6, 2)

# ---------- H  you / system ----------
def sH(c, t):
    head(c, t, [(0, 3.3, 'YOU FOCUS', 'You focus on your business, we care for the system')])
    t2, t7 = lw('H', 'S9', 2), lw('H', 'S9', 7)
    a, dy = appear(t, 0, .35, .55); hl = eio(ap(t, t2, .3)); hr = eio(ap(t, t7, .3))
    card(c, 110, 690, 490, 1070, a, hl); card(c, 590, 690, 970, 1070, a, hr)
    cl_ = g(lerp(SIL, WH, hl), a)
    c.poly([(215, 800), (385, 800), (410, 855), (190, 855)], cl_)
    for xx in (245, 285, 325, 365): c.ln([(xx, 802), (xx-6, 853)], 0, 3)
    c.rect(210, 855, 390, 985, line=cl_, r=4, w=4); c.rect(275, 915, 325, 985, line=cl_, r=3, w=4)
    gear_o(c, 780, 880, 100, t*(25+90*hr), g(lerp(SIL, WH, hr), a), fill=True, hole=g(lerp(CH, CH, 0), a))
    if hr > 0:
        ang = t*3.2; c.ell(780+math.cos(ang)*140, 880+math.sin(ang)*140, 8, fill=g(WH, hr))
    draw_line(c, (490, 880), (590, 880), 1, g(GRA, a), 3); dots_on(c, (490, 880), (590, 880), t, a, 1, .8)
    c.tx(300, 1125, 'YOUR BUSINESS', 'dm5', 30, g(lerp(SIL, WH, hl), a), 'mm', track=5); c.tx(780, 1125, 'THE SYSTEM', 'dm5', 30, g(lerp(SIL, WH, hr), a), 'mm', track=5)
    mini_pulse(c, 300, 880, 200, 270, t, t2, .6); mini_pulse(c, 780, 880, 200, 270, t, t7, .6)

# ---------- I  call to action ----------
def sI(c, t):
    tb = lw('I', 'S10', 8)
    head(c, t, [(0, tb-.1, 'AUTOMATE IT', 'Operations wasting your time?'), (tb-.1, 7, 'AUTOMATE IT', 'Send us a DM')])
    tc = lw('I', 'S10', 15)
    for k in range(3):
        ta = lw('I', 'S10', 2)+0.28*k; a, dy = appear(t, ta, .35, 0.55 if k == 0 else 0)
        if a <= 0: continue
        y = 590+k*125; tk = tc+0.3*k; conv = eio(ap(t, tk, .3))
        card(c, 110, y+dy, 970, y+100+dy, a, conv)
        if conv < .5: clock(c, 190, y+50+dy, 34, (t*540+k*70) % 360, g(SIL, a*(1-conv*2)), 3)
        else: gear_o(c, 190, y+50+dy, 36, t*60+k*20, g(WH, a), 5)
        c.rect(260, y+43+dy, 260+(360, 440, 300)[k], y+57+dy, fill=g(lerp(GRA, SIL, conv), a), r=7)
        if conv > .5: check(c, 900, y+50+dy, 40, g(WH, a), 6)
    a, dy = appear(t, tb, .35)
    if a > 0:
        c.rect(240, 1030+dy, 840, 1230+dy, fill=g(WH, a), r=100); c.poly([(300, 1215+dy), (360, 1215+dy), (290, 1280+dy)], g(WH, a))
        td = lw('I', 'S10', 10)
        if t < td:
            for k in range(3):
                ph = (t*3-k*.33) % 1; c.ell(470+k*70, 1130+dy, 10+6*max(0, math.sin(ph*math.pi)), fill=g(BK, a))
        else: c.tx(540, 1138+dy, 'DM', 'sg7', 120, 0, 'mm')
        pp = ap(t, td, .8)
        if 0 < pp < 1: e = 50*eo(pp); c.rect(240-e, 1030-e+dy, 840+e, 1230+e+dy, line=g(SIL, 1-pp), r=100+e, w=3)

SCENE_FN = {'A': sA, 'B': sB, 'C': sC, 'D': sD, 'E': sE, 'F': sF, 'G': sG, 'H': sH, 'I': sI}
