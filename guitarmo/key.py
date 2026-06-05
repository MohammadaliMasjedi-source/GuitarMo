"""Key detection (Krumhansl-Schmuckler) and diatonic harmony for a key."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import theory
from .theory import NOTE_NAMES

# Krumhansl-Kessler key profiles (tonal hierarchy), tonic at index 0.
# Krumhansl & Kessler (1982), "Tracing the dynamic changes in perceived tonal
# organization in a spatial representation of musical keys."
KK_MAJOR = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                     2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KK_MINOR = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                     2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

# Diatonic chord qualities / roman numerals by scale degree (0-indexed).
_MAJOR_TRIADS = ("maj", "min", "min", "maj", "maj", "min", "dim")
_MAJOR_SEVENTHS = ("maj7", "min7", "min7", "maj7", "dom7", "min7", "m7b5")
_MAJOR_ROMAN = ("I", "ii", "iii", "IV", "V", "vi", "vii°")
_MINOR_TRIADS = ("min", "dim", "maj", "min", "min", "maj", "maj")
_MINOR_SEVENTHS = ("min7", "m7b5", "maj7", "min7", "min7", "maj7", "dom7")
_MINOR_ROMAN = ("i", "ii°", "III", "iv", "v", "VI", "VII")


@dataclass
class Key:
    tonic_pc: int
    mode: str  # "major" | "minor"

    @property
    def name(self) -> str:
        return f"{NOTE_NAMES[self.tonic_pc % 12]} {self.mode}"

    def scale_pcs(self):
        return theory.scale_pcs(self.tonic_pc, self.mode)

    def diatonic_chords(self, seventh: bool = False):
        """List of dicts: degree (0-6), root_pc, quality, roman."""
        steps = (theory.MAJOR_STEPS if self.mode == "major"
                 else theory.NATURAL_MINOR_STEPS)
        if self.mode == "major":
            quals = _MAJOR_SEVENTHS if seventh else _MAJOR_TRIADS
            romans = _MAJOR_ROMAN
        else:
            quals = _MINOR_SEVENTHS if seventh else _MINOR_TRIADS
            romans = _MINOR_ROMAN
        out = []
        for deg in range(7):
            root = (self.tonic_pc + steps[deg]) % 12
            out.append({"degree": deg, "root_pc": root,
                        "quality": quals[deg], "roman": romans[deg]})
        return out


def _pc_histogram(notes):
    hist = np.zeros(12)
    for n in notes:
        hist[n.midi % 12] += max(n.duration, 0.01)
    return hist


def detect_key(notes) -> Key:
    """Estimate the key by correlating the duration-weighted pitch-class
    histogram against the 24 rotated KK profiles."""
    hist = _pc_histogram(notes)
    if hist.sum() <= 0:
        return Key(0, "major")
    best = None  # (corr, tonic, mode)
    for mode, prof in (("major", KK_MAJOR), ("minor", KK_MINOR)):
        for tonic in range(12):
            rotated = np.roll(prof, tonic)  # profile centred on this tonic
            r = float(np.corrcoef(hist, rotated)[0, 1])
            if best is None or r > best[0]:
                best = (r, tonic, mode)
    return Key(best[1], best[2])
