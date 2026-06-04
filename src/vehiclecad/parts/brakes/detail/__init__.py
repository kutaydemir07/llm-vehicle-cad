"""V-model System 5000 - Brakes (pedal/booster/master, lines, F/R corners, handbrake)."""
from __future__ import annotations

from . import (brake_booster_master, brake_lines, front_calipers_rotors,
               handbrake_assembly, rear_calipers_rotors)


def parts():
    out = []
    out.extend(brake_booster_master.parts())
    out.extend(brake_lines.parts())
    out.extend(front_calipers_rotors.parts())
    out.extend(handbrake_assembly.parts())
    out.extend(rear_calipers_rotors.parts())
    return out
