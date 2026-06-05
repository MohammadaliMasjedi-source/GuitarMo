"""Loading, saving and (optionally) recording audio."""
from __future__ import annotations

import librosa
import numpy as np
import soundfile as sf


def load_audio(path, sr=22050):
    """Load a file as mono at the target sample rate. Returns ``(y, sr)``.

    WAV is the most reliable input; MP3/M4A need ffmpeg installed.
    """
    y, sr = librosa.load(str(path), sr=sr, mono=True)
    return y, sr


def save_wav(path, y, sr):
    sf.write(str(path), np.asarray(y), int(sr))
    return path


def record(seconds=8, sr=44100):
    """Capture audio from the default microphone (CLI helper).

    Requires the optional ``sounddevice`` package. The web app records via the
    browser instead, so this is only needed for ``cli.py --record``.
    """
    try:
        import sounddevice as sd
    except Exception as exc:                      # pragma: no cover
        raise RuntimeError(
            "Microphone capture needs the 'sounddevice' package "
            "(pip install sounddevice)."
        ) from exc
    print(f"Recording {seconds}s -- sing now...")
    audio = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()
    print("Done.")
    return audio.flatten(), sr
