from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.core.datums import datum_points
from vehiclecad.geometry.primitives import box_from_center, sphere
from vehiclecad.geometry.tubes import tube_between
from vehiclecad.params.vehicle import VehicleParams


def make_architecture_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="00_architecture")
    ground = box_from_center((arch.body_center_x, 0.0, -1.0), (arch.body_length, arch.overall_width, 2.0))
    assy.add(ground, name="ground_plane", color=colors.cq_color((0.80, 0.82, 0.82, 0.22)))

    assy.add(
        tube_between((arch.front_axle_x, -arch.front_track / 2.0, params.wheels.tire_radius), (arch.front_axle_x, arch.front_track / 2.0, params.wheels.tire_radius), 12),
        name="front_axle_line",
        color=colors.cq_color(colors.DATUM_YELLOW),
    )
    assy.add(
        tube_between((arch.rear_axle_x, -arch.rear_track / 2.0, params.wheels.tire_radius), (arch.rear_axle_x, arch.rear_track / 2.0, params.wheels.tire_radius), 12),
        name="rear_axle_line",
        color=colors.cq_color(colors.DATUM_YELLOW),
    )

    for datum in datum_points(params):
        assy.add(sphere(datum.xyz, 16), name=datum.name, color=colors.cq_color(colors.DATUM_YELLOW))
    return assy

