# AXIOM Reel: "Why choose Axiom for automation?" (44.4 s, 1080x1920, 30 fps)

## Goal / format
Instagram Reel in code (Python Pillow + numpy + ffmpeg), no AI footage, no logos. Voiceover = `voiceover.mp3` (Egyptian Arabic, 44.43 s). All scenes imagined by Claude (user said "imagine all scenes"). One full video, burned-in Egyptian-Arabic captions (exact script words), voice + light ASMR effects.

## Status
- v1 delivered: `AXIOM_reel_41s_v1.mp4` (+ `effects.wav` = effects stem alone). Content scaled 85% inside the safe zone.
- Timing is ESTIMATED: the user's timestamps were ~3 s shorter than the real audio, so cuts use the real pauses of the voice, and word times come from `align.py` (energy valleys + syllable weights; no speech recognizer was reachable). Cut/caption timing may be off by a few tenths of a second inside long sentences (S7/S8 boundary at 30.3 s is the least certain).
- Not watched/heard by Claude; checked on frames, colours and levels only.

## Scenes (imagined; one-line idea each)
A 0-2.2 gear with a big "?" (why choose) | B 2.2-5.7 two people, chat bubbles, link draws, business card fills (meeting) | C 5.7-9.8 workflow rows, magnifier finds a flagged row, checklist ticks (analyze, decide) | D 9.8-17.7 dashed system frame, nodes 01-02-03 with electricity, AI block, three API cards connect | E 17.7-20.5 tangled line straightens, check (solve it best) | F 20.5-25.6 hand-off blocked by an X, link between you and us stays lit (not alone) | G 25.6-34.8 month grid fills, OPERATION / RUNNING COSTS included; then 2x2 tiles CODE, APIs, MAINTENANCE, SUPPORT | H 34.8-38.0 your business vs the system (gear spins) | I 38.0-44.4 clocks become gears, DM bubble
Transitions: 2 soft crossfades (20.48 s and 38.04 s); everything else hard cuts in voice pauses.
On-screen headlines are English translations of script points; captions are Arabic (Cairo SemiBold = the one font exception; Latin words Axiom, AI, APIs, DM in DM Sans).

## Hard rules (copied from the skill; the next AI will not have it)
- Safe zone: top 220, bottom 450, sides 35 px clear (y 220-1470, x 35-1045); right button column x 945-1045 for y 1175-1470 also clear. Centre (540, 845). Content drawn at 2x on a black layer, scaled 0.85 about (540, 845), composited with `ImageChops.lighter` over the full-size background.
- Background: dot grid 60 px, r 2.2, #262626; every 4th row/col a #555555 "+" (14 px); drifts up 18 px/s, loops every 240 px. Never plain black.
- Palette only: #000000 #FFFFFF #262626 #555555 #BFBFBF; flat, no gradients. Fonts: Space Grotesk 600/700, DM Sans 500, Cairo (Arabic).
- Transitions: max 1 per ~20 s. No logos/watermarks/handles/URLs; text only from the script.
- Sound: synthesized ASMR (numpy), one sound per event, >= 80 ms apart; with voice, effects peak ~13 dB under the voice (voice peak -2 dBFS, effects -15 dBFS).
- Captions: one line, 3-4 words, #262626 rounded box y 1357-1433, x 140-940, current word white / spoken silver / upcoming graphite.
- Save to GitHub after every step; revisions as _v2, _v3, never overwrite delivered files.

## Run (from this folder, not with python3 -I)
```
pip install pillow numpy --break-system-packages    # ffmpeg required; fonts already in fonts/
python3 align.py                  # timing.json from voiceover.mp3 (estimated)
python3 audio.py                  # effects.wav + mix.wav (voice + effects)
python3 render.py video video_silent_v1.mp4        # ~80 s on 2 CPUs
ffmpeg -y -i video_silent_v1.mp4 -i mix.wav -c:v copy -c:a aac -b:a 192k -ar 48000 -ac 2 -t 44.43 -movflags +faststart AXIOM_reel_41s_v2.mp4
python3 verify.py                 # safe-zone bbox + palette check
python3 sheet.py out.png 1 5 9    # contact sheet with safe-zone overlay (checking only)
```
Files: script.py (script + syllable weights), align.py, timeline.py (times + sound events), scenes.py, captions.py, audio.py, render.py, verify.py, sheet.py, brand.py, lib.py, fonts/.

## Open
User has not yet heard/seen v1; possible changes: scene visuals, timing offsets, caption style/size, content scale.
