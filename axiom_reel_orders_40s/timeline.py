"""Single timeline shared by visuals (scenes.py), captions and sound (audio.py). Absolute seconds.
Word times come from timing.json (ESTIMATED from the voiceover energy, see align.py)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30; TOTAL = 39.9
WT = json.load(open(os.path.join(HERE, 'timing.json')))
def w(key, i, side=0): return WT[key][i][1+side]
# cuts sit in real voice pauses. (name, start, end)
SCENES = [('S1',0.0,5.28),('S2',5.28,9.87),('S3',9.87,12.92),('S4',12.92,16.40),('S5',16.40,19.62),
          ('S6',19.62,22.26),('S7',22.26,25.70),('S8',25.70,36.73),('S9',36.73,TOTAL)]
START = {n: s for n, s, e in SCENES}; END = {n: e for n, s, e in SCENES}
TRANS = [25.70]; TD = 0.25            # ONE soft crossfade (pain -> solution); everything else hard cuts
HOOK_KEYS = ('H1','H2','H3','H4')     # headline shot: no captions
CAP_KEYS = [k for k in WT if k not in HOOK_KEYS]
def pos(t):  # table scroll position (rows) at global time t: never stops
    return 2.2*t+0.35*t*t

def events():
    """(global_time, kind, pan): one sound per visual event."""
    E = []
    def a(t, kind, pan=0.0): E.append((t, kind, pan))
    # S1 hook: counter ticks, profit countdown, minus
    for k in range(10): a(0.1+k*0.11, 'num')
    a(1.35, 'glass')
    for k in range(5): a(2.3+k*0.2, 'num')
    a(3.45, 'glass', .1); a(4.3, 'tick')
    # S2 midnight
    a(5.3, 'tick')
    for k in range(10): a(5.8+k*0.4, 'tap', -.1 if k%2 else .1)
    # S3 two hours
    a(9.9, 'tsk')
    for k in range(10): a(10.0+k*0.24, 'tick', .1)
    a(12.3, 'glass')
    # S4 shipping
    a(w('D1',0), 'tap', -.1); a(w('D1',1), 'tsk'); a(w('D2',0), 'glass'); a(w('D3',0), 'tsk', .1); a(w('D3',2), 'whoosh', .1)
    # S5 phone: rings, ticks
    for k in range(4): a(16.45+k*0.2, 'hit')
    for k in range(6): a(17.8+k*0.3, 'tick', -.1 if k%2 else .1)
    # S6 peak
    a(19.62, 'glass')
    for k in range(10): a(19.75+k*0.14, 'num')
    a(21.75, 'hit')
    # S7
    a(24.1, 'tsk'); a(24.9, 'tap'); a(25.1, 'glass')
    # S8
    a(25.8, 'whoosh')
    for k in range(5): a(26.2+k*0.9, 'tap', .1)
    a(w('X1',10), 'tsk', -.1); a(w('X1',12), 'tsk', .1); a(w('X2',0), 'glass'); a(w('X2',3), 'tick')
    for k in range(8): a(34.0+k*0.3, 'tick', -.1 if k%2 else .1)
    # text beats (soft taps): two hours, wrong address, phone, returns, hand -> system
    a(10.15, 'tap'); a(w('D2',0)+0.05, 'tap'); a(16.55, 'tap'); a(19.95, 'tap'); a(w('W2',0), 'tap'); a(w('W2',3)+0.45, 'tap')
    # S9: CTA words, ring on FREE, table returns and every row gets its check
    a(36.8, 'tick'); a(w('C1',1), 'glass')
    for k in range(9): a(36.73+1.95+0.08*k, 'tick', .1)
    a(39.4, 'glass')
    a(TRANS[0]-0.12, 'whoosh')
    return sorted(E)
