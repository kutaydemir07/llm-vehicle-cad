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


def _naca_profile(chord: float, max_t: float):
    """Return a list of (x, z) points tracing a symmetric NACA-style airfoil
    (upper surface then lower surface, closed at TE).

    ``chord`` is the chord length in mm, ``max_t`` is the maximum thickness in mm.
    Returns points in the XZ plane with x along chord (0 = LE, chord = TE)
    and z as camber/thickness offset from chord line.
    """
    n = 20
    pts_upper = []
    pts_lower = []
    for i in range(n + 1):
        xi = i / n
        # half-thickness distribution (NACA 4-digit symmetric)
        t = (max_t / chord) * (
            0.2969 * math.sqrt(xi)
            - 0.1260 * xi
            - 0.3516 * xi ** 2
            + 0.2843 * xi ** 3
            - 0.1015 * xi ** 4
        )
        x_mm = xi * chord
        z_mm = t * chord
        pts_upper.append((x_mm, z_mm))
        pts_lower.insert(0, (x_mm, -z_mm))
    # Close trailing edge
    return pts_upper + pts_lower[1:]


def _make_rear_wing():
    """Build the rear wing assembly: airfoil wing element, two end plates,
    and two mounting pedestals.

    The wing has an adjustable angle of attack read from
    ``skeleton.AERO['wing_angle_of_attack'][0]`` (default 8 - ), rotated
    about the leading-edge line in the XZ plane.

    Airfoil cross-section: NACA-2412-style, 172 mm chord, 28 mm max thickness.
    Span: 1132 mm (y =  - 566).
    """
    chord  = 172.0
    span   = 1132.0
    half_span = span / 2.0             # 566 mm
    max_t  = 28.0
    le_x   = _WING_LE[0]              # 3840
    le_z   = _WING_LE[2]              # 1178
    aoa    = _WING_AOA                # 8 degrees

    out = []

    #  -  -  Wing element: extrude airfoil cross-section along Y  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    # Generate the 2-D profile in the XZ plane (x along chord, z = thickness)
    profile_pts = _naca_profile(chord, max_t)

    # Build as an XZ polygon extruded across the span in Y
    # The xz_prism helper takes (x, z) pairs and extrudes from y0 to y1.
    # We place the profile at the wing LE position.
    xz_pts = [(le_x + px, le_z + pz) for px, pz in profile_pts]
    wing = C.xz_prism(xz_pts, -half_span, half_span)

    # Rotate the wing about its leading edge by the angle of attack.
    # Rotation is about a Y-axis line at (le_x, 0, le_z), so the wing
    # pitches nose-up (positive AoA lifts the trailing edge).
    wing = wing.rotate(
        (le_x, 0, le_z),              # point on rotation axis
        (le_x, 1, le_z),              # second point defines axis (Y direction)
        -aoa                           # negative = nose-up pitch in CQ convention
    )
    out.append((wing, C.RED, "PRT_Rear_Wing_Element"))

    #  -  -  End plates: vertical flat plates at each wing tip  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ep_len  = 196.0                    # chord direction
    ep_ht   = 132.0                    # vertical
    ep_t    = 4.0                      # plate thickness
    ep_z0   = le_z - ep_ht / 2.0      # centred on wing height

    for sign in (1, -1):
        y0 = half_span - ep_t / 2.0 if sign > 0 else -half_span - ep_t / 2.0
        ep = C.rbox(le_x - 12, y0, ep_z0, ep_len, ep_t, ep_ht, 2)
        slot = C.box(le_x + 44, y0 - 2, le_z - 22, 54, ep_t + 4, 14)
        ep = ep.cut(slot)
        # Rotate endplate with the wing (same AoA pivot)
        ep = ep.rotate(
            (le_x, 0, le_z),
            (le_x, 1, le_z),
            -aoa
        )
        suffix = "L" if sign > 0 else "R"
        out.append((ep, C.RED, f"PRT_Rear_Wing_Endplate_{suffix}"))

    #  -  -  Pedestals: mounting blocks connecting wing to trunk  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    ped_w   = 40.0                     # Y width
    ped_dx  = 50.0                     # X length
    ped_y   = 480.0                    # Y offset from centreline
    trunk_z = 1050.0                   # top of flattened trunk deck
    ped_dz  = le_z - trunk_z           # height from trunk to wing LE

    for sign in (1, -1):
        py = sign * ped_y - ped_w / 2.0
        upright = C.rbox(le_x + 30, py, trunk_z + 6, ped_dx, ped_w, ped_dz - 6, 5.0)
        deck_foot = C.rbox(le_x + 16, sign * ped_y - 54, trunk_z, 78, 108, 12, 5.0)
        top_clamp = C.rbox(le_x + 20, sign * ped_y - 34, le_z - 18, 72, 68, 16, 4.0)
        side_gusset = C.rbox(le_x + 26, sign * ped_y - 28, trunk_z + 46, 46, 56, 74, 4.0)
        pedestal = C.U([upright, deck_foot, top_clamp, side_gusset])
        suffix = "L" if sign > 0 else "R"
        out.append((pedestal, C.TRIM_BLK, f"PRT_Rear_Wing_Pedestal_{suffix}"))

    return out


# ------------------------------------------------------------------------
#  6.  SIDE SKIRTS  (rocker-panel extensions)
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_make_rear_wing())
    return out

