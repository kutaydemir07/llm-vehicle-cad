from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.geometry.tubes import tube_path
from vehiclecad.params.vehicle import VehicleParams


def make_lv_battery(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.front_axle_x + 250, -arch.overall_width * 0.27, params.wheels.tire_radius + 160), (220, 150, 160))


def make_fuse_box(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.front_axle_x - 60, arch.overall_width * 0.24, params.wheels.tire_radius + 190), (170, 130, 70))


def make_main_harness(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    points = [
        (arch.front_axle_x + 250, -arch.overall_width * 0.27, params.wheels.tire_radius + 200),
        (arch.front_axle_x - 100, 0.0, params.wheels.tire_radius + 240),
        (arch.rear_axle_x * 0.55, 0.0, params.wheels.tire_radius + 260),
        (arch.rear_axle_x + 120, arch.overall_width * 0.18, params.wheels.tire_radius + 180),
    ]
    return tube_path(points, 18)

