from __future__ import annotations

import cadquery as cq
from cadquery import Solid, Vector

from vehiclecad.geometry.primitives import as_workplane
from vehiclecad.params.wheels import WheelsParams


def make_tire(params: WheelsParams) -> cq.Workplane:
    tube_radius = params.tire_width * 0.34
    major_radius = max(params.tire_radius - tube_radius, params.wheel_radius + tube_radius * 0.30)
    tire = Solid.makeTorus(major_radius, tube_radius, Vector(0, 0, 0), Vector(0, 1, 0))
    groove_a = Solid.makeTorus(major_radius, tube_radius * 0.08, Vector(0, 0, 0), Vector(0, 1, 0))
    return as_workplane(tire.cut(groove_a))

