# -*- coding: utf-8 -*-
"""Nine shots built from the user's visual plan. Every scene is a pure function of local time t (seconds since the scene start).
Text policy: headline in shot 1 only; afterwards only captions (captions.py). Words inside pictured objects (order ids, clock digits,
counter numbers) are part of the drawing, not overlays."""
import math
from lib import *
import timeline as T
def G(sc, t): return t+T.START[sc]
def num(c, x, y, s, sz, fill, anc='mm'): c.tx(x, y, s, 'sg7', sz, fill, anc)
def arw(fn, sz, s): return font(fn, sz).getlength(s, direction='rtl', language='ar')/S

# ---------------- icons / shared drawing ----------------
def table(c, tg, x0, y0, w, h, a=1.0, rh=74, done=None, scale_pos=None):
    """Spreadsheet of order rows; rows drop in from the top, one after another, and the scroll never stops."""
    hdr = 52; p = T.pos(tg) if scale_pos is None else scale_pos
    c.rect(x0, y0, x0+w, y0+h, line=g(GRA, a), r=14, w=2)
    c.rect(x0, y0, x0+w, y0+hdr, fill=g(CH, a), line=g(GRA, a), r=14, w=2)
    cx1, cx2 = x0+w*0.30, x0+w*0.72
    for cx in (cx1, cx2): c.ln([(cx, y0), (cx, y0+h)], g(GRA, a), 2)
    for cx, ww in ((x0+w*0.05, 0.12), (cx1+w*0.04, 0.2), (cx2+w*0.04, 0.12)): c.rect(cx, y0+hdr/2-5, cx+w*ww, y0+hdr/2+5, fill=g(SIL, a*0.8), r=5)
    base = int(math.floor(p)); frac = p-base; n = int((h-hdr)//rh)
    for k in range(n+1):
        idx = base-k
        if idx < 0: continue
        y = y0+hdr+(k+frac)*rh
        if y+rh > y0+h+1: continue
        ra = a*(eo(frac) if k == 0 else 1.0)
        if k == n: ra = a*(1-frac)
        if ra <= 0.02: continue
        c.ln([(x0, y+rh), (x0+w, y+rh)], g(GRA, ra), 2)
        c.tx(x0+w*0.05, y+rh/2, '#%d' % (1000+idx), 'dm5', 36 if rh >= 70 else 30, g(SIL, ra), 'lm')
        bw = (w*0.42-w*0.08)*(0.35+0.6*((idx*37) % 10)/10)
        c.rect(cx1+w*0.04, y+rh/2-8, cx1+w*0.04+bw, y+rh/2+8, fill=g(SIL, ra*0.85), r=8)
        bx = cx2+w*0.14; dn = done(k, tg, idx) if done else 0
        c.rect(bx-17, y+rh/2-17, bx+17, y+rh/2+17, fill=g(WH, ra) if dn else None, line=g(WH if dn else GRA, ra), r=7, w=2)
        if dn: check(c, bx, y+rh/2, 22, 0, 4)

def truck(c, cx, cy, s, col, w=4):
    c.rect(cx-s*.55, cy-s*.35, cx+s*.12, cy+s*.2, line=col, r=6, w=w)
    c.ln([(cx+s*.12, cy-s*.15), (cx+s*.4, cy-s*.15), (cx+s*.55, cy+s*.05), (cx+s*.55, cy+s*.2), (cx+s*.12, cy+s*.2)], col, w)
    c.ell(cx-s*.3, cy+s*.28, s*.1, fill=col); c.ell(cx+s*.33, cy+s*.28, s*.1, fill=col)
def grid_icon(c, cx, cy, s, col, w=4):
    c.rect(cx-s/2, cy-s*.42, cx+s/2, cy+s*.42, line=col, r=8, w=w)
    c.ln([(cx-s/2, cy), (cx+s/2, cy)], col, w*.7); c.ln([(cx-s/6, cy-s*.42), (cx-s/6, cy+s*.42)], col, w*.7); c.ln([(cx+s/6, cy-s*.42), (cx+s/6, cy+s*.42)], col, w*.7)
def pin(c, cx, cy, s, col, w=4):
    c.ell(cx, cy-s*.12, s*.3, line=col, w=w); c.ln([(cx-s*.27, cy+s*.05), (cx, cy+s*.5), (cx+s*.27, cy+s*.05)], col, w); c.ell(cx, cy-s*.12, s*.1, fill=col)
def handset(c, cx, cy, s, col, w=14):
    pts = [(cx-s*.42+math.cos(math.radians(a))*s*.5, cy+s*.12+math.sin(math.radians(a))*s*.5) for a in range(-30, 41, 7)]
    pts = [(cx+math.cos(math.radians(a))*s*.5-s*.05, cy+math.sin(math.radians(a))*s*.5) for a in range(130, 231, 6)]
    c.ln([(cx-s*.5, cy-s*.45), (cx-s*.22, cy-s*.45)], col, w); c.ln([(cx-s*.5, cy+s*.45), (cx-s*.22, cy+s*.45)], col, w)
    c.ln([(cx-s*.5, cy-s*.45), (cx-s*.38, cy-s*.1), (cx-s*.38, cy+s*.1), (cx-s*.5, cy+s*.45)], col, w)
    c.ln([(cx-s*.38, cy-s*.1), (cx+s*.12, cy-s*.45)], col, w*.8); c.ln([(cx-s*.38, cy+s*.1), (cx+s*.12, cy+s*.45)], col, w*.8)
def phone(c, cx, cy, s, col, w=8):          # smartphone body, simple and readable
    c.rect(cx-s*.34, cy-s*.6, cx+s*.34, cy+s*.6, line=col, r=s*.1, w=w)
    c.ln([(cx-s*.1, cy-s*.5), (cx+s*.1, cy-s*.5)], col, w*.6); c.ell(cx, cy+s*.5, s*.05, fill=col)
    c.rect(cx-s*.26, cy-s*.38, cx+s*.26, cy+s*.38, fill=g(CH), r=8)
def hand(c, cx, cy, s, col):
    c.rect(cx-s*.32, cy-s*.05, cx+s*.32, cy+s*.5, fill=col, r=s*.12)
    for i, (dx, hh) in enumerate(((-.27, .5), (-.09, .62), (.09, .6), (.27, .48))):
        c.rect(cx+s*dx-s*.075, cy-s*hh, cx+s*dx+s*.075, cy+s*.1, fill=col, r=s*.07)
    c.rect(cx-s*.52, cy+s*.02, cx-s*.28, cy+s*.3, fill=col, r=s*.1)
def code_icon(c, cx, cy, s, col, w=8):
    c.ln([(cx-s*.15, cy-s*.35), (cx-s*.5, cy), (cx-s*.15, cy+s*.35)], col, w); c.ln([(cx+s*.15, cy-s*.35), (cx+s*.5, cy), (cx+s*.15, cy+s*.35)], col, w)
    c.ln([(cx+s*.08, cy-s*.4), (cx-s*.08, cy+s*.4)], col, w*.7)
def server(c, cx, cy, s, col, w=5):
    for k in range(3):
        y = cy+(k-1)*s*.34; c.rect(cx-s*.45, y-s*.13, cx+s*.45, y+s*.13, line=col, r=8, w=w); c.ell(cx+s*.3, y, s*.04, fill=col)
def calendar(c, cx, cy, s, col, w=5):
    c.rect(cx-s*.45, cy-s*.4, cx+s*.45, cy+s*.45, line=col, r=10, w=w); c.ln([(cx-s*.45, cy-s*.12), (cx+s*.45, cy-s*.12)], col, w)
    c.ln([(cx-s*.22, cy-s*.5), (cx-s*.22, cy-s*.3)], col, w); c.ln([(cx+s*.22, cy-s*.5), (cx+s*.22, cy-s*.3)], col, w)
def loop_arrow(c, cx, cy, r, col, w=6):
    c.arc(cx, cy, r, 40, 330, col, w); a = math.radians(330); x, y = cx+math.cos(a)*r, cy+math.sin(a)*r
    c.poly([(x-4, y-22), (x+20, y-2), (x-10, y+10)], col)
def gear_o(c, cx, cy, r, rot, col, w=5, teeth=10):
    pts = []
    for i in range(teeth):
        b = rot+i*360/teeth
        for da, rr in ((-10, .8), (-6, 1), (6, 1), (10, .8)):
            a = math.radians(b+da); pts.append((cx+math.cos(a)*r*rr, cy+math.sin(a)*r*rr))
    c.ln(pts+[pts[0]], col, w); c.ell(cx, cy, r*.35, line=col, w=w)
def slash(c, x0, y0, x1, y1, p, col, w=9):
    if p > 0: c.ln([(x0, y0), (lerp(x0, x1, p), lerp(y0, y1, p))], col, w)
def card_row(c, x, y, w, h, idn, a=1, hi=0, done=0):
    c.rect(x, y, x+w, y+h, fill=g(WH if done else CH, a), line=g(lerp(GRA, WH, max(hi, done)), a), r=14, w=2)
    c.tx(x+22, y+h/2, '#%d' % idn, 'dm5', 36, g(BK if done else SIL, a), 'lm')
    if done: check(c, x+w-40, y+h/2, 26, 0, 5)

# ---------------- S1 hook (headline shot) ----------------
def s1(c, t):
    N = 100 if t < 0.02 else int(round(100*eo(ap(t, 0.03, 1.25))))
    ha = 1-ap(t, T.END['S1']-T.START['S1']-0.2, 0.2)               # headline leaves with a quick 0.2 s exit
    c.ar(540, 560, '١٠٠ أوردر', 150, g(WH, ha), 'mm'); c.ar(540, 735, 'وخسران؟', 150, g(WH, ha), 'mm')
    c.ar(1020, 268, 'مثال', 52, g(SIL, ha), 'rm', fn='ca6')       # example tag (the figures are illustrative)
    cart(c, 220, 985, 130, g(SIL), 6)
    num(c, 630, 985, str(N), 230, g(WH))
    if t < 1.3: c.ln([(900, 900+80*((N % 2))), (900, 960+80*((N % 2)))], g(SIL, .8), 5)   # tick mark per count
    # profit falls through zero and becomes a minus sign
    coin = lambda a: (c.ell(220, 1235, 62, line=g(SIL, a), w=6), c.ln([(220, 1187), (220, 1283)], g(SIL, a), 6))
    if 1.9 <= t < 3.4:
        pv = max(0, 9-int(10*ap(t, 2.0, 1.3))); coin(1); num(c, 630, 1235, str(pv), 190, g(WH))
    elif t >= 3.4:
        pa = 0.45+0.55*eo(ap(t, 3.4, 0.25)); coin(pa)
        c.rect(430, 1213, 830, 1257, fill=g(WH, pa), r=8)
        sparkle_ring(c, 630, 1235, 120, 205, (t-3.4)/0.7, SIL, 4)
        if t > 4.3: sparkle_ring(c, 630, 1235, 120, 205, (t-4.3)/0.7, SIL, 4)

# ---------------- S2 midnight ----------------
def midnight(c, tg, a, done=None, pos=None):
    blink = 1 if int(tg*2) % 2 == 0 else 0.35
    num(c, 400, 400, '00', 210, g(WH, a)); num(c, 540, 395, ':', 210, g(WH, a*blink)); num(c, 680, 400, '00', 210, g(WH, a))
    for k, al in ((3, .10), (2, .18), (1, .3)): c.rect(100-k*6, 560-k*6, 920+k*6, 1300+k*6, line=g(WH, al*a), r=16, w=2)   # the sheet is the only light
    table(c, tg, 100, 560, 820, 740, a, rh=74, done=done, scale_pos=pos)
def s2(c, t):
    midnight(c, G('S2', t), 0.55+0.45*eo(ap(t, 0, 0.3)))

# ---------------- S3 two hours ----------------
def s3(c, t):
    tg = G('S3', t); p = eio(ap(t, 0, 0.5))
    x0, w, y0, h = lerp(100, 50, p), lerp(840, 400, p), lerp(560, 640, p), lerp(740, 650, p)
    table(c, tg, x0, y0, w, h, 1.0, rh=lerp(74, 62, p))
    q = ap(t, 0.15, 2.5); mins = int(120*q); hh, mm = divmod(mins, 60)
    cxx, cyy = 745, 850; r = 200
    num(c, cxx, 470, '%02d:%02d' % (hh, mm), 120, g(WH, 0.5+0.5*p))
    c.ar(540, 310, 'ساعتين', 110, g(WH, eo(ap(t, 0.25, 0.3))), 'mm')
    ang = (t-0.15)*720 if t > 0.15 else 0
    c.ell(cxx, cyy, r, line=g(GRA), w=4)
    for i in range(12):
        a_ = math.radians(i*30); c.ln([(cxx+math.sin(a_)*r*.84, cyy-math.cos(a_)*r*.84), (cxx+math.sin(a_)*r*.95, cyy-math.cos(a_)*r*.95)], g(SIL), 4)
    a_ = math.radians(ang); c.ln([(cxx, cyy), (cxx+math.sin(a_)*r*.8, cyy-math.cos(a_)*r*.8)], g(WH), 12)
    a_ = math.radians(ang/12); c.ln([(cxx, cyy), (cxx+math.sin(a_)*r*.5, cyy-math.cos(a_)*r*.5)], g(WH), 16); c.ell(cxx, cyy, 14, fill=g(WH))

# ---------------- S4 shipping ----------------
def s4(c, t):
    X = (200, 540, 880)
    for cx in X: c.rect(cx-125, 470, cx+125, 1150, line=g(GRA), r=18, w=2)
    grid_icon(c, X[0], 395, 90, g(SIL)); truck(c, X[1], 395, 100, g(SIL)); pin(c, X[2], 390, 90, g(GRA))
    for i, y in enumerate((540, 650, 760, 870)):                              # sheet column rows
        a_ = eo(ap(t, 0.05*i, 0.3))
        if i == 0: continue
        card_row(c, X[0]-105, y, 210, 84, 1010+i, a_)
    # row A goes to shipping (D1)
    p = eio(ap(t, G('S4', 0)-T.START['S4']+ (T.w('D1', 0)-T.START['S4'])-0.05, 0.5))
    x = lerp(X[0]-105, X[1]-105, p); card_row(c, x, 540, 210, 84, 1010, 1, hi=p)
    for i, yy in enumerate((650, 760)):
        if t > T.w('D1', 1)-T.START['S4']: card_row(c, X[1]-105, 540+110*0 if False else 650+110*i, 210, 84, 1030+i, 0.8)
    # bad row: exclamation square, then the arrow to the wrong column and it gets lost
    ts = T.w('D2', 0)-T.START['S4']; tm = T.w('D3', 0)-T.START['S4']; tl = T.w('D3', 3, 1)-T.START['S4']
    bx, by = X[0]-105, 980
    mv = eio(ap(t, tm, 0.7)); fade = 1-ap(t, tm+0.8, 0.9)
    x = lerp(bx, X[2]-105, mv); y = by+jit(t, mv)
    card_row(c, x, y, 210, 84, 1044, max(0.0, fade), hi=1)
    ea = eo(ap(t, ts, 0.3))
    if ea > 0 and mv < 1:
        sq = 74; sx, sy = x+210-sq*.5, y-sq*.55
        c.rect(sx, sy, sx+sq, sy+sq, fill=g(CH, ea*max(0, fade)), line=g(WH, ea*max(0, fade)), r=10, w=3)
        c.ln([(sx+sq/2, sy+16), (sx+sq/2, sy+sq/2+6)], g(WH, ea*max(0, fade)), 7); c.ell(sx+sq/2, sy+sq-16, 4.5, fill=g(WH, ea*max(0, fade)))
    if mv > 0 and mv < 1.0 or (mv >= 1 and fade > 0):
        pa = 0.35+0.65*eo(ap(t, tm-0.05, 0.2))
        c.ln([(X[0]+20, by+42), (lerp(X[0]+20, X[2]-130, eo(ap(t, tm-0.05, 0.6))), by+42)], g(SIL, pa*max(0.2, fade)), 4)
        if t > tm+0.45: c.poly([(X[2]-118, by+42), (X[2]-148, by+26), (X[2]-148, by+58)], g(SIL, pa*max(0.2, fade)))
    if mv >= 1: sparkle_ring(c, X[2], by+42, 70, 150, (t-(tm+0.7))/0.8, SIL, 3)
    c.ar(540, 1255, 'عنوان غلط', 110, g(WH, eo(ap(t, ts, 0.25))), 'mm')
def jit(t, mv): return math.sin(t*60)*4*max(0, mv-0.85)/0.15 if mv > 0.85 else 0.0

# ---------------- S5 phone ----------------
def s5(c, t):
    tg = G('S5', t); sh = math.sin(t*38)*16*(1-ap(t, 0.0, 1.0))+math.sin(t*40)*6*(ap(t, 1.3, 0.05)-ap(t, 1.7, 0.2))
    ta = eo(ap(t, 0.15, 0.3)); c.ar(540, 305, 'تأكيد بالتليفون', 110, g(WH, ta), 'mm')
    phone(c, 540+sh, 520, 210, g(WH))
    for k in range(3):
        for sgn in (-1, 1):
            if (int(t*6)+k) % 3 != 0 or t > 1.9: continue
            c.arc(540+sgn*160, 520, 36+k*24, 300 if sgn > 0 else 120, 60 if sgn > 0 else 240, g(SIL, 0.8), 5)
    tt = [17.8+0.3*i for i in range(6)]
    for i in range(6):
        y = 690+94*i; a = eo(ap(t, 0.15+0.12*i, 0.25)); dn = tg >= tt[i]
        al = a*(0.35 if dn else 1.0); x = 90
        c.rect(x, y, 930, y+84, fill=g(CH, al*0.8), line=g(WH if not dn else GRA, al), r=16, w=2)
        c.tx(x+26, y+42, '#%d' % (1060+i), 'dm5', 40, g(WH if not dn else SIL, al), 'lm')
        c.rect(x+230, y+34, x+230+(120+((i*53) % 5)*40), y+50, fill=g(WH if not dn else SIL, al*0.9), r=8)
        bx = 930-72
        c.rect(bx-28, y+14, bx+28, y+70, fill=g(WH, a) if dn else None, line=g(WH if dn else GRA, a), r=10, w=3)
        if dn: check(c, bx, y+42, 36, 0, 6)

# ---------------- S6 peak: white block, black counter ----------------
def s6(c, t):
    c.rect(0, 0, 1080, 1920, fill=255, r=0)
    N = int(round(40*eo(ap(t, 0.1, 1.55))))
    shk = 0.0; q = ap(t, 2.0-0.05, 0.28)
    if 0 < q < 1: shk = math.sin(q*math.pi*2)*18*(1-q)
    ux, uy = 540+shk, 300; c.arc(ux, uy+20, 80, 180, 360, 0, 14); c.ln([(ux-80, uy+20), (ux-80, uy+100)], 0, 14)
    c.poly([(ux+80-30, uy+14), (ux+80+30, uy+14), (ux+80, uy+76)], 0)
    num(c, 540+shk, 650, str(N), 400, 0)
    c.ar(540+shk, 950, '٤٠ مرتجع', 130, 0, 'mm')
    cols, rows = 10, 4
    for i in range(cols*rows):
        if i < N:
            gx = 540-(cols*52)/2+(i % cols)*52+26+shk; gy = 1110+(i//cols)*52
            c.rect(gx-18, gy-18, gx+18, gy+18, fill=0, r=6)

# ---------------- S7 hand leaves, the rows carry on alone ----------------
def s7(c, t):
    tg = G('S7', t); table(c, tg, 290, 470, 640, 700, 1.0, rh=70)
    tw0 = T.w('W2', 0)-T.START['S7']; ts = T.w('W2', 1)-T.START['S7']
    ha = 1-eo(ap(t, ts+0.55, 0.4)); hy = 820+math.sin(t*5)*14
    if ha > 0.01:
        hand(c, 150, hy, 190, g(SIL, ha)); slash(c, 60, hy-100, 240, hy+110, eo(ap(t, ts, 0.35)), g(WH, ha), 10)
    tk = T.w('W2', 3)-T.START['S7']; tsy = tk+0.45          # strike, then the replacement word
    a1 = eo(ap(t, tw0-0.05, 0.3))*(1-ap(t, tsy-0.1, 0.2)); w1 = arw('ca7', 110, 'الشغل اليدوي')
    if a1 > 0.01:
        c.ar(540, 330, 'الشغل اليدوي', 110, g(WH, a1), 'mm')
        p = eo(ap(t, tk, 0.3))
        if p > 0: c.ln([(540+w1/2+10, 330), (540+w1/2+10-(w1+20)*p, 330)], g(SIL, a1), 9)
    a2 = eo(ap(t, tsy, 0.3))
    if a2 > 0.01: c.ar(540, 330, 'السيستم', 120, g(WH, a2), 'mm')

# ---------------- S8 the solution ----------------
LANES = [700+92*i for i in range(6)]; COLX = (60, 360, 660)
def spawn_list():
    out, s, i = [], 26.1, 0
    while s < 36.4: out.append((s, i)); s += 0.42 if s < 33.9 else 0.3; i += 1
    return out
SPAWN = spawn_list()
def s8(c, t):
    tg = G('S8', t)
    for cx in COLX: c.rect(cx, 560, cx+260, 1250, line=g(GRA, 0.8), r=18, w=2)
    grid_icon(c, COLX[0]+130, 625, 70, g(SIL)); truck(c, COLX[1]+130, 625, 78, g(SIL))
    c.ell(COLX[2]+130, 625, 36, line=g(SIL), w=4); check(c, COLX[2]+130, 625, 36, g(SIL), 5)
    for ts, i in SPAWN:
        f = 1.0 if ts < 33.9 else 0.55; d = tg-ts
        if d < 0 or d > 2.6*f: continue
        y = LANES[i % 6]; st = [0.0, 0.5*f, 0.95*f, 1.45*f, 1.9*f]
        if d < st[1]: x = COLX[0]+20; a = eo(ap(d, 0, 0.25))
        elif d < st[2]: x = lerp(COLX[0]+20, COLX[1]+20, eio(ap(d, st[1], 0.35*f))); a = 1
        elif d < st[3]: x = lerp(COLX[1]+20, COLX[2]+20, eio(ap(d, st[2]+0.1*f, 0.35*f))) if d > st[2]+0.1*f else COLX[1]+20; a = 1
        else: x = COLX[2]+20; a = 1
        dn = 1 if d >= st[3]+0.3*f else 0
        if d > st[4]: a = 1-ap(d, st[4], 0.7*f)
        card_row(c, x, y, 220, 76, 1100+i, a, hi=0, done=dn)
    # top band: tools (gears) -> the words code / servers, struck out -> monthly card -> seconds clock
    tc, tsv = T.w('X1', 10, 0)-T.START['S8'], T.w('X1', 12, 0)-T.START['S8']
    tools_a = eo(ap(t, 0.25, 0.4))*(1-ap(t, tc-0.45, 0.25))
    if tools_a > 0.01:
        gear_o(c, 430, 380, 76, t*30, g(WH, tools_a), 6); gear_o(c, 580, 332, 52, -t*45+15, g(SIL, tools_a), 5, 8); gear_o(c, 640, 430, 42, t*55, g(SIL, tools_a*0.8), 4, 8)
    k_a = eo(ap(t, tc-0.3, 0.3))*(1-ap(t, T.w('X1', 15, 1)-T.START['S8']+0.1, 0.3))
    if k_a > 0.01:
        wk, wsv = arw('ca7', 110, 'كود'), arw('ca7', 110, 'سيرفرات')
        c.ar(300, 380, 'كود', 110, g(WH, k_a), 'mm'); c.ar(730, 380, 'سيرفرات', 110, g(WH, k_a), 'mm')
        for cx, ww, t0 in ((300, wk, tc), (730, wsv, tsv)):
            p = eo(ap(t, t0, 0.28))
            if p > 0: c.ln([(cx+ww/2+10, 380), (cx+ww/2+10-(ww+20)*p, 380)], g(SIL, k_a), 9)
    t2 = T.w('X2', 0)-T.START['S8']; t3 = T.w('Y1', 0)-T.START['S8']
    m_a = eo(ap(t, t2, 0.3))*(1-ap(t, t3-0.1, 0.25))
    if m_a > 0.01:
        c.rect(150, 280, 930, 470, fill=g(CH, m_a), line=g(GRA, m_a), r=26, w=3)
        c.ar(540, 375, 'اشتراك شهري', 110, g(WH, m_a), 'mm')
    s_a = eo(ap(t, t3, 0.3))
    if s_a > 0.01:
        c.ell(540, 380, 105, line=g(SIL, s_a), w=5); ang = math.radians(((t-t3)*360*1.4) % 360)
        c.ln([(540, 380), (540+math.sin(ang)*85, 380-math.cos(ang)*85)], g(WH, s_a), 9); c.ell(540, 380, 11, fill=g(WH, s_a))

# ---------------- S9 CTA: FREE, then the shot-2 table returns with every row checked ----------------
def dm_line(c, cx, cy, sz, col):
    a = arw('ca7', sz, 'في الـ'); dmw = tw('sg7', sz*0.95, 'DM'); gap = sz*0.28; tot = a+gap+dmw; xl = cx-tot/2
    c.tx(xl, cy, 'DM', 'sg7', sz*0.95, col, 'lm'); c.ar(xl+tot, cy, 'في الـ', sz, col, 'rm')
def s9(c, t):
    tg = G('S9', t); tb = 1.95                                           # table returns
    A = eo(ap(t, 0.0, 0.2))*0.6+0.4 if t < 0.2 else 1-ap(t, tb-0.15, 0.2)
    if A > 0.01:
        c.ar(540, 500, 'ابعت', 120, g(WH, A), 'mm')
        num(c, 540, 745, 'FREE', 300, g(WH, A))
        dm_line(c, 540, 985, 120, g(WH, A))
        tf = T.w('C1', 1)-T.START['S9']; sparkle_ring(c, 540, 745, 270, 330, (t-tf)/0.6, SIL, 4)
    B = eo(ap(t, tb-0.1, 0.25))
    if B > 0.01:
        def dn(k, tg_, idx): return 1 if (tg_ >= T.START['S9']+tb+0.08*k) else 0
        midnight(c, tg, B, done=dn, pos=T.pos(T.START['S2'])+1.9*(tg-T.START['S9']))

SCENE_FN = {'S1': s1, 'S2': s2, 'S3': s3, 'S4': s4, 'S5': s5, 'S6': s6, 'S7': s7, 'S8': s8, 'S9': s9}
