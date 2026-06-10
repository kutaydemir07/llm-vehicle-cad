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
from vehiclecad.geometry import machine_elements as ME
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
    # flywheel face starts BEHIND the 8 mm rear engine plate (plate x990..998)
    x0 = L.ENGINE_REAR_X - 2
    fw = _cyl(124, 22, (x0, L.CL_Y, L.CRANK_Z), (1, 0, 0))   # full disc
    # centre bore: receives the pilot bearing, lets the input-shaft stub pass
    fw = fw.cut(_cyl(17, 26, (x0 - 2, L.CL_Y, L.CRANK_Z), (1, 0, 0)))
    # shrunk-on starter RING GEAR with real teeth (module ~2.7, 96 teeth)
    rg = ME.ring_gear_band_x(129.0, 18, x0 + 2, L.CL_Y, L.CRANK_Z, teeth=96, depth=7.0)
    bolts = []
    for sy, sz in ((34, 28), (-34, 28), (34, -28), (-34, -28)):
        bolts.append(_cyl(5.5, 4, (x0 + 18, sy, L.CRANK_Z + sz), (1, 0, 0)))
    return _U([fw, rg] + bolts)


def _pressure_plate():
    """Clutch cover + pressure plate assembly, stacked BEHIND the disc ring
    (flywheel face 1020 -> disc ring to 1028 -> cover 1028..1048)."""
    cover = _cyl(112, 20, (L.ENGINE_REAR_X + 28, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    cover_inner = _cyl(60, 30, (L.ENGINE_REAR_X + 26, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    fingers = [
        C.swept_tube([(L.ENGINE_REAR_X + 44, 0, L.CRANK_Z),
                      (L.ENGINE_REAR_X + 34, y, L.CRANK_Z + z)], 3.5, cap=True)
        for y, z in ((46, 18), (18, 46), (-18, 46), (-46, 18),
                     (-46, -18), (-18, -46), (18, -46), (46, -18))
    ]
    return _U([cover.cut(cover_inner)] + fingers)


def _clutch_disc():
    """Sprung-hub friction disc: friction ring with radial relief slots, a
    carrier flange with four damper-spring windows (springs visible in them),
    and a splined hub bored for the r15 input shaft."""
    x0 = L.ENGINE_REAR_X + 20            # ring face seats on the flywheel (x1020)
    ax0 = (x0, L.CL_Y, L.CRANK_Z)
    ax1 = (x0 + 1, L.CL_Y, L.CRANK_Z)
    ring = _cyl(108, 8, ax0, (1, 0, 0)).cut(_cyl(72, 12, (x0 - 1, L.CL_Y, L.CRANK_Z), (1, 0, 0)))
    for k in range(6):
        slot = C.box(x0 - 2, L.CL_Y - 1.5, L.CRANK_Z + 74, 12, 3.0, 36)
        ring = ring.cut(slot.rotate(ax0, ax1, k * 60.0))
    flange = _cyl(74, 6, (x0 + 1, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
             _cyl(34, 10, (x0, L.CL_Y, L.CRANK_Z), (1, 0, 0)))
    springs = []
    for k in range(4):
        window = C.box(x0 - 2, L.CL_Y - 17, L.CRANK_Z + 40, 12, 34, 22)
        flange = flange.cut(window.rotate(ax0, ax1, 45.0 + k * 90.0))
        spring = _cyl(8, 30, (x0 + 4, L.CL_Y - 15, L.CRANK_Z + 51), (0, 1, 0))
        springs.append(spring.rotate(ax0, ax1, 45.0 + k * 90.0))
    hub = _cyl(40, 22, ax0, (1, 0, 0)).cut(_cyl(15, 26, (x0 - 1, L.CL_Y, L.CRANK_Z), (1, 0, 0)))
    return _U([ring, flange, hub] + springs)


def _release_bearing():
    """Throw-out bearing sleeve, centred on the input shaft inside the bell.

    The guide collar is BORED r17 so it slides over the r15 input shaft with a
    2 mm running clearance, and the whole sleeve sits AFT of the shaft's
    clutch splines (which end at x1042) on the plain journal."""
    bearing = _cyl(44, 26, (L.TRANS_FRONT_X + 28, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
        _cyl(22, 30, (L.TRANS_FRONT_X + 26, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    )
    collar = _cyl(28, 40, (L.TRANS_FRONT_X + 26, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
        _cyl(17, 44, (L.TRANS_FRONT_X + 24, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    )
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
    """Small needle bearing seated concentrically in the crank/flywheel recess.

    Seated INSIDE the flywheel centre bore (r17); its r15.5 bore is a slip fit
    over the r15 input-shaft body that begins at x=TRANS_FRONT_X-28."""
    bearing = _cyl(16, 8, (L.ENGINE_REAR_X + 6, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
        _cyl(15.5, 12, (L.ENGINE_REAR_X + 5, L.CL_Y, L.CRANK_Z), (1, 0, 0))
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
