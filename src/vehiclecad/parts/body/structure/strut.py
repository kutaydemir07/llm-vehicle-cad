"""ASM_Chassis_BiW  -  Body-in-White structural module.

Creates the INTERNAL STRUCTURAL components of the ModelA SportsCar  -  the hidden
skeleton underneath the outer body shell.  These are the parts that provide
structural rigidity, mount the suspension, support the engine, and protect
the occupants.

Parts
-----
PRT_Floorpan_Main            -  floor plate + raised driveshaft tunnel
PRT_Firewall_Bulkhead        -  engine-bay / cabin divider with pass-throughs
PRT_Roof_Panel               -  roof skin (slight crown)
PRT_C_Pillar_Modified_L/R    -  SportsCar-specific wider/shallower C-pillars
PRT_Strut_Tower_Front_L/R    -  reinforced front strut towers with gussets
PRT_Strut_Tower_Rear_L/R     -  rear strut towers
PRT_Rocker_Rail_L/R          -  box-section sill members under the doors
PRT_Rear_Wheel_Tub_L/R       -  sheet-metal tubs inside the rear quarters
"""
from __future__ import annotations

import math
import cadquery as cq
from cadquery import Solid, Vector

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

# shorthand
_box = C.box
_cyl = C.cyl
_U   = C.U
_mirror = C.mirror_y
_plate = C.thick_plate
_shell = C.shell_box
_tapered = C.tapered_box
_xzp = C.xz_prism
COL  = C.STRUCT


# ------------------------------------------------------------------------
#  1. PRT_Floorpan_Main
# ------------------------------------------------------------------------

def _strut_tower_front_left():
    """Reinforced front strut tower (LEFT side).

    - Cylindrical tower r - 120, rising from z - 420 to z - 700  (inner fender area)
    - Top plate/cap r - 140, 8 mm thick at z=700
    - Two triangular gussets connecting tower to firewall and inner fender
    """
    # tower position from skeleton
    tx, ty, tz_top = SK.CHASSIS["strut_tower_FL"]   # (810, 530, 700)
    tz_bot = 420.0
    tower_r = 120.0
    tower_h = tz_top - tz_bot  # 280

    # main cylinder
    tower = _cyl(tower_r, tower_h, (tx, ty, tz_bot), (0, 0, 1))
    # hollow inside (wall  -  3 mm)
    tower_inner = _cyl(tower_r - 3, tower_h + 2, (tx, ty, tz_bot - 1), (0, 0, 1))
    tower = tower.cut(tower_inner)

    # top cap plate
    cap_r = 140.0
    cap = _cyl(cap_r, 8.0, (tx, ty, tz_top), (0, 0, 1))
    # bore hole for strut shaft (r - 22)
    bore = _cyl(22, 12, (tx, ty, tz_top - 2), (0, 0, 1))
    cap = cap.cut(bore)

    # gusset 1: tower  -  firewall (triangular plate in XZ plane)
    # runs from tower rear edge (x - 810+120=930) back to firewall (x - 1220)
    gus1_poly = [
        (tx + tower_r,       tz_bot),       # tower base
        (1220,               tz_bot),       # firewall base
        (1220,               tz_top - 60),  # firewall upper
    ]
    gus1 = _xzp(gus1_poly, ty - 2, ty + 2)

    # gusset 2: tower  -  inner fender rail (XZ plane, forward of tower)
    gus2_poly = [
        (tx - tower_r,       tz_bot),       # tower front base
        (tx - tower_r - 140, tz_bot),       # fender rail (forward)
        (tx - tower_r,       tz_bot + 180), # tower mid-height
    ]
    gus2 = _xzp(gus2_poly, ty - 2, ty + 2)

    tower_assy = _U([tower, cap, gus1, gus2])
    clearance = C.swept_tube(
        [SK.FRONT_SUSP["strut_lower"], SK.FRONT_SUSP["strut_upper_mount"]],
        48,
        cap=True,
    )
    rotor_clearance = _box(tx - 170, ty + 108, 150, 340, 125, 335)
    return tower_assy.cut(clearance).cut(rotor_clearance)




def _strut_tower_rear_left():
    """Simpler rear strut tower (LEFT side).

    At the rear strut mount position  -  a shorter cylindrical tower with cap.
    """
    tx, ty, tz_top = SK.CHASSIS["strut_tower_RL"]   # (3380, 540, 680)
    tz_bot = 440.0
    tower_r = 90.0
    tower_h = tz_top - tz_bot  # 240

    tower = _cyl(tower_r, tower_h, (tx, ty, tz_bot), (0, 0, 1))
    tower_inner = _cyl(tower_r - 3, tower_h + 2, (tx, ty, tz_bot - 1), (0, 0, 1))
    tower = tower.cut(tower_inner)

    cap = _cyl(105, 6, (tx, ty, tz_top), (0, 0, 1))
    bore = _cyl(18, 10, (tx, ty, tz_top - 2), (0, 0, 1))
    cap = cap.cut(bore)

    tower_assy = _U([tower, cap])
    spring_clearance = C.swept_tube(
        [SK.REAR_SUSP["spring_lower"], SK.REAR_SUSP["spring_upper"]],
        98,
        cap=True,
    )
    damper_clearance = C.swept_tube(
        [SK.REAR_SUSP["damper_lower"], SK.REAR_SUSP["damper_upper"]],
        44,
        cap=True,
    )
    return tower_assy.cut(spring_clearance).cut(damper_clearance)


# ------------------------------------------------------------------------
#  6. PRT_Rocker_Rails  (box-section sill members)
# ------------------------------------------------------------------------


def parts():
    out = []
    fl = _strut_tower_front_left()
    rl = _strut_tower_rear_left()
    out.append((fl,             COL, "PRT_Strut_Tower_Front_L"))
    out.append((_mirror(fl),    COL, "PRT_Strut_Tower_Front_R"))
    out.append((rl,             COL, "PRT_Strut_Tower_Rear_L"))
    out.append((_mirror(rl),    COL, "PRT_Strut_Tower_Rear_R"))
    return out

