"""Turn a vocal recording into a quantized, monophonic :class:`Melody`.

Pipeline:  audio -> pYIN f0  ->  note segmentation  ->  tempo estimate  ->
beat quantization.  The output is intentionally "clean" (single voice, snapped
to a grid) so the harmonizer and arranger downstream have something musical to
work with even when the singing is rough.
"""
from __future__ import annotations

import librosa
import numpy as np

from .core import Melody, Note
from .pitch import DEFAULT_HOP, hz_to_midi
from .pitch_backends import PitchBackend, get_backend


def _segment_notes(times, midi_track, voiced_flag, frame_period,
                   max_gap_frames=3, semitone_tol=0.6, min_dur_sec=0.06):
    """Group consecutive, similar-pitch voiced frames into discrete notes.

    Returns a list of ``(midi:int, start_sec, end_sec)`` tuples.
    """
    notes = []
    buf = []            # midi values of the current note
    start_idx = None
    last_voiced = None
    gap = 0

    def close(end_idx):
        if start_idx is None or not buf:
            return
        midi = int(round(float(np.median(buf))))
        start_sec = float(times[start_idx])
        end_sec = float(times[end_idx]) + frame_period
        if end_sec - start_sec >= min_dur_sec:
            notes.append((midi, start_sec, end_sec))

    for i, m in enumerate(midi_track):
        voiced = bool(voiced_flag[i]) and np.isfinite(m)
        if voiced:
            gap = 0
            if start_idx is None:
                buf = [m]
                start_idx = i
            else:
                ref = float(np.median(buf))
                if abs(m - ref) <= semitone_tol:
                    buf.append(m)
                else:                       # pitch jumped -> new note
                    close(last_voiced)
                    buf = [m]
                    start_idx = i
            last_voiced = i
        else:
            gap += 1
            if start_idx is not None and gap > max_gap_frames:
                close(last_voiced)
                buf = []
                start_idx = None
    if start_idx is not None and last_voiced is not None:
        close(last_voiced)
    return notes


def _estimate_tempo(y, sr):
    try:
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        tempo = float(np.atleast_1d(tempo)[0])
    except Exception:
        tempo = 0.0
    if not np.isfinite(tempo) or tempo < 40 or tempo > 220:
        tempo = 100.0
    return tempo


def _note_velocity(y, sr, start_sec, end_sec):
    a = max(0, int(start_sec * sr))
    b = min(len(y), int(end_sec * sr))
    if b <= a:
        return 84
    rms = float(np.sqrt(np.mean(y[a:b] ** 2) + 1e-12))
    # map a fairly quiet-to-loud RMS range onto MIDI velocity
    v = int(np.clip(60 + 700 * rms, 55, 118))
    return v


def transcribe(y, sr, tempo=None, grid=0.5, beats_per_bar=4,
               hop_length=DEFAULT_HOP, pitch_backend=None):
    """Transcribe a mono signal ``y`` into a :class:`Melody`.

    ``grid`` is the quantization resolution in beats (0.5 == eighth notes).
    Pass an explicit ``tempo`` (BPM) to skip automatic tempo detection.

    ``pitch_backend`` selects the f0 estimator: a backend name (e.g. ``"pyin"``
    or ``"crepe"``), a :class:`~guitarmo.pitch_backends.PitchBackend` instance,
    or ``None`` for the default (pYIN). See :mod:`guitarmo.pitch_backends`.
    """
    backend = (pitch_backend if isinstance(pitch_backend, PitchBackend)
               else get_backend(pitch_backend))
    pr = backend.track(y, sr, hop_length=hop_length)
    times = pr.times
    midi_track = hz_to_midi(pr.f0_hz)
    voiced_flag = pr.voiced_flag
    frame_period = pr.frame_period or (hop_length / sr)

    raw = _segment_notes(times, midi_track, voiced_flag, frame_period)
    if not raw:
        raise ValueError(
            "No sung/pitched content detected. Try singing a clear, sustained "
            "melody close to the microphone (and supply a WAV file)."
        )

    if tempo is None:
        tempo = _estimate_tempo(y, sr)
    beat_dur = 60.0 / tempo

    # seconds -> beats, then quantize onto the grid.
    def q(x):
        return round(x / grid) * grid

    quant = []
    for midi, s, e in raw:
        qs = q(s / beat_dur)
        qd = max(grid, q((e - s) / beat_dur))
        quant.append([midi, qs, qd, _note_velocity(y, sr, s, e)])

    quant.sort(key=lambda r: r[1])
    offset = quant[0][1]            # shift so the melody starts at beat 0
    notes = []
    for i, (midi, qs, qd, vel) in enumerate(quant):
        start = qs - offset
        # do not let a note bleed past the onset of the next one
        if i + 1 < len(quant):
            nxt = quant[i + 1][1] - offset
            qd = min(qd, max(grid, nxt - start))
        if qd >= grid:
            notes.append(Note(midi=midi, start=start, duration=qd, velocity=vel))

    # merge immediately-adjacent notes of identical pitch
    merged = [notes[0]]
    for n in notes[1:]:
        prev = merged[-1]
        if n.midi == prev.midi and abs(n.start - prev.end) < 1e-6:
            prev.duration += n.duration
        else:
            merged.append(n)

    return Melody(notes=merged, tempo=float(tempo), beats_per_bar=beats_per_bar)
