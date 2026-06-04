from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.geometry.tubes import tube_between
from vehiclecad.params.vehicle import VehicleParams


def make_longitudinal_rail(params: VehicleParams, side_sign: int) -> cq.Workplane:
    arch = params.architecture
    y = side_sign * arch.overall_width * 0.31
    z = arch.ground_clearance + 80
    return tube_between((arch.front_bumper_x * 0.60, y, z), (arch.rear_bumper_x * 0.90, y, z), 70)


def make_crossmember(params: VehicleParams, x: float, name_width_factor: float = 0.70) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((x, 0.0, arch.ground_clearance + 125), (80, arch.overall_width * name_width_factor, 64))

