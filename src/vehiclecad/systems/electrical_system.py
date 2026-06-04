from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.parts.electrical.components import make_fuse_box, make_lv_battery, make_main_harness
from vehiclecad.params.vehicle import VehicleParams


def make_electrical_system(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="80_electrical")
    assy.add(make_lv_battery(params), name="battery_lv", color=colors.cq_color(colors.ELECTRICAL))
    assy.add(make_fuse_box(params), name="fuse_boxes", color=colors.cq_color(colors.ELECTRICAL))
    assy.add(make_main_harness(params), name="wiring_harnesses", color=colors.cq_color(colors.RUBBER))
    return assy

