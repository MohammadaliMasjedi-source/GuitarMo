"""Render plucked-string audio with Karplus-Strong synthesis (pure NumPy).

Karplus & Strong (1983), "Digital Synthesis of Plucked-String and Drum
Timbres." A short noise burst is fed through a feedback delay line whose loop
length sets the pitch and whose averaging low-pass filter produces the natural
decay of a plucked nylon string -- all without any external synth/soundfont.

The recurrence ``y[n] = decay * 0.5 * (y[n-N] + y[n-N-1])`` is evaluated one
delay-line period at a time so each step is a vectorised NumPy operation.
"""
from __future__ import annotations

import numpy as np

try:
    from scipy.signal import fftconvolve
    _HAVE_SCIPY = True
except Exception:                       # pragma: no cover
    _HAVE_SCIPY = False

_RNG = np.random.default_rng(1234)      # fixed seed -> deterministic renders


def midi_to_hz(midi):
    return 440.0 * 2.0 ** ((midi - 69) / 12.0)


def karplus_strong(freq, dur_sec, sr=44100, decay=0.996):
    """Synthesize one plucked note. Returns a float array in roughly [-1, 1]."""
    if freq <= 0 or dur_sec <= 0:
        return np.zeros(0, dtype=np.float32)
    N = max(2, int(round(sr / freq)))
    L = int(dur_sec * sr)
    if L <= N:
        L = N + 1

    # Excitation: a noise burst, low-passed a little for a warmer nylon attack.
    init = _RNG.uniform(-1.0, 1.0, N)
    init = np.convolve(init, [0.25, 0.5, 0.25], mode="same")

    full = np.empty(L, dtype=np.float64)
    full[:N] = init
    i0 = N
    while i0 < L:
        blk = min(N, L - i0)
        pb = full[i0 - N:i0]                       # previous delay-line period
        shifted = np.empty(N)
        shifted[0] = full[i0 - N - 1] if i0 - N - 1 >= 0 else pb[-1]
        shifted[1:] = pb[:-1]
        new = decay * 0.5 * (pb + shifted)
        full[i0:i0 + blk] = new[:blk]
        i0 += blk

    # amplitude shaping: quick attack + gentle release so notes start/stop clean
    env = np.ones(L)
    atk = min(int(0.005 * sr), L)
    if atk > 0:
        env[:atk] = np.linspace(0.0, 1.0, atk)
    rel = min(int(0.020 * sr), L)
    if rel > 0:
        env[-rel:] *= np.linspace(1.0, 0.0, rel)
    return (full * env).astype(np.float32)


def _reverb(y, sr, wet=0.18, decay_sec=0.32):
    if not _HAVE_SCIPY or wet <= 0:
        return y
    n = int(decay_sec * sr)
    ir = _RNG.uniform(-1.0, 1.0, n) * np.exp(-np.linspace(0, 6, n))
    ir[0] = 1.0
    wetsig = fftconvolve(y, ir)[:len(y)]
    wetsig /= (np.max(np.abs(wetsig)) + 1e-9)
    return (1 - wet) * y + wet * wetsig


def render(events, tempo, sr=44100, reverb=True, tail_sec=1.2):
    """Render a list of :class:`PluckEvent` (timing in beats) to a mono signal.

    Returns ``(y, sr)`` with ``y`` float32 normalised to a 0.9 peak.
    """
    beat = 60.0 / tempo
    if not events:
        return np.zeros(int(0.5 * sr), dtype=np.float32), sr

    end_sec = max(e.end for e in events) * beat + tail_sec
    buf = np.zeros(int(end_sec * sr) + 1, dtype=np.float64)

    for e in events:
        start_sec = e.start * beat
        dur_sec = max(0.12, e.duration * beat + 0.35)    # let strings ring out
        tone = karplus_strong(midi_to_hz(e.midi), dur_sec, sr)
        if tone.size == 0:
            continue
        a = int(start_sec * sr)
        b = min(len(buf), a + len(tone))
        buf[a:b] += tone[:b - a] * (e.velocity / 127.0)

    if reverb:
        buf = _reverb(buf, sr)

    peak = float(np.max(np.abs(buf)))
    if peak > 0:
        buf = 0.9 * buf / peak
    return buf.astype(np.float32), sr
