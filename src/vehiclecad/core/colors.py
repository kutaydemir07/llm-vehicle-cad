from __future__ import annotations

import cadquery as cq


STEEL = (0.40, 0.42, 0.45)
ALUMINUM = (0.66, 0.68, 0.70)
RUBBER = (0.04, 0.04, 0.045)
GLASS = (0.32, 0.54, 0.72, 0.42)
BODY_RED = (0.78, 0.05, 0.03)
BODY_BLUE = (0.04, 0.20, 0.72)
BODY_WHITE = (0.88, 0.88, 0.84)
BODY_GREY = (0.34, 0.36, 0.38)
DATUM_YELLOW = (0.95, 0.82, 0.12)
CHASSIS = (0.24, 0.27, 0.30)
SUSPENSION = (0.18, 0.32, 0.22)
BRAKE = (0.70, 0.18, 0.12)
POWERTRAIN = (0.24, 0.24, 0.27)
THERMAL = (0.10, 0.30, 0.55)
ELECTRICAL = (0.95, 0.65, 0.06)
INTERIOR = (0.10, 0.10, 0.11)
FASTENER = (0.72, 0.72, 0.70)


def cq_color(rgb: tuple[float, ...]) -> cq.Color:
    if len(rgb) == 4:
        return cq.Color(rgb[0], rgb[1], rgb[2], rgb[3])
    return cq.Color(rgb[0], rgb[1], rgb[2])

