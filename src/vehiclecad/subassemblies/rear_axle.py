from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.params.vehicle import VehicleParams


def make_rear_axle(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="rear_axle")
    subframe = box_from_center((arch.rear_axle_x + 30, 0.0, arch.ground_clearance + 120), (320, arch.rear_track * 0.55, 78))
    assy.add(subframe, name="rear_subframe", color=colors.cq_color(colors.CHASSIS))
    return assy

