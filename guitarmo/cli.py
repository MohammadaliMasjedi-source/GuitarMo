"""Command-line interface for GuitarMo.

Examples::

    python -m guitarmo song.wav --style classical --level normal
    python -m guitarmo --record 8 --style bossa --level professional
    python -m guitarmo --list-styles
"""
from __future__ import annotations

import argparse
import sys
import tempfile

from . import LEVELS, list_backends, list_styles, process
from .styles import style_names


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="guitarmo",
        description="Sing a melody -> classical-guitar arrangement "
                    "(tab + MIDI + MusicXML + audio).")
    p.add_argument("input", nargs="?", help="input audio file (WAV recommended)")
    p.add_argument("--style", default="classical", choices=style_names())
    p.add_argument("--level", default="normal", choices=list(LEVELS))
    p.add_argument("--pitch-backend", default=None,
                   choices=sorted(list_backends()),
                   help="f0 estimator to use (default: pyin). 'crepe' needs the "
                        "ML extras and falls back to pyin when unavailable.")
    p.add_argument("--out", default=None, help="output directory")
    p.add_argument("--tempo", type=float, default=None,
                   help="force a tempo in BPM (skip auto-detection)")
    p.add_argument("--record", type=float, metavar="SECONDS", default=None,
                   help="record from the microphone for N seconds, then arrange")
    p.add_argument("--no-reverb", action="store_true")
    p.add_argument("--list-styles", action="store_true")
    p.add_argument("--list-backends", action="store_true",
                   help="list available pitch backends and exit")
    args = p.parse_args(argv)

    if args.list_styles:
        for name, meta in list_styles().items():
            print(f"  {name:12s} {meta['display']:24s} {meta['description']}")
        return 0

    if args.list_backends:
        for name, meta in list_backends().items():
            mark = "available" if meta["available"] else "not installed"
            print(f"  {name:8s} [{mark:13s}] {meta['display']:18s} "
                  f"{meta['description']}")
        return 0

    audio_path = args.input
    if args.record is not None:
        from .audio_io import record, save_wav
        y, sr = record(seconds=args.record)
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        save_wav(tmp.name, y, sr)
        audio_path = tmp.name

    if not audio_path:
        p.error("provide an input file or use --record SECONDS")

    res = process(audio_path, style=args.style, level=args.level,
                  out_dir=args.out, tempo=args.tempo, reverb=not args.no_reverb,
                  pitch_backend=args.pitch_backend)
    print(res.summary())
    print()
    print(res.tab_text)
    print(f"\nOutput written to: {res.out_dir}")
    print(f"  audio : {res.wav_path}")
    print(f"  midi  : {res.midi_path}")
    if res.musicxml_path:
        print(f"  score : {res.musicxml_path}")
    print(f"  tab   : {res.tab_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
