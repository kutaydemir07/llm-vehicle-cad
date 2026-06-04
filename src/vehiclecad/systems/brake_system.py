from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.tubes import tube_path
from vehiclecad.subassemblies.brake_module import make_brake_module
from vehiclecad.params.vehicle import VehicleParams


def make_brake_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    tire_r = params.wheels.tire_radius
    assy = cq.Assembly(name="50_brakes")
    assy.add(make_brake_module(params), name="pedal_booster_module")
    line = tube_path(
        [
            (arch.front_axle_x - arch.wheelbase * 0.16, -190, tire_r + 230),
            (arch.front_axle_x, 0.0, tire_r + 120),
            (arch.rear_axle_x * 0.50, 0.0, tire_r + 95),
            (arch.rear_axle_x, 0.0, tire_r + 95),
        ],
        8,
    )
    assy.add(line, name="hydraulic_main_line", color=colors.cq_color(colors.BRAKE))
    return assy

