# Phase 5 — App, UX & Deployment ⬜

**Goal.** Turn the engine into a polished, hosted product anyone can use from a
browser (including a phone / iPod), with proper score rendering and packaging.

**Status:** ⬜ Planned · **Depends on:** Phase 4 · **Feeds:** Phase 6

---

## Sub-phases

### 5.1 Web app polish
- Waveform + detected-pitch overlay, piano-roll of the transcription, live
  key/tempo readout, per-tier preview.
- **DoD:** users see visual feedback of what was heard.

### 5.2 In-browser notation + PDF
- Render real tab/score with **alphaTab** or **VexFlow**; export **PDF** (via
  LilyPond or MuseScore CLI) and GuitarPro (`.gp`).
- **DoD:** rendered notation in the page + downloadable PDF.

### 5.3 Synced playback
- Play-along with note highlighting; tempo/transpose controls.
- **DoD:** synchronized audio + notation playback.

### 5.4 Deployment & packaging
- **Hugging Face Spaces** / Docker image for the demo; publish `guitarmo` to
  **PyPI**; GitHub Actions CI (tests + build).
- **DoD:** public demo URL + `pip install guitarmo` + green CI.

### 5.5 Mobile / iPod capture
- Mobile-friendly recording UI; handle phone mic formats.
- **DoD:** works end to end from a phone browser.

## Definition of Done (phase)
- [ ] Hosted public demo.
- [ ] In-browser tab/score + PDF export.
- [ ] PyPI package + CI.
