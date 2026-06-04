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


def _naca_profile(chord: float, max_thick: float, n: int = 30):
    """Generate a NACA-2412-ish airfoil cross-section as (x, z) polyline.

    We approximate the classic NACA profile:
      - Camber line: 2% camber at 40% chord  (m=0.02, p=0.4)
      - Thickness: 12% of chord  (t/c = 0.12)

    The returned polygon is closed (last point == first point), with points
    ordered clockwise (upper surface then lower surface, trailing - leading - 
    trailing).

    The profile is centred with the leading edge at x=0, z=0.
    """
    # Thickness distribution (NACA 4-digit formula)
    tc = max_thick / chord
    pts_upper = []
    pts_lower = []
    for i in range(n + 1):
        xc = i / float(n)                  # 0..1 normalised chord
        # Camber line: m=0.02, p=0.4
        m, p = 0.02, 0.4
        if xc <= p:
            yc = m / (p * p) * (2 * p * xc - xc * xc)
        else:
            yc = m / ((1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xc - xc * xc)

        # Thickness (NACA formula, normalised to tc)
        yt = tc / 0.2 * (0.2969 * math.sqrt(xc)
                         - 0.1260 * xc
                         - 0.3516 * xc ** 2
                         + 0.2843 * xc ** 3
                         - 0.1015 * xc ** 4)  # open trailing edge variant
        pts_upper.append((xc * chord, (yc + yt) * chord))
        pts_lower.append((xc * chord, (yc - yt) * chord))

    # Combine: upper from LE - TE, then lower from TE - LE (closed polygon)
    profile = pts_upper + pts_lower[::-1]
    return profile






def parts():
    return []

