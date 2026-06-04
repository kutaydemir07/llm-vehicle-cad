"""ASM_4310_Power_Steering_Reservoir - reservoir, bracket and hydraulic hoses.

The ModelA SportsCar rack lives low under the I4_Engine oil pan.  The reservoir is carried on
the left front inner-bay bracket with two small hoses routed down to the rack
input side, so the part reads as mounted hardware instead of a loose bottle.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

_rbox = C.rbox
_cyl  = C.cyl
_U    = C.U
STEER = SK.STEERING


def _ps_reservoir():
    """Fluid reservoir with bay bracket and two routed rack hoses."""
    bottle = _rbox(464, 420, 690, 70, 70, 100, 8)
    cap = _cyl(18, 14, (484, 455, 790), (0, 0, 1))
    bracket = _rbox(450, 392, 684, 12, 102, 76, 4)
    strap_hi = _rbox(452, 412, 744, 18, 74, 12, 3)
    strap_lo = _rbox(452, 412, 700, 18, 74, 12, 3)

    # Hoses run down to hydraulic ports on the rack VALVE BODY (the pinion side),
    # not onto the mechanical input spline; the ends meet the valve-body surface.
    feed = C.swept_tube([
        (504, 454, 705),
        (620, 424, 620),
        (710, 340, 430),
        (748, 300, 320),
        (760, 278, 252),
    ], 5, cap=True)
    ret = C.swept_tube([
        (476, 422, 694),
        (600, 376, 585),
        (716, 312, 372),
        (772, 270, 258),
    ], 4, cap=True)

    return _U([bottle, cap, bracket, strap_hi, strap_lo, feed, ret])


def parts():
    # No pump on standard SportsCar  -  reservoir only
    return [(_ps_reservoir(), C.ALLOY_E, "PRT_PS_Reservoir")]
