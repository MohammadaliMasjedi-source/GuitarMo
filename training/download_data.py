"""Acquire training corpora for the GuitarMo harmonizer (Phase 3).

Status: SCAFFOLD. The dataset downloaders are TODO (Phase 3.1); the
``--sample`` path already works so the rest of the pipeline can be developed
against a tiny, license-clean, synthetic dataset.

See ../docs/DATASETS.md for sources and licensing.
"""
from __future__ import annotations

import argparse
import json
import os

# (name -> homepage). Downloaders are implemented in Phase 3.1.
SOURCES = {
    "nottingham": "https://github.com/jukedeck/nottingham-dataset",
    "wikifonia": "(archived lead-sheet collection - respect original terms)",
    "mcgill_billboard": "https://ddmal.music.mcgill.ca/research/The_McGill_Billboard_Project",
    "lakh": "https://colinraffel.com/projects/lmd/",
    "pop909": "https://github.com/music-x-lab/POP909-Dataset",
    "guitarset": "https://guitarset.weebly.com/",
    "dadagp": "https://github.com/dada-bots/dadaGP",
}

# A handful of public-domain nursery tunes (MIDI pitches) with simple chords,
# enough to smoke-test preprocessing/training without any download.
_SAMPLE = [
    {"title": "twinkle", "key": "C",
     "melody": [60, 60, 67, 67, 69, 69, 67, 65, 65, 64, 64, 62, 62, 60],
     "chords": ["C", "C", "F", "C", "F", "C", "G",
                "C", "F", "C", "G", "C", "G", "C"]},
    {"title": "mary", "key": "C",
     "melody": [64, 62, 60, 62, 64, 64, 64, 62, 62, 62, 64, 67, 67],
     "chords": ["C", "G", "C", "G", "C", "C", "G",
                "G", "G", "G", "C", "G", "C"]},
]


def write_sample(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "sample.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for row in _SAMPLE:
            f.write(json.dumps(row) + "\n")
    print(f"wrote synthetic sample -> {path} ({len(_SAMPLE)} tunes)")
    return path


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--sample", action="store_true",
                   help="write a tiny synthetic melody+chord sample (no download)")
    p.add_argument("--out", default="raw")
    p.add_argument("--source", choices=list(SOURCES),
                   help="download a named corpus (TODO: Phase 3.1)")
    args = p.parse_args(argv)

    if args.sample:
        write_sample(args.out)
        return 0
    if args.source:
        raise NotImplementedError(
            f"Downloader for '{args.source}' lands in Phase 3.1. "
            f"Source: {SOURCES[args.source]}")
    p.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
