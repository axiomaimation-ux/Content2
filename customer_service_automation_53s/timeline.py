"""Single timeline shared by visuals (scenes.py), captions and sound (audio.py). Absolute times in seconds.
Word times come from timing.json (estimated from the voiceover energy, see align.py)."""
import json, os
from script import KEYS
HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30; TOTAL = 52.76
WT = json.load(open(os.path.join(HERE, 'timing.json')))
def g(key, i, side=0): return WT[key][i][1+side]
# scene cuts sit in the real pauses of the voiceover. (name, start, end)
SCENES = [('A',0.0,2.85),('B',2.85,7.85),('C',7.85,11.48),('D',11.48,16.37),('E',16.37,22.50),
          ('F',22.50,26.62),('G',26.62,31.78),('H',31.78,36.50),('I',36.50,46.18),('J',46.18,TOTAL)]
START = {n: s for n, s, e in SCENES}; END = {n: e for n, s, e in SCENES}
TRANS = [16.37, 36.50]; TD = 0.25            # two soft crossfades in 52.8 s (budget: 1 per ~20 s)
# anchors (global seconds) shared by scenes and sound
AN = {
 'B': dict(trig=g('S2a',5), wf=g('S2a',7), q=g('S2b',0), proc=g('S2b',4)),
 'C': dict(cust=g('S3b',3)),
 'D': dict(prob=g('S4a',0)+0.05, api=g('S4b',2), cost=g('S4b',3), cut=g('S4b',5)),
 'E': dict(py=g('S5b',1)-0.35, link=g('S5c',0)),
 'F': dict(ring=g('S6',3), agent=g('S6',6), cust=g('S6',9)),
 'G': dict(model=g('S7',1), anth=g('S7',4), cards=g('S7',6), info=g('S7',8), client=g('S7',10)),
 'H': dict(q=g('S8',2), data=g('S8',8), guess=g('S8',10), x=min(g('S8',12), END['H']-0.55)),
 'I': dict(api=g('S9b',3), tools=g('S9b',8), perm=g('S9b',9), tasks=g('S9b',13)),
 'J': dict(save=g('S10a',3), server=g('S10a',5), restore=g('S10b',2), ctx=g('S10b',3), ret=g('S10b',6), reply=g('S10b',9)),
}
AN['C'].update(bub=AN['C']['cust']+0.25); AN['C'].update(arr=AN['C']['bub']+0.45, bolt=AN['C']['bub']+0.5, fill=AN['C']['bub']+0.92)
AN['E'].update(b1=AN['E']['link'], b2=AN['E']['link']+0.45, sysl=AN['E']['link']+0.9)
AN['I'].update(b1=AN['I']['api']+0.2, b2=AN['I']['api']+0.65)
def a(sc, name): return AN[sc][name]-START[sc]          # anchor, local to scene
def L(sc, key, i, side=0): return WT[key][i][1+side]-START[sc]     # word time, local to scene

def events():
    """(global_time, kind, pan): one sound per visual event."""
    E = []
    def ad(t, kind, pan=0.0): E.append((t, kind, pan))
    # A hook: skeleton line + 5 nodes + pulse
    ad(0.1,'tsk'); 
    for k in range(5): ad(0.35+0.2*k,'tick',0.0)
    ad(1.5,'zap'); ad(2.55,'glass')
    # B trigger
    s=START['B']; ad(s+0.2,'tick',-.1); ad(s+0.4,'tick',.1); ad(AN['B']['trig'],'glass'); ad(AN['B']['wf'],'tsk'); ad(AN['B']['proc'],'tap')
    # C
    ad(AN['C']['cust'],'tap'); ad(AN['C']['bub'],'tsk'); ad(AN['C']['arr'],'hit'); ad(AN['C']['bolt']+0.05,'zap'); ad(AN['C']['fill'],'glass')
    # D
    ad(AN['D']['prob'],'hit'); ad(AN['D']['api'],'tap')
    for k in range(4): ad(AN['D']['cost']+0.12*k,'tick',-.12+.08*k)
    ad(AN['D']['cut'],'tsk'); ad(AN['D']['cut']+0.3,'hit')
    # E
    ad(START['E']+0.35,'tick',-.1); ad(START['E']+1.5,'tick',.1); ad(START['E']+2.6,'tick',-.1)
    ad(AN['E']['py'],'tap'); ad(AN['E']['py']+0.5,'glass'); ad(AN['E']['b1'],'zap',-.05); ad(AN['E']['b1']+0.5,'hit'); ad(AN['E']['b2'],'zap',.05); ad(AN['E']['sysl']+0.05,'glass')
    # F
    ad(AN['F']['ring'],'tap'); ad(AN['F']['agent'],'glass'); 
    for k in range(4): ad(AN['F']['cust']+0.12+0.3*k,'tick',(-.12,.12,-.12,.12)[k]); ad(AN['F']['cust']+0.3+0.3*k,'hit',(-.1,.1,-.1,.1)[k])
    # G
    ad(AN['G']['model'],'tap'); ad(AN['G']['anth'],'tick'); 
    for k in range(3): ad(AN['G']['cards']+0.55*k+0.4,'hit',(-.1,0,.1)[k])
    ad(AN['G']['cards']+1.75,'glass'); ad(AN['G']['client'],'tick',-.1)
    # H
    ad(AN['H']['q'],'tap'); ad(AN['H']['data'],'tsk'); ad(AN['H']['data']+0.6,'glass'); ad(AN['H']['guess'],'tick',.1); ad(AN['H']['x'],'hit',.1)
    # I
    s=START['I']; ad(s+0.25,'tick'); ad(s+1.4,'tick')
    ad(AN['I']['api'],'tap'); ad(AN['I']['b1'],'zap'); ad(AN['I']['b2'],'zap'); ad(AN['I']['b2']+0.5,'glass')
    ad(AN['I']['tools'],'tap',-.12); ad(AN['I']['perm'],'tap',.12)
    for k in range(3): ad(AN['I']['tasks']+0.4*k,'tick',.1); 
    # J
    for k in range(3): ad(AN['J']['save']+0.35*k,'hit',-.1+.1*k)
    ad(AN['J']['server'],'glass'); ad(AN['J']['restore'],'tick'); ad(AN['J']['ctx'],'zap'); ad(AN['J']['ret'],'tap',.12); ad(AN['J']['reply'],'glass')
    for t in TRANS: ad(t-0.12,'whoosh')
    return sorted(E)
