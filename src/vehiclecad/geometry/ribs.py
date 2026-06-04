from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center


def straight_rib(
    center: tuple[float, float, float],
    length: float,
    thickness: float,
    height: float,
    axis: str = "x",
) -> cq.Workplane:
    if axis.lower() == "x":
        size = (length, thickness, height)
    elif axis.lower() == "y":
        size = (thickness, length, height)
    else:
        raise ValueError("axis must be 'x' or 'y'")
    return box_from_center(center, size)

