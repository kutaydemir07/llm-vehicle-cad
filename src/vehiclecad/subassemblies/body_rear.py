from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.params.vehicle import VehicleParams


def make_body_rear(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="body_rear")
    bumper = box_from_center((arch.rear_bumper_x + 95, 0.0, arch.ground_clearance + 220), (190, arch.overall_width * 0.84, 190))
    assy.add(bumper, name="rear_bumper", color=colors.cq_color(colors.BODY_RED))
    return assy

