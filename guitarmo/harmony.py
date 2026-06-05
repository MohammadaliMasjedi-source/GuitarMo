"""Choose a chord progression that fits the melody.

A transparent, rule-based harmonizer (functional tonal harmony) rather than a
learned model -- it is explainable, deterministic and dependency-light. The
difficulty level controls harmonic rhythm and chord vocabulary:

    easy          : one triad per bar, diatonic only
    normal         : two chords per bar, diatonic 7ths, V at the cadence
    professional  : two chords per bar, 7ths + 9th colours, ii-V-I cadence

See ``RESEARCH.md`` for how this relates to data-driven harmonizers
(Microsoft MySong/Songsmith, DeepBach, HMM melody-harmonization).
"""
from __future__ import annotations

import math

from . import theory
from .core import ChordSpan

_SPAN_LEN = {"easy": 4, "normal": 2, "professional": 2}


def _window_weights(melody, t0, t1):
    """Duration-weighted pitch-class content of the melody within [t0, t1)."""
    w = {}
    for n in melody.notes:
        overlap = min(n.end, t1) - max(n.start, t0)
        if overlap > 0:
            w[n.midi % 12] = w.get(n.midi % 12, 0.0) + overlap
    return w


def _score(chord, weights, key, prev_root):
    pcs = set(theory.chord_pcs(chord["root_pc"], chord["quality"]))
    total = sum(weights.values()) or 1.0
    s = 0.0
    for p, wt in weights.items():
        s += wt if p in pcs else -0.5 * wt
    # functional bias
    if chord["root_pc"] == key.tonic_pc:
        s += 0.25 * total
    elif chord["root_pc"] == (key.tonic_pc + 7) % 12:      # dominant
        s += 0.15 * total
    elif chord["root_pc"] == (key.tonic_pc + 5) % 12:      # subdominant
        s += 0.10 * total
    if prev_root is not None and chord["root_pc"] == prev_root:
        s -= 0.10 * total                                  # encourage motion
    return s


def _pick(cands, weights, key, prev_root, root_filter=None):
    pool = cands if root_filter is None else [c for c in cands
                                              if c["root_pc"] == root_filter]
    pool = pool or cands
    return max(pool, key=lambda c: _score(c, weights, key, prev_root))


def _colorize(chord, weights):
    """Promote chords to add9 / 9th colours when the 9th is in the melody."""
    ninth = (chord["root_pc"] + 2) % 12
    if ninth in weights:
        q = chord["quality"]
        if q == "maj":
            chord = {**chord, "quality": "add9"}
        elif q == "maj7":
            chord = {**chord, "quality": "maj9"}
        elif q == "min7":
            chord = {**chord, "quality": "min9"}
    return chord


def harmonize(melody, key, level="normal", style=None):
    """Return a list of :class:`ChordSpan` covering the whole melody."""
    span_len = _SPAN_LEN.get(level, 2)
    use_seventh = level in ("normal", "professional") or (
        style is not None and style.seventh_bias > 0)

    cands = key.diatonic_chords(seventh=use_seventh)
    # In minor, add the (harmonic-minor) major/dominant-7 V for real cadences.
    if key.mode == "minor":
        dom_root = (key.tonic_pc + 7) % 12
        cands.append({"degree": 4, "root_pc": dom_root,
                      "quality": "dom7" if use_seventh else "maj", "roman": "V"})

    length = melody.length_beats
    n = max(1, math.ceil(length / span_len))

    spans = []
    prev_root = None
    for k in range(n):
        t0 = k * span_len
        weights = _window_weights(melody, t0, t0 + span_len)

        if k == n - 1:                                  # final cadence -> tonic
            chord = _pick(cands, weights, key, prev_root, root_filter=key.tonic_pc)
        elif level in ("normal", "professional") and k == n - 2 and n >= 2:
            chord = _pick(cands, weights, key, prev_root,
                          root_filter=(key.tonic_pc + 7) % 12)   # dominant
        elif level == "professional" and k == n - 3 and n >= 3:
            chord = _pick(cands, weights, key, prev_root,
                          root_filter=(key.tonic_pc + 2) % 12)   # ii (pre-dom)
        elif not weights:                               # silence -> stay tonic
            chord = _pick(cands, weights, key, prev_root, root_filter=key.tonic_pc)
        else:
            chord = _pick(cands, weights, key, prev_root)

        if level == "professional":
            chord = _colorize(chord, weights)

        spans.append(ChordSpan(
            start=float(t0), duration=float(span_len),
            root_pc=chord["root_pc"], quality=chord["quality"],
            roman=chord["roman"],
            label=theory.chord_label(chord["root_pc"], chord["quality"]),
        ))
        prev_root = chord["root_pc"]
    return spans
