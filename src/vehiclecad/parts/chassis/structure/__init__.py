"""V-model System 2000 - Chassis (subframes + underbody crossmembers)."""
from __future__ import annotations

from . import crossmembers, subframe


def parts():
    out = []
    out.extend(crossmembers.parts())
    out.extend(subframe.parts())
    return out
