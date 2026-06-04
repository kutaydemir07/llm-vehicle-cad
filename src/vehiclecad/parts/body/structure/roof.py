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

def _roof_panel():
    """Roof skin  -  flat plate at z - 1365, x - 1800 - 2750, y= - 720, 0.8 mm thick.

    A slight 8 mm crown (higher in centre) is approximated by adding a narrow
    raised strip down the centreline.
    """
    t = 0.8
    x0, x1 = 1805.0, 2745.0
    half_w = 710.0
    roof_z = 1348.0   # INNER roof panel, hidden under the body-shell skin (~1357)
                      #  -  was 1365 and poked THROUGH the red skin (the dark roof patch)

    main = _plate(x0, -half_w, roof_z, x1 - x0, 2 * half_w, t)

    # crown: a gentle raised strip (8 mm extra) tapering to edges
    # model as three stacked progressively narrower plates
    c1 = _plate(x0, -400, roof_z + t, x1 - x0, 800, t)       # +0.8
    c2 = _plate(x0, -250, roof_z + 2 * t, x1 - x0, 500, t)   # +1.6
    c3 = _plate(x0, -120, roof_z + 3 * t, x1 - x0, 240, t)   # +2.4

    return _U([main, c1, c2, c3])


def parts():
    out = []
    out.append((_roof_panel(), COL, "PRT_Roof_Panel"))
    return out

