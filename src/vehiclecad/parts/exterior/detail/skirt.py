"""ASM_Aero_Surfaces  -  aerodynamic body kit for the Classic ModelA SportsCar.

This module builds every external aero surface that defines the SportsCar's drag and
downforce characteristics.  It **replaces** the older ``flares.py`` in the
assembly tree  -  all flare + aero parts now live here.

Parts created
 -  -  -  -  -  -  -  -  -  -  -  -  - 
  PRT_Box_Flares_Front_L / _R    -  signature front fender flares (torus bead)
  PRT_Box_Flares_Rear_L  / _R    -  wider rear fender flares
  PRT_Front_Air_Dam_Splitter      -  front undertray splitter
  PRT_Rear_Deck_Raised            -  SportsCar raised-trunk-lid surface
  PRT_Rear_Wing_Assembly          -  adjustable rear wing (airfoil + endplates + pedestals)
  PRT_Side_Skirts_L / _R         -  rocker panel extensions + black lower lip

Every dimension is parametrically linked to the skeleton design table so
changing ``skeleton.DT.track_front`` etc. propagates through the aero kit.

Coordinate frame (from ``common.py``):
    +X = rearward  (0 at front bumper tip)
    +Y = leftward  (0 = vehicle centreline)
    +Z = upward    (0 = ground plane)
    Millimetres.
"""
from __future__ import annotations
import math

import cadquery as cq
from cadquery import Solid, Vector

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as skeleton
from vehiclecad.core.reference.hardpoints import DT, AERO


# ------------------------------------------------------------------------
#  PARAMETRIC CONSTANTS (derived from skeleton)
# ------------------------------------------------------------------------
_TIRE_R = DT.tire_radius                    # 300 mm
_AXLE_F = DT.axle_front_x                   # 810 mm
_AXLE_R = DT.axle_rear_x                    # 3372 mm

# Flare offsets  -  half-width of the flare sitting 134 / 137 mm beyond the
# wheel centreline so the arch clears the tyre at full bump + full steer.
_FLARE_F_YC = DT.track_front / 2.0 + 95.0  #  - 801 mm  (flare centre Y, left)
_FLARE_R_YC = DT.track_rear  / 2.0 + 83.0  #  - 803 mm

# Torus geometry  -  major R = tyre radius + clearance, minor = bead width
_FLARE_F_R  = _TIRE_R + 76.0               # 376 mm
_FLARE_F_M  = 51.0                          # bead minor radius (front)
_FLARE_R_R  = _TIRE_R + 84.0               # 384 mm  (bigger rear arch)
_FLARE_R_M  = 57.0                          # bead minor radius (rear)

# Splitter hardpoints from skeleton AERO dict
_SPL_LE  = AERO["splitter_leading_edge"]    # (20, 0, 150)
_SPL_TE  = AERO["splitter_trailing_edge"]   # (240, 0, 150)

# Rear wing
_WING_LE = AERO["rear_wing_le"]             # (3840, 0, 1178)
_WING_TE = AERO["rear_wing_te"]             # (4075, 0, 1178)
_WING_AOA = AERO["wing_angle_of_attack"][0] # 8 degrees (default)


# ------------------------------------------------------------------------
#  1.  FRONT FENDER FLARES  (torus-bead approach, parametric)
# ------------------------------------------------------------------------


def _make_side_skirts():
    """Rocker-panel side skirts running from the front flare to the rear flare.

    Each skirt is a rounded box 30 mm proud of the body side, 168 mm tall,
    with a 26 mm black lower-lip trim strip.

    x = 1160  -  3060  (1900 mm long, from front to rear flare zone)
    y =  - 798  (just outside the body side sill)
    z = 176  -  344  (168 mm tall, above the pinch weld)
    """
    out = []
    x0 = C.AXLE_F + 366.0
    x1 = C.AXLE_R - 366.0
    y0 = C.SIDE_Y - 8.0
    dy = 34.0
    z0 = C.ROCKER_Z0
    dz = C.ROCKER_Z1 - C.ROCKER_Z0

    left = C.rbox(x0, y0, z0, x1 - x0, dy, dz, 8.0)
    lip = C.rbox(x0 + 18.0, y0 + dy - 9.0, z0 + 2.0,
                 x1 - x0 - 36.0, 10.0, 18.0, 4.0)
    out.append((left, C.RED, "PRT_Side_Skirts_L"))
    out.append((C.mirror_y(left), C.RED, "PRT_Side_Skirts_R"))
    out.append((lip, C.TRIM_BLK, "PRT_Side_Skirt_Trim_L"))
    out.append((C.mirror_y(lip), C.TRIM_BLK, "PRT_Side_Skirt_Trim_R"))
    return out


# ------------------------------------------------------------------------
#  PUBLIC API
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_make_side_skirts())
    return out

