from __future__ import annotations

import cadquery as cq

from vehiclecad.parts.interior.cabin import make_center_console, make_dashboard, make_roll_cage, make_seat
from vehiclecad.params.vehicle import VehicleParams


def make_interior_cockpit(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="interior_cockpit")
    assy.add(make_dashboard(params), name="dashboard")
    assy.add(make_center_console(params), name="center_console")

    front_x = arch.rear_axle_x * 0.32
    rear_x = arch.rear_axle_x * 0.62
    seat_y = arch.overall_width * 0.18
    assy.add(make_seat(params, front_x, seat_y), name="front_seat_left")
    if params.interior.seat_count > 1:
        assy.add(make_seat(params, front_x, -seat_y), name="front_seat_right")
    if params.interior.seat_count > 2:
        assy.add(make_seat(params, rear_x, 0.0), name="rear_bench")
    if params.interior.has_roll_cage:
        assy.add(make_roll_cage(params), name="roll_cage")
    return assy

