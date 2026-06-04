from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center, cylinder_x
from vehiclecad.params.vehicle import VehicleParams


def make_radiator(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center(
        (arch.front_bumper_x * 0.40, 0.0, params.wheels.tire_radius + 170),
        (params.thermal.radiator_thickness, params.thermal.radiator_width, params.thermal.radiator_height),
    )


def make_fan(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return cylinder_x((arch.front_bumper_x * 0.32, 0.0, params.wheels.tire_radius + 170), 120, 36)

