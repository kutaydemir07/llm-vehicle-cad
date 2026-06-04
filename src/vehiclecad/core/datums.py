from __future__ import annotations

from dataclasses import dataclass

from vehiclecad.params.vehicle import VehicleParams


@dataclass(frozen=True)
class DatumPoint:
    name: str
    xyz: tuple[float, float, float]


@dataclass(frozen=True)
class DatumPlane:
    name: str
    point: tuple[float, float, float]
    normal: tuple[float, float, float]


def datum_points(params: VehicleParams) -> list[DatumPoint]:
    arch = params.architecture
    wheel_z = params.wheels.tire_radius
    return [
        DatumPoint("origin_front_axle_ground", (0.0, 0.0, 0.0)),
        DatumPoint("front_axle_center", (0.0, 0.0, wheel_z)),
        DatumPoint("rear_axle_center", (arch.rear_axle_x, 0.0, wheel_z)),
        DatumPoint("vehicle_cg_estimate", (arch.cg_x, 0.0, arch.cg_z)),
        DatumPoint("front_bumper_center", (arch.front_bumper_x, 0.0, arch.ground_clearance)),
        DatumPoint("rear_bumper_center", (arch.rear_bumper_x, 0.0, arch.ground_clearance)),
    ]


def datum_planes(params: VehicleParams) -> list[DatumPlane]:
    arch = params.architecture
    return [
        DatumPlane("ground", (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)),
        DatumPlane("centerline", (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
        DatumPlane("front_axle", (0.0, 0.0, 0.0), (1.0, 0.0, 0.0)),
        DatumPlane("rear_axle", (arch.rear_axle_x, 0.0, 0.0), (1.0, 0.0, 0.0)),
        DatumPlane("front_bumper", (arch.front_bumper_x, 0.0, 0.0), (1.0, 0.0, 0.0)),
        DatumPlane("rear_bumper", (arch.rear_bumper_x, 0.0, 0.0), (-1.0, 0.0, 0.0)),
    ]
