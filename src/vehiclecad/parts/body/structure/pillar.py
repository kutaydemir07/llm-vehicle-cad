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

def _c_pillar_left():
    """SportsCar C-pillar  -  angled box beam from beltline up to roof.

    The SportsCar's C-pillar is shallower ( - 58 - ) than the base ModelA ( - 65 - ) for the
    wider, lower rear window.  Built as an XZ prism extruded in Y.

    Beltline at z - 1016 near x - 2950; roof junction at z - 1286 near x - 2750.
    The member sits inboard of the outer quarter skin and clear of the glass.
    """
    # pillar cross-section in XZ  -  a quadrilateral
    poly = [
        (2910, 1018),    # bottom-rear (beltline)
        (2942, 1018),    # bottom-rear outer edge
        (2778, 1286),    # top-front outer edge (roof)
        (2746, 1286),    # top-front inner edge (roof)
    ]
    y_centre = 694.0
    pillar_half_t = 18.0
    return _xzp(poly, y_centre - pillar_half_t, y_centre + pillar_half_t)


# ------------------------------------------------------------------------
#  5. PRT_Strut_Towers_Reinforced  (front + rear)
# ------------------------------------------------------------------------


def parts():
    out = []
    left = _c_pillar_left()
    right = _mirror(left)
    out.append((left,  COL, "PRT_C_Pillar_Modified_L"))
    out.append((right, COL, "PRT_C_Pillar_Modified_R"))
    return out

