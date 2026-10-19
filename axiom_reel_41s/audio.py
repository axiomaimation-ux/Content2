"""Close-up ASMR effects synthesized in numpy from timeline.events(). One sound per visual event, >=80 ms apart."""
import numpy as np, wave, subprocess, timeline as T
SR = 48000; rng = np.random.default_rng(7)
def env(n, a_ms, tau_ms):
    t = np.arange(n)/SR; e = np.exp(-t/(tau_ms/1000)); at = int(SR*a_ms/1000)
    if at > 0: e[:at] *= np.linspace(0, 1, at)
    return e
def filt_noise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1/SR); X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n); return y/np.max(np.abs(y)+1e-9)
def sine(n, fr): return np.sin(2*np.pi*fr*np.arange(n)/SR)
def make(kind, var):
    p = 1+(rng.random()-.5)*0.12     # +-6 % pitch
    if kind == 'tick':  n = int(SR*.05);  return (sine(n, 1800*p)*.8+filt_noise(n, 3000, 8000)*.15)*env(n, 1, 12)*.7
    if kind == 'num':   n = int(SR*.03);  return sine(n, 3000*p)*env(n, .5, 6)*.35
    if kind == 'tap':   n = int(SR*.09);  return (filt_noise(n, 600, 2500)*.5+sine(n, 900*p)*.5)*env(n, 2, 20)*.8
    if kind == 'tsk':   n = int(SR*.07);  return filt_noise(n, 4500, 12000)*env(n, 1, 14)*.6
    if kind == 'hit':   n = int(SR*.04);  return (sine(n, 2400*p)*.8+filt_noise(n, 2000, 7000)*.2)*env(n, .5, 9)
    if kind == 'zap':
        n = int(SR*.18); g = (rng.random(n//240+1) > .45).astype(float).repeat(240)[:n]
        return filt_noise(n, 1500, 7000)*g*env(n, 3, 90)*.8
    if kind == 'glass':
        n = int(SR*.28); y = (sine(n, 1320*p)*.6+sine(n, 1980*p)*.3+sine(n, 3140*p)*.1)*env(n, 1, 70)
        m = int(SR*.09); y[:m] += sine(m, 90)*env(m, 2, 25)*.5; return y*.8
    if kind == 'whoosh':
        n = int(SR*.22); y = filt_noise(n, 800, 6000); k = np.hanning(n); return y*k*.25
def build(path='effects.wav'):
    global rng; rng = np.random.default_rng(7)
    ev = T.events(); L = np.zeros(int((T.TOTAL+.5)*SR)); R = np.zeros_like(L); last = -1; kept = 0
    for t, kind, pan in ev:
        t += (rng.random()-.5)*0.008
        if t-last < 0.08: continue
        last = t; y = make(kind, 0)*10**((rng.random()-.5)*4/20)      # +-2 dB
        pan = float(np.clip(pan+(rng.random()-.5)*.1, -.15, .15)); gl, gr = 1-max(0, pan), 1+min(0, pan)
        i = int(t*SR); L[i:i+len(y)] += y[:len(L)-i]*gl; R[i:i+len(y)] += y[:len(R)-i]*gr; kept += 1
    out = []
    for ch in (L, R):                                    # high-pass ~80 Hz
        X = np.fft.rfft(ch); f = np.fft.rfftfreq(len(ch), 1/SR); X[f < 80] *= np.clip(f[f < 80]/80, 0, 1)**2; out.append(np.fft.irfft(X, len(ch)))
    L, R = out; n = int(T.TOTAL*SR); L, R = L[:n], R[:n]
    pk = max(np.abs(L).max(), np.abs(R).max()); L, R = np.tanh(L/pk*1.2)/np.tanh(1.2), np.tanh(R/pk*1.2)/np.tanh(1.2)   # soft limit
    tgt = 10**(-11/20); pk = max(np.abs(L).max(), np.abs(R).max()); L, R = L/pk*tgt, R/pk*tgt           # peak -11 dBFS
    s = (np.stack([L, R], 1)*32767).astype('<i2')
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(s.tobytes())
    print('events in list', len(ev), 'kept', kept, 'peak dBFS', 20*np.log10(pk/pk*tgt))

def mix(effects='effects.wav', voice='voiceover.mp3', out='mix.wav'):
    """Voice peak -2 dBFS; effects peak 13 dB under the voice peak (-15 dBFS)."""
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',voice,'-ac','2','-ar','48000','/tmp/voice48.wav'], check=True)
    def rd(p):
        w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(float).reshape(-1, 2)/32768; return a
    v = rd('/tmp/voice48.wav'); e = rd(effects); n = int(T.TOTAL*SR)
    V = np.zeros((n, 2)); V[:min(n, len(v))] = v[:n]; V *= 10**(-2/20)/np.abs(V).max()
    E_ = np.zeros((n, 2)); E_[:min(n, len(e))] = e[:n]; E_ *= 10**(-15/20)/np.abs(E_).max()
    M = V+E_; assert np.abs(M).max() < 0.98
    with wave.open(out, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((M*32767).astype('<i2').tobytes())
    print('mix peak dBFS', 20*np.log10(np.abs(M).max()))

if __name__ == '__main__': build(); mix()
