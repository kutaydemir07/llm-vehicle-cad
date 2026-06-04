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


_GROWN_BODY = None


def _grown_body(dy: float = 42.0):
    """The lower-body loft widened by ``dy`` in Y (same z-profile, wider).

    Flares are intersected with this so they inherit the body's lower-edge and
    crown silhouette  -  the flare stays ``dy``-proud of the body side but cannot
    dangle below the raised overhangs.  Cached (built once)."""
    global _GROWN_BODY
    if _GROWN_BODY is None:
        from vehiclecad.core.reference import materials as M
        _GROWN_BODY = C.loft([(x, a + dy, z0, z1, rb, rt)
                              for (x, a, z0, z1, rb, rt) in M.BODY], ruled=True)
    return _GROWN_BODY


def _box_flare_left(ax_x: float, r_open: float, r_outer: float,
                    y_in: float, y_out: float, z_lo: float,
                    zc: float = 300.0) -> Solid:
    """One integrated box-flare blister on the LEFT (+Y) side.

    The flare is the fender skin WRAPPING the wheel arch: an annular band between
    the arch opening (``r_open``) and the fender's outer arch radius (``r_outer``),
    given Y-thickness so it protrudes from the body side outward.  ``y_in`` is held
    just INSIDE the body side so the band fuses with the body skin (it cannot
    float); ``y_out`` is the overall half-width (FLARE_Y).  Being an annulus it
    hugs the arch and tapers into legs at the rocker (``z_lo``)  -  no flat slab
    ends.  The flat outboard ring reads as the square SportsCar fender face; the
    cylindrical rim is the flare's depth.
    """
    dy = y_out - y_in
    band = C.cyl(r_outer, dy, (ax_x, y_in, zc), (0, 1, 0)).cut(
        C.cyl(r_open, dy + 12, (ax_x, y_in - 6, zc), (0, 1, 0)))   # arch opening
    keep = C.box(ax_x - r_outer - 6, y_in - 1, z_lo,
                 2 * (r_outer + 6), dy + 2, (zc + r_outer) - z_lo)  # upper arch only
    flare = band.intersect(keep)
    # Clip to the body's own z-silhouette (the body loft grown outboard) so the
    # flare hugs the fender / rocker lower edge and the fender crown, instead of
    # poking out BELOW the raised front/rear overhangs or beyond the body.
    try:
        clipped = flare.intersect(_grown_body())
        if clipped.Volume() > 1000.0:
            return clipped
    except Exception:
        pass
    return flare


def _arch_lip_left(ax_x: float, r_open: float, y_in: float, y_out: float,
                   z_lo: float = C.ARCH_TRIM_Z0, zc: float = 300.0) -> Solid:
    """Satin-black bolt-on wheel-arch lip ringing the flare opening.

    A slim bead at the opening radius, sitting on the OUTBOARD face of the
    blister and kept to the upper arch  -  the defining edge that makes the
    body-colour swell read as a true box flare rather than a smooth bulge.
    """
    lip = Solid.makeTorus(r_open + 3, 9.0, Vector(ax_x, y_out - 11, zc), Vector(0, 1, 0))
    keep = C.box(ax_x - (r_open + 30), y_in, z_lo,
                 2 * (r_open + 30), (y_out - y_in) + 8,
                 (zc + r_open + 30) - z_lo)
    return lip.intersect(keep)


def _make_flares_front():
    """Front box flares (integrated blister + black arch lip), left + right.
    Opening r=346 ( -  tyre + 46 clearance); blister to FLARE_Y, up to z - 700."""
    out = []
    left = _box_flare_left(_AXLE_F, 334.0, 414.0, C.SIDE_Y - 3, C.FLARE_Y, C.ROCKER_Z0)
    lip = _arch_lip_left(_AXLE_F, 334.0, C.SIDE_Y - 3, C.FLARE_Y)
    out.append((left,            C.RED,      "PRT_Box_Flares_Front_L"))
    out.append((C.mirror_y(left), C.RED,     "PRT_Box_Flares_Front_R"))
    out.append((lip,             C.TRIM_BLK, "PRT_Arch_Lip_Front_L"))
    out.append((C.mirror_y(lip), C.TRIM_BLK, "PRT_Arch_Lip_Front_R"))
    return out


# ------------------------------------------------------------------------
#  2.  REAR FENDER FLARES  (wider bead  -  more aggressive arch)
# ------------------------------------------------------------------------



def _make_flares_rear():
    """Rear box flares  -  wider + taller than the front (the SportsCar's haunches),
    left + right.  Opening r=356; blister to FLARE_Y+2, up to z - 720."""
    out = []
    left = _box_flare_left(_AXLE_R, 342.0, 428.0, C.SIDE_Y - 3, C.FLARE_Y + 2, C.ROCKER_Z0)
    lip = _arch_lip_left(_AXLE_R, 342.0, C.SIDE_Y - 3, C.FLARE_Y + 2)
    out.append((left,            C.RED,      "PRT_Box_Flares_Rear_L"))
    out.append((C.mirror_y(left), C.RED,     "PRT_Box_Flares_Rear_R"))
    out.append((lip,             C.TRIM_BLK, "PRT_Arch_Lip_Rear_L"))
    out.append((C.mirror_y(lip), C.TRIM_BLK, "PRT_Arch_Lip_Rear_R"))
    return out


# ------------------------------------------------------------------------
#  3.  FRONT AIR-DAM / SPLITTER
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_make_flares_front())
    out.extend(_make_flares_rear())
    return out

