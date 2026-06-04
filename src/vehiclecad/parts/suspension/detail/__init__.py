"""V-model System 3000 - Suspension (front MacPherson + rear semi-trailing).

The struts/springs/LCAs/knuckles come from ``front_macpherson`` and the rear
hubs/trailing arms from ``rear_semitrailing``; ``strut``/``hub``/``control_arm``/
``trailing_arm`` remain as re-export facades and are intentionally not called.
"""
from __future__ import annotations

from . import antiroll_bars, front_macpherson, misc, rear_semitrailing


def parts():
    out = []
    out.extend(antiroll_bars.parts())
    out.extend(front_macpherson.parts())   # struts, springs, LCAs, knuckles
    out.extend(misc.parts())
    out.extend(rear_semitrailing.parts())  # rear hubs, trailing arms
    return out
