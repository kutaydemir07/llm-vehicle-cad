"""Detailed I4_EngineB23 engine block geometry - defers to engine.py.

This module provides a more granular breakdown of the engine block for the
STEP hierarchy, while engine.py provides the top-level assembly function.
"""
from .engine import _engine_block as _eb


def parts():
    return _eb()
