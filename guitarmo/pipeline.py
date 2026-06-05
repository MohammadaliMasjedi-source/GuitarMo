"""End-to-end orchestration: a vocal recording in, a guitar arrangement out."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from . import notation
from .arrange import arrange
from .audio_io import load_audio, save_wav
from .harmony import harmonize
from .key import detect_key
from .render import render
from .styles import LEVELS, get_style, style_names
from .transcribe import transcribe

__all__ = ["process", "Result", "list_styles", "LEVELS"]


@dataclass
class Result:
    out_dir: str
    wav_path: str
    midi_path: str
    tab_path: str
    tab_text: str
    key_name: str
    tempo: float
    style: str
    level: str
    n_notes: int
    chords: list = field(default_factory=list)
    musicxml_path: str | None = None

    def summary(self) -> str:
        return (f"Key: {self.key_name} | Tempo: {self.tempo:.0f} BPM | "
                f"{self.n_notes} notes | Style: {self.style} | Level: {self.level}\n"
                f"Progression: {'  '.join(self.chords)}")


def list_styles():
    """Return ``{name: {'display':..., 'description':...}}`` for the UI/CLI."""
    from .styles import STYLES
    return {n: {"display": s.display, "description": s.description}
            for n, s in STYLES.items()}


def _build_header(key, melody, style, level, chords):
    bar = "=" * 64
    return (
        f"{bar}\n"
        f"  GuitarMo  -  classical-guitar arrangement\n"
        f"{bar}\n"
        f"  Key   : {key.name}\n"
        f"  Tempo : {melody.tempo:.0f} BPM   ({melody.n_bars} bars, 4/4)\n"
        f"  Style : {style.display}\n"
        f"  Level : {level}\n"
        f"  Chords: {'  '.join(chords)}\n"
        f"{bar}\n"
        f"  Legend: melody on e/B strings, accompaniment on G/D/A/E.\n"
        f"          numbers = fret; '|' = barline. (tab quantized to 1/8)\n"
        f"{bar}"
    )


def process(audio_path, style="classical", level="normal", out_dir=None,
            sr=22050, tempo=None, reverb=True):
    """Run the full pipeline and write wav / midi / musicxml / tab to disk.

    Returns a :class:`Result`.
    """
    if level not in LEVELS:
        raise ValueError(f"level must be one of {LEVELS}, got {level!r}")
    style_obj = get_style(style)

    y, sr = load_audio(audio_path, sr=sr)
    melody = transcribe(y, sr, tempo=tempo)
    key = detect_key(melody.notes)
    spans = harmonize(melody, key, level=level, style=style_obj)
    events = arrange(melody, spans, level=level, style=style_obj)

    audio_out, out_sr = render(events, melody.tempo, reverb=reverb)

    stem = Path(audio_path).stem
    out_dir = Path(out_dir) if out_dir else Path("out") / f"{stem}_{style}_{level}"
    out_dir.mkdir(parents=True, exist_ok=True)

    wav_path = out_dir / "arrangement.wav"
    midi_path = out_dir / "arrangement.mid"
    tab_path = out_dir / "tab.txt"
    xml_path = out_dir / "score.musicxml"

    save_wav(wav_path, audio_out, out_sr)
    notation.to_midi(events, melody.tempo, midi_path)

    chords = [s.label for s in spans]
    header = _build_header(key, melody, style_obj, level, chords)
    tab_text = notation.to_ascii_tab(events, melody.tempo,
                                     beats_per_bar=melody.beats_per_bar,
                                     header=header)
    tab_path.write_text(tab_text, encoding="utf-8")

    mel_notes = [(e.start, e.duration, e.midi) for e in events if e.voice == "mel"]
    xml_ok = notation.to_musicxml(mel_notes, spans, key, melody.tempo, xml_path)

    return Result(
        out_dir=str(out_dir),
        wav_path=str(wav_path),
        midi_path=str(midi_path),
        tab_path=str(tab_path),
        tab_text=tab_text,
        key_name=key.name,
        tempo=melody.tempo,
        style=style_obj.display,
        level=level,
        n_notes=len(melody.notes),
        chords=chords,
        musicxml_path=str(xml_path) if xml_ok else None,
    )
