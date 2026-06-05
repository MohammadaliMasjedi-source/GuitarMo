"""Single source of truth for the GuitarMo project plan.

Phases, sub-phases, Definition of Done and status all live here. The task cards
(docs/tasks/), the live dashboard (dashboard/) and the Obsidian note all derive
from this module, so the plan is described in exactly one place.

Update statuses / DoD here, then run `Sync.bat` (or tools/sync.py) to propagate
everywhere and push.
"""
from __future__ import annotations

DONE, NEXT, TODO = "done", "next", "todo"
EMOJI = {DONE: "✅", NEXT: "🔜", TODO: "⬜"}
STATUS_LABEL = {DONE: "Done", NEXT: "Next up", TODO: "Planned"}
# fraction of a task counted as complete for progress maths
STATUS_WEIGHT = {DONE: 1.0, NEXT: 0.15, TODO: 0.0}

META = {
    "name": "GuitarMo",
    "emoji": "🎸",
    "tagline": "Sing a melody → get a classical-guitar arrangement.",
    "owner": "MohammadaliMasjedi-source",
    "repo": "GuitarMo",
    "repo_url": "https://github.com/MohammadaliMasjedi-source/GuitarMo",
    "local_path": r"D:\Mo.MassJedi\Cadenza",
    "obsidian_note": r"C:\Users\mmasjedi\OneDrive\Synotic\10 Projects\GuitarMo.md",
}

PHASES = [
    {"num": 0, "title": "Foundation & Setup", "status": DONE,
     "file": "PHASE_0_foundation.md",
     "goal": "A clean, reproducible project with the core data model and theory.",
     "tasks": [
        {"id": "0.1", "title": "Repo scaffold & environment", "status": DONE,
         "objective": "Stand up a clean, reproducible Python project.",
         "steps": ["Package layout + venv", "requirements / pyproject", ".gitignore"],
         "dod": ["pip install succeeds clean", "import guitarmo works"]},
        {"id": "0.2", "title": "Core data model", "status": DONE,
         "objective": "Define the dataclasses every stage shares.",
         "steps": ["Note/Melody/ChordSpan/PluckEvent", "Tuning constants",
                   "Beats-based timing"],
         "dod": ["Types importable + documented", "Used across pipeline"]},
        {"id": "0.3", "title": "Music-theory utilities", "status": DONE,
         "objective": "Pure-Python pitch/chord/scale helpers.",
         "steps": ["Pitch classes & names", "Chord tables + labels", "Scales"],
         "dod": ["chord_pcs/chord_label/scale_pcs tested"]},
     ]},
    {"num": 1, "title": "MVP Engine", "status": DONE,
     "file": "PHASE_1_mvp.md",
     "goal": "Complete rule-based sing→guitar pipeline, end to end, tested.",
     "tasks": [
        {"id": "1.1", "title": "Pitch tracking & transcription", "status": DONE,
         "objective": "WAV -> quantized monophonic melody.",
         "steps": ["pYIN f0", "Note segmentation", "Tempo + quantization"],
         "dod": ["A WAV yields a clean Melody"]},
        {"id": "1.2", "title": "Key detection", "status": DONE,
         "objective": "Estimate key from the note stream.",
         "steps": ["Duration-weighted PC histogram", "Correlate vs KK profiles"],
         "dod": ["C-major & A-minor fixtures pass"]},
        {"id": "1.3", "title": "Rule-based harmonizer (3 tiers)", "status": DONE,
         "objective": "Functional harmony scaled by difficulty.",
         "steps": ["Diatonic scoring", "Cadence logic", "9th colours at pro"],
         "dod": ["Covers melody, cadences on tonic", "Pro uses 7ths/9ths"]},
        {"id": "1.4", "title": "Style engine", "status": DONE,
         "objective": "Rhythmic accompaniment templates.",
         "steps": ["5 styles x 3 levels", "Tiled cell patterns"],
         "dod": ["Every style x level emits a pattern"]},
        {"id": "1.5", "title": "Guitar arranger", "status": DONE,
         "objective": "Map melody+chords to a playable fretboard.",
         "steps": ["DP fingering", "Chord voicings", "Register separation"],
         "dod": ["Frets 0-12, valid strings, valid tab"]},
        {"id": "1.6", "title": "Synthesis", "status": DONE,
         "objective": "Render plucked-string audio, no binaries.",
         "steps": ["Karplus-Strong", "Envelope", "Reverb"],
         "dod": ["Finite audio normalised to 0.9 peak"]},
        {"id": "1.7", "title": "Notation export", "status": DONE,
         "objective": "Write tab, MIDI and MusicXML.",
         "steps": ["ASCII tab", "GM nylon MIDI", "MusicXML"],
         "dod": ["All three outputs openable"]},
        {"id": "1.8", "title": "Interfaces (CLI + web)", "status": DONE,
         "objective": "Make it usable.",
         "steps": ["argparse CLI + --record", "Gradio app"],
         "dod": ["app.py and python -m guitarmo both run"]},
        {"id": "1.9", "title": "Tests & demo", "status": DONE,
         "objective": "Lock in correctness.",
         "steps": ["pytest unit + e2e", "Mic-free example generator"],
         "dod": ["pytest green", "make_example.py runs e2e"]},
     ]},
    {"num": 2, "title": "Pitch & Rhythm Accuracy", "status": NEXT,
     "file": "PHASE_2_pitch_accuracy.md",
     "goal": "Swap heuristics for SOTA open-source engines, proven by benchmark.",
     "tasks": [
        {"id": "2.1", "title": "Pluggable pitch backends + CREPE", "status": NEXT,
         "objective": "Add a backend interface and CREPE.",
         "steps": ["PitchBackend interface", "CREPE backend", "--pitch switch"],
         "dod": ["crepe|pyin switchable", "CREPE optional; pYIN fallback"]},
        {"id": "2.2", "title": "basic-pitch backend", "status": TODO,
         "objective": "Add Spotify note-level transcription.",
         "steps": ["Wrap basic-pitch", "Map to Melody", "Document trade-offs"],
         "dod": ["Same interface yields a Melody"]},
        {"id": "2.3", "title": "Onset / beat / meter", "status": TODO,
         "objective": "Better rhythm via madmom.",
         "steps": ["madmom onsets/beats", "Meter estimate", "librosa fallback"],
         "dod": ["Lower tempo/onset error on benchmark"]},
        {"id": "2.4", "title": "Input robustness", "status": TODO,
         "objective": "Handle messy real input.",
         "steps": ["Filter/gate/normalize", "hum vs whistle", "Helpful errors"],
         "dod": ["Noisy/clipped inputs handled gracefully"]},
        {"id": "2.5", "title": "Evaluation harness", "status": TODO,
         "objective": "Measure accuracy objectively.",
         "steps": ["Synthetic ground truth", "mir_eval", "Per-backend report"],
         "dod": ["python -m guitarmo.eval compares backends"]},
     ]},
    {"num": 3, "title": "Data-Driven Harmonization (TRAIN)", "status": TODO,
     "file": "PHASE_3_harmonization_ml.md",
     "goal": "Train a neural harmonizer on data (MySong/DeepBach lineage), RTX-3090.",
     "tasks": [
        {"id": "3.1", "title": "Dataset acquisition", "status": TODO,
         "objective": "Get melody+chord corpora.",
         "steps": ["Download scripts", "Record licenses", "Cache sample"],
         "dod": ["Scripts run; sample cached; licenses noted"]},
        {"id": "3.2", "title": "Preprocessing & representation", "status": TODO,
         "objective": "Tokenize melody->chord with splits.",
         "steps": ["Per-beat tokens", "Transpose augment", "Seeded splits"],
         "dod": ["Deterministic dataset from config"]},
        {"id": "3.3", "title": "HMM baseline (MySong)", "status": TODO,
         "objective": "Fast explainable baseline.",
         "steps": ["HMM (hmmlearn)", "Train + decode"],
         "dod": ["Baseline chord-accuracy reported"]},
        {"id": "3.4", "title": "Neural harmonizer (TRAIN)", "status": TODO,
         "objective": "Train seq2seq melody->chords on RTX-3090.",
         "steps": ["Transformer/BiLSTM", "Style+difficulty conditioning", "Train"],
         "dod": ["Trained weights + curves", "Inference < 1s/song"]},
        {"id": "3.5", "title": "Evaluation & A/B", "status": TODO,
         "objective": "Prove it beats the rules.",
         "steps": ["Chord metrics", "Blind A/B vs rules"],
         "dod": ["Beats rule-based on held-out set"]},
        {"id": "3.6", "title": "Integrate as optional backend", "status": TODO,
         "objective": "Wire model into the pipeline.",
         "steps": ["--harmonizer ml|rules", "Ship weights"],
         "dod": ["ml backend works e2e; rules still default"]},
     ]},
    {"num": 4, "title": "Expressive Arrangement", "status": TODO,
     "file": "PHASE_4_arrangement.md",
     "goal": "Idiomatic, playable, musical guitar writing.",
     "tasks": [
        {"id": "4.1", "title": "Optimal fingering solver", "status": TODO,
         "objective": "Full fretboard graph DP.",
         "steps": ["Joint stream", "Playability cost", "Remove 2-string fold"],
         "dod": ["Fewer shifts, wider range"]},
        {"id": "4.2", "title": "Data-driven voicings/tab", "status": TODO,
         "objective": "Learn idiomatic voicings.",
         "steps": ["GuitarSet/DadaGP", "Sample voicings"],
         "dod": ["Voicings look idiomatic"]},
        {"id": "4.3", "title": "Counter-melody / walking bass", "status": TODO,
         "objective": "Independent voice at pro.",
         "steps": ["Inner-voice generation", "Voice-leading"],
         "dod": ["Audible second voice at professional"]},
        {"id": "4.4", "title": "Expression (ornaments/dynamics)", "status": TODO,
         "objective": "Make renders musical.",
         "steps": ["Style idioms", "Rubato", "Velocity shaping"],
         "dod": ["Blind listeners prefer over Phase 1"]},
        {"id": "4.5", "title": "Hi-fi synthesis (optional)", "status": TODO,
         "objective": "Optional better audio.",
         "steps": ["fluidsynth/SF2 or physical model", "--synth switch"],
         "dod": ["Optional sf2|ks backend; KS default"]},
     ]},
    {"num": 5, "title": "App, UX & Deployment", "status": TODO,
     "file": "PHASE_5_app_deploy.md",
     "goal": "A polished, hosted product anyone can use from a browser/phone.",
     "tasks": [
        {"id": "5.1", "title": "Web app polish", "status": TODO,
         "objective": "Visual feedback.",
         "steps": ["Waveform + pitch overlay", "Piano-roll", "Live key/tempo"],
         "dod": ["Users see what was heard"]},
        {"id": "5.2", "title": "In-browser notation + PDF", "status": TODO,
         "objective": "Real score rendering.",
         "steps": ["alphaTab/VexFlow", "PDF export", "GuitarPro export"],
         "dod": ["Rendered notation + PDF"]},
        {"id": "5.3", "title": "Synced playback", "status": TODO,
         "objective": "Play-along.",
         "steps": ["Note highlight", "Tempo/transpose"],
         "dod": ["Synchronized audio + notation"]},
        {"id": "5.4", "title": "Deploy & package", "status": TODO,
         "objective": "Ship it.",
         "steps": ["HF Spaces / Docker", "PyPI guitarmo", "CI"],
         "dod": ["Public URL + pip install + green CI"]},
        {"id": "5.5", "title": "Mobile / iPod capture", "status": TODO,
         "objective": "Capture from a phone.",
         "steps": ["Mobile UI", "Phone mic formats"],
         "dod": ["Works from a phone browser"]},
     ]},
    {"num": 6, "title": "Evaluation & Release", "status": TODO,
     "file": "PHASE_6_release.md",
     "goal": "Measure it, make it reproducible, write it up, ship v1.0.",
     "tasks": [
        {"id": "6.1", "title": "Evaluation + user study", "status": TODO,
         "objective": "Measure quality.",
         "steps": ["Objective metrics", "Listening/usability study"],
         "dod": ["Metrics + survey reported"]},
        {"id": "6.2", "title": "Reproducibility", "status": TODO,
         "objective": "Make it repeatable.",
         "steps": ["Configs/seeds/model cards", "Manifests"],
         "dod": ["Fresh machine reproduces model + figures"]},
        {"id": "6.3", "title": "Write-up", "status": TODO,
         "objective": "Communicate it.",
         "steps": ["Report/blog/paper draft", "Diagrams"],
         "dod": ["Shareable document"]},
        {"id": "6.4", "title": "Release v1.0", "status": TODO,
         "objective": "Tag the milestone.",
         "steps": ["CHANGELOG + CITATION", "SemVer tag", "Archive"],
         "dod": ["v1.0.0 tagged"]},
     ]},
]


def all_tasks():
    for ph in PHASES:
        for t in ph["tasks"]:
            yield ph, t


def phase_progress(ph):
    tasks = ph["tasks"]
    if not tasks:
        return 0.0
    return sum(STATUS_WEIGHT[t["status"]] for t in tasks) / len(tasks)


def overall_progress():
    tasks = [t for _, t in all_tasks()]
    if not tasks:
        return 0.0
    return sum(STATUS_WEIGHT[t["status"]] for t in tasks) / len(tasks)


def counts():
    c = {DONE: 0, NEXT: 0, TODO: 0}
    for _, t in all_tasks():
        c[t["status"]] += 1
    return c


def to_dict():
    """JSON-serialisable snapshot of the plan (for the dashboard)."""
    return {
        "meta": META,
        "overall": round(overall_progress() * 100, 1),
        "counts": counts(),
        "phases": [
            {"num": ph["num"], "title": ph["title"], "status": ph["status"],
             "goal": ph["goal"], "file": ph["file"],
             "progress": round(phase_progress(ph) * 100, 1),
             "tasks": ph["tasks"]}
            for ph in PHASES
        ],
    }
