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

def _rocker_rail_left():
    """Box-section sill member (LEFT side), running under the door sill.

    x  -  1100  -  3400, y  -  +780, z  -  180 - 310.
    Section: 60 mm wide  -  130 mm tall, 2 mm wall.
    """
    rx0 = SK.CHASSIS["rocker_front"][0]  # 1100
    rx1 = min(SK.CHASSIS["rocker_rear"][0], C.AXLE_R - 380.0)
    ry  = SK.CHASSIS["rocker_front"][1]  # 790
    rz  = SK.CHASSIS["rocker_front"][2]  # 180

    dx = rx1 - rx0              # 2300
    sect_w = 60.0               # Y width
    sect_h = 130.0              # Z height
    wall = 2.0

    # centre the section on rocker_y
    y0 = ry - sect_w / 2.0      # 760
    return _shell(rx0, y0, rz, dx, sect_w, sect_h, wall)


# ------------------------------------------------------------------------
#  7. PRT_Rear_Wheel_Tubs
# ------------------------------------------------------------------------


def parts():
    out = []
    left = _rocker_rail_left()
    right = _mirror(left)
    out.append((left,  COL, "PRT_Rocker_Rail_L"))
    out.append((right, COL, "PRT_Rocker_Rail_R"))
    return out

