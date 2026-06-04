"""Front Recaro bucket seats  -  driver (left) and passenger (right).

H-point at z=430, seat-back rising below the roof/cage header.
Driver centre: x=2020, y=+330.
Passenger centre: x=2020, y=-330.

Collision-free:
   -  Clear of centre tunnel (inner edge > |y| 130; tunnel half-width is 100).
   -  Clear of door cards/cage door bars by keeping the outer bolster < |y| 555.
   -  x=2020 leaves foot room from the pedal box and clears the main roll hoop.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from .seat import _seat

COL_CLOTH  = (0.10, 0.10, 0.11)
COL_RAILS  = (0.40, 0.40, 0.42)


def parts():
    # driver seat (left, +y)
    body_l, rails_l = _seat(2020,  330)
    # passenger seat (right, -y)
    body_r, rails_r = _seat(2020, -330)
    return [
        (body_l,  COL_CLOTH, "PRT_Front_Seat_Driver"),
        (rails_l, COL_RAILS, "PRT_Front_Seat_Rails_Driver"),
        (body_r,  COL_CLOTH, "PRT_Front_Seat_Passenger"),
        (rails_r, COL_RAILS, "PRT_Front_Seat_Rails_Passenger"),
    ]
