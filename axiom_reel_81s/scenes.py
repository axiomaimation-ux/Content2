import math, random
from lib import *
import timeline as T

def sA(c, t):
    head(c, t, [(0,3,'PROBLEM 01','Confirmation messages, sent by hand'),(3,6,'PROBLEM 01','A waste of time and effort')])
    dim = 1-0.45*ap(t, 3.0, 0.4)
    active = next((i for i in range(5) if not (i < 4 and t >= T.A_SENT[i])), 4)
    for i in range(5):
        a, dy = appear(t, T.A_ROW[i], 0.35, 0.5 if i == 0 else 0)
        if a <= 0: continue
        a *= dim; y = 600+i*105+dy
        card(c, 90, y, 990, y+84, a)
        person(c, 150, y+42, 50, g(SIL, a)); c.rect(205, y+35, 385, y+49, fill=g(GRA, a), r=7)
        x0 = 560
        if i < 4 and t >= T.A_SENT[i]:
            bubble(c, x0, y+10, 400, 64, 'Confirmation', 'out', a); check(c, x0+360, y+42, 26, 0, 4)
        else:
            c.rect(x0, y+10, x0+400, y+74, fill=g(CH, a), line=g(GRA, a), r=32, w=2)
            if i == active:
                for k in range(3):
                    ph = (t*3-k*0.33) % 1; c.ell(x0+60+k*30, y+42, 5+3*max(0, math.sin(ph*math.pi)), fill=g(SIL, a))
            else: c.tx(x0+34, y+42, 'Confirmation', 'dm5', 30, g(GRA, a))
    a, dy = appear(t, T.A_CLK)
    if a > 0: clock(c, 540, 1290+dy, 110, (t-3)*720, g(WH, a), 4)

def sB(c, t):
    head(c, t, [(0,3,'AUTOMATION + AI','Confirmations sent instantly, automatically'),(3,6,'AUTOMATION + AI','Answers customer questions for you')])
    d = 1-ap(t, 3.0, 0.3)
    if d > 0:
        ys = [700, 960, 1220]; labs = ['ORDER', 'AI', 'CONFIRMATION']
        hi = [0.6, eio(ap(t, T.B_H[0], .25)), 0]; fw = [0, 0, eio(ap(t, T.B_H[1], .25))]
        for k in range(3):
            a, dy = appear(t, 0.25*k, 0.35, 0.5); block(c, 540, ys[k]+dy, 560, 120, labs[k], hi[k], fw[k], a*d)
        for k in range(2): bolt(c, (540, ys[k]+60), (540, ys[k+1]-60), t, (t-T.B_Z[k])/0.5, d)
        if fw[2] > 0.5: check(c, 540+235, 1220, 34, 0, 6)
    for k in range(4):
        a, dy = appear(t, T.B_CHAT[k], 0.3)
        if a <= 0 or t < 3: continue
        yb = [700, 830, 960, 1090][k]
        if k % 2 == 0: bubble(c, 90-(1-a)*40, yb, 520, 76, 'Customer question', 'in', a)
        else:
            bubble(c, 470+(1-a)*40, yb, 520, 76, 'Instant answer', 'out', a); check(c, 470+480, yb+38, 30, 0, 5)

def sC(c, t):
    head(c, t, [(0,3,'AUTOMATION + AI','No personal reply to every customer')])
    xs = [170, 355, 540, 725, 910]; n_ans = sum(1 for k in range(5) if t >= T.C_T[k])
    for k in range(5):
        a, dy = appear(t, 0.08*k, 0.35, 0.5)
        pc = lerp(GRA, WH, 1-ap(t, T.C_T[k], 0.4)) if t >= T.C_T[k] else GRA
        c.ln([(xs[k], 780), (540, 972)], g(pc, a), 2)
        person(c, xs[k], 720+dy, 90, g(SIL, a))
        if t >= T.C_T[k]+0.15: check(c, xs[k], 625, 36, g(WH, ap(t, T.C_T[k]+0.15, 0.2)), 5)
        sparkle_ring(c, 540, 1050, 78, 135, (t-T.C_T[k])/0.5)
    c.ell(540, 1050, 78, fill=g(CH), line=g(WH), w=3); gear(c, 540, 1050, 40, g(WH))
    c.tx(540, 1290, str(5-n_ans), 'sg7', 110, g(WH), 'mm')
    c.tx(540, 1385, 'PERSONAL REPLIES', 'dm5', 30, g(SIL), 'mm', track=4)

def sheet(c, x0, y0, cols, rows, cw, ch, filled, a=1, header=False):
    for r in range(rows):
        for k in range(cols):
            idx = r*cols+k; xx, yy = x0+k*cw, y0+r*ch
            c.rect(xx, yy, xx+cw, yy+ch, fill=g(CH, a) if (header and r == 0) else None, line=g(GRA, a), w=2)
            if idx in filled and filled[idx] > 0:
                f = filled[idx]; c.rect(xx+cw*.2, yy+ch/2-6, xx+cw*(.2+.6*eo(f)), yy+ch/2+6, fill=g(SIL, a), r=6)

def sD(c, t):
    head(c, t, [(0,3,'PROBLEM 02','Customer data, logged by hand'),(3,6,'PROBLEM 02','Google Sheets or databases, handled manually'),(6,9,'PROBLEM 02','Why still work by hand?')])
    p1 = 1-ap(t, 3.0, 0.3)
    if p1 > 0:
        for k, (x0, lab) in enumerate(((70, 'WHATSAPP'), (560, 'WEBSITE'))):
            a, dy = appear(t, 0.2*k, 0.35, 0.5); card(c, x0, 600+dy, x0+450, 700+dy, a*p1)
            (chat_icon if k == 0 else browser_icon)(c, x0+60, 650+dy, 40, g(SIL, a*p1))
            c.tx(x0+110, 650+dy, lab, 'dm5', 30, g(WH, a*p1), 'lm', track=3)
        fl = {k+4: ap(t, T.D_FILL1[k], 0.25) for k in range(8)}
        sheet(c, 140, 790, 4, 5, 200, 68, fl, p1, header=True)
        nxt = next((k for k in range(8) if t < T.D_FILL1[k]), None)
        if nxt is not None and int(t*3) % 2 == 0:
            idx = nxt+4; xx, yy = 140+(idx % 4)*200, 790+(idx//4)*68
            c.rect(xx+34, yy+16, xx+38, yy+52, fill=g(WH, p1))
    p2 = ap(t, 3.0, 0.3)*(1-ap(t, 6.0, 0.3))
    if p2 > 0:
        card(c, 100, 700, 460, 1060, p2); card(c, 620, 700, 980, 1060, p2)
        fl = {k: ap(t, T.D_FILL2[k], 0.25) for k in range(9)}
        sheet(c, 136, 740, 3, 3, 96, 96, fl, p2)
        bands = [lerp(GRA, WH, ap(t, tt, 0.3)) for tt in (3.7, 4.6, 5.5)]
        cyl(c, 800, 880, 200, 250, [g(b, p2) for b in bands])
        c.tx(280, 1110, 'GOOGLE SHEETS', 'dm5', 30, g(SIL, p2), 'mm', track=4); c.tx(800, 1110, 'DATABASES', 'dm5', 30, g(SIL, p2), 'mm', track=4)
    p3 = ap(t, 6.0, 0.3)
    if p3 > 0:
        fl = eio(ap(t, T.D_FLIP, 0.35)); qa = p3*(1-ap(t, T.D_FLIP, 0.3))
        if qa > 0: c.tx(540, 790, '?', 'sg7', 220, g(SIL, qa), 'mm')
        c.rect(310, 950, 770, 1150, fill=g(lerp(CH, WH, fl), p3), line=g(lerp(GRA, WH, fl), p3), r=100, w=3)
        kx = lerp(410, 670, fl); c.ell(kx, 1050, 76, fill=g(lerp(WH, BK, fl), p3))
        c.tx(410, 1230, 'MANUAL', 'dm5', 30, g(lerp(WH, GRA, fl), p3), 'mm', track=4); c.tx(670, 1230, 'AUTO', 'dm5', 30, g(lerp(GRA, WH, fl), p3), 'mm', track=4)

def sE(c, t):
    head(c, t, [(0,3,'AUTOMATION','Fully automatic, no human touch'),(3,6,'THE EASY PART','The easy side, before the real disaster')])
    d = 1-ap(t, 3.0, 0.3)
    if d > 0:
        for k, (cx, lab) in enumerate(((295, 'WHATSAPP'), (785, 'WEBSITE'))):
            a, dy = appear(t, 0, 0.35, 0.5); block(c, cx, 670, 450, 100, lab, 0.8, 0, a*d)
            bolt(c, (cx, 720), (400 if k == 0 else 680, 1020), t, (t-T.E_Z[k])/0.5, d)
        hi = eio(ap(t, T.E_H[0], .3)); card(c, 190, 1020, 890, 1400, d, hi)
        fl = {r*3+k: ap(t, T.E_ROW[r]+0.08*k, 0.2) for r in range(4) for k in range(3)}
        sheet(c, 240, 1060, 3, 4, 200, 70, fl, d)
    p = ap(t, 3.0, 0.3)
    if p > 0:
        c.rect(90, 960, 990, 1016, line=g(GRA, p), r=28, w=3)
        fw = 900*0.22*eio(ap(t, T.E_BAR, 1.0))
        if fw > 56: c.rect(90, 960, 90+fw, 1016, fill=g(WH, p), r=28)
        for x in range(int(90+max(fw, 56))+14, 970, 28): c.ell(x, 988, 3, fill=g(GRA, p))
        a, dy = appear(t, T.E_EASY, 0.3)
        c.tx(90, 1090, 'EASY', 'dm5', 30, g(WH, a*p), 'lm', track=4)
        c.tx(990, 1090, 'THE REAL DISASTER', 'dm5', 30, g(SIL, p*ap(t, 4.0, .3)), 'rm', track=4)
        a, dy = appear(t, T.E_WARN, 0.3); col = g(SIL, a)
        c.ln([(800, 750+dy), (875, 880+dy), (725, 880+dy), (800, 750+dy)], col, 5)
        c.ln([(800, 790+dy), (800, 830+dy)], col, 6); c.ell(800, 856+dy, 4, fill=col)

def digits(c, x, y, s, sz, col, adv):
    for i, ch in enumerate(s): c.tx(x+i*adv, y, ch, 'sg7', sz, col, 'mm')

def sF(c, t):
    head(c, t, [(0,3,'THE REAL DISASTER','Dozens of customers a day, the same questions'),(3,6,'THE REAL DISASTER','Replies that come too late'),
                (6,9,'THE REAL DISASTER','Lost customers who would have bought'),(9,12,'THE IDEAL SCENARIO','An instant answer, any time, for every customer')])
    p1 = 1-ap(t, 3.0, 0.3)
    if p1 > 0:
        for i in range(24):
            a, dy = appear(t, T.F_Q[i], 0.25, 0.5 if i == 0 else 0)
            if a <= 0: continue
            x, y = 110+(i % 4)*220, 700+(i//4)*92+dy
            c.rect(x, y, x+200, y+70, fill=g(CH, a*p1), line=g(GRA, a*p1), r=35, w=2); c.tx(x+100, y+35, '?', 'sg7', 40, g(SIL, a*p1), 'mm')
    p2 = ap(t, 3.0, 0.3)*(1-ap(t, 6.0, 0.3))
    if p2 > 0:
        clock(c, 540, 950, 190, (t-3)*720, g(WH, p2), 5)
        e = int(max(0, t-3)*50); digits(c, 540-2*48-22, 1270, f"{e//60:02d}:{e%60:02d}", 84, g(SIL, p2), 48)
    p3 = ap(t, 6.0, 0.3)*(1-ap(t, 9.0, 0.3))
    if p3 > 0:
        for i in range(5):
            x = 170+i*185; pr = eo(ap(t, T.F_LEAVE[i], 0.6)); a = p3*(1-pr)
            person(c, x+150*pr, 960, 100, g(SIL, a)); gone = t >= T.F_LEAVE[i]
            cart(c, x, 790, 90, g(lerp(SIL, GRA, pr), p3), 4)
            if gone: cross(c, x, 790, 54, g(WH, p3*ap(t, T.F_LEAVE[i], 0.3)), 6)
    p4 = ap(t, 9.0, 0.3)
    if p4 > 0:
        c.ell(540, 1000, 232, line=g(GRA, p4), w=3)
        for i in range(24):
            ang = math.radians(i*15); lit = ap(t, T.F_TICK[i], 0.15)
            c.ln([(540+math.sin(ang)*242, 1000-math.cos(ang)*242), (540+math.sin(ang)*268, 1000-math.cos(ang)*268)], g(lerp(GRA, WH, lit), p4), lerp(3, 6, lit))
        ang = math.radians((t-9)*180); c.ell(540+math.sin(ang)*205, 1000-math.cos(ang)*205, 8, fill=g(WH, p4))
        c.tx(540, 975, 'ANYTIME', 'sg7', 60, g(WH, p4), 'mm'); c.tx(540, 1045, 'INSTANT ANSWER', 'dm5', 30, g(SIL, p4), 'mm', track=4)

def sG(c, t):
    head(c, t, [(0,3,'AI AGENT','Understands your products in detail'),(3,6,'AI AGENT','Answers every kind of question'),
                (6,9,'AI AGENT','Makes buying decisions easier'),(9,12,'AI + AUTOMATION','The most out of automation and AI')])
    p1 = 1-ap(t, 3.0, 0.3)
    if p1 > 0:
        cards = [(70, 730, 370, 850), (710, 730, 1010, 850), (390, 1200, 690, 1320)]
        ctr = [((220, 850), (480, 925)), ((860, 850), (600, 925)), ((540, 1200), (540, 1075))]
        for k, (x0, y0, x1, y1) in enumerate(cards):
            a, dy = appear(t, 0.2*k, 0.35, 0.5); card(c, x0, y0+dy, x1, y1+dy, a*p1, 0.4)
            c.rect(x0+24, y0+dy+30, x0+84, y0+dy+90, line=g(SIL, a*p1), r=8, w=3)
            c.rect(x0+104, y0+dy+38, x1-30, y0+dy+50, fill=g(GRA, a*p1), r=6); c.rect(x0+104, y0+dy+68, x1-90, y0+dy+80, fill=g(GRA, a*p1), r=6)
            c.ln([ctr[k][0], ctr[k][1]], g(GRA, a*p1), 2)
            bolt(c, ctr[k][0], ctr[k][1], t, (t-T.G_Z[k])/0.4, p1, amp=14)
        c.ell(540, 1000, 95, fill=g(CH, p1), line=g(WH, p1), w=3); gear(c, 540, 1000, 50, g(WH, p1))
        sparkle_ring(c, 540, 1000, 95, 175, (t-T.G_PULSE)/0.6, w=3)
    for k in range(6):
        a, dy = appear(t, T.G_CHAT[k], 0.3)
        if t < 3 or a <= 0 or t > 6.3: continue
        yb = 620+(k//2)*190+(k % 2)*95; f = 1-ap(t, 6.0, 0.3)
        if k % 2 == 0: bubble(c, 90-(1-a)*40, yb, 520, 76, 'Question', 'in', a*f)
        else: bubble(c, 470+(1-a)*40, yb, 520, 76, 'Answer', 'out', a*f); check(c, 950, yb+38, 30, 0, 5)
    p3 = ap(t, 6.0, 0.3)*(1-ap(t, 9.0, 0.3))
    if p3 > 0:
        hi1 = eio(ap(t, T.G_BH[0], .25)); fw = eio(ap(t, T.G_BH[1], .25))
        person(c, 170, 1000, 120, g(SIL, p3))
        card(c, 420, 920, 660, 1080, p3, hi1); cart(c, 540, 1000, 100, g(lerp(SIL, WH, hi1), p3), 5)
        block(c, 850, 1000, 240, 110, 'BUY', 0, fw, p3, 34)
        if fw > 0.5: check(c, 850+85, 1000, 30, 0, 5)
        bolt(c, (240, 1000), (420, 1000), t, (t-T.G_B[0])/0.5, p3, 14); bolt(c, (660, 1000), (730, 1000), t, (t-T.G_B[1])/0.5, p3, 10)
    p4 = ap(t, 9.0, 0.3)
    if p4 > 0:
        labs = ['TRIGGER', 'PROCESS', 'ACTION']; xs = [190, 540, 890-0]
        xs = [160, 540, 920]
        for k in range(3):
            hi = [0.7, eio(ap(t, T.G_CH[0], .25)), 0][k]; fw = [0, 0, eio(ap(t, T.G_CH[1], .25))][k]
            block(c, xs[k], 1000, 220, 130, labs[k], hi, fw, p4)
        bolt(c, (270, 1000), (430, 1000), t, (t-T.G_C[0])/0.5, p4, 18); bolt(c, (650, 1000), (810, 1000), t, (t-T.G_C[1])/0.5, p4, 18)
        sparkle_ring(c, 920, 1000, 110, 170, (t-11.0)/0.6)

def sH(c, t):
    head(c, t, [(0,3,'AUTOMATION','All of it, smoothly, with modern tools'),(3,6,'AUTOMATION + AI','Want to learn how AI can improve your work?')])
    cx, cy, R = 540, 1000, 270
    ang = (t*150) % 360
    for k in range(6):
        a, dy = appear(t, 0.07*k, 0.35, 0.5); th = math.radians(k*60)
        x, y = cx+math.sin(th)*R, cy-math.cos(th)*R
        pa = (ang-k*60) % 360; lit = max(0, 1-pa/200) if t >= T.H_N[k]-0.15 else 0
        c.ell(x, y, 38, fill=g(CH, a), line=g(lerp(GRA, WH, lit), a), w=3); c.ell(x, y, 10, fill=g(lerp(GRA, WH, lit), a))
    c.ell(cx, cy, R, line=g(CH+20), w=2)
    for j in range(24):
        aa = math.radians(ang-j*4); c.ell(cx+math.sin(aa)*R, cy-math.cos(aa)*R, 9*(1-j/30), fill=g(WH, 1-j/24))
    q = ap(t, 3.2, 0.5)
    if t < 3.1: gear(c, cx, cy, 60, g(WH, 0.8)) if False else c.ell(cx, cy, 14, fill=g(WH))
    else: c.tx(cx, cy, '?', 'sg7', 300*eo(q)+20, g(WH, q), 'mm')
    for r0 in T.H_Q: sparkle_ring(c, cx, cy, 60, 300, (t-r0)/1.0)

def sI(c, t):
    head(c, t, [(0,3,'GROWTH','Technology grows your business and your profits'),(3,6,'NEXT STEP','Take the next step and explore more'),
                (6,9,'MODERN TECH','Use modern technology in commerce and business'),(9,12,'KEEP UP',"Keep up with technology, so you don't lose more opportunities"),
                (12,15,'THE GOAL','Managing your business, made simple with technology'),(15,18,'KEEP LEARNING','Keep following to keep learning'),
                (18,21,'','Follow the account to learn the method in detail')])
    p = 1-ap(t, 3.0, 0.3)
    if p > 0:
        pts = []; c.ln([(90, 1350), (990, 1350)], g(SIL, p), 3)
        for i in range(5):
            h = [140, 260, 380, 500, 640][i]*eo(ap(t, T.I_BAR[i], 0.6)); x = 130+i*170
            if h > 4: c.rect(x, 1350-h, x+120, 1350, fill=g(WH if i == 4 else SIL, p), r=8)
            pts.append((x+60, 1350-h-30))
        if t > 1.6: c.ln(pts, g(WH, p*ap(t, 1.6, .5)), 4)
    p = ap(t, 3.0, 0.3)*(1-ap(t, 6.0, 0.3))
    if p > 0:
        c.ell(540, 1000, 190, line=g(GRA, p), w=4); c.arc(540, 1000, 190, -90, -90+360*eio(ap(t, T.I_ARC, 2.0)), g(WH, p), 8)
        c.poly([(500, 930), (500, 1070), (625, 1000)], g(WH, p))
        for r0 in T.I_RING: sparkle_ring(c, 540, 1000, 190, 260, (t-r0)/0.9)
    p = ap(t, 6.0, 0.3)*(1-ap(t, 9.0, 0.3))
    if p > 0:
        hi = eio(ap(t, T.I_BH, .3)); card(c, 130, 900, 400, 1100, p); cart(c, 265, 1000, 130, g(SIL, p), 5)
        card(c, 680, 900, 950, 1100, p, hi); gear(c, 815, 1000, 70, g(lerp(SIL, WH, hi), p))
        bolt(c, (400, 1000), (680, 1000), t, (t-T.I_B)/0.5, p, 18); sparkle_ring(c, 815, 1000, 140, 190, (t-T.I_BH)/0.6)
    p = ap(t, 9.0, 0.3)*(1-ap(t, 12.0, 0.3))
    if p > 0:
        pos = []
        for k in range(5):
            x0 = 120+k*170; ytop = 1250-k*140; c.rect(x0, ytop, x0+170, 1360, fill=g(CH, p), line=g(GRA, p), w=2)
            pos.append((x0+85, ytop-40))
            lit = t >= T.I_STEP[k]+0.25; c.ell(x0+85, ytop-40, 16, fill=g(WH, p) if lit else None, line=g(SIL, p), w=3)
        k = sum(1 for tt in T.I_STEP if t >= tt)
        if k > 0:
            k0 = k-1; pr = eo(ap(t, T.I_STEP[k0], 0.25)); a0 = pos[k0-1] if k0 > 0 else (60, 1300); a1 = pos[k0]
            x = lerp(a0[0], a1[0], pr); y = lerp(a0[1], a1[1], pr)-math.sin(pr*math.pi)*50-34
            c.ell(x, y, 12, fill=g(WH, p))
    p = ap(t, 12.0, 0.3)*(1-ap(t, 15.0, 0.3))
    if p > 0:
        rng = random.Random(5); noise = [(rng.random()-.5)*2 for _ in range(28)]; ph = [rng.random()*6.28 for _ in range(28)]
        s_ = eio(ap(t, T.I_LINE-0.4, 1.3)); pts = []
        for i in range(28):
            x = 90+900*i/27; amp = 250*(1-s_)*noise[i]+14*math.sin(t*4+ph[i])*(1-s_)
            pts.append((x, 1000+amp))
        c.ln(pts, g(WH, p), 5); c.ell(90, 1000, 9, fill=g(WH, p)); c.ell(990, 1000, 9, fill=g(WH, p))
        if t >= T.I_FIN: check(c, 540, 1130, 56, g(WH, p*ap(t, T.I_FIN, .3)), 7)
    p = ap(t, 15.0, 0.3)*(1-ap(t, 18.0, 0.3))
    if p > 0:
        c.ell(540, 1000, 220, line=g(GRA, p), w=3); a0 = (t-15)*200
        for j in range(30):
            aj = a0-j*6; c.arc(540, 1000, 220, aj-6, aj, g(WH, p*(1-j/30)), 9)
        c.ell(540, 1000, 12, fill=g(SIL, p))
    p = ap(t, 18.0, 0.3)
    if p > 0:
        for r0 in T.I_END: sparkle_ring(c, 540, 1050, 40, 260, (t-r0)/1.0)
        c.ell(540, 1050, 12, fill=g(WH, p))

SCENE_FN = dict(A=sA, B=sB, C=sC, D=sD, E=sE, F=sF, G=sG, H=sH, I=sI)
