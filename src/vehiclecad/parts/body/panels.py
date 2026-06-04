from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.geometry.surfaces import loft_rectangular_stations
from vehiclecad.params.vehicle import VehicleParams


def make_floor_structure(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    x_center = (arch.front_axle_x + arch.rear_axle_x) / 2.0
    length = arch.wheelbase + arch.front_overhang * 0.45 + arch.rear_overhang * 0.55
    return box_from_center(
        (x_center, 0.0, arch.ground_clearance + params.body.floor_thickness / 2.0),
        (length, arch.overall_width * 0.72, params.body.floor_thickness * 12.0),
    )


def _make_body_panel_tool(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    z0 = arch.ground_clearance
    shoulder = arch.overall_height * 0.64
    stations = [
        (arch.front_bumper_x, arch.overall_width * 0.22, z0 + 80, z0 + 410),
        (arch.front_axle_x + arch.front_overhang * 0.08, arch.overall_width * 0.46, z0, shoulder),
        (arch.rear_axle_x * 0.46, arch.overall_width * 0.50, z0, shoulder + 80),
        (arch.rear_axle_x, arch.overall_width * 0.47, z0 + 10, shoulder),
        (arch.rear_bumper_x, arch.overall_width * 0.28, z0 + 80, z0 + 430),
    ]
    return loft_rectangular_stations(stations, ruled=True)


def make_body_panels(params: VehicleParams) -> list[tuple[str, cq.Workplane]]:
    arch = params.architecture
    tool = _make_body_panel_tool(params)
    panel_regions = [
        ("front_nose_panel", box_from_center((arch.front_bumper_x - 120, 0.0, arch.ground_clearance + 260), (360, arch.overall_width * 0.70, 430))),
        ("front_fender_left", box_from_center((arch.front_axle_x + 80, arch.overall_width * 0.33, arch.ground_clearance + 300), (700, arch.overall_width * 0.32, 520))),
        ("front_fender_right", box_from_center((arch.front_axle_x + 80, -arch.overall_width * 0.33, arch.ground_clearance + 300), (700, arch.overall_width * 0.32, 520))),
        ("left_aperture_panel", box_from_center((arch.rear_axle_x * 0.45, arch.overall_width * 0.40, arch.ground_clearance + 420), (arch.wheelbase * 0.52, arch.overall_width * 0.26, 640))),
        ("right_aperture_panel", box_from_center((arch.rear_axle_x * 0.45, -arch.overall_width * 0.40, arch.ground_clearance + 420), (arch.wheelbase * 0.52, arch.overall_width * 0.26, 640))),
        ("rear_quarter_left", box_from_center((arch.rear_axle_x + 150, arch.overall_width * 0.34, arch.ground_clearance + 360), (820, arch.overall_width * 0.30, 560))),
        ("rear_quarter_right", box_from_center((arch.rear_axle_x + 150, -arch.overall_width * 0.34, arch.ground_clearance + 360), (820, arch.overall_width * 0.30, 560))),
        ("rear_tail_panel", box_from_center((arch.rear_bumper_x + 180, 0.0, arch.ground_clearance + 280), (420, arch.overall_width * 0.70, 450))),
    ]
    panels = []
    remaining = tool
    for name, cutter in panel_regions:
        panel = remaining.intersect(cutter)
        if panel.val().Volume() > 1.0:
            panels.append((name, panel))
            remaining = remaining.cut(cutter)
    if remaining.val().Volume() > 1.0:
        panels.append(("center_body_panel_remainders", remaining))
    return panels


def make_glasshouse(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    z_base = arch.overall_height * 0.56
    z_top = arch.overall_height
    stations = [
        (arch.front_axle_x - arch.wheelbase * 0.18, arch.overall_width * 0.31, z_base, z_top * 0.92),
        (arch.rear_axle_x * 0.46, arch.overall_width * 0.35, z_base + 40, z_top),
        (arch.rear_axle_x * 0.80, arch.overall_width * 0.26, z_base, z_top * 0.86),
    ]
    return loft_rectangular_stations(stations, ruled=True)


def make_box_fender_flare(params: VehicleParams, x: float, side_sign: int) -> cq.Workplane:
    arch = params.architecture
    y = side_sign * arch.overall_width * 0.485
    return box_from_center((x, y, params.wheels.tire_radius * 0.78), (500, 40, 210))


def make_rear_wing(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center(
        (arch.rear_bumper_x + arch.rear_overhang * 0.22, 0.0, arch.overall_height - 45),
        (420, arch.overall_width * 0.78, 28),
    )
