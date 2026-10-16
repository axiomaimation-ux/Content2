"""Synthesized close-up ASMR effects stem (numpy only, no samples)."""
import wave
import numpy as np
import timeline as T

SR = 48000
PEAK_DBFS = -11.0


def bandpass(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def tvec(n):
    return np.arange(n) / SR


def synth(kind, rng, extra):
    """Returns (left, right) arrays for one event, unit-ish level."""
    v = 1 + rng.uniform(-.06, .06)
    if kind == "tick":
        n = int(.045 * SR); t = tvec(n)
        f = 800 * v
        s = (2 / np.pi) * np.arcsin(np.sin(2 * np.pi * f * t)) * np.exp(-t / .010)
        nz = rng.standard_normal(n) * np.exp(-t / .003) * .25
        return s + nz, s + rng.standard_normal(n) * np.exp(-t / .003) * .25
    if kind == "tsk":
        n = int(.05 * SR); t = tvec(n)
        a = bandpass(rng.standard_normal(n), 4000, 12000) * np.exp(-t / .008)
        b = bandpass(rng.standard_normal(n), 4000, 12000) * np.exp(-t / .008)
        return a * 2.5, b * 2.5
    if kind == "click":
        n = int(.06 * SR); t = tvec(n)
        s = np.sin(2 * np.pi * 1500 * v * t) * np.exp(-t / .015)
        nz = rng.standard_normal(n) * np.exp(-t / .002) * .3
        return s + nz, s + nz * .8
    if kind == "tap":
        n = int(.14 * SR); t = tvec(n)
        s = (np.sin(2 * np.pi * 2000 * v * t) + .5 * np.sin(2 * np.pi * 3000 * v * t)) * np.exp(-t / .03)
        return s * .7, s * .7
    if kind == "glass":
        n = int(.55 * SR); t = tvec(n)
        s = sum(a * np.sin(2 * np.pi * f * v * t) * np.exp(-t / d)
                for f, a, d in ((2200, 1, .12), (3300, .5, .10), (4400, .25, .08)))
        s = s + .35 * np.sin(2 * np.pi * 110 * t) * np.exp(-t / .05)
        return s * .6, s * .6
    if kind == "zap":
        n = int(.18 * SR); t = tvec(n)
        outs = []
        for _ in range(2):
            gate = np.repeat((rng.random(n // int(.004 * SR) + 2) > .35).astype(float), int(.004 * SR))[:n]
            x = bandpass(rng.standard_normal(n), 1500, 6000) * gate * np.exp(-t / .07)
            outs.append(x * 2.0)
        return outs[0], outs[1]
    if kind == "hiss":
        n = int(extra * SR); t = tvec(n)
        env = (t / extra) ** 2
        env *= np.minimum(1, (extra - t) / .03)
        a = bandpass(rng.standard_normal(n), 3000, 9000) * env
        b = bandpass(rng.standard_normal(n), 3000, 9000) * env
        return a * 1.6, b * 1.6
    if kind == "whoosh":
        n = int(extra * SR); t = tvec(n)
        env = np.sin(np.pi * t / extra) ** 2
        a = bandpass(rng.standard_normal(n), 800, 4000) * env
        b = bandpass(rng.standard_normal(n), 800, 4000) * env
        return a * 1.4, b * 1.4
    raise ValueError(kind)


def build(events, path_wav):
    rng = np.random.default_rng(7)
    n = int(T.DUR * SR)
    L = np.zeros(n); R = np.zeros(n)
    log = []
    last = -1
    for (t, kind, pan, gain, extra) in events:
        t = t + rng.uniform(-.003, .003)
        g = gain * 10 ** (rng.uniform(-2, 2) / 20)
        l, r = synth(kind, rng, extra)
        pan = pan + rng.uniform(-.05, .05)
        ang = (pan + 1) * np.pi / 4
        i = int(t * SR)
        m = min(len(l), n - i)
        L[i:i + m] += l[:m] * g * np.cos(ang) * 1.41
        R[i:i + m] += r[:m] * g * np.sin(ang) * 1.41
        log.append((round(t, 3), kind, round(pan, 2), round(g, 2)))
        if t - last < .08:
            print("WARN close events", last, t, kind)
        last = t
    # gentle high-pass ~80 Hz, soft limiter, normalise to PEAK_DBFS
    for ch in (L, R):
        X = np.fft.rfft(ch); f = np.fft.rfftfreq(n, 1 / SR)
        X *= np.clip((f - 60) / 40, 0, 1)
        ch[:] = np.fft.irfft(X, n)
    st = np.stack([L, R], 1)
    st = np.tanh(st * 1.1)
    st *= 10 ** (PEAK_DBFS / 20) / np.abs(st).max()
    pcm = (st * 32767).astype("<i2")
    with wave.open(path_wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return log


if __name__ == "__main__":
    import json, sys
    log = build(T.build_events(), sys.argv[1])
    json.dump(log, open(sys.argv[2], "w"), indent=1)
    print(len(log), "events")
