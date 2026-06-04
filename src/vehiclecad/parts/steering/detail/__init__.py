"""V-model System 4000 - Steering (rack, column, EPS, wheel)."""
from __future__ import annotations

from . import steering_rack, steering_column, power_steering, steering


def parts():
    out = []
    out.extend(steering_rack.parts())
    out.extend(steering_column.parts())
    out.extend(power_steering.parts())
    out.extend(steering.parts())           # steering wheel
    return out
