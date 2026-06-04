from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.parts.suspension.links import make_a_arm, make_link
from vehiclecad.parts.suspension.spring_damper import make_coil_spring, make_damper
from vehiclecad.params.vehicle import VehicleParams


def make_suspension_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    tire_r = params.wheels.tire_radius
    assy = cq.Assembly(name="30_suspension")

    for sign, side in ((1, "left"), (-1, "right")):
        front_outer = (arch.front_axle_x, sign * (arch.front_track / 2.0 - 70), tire_r + 20)
        front_inner_a = (arch.front_axle_x + 120, sign * arch.front_track * 0.24, tire_r + 10)
        front_inner_b = (arch.front_axle_x - 170, sign * arch.front_track * 0.25, tire_r + 10)
        strut_upper = (arch.front_axle_x - 40, sign * arch.front_track * 0.34, arch.overall_height * 0.72)
        assy.add(make_a_arm(front_inner_a, front_inner_b, front_outer), name=f"front_lower_arm_{side}", color=colors.cq_color(colors.SUSPENSION))
        assy.add(make_damper(front_outer, strut_upper), name=f"front_strut_damper_{side}", color=colors.cq_color(colors.SUSPENSION))
        assy.add(make_coil_spring((strut_upper[0], strut_upper[1], (front_outer[2] + strut_upper[2]) / 2.0), 58, 7, 360), name=f"front_spring_{side}", color=colors.cq_color(colors.SUSPENSION))

        rear_outer = (arch.rear_axle_x, sign * (arch.rear_track / 2.0 - 70), tire_r + 20)
        rear_inner = (arch.rear_axle_x + 260, sign * arch.rear_track * 0.23, tire_r + 60)
        rear_damper_upper = (arch.rear_axle_x + 80, sign * arch.rear_track * 0.34, arch.overall_height * 0.66)
        assy.add(make_link(rear_inner, rear_outer, 48), name=f"rear_trailing_arm_{side}", color=colors.cq_color(colors.SUSPENSION))
        assy.add(make_damper(rear_outer, rear_damper_upper), name=f"rear_damper_{side}", color=colors.cq_color(colors.SUSPENSION))
        assy.add(make_coil_spring((arch.rear_axle_x + 130, sign * arch.rear_track * 0.33, tire_r + 240), 72, 8, 300), name=f"rear_spring_{side}", color=colors.cq_color(colors.SUSPENSION))

    return assy

