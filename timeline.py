"""Single source of truth for timing: visuals and sound both read this."""

FPS = 30
DUR = 12.0
CUT_1_2 = 3.2                 # hard cut, part 1 -> part 2
XFADE = (7.05, 0.30)          # the one real transition, part 2 -> part 3

# Part 1 (imagined)
HOPS = [(0.55, 0.85, 0, 1), (0.95, 1.25, 1, 2), (1.35, 1.65, 2, 0)]
RING = (1.7, 0.6)
NODE_FILL = [1.7, 1.9, 2.1]
ORBIT_START = 2.0
TITLE_T = 2.5
SUB_T = 2.75

# Parts 2 and 3: (start, travel) per segment of the electricity pass
STACK = {
    2: dict(first=[(4.35, .45), (4.9, .45), (5.45, .45)],
            second=[(6.05, .25), (6.3, .25), (6.55, .25)],
            rings=[(6.8, 1.0)]),
    3: dict(first=[(7.5, .55), (8.2, .55), (8.9, .55)],
            second=[(9.8, .3), (10.1, .3), (10.4, .3)],
            rings=[(10.7, 1.0), (11.3, .7)]),
}
BLOCK_IN = lambda i: 3.0 + 0.16 * i     # part 2 block entrance
WIRE_IN = lambda j: 3.5 + 0.16 * j      # part 2 wire draw


def activations(mode):
    f = STACK[mode]["first"]
    return [f[0][0]] + [s + d for s, d in f]


def build_events():
    """(time, kind, pan, gain, extra) one sound per visual event."""
    E = []
    # part 1
    E.append((0.20, "tick", 0.0, .8, 0))
    E += [(0.85, "tick", .15, .7, 0), (1.25, "tick", -.15, .7, 0), (1.65, "tick", 0.0, .7, 0)]
    E.append((RING[0], "hiss", 0.0, .7, RING[1]))
    E.append((RING[0] + RING[1], "click", 0.0, .8, 0))
    E.append((TITLE_T, "tap", 0.0, .6, 0))
    E.append((SUB_T, "tick", 0.0, .4, 0))
    # part 2 and 3
    for mode in (2, 3):
        S = STACK[mode]
        if mode == 2:
            for i in range(4):
                E.append((BLOCK_IN(i) + 0.1, "tick", 0.0, .7, 0))
            for j in range(3):
                E.append((WIRE_IN(j) + 0.3, "tsk", 0.0, .4, 0))
        for k, (s, d) in enumerate(S["first"]):
            E.append((s, "zap", 0.0, .8, 0))
            if k < 2:
                E.append((s + d, "click", 0.0, .7, 0))
        E.append((S["first"][2][0] + S["first"][2][1], "glass", 0.0, .9, 0))
        for s, d in S["second"]:
            E.append((s, "zap", 0.0, .5, 0))
        for r, (rt, g) in enumerate(S["rings"]):
            E.append((rt, "glass", 0.0, .5 if r == 0 else .35, 0))
    E.append((XFADE[0] - 0.05, "whoosh", 0.0, .6, 0.25))
    E.sort()
    return E
