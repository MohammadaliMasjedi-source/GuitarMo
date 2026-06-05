"""Map a melody + chord progression onto a six-string classical guitar.

Layout (a standard classical-guitar texture):
    * melody  -> treble strings B & e (indices 4, 5)
    * harmony -> bass strings E A D G (indices 0-3)

Keeping the two registers on disjoint strings guarantees a physically valid
tab (no string is ever asked to sound two notes at once). Melody fingering is
chosen by dynamic programming to minimise left-hand movement -- the classic
"optimal fingering as shortest path" formulation (Sayegh, 1989; Radicioni et
al., 2004). See ``RESEARCH.md``.
"""
from __future__ import annotations

from . import theory
from .core import STANDARD_TUNING, PluckEvent

OPEN = STANDARD_TUNING            # (40,45,50,55,59,64) low E .. high e
MAX_FRET = 12
MEL_STRINGS = (4, 5)             # B3, E4 -- the treble voice
HARM_MAX_STRING = 3             # harmony lives on strings 0..3 (E A D G)
MEL_LO, MEL_HI = OPEN[4], OPEN[5] + MAX_FRET   # 59 .. 76


# --- melody fingering ------------------------------------------------------

def _positions(midi, strings, max_fret=MAX_FRET):
    out = []
    for s in strings:
        fret = midi - OPEN[s]
        if 0 <= fret <= max_fret:
            out.append((s, fret))
    return out


def _fold_to_range(midi, lo=MEL_LO, hi=MEL_HI):
    """Octave-shift a pitch into the playable melody range."""
    while midi < lo:
        midi += 12
    while midi > hi:
        midi -= 12
    return midi


def _pos_cost(pos):
    s, f = pos
    cost = 0.10 * f                 # prefer lower frets
    if f == 0:
        cost -= 0.20                # open strings ring nicely
    return cost


def _trans_cost(a, b):
    return abs(a[1] - b[1]) + 0.5 * abs(a[0] - b[0])


def finger_melody(notes):
    """Choose (string, fret) per melody note via shortest-path DP.

    Returns a list of ``(string, fret, midi)`` aligned with ``notes``.
    """
    seq = []
    for n in notes:
        m = _fold_to_range(n.midi)
        ps = _positions(m, MEL_STRINGS)
        if not ps:                  # safety: clamp onto the high e string
            f = int(max(0, min(MAX_FRET, m - OPEN[5])))
            ps = [(5, f)]
        seq.append(ps)

    n = len(seq)
    costs = [[0.0] * len(seq[i]) for i in range(n)]
    back = [[0] * len(seq[i]) for i in range(n)]
    for j, p in enumerate(seq[0]):
        costs[0][j] = _pos_cost(p)
    for i in range(1, n):
        for j, p in enumerate(seq[i]):
            best_c, best_k = None, 0
            for k, pp in enumerate(seq[i - 1]):
                c = costs[i - 1][k] + _trans_cost(pp, p)
                if best_c is None or c < best_c:
                    best_c, best_k = c, k
            costs[i][j] = best_c + _pos_cost(p)
            back[i][j] = best_k

    j = min(range(len(seq[-1])), key=lambda x: costs[-1][x])
    chosen = [None] * n
    for i in range(n - 1, -1, -1):
        s, f = seq[i][j]
        chosen[i] = (s, f, OPEN[s] + f)
        j = back[i][j]
    return chosen


# --- chord voicings --------------------------------------------------------

def chord_voicing(span, pos_center, level):
    """Build a low->high voicing of (string, fret, midi) on the bass strings."""
    pcs = set(theory.chord_pcs(span.root_pc, span.quality))
    root = span.root_pc
    voicing = []

    bass = None
    for s in (0, 1, 2):                         # root in the bass if possible
        for fret in range(0, 8):
            if (OPEN[s] + fret) % 12 == root:
                bass = (s, fret, OPEN[s] + fret)
                break
        if bass:
            break
    if bass is None:                            # fall back to any chord tone
        for s in (0, 1, 2):
            for fret in range(0, 8):
                if (OPEN[s] + fret) % 12 in pcs:
                    bass = (s, fret, OPEN[s] + fret)
                    break
            if bass:
                break
    if bass is None:
        bass = (0, 0, OPEN[0])
    voicing.append(bass)

    n_upper = 2 if level == "easy" else 3
    for s in range(bass[0] + 1, HARM_MAX_STRING + 1):
        best = None
        for fret in range(0, MAX_FRET + 1):
            if (OPEN[s] + fret) % 12 in pcs:
                cost = abs(fret - pos_center)
                if best is None or cost < best[0]:
                    best = (cost, (s, fret, OPEN[s] + fret))
        if best:
            voicing.append(best[1])
        if len(voicing) >= 1 + n_upper:
            break
    return voicing


# --- assembling the arrangement -------------------------------------------

_BASE_VEL = {"easy": 70, "normal": 74, "professional": 78}


def _emit(out, start, dur, note, vel, voice="acc"):
    s, f, m = note
    out.append(PluckEvent(start=start, duration=dur, string=s, fret=f,
                          midi=m, velocity=int(max(1, min(127, vel))),
                          voice=voice))


def _emit_voice(out, span, voicing, off, dur, code, vel):
    start = span.start + off
    low = voicing[0]
    uppers = voicing[1:]
    if code == "b":
        _emit(out, start, dur, low, vel + 6, "bass")
    elif code == "b2":
        _emit(out, start, dur, uppers[0] if uppers else low, vel, "bass")
    elif code in ("1", "2", "3"):
        idx = int(code)
        note = voicing[idx] if idx < len(voicing) else voicing[-1]
        _emit(out, start, dur, note, vel)
    elif code == "c":
        for i, note in enumerate(uppers):
            _emit(out, start + 0.005 * i, dur, note, vel)
    elif code == "S":                           # strum: stagger low->high
        for i, note in enumerate(voicing):
            _emit(out, start + 0.012 * i, dur, note, vel + (6 if i == 0 else 0))


def arrange(melody, spans, level, style):
    """Return a time-sorted list of :class:`PluckEvent` for the whole piece."""
    events = []
    mel_pos = finger_melody(melody.notes)

    for n, (s, f, m) in zip(melody.notes, mel_pos):
        events.append(PluckEvent(start=n.start, duration=n.duration, string=s,
                                 fret=f, midi=m,
                                 velocity=min(120, n.velocity + 6), voice="mel"))

    base_vel = _BASE_VEL.get(level, 74)
    for span in spans:
        frets = [p[1] for nt, p in zip(melody.notes, mel_pos)
                 if nt.start < span.end and nt.end > span.start]
        pos_center = max(0, min(7, (round(sum(frets) / len(frets)) - 2)
                                if frets else 0))
        voicing = chord_voicing(span, pos_center, level)
        for off, dur, code in style.events(level, span.duration):
            _emit_voice(events, span, voicing, off, dur, code, base_vel)

    events.sort(key=lambda e: (e.start, e.string))
    return events
