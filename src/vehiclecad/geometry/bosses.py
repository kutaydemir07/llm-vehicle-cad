from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import cylinder_z


def boss_z(
    center: tuple[float, float, float],
    outer_diameter: float,
    height: float,
    hole_diameter: float | None = None,
) -> cq.Workplane:
    boss = cylinder_z(center, outer_diameter / 2.0, height)
    if hole_diameter is not None:
        boss = boss.faces(">Z").workplane().hole(hole_diameter)
    return boss

