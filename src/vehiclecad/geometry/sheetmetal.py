from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center


def flat_panel(
    center: tuple[float, float, float],
    length: float,
    width: float,
    thickness: float,
) -> cq.Workplane:
    return box_from_center(center, (length, width, thickness))


def flanged_panel(
    center: tuple[float, float, float],
    length: float,
    width: float,
    thickness: float,
    flange_height: float,
) -> cq.Workplane:
    panel = flat_panel(center, length, width, thickness)
    x, y, z = center
    flange_front = box_from_center((x + length / 2.0, y, z + flange_height / 2.0), (thickness, width, flange_height))
    flange_rear = box_from_center((x - length / 2.0, y, z + flange_height / 2.0), (thickness, width, flange_height))
    return panel.union(flange_front).union(flange_rear)

