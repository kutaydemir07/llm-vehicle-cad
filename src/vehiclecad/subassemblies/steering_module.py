from __future__ import annotations

import cadquery as cq

from vehiclecad.parts.steering.rack import make_steering_rack
from vehiclecad.params.vehicle import VehicleParams


def make_steering_module(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="steering_module")
    assy.add(make_steering_rack(params), name="steering_rack")
    return assy

