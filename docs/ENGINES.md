# 🧩 GuitarMo — Open-Source Engines

GuitarMo deliberately builds on best-in-class open-source MIR engines rather than
reinventing them. The **base install** stays light and binary-free; heavier
engines are **optional extras** (`requirements-ml.txt`) loaded behind pluggable
interfaces.

## In use now (Phase 1)

| Engine | Role | License | Notes |
|--------|------|---------|-------|
| [librosa](https://librosa.org) | pYIN f0, beat/tempo, chroma | ISC | core front-end |
| [music21](https://web.mit.edu/music21/) | MusicXML export, theory | BSD | notation only |
| [pretty_midi](https://github.com/craffel/pretty-midi) | MIDI export | MIT | GM nylon guitar |
| [Gradio](https://gradio.app) | web UI | Apache-2.0 | record/upload |
| NumPy / SciPy | DSP, Karplus–Strong, reverb | BSD | synthesis |

## Planned integrations

### Phase 2 — pitch & rhythm
| Engine | Role | License |
|--------|------|---------|
| [CREPE](https://github.com/marl/crepe) / [torchcrepe](https://github.com/maxrmorrison/torchcrepe) | deep f0 estimation | MIT |
| [basic-pitch](https://github.com/spotify/basic-pitch) (Spotify) | note-level transcription | Apache-2.0 |
| [madmom](https://github.com/CPJKU/madmom) | onsets / beats / meter | BSD (academic use) |
| [mir_eval](https://github.com/craffel/mir_eval) | transcription metrics | MIT |

### Phase 3 — harmonization (trained)
| Engine | Role | License |
|--------|------|---------|
| [PyTorch](https://pytorch.org) | train the neural harmonizer | BSD |
| [hmmlearn](https://github.com/hmmlearn/hmmlearn) | MySong-style HMM baseline | BSD |
| [Hugging Face Hub](https://huggingface.co) | host trained weights | — |

### Phase 4–5 — arrangement, synthesis, app
| Engine | Role | License |
|--------|------|---------|
| [fluidsynth](https://www.fluidsynth.org) + a nylon SF2 | optional hi-fi synth | LGPL |
| [alphaTab](https://alphatab.net) / [VexFlow](https://vexflow.com) | in-browser tab/score | MPL / MIT |
| [LilyPond](https://lilypond.org) / MuseScore CLI | PDF score export | GPL |

## Integration policy

- **Optional & pluggable.** Each engine sits behind an interface
  (`PitchBackend`, `Harmonizer`, `Synth`) with a pure-Python fallback, so a
  minimal `pip install -r requirements.txt` always works.
- **License hygiene.** Engines are dependencies, not vendored code; their
  licenses are recorded here. GPL/LGPL tools (fluidsynth, LilyPond) are used as
  external processes, never linked into the package.
- **Reproducibility.** Pinned versions live in `requirements*.txt`; model
  weights are versioned via releases / HF Hub.
