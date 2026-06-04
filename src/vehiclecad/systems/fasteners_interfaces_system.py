from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.parts.fasteners.brackets import make_default_four_bolt_plate
from vehiclecad.params.vehicle import VehicleParams


def make_fasteners_interfaces_system(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="B0_fasteners_brackets_interfaces")
    hole_d = params.fasteners.default_bolt_diameter + params.fasteners.default_clearance
    mounts = {
        "front_subframe_mount_interface": (arch.front_axle_x - 80, 0.0, arch.ground_clearance + 170),
        "rear_subframe_mount_interface": (arch.rear_axle_x + 80, 0.0, arch.ground_clearance + 180),
        "powertrain_mount_interface": (arch.front_axle_x - 220, 0.0, params.wheels.tire_radius + 60),
    }
    for name, center in mounts.items():
        assy.add(make_default_four_bolt_plate(center, (230, 180, 18), hole_d), name=name, color=colors.cq_color(colors.FASTENER))
    return assy

