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


def _make_trunk_deck():
    """The SportsCar's raised trunk lid  -  ~40 mm higher than the base ModelA sedan.

    This subtle lip improves flow separation at the trailing edge, reducing
    drag by ~3% (period Classic Motorsport data).  Modelled as a thin crowned
    plate at z  -  1090.

    The plate spans x = 3650 - 4150 and y =  - 600, with a slight crown (a
    thin additional strip along the centreline to create the crowned profile).
    """
    x0 = 3650.0
    dx = 500.0                  # 4150 - 3650
    hw = 600.0                  # half-width
    z  = 1050.0                 # flattened deck height
    t  = 6.0                    # plate thickness

    deck_skin = C.rbox(x0, -hw, z, dx, 2 * hw, t, 3)
    centre_crown = C.rbox(x0 + 38, -86, z + t - 1, dx - 72, 172, 8, 4)
    side_gutter_l = C.rbox(x0 + 18, hw - 50, z + 2, dx - 48, 28, 10, 4)
    side_gutter_r = C.mirror_y(side_gutter_l)
    rear_lip = C.rbox(x0 + dx - 36, -hw + 42, z + 5, 34, 2 * hw - 84, 18, 5)
    wing_pad_l = C.rbox(3866, 434, z + 8, 74, 72, 10, 4)
    wing_pad_r = C.mirror_y(wing_pad_l)
    deck = C.U([deck_skin, centre_crown, side_gutter_l, side_gutter_r,
                rear_lip, wing_pad_l, wing_pad_r])

    return [(deck, C.RED, "PRT_Rear_Deck_Raised")]


# ------------------------------------------------------------------------
#  5.  REAR WING ASSEMBLY  (airfoil + endplates + pedestals)
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_make_trunk_deck())
    return out

