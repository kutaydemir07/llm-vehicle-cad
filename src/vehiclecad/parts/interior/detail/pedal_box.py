"""Pedal box assembly  -  clutch, brake and throttle pedals.

All pedals sit inside the cabin, behind the firewall at x=1220.
Left side: y=+340-430 (clutch), y=+210-300 (brake), y=+86-160 (throttle).

Collision-free:
   -  Pedals sit above the carpet (z=232+) and below the steering column.
   -  Firewall bracket touches the cabin side of the firewall; pads remain x>1220.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL_PAD  = (0.08, 0.08, 0.10)
COL_ARM  = (0.40, 0.40, 0.45)


def _pedal(px, py, pz_pivot, pz_pad, reach=118):
    """Generic pedal: pivot tube + arm + rubber pad."""
    z_low  = min(pz_pivot, pz_pad)
    z_high = max(pz_pivot, pz_pad)
    pivot = C.cyl(11, 58, (px, py - 29, pz_pivot), (0, 1, 0))
    arm = C.swept_tube([(px, py, pz_pivot), (px + reach * 0.55, py - 2, 405),
                        (px + reach, py - 4, pz_pad + 20)], 8, cap=True)
    pad = C.rbox(px + reach - 20, py - 36, pz_pad - 32, 44, 72, 30, 5)
    return C.U([pivot, arm, pad])


def _pedal_box():
    firewall_bracket = C.rbox(1226, 92, 486, 38, 366, 54, 6)
    pivot_tube = C.cyl(14, 354, (1260, 92, 520), (0, 1, 0))
    clutch = _pedal(1280, 410, 520, 292, reach=126)
    brake = _pedal(1282, 270, 520, 292, reach=116)
    throttle = _pedal(1276, 158, 500, 304, reach=134)
    dead = C.rbox(1320, 484, 248, 70, 96, 42, 4)
    heel_plate = C.rbox(1370, 124, 232, 150, 382, 8, 3)
    return C.U([firewall_bracket, pivot_tube, clutch, brake, throttle, dead, heel_plate])


def parts():
    box   = _pedal_box()
    # assemble both arms + pads together
    return [(box, COL_ARM, "PRT_Pedal_Box")]
