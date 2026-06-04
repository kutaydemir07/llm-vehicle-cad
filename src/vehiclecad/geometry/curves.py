from __future__ import annotations

import cadquery as cq


def polyline_path(points: list[tuple[float, float]]) -> cq.Workplane:
    if len(points) < 2:
        raise ValueError("polyline_path needs at least two points")
    return cq.Workplane("XY").polyline(points)

