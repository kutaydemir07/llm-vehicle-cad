from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.parts.chassis.rails import make_crossmember, make_longitudinal_rail
from vehiclecad.subassemblies.front_axle import make_front_axle
from vehiclecad.subassemblies.rear_axle import make_rear_axle
from vehiclecad.params.vehicle import VehicleParams


def make_chassis_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="20_chassis")
    assy.add(make_longitudinal_rail(params, 1), name="left_longitudinal_rail", color=colors.cq_color(colors.CHASSIS))
    assy.add(make_longitudinal_rail(params, -1), name="right_longitudinal_rail", color=colors.cq_color(colors.CHASSIS))
    for name, x in {
        "front_crossmember": arch.front_axle_x,
        "center_crossmember": arch.rear_axle_x * 0.50,
        "rear_crossmember": arch.rear_axle_x,
    }.items():
        assy.add(make_crossmember(params, x), name=name, color=colors.cq_color(colors.CHASSIS))
    assy.add(make_front_axle(params), name="front_subframe")
    assy.add(make_rear_axle(params), name="rear_subframe")
    return assy

