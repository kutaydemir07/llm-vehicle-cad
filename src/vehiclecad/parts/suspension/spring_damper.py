from __future__ import annotations

import cadquery as cq
from cadquery import Solid, Vector

from vehiclecad.geometry.primitives import as_workplane, cylinder_between


def make_damper(
    lower: tuple[float, float, float],
    upper: tuple[float, float, float],
) -> cq.Workplane:
    body = cylinder_between(lower, upper, 18.0)
    shaft = cylinder_between(lower, upper, 7.0)
    return body.union(shaft)


def make_coil_spring(
    center: tuple[float, float, float],
    radius: float,
    wire_radius: float,
    height: float,
    turns: int = 5,
) -> cq.Workplane:
    cx, cy, cz = center
    rings = []
    for index in range(turns):
        z = cz - height / 2.0 + (index + 0.5) * height / turns
        rings.append(Solid.makeTorus(radius, wire_radius, Vector(cx, cy, z), Vector(0, 0, 1)))
    result = rings[0]
    for ring in rings[1:]:
        result = result.fuse(ring)
    return as_workplane(result)

