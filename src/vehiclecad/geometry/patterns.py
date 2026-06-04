from __future__ import annotations

import math


def polar_points(
    count: int,
    radius: float,
    start_angle_degrees: float = 0.0,
) -> list[tuple[float, float]]:
    if count <= 0:
        raise ValueError("count must be positive")
    points = []
    for index in range(count):
        angle = math.radians(start_angle_degrees + index * 360.0 / count)
        points.append((radius * math.cos(angle), radius * math.sin(angle)))
    return points

