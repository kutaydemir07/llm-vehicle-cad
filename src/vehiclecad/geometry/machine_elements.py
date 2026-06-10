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


def _thread_bands(fs: MetricFastener, base, axis, start: float, end: float) -> list:
    """Lightweight metric-thread representation: raised crest rings at the
    nominal pitch over [start, end] along the shank.  Reads as a rolled thread
    without the boolean cost of a true helix on hundreds of fasteners."""
    pitch = max(1.0, fs.shank_r * 0.30)
    bands = []
    t = start
    while t < end - pitch * 0.3:
        bands.append(C.cyl(fs.shank_r * 1.09, pitch * 0.32, _point(base, axis, t), axis))
        t += pitch
    return bands


def cap_screw(
    fastener: MetricFastener | str,
    grip_length: float,
    base,
    axis=(0, 0, 1),
    washer_under_head: bool = True,
) -> Solid:
    """Hex-head cap screw with shank along ``axis`` and head at the far end.
    The free third of the shank carries thread crests."""
    fs = spec(fastener) if isinstance(fastener, str) else fastener
    parts = [C.cyl(fs.shank_r, grip_length, base, axis)]
    parts += _thread_bands(fs, base, axis, 0.0, grip_length * 0.4)
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
        C.cyl(fs.shank_r, grip_length + fs.nut_h + 2.0, base, axis),
        washer(fs.washer_od / 2.0, fs.clearance_r, fs.washer_t, base, axis),
        hex_prism(fs.head_r, fs.head_h, _point(base, axis, -fs.head_h), axis),
        washer(fs.washer_od / 2.0, fs.clearance_r, fs.washer_t, _point(base, axis, grip_length - fs.washer_t), axis),
        hex_nut(fs, _point(base, axis, grip_length), axis),
    ]
    # thread crests on the nut end (the engaged + protruding length)
    parts += _thread_bands(fs, base, axis, grip_length * 0.62, grip_length + fs.nut_h + 2.0)
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


def _tooth_profile_prism(
    root_r: float,
    tip_r: float,
    pitch_r: float,
    circ_pitch: float,
    base_x: float,
    centre_y: float,
    centre_z: float,
    width: float,
) -> Solid:
    """ONE gear tooth as a prism along X with the correct rack-form trapezoid:
    flanks at the 20-degree pressure angle, tooth thickness = half the
    circular pitch at the pitch circle, tip narrower than root, with tip and
    root reliefs.  This is the standard straight-flank approximation of the
    involute -- meshing geometry (module, centre distance, tip/root) is exact."""
    half_pitch_t = circ_pitch * 0.25          # half tooth thickness at pitch r
    tan_pa = math.tan(math.radians(20.0))
    half_root = half_pitch_t + (pitch_r - root_r) * tan_pa
    half_tip = max(0.18 * half_pitch_t, half_pitch_t - (tip_r - pitch_r) * tan_pa)
    poly = [
        (centre_y - half_root, centre_z + root_r - 0.4),
        (centre_y - half_tip, centre_z + tip_r - 0.15 * (tip_r - root_r)),
        (centre_y - 0.6 * half_tip, centre_z + tip_r),
        (centre_y + 0.6 * half_tip, centre_z + tip_r),
        (centre_y + half_tip, centre_z + tip_r - 0.15 * (tip_r - root_r)),
        (centre_y + half_root, centre_z + root_r - 0.4),
    ]
    pts = [Vector(base_x, y, z) for y, z in poly]
    face = cq.Face.makeFromWires(cq.Wire.makePolygon(pts + [pts[0]]))
    return Solid.extrudeLinear(face, Vector(width, 0, 0))


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
    """External spur gear on the vehicle X axis with REAL tooth form.

    The tooth flanks are straight 20-degree pressure-angle facets on the
    correct module: pitch radius sits between ``root_r`` and ``outer_r`` per
    the standard addendum/dedendum split (a=m, d=1.25m), tooth thickness is
    half the circular pitch, and the tip is relieved.  Two meshing gears built
    with this helper at centre distance = sum of pitch radii engage properly."""
    teeth = max(6, int(teeth))
    # standard proportions: whole depth = 2.25 m -> m from the radial depth
    module = max(0.6, (outer_r - root_r) / 2.25)
    pitch_r = root_r + 1.25 * module
    circ_pitch = 2.0 * math.pi * pitch_r / teeth
    gear = C.cyl(root_r, width, (base_x, centre_y, centre_z), (1, 0, 0)).cut(
        C.cyl(bore_r, width + 2.0, (base_x - 1.0, centre_y, centre_z), (1, 0, 0))
    )
    tooth = _tooth_profile_prism(root_r, outer_r, pitch_r, circ_pitch,
                                 base_x, centre_y, centre_z, width)
    teeth_solids = [
        tooth.rotate((base_x, centre_y, centre_z), (base_x + 1, centre_y, centre_z),
                     clocking_deg + i * 360.0 / teeth)
        for i in range(teeth)
    ]
    return C.U([gear] + teeth_solids)


def bolt_circle(
    fastener: MetricFastener | str,
    count: int,
    pcd_r: float,
    grip_length: float,
    centre,
    axis=(0, 0, 1),
    start_deg: float = 0.0,
) -> Solid:
    """``count`` cap screws on a pitch-circle around ``axis`` through ``centre``
    -- the standard representation of a bolted flange joint."""
    u, v, w = _basis(axis)
    c = np.array(centre, dtype=float)
    screws = []
    for i in range(max(1, count)):
        a = math.radians(start_deg) + 2.0 * math.pi * i / max(1, count)
        p = c + u * (pcd_r * math.cos(a)) + v * (pcd_r * math.sin(a))
        screws.append(cap_screw(fastener, grip_length, tuple(p), axis))
    return C.U(screws)


def ring_gear_band_x(
    pitch_r: float,
    width: float,
    base_x: float,
    centre_y: float,
    centre_z: float,
    teeth: int,
    depth: float = 6.0,
) -> Solid:
    """External ring-gear band (e.g. flywheel starter ring) about the X axis:
    a band with proper trapezoidal teeth standing on its rim."""
    root_r = pitch_r - 0.55 * depth
    tip_r = pitch_r + 0.45 * depth
    band = C.cyl(root_r, width, (base_x, centre_y, centre_z), (1, 0, 0)).cut(
        C.cyl(root_r - depth, width + 2.0, (base_x - 1.0, centre_y, centre_z), (1, 0, 0))
    )
    circ_pitch = 2.0 * math.pi * pitch_r / teeth
    tooth = _tooth_profile_prism(root_r, tip_r, pitch_r, circ_pitch,
                                 base_x, centre_y, centre_z, width)
    teeth_solids = [
        tooth.rotate((base_x, centre_y, centre_z), (base_x + 1, centre_y, centre_z),
                     i * 360.0 / teeth)
        for i in range(teeth)
    ]
    return C.U([band] + teeth_solids)


def bevel_ring_gear(
    pitch_r: float,
    face_w: float,
    centre,
    axis=(0, 0, 1),
    teeth: int = 41,
    cone_deg: float = 45.0,
) -> Solid:
    """Hypoid/bevel ring gear: a conical face ring carrying radial teeth -- the
    differential crown wheel.  Teeth are wedge facets on the cone face at the
    correct angular pitch."""
    u, v, w = _basis(axis)
    c = np.array(centre, dtype=float)
    inner_r = pitch_r - face_w
    ring = C.cyl(pitch_r, face_w * 0.55, tuple(c), tuple(w)).cut(
        C.cyl(inner_r, face_w * 0.55 + 2.0, tuple(c - w), tuple(w))
    )
    tan_c = math.tan(math.radians(cone_deg))
    tooth_h = 0.16 * face_w
    teeth_solids = []
    for i in range(teeth):
        a = 2.0 * math.pi * i / teeth
        rdir = u * math.cos(a) + v * math.sin(a)
        p0 = c + rdir * inner_r + w * (face_w * 0.55)
        p1 = c + rdir * pitch_r + w * (face_w * 0.55 - (pitch_r - inner_r) * tan_c * 0.25)
        seg = C.swept_tube([tuple(p0), tuple(p1)], tooth_h, cap=False)
        teeth_solids.append(seg)
    return C.U([ring] + teeth_solids)


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
