# AXIOM Reel "100 orders, losing money" (40 s) — handoff
Goal: Instagram Reel 1080x1920, 30 fps, AXIOM monochrome brand, built in code (Pillow + numpy + ffmpeg). No logos/watermarks.

## Setup answers (this Reel only)
- Visuals: user described all 9 shots (see scenes.py). Nothing imagined except: gear icons in shot 8 (tools), shot-1 coin/cart icons, hand icon.
- Output: full video, burned Arabic captions (from shot 2), length 40 s as recorded (exception to the 30 s max, user's choice).
- Text: user's own shot texts kept (override of "headline in shot 1 only"), captions also on from shot 2.
- Stage: trust, CTA = keyword FREE by DM. User kept "Axiom" in the voice at 0:27 (override of "name only in CTA").
- Proof level: 0 (the 100-orders example is hypothetical, tagged "مثال" in shot 1). No real numbers/clients.
- Voice: user's ElevenLabs file `voiceover.mp3`; timing in `timing.json` is ESTIMATED from energy (align.py), not speech-recognised.

## Status
- v1 delivered: `out/axiom_orders_reel_v1.mp4`, `out/cover.png` (frame 0, counter at 100), `out/effects.wav`.

## Hard rules kept
Safe zone x 35-1045, y 220-1470, centre (540,845), right button column x 945-1045 y>=1175 empty; textured dot-grid bg (60 px, #262626 dots, #555555 plus marks, drift 18 px/s); palette #000 #FFF #262626 #555 #BFBFBF; Space Grotesk / DM Sans, Cairo for Arabic; captions >=52 px at one fixed spot (y 1357-1433, box inside x 135-945); <=1 transition (one 0.25 s crossfade at 25.70 s); ASMR synthesized effects, peak -11 dBFS, mix voice -2 dBFS / effects -15 dBFS; no scarcity wording; no invented numbers.

## Run (from this folder, not python -I)
```
python3 align.py            # only if voiceover changes -> timing.json
python3 audio.py            # effects.wav + mix.wav
python3 render.py x out/video_silent.mp4
ffmpeg -y -i out/video_silent.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -movflags +faststart -shortest out/axiom_orders_reel_v2.mp4
python3 sheet.py check.png 0 4.9 7 11.9 14.7 19 21.9 25.3 30.5 38.6 39.8   # safe-zone contact sheet
python3 verify.py           # safe zone / palette / static check
```
## Files
brand.py, lib.py, scenes.py (9 shots), timeline.py (cuts + sound events), captions.py, audio.py, align.py, script.py (script + pause windows), timing.json, verify.py, sheet.py, fonts/, voiceover.mp3.

## Hook test plan
Keep the body, re-make only the first 3 s with a result-framed variant; log 0:06 retention, skip rate, shares per version here.
## Open
- Timing is estimated; if captions drift, re-fit WIN in script.py.
- Not heard by ear / not viewed inside Instagram.
