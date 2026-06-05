"""Turn raw melody+chord data into a tokenized dataset with splits (Phase 3.2).

Status: SCAFFOLD. Defines the target representation; the full builder is TODO.
"""
from __future__ import annotations

import argparse

# Target representation (Phase 3.2):
#   - melody: per-beat pitch-class (+ contour features)
#   - target: chord label per beat (root pitch-class x quality)
#   - augmentation: transpose to all 12 keys
#   - split: train / val / test (seeded, song-level, no leakage)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", required=True)
    p.add_argument("--raw", default="raw")
    p.add_argument("--out", default="processed")
    p.parse_args(argv)
    raise NotImplementedError(
        "preprocess.py is a Phase 3.2 scaffold. It will read raw/*.jsonl, "
        "tokenize melody->chord pairs, transpose-augment, and write seeded "
        "train/val/test splits to processed/.")


if __name__ == "__main__":
    raise SystemExit(main())
