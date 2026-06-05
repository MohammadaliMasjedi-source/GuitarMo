"""Harmonizer models (Phase 3.3-3.4).

Status: SCAFFOLD.
  - HMMHarmonizer : MySong-style baseline (chords=hidden, melody=observed).
  - NeuralHarmonizer : seq2seq (Transformer/BiLSTM) melody -> chord sequence,
    conditioned on style + difficulty.

PyTorch is an optional extra (requirements-ml.txt); imported lazily so this file
is importable without it.
"""
from __future__ import annotations


class HMMHarmonizer:
    """Hidden-Markov baseline. TODO Phase 3.3 (e.g. via hmmlearn)."""

    def fit(self, dataset):
        raise NotImplementedError("HMM baseline lands in Phase 3.3.")

    def harmonize(self, melody):
        raise NotImplementedError("HMM baseline lands in Phase 3.3.")


def build_neural_harmonizer(config):
    """Construct the seq2seq harmonizer. TODO Phase 3.4."""
    try:
        import torch  # noqa: F401
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Install ML extras first: pip install -r requirements-ml.txt") from exc
    raise NotImplementedError(
        "Neural harmonizer (Transformer/BiLSTM) is built in Phase 3.4.")
