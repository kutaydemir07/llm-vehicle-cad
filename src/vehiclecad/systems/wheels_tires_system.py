from __future__ import annotations

import cadquery as cq

from vehiclecad.core.coordinates import Axle, Side
from vehiclecad.subassemblies.wheel_corner import make_wheel_corner
from vehiclecad.params.vehicle import VehicleParams


def make_wheels_tires_system(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="A0_wheels_tires")
    for axle in (Axle.FRONT, Axle.REAR):
        for side in (Side.LEFT, Side.RIGHT):
            assy.add(make_wheel_corner(params, side, axle), name=f"{axle.code}{side.code}_wheel_corner")
    return assy

