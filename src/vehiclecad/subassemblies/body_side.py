from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.params.vehicle import VehicleParams


def make_body_side(params: VehicleParams, side_sign: int) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="body_side_left" if side_sign > 0 else "body_side_right")
    sill = box_from_center((arch.body_center_x, side_sign * arch.overall_width * 0.47, arch.ground_clearance + 100), (arch.body_length * 0.62, 70, 150))
    assy.add(sill, name="rocker_sill", color=colors.cq_color(colors.BODY_RED))
    return assy

