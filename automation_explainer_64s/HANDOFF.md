# Automation explainer 64 s (Arabic script, Instagram Reel) — handoff

Goal: 1080x1920, 30 fps, 64 s Reel in the AXIOM monochrome brand, built in code (Pillow + numpy + ffmpeg). No voiceover yet (user adds it later); effects-only ASMR audio. Arabic burned-in captions, one line, max 3 words, inside the safe zone.

## Status
- `out/automation_64s_v1.mp4` + `out/effects.wav` + `out/sound_events.json`. Next revisions: _v2, _v3 (never overwrite).
- Scenes (all IMAGINED by Claude, user asked for it; times = script timestamps):
  1 title 0-2 ring + orbit dot + "أتمتة ببساطة"; 2 repeat 2-7 task rows ticked by a tapper, then tick themselves, "تلقائياً"; 3 ai 7-13 human glyph -> AI chip, same result card check; 4 three 13-24 TRIGGER/PROCESS/ACTION blocks highlighted in turn; 5 flow 24-35 same stack, electricity runs, Action fills white; 6 site 35-43 website card -> bolt -> sheet rows + notification bell; 7a toggle 43-46 switch flips on "تلقائياً"; 7b chat 46-51 AI/customer bubbles, ORDER confirmed; 8 summary 51-61 fast chain, rising chart "إنتاجية", human glyph + star; 9 follow 61-64 plus -> check, "فولو".
- Transitions: 3 crossfades (0.25 s) at 13, 35, 51 s; all other changes are hard cuts.
- Script lines 13-24 and 24-35 are identical in the user's text; kept as given, shown with two different visuals.

## Hard rules (keep)
1. Safe zone: top 220, bottom 450, sides 35 px clear; right column x 945-1045 for y 1175-1470 clear. Centre (540, 845). Content scaled 0.85 about that centre (`K` in render.py). Captions box centred y 1350, width <= 800.
2. Background: dot grid 60 px, r 2.2, Charcoal; "+" marks Graphite every 4th; drifts up 18 px/s, loops each 240 px (400 frames).
3. Palette only #000000 #FFFFFF #262626 #555555 #BFBFBF. Fonts: Space Grotesk 600/700, DM Sans 500, Cairo 600/700 for Arabic (the one font exception). Labels >= 24 px after scaling.
4. No logos/watermarks. Real services (Google Sheet, WhatsApp, website) only as text labels + generic icons.
5. At most ~1 transition per 20 s. Sound: synthesized ASMR, one sound per visual event, from `timeline.py`, effects peak -11 dBFS.
6. Save to GitHub after every step.

## Run (from this folder, not `python3 -I`)
```
pip install pillow numpy       # ffmpeg required
python3 audio.py out/effects.wav out/sound_events.json
python3 render.py out/automation_64s_v2.mp4 out/effects.wav     # about 5 min on 2 cores
python3 sheet.py check.png 1 5 9 14 30 40 48 56 62               # contact sheet with safe-zone overlay (--raw for none)
```
## Files
brand.py palette/fonts; timeline.py all times, captions, sound events; render.py scenes, background, captions, ffmpeg; audio.py effects; sheet.py check sheets; fonts/.

## Notes
Caption word timing is estimated (character-weighted inside each segment). Not checked by ear or inside Instagram. Colours are working estimates.
## Open questions
Voiceover to re-fit timings; ending screen not requested; the untracked folder `automation_explainer_53s/` in the repo belongs to an earlier video and was left untouched.
