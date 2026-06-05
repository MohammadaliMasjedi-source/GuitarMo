# Changelog

All notable changes to GuitarMo are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/);
versions follow [SemVer](https://semver.org/).

## [Unreleased]
- Phase 2: pluggable pitch backends (CREPE, basic-pitch), madmom beats, eval harness.
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
