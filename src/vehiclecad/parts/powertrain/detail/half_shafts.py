"""Rear half-shafts (drive axles)  -  diff output flange to rear hub.

Left: diff_output_L -> rear hub; right mirrored.
Each is a turned shaft with a CV joint housing at each end and a tapered rubber
boot (lofted bellows) sealing each joint  -  recognisable hardware, not a tube.
"""
from __future__ import annotations
import math
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.geometry import machine_elements as ME
from vehiclecad.parts.powertrain.detail import layout as L

_mirror = C.mirror_y
COL  = C.STRUCT
CV   = (0.30, 0.31, 0.35)
BOOT = (0.08, 0.08, 0.09)
CLAMP = (0.48, 0.49, 0.52)

X, FL_Y, Z = L.DIFF_OUTPUT_L
HUB_Y = L.REAR_HUB_L[1]
SHAFT_Z = Z + 56


def _boot(y0, r0, y1, r1, z0=Z, z1=Z):
    """Tapered boot that can angle from the CV cup to a raised shaft line."""
    ys = [y0, (2 * y0 + y1) / 3, (y0 + 2 * y1) / 3, y1]
    zs = [z0, (2 * z0 + z1) / 3, (z0 + 2 * z1) / 3, z1]
    rs = [r0, r0 * 0.62, r1 * 1.05, r1]
    return C.loft_circles([((X, y, z), r, (0, 1, 0)) for y, z, r in zip(ys, zs, rs)])


def _clamp_band(y, outer_r, inner_r, z=Z):
    """Thin stainless clamp band around a CV boot end, axis along Y."""
    return C.cyl(outer_r, 8, (X, y - 4, z), (0, 1, 0)).cut(
        C.cyl(inner_r, 10, (X, y - 5, z), (0, 1, 0))
    )


def _half_shaft_left():
    out = []
    inner_boot_end = FL_Y + 82
    outer_boot_start = HUB_Y - 92

    # shaft between the two CV joints with SPLINED ends (the boot small clamps
    # grip over the spline run-out, as on the production axle)
    shaft = C.tube_path([
        (X, inner_boot_end, SHAFT_Z),
        (X, (inner_boot_end + outer_boot_start) / 2.0, SHAFT_Z + 8),
        (X, outer_boot_start, SHAFT_Z),
    ], 12)
    # inner ring set stays inboard of the damper tube (damper |y| >= 516)
    for ys, step in ((inner_boot_end + 1, 4.0), (outer_boot_start - 13, 5.0)):
        for k in range(3):
            shaft = shaft.fuse(C.cyl(13.0, 2.4, (X, ys + k * step, SHAFT_Z), (0, 1, 0)))
    out.append((shaft, COL, "Half_Shaft"))

    # CV joint housings: real cups -- bored cavities with the six-ball
    # complement visible in the race, and a boot-clamp groove at each mouth
    inner = C.cyl(34, 50, (X, FL_Y, Z), (0, 1, 0))
    inner = inner.cut(C.cyl(24, 36, (X, FL_Y + 16, Z), (0, 1, 0)))
    inner = inner.cut(C.cyl(35.5, 4, (X, FL_Y + 42, Z), (0, 1, 0)).cut(
        C.cyl(32, 8, (X, FL_Y + 40, Z), (0, 1, 0))))
    outer = C.cyl(36, 52, (X, HUB_Y - 52, Z), (0, 1, 0))
    outer = outer.cut(C.cyl(25, 36, (X, HUB_Y - 52, Z), (0, 1, 0)))
    outer = outer.cut(C.cyl(37.5, 4, (X, HUB_Y - 14, Z), (0, 1, 0)).cut(
        C.cyl(34, 8, (X, HUB_Y - 16, Z), (0, 1, 0))))
    for cy, race_r, host in ((FL_Y + 26, 28.5, "inner"), (HUB_Y - 40, 30.0, "outer")):
        balls = [
            Solid.makeSphere(5.5, Vector(X + race_r * math.cos(a), cy, Z + race_r * math.sin(a)))
            for a in [2 * math.pi * k / 6 for k in range(6)]
        ]
        if host == "inner":
            inner = C.U([inner] + balls)
        else:
            outer = C.U([outer] + balls)
    for y, radius, housing in ((FL_Y + 9, 42, inner), (HUB_Y - 9, 44, outer)):
        for sx, sz in ((24, 18), (-24, 18), (24, -18), (-24, -18)):
            housing = housing.fuse(ME.cap_screw("M8", 8, (X + sx, y, Z + sz), (0, 1, 0)))
        if y < (FL_Y + HUB_Y) / 2:
            inner = housing.fuse(C.cyl(radius, 6, (X, FL_Y - 3, Z), (0, 1, 0)))
        else:
            outer = housing.fuse(C.cyl(radius, 6, (X, HUB_Y - 3, Z), (0, 1, 0)))
    out.append((inner, CV, "CV_Inner"))
    out.append((outer, CV, "CV_Outer"))

    # rubber boots over each joint
    out.append((_boot(FL_Y + 48, 30, inner_boot_end, 14, Z, SHAFT_Z), BOOT, "CV_Boot_Inner"))
    out.append((_boot(HUB_Y - 48, 32, outer_boot_start, 14, Z, SHAFT_Z), BOOT, "CV_Boot_Outer"))
    out.append((_clamp_band(FL_Y + 48, 32, 28, Z), CLAMP, "CV_Boot_Inner_Clamp_Large"))
    out.append((_clamp_band(inner_boot_end, 16, 12, SHAFT_Z), CLAMP, "CV_Boot_Inner_Clamp_Small"))
    out.append((_clamp_band(HUB_Y - 48, 34, 30, Z), CLAMP, "CV_Boot_Outer_Clamp_Large"))
    out.append((_clamp_band(outer_boot_start, 13, 10, SHAFT_Z), CLAMP, "CV_Boot_Outer_Clamp_Small"))

    # Axle nut just outboard of the outer CV/hub interface.
    axle_nut = C.U([
        ME.washer(22, 8, 3, (X, HUB_Y - 1, Z), (0, 1, 0)),
        ME.hex_nut("M14", (X, HUB_Y + 2, Z), (0, 1, 0)),
    ])
    out.append((axle_nut, CLAMP, "CV_Axle_Nut"))
    return out


def parts():
    out = []
    for solid, color, name in _half_shaft_left():
        out.append((solid, color, f"PRT_{name}_RL"))
        out.append((_mirror(solid), color, f"PRT_{name}_RR"))
    return out
