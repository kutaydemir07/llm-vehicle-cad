from __future__ import annotations

import cadquery as cq

from vehiclecad.parts.thermal.cooling import make_fan, make_radiator
from vehiclecad.params.vehicle import VehicleParams


def make_thermal_module(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="thermal_module")
    assy.add(make_radiator(params), name="radiator")
    assy.add(make_fan(params), name="cooling_fan")
    return assy

