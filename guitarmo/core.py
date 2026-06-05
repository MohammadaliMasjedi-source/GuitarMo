"""Core data structures shared across the GuitarMo pipeline.

Timing convention: everything upstream of rendering is measured in *beats*.
Seconds are derived from the tempo only at render / MIDI export time.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

# Standard guitar tuning, 6th (low) string -> 1st (high) string, as MIDI numbers.
# E2 A2 D3 G3 B3 E4
STANDARD_TUNING = (40, 45, 50, 55, 59, 64)
STRING_NAMES = ("E", "A", "D", "G", "B", "e")  # index 0..5 == 6th..1st string


@dataclass
class Note:
    """A transcribed melody note. Timing is in beats."""

    midi: int
    start: float        # onset, in beats from the start
    duration: float     # length, in beats
    velocity: int = 84

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class Melody:
    """A quantized monophonic melody plus its musical context."""

    notes: list          # list[Note], sorted by start
    tempo: float         # beats per minute
    beats_per_bar: int = 4

    @property
    def length_beats(self) -> float:
        return max((n.end for n in self.notes), default=0.0)

    @property
    def n_bars(self) -> int:
        return max(1, math.ceil(self.length_beats / self.beats_per_bar))


@dataclass
class ChordSpan:
    """A harmony region: one chord sounding over [start, start+duration) beats."""

    start: float
    duration: float
    root_pc: int         # 0..11
    quality: str         # key into theory.CHORD_INTERVALS
    roman: str = ""
    label: str = ""      # e.g. "Cmaj7"

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class PluckEvent:
    """A single plucked string in the final arrangement (timing in beats)."""

    start: float
    duration: float
    string: int          # 0 (low E) .. 5 (high e)
    fret: int
    midi: int
    velocity: int = 80
    voice: str = "mel"   # "mel" | "acc" | "bass"

    @property
    def end(self) -> float:
        return self.start + self.duration
