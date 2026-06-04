from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.patterns import polar_points
from vehiclecad.geometry.primitives import cylinder_y


def make_brake_disc(diameter: float) -> cq.Workplane:
    disc = cylinder_y((0, -72, 0), diameter / 2.0, 24.0)
    hat_cut = cylinder_y((0, -72, 0), diameter * 0.22, 30.0)
    disc = disc.cut(hat_cut)
    hat = cylinder_y((0, -58, 0), diameter * 0.24, 32.0)
    disc = disc.union(hat)
    for x, z in polar_points(12, diameter * 0.39, start_angle_degrees=7.0):
        disc = disc.cut(cylinder_y((x, -72, z), 3.5, 34.0))
    return disc

