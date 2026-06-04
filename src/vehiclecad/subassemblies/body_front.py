from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.params.vehicle import VehicleParams


def make_body_front(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="body_front")
    bumper = box_from_center((arch.front_bumper_x - 90, 0.0, arch.ground_clearance + 210), (180, arch.overall_width * 0.86, 190))
    assy.add(bumper, name="front_bumper", color=colors.cq_color(colors.BODY_RED))
    return assy

