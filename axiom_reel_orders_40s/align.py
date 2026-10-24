"""Estimate word timings from the voiceover energy. Output timing.json: {sentence: [[text, t0, t1], ...]}.
No speech recognizer is reachable in the sandbox, so words are placed by dynamic programming:
each word's length ~ its syllable weight, and word boundaries prefer low-energy frames. TIMING IS ESTIMATED."""
import wave, json, subprocess, numpy as np
from script import SENT, WIN
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','voiceover.mp3','-ac','1','-ar','16000','/tmp/vo16.wav'], check=True)
w = wave.open('/tmp/vo16.wav'); x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float)/32768
fr = 160; n = len(x)//fr; db = 20*np.log10(np.sqrt((x[:n*fr].reshape(n, fr)**2).mean(1))+1e-9)   # 10 ms frames
db = np.convolve(db, np.ones(3)/3, 'same'); MX = db.max()
def energy(i): return float(np.clip((db[i]-(MX-40))/34, 0, 1))      # 0 silence .. 1 loud
def dp(words, a, b):
    A, B = int(round(a*100)), int(round(b*100)); N = len(words); W = [x[1] for x in words]
    r = (B-A)/sum(W)/100                 # seconds per weight unit
    INF = 1e18; best = {0: {A: 0.0}}; back = {}
    for k in range(1, N+1):
        best[k] = {}; wk = W[k-1]*r*100
        lo = A+int(sum(W[:k])*r*100*0.6); hi = A+int(sum(W[:k])*r*100*1.4)
        for pos in range(max(lo, A+k*8), min(hi, B)+1):
            if k == N and pos != B: continue
            bc = INF; bp = None
            for pp, c in best[k-1].items():
                d = pos-pp
                if d < 8 or d > wk*2.2: continue
                cost = c+((d-wk)/max(wk, 6))**2*3+(0 if k == N else 5*energy(pos))
                if cost < bc: bc, bp = cost, pp
            if bp is not None: best[k][pos] = bc; back[(k, pos)] = bp
    pos = B; bounds = [B]
    for k in range(N, 0, -1): pos = back[(k, pos)]; bounds.append(pos)
    bounds = bounds[::-1]
    return [[words[i][0], round(bounds[i]/100, 2), round(bounds[i+1]/100, 2)] for i in range(N)]
out = {}
for key in SENT: out[key] = dp(SENT[key], *WIN[key])
json.dump(out, open('timing.json', 'w'), ensure_ascii=False, indent=0)
for k, v in out.items(): print(k, [(t, a, b) for t, a, b in v])
