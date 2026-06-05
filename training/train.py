"""Train the GuitarMo harmonizer (Phase 3.4). Runs on the RTX-3090 (ISSE).

Status: SCAFFOLD. Will: load processed splits, build the model, train with
seeded determinism, log curves, and checkpoint to runs/<id>/ with a model card.
"""
from __future__ import annotations

import argparse


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True)
    p.add_argument("--data", default="processed")
    p.add_argument("--out", default="runs")
    p.add_argument("--seed", type=int, default=1234)
    p.parse_args(argv)
    raise NotImplementedError(
        "train.py is a Phase 3.4 scaffold. Target: deterministic training loop, "
        "early stopping on val chord-accuracy, checkpoints + model card.")


if __name__ == "__main__":
    raise SystemExit(main())
