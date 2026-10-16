"""AXIOM monochrome brand values (working estimates, not pixel-sampled)."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))

BLACK = (0, 0, 0)          # Midnight Black  #000000
WHITE = (255, 255, 255)    # Pure White      #FFFFFF
CHARCOAL = (38, 38, 38)    # Charcoal        #262626
GRAPHITE = (85, 85, 85)    # Graphite Gray   #555555
SILVER = (191, 191, 191)   # Silver Gray     #BFBFBF
PALETTE = [BLACK, WHITE, CHARCOAL, GRAPHITE, SILVER]

F = lambda n: os.path.join(HERE, "fonts", n)
FONT = {
    "sg600": F("space-grotesk-latin-600-normal.woff"),
    "sg700": F("space-grotesk-latin-700-normal.woff"),
    "dm500": F("dm-sans-latin-500-normal.woff"),
    # Arabic: the one font exception (brand fonts have no Arabic glyphs)
    "ar600": F("cairo-arabic-600-normal.woff"),
    "ar700": F("cairo-arabic-700-normal.woff"),
}


def mix(c1, c2, a):
    a = max(0.0, min(1.0, a))
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * a)) for i in range(3))


def dim(c, a):
    """Colour c at brightness a over the black background."""
    return mix(BLACK, c, a)
