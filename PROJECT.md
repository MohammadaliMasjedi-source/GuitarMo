# 🎸 GuitarMo
> Sing → classical-guitar transcription.

**Status:** active · **Priority:** med · **Progress:** computed from phases · **Private:** no
**Links:** [GitHub](https://github.com/MohammadaliMasjedi-source/GuitarMo) · Dashboard (n/a) · Board (n/a) · Obsidian (n/a) · [Docs](PROJECT.md)

> This file is the human-readable companion to `.mc/project.json` (the machine-readable source of
> truth that Mission Control and this project's dashboard both read). Keep the two roughly in sync.

## Vision
GuitarMo turns a sung or hummed melody into a complete, playable classical-guitar arrangement. It
tracks pitch, infers the key, harmonizes the melody at three difficulty tiers and several styles, then
synthesizes a nylon-string guitar and exports tab, MIDI and MusicXML. It is built as a transparent,
research-grade pipeline that ships a working rule-based baseline first and progressively swaps in
state-of-the-art open-source engines and trained models.

## Phases
### Phase 1 — Foundation & rule-based MVP  ✅ 100%
- [x] Repo scaffold, data model & music-theory utilities
- [x] Pitch tracking + transcription (pYIN) and key detection
- [x] Rule-based 3-tier harmonizer + style engine
- [x] Guitar arranger + Karplus–Strong synthesis
- [x] Notation export (ASCII tab / MIDI / MusicXML)
- [x] CLI + Gradio web app, pytest suite & demo

### Phase 2 — Pitch accuracy & data-driven harmonization  🔵 ~17%  ← current
- [x] Pluggable pitch backends + CREPE (pYIN fallback)
- [ ] basic-pitch backend behind same interface   ← next action
- [ ] Onset / beat / meter accuracy + robustness
- [ ] Evaluation harness comparing backends
- [ ] Train neural harmonizer, beat rule-based baseline
- [ ] Integrate ML harmonizer as optional backend

### Phase 3 — Expressive arrangement & synthesis  ⚪ 0%
- [ ] Optimal fingering solver
- [ ] Data-driven voicings / idiomatic tab
- [ ] Counter-melody / walking bass
- [ ] Expression (ornaments / dynamics)
- [ ] Optional hi-fi synthesis backend

### Phase 4 — App, export, evaluation & release  ⚪ 0%
- [ ] Web app polish + synced playback
- [ ] In-browser notation + PDF export
- [ ] Deploy hosted demo + pip install + CI
- [ ] Evaluation, user study & reproducibility
- [ ] Write-up and tagged v1.0 release

*(Mark phases ✅ when 100%, 🔵 when active, ⚪ when not started.)*

## Approach
A dependency-light Python pipeline: pYIN pitch tracking (librosa) → note segmentation & beat
quantization → Krumhansl–Schmuckler key detection → rule-based functional harmony (3 tiers) →
style accompaniment templates → DP fingering / chord voicings → Karplus–Strong synthesis →
ASCII tab / MIDI / MusicXML export. Interfaces are a CLI (`python -m guitarmo`) and a Gradio web
app (`app.py`). The roadmap progressively replaces heuristics with open-source engines (CREPE,
basic-pitch, madmom) and a trained neural harmonizer (MySong/DeepBach lineage).

## Decisions (log)
| Date | Decision | Why | Rejected alternatives |
|------|----------|-----|-----------------------|
| 2026-06-05 | Ship a transparent rule-based MVP first, then progressively add trained models | Immediately useful baseline + reference to measure learned components | ML-first approach |
| 2026-06-05 | Synthesize guitar with Karplus–Strong instead of soundfonts | Keeps the pipeline dependency-light, no external binaries | soundfont / sf2 synthesis |

## SWOT
- **Strengths** — Unique sing→classical-guitar angle; working, tested end-to-end MVP; transparent, dependency-light pipeline.
- **Weaknesses** — Heuristic pitch/harmony, no trained models yet; no hosted demo or packaging; Windows-centric tooling.
- **Opportunities** — Music-education market; plug in SOTA MIR engines; research-grade write-up / paper.
- **Threats** — Established transcription apps; high quality bar for real sung input.

## Stats
Phases 0–1 (rule-based MVP) complete · Phase 2 started (pluggable pitch backends) · 22 tests passing.
