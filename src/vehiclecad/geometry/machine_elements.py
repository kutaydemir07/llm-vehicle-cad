"""Reusable machine elements for production-oriented CAD details.

The vehicle modules should not redraw bolts, nuts, washers, bearings, and
bushings as anonymous cylinders.  These helpers provide recognisable metric
hardware proportions so critical interfaces look and audit like real assemblies.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import cadquery as cq
from cadquery import Solid, Vector
import numpy as np

from vehiclecad.core.reference import common as C


@dataclass(frozen=True)
class MetricFastener:
    designation: str
    shank_r: float
    clearance_r: float
    head_af: float
    head_h: float
    nut_af: float
    nut_h: float
    washer_od: float
    washer_t: float

    @property
    def head_r(self) -> float:
        return self.head_af / math.sqrt(3.0)

    @property
    def nut_r(self) -> float:
        return self.nut_af / math.sqrt(3.0)


METRIC_FASTENERS: dict[str, MetricFastener] = {
    "M6": MetricFastener("M6", 3.0, 3.4, 10.0, 4.0, 10.0, 5.0, 12.0, 1.6),
    "M8": MetricFastener("M8", 4.0, 4.5, 13.0, 5.3, 13.0, 6.5, 17.0, 1.6),
    "M10": MetricFastener("M10", 5.0, 5.5, 17.0, 6.4, 17.0, 8.0, 21.0, 2.0),
    "M12": MetricFastener("M12", 6.0, 6.6, 19.0, 7.5, 19.0, 10.0, 24.0, 2.5),
    "M14": MetricFastener("M14", 7.0, 7.7, 22.0, 8.8, 22.0, 11.0, 28.0, 2.5),
}


def spec(designation: str) -> MetricFastener:
    try:
        return METRIC_FASTENERS[designation.upper()]
    except KeyError as exc:
        raise KeyError(f"unknown metric fastener: {designation}") from exc


def _unit(axis: tuple[float, float, float]) -> np.ndarray:
    v = np.array(axis, dtype=float)
    n = float(np.linalg.norm(v))
    if n <= 1e-9:
        raise ValueError("axis must be non-zero")
    return v / n


def _point(base, axis, distance: float) -> tuple[float, float, float]:
    b = np.array(base, dtype=float)
    return tuple(b + _unit(axis) * distance)


def _basis(axis) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    w = _unit(axis)
    seed = np.array([0.0, 0.0, 1.0])
    if abs(float(np.dot(w, seed))) > 0.92:
        seed = np.array([1.0, 0.0, 0.0])
    u = np.cross(seed, w)
    u = u / float(np.linalg.norm(u))
    v = np.cross(w, u)
    return u, v, w


def _orient_from_z(shape: Solid, axis) -> Solid:
    target = _unit(axis)
    source = np.array([0.0, 0.0, 1.0])
    dot = max(-1.0, min(1.0, float(np.dot(source, target))))
    if dot > 0.999999:
        return shape
    if dot < -0.999999:
        return shape.rotate((0, 0, 0), (1, 0, 0), 180)
    rot_axis = np.cross(source, target)
    angle = math.degrees(math.acos(dot))
    return shape.rotate((0, 0, 0), tuple(rot_axis), angle)


def hex_prism(radius: float, height: float, base, axis=(0, 0, 1), clocking_deg: float = 30.0) -> Solid:
    """Regular hexagonal prism with ``base`` at the lower face centre."""
    pts = []
    for i in range(6):
        a = math.radians(clocking_deg + i * 60.0)
        pts.append(Vector(radius * math.cos(a), radius * math.sin(a), 0.0))
    face = cq.Face.makeFromWires(cq.Wire.makePolygon(pts + [pts[0]]))
    prism = Solid.extrudeLinear(face, Vector(0, 0, height))
    return _orient_from_z(prism, axis).translate(base)


def washer(outer_r: float, inner_r: float, thickness: float, base, axis=(0, 0, 1)) -> Solid:
    return C.cyl(outer_r, thickness, base, axis).cut(
        C.cyl(inner_r, thickness + 2.0, _point(base, axis, -1.0), axis)
    )


def hex_nut(fastener: MetricFastener | str, base, axis=(0, 0, 1)) -> Solid:
    fs = spec(fastener) if isinstance(fastener, str) else fastener
    nut = hex_prism(fs.nut_r, fs.nut_h, base, axis)
    return nut.cut(C.cyl(fs.clearance_r, fs.nut_h + 2.0, _point(base, axis, -1.0), axis))


def cap_screw(
    fastener: MetricFastener | str,
    grip_length: float,
    base,
    axis=(0, 0, 1),
    washer_under_head: bool = True,
) -> Solid:
    """Hex-head cap screw with shank along ``axis`` and head at the far end."""
    fs = spec(fastener) if isinstance(fastener, str) else fastener
    parts = [C.cyl(fs.shank_r, grip_length, base, axis)]
    if washer_under_head:
        parts.append(washer(fs.washer_od / 2.0, fs.clearance_r, fs.washer_t, _point(base, axis, grip_length), axis))
        head_base = _point(base, axis, grip_length + fs.washer_t)
    else:
        head_base = _point(base, axis, grip_length)
    parts.append(hex_prism(fs.head_r, fs.head_h, head_base, axis))
    return C.U(parts)


def through_bolt(
    fastener: MetricFastener | str,
    grip_length: float,
    base,
    axis=(0, 0, 1),
) -> Solid:
    """Bolt, two washers, and nut clamping a joint of ``grip_length``."""
    fs = spec(fastener) if isinstance(fastener, str) else fastener
    parts = [
        C.cyl(fs.shank_r, grip_length, base, axis),
        washer(fs.washer_od / 2.0, fs.clearance_r, fs.washer_t, base, axis),
        hex_prism(fs.head_r, fs.head_h, _point(base, axis, -fs.head_h), axis),
        washer(fs.washer_od / 2.0, fs.clearance_r, fs.washer_t, _point(base, axis, grip_length - fs.washer_t), axis),
        hex_nut(fs, _point(base, axis, grip_length), axis),
    ]
    return C.U(parts)


def threaded_stud_with_nut(
    fastener: MetricFastener | str,
    exposed_length: float,
    base,
    axis=(0, 0, 1),
) -> Solid:
    """Stud with washer and nut on the exposed end."""
    fs = spec(fastener) if isinstance(fastener, str) else fastener
    parts = [
        C.cyl(fs.shank_r, exposed_length, base, axis),
        washer(fs.washer_od / 2.0, fs.clearance_r, fs.washer_t, _point(base, axis, exposed_length - fs.washer_t), axis),
        hex_nut(fs, _point(base, axis, exposed_length), axis),
    ]
    # Light thread indication on the free end.
    thread_start = max(0.0, exposed_length - 0.45 * exposed_length)
    pitch = max(1.0, fs.shank_r * 0.28)
    n_bands = max(2, int((exposed_length - thread_start) / pitch))
    for i in range(n_bands):
        z = thread_start + i * pitch
        parts.append(C.cyl(fs.shank_r * 1.08, pitch * 0.28, _point(base, axis, z), axis))
    return C.U(parts)


def radial_ball_bearing(
    outer_r: float,
    inner_r: float,
    width: float,
    base,
    axis=(0, 0, 1),
    ball_count: int = 12,
) -> Solid:
    """Simplified deep-groove bearing with rings and visible ball complement."""
    u, v, w = _basis(axis)
    b = np.array(base, dtype=float)
    centre = b + w * (width * 0.5)
    race_r = 0.5 * (outer_r + inner_r)
    ball_r = max(2.0, 0.18 * (outer_r - inner_r))
    outer = C.cyl(outer_r, width, base, axis).cut(
        C.cyl(race_r + ball_r * 0.75, width + 2.0, _point(base, axis, -1.0), axis)
    )
    inner = C.cyl(inner_r + ball_r * 0.75, width, base, axis).cut(
        C.cyl(inner_r, width + 2.0, _point(base, axis, -1.0), axis)
    )
    balls = []
    for i in range(ball_count):
        a = 2.0 * math.pi * i / ball_count
        p = centre + u * (race_r * math.cos(a)) + v * (race_r * math.sin(a))
        balls.append(Solid.makeSphere(ball_r, Vector(*p)))
    return C.U([outer, inner] + balls)


def bonded_bushing(
    outer_r: float,
    inner_r: float,
    width: float,
    base,
    axis=(0, 0, 1),
    sleeve_wall: float = 4.0,
) -> Solid:
    """Rubber bushing with metal inner sleeve and thin outer crush tube."""
    rubber_inner = inner_r + sleeve_wall
    rubber = C.cyl(outer_r, width, base, axis).cut(
        C.cyl(rubber_inner, width + 2.0, _point(base, axis, -1.0), axis)
    )
    sleeve = C.cyl(rubber_inner, width + 4.0, _point(base, axis, -2.0), axis).cut(
        C.cyl(inner_r, width + 6.0, _point(base, axis, -3.0), axis)
    )
    outer_shell = C.cyl(outer_r + 2.0, width, base, axis).cut(
        C.cyl(outer_r, width + 2.0, _point(base, axis, -1.0), axis)
    )
    return C.U([rubber, sleeve, outer_shell])


def clevis_pin(pin_r: float, grip_length: float, base, axis=(0, 0, 1)) -> Solid:
    """Plain clevis pin with washer and retaining clip groove indication."""
    parts = [
        C.cyl(pin_r, grip_length, base, axis),
        C.cyl(pin_r * 1.7, pin_r * 0.45, _point(base, axis, -pin_r * 0.45), axis),
        washer(pin_r * 1.65, pin_r * 1.05, pin_r * 0.35, _point(base, axis, grip_length), axis),
        C.cyl(pin_r * 1.08, pin_r * 0.30, _point(base, axis, grip_length + pin_r * 0.40), axis),
    ]
    return C.U(parts)


def spur_gear_x(
    root_r: float,
    outer_r: float,
    width: float,
    base_x: float,
    centre_y: float,
    centre_z: float,
    teeth: int,
    bore_r: float = 10.0,
    clocking_deg: float = 0.0,
) -> Solid:
    """Simple external spur gear on the vehicle X axis.

    It is intentionally lightweight: root cylinder plus individual raised teeth
    and a bored centre.  The teeth make gear trains visually/mechanically legible
    without the cost of involute tooth surfaces for every audit build.
    """
    gear = C.cyl(root_r, width, (base_x, centre_y, centre_z), (1, 0, 0)).cut(
        C.cyl(bore_r, width + 2.0, (base_x - 1.0, centre_y, centre_z), (1, 0, 0))
    )
    tooth_h = max(1.0, outer_r - root_r)
    pitch = 2.0 * math.pi * outer_r / max(1, teeth)
    tooth_w = min(pitch * 0.45, tooth_h * 1.8)
    teeth_solids = []
    for i in range(teeth):
        angle = clocking_deg + i * 360.0 / teeth
        tooth = C.rbox(
            base_x,
            centre_y - tooth_w / 2.0,
            centre_z + root_r - 0.3,
            width,
            tooth_w,
            tooth_h + 0.6,
            min(1.5, tooth_w * 0.25),
        )
        teeth_solids.append(tooth.rotate((base_x, centre_y, centre_z), (base_x + 1, centre_y, centre_z), angle))
    return C.U([gear] + teeth_solids)


def dog_clutch_ring_x(
    outer_r: float,
    inner_r: float,
    width: float,
    base_x: float,
    centre_y: float,
    centre_z: float,
    dogs: int = 6,
) -> Solid:
    """Synchro/dog ring with drive lugs around an X-axis shaft."""
    ring = C.cyl(outer_r, width, (base_x, centre_y, centre_z), (1, 0, 0)).cut(
        C.cyl(inner_r, width + 2.0, (base_x - 1.0, centre_y, centre_z), (1, 0, 0))
    )
    lugs = []
    for i in range(dogs):
        a = i * 360.0 / dogs
        lug = C.rbox(base_x, centre_y - 5, centre_z + outer_r - 1, width, 10, 8, 2)
        lugs.append(lug.rotate((base_x, centre_y, centre_z), (base_x + 1, centre_y, centre_z), a))
    return C.U([ring] + lugs)
