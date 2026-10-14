"""12 s AXIOM motion clip: imagined part 1, block-stack parts 2 and 3."""
import math, random, subprocess, sys, os
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFont
import brand as B
import timeline as T

W, H, S = 1080, 1920, 2
FPS = T.FPS
NFR = int(T.DUR * FPS)

# ---------- helpers ----------
_fonts = {}
def font(key, size):
    k = (key, size)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(B.FONT[key], int(size * S))
    return _fonts[k]

def P(v): return int(round(v * S))
def clamp(x): return max(0.0, min(1.0, x))
def prog(t, t0, dur): return clamp((t - t0) / dur)
def ease_out(u): return 1 - (1 - u) ** 3
def ease_io(u): return 4 * u ** 3 if u < .5 else 1 - (-2 * u + 2) ** 3 / 2
def lerp(a, b, u): return a + (b - a) * u

def line(d, pts, c, w):
    d.line([(P(x), P(y)) for x, y in pts], fill=c, width=max(1, P(w)), joint="curve")
def circ(d, cx, cy, r, fill=None, outline=None, w=2):
    d.ellipse([P(cx - r), P(cy - r), P(cx + r), P(cy + r)], fill=fill, outline=outline, width=P(w))
def rrect(d, x0, y0, x1, y1, r, fill=None, outline=None, w=2):
    d.rounded_rectangle([P(x0), P(y0), P(x1), P(y1)], radius=P(r), fill=fill, outline=outline, width=P(w))
def arc(d, x0, y0, x1, y1, a0, a1, c, w):
    d.arc([P(x0), P(y0), P(x1), P(y1)], a0, a1, fill=c, width=max(1, P(w)))

def text(d, x, y, s, fk, size, c, anchor="ls", track=0):
    f = font(fk, size)
    if not track:
        d.text((P(x), P(y)), s, font=f, fill=c, anchor=anchor); return
    widths = [d.textlength(ch, font=f) for ch in s]
    total = sum(widths) + P(track) * (len(s) - 1)
    px = P(x) - (total / 2 if anchor == "ms" else 0)
    for ch, wd in zip(s, widths):
        d.text((px, P(y)), ch, font=f, fill=c, anchor="ls")
        px += wd + P(track)

_T = [0.0]
GRID = 60

K = 0.85                      # content scale about the Reels safe-zone centre
CX0, CY0 = 540, 845

def new():
    img = Image.new("RGB", (W * S, H * S), B.BLACK)
    return img, ImageDraw.Draw(img)

def finish(content):
    from PIL import ImageChops
    cw, ch = int(W * S * K), int(H * S * K)
    small = content.resize((cw, ch), Image.LANCZOS)
    canvas = Image.new("RGB", (W * S, H * S), B.BLACK)
    canvas.paste(small, (int(round(CX0 * S * (1 - K))), int(round(CY0 * S * (1 - K)))))
    return ImageChops.lighter(background(), canvas)

def background():
    img = Image.new("RGB", (W * S, H * S), B.BLACK)
    d = ImageDraw.Draw(img)
    # background texture: precise dot grid drifting slowly upward, with a few "+" marks
    off = (_T[0] * 18) % (GRID * 4)
    k0 = int(off // GRID)
    oy = off - k0 * GRID
    for gy in range(-1, H // GRID + 2):
        y = gy * GRID - oy
        row = gy + k0
        for gx in range(0, W // GRID + 1):
            x = gx * GRID
            if row % 4 == 0 and gx % 4 == 0:
                line(d, [(x - 7, y), (x + 7, y)], B.GRAPHITE, 1.5)
                line(d, [(x, y - 7), (x, y + 7)], B.GRAPHITE, 1.5)
            else:
                circ(d, x, y, 2.2, fill=B.CHARCOAL)
    return img

# ---------- icons (shapes only) ----------
def icon(d, kind, cx, cy, c):
    if kind == "trigger":
        circ(d, cx, cy, 34, outline=c, w=4)
        d.polygon([(P(cx - 9), P(cy - 15)), (P(cx - 9), P(cy + 15)), (P(cx + 16), P(cy))], fill=c)
    elif kind == "gear":
        circ(d, cx, cy, 17, outline=c, w=4)
        for k in range(8):
            a = math.radians(k * 45)
            line(d, [(cx + 25 * math.cos(a), cy + 25 * math.sin(a)),
                     (cx + 36 * math.cos(a), cy + 36 * math.sin(a))], c, 6)
    elif kind == "list":
        for dy, ln in ((-20, 64), (0, 50), (20, 36)):
            line(d, [(cx - 32, cy + dy), (cx - 32 + ln, cy + dy)], c, 5)
    elif kind == "check":
        line(d, [(cx - 28, cy + 2), (cx - 9, cy + 20), (cx + 28, cy - 20)], c, 7)
    elif kind == "bag":
        # shopping cart
        line(d, [(cx - 36, cy - 28), (cx - 24, cy - 28), (cx - 14, cy + 12), (cx + 26, cy + 12)], c, 4)
        line(d, [(cx - 21, cy - 16), (cx + 34, cy - 16), (cx + 28, cy + 4), (cx - 15, cy + 4)], c, 4)
        circ(d, cx - 8, cy + 28, 5, fill=c)
        circ(d, cx + 20, cy + 28, 5, fill=c)
    elif kind == "db":
        arc(d, cx - 30, cy - 36, cx + 30, cy - 16, 0, 360, c, 4)
        arc(d, cx - 30, cy - 16, cx + 30, cy + 4, 0, 180, c, 4)
        arc(d, cx - 30, cy + 4, cx + 30, cy + 24, 0, 180, c, 4)
        line(d, [(cx - 30, cy - 26), (cx - 30, cy + 14)], c, 4)
        line(d, [(cx + 30, cy - 26), (cx + 30, cy + 14)], c, 4)
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

# ---------- part 1 (imagined): a repeated task becomes automatic ----------
def scene1(t):
    img, d = new()
    cx, cy, R = 540, 720, 250
    nodes = [(cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    land = [1.65, .85, 1.25]  # arrival time at A, B, C (A also at 1.65)
    appear = .35 + .65 * ease_out(prog(t, 0.0, .35))
    for k, (nx, ny) in enumerate(nodes):
        fa = ease_out(prog(t, T.NODE_FILL[k], .15))
        flash = max(0.0, 1 - (t - land[k]) / .25) if t >= land[k] and t < T.NODE_FILL[k] else 0.0
        oc = B.mix(B.GRAPHITE, B.SILVER, flash)
        circ(d, nx, ny, 34 + 3 * fa, fill=B.mix(B.BLACK, B.WHITE, fa), outline=B.dim(oc, appear), w=3)
    # ring draws clockwise from the top node
    if t > T.RING[0]:
        p = ease_io(prog(t, *T.RING))
        bb = (P(cx - R), P(cy - R), P(cx + R), P(cy + R))
        if p >= .999:
            d.ellipse(bb, outline=B.SILVER, width=P(2))
        else:
            d.arc(bb, -90, -90 + 360 * p, fill=B.SILVER, width=P(2))
    # hopper
    pos = nodes[0]
    for a, b, i, j in T.HOPS:
        if t >= b:
            pos = nodes[j]
        elif t > a:
            u = ease_io(prog(t, a, b - a))
            pos = (lerp(nodes[i][0], nodes[j][0], u), lerp(nodes[i][1], nodes[j][1], u)); break
        else:
            break
    r = 22 - 8 * ease_out(prog(t, 1.7, .3))
    solid = ease_out(prog(t, 1.7, .15))
    ha = ease_out(prog(t, .2, .2))
    def orbit_pos(tt):
        tau = tt - T.ORBIT_START
        a_ = 13.09
        ph = .5 * a_ * tau ** 2 if tau < 1.2 else .5 * a_ * 1.44 + a_ * 1.2 * (tau - 1.2)
        th = math.radians(-90) + ph
        return cx + R * math.cos(th), cy + R * math.sin(th)
    if t >= T.ORBIT_START:
        for k in range(6, 0, -1):
            tx, ty = orbit_pos(max(T.ORBIT_START, t - k * .02))
            circ(d, tx, ty, 14 * (1 - k * .1), fill=B.dim(B.WHITE, 1 - k / 7.0))
        pos = orbit_pos(t)
    circ(d, pos[0], pos[1], r, fill=B.mix(B.BLACK, B.WHITE, solid) if solid > 0 else None,
         outline=B.dim(B.SILVER, ha) if solid < 1 else None, w=3)
    # words from the script
    a1 = ease_out(prog(t, T.TITLE_T, .4))
    if a1 > 0:
        text(d, 540, 1180 + 24 * (1 - a1), "Automation", "sg700", 120, B.dim(B.WHITE, a1), "ms")
    a2 = ease_out(prog(t, T.SUB_T, .4))
    if a2 > 0:
        text(d, 540, 1252, "TRIGGER · PROCESS · ACTION", "dm500", 26, B.dim(B.SILVER, a2), "ms", track=6)
    return finish(img)

# ---------- parts 2 and 3: the block stack ----------
BX0, BX1, BH, GAP, TOP = 160, 920, 180, 150, 260
def by(i): return TOP + i * (BH + GAP)

BLOCKS = {
    2: [("Trigger", None, "trigger"), ("Process", None, "gear"), ("Process", None, "list"), ("Action", None, "check")],
    3: [("TRIGGER", "New Order", "bag"), ("PROCESS", "Order Data", "db"),
        ("PROCESS", "Google Sheets", "grid"), ("ACTION", "Notification", "bell")],
}

def bolt(d, y_a, y_b, lo, hi, seed):
    rng = random.Random(seed)
    n = max(3, int(14 * (hi - lo)) + 2)
    for amp, w, col in ((26, 6, B.WHITE), (42, 3, B.SILVER)):
        pts = []
        for k in range(n):
            f = lo + (hi - lo) * k / (n - 1)
            x = 540 + (rng.uniform(-1, 1) * amp * math.sin(math.pi * f) if 0 < k < n - 1 or (0 < f < 1) else 0)
            pts.append((x, lerp(y_a, y_b, f)))
        line(d, pts, col, w)

def stack(t, mode):
    img, d = new()
    cfg = T.STACK[mode]
    act = T.activations(mode)
    # wires
    for j in range(3):
        wp = ease_out(prog(t, T.WIRE_IN(j), .3)) if mode == 2 else 1.0
        if wp <= 0: continue
        e = prog(t, act[j + 1], .2)
        ya, yb = by(j) + BH, by(j + 1)
        line(d, [(540, ya), (540, lerp(ya, yb, wp))], B.mix(B.GRAPHITE, B.SILVER, e), 3)
    # blocks
    for i, (role, name, ic) in enumerate(BLOCKS[mode]):
        if mode == 2:
            e = ease_out(prog(t, T.BLOCK_IN(i), .45))
            if e <= 0: continue
            sl = 50 * (1 - e)
        else:
            e, sl = 1.0, 0.0
        lvl = ease_out(prog(t, act[i], .15))
        f3 = ease_out(prog(t, act[3], .25)) if i == 3 else 0.0
        y0, y1 = by(i) + sl, by(i) + BH + sl
        mid = (y0 + y1) / 2
        fill = B.dim(B.mix(B.CHARCOAL, B.WHITE, f3), e)
        border = B.dim(B.mix(B.GRAPHITE, B.WHITE, lvl), e)
        rrect(d, BX0, y0, BX1, y1, 28, fill=fill, outline=border, w=2)
        main = B.dim(B.mix(B.mix(B.SILVER, B.WHITE, lvl), B.BLACK, f3), e)
        icon(d, ic, BX0 + 100, mid, main)
        if mode == 2:
            text(d, BX0 + 190, mid + 22, role, "sg600", 64, main)
        else:
            sub = B.dim(B.mix(B.SILVER, B.GRAPHITE, f3), e)
            text(d, BX0 + 190, mid - 16, role, "dm500", 28, sub, track=5)
            text(d, BX0 + 190, mid + 42, name, "sg600", 58, main)
    # electricity
    for pi, key in enumerate(("first", "second")):
        for j, (s, dur) in enumerate(cfg[key]):
            u = (t - s) / dur
            ya, yb = by(j) + BH, by(j + 1)
            if 0 < u < 1.6:
                lo, hi = max(0.0, u - .6), min(1.0, u)
                if hi - lo > 0.02:
                    bolt(d, ya, yb, lo, hi, mode * 100000 + pi * 10000 + j * 1000 + int(t * 15))
                if u < 1:
                    circ(d, 540, lerp(ya, yb, u), 7, fill=B.WHITE)
            tau = t - (s + dur)
            if 0 <= tau < .2:
                g = ease_out(tau / .2)
                for k in range(6):
                    a = math.radians(-170 + k * 32)
                    r0, r1 = 8 + 4 * g, 14 + 22 * g
                    line(d, [(540 + r0 * math.cos(a), yb + r0 * math.sin(a)),
                             (540 + r1 * math.cos(a), yb + r1 * math.sin(a))], B.dim(B.SILVER, 1 - tau / .2), 3)
    # action ring pulses
    for rt, _ in cfg["rings"]:
        tau = t - rt
        if 0 <= tau < .5:
            g = ease_out(tau / .5) * 26
            rrect(d, BX0 - g, by(3) - g, BX1 + g, by(3) + BH + g, 28 + g, outline=B.dim(B.WHITE, 1 - tau / .5), w=2)
    return finish(img)

def frame_img(i):
    t = i / FPS
    _T[0] = t
    x0, xd = T.XFADE
    if t < T.CUT_1_2:
        im = scene1(t)
    elif t < x0:
        im = stack(t, 2)
    elif t <= x0 + xd:
        im = Image.blend(stack(t, 2), stack(t, 3), ease_io(prog(t, x0, xd)))
    else:
        im = stack(t, 3)
    return im.reduce(S)

def frame_bytes(i):
    return frame_img(i).tobytes()

if __name__ == "__main__":
    out, wav = sys.argv[1], sys.argv[2]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", wav, "-map", "0:v", "-map", "1:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "-t", str(T.DUR), out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(2) as pool:
        for b in pool.imap(frame_bytes, range(NFR), chunksize=2):
            p.stdin.write(b)
    p.stdin.close(); p.wait()
    print("done", out)
