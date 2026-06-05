"""Evaluate a trained harmonizer and A/B it against the rule-based baseline
(Phase 3.5).

Status: SCAFFOLD. Metrics: chord accuracy, chord-tone coverage, harmonic-rhythm
plausibility; plus a blind A/B vs guitarmo.harmony (rules).
"""
from __future__ import annotations

import argparse


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--checkpoint", required=True)
    p.add_argument("--data", default="processed")
    p.add_argument("--baseline", default="rules", choices=["rules", "hmm"])
    p.parse_args(argv)
    raise NotImplementedError(
        "evaluate.py is a Phase 3.5 scaffold. Target: report chord-accuracy and "
        "coverage on the held-out split and compare against the chosen baseline.")


if __name__ == "__main__":
    raise SystemExit(main())
