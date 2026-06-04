from __future__ import annotations

import cadquery as cq


def mirror_y(part: cq.Workplane) -> cq.Workplane:
    return part.mirror("XZ")


def translate(part: cq.Workplane, xyz: tuple[float, float, float]) -> cq.Workplane:
    return part.translate(xyz)


def rotate_z(part: cq.Workplane, angle_degrees: float) -> cq.Workplane:
    return part.rotate((0, 0, 0), (0, 0, 1), angle_degrees)

