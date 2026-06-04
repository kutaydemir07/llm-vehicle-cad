"""Chassis strut-tower reinforcement plates and brace bar."""
from __future__ import annotations
import cadquery as cq
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

_box    = C.box
_cyl    = C.cyl
_U      = C.U
_mirror = C.mirror_y
_xzp    = C.xz_prism
COL     = C.STRUCT


def _strut_top_plate_left():
    """Strut-tower top reinforcement plate (LEFT).

    Flat 4 mm plate at z=700, 280  -  280, centred on the top mount.
    Three M14 captive-nut bosses at the mount bolt circle (r=70 mm, 120 -  apart).
    """
    tx, ty = SK.CHASSIS["strut_tower_FL"][0], SK.CHASSIS["strut_tower_FL"][1]  # 810, 530
    tz = 700.0
    plate = _box(tx - 140, ty - 140, tz, 280, 280, 4)

    # three mount bosses on a 120 PCD pattern at 30, 150, 270 deg
    import math
    pcd = 70.0
    bosses = []
    for deg in (30, 150, 270):
        bx = tx + pcd * math.cos(math.radians(deg))
        by = ty + pcd * math.sin(math.radians(deg))
        boss = _cyl(12, 14, (bx, by, tz - 2), (0, 0, 1))
        bosses.append(boss)

    result = _U([plate] + bosses)
    clearance = C.swept_tube(
        [SK.FRONT_SUSP["strut_lower"], SK.FRONT_SUSP["strut_upper_mount"]],
        42,
        cap=True,
    )
    return result.cut(clearance)


def _strut_brace_bar():
    """Front strut brace bar connecting L and R top mounts.

    Arches UP and OVER the engine: it rises from each strut-tower top
    (z - 712) to a central peak at z=868, clearing the I4_Engine cam-cover top
    (z - 790) by ~60 mm.  (The old bar dipped DOWN to z=650 and speared
    straight through the cylinder head / block  -  a 450 cc interference.)
    """
    path = [
        (810,  420, 900),
        (810,  260, 940),
        (810,    0, 960),
        (810, -260, 940),
        (810, -420, 900),
    ]
    return C.swept_tube(path, 18, cap=True)


def parts():
    out = []
    left_plate = _strut_top_plate_left()
    out.append((left_plate,           COL, "PRT_Strut_Top_Plate_FL"))
    out.append((_mirror(left_plate),  COL, "PRT_Strut_Top_Plate_FR"))
    out.append((_strut_brace_bar(),   COL, "PRT_Strut_Brace_Bar_Front"))
    return out

