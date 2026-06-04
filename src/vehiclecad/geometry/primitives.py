from __future__ import annotations

import cadquery as cq
from cadquery import Solid, Vector


def as_workplane(shape: cq.Shape | cq.Workplane) -> cq.Workplane:
    if isinstance(shape, cq.Workplane):
        return shape
    return cq.Workplane(obj=shape)


def box_from_center(
    center: tuple[float, float, float],
    size: tuple[float, float, float],
) -> cq.Workplane:
    return cq.Workplane("XY").box(*size).translate(center)


def box_from_min(
    xyz_min: tuple[float, float, float],
    size: tuple[float, float, float],
) -> cq.Workplane:
    x, y, z = xyz_min
    dx, dy, dz = size
    return box_from_center((x + dx / 2.0, y + dy / 2.0, z + dz / 2.0), size)


def cylinder_between(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    radius: float,
) -> cq.Workplane:
    sx, sy, sz = start
    ex, ey, ez = end
    dx, dy, dz = ex - sx, ey - sy, ez - sz
    length = (dx * dx + dy * dy + dz * dz) ** 0.5
    if length <= 1e-6:
        solid = Solid.makeSphere(radius, Vector(sx, sy, sz))
    else:
        solid = Solid.makeCylinder(
            radius,
            length,
            Vector(sx, sy, sz),
            Vector(dx / length, dy / length, dz / length),
        )
    return as_workplane(solid)


def cylinder_y(center: tuple[float, float, float], radius: float, length: float) -> cq.Workplane:
    x, y, z = center
    solid = Solid.makeCylinder(radius, length, Vector(x, y - length / 2.0, z), Vector(0, 1, 0))
    return as_workplane(solid)


def cylinder_x(center: tuple[float, float, float], radius: float, length: float) -> cq.Workplane:
    x, y, z = center
    solid = Solid.makeCylinder(radius, length, Vector(x - length / 2.0, y, z), Vector(1, 0, 0))
    return as_workplane(solid)


def cylinder_z(center: tuple[float, float, float], radius: float, length: float) -> cq.Workplane:
    x, y, z = center
    solid = Solid.makeCylinder(radius, length, Vector(x, y, z - length / 2.0), Vector(0, 0, 1))
    return as_workplane(solid)


def sphere(center: tuple[float, float, float], radius: float) -> cq.Workplane:
    return as_workplane(Solid.makeSphere(radius, Vector(*center)))


def union_all(parts: list[cq.Workplane]) -> cq.Workplane:
    if not parts:
        raise ValueError("union_all needs at least one part")
    result = parts[0]
    for part in parts[1:]:
        result = result.union(part)
    return result

