"""Lightweight music-theory helpers: pitch classes, chords, scales.

Kept deliberately dependency-free (pure Python) so it is easy to test and reason
about. The heavier theory in :mod:`music21` is only used for notation export.
"""
from __future__ import annotations

NOTE_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

MAJOR_STEPS = (0, 2, 4, 5, 7, 9, 11)
NATURAL_MINOR_STEPS = (0, 2, 3, 5, 7, 8, 10)

# Interval content (semitones above the root) for each supported chord quality.
CHORD_INTERVALS = {
    "maj":  (0, 4, 7),
    "min":  (0, 3, 7),
    "dim":  (0, 3, 6),
    "aug":  (0, 4, 8),
    "sus2": (0, 2, 7),
    "sus4": (0, 5, 7),
    "maj7": (0, 4, 7, 11),
    "min7": (0, 3, 7, 10),
    "dom7": (0, 4, 7, 10),
    "dim7": (0, 3, 6, 9),
    "m7b5": (0, 3, 6, 10),
    "add9": (0, 4, 7, 14),
    "maj9": (0, 4, 7, 11, 14),
    "min9": (0, 3, 7, 10, 14),
}

# Human-readable suffixes used when labelling chords (e.g. "C", "Am", "G7").
QUALITY_SUFFIX = {
    "maj": "", "min": "m", "dim": "dim", "aug": "aug",
    "sus2": "sus2", "sus4": "sus4",
    "maj7": "maj7", "min7": "m7", "dom7": "7", "dim7": "dim7",
    "m7b5": "m7b5", "add9": "add9", "maj9": "maj9", "min9": "m9",
}


def pc(midi: int) -> int:
    """Pitch class (0-11) of a MIDI note."""
    return midi % 12


def midi_to_name(midi: int) -> str:
    """e.g. 60 -> 'C4'."""
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"


def name_to_pc(name: str) -> int:
    return NOTE_NAMES.index(name)


def chord_pcs(root_pc: int, quality: str) -> tuple:
    """Pitch classes contained in a chord."""
    return tuple((root_pc + iv) % 12 for iv in CHORD_INTERVALS[quality])


def chord_label(root_pc: int, quality: str) -> str:
    return f"{NOTE_NAMES[root_pc % 12]}{QUALITY_SUFFIX.get(quality, quality)}"


def scale_pcs(tonic_pc: int, mode: str) -> tuple:
    steps = MAJOR_STEPS if mode == "major" else NATURAL_MINOR_STEPS
    return tuple((tonic_pc + s) % 12 for s in steps)
