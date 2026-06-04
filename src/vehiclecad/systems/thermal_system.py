from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.tubes import tube_path
from vehiclecad.subassemblies.thermal_module import make_thermal_module
from vehiclecad.params.vehicle import VehicleParams


def make_thermal_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="70_thermal")
    assy.add(make_thermal_module(params), name="radiator_fan_module")
    coolant = tube_path(
        [
            (arch.front_bumper_x * 0.38, 170, params.wheels.tire_radius + 150),
            (arch.front_axle_x + 130, 170, params.wheels.tire_radius + 180),
            (arch.front_axle_x + 80, 0.0, params.wheels.tire_radius + 280),
        ],
        32,
    )
    assy.add(coolant, name="coolant_lines", color=colors.cq_color(colors.THERMAL))
    return assy

