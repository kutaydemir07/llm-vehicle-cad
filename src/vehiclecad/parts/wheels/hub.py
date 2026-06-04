from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.patterns import polar_points
from vehiclecad.geometry.primitives import cylinder_y
from vehiclecad.params.wheels import WheelsParams


def make_hub(params: WheelsParams) -> cq.Workplane:
    flange = cylinder_y((0, -24, 0), params.center_bore * 0.78, 28.0)
    bearing = cylinder_y((0, -48, 0), params.center_bore * 0.46, 54.0)
    hub = flange.union(bearing)
    for x, z in polar_points(params.bolt_count, params.pcd / 2.0, start_angle_degrees=90.0):
        hub = hub.union(cylinder_y((x, -4, z), 4.5, 32.0))
    return hub

