from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.params.vehicle import VehicleParams


def make_front_axle(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="front_axle")
    subframe = box_from_center((arch.front_axle_x - 40, 0.0, arch.ground_clearance + 110), (260, arch.front_track * 0.58, 70))
    assy.add(subframe, name="front_subframe", color=colors.cq_color(colors.CHASSIS))
    return assy

