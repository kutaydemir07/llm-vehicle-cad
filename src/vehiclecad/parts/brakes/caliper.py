from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center, cylinder_y


def make_caliper(disc_diameter: float, piston_count: int = 4) -> cq.Workplane:
    radius = disc_diameter / 2.0
    body = box_from_center((radius * 0.92, -72, 0), (52, 58, 116))
    bridge = box_from_center((radius * 0.72, -72, 0), (42, 68, 72))
    caliper = body.union(bridge)
    spacing = 24 if piston_count >= 4 else 0
    for z in (-spacing, spacing) if piston_count >= 4 else (0,):
        caliper = caliper.union(cylinder_y((radius * 0.94, -44, z), 13, 10))
    return caliper

