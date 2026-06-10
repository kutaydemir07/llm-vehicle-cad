"""ASM_4110_Rack_And_Tie_Rods - ModelA SportsCar rack-and-pinion steering gear.

The rack is drawn like a real CAD subassembly: a centred rack housing carried on
two rubber bush brackets, a left-side pinion tower, corrugated inner boots, and
tie rods mated to the front upright steering-arm hardpoints.  The rack sits low
under the I4_Engine oil pan, while the tie rods slope up to the knuckles.
"""
from __future__ import annotations
import math
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.geometry import machine_elements as ME

FRONT = SK.FRONT_SUSP
STEER = SK.STEERING
_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.ARM


def _tie_rod(inner, outer, side: int):
    """Inner joint, adjuster sleeve, rod and outer ball joint on one hardpoint axis."""
    mid1 = (inner[0] - 45, inner[1] + side * 82, inner[2] + 32)
    mid2 = (outer[0] - 28, outer[1] - side * 18, outer[2] - 38)
    neck = (outer[0] - 8, outer[1] - side * 6, outer[2])
    rod = C.swept_tube([inner, mid1, mid2, neck, outer], 7, cap=True)
    adjuster = C.swept_tube([mid1, mid2], 10, cap=True)
    inner_ball = _cyl(20, 22, (inner[0], inner[1] - side * 11, inner[2]), (0, side, 0))
    outer_ball = _cyl(10, 10, (outer[0], outer[1] - side * 5, outer[2]), (0, side, 0))
    locknut_i = _cyl(12, 12, (mid1[0], mid1[1] - side * 6, mid1[2]), (0, side, 0))
    locknut_o = _cyl(8, 8, (mid2[0], mid2[1] - side * 3, mid2[2]), (0, side, 0))
    return _U([rod, adjuster, inner_ball, outer_ball, locknut_i, locknut_o])


def _rack_boot(inner, side: int):
    """Corrugated rubber boot around the inner joint."""
    y0 = inner[1] - side * 76
    boot_core = _cyl(18, 74, (inner[0], y0, inner[2]), (0, side, 0))
    rings = []
    for i in range(5):
        y = y0 + side * (8 + i * 14)
        rings.append(_cyl(24, 7, (inner[0], y, inner[2]), (0, side, 0)))
    collar = _cyl(28, 12, (inner[0], inner[1] - side * 6, inner[2]), (0, side, 0))
    return _U([boot_core, collar] + rings)


def _rack():
    """Rack housing, pinion tower, boots, tie rods and mounting brackets."""
    x, _, z = STEER["rack_centre"]
    left_inner = STEER["rack_inner_L"]
    right_inner = STEER["rack_inner_R"]

    # Rack casting spans between inner joints and clears the oil-pan underside.
    rack_housing = _cyl(28, 650, (x, -325, z), (0, 1, 0)).cut(
        _cyl(13, 654, (x, -327, z), (0, 1, 0))
    )
    centre_bulge = _cyl(38, 78, (x - 4, -39, z), (0, 1, 0))
    cap_l = _cyl(32, 18, (left_inner[0], left_inner[1] - 9, z), (0, 1, 0))
    cap_r = _cyl(32, 18, (right_inner[0], right_inner[1] - 9, z), (0, 1, 0))

    # Left-side pinion housing + valve body, with the input spline protruding UP
    # so the column coupler clamps onto it (above the housing).
    px, py, pz = STEER["pinion_base"]    # (760, 240, 220)
    ix, iy, iz = STEER["pinion_input"]   # (760, 240, 305)
    pinion_tower = _cyl(20, iz - pz, (px, py, pz), (0, 0, 1))      # housing z220..305
    pinion_boss = _cyl(34, 48, (px, py - 24, pz - 2), (0, 1, 0))   # valve body, low (z218)
    input_spline = _cyl(12, 48, (ix, iy, iz - 5), (0, 0, 1))       # spline z300..348, r12

    # Rubber-isolated clamps to the front subframe/rack carrier.
    mount_l = _rbox(x - 35, 170, z - 38, 70, 62, 32, 6)
    mount_r = _rbox(x - 35, -232, z - 38, 70, 62, 32, 6)
    bush_l = _cyl(18, 62, (x, 170, z), (0, 1, 0))
    bush_r = _cyl(18, 62, (x, -232, z), (0, 1, 0))

    boot_l = _rack_boot(left_inner, 1)
    boot_r = _rack_boot(right_inner, -1)
    tie_l = _tie_rod(left_inner, STEER["tie_rod_outer_L"], 1)
    tie_r = _tie_rod(right_inner, STEER["tie_rod_outer_R"], -1)

    # rack clamp through-bolts into the subframe carrier (two per bracket)
    clamp_bolts = [
        ME.through_bolt("M10", 44, (bx, by, z - 44), (0, 0, 1))
        for by in (170 + 31, -232 + 31)
        for bx in (x - 22, x + 22)
    ]

    return _U([
        rack_housing, centre_bulge, cap_l, cap_r,
        pinion_tower, pinion_boss, input_spline,
        mount_l, mount_r, bush_l, bush_r,
        boot_l, boot_r, tie_l, tie_r,
    ] + clamp_bolts)


def _rack_bar_pinion_gear():
    """Toothed rack bar and pinion gear inside the hollow rack housing."""
    x, _, z = STEER["rack_centre"]
    px, py, pz = STEER["pinion_base"]
    rack_bar = _rbox(x - 7, -286, z - 7, 14, 572, 14, 3)
    # rack teeth at the PINION's circular pitch (2*pi*r_pitch/14 ~ 9 mm) so the
    # pair actually indexes tooth-for-tooth
    teeth = []
    for i in range(60):
        y = -268 + i * 9.0
        teeth.append(_rbox(x - 9, y, z + 7, 18, 4.5, 5, 1))

    pinion = _cyl(20, 18, (px, py, pz + 4), (0, 0, 1))
    # radial teeth ON the pinion barrel (not a floating crown above it)
    pinion_teeth = []
    for i in range(14):
        tooth = _rbox(px + 17, py - 3, pz + 5, 8, 6, 16, 1)
        pinion_teeth.append(tooth.rotate((px, py, pz), (px, py, pz + 1), i * 360.0 / 14))
    lower_bearing = ME.radial_ball_bearing(13, 6, 8, (px, py, pz - 6), (0, 0, 1), ball_count=8)
    upper_bearing = ME.radial_ball_bearing(13, 6, 8, (px, py, pz + 88), (0, 0, 1), ball_count=8)
    return _U([rack_bar, pinion, lower_bearing, upper_bearing] + teeth + pinion_teeth)


def parts():
    return [
        (_rack(), COL, "PRT_Steering_Rack"),
        (_rack_bar_pinion_gear(), (0.58, 0.59, 0.62), "PRT_Steering_Rack_Bar_Pinion_Gear"),
    ]
