from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center


def shell_box(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
    wall: float,
) -> cq.Workplane:
    dx, dy, dz = size
    inner_size = (dx - 2 * wall, dy - 2 * wall, dz - 2 * wall)
    outer = box_from_center(center, size)
    if min(inner_size) <= 0:
        return outer
    inner = box_from_center(center, inner_size)
    return outer.cut(inner)


def rounded_box(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
    radius: float,
) -> cq.Workplane:
    part = box_from_center(center, size)
    safe_radius = min(radius, min(size) * 0.45)
    try:
        return part.edges().fillet(safe_radius)
    except Exception:
        return part

