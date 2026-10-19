# AXIOM brand constants (working values from visual estimates, not verified pixel samples)
BLACK, WHITE, CHARCOAL, GRAPHITE, SILVER = 0, 255, 38, 85, 191   # grayscale values of #000 #FFF #262626 #555 #BFBFBF
FONTS = {'sg6': 'space-grotesk-latin-600-normal.woff',   # headings 600
         'sg7': 'space-grotesk-latin-700-normal.woff',   # large statements 700
         'dm4': 'dm-sans-latin-400-normal.woff',          # body 400
         'dm5': 'dm-sans-latin-500-normal.woff'}          # labels / buttons 500
# Reels format and safe zone
FW, FH, FPS = 1080, 1920, 30
SAFE = dict(top=220, bottom=450, side=35)
CONTENT_SCALE = 0.85
SAFE_CENTER = (540, 845)
# background: dot grid 60 px, drift 18 px/s, loop 240 px
GRID, DRIFT, LOOP = 60, 18, 240
