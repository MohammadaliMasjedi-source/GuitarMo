"""GuitarMo web app -- sing or upload a melody, get a classical-guitar arrangement.

Run::

    python app.py

then open the printed local URL. Record straight from the browser, choose a
style and a difficulty level, and download the tab / MIDI / audio.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr

from guitarmo import LEVELS, list_styles, process

_STYLES = list_styles()
_STYLE_CHOICES = [(meta["display"], name) for name, meta in _STYLES.items()]

_INTRO = """
# 🎸 GuitarMo
**Sing a melody → get a classical-guitar arrangement.**
Record (or upload) a short, clear melody, pick a *style* and a *difficulty
level*, and GuitarMo transcribes your pitch, finds the key, harmonizes it, and
plays it back on a synthesized nylon-string guitar — with tab, MIDI and sheet
music to download.
"""

_TIPS = """
**Tips for a good result**
- Sing one clear note at a time, fairly close to the mic.
- A simple, sustained tune works best (think nursery rhyme).
- WAV uploads are the most reliable input format.
"""


def run(audio_path, style, level):
    if not audio_path:
        raise gr.Error("Please record or upload a short sung melody first.")
    try:
        res = process(audio_path, style=style, level=level)
    except ValueError as exc:
        raise gr.Error(str(exc))

    info = (f"### {res.key_name}  ·  {res.tempo:.0f} BPM  ·  {res.n_notes} notes\n"
            f"**Style:** {res.style}  **Level:** {res.level}\n\n"
            f"**Progression:**  {'  '.join(res.chords)}")
    downloads = [p for p in (res.midi_path, res.musicxml_path, res.tab_path) if p]
    return res.wav_path, res.tab_text, info, downloads


def build():
    with gr.Blocks(title="GuitarMo", theme=gr.themes.Soft()) as demo:
        gr.Markdown(_INTRO)
        with gr.Row():
            with gr.Column(scale=1):
                audio = gr.Audio(sources=["microphone", "upload"],
                                 type="filepath", label="Your melody")
                style = gr.Dropdown(_STYLE_CHOICES, value="classical",
                                    label="Style")
                level = gr.Radio(list(LEVELS), value="normal",
                                 label="Difficulty")
                go = gr.Button("🎼 Arrange it", variant="primary")
                gr.Markdown(_TIPS)
            with gr.Column(scale=2):
                info = gr.Markdown()
                out_audio = gr.Audio(label="Guitar arrangement", type="filepath")
                tab = gr.Code(label="Tablature", language=None)
                files = gr.File(label="Downloads (MIDI · MusicXML · tab)",
                                file_count="multiple")
        go.click(run, inputs=[audio, style, level],
                 outputs=[out_audio, tab, info, files])
    return demo


if __name__ == "__main__":
    build().launch()
