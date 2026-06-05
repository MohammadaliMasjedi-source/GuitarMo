# Phase 3 — Data-Driven Harmonization (TRAIN a model) ⬜

**Goal.** Learn to harmonize a melody from **data** instead of hand-written
rules — a modern take on Microsoft *MySong*/Songsmith (Simon et al. 2008) and
*DeepBach* (Hadjeres et al. 2017). This is the project's **training** milestone;
it runs on the RTX-3090 (ISSE).

**Status:** ⬜ Planned · **Depends on:** Phase 2 · **Feeds:** Phase 1 pipeline
(as an optional backend), Phase 4, Phase 6

---

## Sub-phases

### 3.1 Dataset acquisition
- Collect melody+chord corpora: **Nottingham** (folk, ABC w/ chords),
  **Hooktheory/TheoryTab**, **Wikifonia** leadsheets, **McGill Billboard**
  (chord annotations), **Lakh MIDI** (for augmentation). See
  [docs/DATASETS.md](../DATASETS.md). Provide `training/download_data.py`.
- **DoD:** download scripts run; license/attribution recorded; a small cached
  sample committed for smoke tests.

### 3.2 Preprocessing & representation
- Convert to a tokenized (melody → chord-per-beat) dataset; transpose-augment to
  all keys; reproducible train/val/test split.
- **DoD:** `dataset.npz`/`.jsonl` built deterministically from a config.

### 3.3 HMM baseline (reproduce MySong)
- Hidden-Markov harmonizer (chords = hidden states, melody = observations) — the
  classic, fast, explainable baseline.
- **DoD:** baseline chord-accuracy number on the test split.

### 3.4 Neural harmonizer (the trained model)
- Seq2seq (Transformer or BiLSTM) mapping melody → chord sequence; conditioned
  on style + difficulty. Train on RTX-3090; log curves.
- **DoD:** trained weights + training/val curves; inference < 1 s per song.

### 3.5 Evaluation & A/B vs rule-based
- Metrics: chord accuracy, chord-tone coverage, harmonic-rhythm plausibility;
  blind A/B listening vs the Phase-1 rule harmonizer.
- **DoD:** the trained model **beats the rule-based baseline** on held-out data.

### 3.6 Integrate as optional backend
- Wire into `harmony.py` behind `--harmonizer ml|rules`; ship weights via release
  assets / HF Hub; rules remain the zero-dependency default.
- **DoD:** `--harmonizer ml` works end to end; rules still default.

## Training infrastructure
- `training/` package: `download_data.py`, `preprocess.py`, `model.py`,
  `train.py`, `evaluate.py`, `configs/`. PyTorch. Deterministic seeds, model
  cards, checkpoints.

## Risks
- Dataset licensing (Hooktheory/Wikifonia) — prefer openly-licensed sources;
  document terms; don't redistribute restricted data.
- Style/difficulty conditioning needs labels — derive heuristically at first.

## Definition of Done (phase)
- [ ] Reproducible dataset pipeline.
- [ ] HMM baseline + trained neural model.
- [ ] Trained model beats baseline; integrated as optional backend with weights versioned.
