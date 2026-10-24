# AXIOM brand constants (working values from visual estimates, not verified pixel samples)
BLACK, WHITE, CHARCOAL, GRAPHITE, SILVER = 0, 255, 38, 85, 191   # grayscale values of #000 #FFF #262626 #555 #BFBFBF
FONTS = {'sg6': 'space-grotesk-latin-600-normal.woff',   # headings 600
         'sg7': 'space-grotesk-latin-700-normal.woff',   # large statements 700
         'dm4': 'dm-sans-latin-400-normal.woff',          # body 400
         'dm5': 'dm-sans-latin-500-normal.woff',
         'ca6': 'cairo-arabic-600-normal.woff',   # Arabic (the one font exception)
         'ca7': 'cairo-arabic-700-normal.woff'}          # labels / buttons 500
# Reels format and safe zone
FW, FH, FPS = 1080, 1920, 30
SAFE = dict(top=220, bottom=450, side=35)
CONTENT_SCALE = 1.0
SCENE_K = {'S1':1.0,'S2':1.0,'S3':1.0,'S4':1.0,'S5':1.0,'S6':1.0,'S7':1.0,'S8':1.0,'S9':1.0}
SAFE_CENTER = (540, 845)
# background: dot grid 60 px, drift 18 px/s, loop 240 px
GRID, DRIFT, LOOP = 60, 18, 240
