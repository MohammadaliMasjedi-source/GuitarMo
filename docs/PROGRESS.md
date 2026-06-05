# ✅ GuitarMo — Progress Tracker

> **Live status of the plan.** Update this file as work lands. Each sub-phase
> lists its **Definition of Done (DoD)**. Legend: ✅ done · 🔄 in progress ·
> ⬜ not started · 🔜 next up.

**Overall:** ▓▓▓▓▓▓▓░░░░░░░░░░░░░ **~33%** (Phases 0–1 of 6 complete)

| Phase | Status | Progress |
|------:|--------|----------|
| 0 — Foundation & Setup | ✅ Done | ▓▓▓▓▓▓▓▓▓▓ 100% |
| 1 — MVP Engine | ✅ Done | ▓▓▓▓▓▓▓▓▓▓ 100% |
| 2 — Pitch & Rhythm Accuracy | 🔜 Next | ░░░░░░░░░░ 0% |
| 3 — Data-Driven Harmonization | ⬜ Planned | ░░░░░░░░░░ 0% |
| 4 — Expressive Arrangement | ⬜ Planned | ░░░░░░░░░░ 0% |
| 5 — App, UX & Deployment | ⬜ Planned | ░░░░░░░░░░ 0% |
| 6 — Evaluation & Release | ⬜ Planned | ░░░░░░░░░░ 0% |

---

## Phase 0 — Foundation & Setup ✅

- [x] **0.1** Repo scaffold, venv, dependencies, `.gitignore` — *DoD:* `pip install -r requirements.txt` succeeds; repo structure in place. ✅
- [x] **0.2** Core data model (`Note`, `Melody`, `ChordSpan`, `PluckEvent`) — *DoD:* importable, documented dataclasses. ✅
- [x] **0.3** Music-theory utilities (scales, chords, labels) — *DoD:* unit-tested chord/scale helpers. ✅

## Phase 1 — MVP Engine ✅

- [x] **1.1** Pitch tracking (pYIN) + note segmentation + quantization — *DoD:* WAV → quantized `Melody`. ✅
- [x] **1.2** Key detection (Krumhansl–Schmuckler) — *DoD:* C-major / A-minor test cases pass. ✅
- [x] **1.3** Rule-based harmonizer, 3 tiers — *DoD:* diatonic progression, cadence on tonic, ii–V–I at pro. ✅
- [x] **1.4** Style engine (classical, flamenco, folk, bossa, pop) — *DoD:* 5 styles × 3 levels produce patterns. ✅
- [x] **1.5** Guitar arranger (DP fingering + voicings) — *DoD:* physically valid tab (frets 0–12, registers separated). ✅
- [x] **1.6** Karplus–Strong synthesis + reverb — *DoD:* finite audio normalised to 0.9 peak, no external binaries. ✅
- [x] **1.7** Notation export (ASCII tab, MIDI, MusicXML) — *DoD:* all three files written and openable. ✅
- [x] **1.8** CLI + Gradio web app — *DoD:* `python app.py` and `python -m guitarmo` both work. ✅
- [x] **1.9** Test suite + example generator — *DoD:* `pytest` green (11 passing); `make_example.py` runs end-to-end. ✅

## Phase 2 — Pitch & Rhythm Accuracy 🔜

- [ ] **2.1** Pluggable pitch backends + CREPE/torchcrepe — *DoD:* `--pitch crepe|pyin` switch; CREPE optional install. ⬜
- [ ] **2.2** Spotify **basic-pitch** transcription backend — *DoD:* note-level transcription option behind same interface. ⬜
- [ ] **2.3** Onset/beat/meter (madmom) — *DoD:* tempo error reduced vs librosa on benchmark. ⬜
- [ ] **2.4** Input robustness (hum / whistle / noisy) — *DoD:* graceful handling + pre-filtering. ⬜
- [ ] **2.5** Evaluation harness (`mir_eval`, synthetic ground truth) — *DoD:* reported note-F-measure per backend. ⬜

## Phase 3 — Data-Driven Harmonization (TRAIN) ⬜

- [ ] **3.1** Dataset acquisition (Nottingham, Hooktheory, Wikifonia, McGill Billboard, Lakh) — *DoD:* download scripts + license notes; samples cached. ⬜
- [ ] **3.2** Preprocessing → melody/chord token dataset — *DoD:* reproducible train/val/test split. ⬜
- [ ] **3.3** HMM baseline (MySong-style) — *DoD:* baseline chord-accuracy number. ⬜
- [ ] **3.4** Neural harmonizer (seq2seq Transformer/LSTM), train on RTX-3090 — *DoD:* trained weights, training curves. ⬜
- [ ] **3.5** Evaluation + A/B vs rule-based — *DoD:* beats baseline on held-out set. ⬜
- [ ] **3.6** Integrate as optional harmony backend — *DoD:* `--harmonizer ml|rules` switch. ⬜

## Phase 4 — Expressive Arrangement ⬜

- [ ] **4.1** Optimal fingering (full graph DP, playability cost) — *DoD:* fewer position shifts vs current heuristic. ⬜
- [ ] **4.2** Data-driven voicings/tab (GuitarSet, DadaGP) — *DoD:* idiomatic voicings sampled from data. ⬜
- [ ] **4.3** Counter-melody / walking bass (pro tier) — *DoD:* independent inner voice at pro level. ⬜
- [ ] **4.4** Ornaments, dynamics, rubato; style idioms — *DoD:* perceptibly more musical renders. ⬜
- [ ] **4.5** Optional physical-model / soundfont synthesis — *DoD:* higher-fidelity audio backend, still optional. ⬜

## Phase 5 — App, UX & Deployment ⬜

- [ ] **5.1** Web app polish (waveform, piano-roll, live key/tempo) — *DoD:* visual feedback in UI. ⬜
- [ ] **5.2** In-browser tab/score (alphaTab/VexFlow) + PDF export — *DoD:* rendered notation + downloadable PDF. ⬜
- [ ] **5.3** Synced playback + tempo control — *DoD:* play-along with highlighting. ⬜
- [ ] **5.4** Deploy (HF Spaces / Docker) + PyPI `guitarmo` — *DoD:* public URL + `pip install guitarmo`. ⬜
- [ ] **5.5** Mobile/iPod-friendly capture — *DoD:* works from a phone browser. ⬜

## Phase 6 — Evaluation & Release ⬜

- [ ] **6.1** Formal evaluation + small user study — *DoD:* metrics + survey results. ⬜
- [ ] **6.2** Reproducibility (configs, seeds, model cards) — *DoD:* one-command repro of trained model. ⬜
- [ ] **6.3** Write-up / blog / paper draft — *DoD:* shareable document. ⬜
- [ ] **6.4** v1.0 release (CHANGELOG, CITATION.cff, tag) — *DoD:* tagged `v1.0.0`. ⬜

---

## Changelog of progress

| Date | Phase | What landed |
|------|-------|-------------|
| 2026-06-05 | 0 + 1 | Full rule-based MVP: pitch→transcribe→key→harmonize→arrange→synthesize→tab/MIDI/MusicXML; CLI + web app; 11 tests passing; demo generator. Repo published. |
