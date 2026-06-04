from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.parts.steering.rack import make_steering_rack, make_tie_rod
from vehiclecad.params.vehicle import VehicleParams


def make_steering_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    tire_r = params.wheels.tire_radius
    assy = cq.Assembly(name="40_steering")
    assy.add(make_steering_rack(params), name="rack", color=colors.cq_color(colors.STEEL))
    for sign, side in ((1, "left"), (-1, "right")):
        inner = (arch.front_axle_x + 40, sign * arch.front_track * 0.27, tire_r + 80)
        outer = (arch.front_axle_x, sign * (arch.front_track / 2.0 - 78), tire_r + 45)
        assy.add(make_tie_rod(inner, outer), name=f"tie_rod_{side}", color=colors.cq_color(colors.STEEL))
    column = make_tie_rod((arch.front_axle_x - arch.wheelbase * 0.15, -170, tire_r + 480), (arch.front_axle_x + 50, -80, tire_r + 120))
    assy.add(column, name="steering_column", color=colors.cq_color(colors.STEEL))
    return assy

