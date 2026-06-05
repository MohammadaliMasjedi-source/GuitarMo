# 🏗️ GuitarMo — Architecture

GuitarMo is a linear pipeline of small, independently-testable modules. Data
flows left-to-right; timing is in **beats** until the final render.

```
                        ┌──────────────────────────────────────────────┐
   WAV (your voice)     │                guitarmo                       │
        │               │                                              │
        ▼               │  pitch.py        transcribe.py     key.py     │
  audio_io.load_audio ──┼─▶ pYIN f0 ──────▶ notes+tempo ───▶ Krumhansl  │
                        │                       │              │        │
                        │                       ▼              ▼        │
                        │  styles.py       harmony.py (3 tiers, uses key)│
                        │     │                  │                       │
                        │     ▼                  ▼                       │
                        │  arrange.py  ◀── ChordSpans + Melody           │
                        │   (DP fingering + voicings)                    │
                        │           │                                    │
                        │           ▼   list[PluckEvent]                 │
                        │   ┌───────┼─────────────┐                      │
                        │   ▼       ▼             ▼                      │
                        │ render.py notation.to_*  (tab / midi / xml)    │
                        │  (Karplus-Strong)                              │
                        └───────────┼──────────────────────────────────┘
                                    ▼
                    arrangement.wav · arrangement.mid · score.musicxml · tab.txt
```

## Modules

| Module | Responsibility | Key types in/out |
|--------|----------------|------------------|
| `core.py` | shared dataclasses + tuning constants | `Note`, `Melody`, `ChordSpan`, `PluckEvent` |
| `audio_io.py` | load / save / record audio | path → `(y, sr)` |
| `pitch.py` | f0 estimation (pYIN) | `y` → f0 track |
| `transcribe.py` | f0 → quantized notes + tempo | `y` → `Melody` |
| `theory.py` | pitch classes, chords, scales | pure functions |
| `key.py` | key detection + diatonic chords | `notes` → `Key` |
| `harmony.py` | melody → chord progression (3 tiers) | `Melody,Key` → `[ChordSpan]` |
| `styles.py` | rhythmic accompaniment templates | `(level, beats)` → events |
| `arrange.py` | melody+chords → fretboard | → `[PluckEvent]` |
| `render.py` | Karplus–Strong audio | events → `(y, sr)` |
| `notation.py` | tab / MIDI / MusicXML | events → files |
| `pipeline.py` | orchestrates all of the above | path → `Result` |
| `cli.py` / `app.py` | CLI / Gradio interfaces | — |

## Design principles

1. **Runnable at every phase.** New engines/models plug in behind interfaces;
   the rule-based path always works with zero heavy dependencies.
2. **Beats, not seconds.** Tempo-independent until render → clean quantization
   and arrangement.
3. **Disjoint registers.** Melody on treble strings, harmony on bass strings →
   tabs are always physically valid.
4. **No external binaries.** Karplus–Strong instead of soundfonts/ffmpeg keeps
   install trivial; richer synthesis is optional later.
5. **Explainable baseline first, learned components later** (see ROADMAP).

## Extension points (later phases)

- `PitchBackend` (Phase 2): `pyin` | `crepe` | `basic-pitch`.
- `Harmonizer` (Phase 3): `rules` | `ml` (trained model).
- `Synth` (Phase 4): `ks` | `sf2` (soundfont/physical model).
- `FingeringSolver` (Phase 4): heuristic | full fretboard graph.
