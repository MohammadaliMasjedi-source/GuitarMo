"""End-to-end test: synthesize a short sung melody, run the full pipeline.

This is the one test that exercises the (slow) pYIN pitch tracker, so it is
kept short on purpose.
"""
import numpy as np
import soundfile as sf

from guitarmo import process

SR = 22050


def _synth(midi, dur_sec):
    t = np.arange(int(dur_sec * SR)) / SR
    f = 440.0 * 2 ** ((midi - 69) / 12)
    phase = 2 * np.pi * f * t + 0.4 * np.sin(2 * np.pi * 5.0 * t)
    sig = np.sin(phase) + 0.3 * np.sin(2 * phase)
    env = np.ones_like(t)
    a, r = int(0.02 * SR), int(0.06 * SR)
    env[:a] = np.linspace(0, 1, a)
    env[-r:] = np.linspace(1, 0, r)
    return (sig * env * 0.4).astype(np.float32)


def test_end_to_end(tmp_path):
    # C E G C -- a clear C-major arpeggio
    seq = [(60, 0.6), (64, 0.6), (67, 0.6), (72, 0.9)]
    y = np.concatenate([_synth(m, d) for m, d in seq])
    wav = tmp_path / "voice.wav"
    sf.write(str(wav), y, SR)

    res = process(str(wav), style="classical", level="normal",
                  out_dir=str(tmp_path / "out"))

    assert res.key_name.startswith("C")          # detected C-ish tonality
    assert res.n_notes >= 3
    assert res.chords[-1].startswith("C")         # cadence on the tonic
    import os
    assert os.path.exists(res.wav_path)
    assert os.path.exists(res.midi_path)
    assert os.path.exists(res.tab_path)
    assert "e|" in res.tab_text and "E|" in res.tab_text
