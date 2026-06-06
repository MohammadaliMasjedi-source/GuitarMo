# GuitarMo (Cadenza) — notes for Claude

(Style rules live in the global `~/.claude/CLAUDE.md`. This file is only **facts about this project**.)

## What it is
Sing or hum a melody → it makes a playable **classical-guitar** arrangement, and exports tab, MIDI, and MusicXML.

## How it's built
- **Python** pipeline, dependency-light.
- Flow: pitch tracking (pYIN / librosa) → notes → key detection → rule-based harmony (3 tiers) → guitar arranger → Karplus–Strong synth → export.
- Main code is in `guitarmo/`. Web app is `app.py` (Gradio).

## How to run it
- CLI: `python -m guitarmo`
- Web app: `python app.py`
- Tests: `pytest`
- Dashboard: `Dashboard.bat`
- Install: `pip install -r requirements.txt` (ML extras: `requirements-ml.txt`)

## Good to know
- Phase 1 (rule-based MVP) is **done**. Now working on better pitch detection + an ML harmonizer.
- Public repo.
