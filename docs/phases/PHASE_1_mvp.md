# Phase 1 — MVP Engine (rule-based) ✅

**Goal.** A complete, transparent sing→guitar pipeline that runs end to end with
no ML and no external binaries — the baseline everything else is measured
against.

**Status:** ✅ Complete · **Depends on:** Phase 0 · **Feeds:** Phases 2–6

---

## Sub-phases

### 1.1 Pitch tracking & transcription
- pYIN f0 (`pitch.py`) → note segmentation, tempo estimate, beat quantization
  (`transcribe.py`).
- **DoD:** a WAV produces a clean, quantized monophonic `Melody`.

### 1.2 Key detection
- Krumhansl–Schmuckler profile correlation (`key.py`).
- **DoD:** C-major and A-minor fixtures detected correctly.

### 1.3 Rule-based harmonizer (3 tiers)
- Functional harmony with difficulty-scaled vocabulary (`harmony.py`):
  easy = triads/bar; normal = 7ths + V cadence; pro = 9th colours + ii–V–I.
- **DoD:** progression covers the melody, cadences on the tonic, pro uses 7ths/9ths.

### 1.4 Style engine
- Rhythmic accompaniment templates per style × level (`styles.py`):
  classical, flamenco, folk, bossa, pop_ballad.
- **DoD:** every style×level emits a tiled pattern.

### 1.5 Guitar arranger
- DP melody fingering (shortest-path / least hand movement) + chord voicings;
  melody on treble strings, harmony on bass strings (`arrange.py`).
- **DoD:** all events have frets 0–12, valid strings, registers separated → a
  physically playable tab.

### 1.6 Synthesis
- Karplus–Strong plucked-string synthesis + light reverb (`render.py`).
- **DoD:** finite audio, normalised to 0.9 peak, no soundfont/ffmpeg needed.

### 1.7 Notation export
- ASCII tablature, MIDI (GM nylon guitar), MusicXML (`notation.py`).
- **DoD:** all three outputs written; MusicXML opens in MuseScore.

### 1.8 Interfaces
- CLI (`python -m guitarmo`) and Gradio web app (`app.py`).
- **DoD:** both run; web app records/uploads → returns audio + tab + downloads.

### 1.9 Tests & demo
- pytest unit + end-to-end tests; `examples/make_example.py`.
- **DoD:** `pytest` green (11 tests); example arranges synthesized audio.

## Known limitations (carried into later phases)
- pYIN can be noisy on rough singing → **Phase 2** (CREPE/basic-pitch).
- Harmony is heuristic, not learned → **Phase 3** (trained model).
- Voicings/fingering are pragmatic, not optimal/idiomatic → **Phase 4**.
- Melody is folded into a 2-string range (octave compression possible) → revisit
  in Phase 4 with a full fretboard solver.

## Definition of Done (phase)
- [x] End-to-end sing→guitar works and is tested.
- [x] CLI + web app shipped.
- [x] Outputs: audio, MIDI, tab, MusicXML.
