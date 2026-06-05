"""Fundamental-frequency (f0) estimation from a vocal recording.

Uses pYIN (Mauch & Dixon, 2014) via librosa -- a probabilistic refinement of the
YIN algorithm (de Cheveigne & Kawahara, 2002) that adds voiced/unvoiced
probabilities, which we use to gate note segmentation.
"""
from __future__ import annotations

import librosa
import numpy as np

DEFAULT_HOP = 512


def estimate_f0(y, sr, fmin=None, fmax=None, hop_length=DEFAULT_HOP):
    """Track the sung melody's f0 with pYIN.

    Returns ``(times, f0_hz, voiced_flag, voiced_prob)``.
    ``f0_hz`` is ``NaN`` on unvoiced frames.
    """
    if fmin is None:
        fmin = librosa.note_to_hz("C2")   # ~65 Hz, comfortably below a bass voice
    if fmax is None:
        fmax = librosa.note_to_hz("C6")   # ~1047 Hz, above a soprano

    f0, voiced_flag, voiced_prob = librosa.pyin(
        y, fmin=float(fmin), fmax=float(fmax), sr=sr, hop_length=hop_length,
    )
    times = librosa.times_like(f0, sr=sr, hop_length=hop_length)
    return times, f0, voiced_flag, voiced_prob


def hz_to_midi(f0_hz):
    """Vectorised Hz -> (float) MIDI, preserving NaN."""
    f0_hz = np.asarray(f0_hz, dtype=float)
    out = np.full_like(f0_hz, np.nan)
    valid = np.isfinite(f0_hz) & (f0_hz > 0)
    out[valid] = 69.0 + 12.0 * np.log2(f0_hz[valid] / 440.0)
    return out
