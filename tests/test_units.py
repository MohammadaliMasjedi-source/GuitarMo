"""Fast unit tests for the music-theory, harmony, arrangement and synthesis
layers -- none of these touch the (slow) pitch tracker."""
import numpy as np

from guitarmo import Note, detect_key
from guitarmo.arrange import HARM_MAX_STRING, MEL_STRINGS, OPEN, arrange
from guitarmo.core import Melody
from guitarmo.harmony import harmonize
from guitarmo.render import karplus_strong, midi_to_hz, render
from guitarmo.styles import LEVELS, get_style, style_names
from guitarmo.theory import chord_label, chord_pcs, scale_pcs


def c_major_scale():
    return [Note(midi=m, start=i, duration=1.0)
            for i, m in enumerate([60, 62, 64, 65, 67, 69, 71, 72])]


# --- theory ---------------------------------------------------------------

def test_chord_pcs_and_labels():
    assert chord_pcs(0, "maj") == (0, 4, 7)
    assert chord_pcs(9, "min7") == (9, 0, 4, 7)
    assert chord_label(0, "maj") == "C"
    assert chord_label(9, "min") == "Am"
    assert chord_label(7, "dom7") == "G7"


def test_scale_pcs():
    assert scale_pcs(0, "major") == (0, 2, 4, 5, 7, 9, 11)
    assert scale_pcs(9, "minor") == (9, 11, 0, 2, 4, 5, 7)


# --- key ------------------------------------------------------------------

def test_key_detection_major():
    assert detect_key(c_major_scale()).name == "C major"


def test_key_detection_minor():
    notes = [Note(midi=m, start=i, duration=1.0)
             for i, m in enumerate([69, 71, 72, 74, 76, 77, 79, 69])]
    k = detect_key(notes)
    assert k.tonic_pc == 9 and k.mode == "minor"


# --- harmony --------------------------------------------------------------

def test_harmony_cadences_on_tonic():
    mel = Melody(notes=c_major_scale(), tempo=100.0)
    key = detect_key(mel.notes)
    for level in LEVELS:
        spans = harmonize(mel, key, level=level, style=get_style("classical"))
        assert spans[-1].root_pc == key.tonic_pc           # ends on tonic
        assert spans[0].start == 0.0
        assert spans[-1].end >= mel.length_beats           # full coverage


def test_professional_uses_sevenths():
    mel = Melody(notes=c_major_scale(), tempo=100.0)
    key = detect_key(mel.notes)
    spans = harmonize(mel, key, level="professional", style=get_style("bossa"))
    assert any("7" in s.label or "9" in s.label for s in spans)


# --- arrangement ----------------------------------------------------------

def test_arrangement_is_physically_valid():
    mel = Melody(notes=c_major_scale(), tempo=100.0)
    key = detect_key(mel.notes)
    for style in style_names():
        for level in LEVELS:
            spans = harmonize(mel, key, level=level, style=get_style(style))
            events = arrange(mel, spans, level=level, style=get_style(style))
            assert events, f"no events for {style}/{level}"
            for e in events:
                assert 0 <= e.fret <= 12
                assert 0 <= e.string <= 5
                assert e.midi == OPEN[e.string] + e.fret     # fret math is consistent
            # registers stay separated: melody on treble, harmony on bass
            mel_strings = {e.string for e in events if e.voice == "mel"}
            acc_strings = {e.string for e in events if e.voice != "mel"}
            assert mel_strings <= set(MEL_STRINGS)
            assert all(s <= HARM_MAX_STRING for s in acc_strings)


# --- synthesis ------------------------------------------------------------

def test_karplus_strong_is_finite_and_bounded():
    y = karplus_strong(220.0, 0.5)
    assert y.size > 0
    assert np.isfinite(y).all()
    assert np.max(np.abs(y)) <= 1.5


def test_render_normalises():
    mel = Melody(notes=c_major_scale(), tempo=120.0)
    key = detect_key(mel.notes)
    spans = harmonize(mel, key, level="normal", style=get_style("classical"))
    events = arrange(mel, spans, level="normal", style=get_style("classical"))
    y, sr = render(events, mel.tempo)
    assert sr == 44100
    assert np.isfinite(y).all()
    assert 0.0 < np.max(np.abs(y)) <= 0.9001


def test_midi_to_hz():
    assert abs(midi_to_hz(69) - 440.0) < 1e-6
