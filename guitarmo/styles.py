"""Accompaniment *styles*: rhythmic templates the arranger fills with chord tones.

A style describes, for each difficulty level, a short rhythmic *cell* that is
tiled across every chord span. Each cell event is ``(offset_beats, dur_beats,
voice)`` where ``voice`` is one of:

    'b'   bass note (root, lowest voiced string)
    'b2'  alternate bass (the chord fifth) -- for alternating-bass feels
    '1'   '2' '3'   successively higher chord tones (arpeggio voices)
    'c'   chord block (all upper voices struck together)
    'S'   full strum (all voiced strings, staggered low->high)

The arranger maps these onto concrete (string, fret) positions for the chord
voicing it has chosen, so styles stay independent of any particular key.
"""
from __future__ import annotations

from dataclasses import dataclass, field

LEVELS = ("easy", "normal", "professional")


def _tile(cell, cell_len, beats):
    """Repeat a rhythmic cell to cover ``beats`` beats."""
    out = []
    t = 0.0
    while t < beats - 1e-9:
        for off, dur, voice in cell:
            start = t + off
            if start >= beats - 1e-9:
                continue
            d = min(dur, beats - start)
            out.append((round(start, 4), round(d, 4), voice))
        t += cell_len
    return out


@dataclass
class Style:
    name: str
    display: str
    description: str
    cells: dict                      # level -> (cell_events, cell_len)
    seventh_bias: float = 0.0        # nudges the harmonizer toward 7th chords
    color: str = ""                  # free-text flavour note

    def events(self, level, beats):
        cell, cell_len = self.cells.get(level, self.cells["normal"])
        return _tile(cell, cell_len, beats)


# --- pattern cells ---------------------------------------------------------
# fmt: off
_ARP4 = [(0, .5, 'b'), (.5, .5, '1'), (1, .5, '2'), (1.5, .5, '3')]
_ARP8 = [(0, .25, 'b'), (.25, .25, '1'), (.5, .25, '2'), (.75, .25, '3'),
         (1, .25, 'b'), (1.25, .25, '1'), (1.5, .25, '2'), (1.75, .25, '3')]
_BASS_CHORD = [(0, 1, 'b'), (1, 1, 'c')]

STYLES = {
    "classical": Style(
        "classical", "Classical (arpeggio)",
        "Free-stroke broken chords in the Spanish/classical tradition (p-i-m-a).",
        cells={
            "easy":         (_BASS_CHORD, 2),
            "normal":       (_ARP4, 2),
            "professional": (_ARP8, 2),
        },
    ),
    "folk": Style(
        "folk", "Folk / Fingerstyle",
        "Alternating-bass 'boom-chick' Travis picking.",
        cells={
            "easy":         (_BASS_CHORD, 2),
            "normal":       ([(0, .5, 'b'), (.5, .5, 'c'),
                              (1, .5, 'b2'), (1.5, .5, 'c')], 2),
            "professional": ([(0, .5, 'b'), (.5, .5, '2'), (1, .5, 'b2'),
                              (1.5, .25, '3'), (1.75, .25, '1')], 2),
        },
    ),
    "bossa": Style(
        "bossa", "Bossa / Latin",
        "Syncopated nylon-string comping with lush 7th/9th colours.",
        seventh_bias=1.5, color="seventh",
        cells={
            "easy":         (_BASS_CHORD, 2),
            "normal":       ([(0, .5, 'b'), (.5, .5, 'c'),
                              (1, .5, 'b2'), (1.5, .5, 'c')], 2),
            "professional": ([(0, .5, 'b'), (.5, .5, 'c'), (1.5, .5, 'c'),
                              (2, .5, 'b2'), (2.5, .5, 'c'), (3.5, .5, 'c')], 4),
        },
    ),
    "flamenco": Style(
        "flamenco", "Flamenco (rasgueado)",
        "Percussive rasgueado strumming with a Phrygian lean.",
        color="phrygian",
        cells={
            "easy":         ([(0, 1, 'S'), (1, 1, 'S')], 2),
            "normal":       ([(0, .5, 'S'), (.5, .5, 'S'),
                              (1, .5, 'S'), (1.5, .5, 'S')], 2),
            "professional": ([(0, .25, 'S'), (.25, .25, 'S'), (.5, .5, 'S'),
                              (1, .25, 'S'), (1.25, .25, 'S'), (1.5, .5, 'S')], 2),
        },
    ),
    "pop_ballad": Style(
        "pop_ballad", "Pop Ballad",
        "Slow, open arpeggios and gentle strums for a singer-songwriter feel.",
        cells={
            "easy":         ([(0, 2, 'S'), (2, 2, 'S')], 4),
            "normal":       ([(0, .5, 'b'), (.5, .5, 'c'),
                              (1, .5, 'c'), (1.5, .5, 'c')], 2),
            "professional": (_ARP4, 2),
        },
    ),
}
# fmt: on


def get_style(name):
    if name not in STYLES:
        raise KeyError(f"Unknown style '{name}'. Available: {list(STYLES)}")
    return STYLES[name]


def style_names():
    return list(STYLES.keys())
