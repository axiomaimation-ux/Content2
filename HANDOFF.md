# Automation explainer clip — handoff

Goal: a 12 s Instagram Reel (1080x1920, 30 fps) in the AXIOM monochrome brand, built in code (Pillow + numpy + ffmpeg). No logos or watermarks anywhere.

## Status
- DONE: `out/automation_12s_v4.mp4` (latest, content at 85%), `out/effects.wav` (ASMR effects stem), `out/sound_events.json`.
- Scenes: part 1 (0-3.2 s, imagined: a hand-repeated task becomes an automatic orbiting loop, words "Automation" / "TRIGGER · PROCESS · ACTION"); hard cut; part 2 (3.2-7.2 s: four stacked blocks Trigger, Process, Process, Action, electricity runs block to block, Action fills white); one 0.3 s crossfade at 7.05 s; part 3 (7.2-12 s: same stack with New Order, Order Data, Google Sheets, Notification; generic shape icons, no real logos).
- Audio: effects only, no voice (user adds a voiceover in the bigger video). Effects peak about -11 dBFS.
- Not checked by ear or in the Instagram app; timing is hand-set, not from a voiceover.

## Hard rules (always keep)
1. Instagram Reels safe zone: keep top 220 px, bottom 450 px, left/right 35 px clear; also keep the 100 px right column (x 945-1045, y about 1175-1470) clear. Safe band y 220-1470, centre (540, 845). Content is scaled to 85% about that centre (`K` in render.py). Verify with a safe-zone overlay on frames.
2. Textured background, never plain black: Charcoal #262626 dots (r 2.2 px, 60 px grid), Graphite #555555 "+" marks every 4th intersection, drifting up 18 px/s. Flat, no gradients, behind everything.
3. Palette only: #000000, #FFFFFF, #262626, #555555, #BFBFBF. Fonts: Space Grotesk 600/700, DM Sans 500 (Cairo for any Arabic). Captions off.
4. At most one real transition per ~20 s; hard cuts otherwise. No black gaps.
5. Sound: synthesized ASMR, one sound per visual event, driven from `timeline.py`.

## Run
```
pip install pillow numpy            # ffmpeg must be installed
python3 audio.py out/effects.wav out/sound_events.json
python3 render.py out/automation_12s_v5.mp4 out/effects.wav
python3 sheet.py check.png 0.5 2.9 4.6 7.2 8.5 11.9   # contact sheet of frames at those seconds
```
Run from this folder (not with `python3 -I`). Save revisions as _v5, _v6; never overwrite delivered files.

## Files
- `brand.py` palette + font paths; `timeline.py` all timings and the sound event list; `audio.py` effects synthesis; `render.py` scenes, background, compositing, ffmpeg render; `sheet.py` contact sheet helper; `fonts/` .woff files.

## Open questions
- Does the user want the clip as separate shots instead? (Currently one clip because a transition was requested.)
- Voiceover not supplied yet; timing may need re-fitting when it arrives.
