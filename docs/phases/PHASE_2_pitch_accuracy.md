# Phase 2 — Pitch & Rhythm Accuracy 🔜

**Goal.** Replace the heuristic front-end with **state-of-the-art open-source
engines** behind a pluggable interface, and prove the improvement with a real
benchmark. Accurate transcription is the foundation for good harmonization
(Phase 3).

**Status:** 🔜 Next · **Depends on:** Phase 1 · **Feeds:** Phase 3

---

## Sub-phases

### 2.1 Pluggable pitch backends + CREPE
- Define a `PitchBackend` interface; implement `pyin` (current) and `crepe`
  (Kim et al. 2018) via `torchcrepe`/`crepe`. Select with `--pitch`.
- **DoD:** `--pitch crepe|pyin` works; CREPE is an *optional* extra
  (`requirements-ml.txt`); falls back to pYIN if not installed.

### 2.2 Spotify basic-pitch backend
- Add `basic-pitch` (Bittner et al. 2022) as a note-level transcription option
  (handles light polyphony, gives note events directly).
- **DoD:** same interface produces a `Melody`; documented trade-offs.

### 2.3 Onset / beat / meter
- Integrate **madmom** for onset & beat tracking; estimate meter; improve
  quantization. Keep librosa as fallback.
- **DoD:** lower tempo/onset error than librosa on the benchmark set.

### 2.4 Input robustness
- Pre-processing: high-pass, noise gate, loudness normalize; detect hum vs
  whistle vs sung vowel; helpful error messages.
- **DoD:** noisy/clipped inputs handled gracefully; no crashes.

### 2.5 Evaluation harness
- Synthetic ground-truth generator (known MIDI → audio) + real clips; score with
  `mir_eval` (note F-measure, raw-pitch accuracy, tempo error).
- **DoD:** a `python -m guitarmo.eval` report comparing all backends.

## Open-source engines (see docs/ENGINES.md)
| Engine | Use | License |
|--------|-----|---------|
| CREPE / torchcrepe | f0 | MIT |
| Spotify basic-pitch | note transcription | Apache-2.0 |
| madmom | onsets/beats | BSD (academic) |
| mir_eval | evaluation | MIT |

## Risks
- Heavy deps (TensorFlow/PyTorch) — keep them **optional** behind extras so the
  base install stays light.
- CREPE latency — offer `tiny`/`full` model sizes.

## Definition of Done (phase)
- [ ] ≥2 pitch backends + 1 note-transcription backend, switchable.
- [ ] Benchmark shows measurable accuracy gain over Phase 1.
- [ ] Base install remains binary-free; ML engines optional.
