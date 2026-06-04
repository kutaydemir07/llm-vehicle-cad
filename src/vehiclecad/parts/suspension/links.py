from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.tubes import tube_between


def make_link(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    diameter: float = 34.0,
) -> cq.Workplane:
    return tube_between(start, end, diameter)


def make_a_arm(
    inner_front: tuple[float, float, float],
    inner_rear: tuple[float, float, float],
    outer: tuple[float, float, float],
    diameter: float = 32.0,
) -> cq.Workplane:
    return (
        tube_between(inner_front, outer, diameter)
        .union(tube_between(inner_rear, outer, diameter))
        .union(tube_between(inner_front, inner_rear, diameter * 0.75))
    )

