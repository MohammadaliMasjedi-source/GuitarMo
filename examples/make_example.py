"""Generate a demo: synthesize a *sung* melody, then arrange it for guitar.

This doubles as an end-to-end check of the audio -> notes -> harmony -> guitar
path without needing a microphone. Run from the repo root::

    python examples/make_example.py
"""
import os
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guitarmo import process  # noqa: E402

SR = 22050

# "Twinkle, Twinkle, Little Star" -- unambiguously C major.
TWINKLE = [
    (60, 1), (60, 1), (67, 1), (67, 1), (69, 1), (69, 1), (67, 2),
    (65, 1), (65, 1), (64, 1), (64, 1), (62, 1), (62, 1), (60, 2),
]


def synth_note(midi, dur_sec, sr=SR):
    """A vibrato'd, harmonically rich tone that loosely imitates a voice."""
    t = np.arange(int(dur_sec * sr)) / sr
    f = 440.0 * 2 ** ((midi - 69) / 12)
    phase = 2 * np.pi * f * t + 0.4 * np.sin(2 * np.pi * 5.0 * t)   # 5 Hz vibrato
    sig = np.sin(phase) + 0.3 * np.sin(2 * phase) + 0.15 * np.sin(3 * phase)
    env = np.ones_like(t)
    a, r = int(0.02 * sr), int(0.06 * sr)
    if a:
        env[:a] = np.linspace(0, 1, a)
    if r:
        env[-r:] = np.linspace(1, 0, r)
    return (sig * env * 0.4).astype(np.float32)


def synth_sung(seq, bpm=100, sr=SR):
    beat = 60.0 / bpm
    return np.concatenate([synth_note(m, b * beat, sr) for m, b in seq])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    wav = os.path.join(here, "twinkle_voice.wav")
    sf.write(wav, synth_sung(TWINKLE), SR)
    print(f"wrote {wav}")

    for style, level in [("classical", "easy"),
                         ("classical", "normal"),
                         ("bossa", "professional")]:
        out = os.path.join(here, "demo_output", f"twinkle_{style}_{level}")
        res = process(wav, style=style, level=level, out_dir=out)
        print("\n" + "#" * 70)
        print(res.summary())
        print(f"wav : {res.wav_path}")
        print(f"midi: {res.midi_path}")
        print(f"tab : {res.tab_path}")
    # show one full tab
    print("\n" + res.tab_text)


if __name__ == "__main__":
    main()
