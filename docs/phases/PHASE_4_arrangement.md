# Phase 4 — Expressive Guitar Arrangement ⬜

**Goal.** Make the guitar writing *idiomatic, playable and musical* — optimal
fingering, learned voicings, independent inner voices, ornaments, and
higher-fidelity synthesis.

**Status:** ⬜ Planned · **Depends on:** Phase 3 · **Feeds:** Phase 5/6

---

## Sub-phases

### 4.1 Optimal fingering (full fretboard solver)
- Graph/DP over the *joint* melody+chord stream with a real playability cost
  (hand span, position shifts, open strings) — Sayegh (1989), Radicioni et al.
  (2004). Removes the current 2-string melody fold.
- **DoD:** fewer position shifts and wider melodic range than the Phase-1 heuristic.

### 4.2 Data-driven voicings & tab
- Learn idiomatic chord voicings/fingerings from **GuitarSet** (Xi et al. 2018)
  and **DadaGP** (Sarmento et al. 2021).
- **DoD:** voicings sampled from data look idiomatic to a guitarist.

### 4.3 Counter-melody & walking bass (pro tier)
- Generate an independent inner/bass voice with voice-leading at the pro level.
- **DoD:** audibly independent second voice at `professional`.

### 4.4 Expression: ornaments, dynamics, rubato
- Per-style idioms (rasgueado bursts, Travis independence), cadential ritardando,
  velocity shaping.
- **DoD:** blind listeners rate renders as more musical than Phase 1.

### 4.5 Higher-fidelity synthesis (optional)
- Optional physical-model or soundfont (fluidsynth) backend; keep Karplus–Strong
  as the zero-dependency default.
- **DoD:** an optional `--synth sf2|ks` switch with better audio.

## Definition of Done (phase)
- [ ] Optimal fingering solver replaces the heuristic.
- [ ] Idiomatic, data-informed voicings.
- [ ] Pro tier has a real counter-voice; renders are more expressive.
