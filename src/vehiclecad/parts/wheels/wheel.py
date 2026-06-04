from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.patterns import polar_points
from vehiclecad.geometry.primitives import cylinder_y
from vehiclecad.params.wheels import WheelsParams


def make_wheel(params: WheelsParams) -> cq.Workplane:
    width = params.tire_width * 0.68
    outer = cylinder_y((0, 0, 0), params.wheel_radius, width)
    inner = cylinder_y((0, 0, 0), params.center_bore / 2.0, width + 8.0)
    wheel = outer.cut(inner)

    face = cylinder_y((0, width * 0.32, 0), params.wheel_radius * 0.82, 14.0)
    hub_pad = cylinder_y((0, width * 0.42, 0), params.center_bore * 0.72, 18.0)
    wheel = wheel.union(face).union(hub_pad)

    for x, z in polar_points(params.bolt_count, params.pcd / 2.0, start_angle_degrees=90.0):
        wheel = wheel.cut(cylinder_y((x, width * 0.44, z), 5.5, 26.0))
    return wheel

