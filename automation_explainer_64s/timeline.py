"""Single source of truth for timing: visuals, captions and sound all read this.
No voiceover exists yet: segment times come from the user's script timestamps;
word times inside a segment are ESTIMATED (character-weighted)."""
import math
import re

FPS = 30
DUR = 64.0

# real transitions (soft crossfades), centred on these times
XF = [13.0, 35.0, 51.0]
XFD = 0.25

# scene name, start, end (hard cuts between them except at XF)
SCENES = [
    ("title", 0.0, 2.0), ("repeat", 2.0, 7.0), ("ai", 7.0, 13.0),
    ("three", 13.0, 24.0), ("flow", 24.0, 35.0),
    ("site", 35.0, 43.0), ("toggle", 43.0, 46.0), ("chat", 46.0, 51.0),
    ("summary", 51.0, 61.0), ("follow", 61.0, 64.0),
]

# ---------- scene event times ----------
# 1 title
TI_RING = (0.05, 0.55); TI_TITLE = 0.55
# 2 repeat -> automatic
RP_ROWIN = 2.0
RP_TAPS = [2.55, 3.0, 3.45, 3.9]
RP_RESET = 4.35
RP_POWER = 4.65
RP_AUTO = [[4.8, 4.95, 5.1, 5.25], [5.95, 6.1, 6.25, 6.4]]
RP_RESET2 = 5.65
RP_LABEL = 4.9
# 3 AI replaces the human brain
AI_P1 = (8.2, 0.6); AI_CHECK1 = 8.8
AI_OUT = (9.8, 0.4); AI_RESET = 10.2
AI_CHIP = (10.1, 0.6)
AI_P2 = (10.95, 0.6); AI_CHECK2 = 11.55; AI_RING = 11.85
# 4 three things
TH_BLOCK = [13.0, 13.15, 13.3]
TH_WIRE = [13.5, 13.75]
TH_HI = [15.0, 18.0, 21.0]
# 5 flow (electricity)
FL_PRE = [24.5, 26.3]
FL_B1 = (28.7, 0.5)
FL_B2 = (31.7, 0.5)
FL_FILL = 32.25
FL_RINGS = [32.6, 33.5]
# 6 website
SI_ORDER = [36.1, 40.0]
SI_ORDER_RESET = 39.4
SI_BOLT = [(37.2, 0.6), (40.9, 0.6)]
SI_ROWS = [[37.9, 38.2, 38.5], [41.6, 41.9, 42.2]]
SI_ROWS_RESET = 39.6
SI_BELL = [38.0, 41.6]
SI_BELL_RESET = 39.6
# 7 toggle / chat
TG_FLIP = (43.7, 0.4); TG_LABEL = 44.05; TG_RING = 44.1
CH_DOTS = [(46.05, 46.5), (48.0, 48.4)]
CH_BUB = [46.5, 47.4, 48.4, 49.3]
CH_ORDER = 50.0
# 8 summary
SU_CYCLES = [51.3, 52.8, 53.9, 54.7, 55.3]
SU_A_FADE = (55.8, 0.5)
SU_CHART = (56.3, 1.4); SU_CHART_RING = 57.8
SU_B_FADE = (58.1, 0.4)
SU_HUMAN = 58.4; SU_HRING = (58.6, 0.6); SU_STAR = 59.3
# 9 follow
FO_PLUS = 61.0; FO_LABEL = 61.4; FO_FILL = 62.3; FO_RING = 62.35

# ---------- captions (script, timestamps from the user) ----------
SEGS = [
    (0, 2, "هو إزاي الأتمتة بيشتغل؟ أتمتة ببساطة"),
    (2, 7, "هو انك تأتمت عملية بتعملها بشكل متكرر بحيث تتنفذ تلقائياً بدل ما تعملها بنفسك كل مرة،"),
    (7, 13, "حتى لو عملية محتاجة فيها ذكاء أو عقل بشري، ممكن تدخل فيها الـ AI عشان تطلع نفس النتيجة البشرية."),
    (13, 18, "وده بيحصل بأنك تحدد تلات حاجات، أولهم التريجر: إيه اللي بيبدأ العملية دي؟"),
    (18, 21, "تاني حاجه البروسيس: الخطوات المفروض تتنفذ."),
    (21, 24, "وتالت حاجه الاكشن: النتيجة اللي عايزين نوصل لها."),
    (24, 29, "وده بيحصل بأنك تحدد تلات حاجات، أولهم التريجر: إيه اللي بيبدأ العملية دي؟"),
    (29, 32, "تاني حاجه البروسيس: الخطوات المفروض تتنفذ."),
    (32, 35, "وتالت حاجه الاكشن: النتيجة اللي عايزين نوصل لها."),
    (35, 43, "مثلاً لو عندك ويبسايت، اول ما العميل يعمل أوردر، السيستم بيسحب بالداتا بتاعة الأوردر ويسجلها في جوجل شيت ويبعتلك نوتفيكيشن،"),
    (43, 51, "وكل ده تلقائياً من غير ما تتدخل، وكمان الـ AI يبعت للعميل على الواتس عشان ياخد منه معلومات وياكد الأوردر."),
    (51, 60, "يعني باختصار احنا بنحدد للسيستم إمتا يبدأ، وإيه الخطوات اللي ينفذها، والنتيجة المطلوبة، عشان نسرع إنتاجية البِزنس ونخلي البشر يفضلوا الحاجات المهمة،"),
    (61, 64, "وما تنساش تعمل فولو لو عايز تشوف محتوى AI أتمتة تاني."),
]

_PUNCT = re.compile(r"[،,:؟?.؛;!]")


def tokens(text):
    """Words for captions. A dangling 'الـ' (ends with tatweel) is merged with the next word."""
    raw = [w for w in _PUNCT.sub(" ", text).split() if w]
    out, i = [], 0
    while i < len(raw):
        w = raw[i]
        if w.endswith("ـ") and i + 1 < len(raw):
            out.append([w, raw[i + 1]]); i += 2   # logical (reading) order
        else:
            out.append([w]); i += 1
    return out


def _weight(tok):
    return sum(len(p) + 2 for p in tok)


def caption_chunks():
    """[(start, end, [token,...], [(w0,w1) per token as fraction of chunk])], max 3 words each."""
    chunks = []
    for (a, b, text) in SEGS:
        toks = tokens(text)
        n = len(toks)
        k = math.ceil(n / 3)
        base, extra = divmod(n, k)
        sizes = [base + (1 if i < extra else 0) for i in range(k)]
        weights = [_weight(t) for t in toks]
        total = sum(weights)
        pos = 0
        acc = 0.0
        for s in sizes:
            grp = toks[pos:pos + s]; gw = weights[pos:pos + s]; pos += s
            t0 = a + (b - a) * acc / total
            acc += sum(gw)
            t1 = a + (b - a) * acc / total
            c = 0.0; spans = []
            for w in gw:
                spans.append((t0 + (t1 - t0) * c / sum(gw), t0 + (t1 - t0) * (c + w) / sum(gw)))
                c += w
            chunks.append((t0, t1, grp, spans))
    return chunks


# ---------- sound events ----------
def build_events():
    """(time, kind, pan, gain, extra): one sound per visual event."""
    E = []
    a = E.append
    # 1 title
    a((TI_RING[0], "hiss", 0.0, .6, TI_RING[1]))
    a((TI_RING[0] + TI_RING[1], "click", 0.0, .8, 0))
    a((TI_TITLE + 0.1, "tap", 0.0, .6, 0))
    # 2 repeat
    for i in range(4):
        a((RP_ROWIN + .08 * i + .12, "tick", 0.0, .5, 0))
    for i, t in enumerate(RP_TAPS):
        a((t, "tick", .12, .75, 0))
    a((RP_RESET, "tsk", 0.0, .35, 0))
    a((RP_POWER, "click", 0.0, .8, 0))
    a((RP_LABEL, "tap", 0.0, .6, 0))
    for i, t in enumerate(RP_AUTO[0]):
        a((t, "tick", -.1, .4, 0))
    a((RP_RESET2, "tsk", 0.0, .3, 0))
    for i, t in enumerate(RP_AUTO[1]):
        a((t, "tick", .1, .4, 0))
    # 3 AI
    a((AI_P1[0], "zap", 0.0, .8, 0)); a((AI_P1[0] + AI_P1[1], "click", 0.0, .7, 0))
    a((AI_CHECK1, "tick", 0.0, .5, 0))
    a((AI_OUT[0] + .05, "tsk", 0.0, .35, 0))
    a((AI_CHIP[0] + .35, "glass", 0.0, .5, 0))
    a((AI_P2[0], "zap", 0.0, .8, 0)); a((AI_P2[0] + AI_P2[1], "click", 0.0, .7, 0))
    a((AI_CHECK2, "tick", 0.0, .5, 0))
    a((AI_RING, "glass", 0.0, .5, 0))
    # 4 three things
    for i, t in enumerate(TH_BLOCK):
        a((t + .12, "tick", 0.0, .6, 0))
    for j, t in enumerate(TH_WIRE):
        a((t + .3, "tsk", 0.0, .35, 0))
    for i, t in enumerate(TH_HI):
        a((t, "click", 0.0, .7, 0))
    # 5 flow
    for t in FL_PRE:
        a((t, "click", 0.0, .6, 0))
    for (s, d) in (FL_B1, FL_B2):
        a((s, "zap", 0.0, .8, 0)); a((s + d, "click", 0.0, .7, 0))
    a((FL_FILL + .05, "glass", 0.0, .9, 0))
    a((FL_RINGS[1], "glass", 0.0, .45, 0))
    # 6 site
    a((35.15, "tick", 0.0, .5, 0))
    for t in SI_ORDER:
        a((t, "tick", 0.0, .7, 0))
    for (s, d) in SI_BOLT:
        a((s, "zap", 0.0, .8, 0)); a((s + d, "click", .0, .7, 0))
    for r in SI_ROWS:
        for t in r:
            a((t + .1, "tick", -.15, .4, 0))
    for t in SI_BELL:
        a((t + .45, "glass", .15, .45, 0))
    a((SI_ORDER_RESET, "tsk", 0.0, .3, 0))
    # 7 toggle / chat
    a((TG_FLIP[0], "click", 0.0, .9, 0))
    a((TG_RING + .1, "glass", 0.0, .5, 0))
    a((TG_LABEL + .2, "tap", 0.0, .6, 0))
    for (s, e) in CH_DOTS:
        a((s, "tick", -.12, .35, 0))
    for i, t in enumerate(CH_BUB):
        a((t + .02, "tap", -.12 if i % 2 == 0 else .12, .55, 0))
    a((CH_ORDER, "glass", 0.0, .8, 0))
    # 8 summary
    for c in SU_CYCLES:
        a((c, "zap", 0.0, .6, 0)); a((c + .24, "click", 0.0, .5, 0))
        a((c + .34, "zap", 0.0, .6, 0)); a((c + .58, "click", 0.0, .5, 0))
    a((SU_CHART[0], "hiss", 0.0, .55, SU_CHART[1]))
    a((SU_CHART[0] + SU_CHART[1], "click", .1, .7, 0))
    a((SU_CHART_RING + .02, "glass", 0.0, .4, 0))
    a((SU_HUMAN + .05, "tick", 0.0, .6, 0))
    a((SU_HRING[0], "hiss", 0.0, .45, SU_HRING[1]))
    a((SU_STAR, "glass", 0.0, .6, 0))
    # 9 follow
    a((FO_PLUS + .05, "tick", 0.0, .6, 0))
    a((FO_LABEL + .1, "tap", 0.0, .6, 0))
    a((FO_FILL, "glass", 0.0, .9, 0))
    # transitions: airy whoosh, only the three crossfades
    for x in XF:
        a((x - XFD / 2 - .02, "whoosh", 0.0, .55, 0.28))
    E.sort(key=lambda e: e[0])
    # enforce >= 80 ms spacing between events by nudging later
    out, last = [], -1.0
    for e in E:
        t = e[0]
        if t - last < .08:
            t = last + .08
        out.append((t,) + tuple(e[1:])); last = t
    return out
