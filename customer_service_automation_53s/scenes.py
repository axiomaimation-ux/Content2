"""Scenes A-J (all imagined by Claude). Each scene = pure function of local time t drawing on a black 2x layer (lib.Cv).
Layout is planned inside the Reels safe zone: content region x 70-1010, y 250-1390 before the 0.85 scale about (540, 845)."""
import math, random
from lib import *
import timeline as T

def A_(sc, n): return T.a(sc, n)
def dashln(c, p0, p1, col, w=2, d=14, gp=12):
    x0, y0 = p0; x1, y1 = p1; L = math.hypot(x1-x0, y1-y0); n = int(L//(d+gp))+1
    for k in range(n):
        s0 = k*(d+gp)/L; s1 = min(1, (k*(d+gp)+d)/L)
        if s0 < 1: c.ln([(lerp(x0, x1, s0), lerp(y0, y1, s0)), (lerp(x0, x1, s1), lerp(y0, y1, s1))], col, w)
def dashrect(c, cx, cy, w, h, col, wd=2):
    x0, y0, x1, y1 = cx-w/2, cy-h/2, cx+w/2, cy+h/2
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): dashln(c, p, q, col, wd)
def stubs(c, x, y, w, col, n=2, h=9, gap=16):
    for k in range(n): c.rect(x, y+k*gap, x+w*(1 if k < n-1 else 0.62), y+k*gap+h, fill=col, r=4)
def bub(c, cx, cy, w, h, kind, a=1.0):
    if kind == 'out':
        c.rect(cx-w/2, cy-h/2, cx+w/2, cy+h/2, fill=g(WH, a), r=h/2); stubs(c, cx-w/2+h*0.5, cy-h*0.22, w-h, 0, 2, h=max(6, h*0.14), gap=h*0.3)
    else:
        c.rect(cx-w/2, cy-h/2, cx+w/2, cy+h/2, fill=g(CH, a), line=g(SIL, a), r=h/2, w=2)
        stubs(c, cx-w/2+h*0.5, cy-h*0.22, w-h, g(SIL, a), 2, h=max(6, h*0.14), gap=h*0.3)
def pt(p0, p1, x): return (lerp(p0[0], p1[0], x), lerp(p0[1], p1[1], x))
def power(c, cx, cy, r, col, w=5):
    c.arc(cx, cy, r, -60, 240, col, w); c.ln([(cx, cy-r*1.15), (cx, cy-r*0.15)], col, w)
def warn(c, cx, cy, s, col, w=5):
    c.ln([(cx, cy-s*.55), (cx+s*.62, cy+s*.45), (cx-s*.62, cy+s*.45), (cx, cy-s*.55)], col, w)
    c.ln([(cx, cy-s*.18), (cx, cy+s*.12)], col, w); c.ell(cx, cy+s*.3, w*.55, fill=col)
def lock(c, cx, cy, s, col, w=4):
    c.rect(cx-s*.4, cy-s*.05, cx+s*.4, cy+s*.45, line=col, r=s*.08, w=w)
    c.arc(cx, cy-s*.05, s*.26, 180, 360, col, w); c.ln([(cx-s*.26, cy-s*.05), (cx-s*.26, cy-s*.2)], col, w); c.ln([(cx+s*.26, cy-s*.05), (cx+s*.26, cy-s*.2)], col, w)
    c.ell(cx, cy+s*.2, w*.7, fill=col)
def magnifier(c, cx, cy, r, col, w=5):
    c.ell(cx, cy, r, line=col, w=w); c.ln([(cx+r*.72, cy+r*.72), (cx+r*1.55, cy+r*1.55)], col, w+1)
def server(c, cx, cy, w, h, a=1.0, hi=0.0, leds=(0, 0, 0)):
    for k in range(3):
        y = cy+(k-1)*(h+16)
        c.rect(cx-w/2, y-h/2, cx+w/2, y+h/2, fill=g(CH, a), line=g(lerp(GRA, WH, hi), a), r=14, w=2)
        c.ell(cx-w/2+36, y, 8, fill=g(lerp(GRA, WH, leds[k]), a)); c.ell(cx-w/2+66, y, 8, fill=g(GRA, a))
        c.ln([(cx+w/2-110, y), (cx+w/2-36, y)], g(GRA, a), 4)
def docs(c, cx, cy, w, h, a=1.0, hi=0.0):
    c.rect(cx-w/2, cy-h/2, cx+w/2, cy+h/2, fill=g(CH, a), line=g(lerp(GRA, WH, hi), a), r=12, w=2)
    for k in range(3): c.ln([(cx-w/2+22, cy-h/2+34+k*30), (cx+w/2-22-(k==2)*50, cy-h/2+34+k*30)], g(lerp(GRA, SIL, hi), a), 4)
def node_ai(c, cx, cy, r, a=1.0, hi=1.0, sz=None, t=0.0, orbit=True):
    col = g(lerp(GRA, WH, hi), a)
    c.ell(cx, cy, r, fill=g(CH, a), line=col, w=3)
    c.tx(cx, cy-2, 'AI', 'sg7', sz or r*0.62, col, 'mm')
    if orbit:
        for k in range(3):
            ang = t*1.6+k*2.094; c.ell(cx+math.cos(ang)*(r+22), cy+math.sin(ang)*(r+22), 6, fill=g(SIL, a*0.9))

# ------------------------------------------------------------------ A  hook: the pipeline skeleton
def A(c, t):
    head(c, t, [(0, 99, 'CUSTOMER SERVICE', 'How I automated customer service')])
    ys = [660, 835, 1010, 1185, 1360]
    for k in range(4):
        p = eo(ap(t, 0.15+0.12*k, 0.5))
        if p > 0: c.ln([(540, ys[k]+20), (540, lerp(ys[k]+20, ys[k+1]-20, p))], g(GRA), 2)
    pulse = ap(t, 0.9, 1.9)                       # pulse runs down the line
    py = lerp(ys[0], ys[-1], pulse)
    for k, y in enumerate(ys):
        a, dy = appear(t, 0.1+0.1*k, 0.3, floor=0.5)
        lit = eo(ap(t, 0.0, 0.01)) * (1 if (pulse > 0 and py >= y-2) else 0)
        c.ell(540, y, 20, fill=g(WH if lit else CH, a), line=g(lerp(GRA, WH, lit), a), w=3)
        if lit and py-y < 120: sparkle_ring(c, 540, y, 22, 60, (py-y)/120)
    if 0 < pulse < 1: c.ell(540, py, 11, fill=WH)
    a1, d1 = appear(t, 0.25, 0.4, floor=0.5)
    bub(c, 270, ys[0], 300, 76, 'in', a1)
    a2 = eo(ap(t, 2.0, 0.4))
    if a2 > 0: bub(c, 810, ys[-1], 300, 76, 'out', a2)

# ------------------------------------------------------------------ B  01 trigger
def B(c, t):
    tq = A_('B', 'q'); tt = A_('B', 'trig'); twf = A_('B', 'wf'); tp = A_('B', 'proc')
    head(c, t, [(0, tq-0.05, '01 · TRIGGER', 'Defining the workflow trigger'), (tq, 99, '01 · TRIGGER', 'What starts the process?')])
    ys = [700, 920, 1140]
    # workflow bracket (appears with the word "workflow")
    pb = eo(ap(t, twf-0.1, 0.5))
    if pb > 0:
        c.ln([(150, ys[0]-70), (150, lerp(ys[0]-70, ys[2]+70, pb))], g(SIL), 2); c.ln([(150, ys[0]-70), (176, ys[0]-70)], g(SIL), 2); c.ln([(150, ys[2]+70), (176, ys[2]+70)], g(SIL, pb), 2)
        c.tx(150, ys[0]-104, 'WORKFLOW', 'dm5', 28, g(SIL, pb), 'lm', track=4)
    for k in (1, 2):
        a, _ = appear(t, 0.1+0.15*k, 0.3, floor=0.5)
        dashrect(c, 540, ys[k], 540, 120, g(GRA, a))
        if k == 1 and t >= tp-0.1:
            pa = eo(ap(t, tp-0.1, 0.3)); dashrect(c, 540, ys[k], 540, 120, g(SIL, pa)); c.tx(540, ys[k], 'PROCESS', 'dm5', 30, g(SIL, pa), 'mm', track=3)
        if pb > 0 and k >= 1: dashln(c, (540, ys[k-1]+60), (540, ys[k]-60), g(GRA, pb), 2)
    lit = ap(t, tt, 0.35)
    a, _ = appear(t, 0.0, 0.3, floor=0.5)
    card(c, 270, ys[0]-60, 810, ys[0]+60, a, hi=lit, fw=0)
    c.tx(560, ys[0], 'TRIGGER', 'dm5', 30, g(lerp(GRA, WH, lit), a), 'mm', track=3)
    power(c, 350, ys[0], 24, g(lerp(GRA, WH, lit), a), 4)
    # rings wait for the trigger (repeat), "?" next to it while the question is asked
    if t >= tt:
        for k in range(2):
            p = ((t-tt-0.5*k) % 1.4)/1.4
            if t-tt-0.5*k > 0: sparkle_ring(c, 350, ys[0], 28, 76, p, SIL, 3)
    if t >= tq:
        qa = eo(ap(t, tq, 0.4)); c.tx(870, ys[0], '?', 'sg7', 96, g(WH, qa), 'mm')

# ------------------------------------------------------------------ C  trigger = customer sends a WhatsApp message
def C(c, t):
    head(c, t, [(0, 99, '01 · TRIGGER', 'A customer sends a WhatsApp message')])
    tc = A_('C', 'cust'); tb = A_('C', 'bub'); ta = A_('C', 'arr'); tl = A_('C', 'bolt'); tf = A_('C', 'fill')
    y_p, y_w, y_t = 650, 1010, 1260
    a0, _ = appear(t, 0.0, 0.3, floor=0.5)
    pa = max(0.35, eo(ap(t, tc-0.1, 0.35)))
    person(c, 540, y_p, 100, g(WH, pa)); c.tx(540, y_p+82, 'CUSTOMER', 'dm5', 28, g(SIL, pa), 'mm', track=4)
    wl = ap(t, ta, 0.35)
    card(c, 250, y_w-55, 830, y_w+55, a0, hi=wl)
    chat_icon(c, 330, y_w, 56, g(lerp(GRA, WH, wl), a0))
    c.tx(570, y_w, 'WHATSAPP MESSAGE', 'dm5', 30, g(lerp(GRA, WH, wl), a0), 'mm', track=3)
    # message bubble travels person -> block
    pb = ap(t, tb, 0.45)
    if 0 < pb < 1:
        x, y = pt((540, y_p+150), (540, y_w-100), eio(pb)); bub(c, x, y, 230, 70, 'in', 1-0.6*ap(pb, 0.8, 0.2))
    ft = ap(t, tf, 0.3)
    card(c, 250, y_t-55, 830, y_t+55, a0, hi=ft, fw=ft)
    power(c, 330, y_t, 22, g(lerp(GRA, BK, ft), a0) if ft > 0.5 else g(GRA, a0), 4)
    c.tx(570, y_t, 'TRIGGER', 'dm5', 30, g(lerp(lerp(GRA, WH, 0), BK, ft), a0) if ft > 0.5 else g(GRA, a0), 'mm', track=3)
    bolt(c, (540, y_w+55), (540, y_t-55), t, (t-tl)/0.42, 1.0, amp=18)
    if ft > 0: sparkle_ring(c, 540, y_t, 300, 340, ap(t, tf+0.05, 0.4), SIL, 3) if False else None

# ------------------------------------------------------------------ D  the problem: WhatsApp Business API cost
def D(c, t):
    tp = A_('D', 'prob'); ta = A_('D', 'api'); tc = A_('D', 'cost'); tx = A_('D', 'cut')
    head(c, t, [(0, ta-0.05, 'THE PROBLEM', 'The first problem'), (ta, 99, 'THE PROBLEM', 'Cut the WhatsApp Business API cost')])
    # warning sign (first phrase)
    wa = min(max(0.55, eo(ap(t, 0.15, 0.35))), 1-ap(t, ta-0.05, 0.3))
    if wa > 0.01:
        warn(c, 540, 830, 190, g(WH, wa), 6)
        for k in range(2):
            p = ((t-0.5-0.55*k) % 1.5)/1.5
            if t > 0.5+0.55*k and t < ta: sparkle_ring(c, 540, 840, 120, 220, p, SIL, 3)
    # API block + cost bars
    ba = eo(ap(t, ta, 0.35))
    if ba > 0:
        by = 760
        cut = eo(ap(t, tx, 0.4))
        card(c, 130, by-70, 950, by+70, ba, hi=0.8*(1-cut))
        c.tx(540, by, 'WHATSAPP BUSINESS API', 'dm5', 30, g(lerp(WH, GRA, cut), ba), 'mm', track=3)
        heights = [90, 150, 130, 210, 190, 270, 320]
        for k, hh in enumerate(heights):
            gp = eo(ap(t, tc+0.1*k, 0.45)); hk = hh*gp*(1-0.88*cut)
            x = 215+k*100
            if hk > 1: c.rect(x-26, 1300-hk, x+26, 1300, fill=g(lerp(SIL, GRA, cut), ba), r=6)
        c.ln([(150, 1308), (930, 1308)], g(GRA, ba), 2)
        if tc-0.1 < t: c.tx(150, 962, 'COST', 'dm5', 28, g(SIL, eo(ap(t, tc, 0.3))), 'lm', track=4)
        if cut > 0:
            p = eo(ap(t, tx, 0.35)); c.ln([(130, by-70), (lerp(130, 950, p), lerp(by-70, by+70, p))], g(WH), 6)

# ------------------------------------------------------------------ E  02 python bridge
def E(c, t):
    tpy = A_('E', 'py'); tl = A_('E', 'link'); b1 = A_('E', 'b1'); b2 = A_('E', 'b2'); ts = A_('E', 'sysl')
    head(c, t, [(0, tpy+0.1, '02 · PYTHON', 'Linking messages to my system'), (tpy+0.1, 99, '02 · PYTHON', 'Python makes the link')])
    ytop, ymid, ybot = 680, 970, 1290
    a0, _ = appear(t, 0.0, 0.3, floor=0.55)
    lt = ap(t, b1+0.5, 0.3); ls = ap(t, ts, 0.3)
    block(c, 540, ytop, 480, 100, 'MESSAGES', hi=0.6+0.4*lt, a=a0)
    block(c, 540, ybot, 480, 100, 'MY SYSTEM', hi=0.4+0.6*ls, a=a0, fw=0)
    # search phase: dashed gap + magnifier sweeping, before Python arrives
    gone = ap(t, tpy, 0.3)
    if gone < 1:
        dashln(c, (540, ytop+50), (540, ybot-50), g(GRA, 1-gone), 2)
        mx = 540+math.sin(t*2.4)*200; my = 975+math.sin(t*1.7+1)*90
        magnifier(c, mx, my, 44, g(SIL, 1-gone), 5)
    # Python block drops in
    pp = eo(ap(t, tpy, 0.5))
    if pp > 0:
        y = lerp(ymid-150, ymid, pp); hi = 0.6+0.4*ap(t, b1+0.2, 0.3)
        block(c, 540, y, 440, 110, 'PYTHON', hi=hi, a=pp)
        lk = ap(t, tpy+0.3, 0.4)
        c.ln([(540, ytop+50), (540, lerp(ytop+50, ymid-55, lk))], g(GRA), 2); c.ln([(540, ymid+55), (540, lerp(ymid+55, ybot-50, lk))], g(GRA), 2)
    bolt(c, (540, ytop+50), (540, ymid-55), t, (t-b1)/0.45, 1.0, amp=20)
    bolt(c, (540, ymid+55), (540, ybot-50), t, (t-b2)/0.45, 1.0, amp=20)
    # message packets flow through after the link is made
    for k in range(3):
        p = ((t-(b2+0.5)-0.55*k)/1.5)
        if 0 < p < 1 and t > b2+0.5:
            x, y = pt((540, ytop+60), (540, ybot-60), p); bub(c, x, y, 120, 40, 'in', 1-0.5*ap(p, 0.8, 0.2))

# ------------------------------------------------------------------ F  03 AI agent
def F(c, t):
    tr = A_('F', 'ring'); tg = A_('F', 'agent'); tc = A_('F', 'cust')
    head(c, t, [(0, L_ := T.L('F', 'S6', 7)-0.05, '03 · AI AGENT', 'Adding an AI agent'), (T.L('F', 'S6', 7), 99, '03 · AI AGENT', 'It replies to customers')])
    cx, cy = 540, 960
    ra = max(0.5, eo(ap(t, tr-0.1, 0.4)))
    node_ai(c, cx, cy, 120, a=ra, hi=0.55+0.45*ap(t, tr, 0.4), t=t)
    la = eo(ap(t, tg, 0.3))
    if la > 0: c.tx(cx, cy+190, 'AI AGENT', 'dm5', 30, g(SIL, la), 'mm', track=4)
    pos = [(200, 700), (880, 700), (200, 1220), (880, 1220)]
    for k, (px, py) in enumerate(pos):
        pa = eo(ap(t, tc-0.1+0.12*k, 0.3))
        if pa > 0: person(c, px, py, 80, g(WH, pa))
        t0 = tc+0.05+0.27*k; p = ap(t, t0, 0.22); q = ap(t, t0+0.24, 0.22)
        src = (px+(80 if px < 540 else -80), py+(50 if py < 960 else -50)); dst = (cx+(-110 if px < 540 else 110)*0.9, cy+(-60 if py < 960 else 60))
        if 0 < p < 1: x, y = pt(src, dst, eio(p)); bub(c, x, y, 130, 46, 'in')
        if 0 < q < 1: x, y = pt(dst, src, eio(q)); bub(c, x, y, 130, 46, 'out')

# ------------------------------------------------------------------ G  04 Haiku + business info
def G(c, t):
    tm = A_('G', 'model'); ta = A_('G', 'anth'); tc = A_('G', 'cards'); ti = A_('G', 'info'); tcl = A_('G', 'client')
    head(c, t, [(0, tc-0.05, '04 · MODEL', 'Haiku model from Anthropic'), (tc, 99, '04 · MODEL', 'Loaded with the business info')])
    my = 790
    a0, _ = appear(t, 0.0, 0.3, floor=0.5)
    fill = [ap(t, tc+0.4+0.55*k+0.3, 0.3) for k in range(3)]; fl = sum(fill)/3
    card(c, 280, my-110, 800, my+110, a0, hi=0.4+0.6*fl, fw=0)
    ma = eo(ap(t, tm-0.1, 0.35)); c.tx(540, my+8, 'HAIKU', 'sg7', 72, g(lerp(GRA, WH, max(ma, 0.2)+0.0), 1), 'mm')
    if ta-0.1 < t: c.tx(540, my-62, 'ANTHROPIC', 'dm5', 28, g(SIL, eo(ap(t, ta, 0.3))), 'mm', track=5)
    c.rect(340, my+74, 740, my+84, fill=g(CH), line=g(GRA), r=5, w=2)
    if fl > 0: c.rect(340, my+74, 340+400*fl, my+84, fill=g(WH), r=5)
    # business-info cards rise into the model block
    xs = [270, 540, 810]
    for k in range(3):
        t0 = tc+0.4+0.55*k; p = ap(t, t0, 0.45); show = eo(ap(t, ti-0.4, 0.3)) if k == 0 else 1
        y = lerp(1230, my+20, eio(p)); a = 1-ap(p, 0.75, 0.25)
        ca = max(0.6, eo(ap(t, 0.05+0.1*k, 0.3)))
        if a > 0.02: 
            sc_ = lerp(1, 0.55, ap(p, 0.4, 0.6)); x = lerp(xs[k], 540, ap(p, 0.3, 0.7))
            docs(c, x, y, 220*sc_, 160*sc_, ca*a, hi=0.7*p)
    if ti-0.1 < t < 99 and fl < 1:
        c.tx(540, 1400-12, 'BUSINESS INFO', 'dm5', 28, g(SIL, eo(ap(t, ti, 0.3))*(1-ap(fl, 0.7, 0.3))), 'mm', track=5)
    if tcl-0.1 < t:
        pa = eo(ap(t, tcl, 0.3)); person(c, 160, 1070, 66, g(SIL, pa)); c.tx(160, 1130, 'CLIENT', 'dm5', 28, g(SIL, pa), 'mm', track=4)
        dashln(c, (230, 1090), (360, 1170), g(GRA, pa), 2)
    if fl >= 1: sparkle_ring(c, 540, my, 300, 360, ap(t, tc+2.25, 0.5), SIL, 3) if False else None

# ------------------------------------------------------------------ H  04 answers from data, not guesses
def H(c, t):
    tq = A_('H', 'q'); td = A_('H', 'data'); tg = A_('H', 'guess'); tx = A_('H', 'x')
    head(c, t, [(0, td-0.05, '04 · ACCURACY', 'Answering customer questions'), (td, 99, '04 · ACCURACY', 'From real data, not guesses')])
    xl, xr = 300, 780
    qa = max(0.55, eo(ap(t, tq-0.2, 0.35)))
    bub(c, 540, 650, 300, 84, 'in', qa)
    # two lanes (skeleton visible from the start)
    la = max(0.45, eo(ap(t, 0.1, 0.4)))
    c.ln([(540, 700), (540, 760)], g(GRA, la), 2); c.ln([(xl, 760), (xr, 760)], g(GRA, la), 2)
    c.ln([(xl, 760), (xl, 840)], g(GRA, la), 2); c.ln([(xr, 760), (xr, 840)], g(GRA, la), 2)
    dl = ap(t, td, 0.4)
    cols = [g(lerp(GRA, WH, dl), 1)]*3
    cyl(c, xl, 960, 170, 190, [g(lerp(GRA, WH, dl))]*3)
    c.tx(xl, 1100, 'DATA', 'dm5', 30, g(lerp(GRA, WH, dl)), 'mm', track=4)
    qp = ap(t, tq, 0.5)
    if 0 < qp < 1: x, y = pt((540, 650), (xl, 870), eio(qp)); bub(c, x, y, 150, 50, 'in')
    pa = ap(t, td+0.35, 0.5)
    if pa > 0:
        x, y = pt((xl, 1050), (xl, 1250), eio(pa)) if False else (xl, lerp(1170, 1255, eo(pa)))
        bub(c, xl, 1255, 260, 84, 'out', eo(pa)); check(c, xl-150+0, 1255, 0, 0) if False else None
        ck = eo(ap(t, td+0.7, 0.3))
        if ck > 0: check(c, xl, 1350, 44, g(WH, ck), 7)
    # guess lane: dashed wobble, "?", crossed out
    gl = max(0.0, ap(t, tg, 0.4)); gx = ap(t, tx, 0.25)
    if gl > 0:
        pts = [(xr+math.sin(k*1.3+t*2)*26*gl, 840+k*40) for k in range(6)]
        c.ln(pts, g(GRA, gl), 3)
        c.tx(xr, 1000, '?', 'sg7', 150, g(lerp(GRA, 0.35*GRA, 0), gl), 'mm')
        c.tx(xr, 1100, 'GUESS', 'dm5', 30, g(GRA, gl), 'mm', track=4)
    if gx > 0:
        s = 110*eo(gx); c.ln([(xr-s/2, 1255-s/2), (xr+s/2, 1255+s/2)], g(SIL), 8); c.ln([(xr-s/2, 1255+s/2), (xr+s/2, 1255-s/2)], g(SIL), 8)

# ------------------------------------------------------------------ I  05 Shopify API: store data, tools, permissions
def I(c, t):
    ta = A_('I', 'api'); tt = A_('I', 'tools'); tpm = A_('I', 'perm'); tk = A_('I', 'tasks'); b1 = A_('I', 'b1'); b2 = A_('I', 'b2')
    head(c, t, [(0, 2.5, '05 · SHOPIFY', 'Handling the store data'), (2.5, tt-0.05, '05 · SHOPIFY', 'Connected to the Shopify API'), (tt, 99, '05 · SHOPIFY', 'Tools and permissions to run tasks')])
    ya, yb, yc = 650, 830, 1300
    a0 = max(0.55, eo(ap(t, 0.05, 0.3)))
    node_ai(c, 540, ya, 62, a=a0, hi=0.8, sz=40, t=t)
    # store data cylinder
    lit = ap(t, b2+0.4, 0.3)
    cyl(c, 540, yc, 190, 170, [g(lerp(GRA, WH, lit), a0)]*3)
    c.tx(540, yc+112, 'STORE DATA', 'dm5', 28, g(lerp(GRA, SIL, lit), a0), 'mm', track=4)
    # before the API: dashed gap with a "?"
    gone = ap(t, ta, 0.3)
    if gone < 1:
        dashln(c, (540, ya+90), (540, yc-100), g(GRA, 0.9*(1-gone)), 2)
        qa = (0.5+0.5*math.sin(t*3))*(1-gone)
        c.tx(540, 960, '?', 'sg7', 96, g(SIL, 0.35+0.45*qa), 'mm')
    pp = eo(ap(t, ta, 0.4))
    if pp > 0:
        y = lerp(yb-120, yb, pp)
        card(c, 340, y-60, 740, y+60, pp, hi=0.6+0.4*ap(t, b1+0.25, 0.3))
        cart(c, 410, y, 56, g(lerp(SIL, WH, ap(t, b1+0.25, 0.3)), pp), 4)
        c.tx(580, y, 'SHOPIFY API', 'dm5', 28, g(lerp(GRA, WH, 0.6+0.4*ap(t, b1+0.25, 0.3)), pp), 'mm', track=2)
        lk = ap(t, ta+0.2, 0.4)
        c.ln([(540, ya+64), (540, lerp(ya+64, yb-60, lk))], g(GRA), 2)
        c.ln([(540, yb+60), (540, lerp(yb+60, yc-92, lk))], g(GRA), 2)
    bolt(c, (540, ya+64), (540, yb-60), t, (t-b1)/0.45, 1.0, amp=14)
    bolt(c, (540, yb+60), (540, yc-92), t, (t-b2)/0.45, 1.0, amp=16)
    # tools + permissions chips
    for (t0, cx_, lab, kind) in ((tt, 280, 'TOOLS', 'gear'), (tpm, 800, 'PERMISSIONS', 'lock')):
        p = eo(ap(t, t0, 0.4))
        if p > 0:
            y = 1050
            c.rect(cx_-120, y-72, cx_+120, y+72, fill=g(CH, p), line=g(SIL, p), r=16, w=2)
            if kind == 'gear': gear(c, cx_, y-20, 28, g(SIL, p))
            else: lock(c, cx_, y-20, 66, g(SIL, p), 4)
            c.tx(cx_, y+44, lab, 'dm5', 28, g(WH, p), 'mm', track=1.5)
            dashln(c, (cx_, y-72), (540+(-100 if cx_ < 540 else 100), yb+44), g(GRA, p), 2, d=8, gp=8)
    # tasks list with ticks
    if tk-0.1 < t:
        pa = eo(ap(t, tk-0.1, 0.3)); c.tx(740, 1210, 'TASKS', 'dm5', 28, g(SIL, pa), 'lm', track=4)
        for k in range(3):
            ck = eo(ap(t, tk+0.4*k, 0.25))
            if ck > 0:
                check(c, 765, 1262+k*52, 30, g(WH, ck), 5); c.ln([(805, 1262+k*52), (940-(k==2)*50, 1262+k*52)], g(GRA, ck), 4)

# ------------------------------------------------------------------ J  06 chat saved on the server, context restored
def J(c, t):
    ts = A_('J', 'save'); tsv = A_('J', 'server'); tr = A_('J', 'restore'); tc = A_('J', 'ctx'); tre = A_('J', 'ret'); trp = A_('J', 'reply')
    head(c, t, [(0, tr-0.1, '06 · SERVER', 'Saving the chat on the server'), (tr, 99, '06 · SERVER', 'Context restored when they return')])
    ag = (230, 700); cu = (850, 700); sv = (540, 1130)
    a0 = max(0.55, eo(ap(t, 0.05, 0.3)))
    node_ai(c, ag[0], ag[1], 64, a=a0, hi=0.7+0.3*ap(t, tc+0.5, 0.3), sz=42, t=t)
    cp = max(0.5, eo(ap(t, 0.0, 0.2)))
    person(c, cu[0], cu[1], 90, g(WH, cp))
    leds = [ap(t, ts+0.35*k+0.35, 0.2) for k in range(3)]
    ledfade = 1.0
    server(c, sv[0], sv[1]-10, 360, 84, a0, hi=0.4+0.6*ap(t, tsv, 0.3), leds=leds)
    c.tx(540, 1380, 'SERVER', 'dm5', 30, g(SIL, a0), 'mm', track=5)
    # phase 1: chat bubbles go into the server
    for k in range(3):
        t0 = ts+0.35*k-0.25; p = ap(t, t0, 0.55)
        if 0 < p < 1:
            src = (ag[0]+60 if k != 1 else cu[0]-60, ag[1]+90) if k != 1 else (cu[0]-40, cu[1]+90)
            x, y = pt(src, (540, sv[1]-150), eio(p)); bub(c, x, y, 150, 50, 'out' if k == 1 else 'in', 1-0.7*ap(p, 0.8, 0.2))
    # phase 2: context flows back to the agent
    for k in range(3):
        t0 = tc+0.25*k; p = ap(t, t0, 0.55)
        if 0 < p < 1:
            x, y = pt((520, sv[1]-170), (ag[0]+60, ag[1]+80), eio(p)); bub(c, x, y, 120, 42, 'out', 1-0.5*ap(p, 0.8, 0.2))
    if t > tc: c.tx(ag[0], ag[1]+175, 'CONTEXT', 'dm5', 28, g(SIL, eo(ap(t, tc+0.3, 0.3))), 'mm', track=4)
    # phase 3: the customer returns with a new message, the agent answers with context
    rp = ap(t, tre, 0.5)
    if 0 < rp < 1: x, y = pt((cu[0]-60, cu[1]+10), (ag[0]+80, ag[1]+10), eio(rp)); bub(c, x, y, 130, 46, 'in')
    rp2 = ap(t, trp-0.1, 0.45)
    if 0 < rp2 < 1: x, y = pt((ag[0]+80, ag[1]-24), (cu[0]-60, cu[1]-24), eio(rp2)); bub(c, x, y, 130, 46, 'out')
    if t > trp: sparkle_ring(c, ag[0], ag[1], 90, 150, ap(t, trp, 0.5), SIL, 3)

SCENE_FN = dict(A=A, B=B, C=C, D=D, E=E, F=F, G=G, H=H, I=I, J=J)
