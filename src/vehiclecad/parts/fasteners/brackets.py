from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.holes import apply_hole_pattern
from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.interfaces.hole_patterns import HolePattern, rectangular_four_bolt_pattern


def make_mounting_plate(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
    pattern: HolePattern | None = None,
) -> cq.Workplane:
    plate = box_from_center(center, size)
    if pattern is not None:
        plate = apply_hole_pattern(plate, pattern)
    return plate


def make_default_four_bolt_plate(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
    hole_diameter: float,
) -> cq.Workplane:
    pattern = rectangular_four_bolt_pattern("default_four_bolt", size[0] * 0.55, size[1] * 0.55, hole_diameter)
    return make_mounting_plate(center, size, pattern)

