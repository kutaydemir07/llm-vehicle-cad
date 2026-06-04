"""Fuel system components and separate fuel-line routes."""

from __future__ import annotations

from vehiclecad.core.reference import common as C

_box = C.box
_cyl = C.cyl
_rbox = C.rbox
_U = C.U
COL = (0.28, 0.32, 0.38)


def _fuel_tank():
    # saddle tank drawn as hollow shells so the in-tank pump runs in clearance
    left = _rbox(2965, 70, 270, 175, 275, 140, 10).cut(
        _box(2975, 80, 280, 155, 255, 130))
    right = _rbox(2965, -345, 270, 175, 275, 140, 10).cut(
        _box(2975, -335, 280, 155, 255, 130))
    neck = _cyl(26, 70, (3010, 320, 360), (0, 0, 1))
    return _U([left, right, neck])


def _fuel_pump():
    return _cyl(46, 150, (3050, 150, 300), (0, 0, 1))


def _fuel_filter():
    return _cyl(30, 90, (2700, 430, 300), (1, 0, 0))


def _fuel_rail():
    # ITB fuel rail runs OUTBOARD of the runners (clear of the head and the intake
    # flange), with injectors dropping inboard toward the runner ports.
    rail = _rbox(490, 352, 694, 420, 18, 16, 6)
    injectors = []
    for index in range(4):
        ix = 510 + index * 120
        injectors.append(_cyl(7, 34, (ix, 356, 700), (0, -0.5, -1)))
    return _U([rail] + injectors)


def _fuel_feed_line():
    # tank -> filter -> forward under the floor -> up to the ITB fuel-rail inlet
    # (which now sits outboard of the runners at y~356)
    return C.swept_tube(
        [(3060, 350, 340), (2700, 430, 300), (2000, 360, 265), (1200, 340, 270), (640, 348, 540), (505, 356, 701)],
        8,
        cap=True,
    )


def _fuel_return_line():
    return C.swept_tube(
        [(520, 238, 666), (700, 305, 286), (1200, 318, 258), (2000, 338, 252), (2700, 406, 286), (3060, 320, 324)],
        6,
        cap=True,
    )


def _fuel_tank_vent_line():
    return C.swept_tube([(3010, 320, 405), (3300, 390, 470), (3460, 420, 520)], 5, cap=True)


def parts():
    return [
        (_fuel_tank(), COL, "PRT_Fuel_Tank"),
        (_fuel_pump(), C.STEEL, "PRT_Fuel_Pump"),
        (_fuel_filter(), C.STEEL, "PRT_Fuel_Filter"),
        (_fuel_rail(), C.ALLOY_E, "PRT_Fuel_Rail_ITB"),
        (_fuel_feed_line(), C.STEEL, "PRT_Fuel_Feed_Line"),
        (_fuel_return_line(), C.STEEL, "PRT_Fuel_Return_Line"),
        (_fuel_tank_vent_line(), C.STEEL, "PRT_Fuel_Tank_Vent_Line"),
    ]

