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


def _make_splitter():
    """Front splitter: a thin carbon/ABS plate extending forward from under
    the front bumper.  Slight 2 -  upturn at the leading edge to help separate
    airflow and reduce underbody stagnation pressure.

    The splitter is parametrically placed at the skeleton AERO hardpoints
    ``splitter_leading_edge`` and ``splitter_trailing_edge``.
    """
    x0  = _SPL_LE[0]                        # 20 mm
    x1  = _SPL_TE[0]                        # 240 mm
    z   = _SPL_LE[2]                        # 150 mm (ride-height level)
    dx  = x1 - x0                           # 220 mm chord
    t   = 8.0                               # plate thickness
    hw  = 700.0                             # half-width ( - Y)

    # Main flat plate
    plate = C.box(x0, -hw, z, dx, 2 * hw, t)

    # Leading-edge upturn: a thin wedge from x0 back ~40 mm,
    # tilted up by 2 -   -  modelled as a small box rotated about the Y axis.
    upturn_len = 40.0
    upturn = C.box(x0, -hw, z, upturn_len, 2 * hw, t)
    angle_rad = math.radians(2.0)
    dz_up = upturn_len * math.tan(angle_rad)
    # Approximate upturn: just add a thin tapered strip at the front edge
    upturn_strip = C.box(x0, -hw, z + t, upturn_len, 2 * hw, dz_up)
    splitter = C.U([plate, upturn_strip])

    return [(splitter, C.TRIM_BLK, "PRT_Front_Air_Dam_Splitter")]


# ------------------------------------------------------------------------
#  4.  RAISED TRUNK DECK
# ------------------------------------------------------------------------





def parts():
    return []

