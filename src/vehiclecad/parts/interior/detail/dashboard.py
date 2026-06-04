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

def _dashboard():
    """Dashboard mated to the cowl/firewall with driver and HVAC clearances."""
    # The rear face sits at x=1670 for the occupant-facing dash surface.  End caps
    # stop inboard of the cage A-pillar bars, leaving service clearance at both
    # kick panels.
    upper_pad = C.rbox(1448, -635, 898, 222, 1270, 62, 18)
    lower_fascia = C.rbox(1510, -610, 736, 160, 1220, 175, 12)
    knee_roll = C.rbox(1588, -570, 690, 74, 1140, 64, 16)
    cowl_brackets = C.U([
        C.rbox(1450, 548, 840, 46, 74, 112, 6),
        C.rbox(1450, -622, 840, 46, 74, 112, 6),
        C.rbox(1476, -34, 908, 36, 68, 52, 5),
    ])
    main = C.U([upper_pad, lower_fascia, knee_roll, cowl_brackets])

    # Openings that a real CAD assembly would reserve before installing trim:
    # steering column sweep, pedal-knee space, glovebox, radio/HVAC and demist ducts.
    column_sweep = C.rbox(1488, 230, 668, 246, 248, 228, 18)
    pedal_knee = C.rbox(1560, 292, 650, 120, 260, 110, 12)
    glovebox_opening = C.rbox(1600, -545, 760, 98, 326, 134, 10)
    centre_stack_opening = C.rbox(1602, -130, 774, 96, 260, 142, 10)
    demist_l = C.rbox(1468, 280, 944, 54, 250, 18, 5)
    demist_r = C.rbox(1468, -530, 944, 54, 250, 18, 5)
    for cutter in (column_sweep, pedal_knee, glovebox_opening,
                   centre_stack_opening, demist_l, demist_r):
        main = main.cut(cutter)

    # LHD instrument binnacle - hooded, rear-facing, and clear of the steering rim.
    binnacle_shell = C.rbox(1518, 190, 820, 174, 340, 132, 14)
    binnacle_lip = C.rbox(1510, 174, 930, 178, 372, 40, 12)
    binnacle_recess = C.rbox(1598, 222, 842, 102, 276, 82, 8)
    binnacle = C.U([binnacle_shell, binnacle_lip]).cut(binnacle_recess)

    # Gauge plate and individual round gauge bosses, all centred in the binnacle.
    gauge_plate = C.rbox(1662, 236, 846, 8, 254, 86, 5)
    tach = C.cyl(38, 10, (1660, 312, 888), (1, 0, 0))
    speedo = C.cyl(38, 10, (1660, 418, 888), (1, 0, 0))
    aux_l = C.cyl(18, 10, (1660, 262, 858), (1, 0, 0))
    aux_r = C.cyl(18, 10, (1660, 468, 858), (1, 0, 0))
    gauge_face = C.U([gauge_plate, tach, speedo, aux_l, aux_r])

    # Centre vents and radio/HVAC stack share the dash centreline and sit on the
    # occupant-facing rear plane rather than floating on the firewall side.
    vent_frame = C.rbox(1660, -126, 842, 14, 252, 118, 5)
    vent_opening = C.box(1656, -102, 858, 24, 204, 84)
    slats = [
        C.rbox(1662, -94, 878 + i * 22, 16, 188, 5, 2)
        for i in range(3)
    ]
    centre_vents = C.U([vent_frame.cut(vent_opening)] + slats)

    glovebox_lid = C.U([
        C.rbox(1660, -548, 764, 12, 322, 128, 8),
        C.rbox(1670, -418, 824, 10, 60, 12, 3),
    ])

    return [
        (main, DARK, "dashboard"),
        (binnacle, DARK, "instrument_binnacle"),
        (gauge_face, GAUGE, "gauge_cluster"),
        (centre_vents, DARK, "centre_vents"),
        (glovebox_lid, DARK, "glovebox"),
    ]


# ------------------------------------------------------------------------
#  STEERING
# ------------------------------------------------------------------------




def parts():
    out = []
    out.extend(_dashboard())
    return out

