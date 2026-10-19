# Customer-service automation explainer reel (52.76 s) — handoff
Goal: 1080x1920, 30 fps Instagram Reel, AXIOM monochrome, code-only (Pillow+numpy+ffmpeg), no logos. Voiceover `voiceover.mp3` (Egyptian Arabic, user's own explanation of how he built the customer-service automation). On-screen words English; burned-in Egyptian-Arabic captions (Cairo = the one font exception). All scenes imagined by Claude (user said "use your imagination").

## Status
- v1 delivered: `out/customer_service_automation_52s_v1.mp4` (+ `out/effects.wav` effects stem). Content scaled 85% inside the safe zone; 2 crossfades (16.37 s, 36.50 s), all other cuts hard cuts in voice pauses.
- Timing ESTIMATED: sentence windows come from real pauses in the voice (checked with a whisper-small transcript per chunk); word times inside a phrase are placed by `align.py` (energy valleys + syllable weights). Captions may be off by a few tenths of a second inside long phrases.
- Not watched/heard by Claude; checked on frames, colours and levels only.

## Caption text
User's transcript with 3 spelling fixes: قبلتني→قابلتني, أبحت→أبحث, وده تجهزه→وده جهزته (the last one is a guess; verify against the voice). Commas/periods dropped.

## Scenes (imagined; one-line idea each)
A 0-2.85 vertical 5-node pipeline skeleton, pulse runs down | B 2.85-7.85 workflow of 3 blocks, TRIGGER lights, "?" | C 7.85-11.48 customer sends bubble to WHATSAPP MESSAGE block, bolt lights TRIGGER | D 11.48-16.37 warning sign, then WHATSAPP BUSINESS API block with rising cost bars, slashed and collapsed | E 16.37-22.5 magnifier searches the gap, PYTHON block drops in as bridge, messages flow | F 22.5-26.62 AI ring with orbiting dots, 4 customers exchange bubbles | G 26.62-31.78 HAIKU / ANTHROPIC block fed by BUSINESS INFO cards, fill bar | H 31.78-36.5 question splits to DATA (answer + check) vs GUESS (crossed out) | I 36.5-46.18 AI to SHOPIFY API to STORE DATA, TOOLS and PERMISSIONS chips, TASKS ticks | J 46.18-52.76 chat bubbles saved into SERVER, context returns to the agent when the customer comes back.

## Hard rules (copied from the skill)
- Safe zone: top 220, bottom 450, sides 35 px clear (y 220-1470, x 35-1045); right button column x 945-1045 for y>=1175 also clear. Centre (540, 845). Content drawn at 2x on a black layer, scaled 0.85 about (540, 845), composited with ImageChops.lighter over the full-size background.
- Background: dot grid 60 px, r 2.2, #262626; every 4th row/col a #555555 "+" (14 px); drifts up 18 px/s, loops every 240 px.
- Palette only: #000000 #FFFFFF #262626 #555555 #BFBFBF; flat. Fonts: Space Grotesk 600/700, DM Sans 500, Cairo (Arabic captions). Small labels >= 28 px pre-scale.
- Transitions: max 1 per ~20 s. No logos/watermarks/handles/URLs; on-screen text only from the script.
- Sound: synthesized ASMR (numpy), one sound per event >= 80 ms apart; voice peak -2 dBFS, effects ~13 dB under.
- Captions: one line, 2-4 words, #262626 rounded box y 1357-1433; current word white, spoken silver, upcoming graphite.
- Save to GitHub after every step; revisions as _v2, _v3, never overwrite delivered files.

## Run (from this folder, not python3 -I)
```
pip install pillow numpy --break-system-packages   # ffmpeg required; fonts in fonts/
python3 align.py                  # timing.json from voiceover.mp3
python3 audio.py                  # effects.wav + mix.wav
python3 render.py video silent.mp4        # ~95 s on 2 CPUs
ffmpeg -y -i silent.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -t 52.76 -movflags +faststart out/customer_service_automation_52s_v2.mp4
python3 verify.py                 # safe-zone bbox + palette
python3 sheet.py out.png 1 5 9    # contact sheet with safe-zone overlay (checking only)
```
Files: script.py, align.py, timeline.py (times, anchors, sound events), scenes.py, captions.py, audio.py, render.py, verify.py, sheet.py, brand.py, lib.py, fonts/, voiceover.mp3, timing.json.

## Open
User has not yet seen v1. Possible changes: scene visuals, caption timing/spelling, content scale.
