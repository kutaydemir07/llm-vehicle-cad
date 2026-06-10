"""Fuel system components and separate fuel-line routes.

Packaging notes (all verified against the underbody):
  * The tank's outboard-lower corners are NOTCHED where the semi-trailing
    arms sweep (arm envelope x2906..3418, |y|>252, z254..358) -- the
    production saddle tank has exactly these reliefs.
  * The in-tank pump hangs from a top flange; nothing rises above z448 so it
    stays inside the bench's pump-hatch pocket.
  * Filter and feed/return lines run UNDER the floor (tube top < z215), never
    through the cabin: floor sheet z215/220, frame rails at |y|~462..518.
"""

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
    tank = _U([left, right, neck])
    # trailing-arm corner notches (arm sweep z254..358 outboard of |y|252)
    tank = tank.cut(_box(2958, 250, 256, 192, 108, 110))
    tank = tank.cut(_box(2958, -358, 256, 192, 108, 110))
    return tank


def _fuel_pump():
    """In-tank pump: canister body hanging from a top mounting flange with
    feed/return spigots and the electrical stub -- not a bare cylinder."""
    canister = _cyl(40, 118, (3050, 150, 302), (0, 0, 1))
    canister = canister.cut(_cyl(36, 6, (3050, 150, 300), (0, 0, 1)))
    flange = _cyl(48, 6, (3050, 150, 424), (0, 0, 1))
    feed = _cyl(6, 16, (3032, 150, 430), (0, 0, 1))
    ret = _cyl(5, 14, (3068, 150, 430), (0, 0, 1))
    elec = _rbox(3044, 168, 428, 12, 18, 10, 3)
    strainer = _cyl(30, 8, (3050, 150, 294), (0, 0, 1))
    return _U([canister, flange, feed, ret, elec, strainer])


def _fuel_filter():
    """Inline canister filter UNDER the floor beside the left frame rail
    (production position) with hose-barb end fittings."""
    body = _cyl(30, 78, (2706, 430, 184), (1, 0, 0))
    dome_f = C.loft_circles([((2706, 430, 184), 30, (1, 0, 0)),
                             ((2698, 430, 184), 22, (1, 0, 0)),
                             ((2694, 430, 184), 10, (1, 0, 0))])
    dome_r = C.loft_circles([((2784, 430, 184), 30, (1, 0, 0)),
                             ((2792, 430, 184), 22, (1, 0, 0)),
                             ((2796, 430, 184), 10, (1, 0, 0))])
    barb_f = _cyl(6, 14, (2680, 430, 184), (1, 0, 0))
    barb_r = _cyl(6, 14, (2796, 430, 184), (1, 0, 0))
    band = _cyl(32, 10, (2740, 430, 184), (1, 0, 0)).cut(
        _cyl(30.5, 14, (2738, 430, 184), (1, 0, 0)))
    return _U([body, dome_f, dome_r, barb_f, barb_r, band])


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
    # tank -> under-floor run beside the left rail (tube top z<=208 < floor 215)
    # -> filter -> rises in the ENGINE BAY (x<1220, ahead of the firewall) -> rail
    return C.swept_tube(
        [(3060, 350, 340), (2965, 380, 280), (2880, 420, 210),
         (2796, 430, 184),                       # filter outlet barb
         (2200, 430, 196), (1300, 430, 196),
         (1180, 410, 250), (640, 348, 540), (505, 356, 701)],
        8,
        cap=True,
    )


def _fuel_return_line():
    # rail -> engine-bay drop (clear below the intake head flange, z<650 at
    # its y-band) -> under-floor run 14 mm inboard of the feed line
    return C.swept_tube(
        [(520, 238, 666), (560, 300, 560), (700, 340, 360), (1180, 444, 246),
         (1300, 444, 190), (2200, 444, 190), (2700, 444, 190),
         (2880, 430, 214), (3060, 320, 324)],
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
