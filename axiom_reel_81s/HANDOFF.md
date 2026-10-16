# AXIOM Reel: "Manual work vs. automation" (81 s, 1080x1920, 30 fps)

## Goal / format
Instagram Reel built entirely in code (Python Pillow + numpy + ffmpeg). No AI footage. Script = timed outline (Arabic, 00:00-01:21); on-screen text is English translations of the script's own points. All visuals were imagined by Claude (user asked for "imagine all scenes").

## Status
- v1: full video without captions (delivered, kept).
- v2: same video + burned-in captions (`captions.py`): one line, 3-4 words, #262626 rounded box, DM Sans 500, current word white / spoken silver / upcoming graphite, box y 1357-1433, x 140-940 (inside safe zone). Word timing estimated (even split per 3 s segment); text is an English rendering of the outline points, not the spoken words. Run: `python3 render.py video video_silent_v2.mp4` then mux as below.
- v3: same as v2 but captions in ARABIC (user request). Font exception: Cairo SemiBold 600 (`fonts/cairo-arabic-600-normal.woff`, npm `@fontsource/cairo`) because Space Grotesk/DM Sans have no Arabic glyphs; same white/silver/graphite roles, drawn right to left with Pillow raqm (`direction='rtl'`), word by word. Text = `LINES_AR` in captions.py (spoken-style Arabic written from the outline points, not the speaker's real words). On-screen headlines stay English. English captions: `CAPLANG=en python3 render.py video out.mp4`. Run v3: `python3 render.py video video_silent_v3.mp4` then mux.
- v4: same as v3 but the Arabic captions are rewritten in EGYPTIAN dialect (user request): `LINES_AR` in captions.py (spoken-style Egyptian from the outline points, no Latin words because Cairo's Arabic subset has no Latin glyphs). Scenes, timing and audio unchanged. Run: `python3 render.py video video_silent_v4.mp4` then mux as above (about 3.5 min).
- `effects.wav` is the separate effects stem. No voiceover supplied yet.

## Scenes (all imagined; ideas in one line)
- A 0-6 Problem 01: rows of customers with hand-typed confirmations, then a spinning clock (wasted time)
- B 6-12 Automation: ORDER > AI > CONFIRMATION chain with electricity, then question/answer chat
- C 12-15 Five customers answered at once by an AI node, counter "personal replies" 5 > 0
- D 15-24 Problem 02: WhatsApp/Website > sheet filled cell by cell; sheet + database icons; "Why still by hand?" toggle flips MANUAL > AUTO
- E 24-30 Sources > bolts > sheet fills itself; progress bar "EASY" vs "THE REAL DISASTER" with warning triangle
- F 30-42 Flood of "?" bubbles; late-reply clock with timer; customers walk away from carts; 24-tick ring "ANYTIME / INSTANT ANSWER"
- G 42-54 AI agent absorbing product cards; Q/A chat; person > cart > BUY; TRIGGER > PROCESS > ACTION chain
- H 54-60 Orbiting pulse around nodes; big "?" with ring pulses
- I 60-81 Growth bars; play-circle "next step"; cart + gear; stair climb collecting opportunities; tangled line becomes straight; learning loop; closing text (follow the account)

## Hard rules (copied from the skill, the next AI will not have it)
- Safe zone: top 220 px, bottom 450 px, sides 35 px clear (y 220-1470, x 35-1045); right button column x 945-1045 for y 1175-1470 also clear. Centre of the zone is (540, 845).
- Content is drawn on a 2x black L layer at full-frame coords, scaled by 0.85 about (540, 845), composited over the background with `ImageChops.lighter`. Background is full size, unscaled.
- Background: Midnight Black, dot grid 60 px (r 2.2, #262626), every 4th row/col intersection a graphite (#555555) "+" mark ~14 px, drifting upward 18 px/s, loop every 240 px. Same on every scene.
- Palette (working values from visual estimates): #000000, #FFFFFF, #262626, #555555, #BFBFBF. Flat, monochrome, no gradients.
- Fonts: Space Grotesk 600/700 (headings, wordmark-level text), DM Sans 400/500 (body, labels, buttons). Small labels uppercase with wide tracking, >= 24 px after scaling.
- No logos, wordmarks, watermarks, handles, URLs. Text only from the script.
- Transitions: max 1 per ~20 s; used 4 (soft 0.25 s crossfades at 15, 30, 42, 60 s). Everything else hard cuts or in-scene changes.
- Sound: synthesized close-up ASMR (numpy), one sound per on-screen event, >= 80 ms apart, effects peak -11 dBFS with no voiceover; separate `effects.wav`.

## How to run (from this folder)
```
npm i @fontsource/space-grotesk @fontsource/dm-sans   # then copy the 4 .woff files listed in brand.py into fonts/ (already included)
pip install pillow numpy --break-system-packages
python3 audio.py                  # effects.wav
python3 render.py video           # video_silent.mp4 (about 3 min on 1 CPU)
ffmpeg -y -i video_silent.mp4 -i effects.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -t 81 -movflags +faststart AXIOM_reel_v1.mp4
python3 verify.py                 # safe-zone check at 10 fps
python3 sheet.py out.png 1 5 9    # contact sheet with safe-zone overlay (checking only)
```
Files: brand.py (constants), timeline.py (shared times + sound events), lib.py (drawing), scenes.py (nine scenes), audio.py, render.py, verify.py, sheet.py.

## Decisions made
Imagine all scenes; one full video (not shots); English on-screen text; captions ON from v2 (user asked); no ending screen; audio = ASMR effects only (voiceover to be added by user).

## Open
Voiceover file (to align timing exactly); whether the final "follow the account" line needs a handle (none invented).
