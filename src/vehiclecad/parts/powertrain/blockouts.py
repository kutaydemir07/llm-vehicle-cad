from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center, cylinder_x
from vehiclecad.params.vehicle import VehicleParams


def make_engine_or_motor(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    if params.powertrain.is_ev:
        return cylinder_x((arch.front_axle_x - 180, 0.0, params.wheels.tire_radius + 110), 145, 360)
    return box_from_center((arch.front_axle_x + 90, 0.0, params.wheels.tire_radius + 210), (520, 420, 430))


def make_transmission(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.front_axle_x - 360, 0.0, params.wheels.tire_radius + 110), (340, 250, 210))


def make_driveshaft(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    z = params.wheels.tire_radius + 40
    return cylinder_x((arch.rear_axle_x / 2.0, 0.0, z), 28, abs(arch.rear_axle_x) * 0.82)


def make_differential(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.rear_axle_x + 90, 0.0, params.wheels.tire_radius + 20), (230, 260, 180))


def make_battery_pack(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.rear_axle_x / 2.0, 0.0, arch.ground_clearance + 95), (arch.wheelbase * 0.60, arch.overall_width * 0.58, 150))

