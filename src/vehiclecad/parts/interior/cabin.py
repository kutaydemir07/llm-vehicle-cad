from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.geometry.tubes import tube_path
from vehiclecad.params.vehicle import VehicleParams


def make_dashboard(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.front_axle_x - arch.wheelbase * 0.22, 0.0, params.wheels.tire_radius + 430), (120, arch.overall_width * 0.70, 160))


def make_seat(params: VehicleParams, x: float, y: float) -> cq.Workplane:
    base = box_from_center((x, y, params.wheels.tire_radius + 105), (360, 280, 90))
    back = box_from_center((x - 115, y, params.wheels.tire_radius + 280), (80, 280, 360))
    return base.union(back)


def make_center_console(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.rear_axle_x * 0.34, 0.0, params.wheels.tire_radius + 120), (720, 140, 120))


def make_roll_cage(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    x_front = arch.front_axle_x - arch.wheelbase * 0.30
    x_rear = arch.rear_axle_x * 0.64
    y = arch.overall_width * 0.35
    z0 = params.wheels.tire_radius + 120
    z1 = arch.overall_height * 0.92
    left = tube_path([(x_front, y, z0), (x_front, y, z1), (x_rear, y, z1), (x_rear, y, z0)], 42)
    right = tube_path([(x_front, -y, z0), (x_front, -y, z1), (x_rear, -y, z1), (x_rear, -y, z0)], 42)
    cross = tube_path([(x_front, y, z1), (x_front, -y, z1), (x_rear, y, z1), (x_rear, -y, z1)], 36)
    return left.union(right).union(cross)

