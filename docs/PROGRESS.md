# ✅ GuitarMo — Progress Tracker

> Auto-generated from `project_plan.py` (via `Sync.bat`). Edit the plan, not this file.

**Overall: 33%** · ✅ 12 done · 🔜 1 next · ⬜ 24 planned

| Phase | Status | Progress |
|------:|--------|----------|
| 0 — Foundation & Setup | ✅ Done | ▓▓▓▓▓▓▓▓▓▓ 100% |
| 1 — MVP Engine | ✅ Done | ▓▓▓▓▓▓▓▓▓▓ 100% |
| 2 — Pitch & Rhythm Accuracy | 🔜 Next up | ░░░░░░░░░░ 3% |
| 3 — Data-Driven Harmonization (TRAIN) | ⬜ Planned | ░░░░░░░░░░ 0% |
| 4 — Expressive Arrangement | ⬜ Planned | ░░░░░░░░░░ 0% |
| 5 — App, UX & Deployment | ⬜ Planned | ░░░░░░░░░░ 0% |
| 6 — Evaluation & Release | ⬜ Planned | ░░░░░░░░░░ 0% |

## Phase 0 — Foundation & Setup ✅
*A clean, reproducible project with the core data model and theory.*

- [x] **0.1** Repo scaffold & environment ✅ — *DoD:* pip install succeeds clean; import guitarmo works
- [x] **0.2** Core data model ✅ — *DoD:* Types importable + documented; Used across pipeline
- [x] **0.3** Music-theory utilities ✅ — *DoD:* chord_pcs/chord_label/scale_pcs tested

## Phase 1 — MVP Engine ✅
*Complete rule-based sing→guitar pipeline, end to end, tested.*

- [x] **1.1** Pitch tracking & transcription ✅ — *DoD:* A WAV yields a clean Melody
- [x] **1.2** Key detection ✅ — *DoD:* C-major & A-minor fixtures pass
- [x] **1.3** Rule-based harmonizer (3 tiers) ✅ — *DoD:* Covers melody, cadences on tonic; Pro uses 7ths/9ths
- [x] **1.4** Style engine ✅ — *DoD:* Every style x level emits a pattern
- [x] **1.5** Guitar arranger ✅ — *DoD:* Frets 0-12, valid strings, valid tab
- [x] **1.6** Synthesis ✅ — *DoD:* Finite audio normalised to 0.9 peak
- [x] **1.7** Notation export ✅ — *DoD:* All three outputs openable
- [x] **1.8** Interfaces (CLI + web) ✅ — *DoD:* app.py and python -m guitarmo both run
- [x] **1.9** Tests & demo ✅ — *DoD:* pytest green; make_example.py runs e2e

## Phase 2 — Pitch & Rhythm Accuracy 🔜
*Swap heuristics for SOTA open-source engines, proven by benchmark.*

- [ ] **2.1** Pluggable pitch backends + CREPE 🔜 — *DoD:* crepe|pyin switchable; CREPE optional; pYIN fallback
- [ ] **2.2** basic-pitch backend ⬜ — *DoD:* Same interface yields a Melody
- [ ] **2.3** Onset / beat / meter ⬜ — *DoD:* Lower tempo/onset error on benchmark
- [ ] **2.4** Input robustness ⬜ — *DoD:* Noisy/clipped inputs handled gracefully
- [ ] **2.5** Evaluation harness ⬜ — *DoD:* python -m guitarmo.eval compares backends

## Phase 3 — Data-Driven Harmonization (TRAIN) ⬜
*Train a neural harmonizer on data (MySong/DeepBach lineage), RTX-3090.*

- [ ] **3.1** Dataset acquisition ⬜ — *DoD:* Scripts run; sample cached; licenses noted
- [ ] **3.2** Preprocessing & representation ⬜ — *DoD:* Deterministic dataset from config
- [ ] **3.3** HMM baseline (MySong) ⬜ — *DoD:* Baseline chord-accuracy reported
- [ ] **3.4** Neural harmonizer (TRAIN) ⬜ — *DoD:* Trained weights + curves; Inference < 1s/song
- [ ] **3.5** Evaluation & A/B ⬜ — *DoD:* Beats rule-based on held-out set
- [ ] **3.6** Integrate as optional backend ⬜ — *DoD:* ml backend works e2e; rules still default

## Phase 4 — Expressive Arrangement ⬜
*Idiomatic, playable, musical guitar writing.*

- [ ] **4.1** Optimal fingering solver ⬜ — *DoD:* Fewer shifts, wider range
- [ ] **4.2** Data-driven voicings/tab ⬜ — *DoD:* Voicings look idiomatic
- [ ] **4.3** Counter-melody / walking bass ⬜ — *DoD:* Audible second voice at professional
- [ ] **4.4** Expression (ornaments/dynamics) ⬜ — *DoD:* Blind listeners prefer over Phase 1
- [ ] **4.5** Hi-fi synthesis (optional) ⬜ — *DoD:* Optional sf2|ks backend; KS default

## Phase 5 — App, UX & Deployment ⬜
*A polished, hosted product anyone can use from a browser/phone.*

- [ ] **5.1** Web app polish ⬜ — *DoD:* Users see what was heard
- [ ] **5.2** In-browser notation + PDF ⬜ — *DoD:* Rendered notation + PDF
- [ ] **5.3** Synced playback ⬜ — *DoD:* Synchronized audio + notation
- [ ] **5.4** Deploy & package ⬜ — *DoD:* Public URL + pip install + green CI
- [ ] **5.5** Mobile / iPod capture ⬜ — *DoD:* Works from a phone browser

## Phase 6 — Evaluation & Release ⬜
*Measure it, make it reproducible, write it up, ship v1.0.*

- [ ] **6.1** Evaluation + user study ⬜ — *DoD:* Metrics + survey reported
- [ ] **6.2** Reproducibility ⬜ — *DoD:* Fresh machine reproduces model + figures
- [ ] **6.3** Write-up ⬜ — *DoD:* Shareable document
- [ ] **6.4** Release v1.0 ⬜ — *DoD:* v1.0.0 tagged

---
See [CHANGELOG.md](../CHANGELOG.md) for the dated history.