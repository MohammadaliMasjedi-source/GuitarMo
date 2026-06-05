<div align="center">

# 🎸 GuitarMo

### Sing a melody → get a classical-guitar arrangement.

*Hum or sing into your laptop, pick a **style** and a **difficulty level**, and
GuitarMo transcribes your pitch, finds the key, harmonizes it, and plays it back
on a synthesized nylon-string guitar — with **tab**, **MIDI** and **sheet music**
to download.*

**Easy · Normal · Professional** &nbsp;|&nbsp; Classical · Flamenco · Folk · Bossa · Pop

![python](https://img.shields.io/badge/python-3.12-blue)
![status](https://img.shields.io/badge/status-Phase%201%20MVP%20complete-brightgreen)
![license](https://img.shields.io/badge/license-MIT-green)
![tests](https://img.shields.io/badge/tests-11%20passing-success)

</div>

---

## What it does

```
  🎤 your voice ──▶ pitch tracking ──▶ note transcription ──▶ key detection
                                                                   │
   guitar audio ◀── synthesis ◀── arrangement ◀── harmonization ◀──┘
   + tab + MIDI + MusicXML
```

You give it a sung melody (WAV). GuitarMo gives you back a complete,
**playable classical-guitar arrangement** at the difficulty you choose.

| Tier | Harmony | Texture |
|------|---------|---------|
| **Easy** | one diatonic triad per bar | bass + block chord |
| **Normal** | two chords/bar, diatonic 7ths, V at the cadence | fingerpicking / arpeggio |
| **Professional** | 7ths + 9th colours, **ii–V–I** cadence | dense arpeggios, voice-leading, counter-bass |

**Styles** change the rhythmic feel: `classical` (p-i-m-a arpeggios),
`flamenco` (rasgueado), `folk` (Travis alternating bass), `bossa` (syncopated
7th/9th comping), `pop_ballad` (slow open arpeggios).

## Quickstart

```bash
git clone https://github.com/MohammadaliMasjedi-source/GuitarMo.git
cd GuitarMo
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Web app (record straight from the browser)
```bash
python app.py        # then open the local URL it prints
```

### Command line
```bash
python -m guitarmo song.wav --style classical --level normal
python -m guitarmo --record 8 --style bossa --level professional
python -m guitarmo --list-styles
```

### Python API
```python
from guitarmo import process
res = process("humming.wav", style="classical", level="professional")
print(res.summary())     # key, tempo, chord progression
print(res.tab_text)      # ASCII tablature
# res.wav_path / res.midi_path / res.musicxml_path are written to disk
```

### Try it with no microphone
```bash
python examples/make_example.py   # synthesizes "Twinkle Twinkle" and arranges it
```

## How it works

GuitarMo is a transparent, **dependency-light** pipeline (no soundfonts, no
external binaries — the guitar is synthesized with Karplus–Strong):

| Stage | Module | Method |
|-------|--------|--------|
| Pitch tracking | `guitarmo/pitch.py` | pYIN (Mauch & Dixon 2014) via librosa |
| Transcription | `guitarmo/transcribe.py` | note segmentation + beat quantization |
| Key detection | `guitarmo/key.py` | Krumhansl–Schmuckler profiles |
| Harmonization | `guitarmo/harmony.py` | rule-based functional harmony (3 tiers) |
| Styles | `guitarmo/styles.py` | rhythmic accompaniment templates |
| Arrangement | `guitarmo/arrange.py` | DP fingering + chord voicings |
| Synthesis | `guitarmo/render.py` | Karplus–Strong plucked string + reverb |
| Notation | `guitarmo/notation.py` | ASCII tab · MIDI · MusicXML |

See **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for the full design and
**[docs/RESEARCH.md](docs/RESEARCH.md)** for the literature this is built on.

## Project plan & progress

This is a **phased, research-grade** project. Track it here:

- 🗺️ **[docs/ROADMAP.md](docs/ROADMAP.md)** — all phases at a glance
- ✅ **[docs/PROGRESS.md](docs/PROGRESS.md)** — live progress tracker (per phase / sub-phase, with Definition of Done)
- 🌟 **[docs/VISION_AND_QUALITY.md](docs/VISION_AND_QUALITY.md)** — the plan to make it paper-, presentation- & career-grade
- 📂 **[docs/phases/](docs/phases/)** — one document per phase
- 🗃️ **[docs/tasks/](docs/tasks/)** — one card per task
- 🔬 **[docs/RESEARCH.md](docs/RESEARCH.md)** — cited literature review
- 🧩 **[docs/ENGINES.md](docs/ENGINES.md)** — open-source engines we build on
- 📊 **[docs/DATASETS.md](docs/DATASETS.md)** — data for the trainable models

### 📺 Live dashboard & auto-sync
- **`Dashboard.bat`** → a live dashboard (phases, progress rings, task board) that
  bakes the **local** repo state and pulls **online** GitHub activity live
  (auto-refreshing). See [dashboard/](dashboard/).
- **`Sync.bat`** → regenerates task cards, `PROGRESS.md`, the dashboard and the
  Obsidian note from the single source of truth (`project_plan.py`), then commits
  & pushes **only when something changed**. Schedule it with
  `tools/install_schedule.ps1` for hands-off updates.

**Current status:** Phase 0 & 1 (rule-based MVP) complete and tested.
Next: Phase 2 (pitch accuracy with CREPE/basic-pitch) and Phase 3 (a *trained*
neural harmonizer).

## Repository layout

```
GuitarMo/
├── guitarmo/            # the engine (Python package)
├── app.py               # Gradio web app
├── project_plan.py      # single source of truth (phases, tasks, DoD, status)
├── Dashboard.bat        # build + open the live dashboard
├── Sync.bat             # regenerate docs/Obsidian/dashboard + push if changed
├── dashboard/           # live dashboard builder
├── tools/               # sync.py, update_obsidian.py, scheduler installer
├── examples/            # demo generator + sample audio + outputs
├── tests/               # pytest suite
├── training/            # scaffold for the trainable models (Phase 3+)
├── docs/                # roadmap, phases, tasks, research, datasets, vision
├── requirements.txt
└── pyproject.toml
```

## Status of the outputs

- ✅ **Audio** (WAV) — Karplus–Strong nylon-string render
- ✅ **MIDI** — General-MIDI nylon guitar
- ✅ **ASCII tab** — 6-line tablature
- ✅ **MusicXML** — opens in MuseScore / any notation editor
- 🔜 **PDF score & in-browser tab** (Phase 5)

## License

MIT — see [LICENSE](LICENSE).

## Acknowledgements

Built on the shoulders of open-source MIR: **librosa**, **music21**,
**pretty_midi**, **Gradio**, and the research cited in
[docs/RESEARCH.md](docs/RESEARCH.md).
