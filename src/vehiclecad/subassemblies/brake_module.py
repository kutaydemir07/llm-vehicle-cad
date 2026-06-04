from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.geometry.primitives import box_from_center, cylinder_x
from vehiclecad.params.vehicle import VehicleParams


def make_brake_module(params: VehicleParams) -> cq.Assembly:
    arch = params.architecture
    assy = cq.Assembly(name="brake_module")
    pedal_box = box_from_center((arch.front_axle_x - arch.wheelbase * 0.20, -180, params.wheels.tire_radius + 170), (160, 120, 150))
    booster = cylinder_x((arch.front_axle_x - arch.wheelbase * 0.14, -210, params.wheels.tire_radius + 260), 70, 70)
    assy.add(pedal_box, name="pedal_box", color=colors.cq_color(colors.STEEL))
    assy.add(booster, name="booster_master_cylinder", color=colors.cq_color(colors.BRAKE))
    return assy

