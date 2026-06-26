"""Pluggable pitch (f0) backends.

The transcriber only needs one thing from a pitch tracker: given a mono signal,
hand back a per-frame fundamental-frequency track plus a voiced/unvoiced mask.
Different engines (pYIN, CREPE, basic-pitch, ...) do that with very different
trade-offs, so we hide each behind a small, uniform interface and pick one by
name at run time.

Design
------
* :class:`PitchResult` -- the common return type (times, f0 in Hz, voiced flag,
  voiced probability). ``f0_hz`` is ``NaN`` on unvoiced frames, matching pYIN.
* :class:`PitchBackend` -- the interface. A backend is *available* only if its
  optional dependencies import; otherwise it advertises ``available == False``
  and the caller can fall back.
* :func:`get_backend` / :func:`list_backends` -- the registry the CLI, web app
  and :mod:`guitarmo.transcribe` use.

The default backend is **pYIN** (always available; only needs librosa). The
**CREPE** backend uses a trained CNN (Kim et al., 2018) for higher accuracy on
real singing but needs the optional ``crepe``/``tensorflow`` extras; when those
are missing it transparently falls back to pYIN so the pipeline never breaks.
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

import numpy as np

from .pitch import DEFAULT_HOP, estimate_f0

__all__ = [
    "PitchResult",
    "PitchBackend",
    "PyinBackend",
    "CrepeBackend",
    "register_backend",
    "get_backend",
    "list_backends",
    "available_backends",
    "DEFAULT_BACKEND",
]

DEFAULT_BACKEND = "pyin"


@dataclass
class PitchResult:
    """Per-frame f0 track shared by every backend.

    Attributes
    ----------
    times : np.ndarray
        Frame centre times, in seconds.
    f0_hz : np.ndarray
        Fundamental frequency in Hz, ``NaN`` on unvoiced frames.
    voiced_flag : np.ndarray
        Boolean voiced/unvoiced mask, same length as ``times``.
    voiced_prob : np.ndarray
        Voicing probability in ``[0, 1]``.
    backend : str
        Name of the backend that actually produced the result (useful when a
        backend fell back to another one).
    """

    times: np.ndarray
    f0_hz: np.ndarray
    voiced_flag: np.ndarray
    voiced_prob: np.ndarray
    backend: str = ""

    @property
    def frame_period(self) -> float:
        """Seconds between consecutive frames."""
        if len(self.times) > 1:
            return float(self.times[1] - self.times[0])
        return 0.0


class PitchBackend:
    """Common interface for f0 estimators.

    Subclasses implement :meth:`_track`. Override :attr:`available` to report
    whether optional dependencies are importable.
    """

    name: str = "base"
    display: str = "Pitch backend"
    description: str = ""

    @property
    def available(self) -> bool:  # pragma: no cover - trivial
        return True

    def track(self, y, sr, fmin=None, fmax=None, hop_length=DEFAULT_HOP) -> PitchResult:
        """Estimate f0 for mono signal ``y`` sampled at ``sr`` Hz."""
        y = np.asarray(y, dtype=float)
        if y.ndim > 1:                       # collapse accidental stereo
            y = y.mean(axis=0)
        if y.size == 0:
            raise ValueError("empty audio signal passed to pitch backend")
        return self._track(y, sr, fmin=fmin, fmax=fmax, hop_length=hop_length)

    def _track(self, y, sr, fmin, fmax, hop_length) -> PitchResult:  # pragma: no cover
        raise NotImplementedError


class PyinBackend(PitchBackend):
    """Probabilistic YIN (Mauch & Dixon, 2014) via librosa. Always available."""

    name = "pyin"
    display = "pYIN (librosa)"
    description = "Probabilistic YIN. Robust, dependency-light, the default."

    def _track(self, y, sr, fmin, fmax, hop_length) -> PitchResult:
        times, f0, voiced_flag, voiced_prob = estimate_f0(
            y, sr, fmin=fmin, fmax=fmax, hop_length=hop_length
        )
        return PitchResult(
            times=np.asarray(times, dtype=float),
            f0_hz=np.asarray(f0, dtype=float),
            voiced_flag=np.asarray(voiced_flag, dtype=bool),
            voiced_prob=np.asarray(voiced_prob, dtype=float),
            backend=self.name,
        )


class CrepeBackend(PitchBackend):
    """CREPE deep-CNN pitch tracker (Kim et al., 2018).

    Needs the optional ``crepe`` + ``tensorflow`` extras (see
    ``requirements-ml.txt``). When they are not importable the backend reports
    ``available == False`` and :meth:`track` transparently falls back to pYIN,
    so callers can always request "crepe" without first checking for the heavy
    dependencies.
    """

    name = "crepe"
    display = "CREPE (deep CNN)"
    description = ("Trained CNN pitch tracker; higher accuracy on real singing. "
                   "Falls back to pYIN if TensorFlow/CREPE are not installed.")

    #: CREPE model capacity: tiny | small | medium | large | full.
    model_capacity = "full"
    #: confidence threshold above which a frame counts as voiced.
    confidence_threshold = 0.5

    def __init__(self, model_capacity=None, confidence_threshold=None,
                 fallback=True):
        if model_capacity is not None:
            self.model_capacity = model_capacity
        if confidence_threshold is not None:
            self.confidence_threshold = confidence_threshold
        self.fallback = fallback

    @property
    def available(self) -> bool:
        try:
            import crepe  # noqa: F401
            import tensorflow  # noqa: F401
        except Exception:
            return False
        return True

    def _track(self, y, sr, fmin, fmax, hop_length) -> PitchResult:
        if not self.available:
            if not self.fallback:
                raise RuntimeError(
                    "CREPE backend requested but 'crepe'/'tensorflow' are not "
                    "installed. Install the ML extras (requirements-ml.txt) or "
                    "use the pYIN backend."
                )
            warnings.warn(
                "CREPE not available (missing crepe/tensorflow); "
                "falling back to pYIN.",
                RuntimeWarning,
                stacklevel=2,
            )
            res = PyinBackend()._track(y, sr, fmin, fmax, hop_length)
            res.backend = "pyin (crepe-fallback)"
            return res

        import crepe

        # CREPE samples every 10 ms regardless of hop_length; we still honour the
        # voiced range by masking f0 outside [fmin, fmax].
        if fmin is None:
            import librosa
            fmin = float(librosa.note_to_hz("C2"))
        if fmax is None:
            import librosa
            fmax = float(librosa.note_to_hz("C6"))

        times, frequency, confidence, _ = crepe.predict(
            y, sr, model_capacity=self.model_capacity,
            viterbi=True, center=True, step_size=10, verbose=0,
        )
        times = np.asarray(times, dtype=float)
        f0 = np.asarray(frequency, dtype=float)
        conf = np.asarray(confidence, dtype=float)

        in_range = (f0 >= fmin) & (f0 <= fmax)
        voiced = (conf >= self.confidence_threshold) & in_range
        f0 = np.where(voiced, f0, np.nan)
        return PitchResult(
            times=times,
            f0_hz=f0,
            voiced_flag=voiced.astype(bool),
            voiced_prob=conf,
            backend=self.name,
        )


# --- registry --------------------------------------------------------------

_REGISTRY: dict = {}


def register_backend(backend: PitchBackend) -> None:
    """Add (or replace) a backend in the global registry, keyed by its name."""
    if not getattr(backend, "name", None):
        raise ValueError("pitch backend must have a non-empty .name")
    _REGISTRY[backend.name] = backend


def get_backend(name=None) -> PitchBackend:
    """Return the backend registered under ``name`` (default: pYIN).

    Raises ``ValueError`` for an unknown name, listing the valid options.
    """
    if name is None:
        name = DEFAULT_BACKEND
    name = str(name).lower()
    if name not in _REGISTRY:
        opts = ", ".join(sorted(_REGISTRY))
        raise ValueError(f"unknown pitch backend {name!r}; choose from: {opts}")
    return _REGISTRY[name]


def list_backends() -> dict:
    """``{name: {'display', 'description', 'available'}}`` for UI/CLI listing."""
    return {
        name: {
            "display": b.display,
            "description": b.description,
            "available": b.available,
        }
        for name, b in _REGISTRY.items()
    }


def available_backends() -> list:
    """Names of backends whose optional dependencies are importable."""
    return [name for name, b in _REGISTRY.items() if b.available]


register_backend(PyinBackend())
register_backend(CrepeBackend())
