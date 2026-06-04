from __future__ import annotations

import cadquery as cq

from vehiclecad.core import colors
from vehiclecad.core.coordinates import Axle, Side
from vehiclecad.parts.brakes.brake_disc import make_brake_disc
from vehiclecad.parts.brakes.caliper import make_caliper
from vehiclecad.parts.wheels.hub import make_hub
from vehiclecad.parts.wheels.tire import make_tire
from vehiclecad.parts.wheels.wheel import make_wheel
from vehiclecad.params.vehicle import VehicleParams


def _coerce_side(side: str | Side) -> Side:
    if isinstance(side, Side):
        return side
    return Side.LEFT if side.lower() in {"left", "l"} else Side.RIGHT


def _coerce_axle(axle: str | Axle) -> Axle:
    if isinstance(axle, Axle):
        return axle
    return Axle.FRONT if axle.lower() in {"front", "f"} else Axle.REAR


def wheel_center(params: VehicleParams, side: str | Side, axle: str | Axle) -> tuple[float, float, float]:
    arch = params.architecture
    wheels = params.wheels
    side_value = _coerce_side(side)
    axle_value = _coerce_axle(axle)
    x = arch.front_axle_x if axle_value is Axle.FRONT else arch.rear_axle_x
    track = arch.front_track if axle_value is Axle.FRONT else arch.rear_track
    return (x, side_value.sign * track / 2.0, wheels.tire_radius)


def make_wheel_corner(params: VehicleParams, side: str | Side, axle: str | Axle) -> cq.Assembly:
    side_value = _coerce_side(side)
    axle_value = _coerce_axle(axle)
    corner = cq.Assembly(name=f"{axle_value.value}_{side_value.value}_wheel_corner")
    loc = cq.Location(cq.Vector(*wheel_center(params, side_value, axle_value)))
    disc_diameter = (
        params.brakes.front_disc_diameter
        if axle_value is Axle.FRONT
        else params.brakes.rear_disc_diameter
    )

    corner.add(make_tire(params.wheels), name="tire", loc=loc, color=colors.cq_color(colors.RUBBER))
    corner.add(make_wheel(params.wheels), name="wheel", loc=loc, color=colors.cq_color(colors.ALUMINUM))
    corner.add(make_hub(params.wheels), name="hub", loc=loc, color=colors.cq_color(colors.STEEL))
    corner.add(make_brake_disc(disc_diameter), name="brake_disc", loc=loc, color=colors.cq_color(colors.STEEL))
    corner.add(
        make_caliper(disc_diameter, params.brakes.caliper_piston_count),
        name="caliper",
        loc=loc,
        color=colors.cq_color(colors.BRAKE),
    )
    return corner

