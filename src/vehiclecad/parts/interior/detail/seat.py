"""ASM_Packaging_Interior  -  ergonomic spatial-claim volumes.

Upgraded from the basic box shapes to proper packaging envelopes:
  * Recaro bucket seats (with bolsters, H-point at SAE J826 reference)
  * Dashboard with instrument binnacle recess + centre vents
  * Centre console with gearshift
  * Steering wheel, column, and rack-and-pinion housing
  * Bolt-in roll cage (main hoop + A-pillar bars + harness bar)

All geometry sits inside the greenhouse (between the A- and C-pillars,
below the roof, above the floorpan) and is visible through the glazing.
"""
from __future__ import annotations
import numpy as np
import cadquery as cq
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

#  -  -  local colours  -  - 
DARK    = (0.09, 0.09, 0.10)
SEAT_BK = (0.10, 0.10, 0.11)    # black Recaro cloth
SEAT_FL = (0.12, 0.12, 0.14)    # seat flank / bolster
CAGE    = (0.55, 0.05, 0.05)    # roll-cage red
ALCANT  = (0.14, 0.14, 0.16)    # alcantara / suede-touch surfaces
GAUGE   = (0.04, 0.04, 0.05)    # instrument cluster face


# ------------------------------------------------------------------------
#  SEATS  -  Recaro SportsCar buckets
# ------------------------------------------------------------------------

def _seat(cx, cy):
    """Recaro-style bucket seat, H-point (hip) at (cx, cy, 430).

    Vehicle frame: +x = REARWARD.  The occupant faces FORWARD (-x), so the seat
    cushion extends forward of the hip (lower x) under the thighs, and the
    backrest rises BEHIND the hip (higher x), reclined ~15 deg.  The earlier
    version had the backrest in front of the cushion -- the seat faced backwards.
    """
    z_h = 430.0

    # --- lower cushion: forward of the hip with bolsters clear of the tunnel ---
    base = C.rbox(cx - 390, cy - 192, 300, 450, 384, 92, 18)
    thigh_pad = C.rbox(cx - 420, cy - 150, 364, 280, 300, 52, 16)
    rear_pad = C.rbox(cx - 132, cy - 172, 350, 170, 344, 70, 16)
    bolster_base_L = C.rbox(cx - 388, cy + 152, 314, 424, 48, 110, 12)
    bolster_base_R = C.rbox(cx - 388, cy - 200, 314, 424, 48, 110, 12)
    cushion = C.U([base, thigh_pad, rear_pad, bolster_base_L, bolster_base_R])

    # --- backrest: behind the hip, reclined rearward, with harness slots ---
    back = C.rbox(cx + 0, cy - 170, 430, 122, 340, 490, 20)
    bolster_back_L = C.rbox(cx - 12, cy + 128, 442, 146, 54, 468, 14)
    bolster_back_R = C.rbox(cx - 12, cy - 182, 442, 146, 54, 468, 14)
    headrest = C.rbox(cx + 18, cy - 98, 900, 94, 196, 130, 24)
    shoulder_pad = C.rbox(cx - 6, cy - 186, 718, 148, 372, 122, 16)
    backrest = C.U([back, bolster_back_L, bolster_back_R, shoulder_pad, headrest])
    harness_l = C.rbox(cx + 22, cy + 36, 746, 160, 46, 90, 10)
    harness_r = C.rbox(cx + 22, cy - 82, 746, 160, 46, 90, 10)
    backrest = backrest.cut(harness_l).cut(harness_r)
    # recline about the hip line (+Y axis): tilts the top rearward (+x) ~15 deg
    backrest = backrest.rotate((cx, cy, z_h), (cx, cy + 1.0, z_h), 15.0)

    seat_body = cushion.fuse(backrest)

    # --- slider rails and mounting feet: carpet top is z~231, seat pan bottom is z=300 ---
    rail_L = C.rbox(cx - 372, cy - 162, 242, 408, 24, 28, 4)
    rail_R = C.rbox(cx - 372, cy + 138, 242, 408, 24, 28, 4)
    cross_front = C.rbox(cx - 350, cy - 150, 270, 36, 300, 30, 4)
    cross_rear = C.rbox(cx - 20, cy - 150, 270, 36, 300, 30, 4)
    feet = []
    for px in (cx - 350, cx - 20):
        for py in (cy - 162, cy + 138):
            feet.append(C.rbox(px - 22, py - 8, 232, 68, 40, 10, 3))
            feet.append(C.rbox(px, py, 270, 28, 24, 30, 3))
    rails = C.U([rail_L, rail_R, cross_front, cross_rear] + feet)
    return seat_body, rails


# ------------------------------------------------------------------------
#  DASHBOARD
# ------------------------------------------------------------------------


def parts():
    """Defers to seats_front.py for actual seat assemblies."""
    return []

