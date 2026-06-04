from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.subassemblies.interior_cockpit import make_interior_cockpit
from vehiclecad.params.vehicle import VehicleParams


def make_interior_system(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="90_interior")
    assy.add(make_interior_cockpit(params), name="cockpit", color=colors.cq_color(colors.INTERIOR))
    return assy

