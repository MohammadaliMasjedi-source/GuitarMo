"""Generate one Markdown task card per sub-phase into docs/tasks/.

Docs-as-code: edit the SPEC below and re-run to regenerate all cards + index.

    python docs/generate_task_cards.py
"""
from __future__ import annotations

import os

DONE, NEXT, TODO = "done", "next", "todo"
EMOJI = {DONE: "✅", NEXT: "🔜", TODO: "⬜"}

# phase_num: (phase_title, phase_file, [ (id, title, status, objective, steps, dod) ])
SPEC = {
    0: ("Foundation & Setup", "PHASE_0_foundation.md", [
        ("0.1", "Repo scaffold & environment", DONE,
         "Stand up a clean, reproducible Python project.",
         ["Package layout + venv", "requirements.txt / pyproject.toml", ".gitignore"],
         ["pip install succeeds on a clean machine", "import guitarmo works"]),
        ("0.2", "Core data model", DONE,
         "Define the dataclasses every stage shares.",
         ["Note / Melody / ChordSpan / PluckEvent", "Standard tuning constants",
          "Beats-based timing convention"],
         ["Types importable and documented", "Used across the pipeline"]),
        ("0.3", "Music-theory utilities", DONE,
         "Pure-Python pitch/chord/scale helpers.",
         ["Pitch classes & note names", "Chord interval tables + labels",
          "Scale builders"],
         ["chord_pcs / chord_label / scale_pcs unit-tested"]),
    ]),
    1: ("MVP Engine", "PHASE_1_mvp.md", [
        ("1.1", "Pitch tracking & transcription", DONE,
         "WAV -> quantized monophonic melody.",
         ["pYIN f0", "Note segmentation w/ gap tolerance", "Tempo + beat quantization"],
         ["A WAV yields a clean Melody"]),
        ("1.2", "Key detection", DONE,
         "Estimate key from the note stream.",
         ["Duration-weighted PC histogram", "Correlate vs 24 KK profiles"],
         ["C-major and A-minor fixtures pass"]),
        ("1.3", "Rule-based harmonizer (3 tiers)", DONE,
         "Functional harmony scaled by difficulty.",
         ["Diatonic candidate scoring", "Cadence logic (V, ii-V-I)",
          "9th colours at pro"],
         ["Covers melody, cadences on tonic", "Pro uses 7ths/9ths"]),
        ("1.4", "Style engine", DONE,
         "Rhythmic accompaniment templates.",
         ["5 styles x 3 levels", "Tiled cell patterns"],
         ["Every style x level emits a pattern"]),
        ("1.5", "Guitar arranger", DONE,
         "Map melody+chords to a playable fretboard.",
         ["DP melody fingering", "Chord voicings on bass strings",
          "Register separation"],
         ["Frets 0-12, valid strings, valid tab"]),
        ("1.6", "Synthesis", DONE,
         "Render plucked-string audio with no binaries.",
         ["Karplus-Strong (vectorized)", "Attack/release envelope", "Light reverb"],
         ["Finite audio normalised to 0.9 peak"]),
        ("1.7", "Notation export", DONE,
         "Write tab, MIDI and MusicXML.",
         ["ASCII 6-line tab", "GM nylon MIDI", "music21 MusicXML"],
         ["All three outputs written and openable"]),
        ("1.8", "Interfaces (CLI + web)", DONE,
         "Make it usable.",
         ["argparse CLI + --record", "Gradio app (record/upload)"],
         ["python app.py and python -m guitarmo both run"]),
        ("1.9", "Tests & demo", DONE,
         "Lock in correctness.",
         ["pytest unit + e2e", "Microphone-free example generator"],
         ["pytest green", "make_example.py runs end-to-end"]),
    ]),
    2: ("Pitch & Rhythm Accuracy", "PHASE_2_pitch_accuracy.md", [
        ("2.1", "Pluggable pitch backends + CREPE", NEXT,
         "Add a backend interface and CREPE.",
         ["PitchBackend interface", "CREPE/torchcrepe backend", "--pitch switch"],
         ["crepe|pyin switchable", "CREPE optional; pYIN fallback"]),
        ("2.2", "basic-pitch backend", TODO,
         "Add Spotify note-level transcription.",
         ["Wrap basic-pitch", "Map to Melody", "Document trade-offs"],
         ["Same interface yields a Melody"]),
        ("2.3", "Onset / beat / meter", TODO,
         "Better rhythm via madmom.",
         ["madmom onsets/beats", "Meter estimate", "librosa fallback"],
         ["Lower tempo/onset error on benchmark"]),
        ("2.4", "Input robustness", TODO,
         "Handle messy real input.",
         ["HP filter / noise gate / normalize", "hum vs whistle detect",
          "Helpful errors"],
         ["Noisy/clipped inputs handled gracefully"]),
        ("2.5", "Evaluation harness", TODO,
         "Measure accuracy objectively.",
         ["Synthetic ground truth", "mir_eval metrics", "Per-backend report"],
         ["python -m guitarmo.eval compares backends"]),
    ]),
    3: ("Data-Driven Harmonization (TRAIN)", "PHASE_3_harmonization_ml.md", [
        ("3.1", "Dataset acquisition", TODO,
         "Get melody+chord corpora.",
         ["Download scripts (Nottingham, etc.)", "Record licenses",
          "Cache committed sample"],
         ["Scripts run; sample cached; licenses noted"]),
        ("3.2", "Preprocessing & representation", TODO,
         "Tokenize melody->chord with splits.",
         ["Per-beat tokens", "Transpose augment", "Seeded train/val/test"],
         ["Deterministic dataset built from config"]),
        ("3.3", "HMM baseline (MySong)", TODO,
         "Fast explainable baseline.",
         ["HMM (hmmlearn)", "Train + decode"],
         ["Baseline chord-accuracy reported"]),
        ("3.4", "Neural harmonizer (TRAIN)", TODO,
         "Train seq2seq melody->chords on RTX-3090.",
         ["Transformer/BiLSTM", "Style+difficulty conditioning",
          "Train + log curves"],
         ["Trained weights + curves", "Inference < 1s/song"]),
        ("3.5", "Evaluation & A/B", TODO,
         "Prove it beats the rules.",
         ["Chord metrics", "Blind A/B vs rules"],
         ["Beats rule-based on held-out set"]),
        ("3.6", "Integrate as optional backend", TODO,
         "Wire model into the pipeline.",
         ["--harmonizer ml|rules", "Ship weights (HF/release)"],
         ["ml backend works e2e; rules still default"]),
    ]),
    4: ("Expressive Arrangement", "PHASE_4_arrangement.md", [
        ("4.1", "Optimal fingering solver", TODO,
         "Full fretboard graph DP.",
         ["Joint melody+chord stream", "Playability cost", "Remove 2-string fold"],
         ["Fewer shifts, wider range than heuristic"]),
        ("4.2", "Data-driven voicings/tab", TODO,
         "Learn idiomatic voicings.",
         ["GuitarSet/DadaGP", "Sample voicings"],
         ["Voicings look idiomatic to a guitarist"]),
        ("4.3", "Counter-melody / walking bass", TODO,
         "Add an independent voice at pro.",
         ["Inner-voice generation", "Voice-leading"],
         ["Audible second voice at professional"]),
        ("4.4", "Expression (ornaments/dynamics)", TODO,
         "Make renders musical.",
         ["Style idioms", "Cadential rubato", "Velocity shaping"],
         ["Blind listeners prefer over Phase 1"]),
        ("4.5", "Hi-fi synthesis (optional)", TODO,
         "Optional better audio.",
         ["fluidsynth/SF2 or physical model", "--synth switch"],
         ["Optional sf2|ks backend; KS still default"]),
    ]),
    5: ("App, UX & Deployment", "PHASE_5_app_deploy.md", [
        ("5.1", "Web app polish", TODO,
         "Visual feedback.",
         ["Waveform + pitch overlay", "Piano-roll", "Live key/tempo"],
         ["Users see what was heard"]),
        ("5.2", "In-browser notation + PDF", TODO,
         "Real score rendering.",
         ["alphaTab/VexFlow", "PDF via LilyPond/MuseScore", "GuitarPro export"],
         ["Rendered notation + PDF download"]),
        ("5.3", "Synced playback", TODO,
         "Play-along.",
         ["Highlight notes", "Tempo/transpose controls"],
         ["Synchronized audio + notation"]),
        ("5.4", "Deploy & package", TODO,
         "Ship it.",
         ["HF Spaces / Docker", "PyPI guitarmo", "GitHub Actions CI"],
         ["Public URL + pip install + green CI"]),
        ("5.5", "Mobile / iPod capture", TODO,
         "Capture from a phone.",
         ["Mobile recording UI", "Phone mic formats"],
         ["Works end-to-end from a phone browser"]),
    ]),
    6: ("Evaluation & Release", "PHASE_6_release.md", [
        ("6.1", "Evaluation + user study", TODO,
         "Measure quality.",
         ["Objective metrics", "Blind listening / usability study"],
         ["Metrics + survey results reported"]),
        ("6.2", "Reproducibility", TODO,
         "Make it repeatable.",
         ["Configs/seeds/model cards", "Dataset manifests"],
         ["Fresh machine reproduces model + figures"]),
        ("6.3", "Write-up", TODO,
         "Communicate it.",
         ["Technical report / blog / paper draft", "Diagrams"],
         ["Shareable document"]),
        ("6.4", "Release v1.0", TODO,
         "Tag the milestone.",
         ["CHANGELOG + CITATION", "SemVer tag", "Archive demo + weights"],
         ["v1.0.0 tagged"]),
    ]),
}


def slug(title):
    keep = [c.lower() if c.isalnum() else "_" for c in title]
    s = "".join(keep)
    while "__" in s:
        s = s.replace("__", "_")
    return s.strip("_")


def card(phase_title, phase_file, tid, title, status, objective, steps, dod):
    box = "x" if status == DONE else " "
    lines = [f"# Task {tid} — {title}", "",
             f"**Phase:** {phase_title} · **Status:** {EMOJI[status]} "
             f"{ {DONE:'Done', NEXT:'Next up', TODO:'Planned'}[status] }", "",
             "## Objective", objective, "", "## Steps"]
    lines += [f"- [{box}] {s}" for s in steps]
    lines += ["", "## Definition of Done"]
    lines += [f"- [{box}] {d}" for d in dod]
    lines += ["", "## Links",
              f"- Phase: [../phases/{phase_file}](../phases/{phase_file})",
              "- Progress: [../PROGRESS.md](../PROGRESS.md)",
              "- Roadmap: [../ROADMAP.md](../ROADMAP.md)", ""]
    return "\n".join(lines)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "tasks")
    os.makedirs(out, exist_ok=True)
    index = ["# 🗃️ Task cards", "",
             "One card per sub-phase. Generated by `generate_task_cards.py`.", ""]
    for phase in sorted(SPEC):
        ptitle, pfile, tasks = SPEC[phase]
        index.append(f"## Phase {phase} — {ptitle}")
        for (tid, title, status, objective, steps, dod) in tasks:
            fname = f"T{tid.replace('.', '_')}_{slug(title)}.md"
            with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
                f.write(card(ptitle, pfile, tid, title, status,
                             objective, steps, dod))
            index.append(f"- {EMOJI[status]} [{tid} {title}]({fname})")
        index.append("")
    with open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index))
    n = sum(len(v[2]) for v in SPEC.values())
    print(f"generated {n} task cards + INDEX.md in {out}")


if __name__ == "__main__":
    main()
