"""Tests for the pluggable pitch-backend layer (sub-phase 2.1).

These avoid the heavy optional deps: pYIN is exercised on a short synthetic
tone, and the CREPE backend is checked for correct *fallback* behaviour when
TensorFlow/CREPE are not installed (the common case in CI).
"""
import warnings

import numpy as np
import pytest

from guitarmo import available_backends, list_backends
from guitarmo.pitch_backends import (CrepeBackend, PitchResult, PyinBackend,
                                      get_backend, register_backend)

SR = 22050


def _tone(midi=69, dur=0.5, sr=SR):
    """A clean sine tone at the given MIDI pitch."""
    t = np.arange(int(dur * sr)) / sr
    f = 440.0 * 2 ** ((midi - 69) / 12)
    return (0.5 * np.sin(2 * np.pi * f * t)).astype(np.float32)


# --- registry -------------------------------------------------------------

def test_registry_has_pyin_and_crepe():
    names = set(list_backends())
    assert {"pyin", "crepe"} <= names


def test_pyin_is_always_available():
    assert "pyin" in available_backends()
    assert list_backends()["pyin"]["available"] is True


def test_get_backend_default_is_pyin():
    assert get_backend().name == "pyin"
    assert get_backend(None).name == "pyin"


def test_get_backend_unknown_raises():
    with pytest.raises(ValueError):
        get_backend("does-not-exist")


def test_register_requires_name():
    bad = PyinBackend()
    bad.name = ""
    with pytest.raises(ValueError):
        register_backend(bad)


# --- pYIN backend ---------------------------------------------------------

def test_pyin_tracks_a_tone():
    y = _tone(midi=69, dur=0.6)          # A4 = 440 Hz
    res = get_backend("pyin").track(y, SR)
    assert isinstance(res, PitchResult)
    assert res.backend == "pyin"
    assert len(res.times) == len(res.f0_hz) == len(res.voiced_flag)
    voiced = res.f0_hz[res.voiced_flag]
    assert voiced.size > 0
    # the median voiced f0 should sit near 440 Hz
    assert abs(float(np.nanmedian(voiced)) - 440.0) < 25.0
    assert res.frame_period > 0


def test_pyin_rejects_empty_signal():
    with pytest.raises(ValueError):
        get_backend("pyin").track(np.array([], dtype=float), SR)


def test_backend_collapses_stereo():
    mono = _tone(dur=0.4)
    stereo = np.stack([mono, mono])      # shape (2, N)
    res = PyinBackend().track(stereo, SR)
    assert res.f0_hz.ndim == 1


# --- CREPE backend (fallback path) ----------------------------------------

def test_crepe_falls_back_to_pyin_when_unavailable():
    backend = CrepeBackend()
    if backend.available:
        pytest.skip("CREPE actually installed; fallback path not exercised")
    y = _tone(midi=67, dur=0.5)          # G4
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = backend.track(y, SR)
    assert "fallback" in res.backend
    assert res.f0_hz[res.voiced_flag].size > 0


def test_crepe_can_disable_fallback():
    backend = CrepeBackend(fallback=False)
    if backend.available:
        pytest.skip("CREPE actually installed; no-fallback error not raised")
    with pytest.raises(RuntimeError):
        backend.track(_tone(), SR)


# --- transcribe wiring ----------------------------------------------------

def test_transcribe_accepts_backend_name():
    from guitarmo.transcribe import transcribe
    # a tiny C-major run so segmentation yields a couple of notes
    y = np.concatenate([_tone(m, 0.4) for m in (60, 64, 67)])
    mel = transcribe(y, SR, pitch_backend="pyin")
    assert mel.notes
    assert mel.tempo > 0
