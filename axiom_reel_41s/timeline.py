"""Single timeline shared by visuals (scenes.py), captions and sound (audio.py). Absolute times in seconds.
Word times come from timing.json (estimated from the voiceover energy, see align.py)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30; TOTAL = 44.43
WT = json.load(open(os.path.join(HERE, 'timing.json')))
def w(key, i): return WT[key][i][1], WT[key][i][2]
# scene cuts sit in the real pauses of the voiceover. (name, start, end)
SCENES = [('A',0.0,2.21),('B',2.21,5.74),('C',5.74,9.75),('D',9.75,17.70),('E',17.70,20.48),
          ('F',20.48,25.56),('G',25.56,34.78),('H',34.78,38.04),('I',38.04,TOTAL)]
START = {n: s for n, s, e in SCENES}; END = {n: e for n, s, e in SCENES}
TRANS = [20.48, 38.04]; TD = 0.25            # two soft crossfades in 44 s (budget: 1 per ~20 s)
def L(sc, key, i, side=0): return WT[key][i][1+side]-START[sc]     # word time, local to scene

def events():
    """(global_time, kind, pan): one sound per visual event."""
    E = []
    def a(t, kind, pan=0.0): E.append((t, kind, pan))
    # A hook
    a(0.12,'tick'); a(w('S1',2)[0],'glass'); a(w('S1',5)[0],'glass')
    # B meeting
    for k,i in enumerate((0,2)): a(w('S2',i)[0],'tap',-.12 if k==0 else .12)
    a(w('S2',3)[0],'tsk'); a(w('S2',3)[0]+0.5,'hit'); a(w('S2',8)[0],'tap'); a(w('S2',9)[0],'glass')
    # C analyze
    a(w('S3',0)[0],'tsk'); a(w('S3',3)[0],'hit'); a(w('S3',4)[0],'tap')
    for i in (7,8,9): a(w('S3',i)[0],'tick' if i<9 else 'glass',.1)
    # D system
    a(w('S4',2)[0],'tsk')
    for i in (4,5,6): a(w('S4',i)[0],'tick',(-.1,0,.1)[i-4])
    a(w('S4',11)[0],'zap'); a(w('S4',11)[0]+0.5,'hit'); a(w('S4',12)[0],'zap'); a(w('S4',12)[0]+0.5,'hit')
    a(w('S4',14)[0],'zap'); a(w('S4',14)[0]+0.5,'hit'); a(w('S4',15)[0],'zap',.1); a(w('S4',15)[0]+0.5,'hit'); a(w('S4',18)[0]+0.15,'glass')
    # E problem solved
    a(w('S5',2)[0],'tick'); a(w('S5',4)[0],'tsk'); a(w('S5',6)[0]+0.1,'glass')
    # F not alone
    a(w('S6',5)[0],'tap'); a(w('S6',6)[0],'whoosh'); a(w('S6',9)[0],'tsk'); a(w('S6',11)[0],'glass')
    # G monthly + technical
    for k in range(5): a(w('S7',5)[0]+0.25*k,'tick',-.1)
    a(w('S7',8)[0],'tap'); a(w('S7',8)[0]+0.35,'tick'); a(w('S7',10)[0],'tap'); a(w('S7',10)[0]+0.35,'glass')
    for i,k in ((5,'S8'),(6,'S8'),(8,'S8'),(9,'S8')): a(w(k,i)[0],'hit',(-.1,.1,-.1,.1)[(5,6,8,9).index(i)]); a(w(k,i)[0]+0.15,'tick')
    # H you / system
    a(w('S9',2)[0],'glass',-.12); a(w('S9',7)[0],'glass',.12)
    # I CTA
    for k in range(3): a(w('S10',2)[0]+0.3*k,'tick')
    a(w('S10',8)[0],'tap'); a(w('S10',10)[0],'glass')
    for k in range(3): a(w('S10',15)[0]+0.25*k,'hit',(-.1,0,.1)[k])
    a(w('S10',16)[0]+0.3,'glass')
    for t in TRANS: a(t-0.12,'whoosh')
    return sorted(E)
