from __future__ import annotations

import cadquery as cq

from vehiclecad.geometry.primitives import box_from_center
from vehiclecad.geometry.tubes import tube_between
from vehiclecad.params.vehicle import VehicleParams


def make_steering_rack(params: VehicleParams) -> cq.Workplane:
    arch = params.architecture
    return box_from_center((arch.front_axle_x + 40, 0.0, params.wheels.tire_radius + 80), (80, arch.front_track * 0.62, 46))


def make_tie_rod(inner: tuple[float, float, float], outer: tuple[float, float, float]) -> cq.Workplane:
    return tube_between(inner, outer, 20)

