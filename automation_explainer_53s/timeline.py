"""Single source of truth for timing: visuals, captions and sound all read this.
Segment times come from the user's voiceover transcript; word times inside a segment
are ESTIMATED (character-weighted), segment boundaries are exact."""
import re

FPS = 30
DUR = 53.4   # voiceover ends 52.81 + short tail

# (start, end, text). Typos in the pasted transcript fixed: تتفذ->تتنفذ, أوامر->أوردر, نوصـلها->نوصلها
SEGS = [
    (0.00, 2.05, "هو ازاي الأوتوميشن بيشتغل؟"),
    (2.05, 8.35, "الأوتوميشن ببساطة هو انك تأتمت عملية بتعملها بشكل متكرر، بحيث تتنفذ تلقائياً بدل ما تعملها بنفسك كل مرة"),
    (8.35, 13.91, "حتى لو عملية محتاجة فيها ذكاء أو عقل بشري، ممكن تدخل فيها الـ AI عشان تطلع نفس النتيجة البشرية"),
    (13.91, 20.37, "وده بيحصل بأنك تحدد ثلاث حاجات، أولهم التريجر ايه اللي بيبدأ العملية دي؟"),
    (20.37, 23.47, "ثاني حاجة البروسيس ايه الخطوات المفروض تتنفذ؟"),
    (23.75, 27.67, "وثالث حاجة الأكشن ايه النتيجة اللي عايزين نوصلها؟"),
    (27.67, 36.87, "مثلاً لو عندك ويبسايت، أول ما العميل يعمل أوردر، السيستم بيسحب بالداتا بتاعت الأوردر ويسجلها في جوجل شيت ويبعت لك نوتفيكيشن"),
    (36.87, 42.63, "وكل ده تلقائياً من غير ما تدخل، وكمان الـ AI يبعت للعميل على الواتس عشان ياخد منه معلومات ويأكد الأوردر"),
    (42.63, 48.97, "يعني باختصار احنا بنحدد للسيستم امتى يبدأ، وإيه الخطوات اللي ينفذها، والنتيجة المطلوبة"),
    (49.11, 52.81, "علشان نسرع إنتاجية البزنس ونخلي البشر يفضلوا الحاجات المهمة"),
]
PUNCT = "،؟"

def bare(s):
    return "".join(ch for ch in s if ch not in PUNCT)

def _tokens(seg_i):
    t0, t1, txt = SEGS[seg_i]
    raw = txt.split()
    toks = []
    i = 0
    while i < len(raw):
        if raw[i] == "الـ" and i + 1 < len(raw) and raw[i + 1] == "AI":
            toks.append("الـ AI"); i += 2
        else:
            toks.append(raw[i]); i += 1
    w = [len(bare(x)) + 1.5 for x in toks]
    pause = [3.0 if (x[-1] in PUNCT and k < len(toks) - 1) else 0.0 for k, x in enumerate(toks)]
    total = sum(w) + sum(pause)
    scale = (t1 - t0) / total
    out, cur = [], t0
    for x, wi, pi in zip(toks, w, pause):
        out.append(dict(text=x, start=round(cur, 3), end=round(cur + wi * scale, 3), seg=seg_i))
        cur += (wi + pi) * scale
    return out

TOK = [_tokens(i) for i in range(len(SEGS))]

def tok(seg, key):
    for x in TOK[seg]:
        if bare(x["text"]).startswith(key):
            return x
    raise KeyError((seg, key))

def ts(seg, key):  return tok(seg, key)["start"]
def te(seg, key):  return tok(seg, key)["end"]

# ---- captions: one line, at most 3 words per chunk ----
def _chunks():
    chunks = []
    for si, toks in enumerate(TOK):
        cur = []
        for x in toks:
            cur.append(x)
            if len(cur) == 3 or x["text"][-1] in PUNCT:
                chunks.append(cur); cur = []
        if cur:
            if len(cur) == 1 and chunks and chunks[-1][0]["seg"] == si and len(chunks[-1]) < 3:
                chunks[-1] += cur
            else:
                chunks.append(cur)
    res = []
    for k, c in enumerate(chunks):
        s = c[0]["start"]
        nxt = chunks[k + 1][0]["start"] if k + 1 < len(chunks) else DUR
        segend = SEGS[c[0]["seg"]][1]
        e = nxt if (nxt <= segend + 1e-6 and chunks[k + 1][0]["seg"] == c[0]["seg"]) else min(segend + 0.12, nxt)
        res.append(dict(start=s, end=e, toks=c))
    return res

CHUNKS = _chunks()

# ---- scenes ----
B = [0.0, 2.05, 8.35, 13.91, 20.37, 23.75, 27.67, 36.87, 42.63, 48.97, DUR]   # scene k = [B[k], B[k+1])
XF = [(27.62, 0.25, 5, 6), (48.92, 0.25, 8, 9)]    # (start, dur, from scene idx, to scene idx): the 2 crossfades
def scene_index(t):
    for k in range(10):
        if B[k] <= t < B[k + 1]:
            return k
    return 9

# scene 1 (hook)
S1_ARC = (0.15, 0.7); S1_STEM = (0.85, 0.2); S1_DOT = 1.15

# scene 2 (a repeated task becomes automatic)
S2_AUTO = ts(1, "تتنفذ")
S2_MANUAL = []
_t = 2.55
while _t < S2_AUTO - 0.45:
    S2_MANUAL.append(round(_t, 3)); _t += 0.85
S2_AUTOTAPS = []
_t, _iv = S2_AUTO + 0.35, 0.55
while _t < 8.25:
    S2_AUTOTAPS.append(round(_t, 3)); _t += _iv; _iv = max(0.36, _iv - 0.05)

# scene 3 (AI does the human job)
S3_THINK0 = 8.55
S3_CARD1 = te(2, "عقل")
S3_AI = ts(2, "الـ")
S3_CARD2 = S3_AI + 0.55
S3_SAME = ts(2, "نفس")

# scenes 4-6 (trigger, process, action)
S4_BARS = ts(3, "ثلاث")
S4_LIGHT = ts(3, "أولهم")
S4_LABEL = ts(3, "التريجر")
S4_PRESS = ts(3, "بيبدأ")
S5_LIGHT = ts(4, "ثاني")
S5_LABEL = ts(4, "البروسيس")
S5_ROWS = [ts(4, "الخطوات"), ts(4, "المفروض"), ts(4, "تتنفذ")]
S6_LIGHT = ts(5, "وثالث")
S6_LABEL = ts(5, "الأكشن")
S6_HIT = ts(5, "نوصلها")
S6_LAUNCH = S6_HIT - 0.55

# scene 7 (website order example)
S7_CLICK = ts(6, "يعمل")
S7_PKT1 = ts(6, "بيسحب")
S7_ROW = ts(6, "ويسجلها")
S7_PKT2 = ts(6, "نوتفيكيشن") - 0.45
S7_BELL = ts(6, "نوتفيكيشن")
S7_REST = ts(6, "السيستم")

# scene 8 (hands-off, AI talks to the customer)
S8_CHAT = ts(7, "وكمان")
S8_B1 = ts(7, "يبعت")
S8_B2 = ts(7, "معلومات")
S8_B3 = ts(7, "ويأكد")

# scene 9 (recap)
S9_L = [ts(8, "امتى"), ts(8, "الخطوات"), ts(8, "والنتيجة")]
S9_PULSE = ts(8, "المطلوبة")

# scene 10 (benefit)
S10_BARS = ts(9, "نسرع")
S10_TREND = ts(9, "إنتاجية")
S10_PERSON = ts(9, "البشر")
S10_STAR = ts(9, "المهمة")


def build_events():
    """(time, kind, pan, gain, extra): one sound per visual event."""
    E = []
    a = E.append
    # 1 hook
    a((S1_ARC[0], "hiss", 0.0, .6, 0.8)); a((S1_DOT, "tap", 0.0, .7, 0))
    # 2 repeat -> automatic
    for i, x in enumerate(S2_MANUAL): a((x, "click", .1, .8, 0))
    a((S2_AUTO, "tap", 0.0, .7, 0))
    for i, x in enumerate(S2_AUTOTAPS): a((x, "tick", -.1, .5, 0))
    # 3 AI
    for k, x in enumerate([S3_THINK0 + .3, S3_THINK0 + 1.2, S3_THINK0 + 2.1]): a((x, "tick", (-.12, .12, 0)[k], .5, 0))
    a((S3_CARD1, "click", 0.0, .6, 0)); a((S3_AI, "tap", 0.0, .8, 0)); a((S3_CARD2, "glass", 0.0, .5, 0))
    # 4-6
    a((S4_BARS, "tsk", 0.0, .4, 0)); a((S4_LIGHT, "tick", -.15, .6, 0)); a((S4_LABEL, "tap", 0.0, .6, 0))
    a((S4_PRESS, "click", 0.0, .8, 0)); a((S4_PRESS + .18, "glass", 0.0, .5, 0))
    a((S5_LIGHT, "tick", 0.0, .6, 0)); a((S5_LABEL, "hiss", 0.0, .5, 0.5))
    for x in S5_ROWS: a((x + .1, "tick", .12, .5, 0))
    a((S6_LIGHT, "tick", .15, .6, 0)); a((S6_LABEL + .2, "tsk", 0.0, .5, 0))
    a((S6_LAUNCH, "zap", .1, .5, 0)); a((S6_HIT, "click", 0.0, .9, 0)); a((S6_HIT + .12, "glass", 0.0, .6, 0))
    # 7 example
    a((B[6] + .2, "tap", 0.0, .5, 0)); a((S7_REST + .1, "tsk", 0.0, .4, 0))
    a((S7_CLICK, "click", .1, .8, 0)); a((S7_PKT1, "zap", 0.0, .5, 0)); a((S7_ROW, "tick", 0.0, .6, 0))
    a((S7_PKT2, "zap", 0.0, .5, 0)); a((S7_BELL, "glass", 0.0, .6, 0))
    # 8 hands-off
    a((B[7] + .25, "tap", -.1, .5, 0)); a((S8_CHAT, "tsk", 0.0, .5, 0))
    a((S8_B1, "tap", -.12, .6, 0)); a((S8_B2, "tap", .12, .6, 0)); a((S8_B3, "tap", -.12, .6, 0)); a((S8_B3 + .35, "glass", 0.0, .7, 0))
    # 9 recap
    for k, x in enumerate(S9_L): a((x, "tick", 0.0, .7, 0))
    a((S9_PULSE, "zap", 0.0, .5, 0)); a((S9_PULSE + .42, "glass", 0.0, .7, 0))
    # 10 benefit
    for k in range(5): a((S10_BARS + .1 + k * .2, "tick", -.15 + .075 * k, .5, 0))
    a((S10_PERSON, "tap", 0.0, .6, 0)); a((S10_STAR, "glass", 0.0, .8, 0))
    # the two crossfades (the only transitions)
    for (x0, xd, _, _) in XF: a((x0, "whoosh", 0.0, .5, xd))
    E.sort()
    # enforce >= 85 ms between events (nudge later ones)
    for i in range(1, len(E)):
        if E[i][0] - E[i - 1][0] < 0.085:
            E[i] = (round(E[i - 1][0] + 0.085, 3),) + E[i][1:]
    E.sort()
    return E

if __name__ == "__main__":
    import json
    out = dict(segments=[dict(start=s, end=e, text=t) for s, e, t in SEGS],
               tokens=[x for seg in TOK for x in seg],
               chunks=[dict(start=c["start"], end=c["end"], text=" ".join(x["text"] for x in c["toks"])) for c in CHUNKS])
    json.dump(out, open("timing.json", "w"), ensure_ascii=False, indent=1)
    for c in CHUNKS: print(f'{c["start"]:6.2f}-{c["end"]:6.2f}', " ".join(x["text"] for x in c["toks"]))
    print(len(build_events()), "events")
