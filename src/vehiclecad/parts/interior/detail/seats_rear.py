"""Rear bench seat.

Positioned at x=2765-3035, y=-455 to +455, z=304-728.
Backrest at x=3040-3114, z=330-850.

Collision-free:
   -  x=2765 is behind front seats and ahead of the rear bulkhead.
   -  y= - 455 clears the wheel tubs and quarter inner panels.
   -  z top of seat = 850, clear of C-pillar shelf (z=1016+).
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL  = (0.11, 0.11, 0.13)


def _rear_bench():
    # Rear squab sits on the rear floor and is narrowed between the wheel tubs.
    cushion = C.rbox(2765, -455, 304, 270, 910, 124, 12)
    front_roll = C.cyl(38, 900, (2762, -450, 410), (0, 1, 0))
    backrest = C.rbox(3040, -438, 330, 74, 876, 520, 14)
    shoulder_roll = C.cyl(34, 840, (3036, -420, 830), (0, 1, 0))
    bol_l = C.rbox(2784, 418, 326, 240, 46, 118, 8)
    bol_r = C.mirror_y(bol_l)
    centre_seam = C.rbox(2782, -8, 428, 238, 16, 16, 3)
    return C.U([cushion, front_roll, backrest, shoulder_roll, bol_l, bol_r, centre_seam])


def parts():
    return [(_rear_bench(), COL, "PRT_Rear_Bench_Seat")]
