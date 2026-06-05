# Phase 0 — Foundation & Setup ✅

**Goal.** A clean, reproducible Python project with the core data model and
music-theory primitives every later phase depends on.

**Status:** ✅ Complete · **Depends on:** — · **Feeds:** all phases

---

## Sub-phases

### 0.1 Repo scaffold & environment
- Tasks: create package layout, virtualenv, `requirements.txt`, `.gitignore`,
  `pyproject.toml`.
- **DoD:** `python -m venv` + `pip install -r requirements.txt` succeed on a
  clean machine; `import guitarmo` works.

### 0.2 Core data model
- Tasks: `Note`, `Melody`, `ChordSpan`, `PluckEvent`, `STANDARD_TUNING`
  (`guitarmo/core.py`). Beats-based timing convention.
- **DoD:** dataclasses importable, documented, used by every stage.

### 0.3 Music-theory utilities
- Tasks: pitch classes, scales, chord interval tables, chord labelling
  (`guitarmo/theory.py`).
- **DoD:** `chord_pcs`, `chord_label`, `scale_pcs` unit-tested.

## Risks & decisions
- **Decision:** keep theory pure-Python (no music21 in the hot path) for speed
  and testability; music21 is used only for notation export.
- **Decision:** all timing in *beats* upstream; seconds derived from tempo only
  at render/MIDI time — keeps quantization and arrangement tempo-independent.

## Definition of Done (phase)
- [x] Repo builds and imports.
- [x] Core types and theory helpers in place and tested.
