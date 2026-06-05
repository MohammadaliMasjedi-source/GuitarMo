# 🗺️ GuitarMo — Roadmap

GuitarMo turns a sung melody into a classical-guitar arrangement. The project is
delivered in **phases**; each phase has **sub-phases**, each sub-phase has a
**Definition of Done (DoD)**. Progress is tracked live in
[PROGRESS.md](PROGRESS.md), and every task has a card in [tasks/](tasks/).

> **Philosophy.** Ship a working, transparent rule-based system first (Phases
> 0–1), then progressively replace heuristics with **open-source engines** and
> **trained models** (Phases 2–4), then polish and release (Phases 5–6). Every
> stage stays runnable end-to-end.

---

## Phase overview

| Phase | Title | Theme | Status |
|------:|-------|-------|--------|
| **0** | [Foundation & Setup](phases/PHASE_0_foundation.md) | repo, data model, theory | ✅ Done |
| **1** | [MVP Engine](phases/PHASE_1_mvp.md) | rule-based sing→guitar, end to end | ✅ Done |
| **2** | [Pitch & Rhythm Accuracy](phases/PHASE_2_pitch_accuracy.md) | integrate CREPE / basic-pitch / madmom | 🔜 Next |
| **3** | [Data-Driven Harmonization](phases/PHASE_3_harmonization_ml.md) | **train** a neural harmonizer on data | ⬜ Planned |
| **4** | [Expressive Arrangement](phases/PHASE_4_arrangement.md) | optimal fingering, counter-melody, better synth | ⬜ Planned |
| **5** | [App, UX & Deployment](phases/PHASE_5_app_deploy.md) | hosted demo, PDF/score, packaging | ⬜ Planned |
| **6** | [Evaluation & Release](phases/PHASE_6_release.md) | benchmarks, write-up, v1.0 | ⬜ Planned |

---

## Why each phase exists

- **Phase 0–1** give us a *baseline that already works* — useful immediately and
  a reference to measure every learned component against.
- **Phase 2** swaps the heuristic pitch tracker for state-of-the-art
  open-source engines (CREPE, Spotify basic-pitch, madmom) behind a pluggable
  interface, with a proper accuracy benchmark.
- **Phase 3** is the **training** milestone: collect melody+chord datasets and
  train a neural harmonizer (a modern take on Microsoft *MySong*/Songsmith and
  *DeepBach*). Runs on the RTX-3090 (ISSE).
- **Phase 4** makes the guitar writing *expressive and idiomatic* — optimal
  fingering, counter-melodies, ornaments, and optional physical-model/soundfont
  synthesis.
- **Phase 5** turns the engine into a polished, hosted product (HF Spaces /
  Docker), with in-browser tab rendering and PDF export, and PyPI packaging.
- **Phase 6** delivers the *research-grade* close: formal evaluation, a user
  study, reproducibility, a write-up, and a tagged v1.0.

---

## Dependency graph

```
P0 ─▶ P1 ─▶ P2 ─▶ P3 ─▶ P4 ─▶ P5 ─▶ P6
             └────────────┘
        (P2 accuracy feeds P3 training quality;
         P3 model + P4 arrangement both plug into P1's pipeline)
```

## Definition of Done — project level (v1.0)

- [ ] Sing → playable arrangement works for non-trivial real recordings.
- [ ] A *trained* harmonizer beats the rule-based baseline on a held-out set.
- [ ] Arrangements pass a guitarist-playability rubric at all three tiers.
- [ ] Public hosted demo + `pip install guitarmo`.
- [ ] Reproducible (configs, seeds, model cards) and documented.
- [ ] Tagged `v1.0.0` with CHANGELOG and CITATION.

See [PROGRESS.md](PROGRESS.md) for the live checklist.
