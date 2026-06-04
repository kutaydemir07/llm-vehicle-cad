"""V-model System 7000 - Thermal / HVAC (engine cooling + cabin HVAC)."""
from __future__ import annotations

from . import cooling_system, hvac_blower


def parts():
    out = []
    out.extend(cooling_system.parts())
    out.extend(hvac_blower.parts())
    return out
