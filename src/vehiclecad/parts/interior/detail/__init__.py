"""V-model System 9000 - Interior (dash, console, seats, trim, pedals, cage).

The steering wheel moved to System 4000 (Steering); it is not called here.
"""
from __future__ import annotations

from . import (carpets_headliner, center_console, dashboard, door_panels,
               pedal_box, roll_cage, seat, seats_front, seats_rear)


def parts():
    out = []
    out.extend(carpets_headliner.parts())
    out.extend(center_console.parts())
    out.extend(dashboard.parts())
    out.extend(door_panels.parts())
    out.extend(pedal_box.parts())
    out.extend(roll_cage.parts())
    out.extend(seat.parts())
    out.extend(seats_front.parts())
    out.extend(seats_rear.parts())
    return out
