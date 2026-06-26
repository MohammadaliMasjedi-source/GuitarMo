# Changelog

All notable changes to GuitarMo are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/);
versions follow [SemVer](https://semver.org/).

## [Unreleased]
### Added — Phase 2 (in progress)
- Pluggable pitch-backend layer (`guitarmo.pitch_backends`): a `PitchBackend`
  interface, a `PitchResult` return type, and a name-keyed registry.
- pYIN backend (default, always available) and a CREPE deep-CNN backend that
  lazily loads the optional `crepe`/`tensorflow` extras and transparently falls
  back to pYIN when they are not installed.
- `transcribe()` / `process()` take a `pitch_backend` argument; the CLI gains
  `--pitch-backend` and `--list-backends`; the web app gains a "Pitch engine"
  picker. 11 new tests (22 total).

### Planned
- Phase 2: basic-pitch backend, madmom beats, evaluation harness.
- Phase 3: trained neural harmonizer + HMM baseline.

## [0.1.0] — 2026-06-05
### Added — Phases 0 & 1 (rule-based MVP)
- Core data model and music-theory utilities.
- pYIN pitch tracking, note segmentation and beat quantization.
- Krumhansl–Schmuckler key detection.
- Rule-based harmonizer with three difficulty tiers (easy / normal / professional).
- Five accompaniment styles (classical, flamenco, folk, bossa, pop ballad).
- DP guitar fingering + chord voicings (melody on treble, harmony on bass strings).
- Karplus–Strong plucked-string synthesis + light reverb (no external binaries).
- Output exporters: ASCII tab, MIDI (GM nylon guitar), MusicXML.
- Gradio web app and `python -m guitarmo` CLI.
- pytest suite (11 tests) and a microphone-free example generator.
- Full phased project documentation (roadmap, phases, tasks, research, datasets).
