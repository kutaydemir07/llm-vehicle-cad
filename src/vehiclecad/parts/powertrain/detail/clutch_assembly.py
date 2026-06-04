"""Clutch assembly  -  flywheel, clutch disc, pressure plate.

Positioned at the engine-transmission interface:
  Flywheel rear face: x=1020, y=0, z=460.
  Pressure plate + disc sandwich:
    z=440-480, r=120 mm (225 mm OD single-plate).

Collision-free:
  Sits between engine (x=380-1000) and gearbox bell-housing (x=1020-1080).
  y stays within  - 130 mm  -  clear of tunnel walls ( - 100 to  - 130 transition).
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.parts.powertrain.detail import layout as L

_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.TRANS
FASTENER = (0.13, 0.13, 0.14)


def _flywheel():
    """Forged steel flywheel, r=128, thickness=22 mm.

    For cyl(r, h, base, (1,0,0)): base[1]=y_centre, base[2]=z_centre.
    """
    x0 = L.ENGINE_REAR_X - 10
    fw = _cyl(128, 22, (x0, L.CL_Y, L.CRANK_Z), (1, 0, 0))   # full disc
    # ring gear outer band
    rg = _cyl(132, 22, (x0, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
         _cyl(126, 30, (x0 - 2, L.CL_Y, L.CRANK_Z), (1, 0, 0)))
    bolts = []
    for sy, sz in ((34, 28), (-34, 28), (34, -28), (-34, -28)):
        bolts.append(_cyl(5.5, 8, (x0 + 18, sy, L.CRANK_Z + sz), (1, 0, 0)))
    return _U([fw, rg] + bolts)


def _pressure_plate():
    """Clutch cover + pressure plate assembly."""
    cover = _cyl(112, 20, (L.ENGINE_REAR_X + 20, L.CL_Y, L.CRANK_Z), (1, 0, 0))   # behind the disc
    cover_inner = _cyl(60, 30, (L.ENGINE_REAR_X + 18, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    fingers = [
        C.swept_tube([(L.ENGINE_REAR_X + 36, 0, L.CRANK_Z),
                      (L.ENGINE_REAR_X + 26, y, L.CRANK_Z + z)], 3.5, cap=True)
        for y, z in ((46, 18), (18, 46), (-18, 46), (-46, 18),
                     (-46, -18), (-18, -46), (18, -46), (46, -18))
    ]
    return _U([cover.cut(cover_inner)] + fingers)


def _clutch_disc():
    """Friction disc, seated against the flywheel rear face (x1012)."""
    disc = _cyl(108, 8, (L.ENGINE_REAR_X + 12, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
           _cyl(38,  12, (L.ENGINE_REAR_X + 11, L.CL_Y, L.CRANK_Z), (1, 0, 0)))
    hub = _cyl(44, 22, (L.ENGINE_REAR_X + 12, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    return disc.fuse(hub)


def _release_bearing():
    """Throw-out bearing sleeve, centred on the input shaft inside the bell."""
    bearing = _cyl(44, 26, (L.TRANS_FRONT_X + 18, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
        _cyl(22, 30, (L.TRANS_FRONT_X + 16, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    )
    collar = _cyl(28, 42, (L.TRANS_FRONT_X + 4, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    return bearing.fuse(collar)


def _clutch_fork():
    """Pressed clutch release fork pivoting through the bellhousing window."""
    arm = C.swept_tube([
        (L.TRANS_FRONT_X + 24, -78, L.CRANK_Z - 2),
        (L.TRANS_FRONT_X + 40, -142, L.CRANK_Z + 26),
        (L.TRANS_FRONT_X + 56, -192, L.CRANK_Z + 44),
    ], 8, cap=True)
    pads = _U([
        _rbox(L.TRANS_FRONT_X + 18, -88, L.CRANK_Z - 14, 20, 28, 12, 4),
        _rbox(L.TRANS_FRONT_X + 42, -196, L.CRANK_Z + 34, 28, 20, 14, 4),
    ])
    return arm.fuse(pads)


def _pilot_bearing():
    """Small needle bearing seated concentrically in the crank/flywheel recess."""
    bearing = _cyl(16, 8, (L.ENGINE_REAR_X + 24, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
        _cyl(8, 10, (L.ENGINE_REAR_X + 23, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    )
    return bearing


def _clutch_slave_cylinder():
    """External slave cylinder and pushrod aimed at the release fork."""
    body = _cyl(16, 74, (L.TRANS_FRONT_X + 24, -214, L.CRANK_Z + 48), (1, 0, 0))
    pushrod = C.swept_tube([
        (L.TRANS_FRONT_X + 78, -214, L.CRANK_Z + 48),
        (L.TRANS_FRONT_X + 56, -190, L.CRANK_Z + 44),
    ], 4, cap=True)
    bracket = _rbox(L.TRANS_FRONT_X + 18, -230, L.CRANK_Z + 28, 34, 20, 44, 4)
    hose_stub = C.swept_tube([
        (L.TRANS_FRONT_X + 30, -230, L.CRANK_Z + 58),
        (L.TRANS_FRONT_X + 12, -260, L.CRANK_Z + 72),
    ], 3, cap=True)
    return _U([body, pushrod, bracket, hose_stub])


def _release_pivot_hardware():
    """Fork pivot ball and spring clip on the bellhousing side."""
    pivot = _cyl(8, 16, (L.TRANS_FRONT_X + 28, -106, L.CRANK_Z - 12), (0, 1, 0))
    clip = _rbox(L.TRANS_FRONT_X + 18, -116, L.CRANK_Z - 22, 24, 6, 20, 2)
    return pivot.fuse(clip)


def parts():
    return [
        (_flywheel(),       (0.32, 0.33, 0.38), "PRT_Flywheel"),
        (_pressure_plate(), COL,                "PRT_Pressure_Plate"),
        (_clutch_disc(),    (0.15, 0.15, 0.18), "PRT_Clutch_Disc"),
        (_release_bearing(), COL,               "PRT_Release_Bearing"),
        (_clutch_fork(),     COL,               "PRT_Clutch_Fork"),
        (_pilot_bearing(),   FASTENER,          "PRT_Pilot_Bearing"),
        (_clutch_slave_cylinder(), COL,          "PRT_Clutch_Slave_Cylinder"),
        (_release_pivot_hardware(), FASTENER,   "PRT_Release_Fork_Pivot_Hardware"),
    ]
