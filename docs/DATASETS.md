# 📊 GuitarMo — Datasets (for the trainable models)

The learned components (Phase 3 harmonizer, Phase 4 arrangement) need data.
This document lists candidate corpora, what each is for, and licensing notes.
Acquisition scripts live in [`training/`](../training/).

> ⚠️ **Licensing first.** Several music datasets have research-only or
> share-alike terms, and some (e.g. Hooktheory) are not freely redistributable.
> GuitarMo **does not redistribute** restricted data — scripts download from the
> original source and we cache only what each license permits. Always check the
> source terms.

## Melody → chord (Phase 3 harmonization)

| Dataset | Content | Size | Use | License / terms |
|---------|---------|------|-----|-----------------|
| **Nottingham** | folk tunes, ABC with chord symbols | ~1000 tunes | primary train | public domain tunes (collection MIT-ish) |
| **Wikifonia** (archived) | lead sheets (melody + chords) | ~6000+ | train/augment | mixed; respect original terms |
| **Hooktheory / TheoryTab** | melody + functional chords | large | train (if licensed) | **not freely redistributable** — API/manual only |
| **McGill Billboard** | expert chord annotations | 1000 songs | chord modelling | research license |
| **Lakh MIDI (LMD)** | 176k MIDI files | huge | augmentation / pretraining | CC-BY 4.0 |
| **POP909** | 909 pop songs, melody+chords+arr. | 909 | train/eval | research use |

**Target representation.** Per-beat tokens: melody pitch-classes (+ contour) →
chord label (root + quality), transpose-augmented to all 12 keys.

## Guitar voicings / tab (Phase 4 arrangement)

| Dataset | Content | Use | License |
|---------|---------|-----|---------|
| **GuitarSet** | 360 recordings w/ string/fret annotations | voicings, fingering | MIT |
| **DadaGP** | 26k tokenized GuitarPro songs | tab/voicing modelling | research use |
| **mirdata** loaders | unified access to many of the above | tooling | BSD |

## Pitch / transcription benchmarking (Phase 2)

| Dataset | Use |
|---------|-----|
| **MIR-1K**, **MedleyDB** | melody-extraction ground truth |
| **GuitarSet** | note-transcription ground truth |
| *synthetic* (MIDI→audio) | controllable ground truth (built in `training/`) |

## Data pipeline (planned)

```
download_data.py  →  raw/           (per-source, with LICENSE notes)
preprocess.py     →  processed/     (tokenized melody/chord pairs)
                  →  splits/        (train / val / test, seeded)
```

A tiny committed **sample** (a handful of public-domain tunes) lets tests and
demos run without downloading gigabytes.
