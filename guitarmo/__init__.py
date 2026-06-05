"""GuitarMo -- sing a melody, get a classical-guitar arrangement.

Public API::

    from guitarmo import process
    result = process("humming.wav", style="classical", level="normal")
    print(result.tab_text)

See :mod:`guitarmo.pipeline` for the orchestration and ``app.py`` for the web UI.
"""

__version__ = "0.1.0"

from .core import ChordSpan, Melody, Note, PluckEvent, STANDARD_TUNING  # noqa: F401
from .key import Key, detect_key  # noqa: F401

# The pipeline pulls in librosa / music21; import lazily-friendly but eager here
# since those are declared runtime dependencies.
from .pipeline import LEVELS, Result, list_styles, process  # noqa: F401, E402

__all__ = [
    "process", "Result", "list_styles", "LEVELS",
    "Note", "Melody", "ChordSpan", "PluckEvent", "STANDARD_TUNING",
    "Key", "detect_key", "__version__",
]
