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

def _roll_cage():
    """Bolt-in roll cage: floor-plated, roof-hugging, and clear of the seats."""
    R = 18.0  # tube outer radius
    bars = []

    # Main hoop behind the front seats. Feet sit on plates above the carpet
    # datum; the upper tube is pulled inboard so it cannot read through the DLO
    # as an exterior greenhouse clash.
    bars.append(C.cyl(R, 984, (2520, 580, 240), (0, 0, 1)))
    bars.append(C.cyl(R, 984, (2520, -580, 240), (0, 0, 1)))
    bars.append(C.cyl(R, 1160, (2520, -580, 1224), (0, 1, 0)))

    # A-pillar/down bars and roof side bars run outside the dash and seats.
    bars.append(C.swept_tube([(1588, 606, 240), (1605, 606, 990),
                              (1850, 592, 1204), (2520, 580, 1224)], R, cap=True))
    bars.append(C.swept_tube([(1588, -606, 240), (1605, -606, 990),
                              (1850, -592, 1204), (2520, -580, 1224)], R, cap=True))

    # Harness and dash bars sit behind the seat shoulders and ahead of knees.
    bars.append(C.cyl(R - 3, 1100, (2520, -550, 858), (0, 1, 0)))
    bars.append(C.cyl(R - 4, 1080, (1598, -540, 724), (0, 1, 0)))

    # Door bars are outside the front seat bolsters and inside the door cards.
    for sy in (1, -1):
        bars.append(C.swept_tube([(1660, sy * 560, 506), (2050, sy * 558, 642),
                                  (2460, sy * 558, 802)], R - 4, cap=True))
        bars.append(C.swept_tube([(1665, sy * 560, 792), (2050, sy * 558, 660),
                                  (2460, sy * 558, 524)], R - 4, cap=True))

    # Rear stays route over the rear bench shoulders to the rear shelf area.
    bars.append(C.swept_tube([(2520, 550, 1206), (2760, 544, 1020),
                              (3070, 520, 760)], R - 3, cap=True))
    bars.append(C.swept_tube([(2520, -550, 1206), (2760, -544, 1020),
                              (3070, -520, 760)], R - 3, cap=True))

    # Main hoop diagonal brace and small node gussets.
    bars.append(C.swept_tube([(2520, -526, 1194), (2520, 526, 300)], R - 4, cap=False))
    for x, cy in ((1588, 606), (1588, -606), (2520, 580), (2520, -580)):
        bars.append(C.rbox(x - 46, cy - 42, 232, 92, 84, 8, 3))
        bars.append(C.rbox(x - 20, cy - 20, 240, 40, 40, 16, 4))

    return [(C.U(bars), CAGE, "roll_cage")]


# ------------------------------------------------------------------------
#  PUBLIC API
# ------------------------------------------------------------------------




def parts():
    return _roll_cage()

