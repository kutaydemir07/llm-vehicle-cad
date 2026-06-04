from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.parts.body.panels import make_body_panels, make_box_fender_flare, make_floor_structure, make_glasshouse, make_rear_wing
from vehiclecad.subassemblies.body_front import make_body_front
from vehiclecad.subassemblies.body_rear import make_body_rear
from vehiclecad.subassemblies.body_side import make_body_side
from vehiclecad.params.vehicle import VehicleParams


def make_body_system(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="10_body")
    body_color = colors.BODY_RED if "classic" in params.name else colors.BODY_BLUE
    for name, panel in make_body_panels(params):
        assy.add(panel, name=name, color=colors.cq_color(body_color))
    assy.add(make_floor_structure(params), name="floor_structure", color=colors.cq_color(colors.CHASSIS))
    if params.body.has_roof:
        assy.add(make_glasshouse(params), name="glazing_greenhouse", color=colors.cq_color(colors.GLASS))
    assy.add(make_body_front(params), name="front_structure")
    assy.add(make_body_rear(params), name="rear_structure")
    assy.add(make_body_side(params, 1), name="side_structure_left")
    assy.add(make_body_side(params, -1), name="side_structure_right")

    if params.body.has_box_fenders:
        for x in (params.architecture.front_axle_x, params.architecture.rear_axle_x):
            assy.add(make_box_fender_flare(params, x, 1), name=f"box_fender_left_{int(x)}", color=colors.cq_color(body_color))
            assy.add(make_box_fender_flare(params, x, -1), name=f"box_fender_right_{int(x)}", color=colors.cq_color(body_color))
    if params.body.has_rear_wing:
        assy.add(make_rear_wing(params), name="rear_wing", color=colors.cq_color(colors.BODY_GREY))
    return assy
