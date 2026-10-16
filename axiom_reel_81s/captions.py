"""Burned-in captions: one line, 3-4 words, rounded #262626 box, DM Sans 500.
Current word white, spoken silver, upcoming graphite. Drawn on the final frame (not scaled),
box centred at (540, 1395): y 1357-1433 (limit 1470), width <= 800 so x stays inside 140-940 (button column starts 945).
Word timing is ESTIMATED (even split over each 3 s timeline segment); text is an English rendering of the outline points."""
import math
from PIL import Image, ImageDraw
import os
from PIL import ImageFont
from lib import font, S, HERE
from brand import *
LINES = ["Confirmation messages to customers, sent by hand, waste a lot of time.", "A traditional method that wastes time and drains effort.",
 "Automation and AI send confirmations instantly and automatically.", "Automated systems answer customer questions for you, saving time.",
 "No need to reply personally to every single customer.", "Problem two: logging WhatsApp and website customers by hand.",
 "Google Sheets or databases, all handled manually.", "Why keep working by hand when it can happen automatically?",
 "Data logging can become fully automatic, with no human touch.", "This is the easy part, before the real disaster.",
 "Dozens of customers a day, repeating the same questions.", "And you can't always reply in time.",
 "So you lose customers who would have bought from you.", "Imagine every customer getting an instant answer, any time.",
 "Meet the AI agent, which understands your products precisely.", "It helps customers with all kinds of questions.",
 "And it makes buying decisions easier for them.", "Get the most out of automation and AI.",
 "All of this works smoothly with modern automation tools.", "Want to know how to use AI to improve your work?",
 "Technology grows your business, profits and operations.", "Take the next step and explore more.",
 "Remember to use modern technology in commerce and business.", "Keep up with tech so you don't lose more opportunities.",
 "The goal: making business management simple through technology.", "Stay with us and keep learning.",
 "Follow the account to learn the method in detail."]
assert len(LINES) == 27
LINES_AR = ["بعت رسايل التأكيد للعملاء بإيدك بيضيع وقت كتير.", "طريقة قديمة بتهدر الوقت وبتستنزف مجهودك.",
 "الأتمتة والذكاء الاصطناعي بيبعتوا التأكيدات فوراً وتلقائي.", "السيستم بيرد على أسئلة العملاء بدالك.",
 "مش هتحتاج ترد بنفسك على كل عميل.", "المشكلة التانية: تسجيل بيانات عملاء الواتس والموقع بإيدك.",
 "جوجل شيتس أو الداتا بيز، كله بإيدك.", "ليه تشتغل بإيدك وممكن كله يحصل لوحده؟",
 "تسجيل الداتا ممكن يبقى أوتوماتيك من غير أي تدخل.", "ودي أسهل حتة قبل الكارثة الحقيقية.",
 "عشرات العملاء كل يوم بيسألوا نفس الأسئلة.", "وانت مش بتلحق ترد عليهم في الوقت المناسب.",
 "فبتخسر عملاء كانوا هيشتروا منك.", "تخيل كل عميل ياخد رد فوري في أي وقت.",
 "وكيل الذكاء الاصطناعي بيفهم تفاصيل منتجاتك بالظبط.", "وبيساعد العملاء في كل أسئلتهم المختلفة.",
 "وبيسهل عليهم قرار الشراء بسرعة.", "استفيد أقصى استفادة من الأتمتة والذكاء الاصطناعي.",
 "وكل ده بيتم بسلاسة بأدوات الأتمتة الحديثة.", "عايز تعرف تستغل الذكاء الاصطناعي إزاي في شغلك؟",
 "التكنولوجيا بتكبر البزنس وبتوسع الأرباح والعمليات.", "خد الخطوة الجاية دلوقتي واستكشف أكتر.",
 "استفيد من التقنيات الحديثة دي في التجارة والبزنس.", "واكب التطور التقني عشان ماتخسرش فرص أكتر.",
 "الهدف: نبسط إدارة البزنس بالتكنولوجيا.", "خليك معانا وكمل تعلم على طول.",
 "تابع الأكاونت لو عايز تعرف الطريقة بالتفصيل."]
assert len(LINES_AR) == 27
LANG = os.environ.get('CAPLANG', 'ar')
if LANG == 'ar': LINES = LINES_AR
_cf = {}
def cfont(sz):
    if sz not in _cf: _cf[sz] = ImageFont.truetype(os.path.join(HERE, 'fonts', 'cairo-arabic-600-normal.woff'), sz*S, layout_engine=ImageFont.Layout.RAQM)
    return _cf[sz]
def meas(f, s): return f.getlength(s, direction='rtl', language='ar')/S if LANG == 'ar' else f.getlength(s)/S
def getfont(sz): return cfont(sz) if LANG == 'ar' else font('dm5', sz)
CAPS = []
for i, line in enumerate(LINES):
    w = line.split(); k = math.ceil(len(w)/4); base, extra = divmod(len(w), k); p = 0
    for c in range(k):
        n = base+(1 if c < extra else 0); CAPS.append((i*3+c*3/k, i*3+(c+1)*3/k, w[p:p+n])); p += n
Y0, CY = 1340, 1395
def layout(words):
    sz = 46
    while True:
        f = getfont(sz); ws = [meas(f, x) for x in words]; sp = f.getlength(' ')/S; tot = sum(ws)+sp*(len(ws)-1)
        if tot+88 <= 800: return sz, ws, sp, tot
        sz -= 2
def box_for(words):
    sz, ws, sp, tot = layout(words); return (540-(tot+88)/2, 1357, 540+(tot+88)/2, 1433)
def draw(bg, t):
    cap = next((c for c in CAPS if c[0] <= t < c[1]), None)
    if cap is None: return
    t0, t1, words = cap; sz, ws, sp, tot = layout(words); f = getfont(sz)
    cur = min(len(words)-1, int((t-t0)/(t1-t0)*len(words)))
    lay = Image.new('L', (FW*2, 110*2), 0); msk = Image.new('L', (FW*2, 110*2), 0); d = ImageDraw.Draw(lay); m = ImageDraw.Draw(msk)
    bx0, by0, bx1, by1 = box_for(words); r = [bx0*2, (by0-Y0)*2, bx1*2, (by1-Y0)*2]
    d.rounded_rectangle(r, radius=38*2, fill=CHARCOAL); m.rounded_rectangle(r, radius=38*2, fill=255)
    x = 540-tot/2 if LANG != 'ar' else 540+tot/2          # Arabic: first word on the right, reading right to left
    for j, wd in enumerate(words):
        col = WHITE if j == cur else SILVER if j < cur else GRAPHITE
        if LANG == 'ar': x -= ws[j]; d.text((x*2, (CY-Y0)*2), wd, font=f, fill=col, anchor='lm', direction='rtl', language='ar'); x -= sp
        else: d.text((x*2, (CY-Y0)*2), wd, font=f, fill=col, anchor='lm'); x += ws[j]+sp
    bg.paste(lay.reduce(2), (0, Y0), msk.reduce(2))
if __name__ == '__main__':
    bx = [box_for(c[2]) for c in CAPS]
    print('chunks', len(CAPS), 'max words', max(len(c[2]) for c in CAPS), 'min words', min(len(c[2]) for c in CAPS))
    print('box x', min(b[0] for b in bx), max(b[2] for b in bx), 'y', bx[0][1], bx[0][3], '| safe x 35-1045, y<1470, button col x>=945')
