from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import cylinder_between, sphere


def tube_between(
    start: tuple[float, float, float],
    end: tuple[float, float, float],
    outer_diameter: float,
) -> cq.Workplane:
    return cylinder_between(start, end, outer_diameter / 2.0)


def tube_path(
    points: list[tuple[float, float, float]],
    outer_diameter: float,
    smooth_joints: bool = True,
) -> cq.Workplane:
    if len(points) < 2:
        raise ValueError("tube_path needs at least two points")
    radius = outer_diameter / 2.0
    result = cylinder_between(points[0], points[1], radius)
    for index in range(1, len(points) - 1):
        result = result.union(cylinder_between(points[index], points[index + 1], radius))
        if smooth_joints:
            result = result.union(sphere(points[index], radius * 1.03))
    return result


def swept_tube(path: cq.Workplane, outer_diameter: float) -> cq.Workplane:
    section = cq.Workplane("YZ").circle(outer_diameter / 2.0)
    return section.sweep(path)

