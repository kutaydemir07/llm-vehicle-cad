"""V-model System 8000 - Electrical / Electronics (battery, ECU/fusebox, harness)."""
from __future__ import annotations

from . import battery_alternator, ecu_fusebox, wiring_harness


def parts():
    out = []
    out.extend(battery_alternator.parts())
    out.extend(ecu_fusebox.parts())
    out.extend(wiring_harness.parts())
    return out
