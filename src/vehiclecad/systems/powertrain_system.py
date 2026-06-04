from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.tubes import tube_path
from vehiclecad.subassemblies.powertrain_module import make_powertrain_module
from vehiclecad.params.vehicle import VehicleParams


def make_powertrain_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="60_powertrain")
    assy.add(make_powertrain_module(params), name="powertrain_module")
    if not params.powertrain.is_ev:
        exhaust = tube_path(
            [
                (arch.front_axle_x + 80, -250, params.wheels.tire_radius + 120),
                (arch.rear_axle_x * 0.30, -260, params.wheels.tire_radius + 50),
                (arch.rear_axle_x * 0.78, -300, params.wheels.tire_radius + 70),
                (arch.rear_bumper_x + 160, -320, params.wheels.tire_radius + 120),
            ],
            46,
        )
        assy.add(exhaust, name="exhaust_or_hv_routing", color=colors.cq_color((0.42, 0.36, 0.30)))
    return assy

