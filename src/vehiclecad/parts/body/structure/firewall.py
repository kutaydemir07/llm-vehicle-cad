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

def _firewall():
    """Vertical plate at x - 1220 separating engine bay from cabin.

    Spans z - 220 - 920, y= - 760, 1.2 mm thick.
    Three pass-through holes:
       -  steering column    -  y - +340, z - 550, r - 44
       -  wiring harness     -  y -  - 200, z - 600, r - 40
       -  brake booster dome  -  y -  - 400, z - 700, r - 110
    """
    fw_x = SK.CHASSIS["firewall_top"][0]        # 1220
    z_bot = SK.CHASSIS["firewall_bottom"][2]     # 220
    z_top = SK.CHASSIS["firewall_top"][2]        # 920
    half_w = 760.0
    t = 1.2

    plate = _box(fw_x - t / 2, -half_w, z_bot, t, 2 * half_w, z_top - z_bot)

    # cut pass-through holes (cylinders through the plate in X)
    steer  = _cyl(44,  20, (fw_x - 10, 340,  550), (1, 0, 0))
    wiring = _cyl(40,  20, (fw_x - 10, -200, 600), (1, 0, 0))
    brake  = _cyl(110, 20, (fw_x - 10, -400, 700), (1, 0, 0))

    pedals = _box(fw_x - 10, -20, 245, 26, 585, 320)
    result = plate.cut(steer).cut(wiring).cut(brake).cut(pedals)

    # brake-booster dome  -  pushed-out hemisphere on the engine-bay side
    dome = Solid.makeSphere(110, Vector(fw_x - t / 2, -400, 700))
    # clip to engine-bay side (x < firewall)
    dome_clip = _box(fw_x - t / 2, -600, 550, 200, 400, 300)
    dome = dome.intersect(dome_clip)
    # make it a thin shell (subtract slightly smaller sphere)
    dome_inner = Solid.makeSphere(108, Vector(fw_x - t / 2, -400, 700))
    dome = dome.cut(dome_inner)

    return _U([result, dome])


def parts():
    out = []
    out.append((_firewall(), COL, "PRT_Firewall_Bulkhead"))
    return out

