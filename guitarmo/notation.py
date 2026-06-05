"""Export the arrangement as guitar tab (ASCII), MIDI, and MusicXML."""
from __future__ import annotations

import math

from .core import STRING_NAMES


def beats_to_sec(beats, tempo):
    return beats * 60.0 / tempo


# --- ASCII tablature -------------------------------------------------------

# Display order: high e (string index 5) on top, low E (0) on the bottom.
_DISPLAY_ORDER = (5, 4, 3, 2, 1, 0)


def to_ascii_tab(events, tempo, beats_per_bar=4, col_grid=0.5,
                 bars_per_line=4, header=None):
    """Render a readable 6-line tablature.

    The tab is a *quantized view* (snapped to eighth notes by default); the
    exact timing is preserved in the MIDI/audio outputs.
    """
    if not events:
        return "(empty)"

    total_beats = max(e.end for e in events)
    n_cols = max(1, int(math.ceil(total_beats / col_grid)))
    cols_per_bar = max(1, int(round(beats_per_bar / col_grid)))
    cols_per_line = cols_per_bar * bars_per_line

    # token[string][col] -> fret string
    token = [[None] * n_cols for _ in range(6)]
    for e in events:
        col = int(round(e.start / col_grid))
        if 0 <= col < n_cols and token[e.string][col] is None:
            token[e.string][col] = str(e.fret)

    # drop any trailing all-empty columns (e.g. a strum ringing past the last
    # bar), rounding the end up to a whole bar for a clean barline.
    last = 0
    for col in range(n_cols):
        if any(token[s][col] is not None for s in range(6)):
            last = col
    n_cols = max(cols_per_bar, ((last // cols_per_bar) + 1) * cols_per_bar)
    # resize the token grid to match (pad with rests / truncate)
    for s in range(6):
        if len(token[s]) < n_cols:
            token[s].extend([None] * (n_cols - len(token[s])))
        else:
            token[s] = token[s][:n_cols]

    lines = []
    if header:
        lines.append(header.rstrip())
        lines.append("")

    n_systems = int(math.ceil(n_cols / cols_per_line))
    for sysi in range(n_systems):
        c0 = sysi * cols_per_line
        c1 = min(n_cols, c0 + cols_per_line)
        for s in _DISPLAY_ORDER:
            row = f"{STRING_NAMES[s]}|"
            for col in range(c0, c1):
                tok = token[s][col] or "-"
                row += tok.ljust(2, "-")            # '5-', '12', '--'
                row += "|" if (col + 1) % cols_per_bar == 0 else "-"
            lines.append(row)
        lines.append("")                            # blank line between systems

    return "\n".join(lines).rstrip()


# --- MIDI ------------------------------------------------------------------

def to_midi(events, tempo, path, program=24):
    """Write a General-MIDI file (program 24 = Acoustic Guitar, nylon)."""
    import pretty_midi

    pm = pretty_midi.PrettyMIDI(initial_tempo=float(tempo))
    inst = pretty_midi.Instrument(program=program, name="Classical Guitar")
    for e in events:
        start = beats_to_sec(e.start, tempo)
        end = beats_to_sec(e.end, tempo) + 0.25      # ring out
        inst.notes.append(pretty_midi.Note(
            velocity=int(max(1, min(127, e.velocity))),
            pitch=int(e.midi), start=start, end=end))
    pm.instruments.append(inst)
    pm.write(str(path))
    return path


# --- MusicXML (notation that opens in MuseScore) ---------------------------

def to_musicxml(mel_notes, spans, key, tempo, path):
    """Write a two-part score (melody + chords). Returns ``path`` or ``None``.

    ``mel_notes`` is a list of ``(start_beats, dur_beats, midi)``.
    """
    try:
        from music21 import (chord, clef, instrument, key as m21key, meter,
                              note, stream, tempo as m21tempo)
        from .theory import CHORD_INTERVALS

        score = stream.Score()

        mel = stream.Part()
        mel.insert(0, instrument.AcousticGuitar())
        mel.insert(0, clef.TrebleClef())
        mel.insert(0, m21tempo.MetronomeMark(number=float(tempo)))
        mel.insert(0, meter.TimeSignature(f"{key_beats(spans)}/4"))
        try:
            mel.insert(0, m21key.Key(_tonic_name(key), key.mode))
        except Exception:
            pass
        for start, dur, midi in mel_notes:
            n = note.Note(int(midi))
            n.quarterLength = max(0.25, float(dur))
            mel.insert(float(start), n)

        harm = stream.Part()
        harm.insert(0, instrument.AcousticGuitar())
        for sp in spans:
            root_midi = 48 + (sp.root_pc % 12)        # ~octave 3
            pitches = [root_midi + iv for iv in CHORD_INTERVALS[sp.quality]]
            c = chord.Chord(pitches)
            c.quarterLength = max(0.5, float(sp.duration))
            harm.insert(float(sp.start), c)

        score.insert(0, mel)
        score.insert(0, harm)
        score.write("musicxml", fp=str(path))
        return path
    except Exception:
        return None


def key_beats(spans):
    return 4            # fixed 4/4 for now


def _tonic_name(key):
    from .theory import NOTE_NAMES
    return NOTE_NAMES[key.tonic_pc % 12].replace("#", "#")
