"""ManualGearbox 265/5 five-speed manual transmission.

The ManualGearbox 265 is a compact 5-speed unit.  It is positioned inline on the
centreline, bolted to the I4_Engine flywheel housing at the engine rear plane,
with the tailshaft output mated to the propshaft front hardpoint.

Dimensions (real ManualGearbox 265):
  Length: ~400 mm (bell-housing face to tailshaft)
  Width (widest): ~280 mm at the bell-housing
  Height: ~240 mm

CAD mating notes:
  * bellhousing front flange is concentric with the clutch / crank axis.
  * rear output flange is centred at POWERTRAIN["prop_front"].
  * transmission mount pad is centred at POWERTRAIN["trans_mount"].
  * the tail cone slopes from the clutch axis down to the propshaft axis, so the
    gearbox, clutch, and propshaft are one continuous driveline chain.
  * the casing is hollowed around the gear train and emits functional internals:
    input shaft, layshaft, output shaft, five gear pairs, reverse idler, synchro
    hubs, selector forks/rails, and bearings.
"""
from __future__ import annotations
import math
from vehiclecad.core.reference import common as C
from vehiclecad.geometry import machine_elements as ME
from vehiclecad.parts.powertrain.detail import layout as L

_box  = C.box
_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.TRANS
GEAR_C = (0.48, 0.49, 0.52)
SHAFT_C = (0.62, 0.63, 0.66)
SELECTOR_C = (0.34, 0.35, 0.38)
BEARING_C = (0.56, 0.57, 0.60)

MAIN_Y, MAIN_Z = 0.0, L.CRANK_Z
LAY_Y, LAY_Z = -72.0, 394.0
GEAR_XS = (1118.0, 1158.0, 1198.0, 1238.0, 1278.0)
GEAR_WIDTH = 22.0


def _manualgearbox_265():
    """Bellhousing + main casing + tail cone, centred on the skeleton axes."""
    prop_x, prop_y, prop_z = L.PROPSHAFT_FRONT
    mount_x, mount_y, mount_z = L.GEARBOX_MOUNT

    # Bellhousing: a shallow cast cone with a flat engine-side flange.  Its
    # front face sits directly behind the clutch pack at x=1020 and shares the
    # crank axis (y=0, z=445).
    bell = C.loft_circles([
        ((L.TRANS_FRONT_X, L.CL_Y, L.CRANK_Z), 145, (1, 0, 0)),
        ((1056,           L.CL_Y, L.CRANK_Z), 162, (1, 0, 0)),
        ((1092,           L.CL_Y, 438),       120, (1, 0, 0)),
    ], ruled=True)
    bell_inner = C.loft_circles([
        ((L.TRANS_FRONT_X - 6, L.CL_Y, L.CRANK_Z), 132, (1, 0, 0)),
        ((1056,               L.CL_Y, L.CRANK_Z), 130, (1, 0, 0)),
        ((1100,               L.CL_Y, 438),        78, (1, 0, 0)),
    ], ruled=True)
    bell = bell.cut(bell_inner)
    bell_mouth = _cyl(88, 10, (L.TRANS_FRONT_X - 5, L.CL_Y, L.CRANK_Z), (1, 0, 0)).cut(
        _cyl(50, 14, (L.TRANS_FRONT_X - 7, L.CL_Y, L.CRANK_Z), (1, 0, 0))
    )
    bell = bell.fuse(bell_mouth)

    # Gearbox casing and ribs.  The main case is tight to the tunnel envelope but
    # stays symmetric about the centreline.
    main_case = _rbox(1090, -108, 344, 218, 216, 204, 14)
    gear_cavity = _rbox(1102, -96, 374, 194, 188, 154, 10)
    shaft_bores = _U([
        _cyl(26, 248, (1076, MAIN_Y, MAIN_Z), (1, 0, 0)),
        _cyl(24, 248, (1076, LAY_Y, LAY_Z), (1, 0, 0)),
    ])
    main_case = main_case.cut(gear_cavity).cut(shaft_bores)
    top_cover = _rbox(1120, -54, 548, 150, 108, 30, 6)
    side_ribs = [
        _rbox(1110 + i * 44, 104, 390, 10, 16, 118, 3) for i in range(4)
    ] + [
        _rbox(1110 + i * 44, -120, 390, 10, 16, 118, 3) for i in range(4)
    ]

    # Tail cone: mated to the propshaft front hardpoint at the rear.  The output
    # flange is centred exactly on that hardpoint, eliminating the prior z offset.
    tail = C.loft_circles([
        ((1296, L.CL_Y, 432), 80, (1, 0, 0)),
        ((1360, L.CL_Y, 424), 58, (1, 0, 0)),
        ((prop_x, prop_y, prop_z), 42, (1, 0, 0)),
    ], ruled=True)
    output_flange = _cyl(46, 18, (prop_x - 9, prop_y, prop_z), (1, 0, 0))
    pilot = _cyl(22, 34, (prop_x - 4, prop_y, prop_z), (1, 0, 0))
    guibo_clearance = []
    for i in range(6):
        a = 2.0 * math.pi * i / 6
        guibo_clearance.append(_cyl(
            9.0,
            74,
            (prop_x - 37, prop_y + 42 * math.cos(a), prop_z + 42 * math.sin(a)),
            (1, 0, 0),
        ))

    # Shift tower and selector rod on the gearbox top, positioned between the
    # tunnel opening and the tail without touching the propshaft line.
    shift_tower = _cyl(22, 70, (1242, 0, 566), (0, 0, 1))
    shift_boot = _cyl(36, 28, (1242, 0, 632), (0, 0, 1))
    selector_rod = _cyl(8, 214, (1168, 0, 604), (1, 0, 0))

    # Rubber mount lands on the chassis crossmember and shares its hardpoint.
    mount_pad = _rbox(mount_x - 46, mount_y - 62, mount_z - 24, 92, 124, 18, 6)
    mount_boss = _cyl(18, 20, (mount_x - 10, mount_y, mount_z - 12), (1, 0, 0))

    gearbox = _U([
        bell,
        main_case,
        top_cover,
        tail,
        output_flange,
        pilot,
        shift_tower,
        shift_boot,
        selector_rod,
        mount_pad,
        mount_boss,
    ] + side_ribs)
    return gearbox.cut(_U(guibo_clearance))


def _shaft_with_splines(base_x: float, length: float, y: float, z: float, radius: float, name: str):
    shaft = _cyl(radius, length, (base_x, y, z), (1, 0, 0))
    splines = []
    for i in range(8):
        a = i * 45.0
        spline = _rbox(base_x + length - 54, y - 2.0, z + radius - 0.5, 48, 4, 4, 1)
        splines.append(spline.rotate((base_x, y, z), (base_x + 1, y, z), a))
    return _U([shaft] + splines), SHAFT_C, name


def _input_shaft():
    shaft, color, name = _shaft_with_splines(
        L.TRANS_FRONT_X - 28,
        172,
        MAIN_Y,
        MAIN_Z,
        15,
        "PRT_ManualGearbox_265_Input_Shaft",
    )
    pilot = _cyl(10, 34, (L.TRANS_FRONT_X - 58, MAIN_Y, MAIN_Z), (1, 0, 0))
    return shaft.fuse(pilot), color, name


def _layshaft():
    shaft, color, name = _shaft_with_splines(1082, 236, LAY_Y, LAY_Z, 13, "PRT_ManualGearbox_265_Layshaft")
    return shaft, color, name


def _output_shaft():
    shaft = C.tube_path([
        (1160, MAIN_Y, MAIN_Z),
        (1288, MAIN_Y, 438),
        L.PROPSHAFT_FRONT,
    ], 14)
    spline = _cyl(17, 46, (L.PROPSHAFT_FRONT[0] - 30, MAIN_Y, L.PROPSHAFT_FRONT[2]), (1, 0, 0))
    return shaft.fuse(spline), SHAFT_C, "PRT_ManualGearbox_265_Output_Shaft"


def _gear_pair(index: int, base_x: float, main_outer: float, lay_outer: float, main_teeth: int, lay_teeth: int):
    main = ME.spur_gear_x(main_outer - 6.0, main_outer, GEAR_WIDTH, base_x, MAIN_Y, MAIN_Z, main_teeth, bore_r=15)
    lay = ME.spur_gear_x(lay_outer - 5.5, lay_outer, GEAR_WIDTH, base_x, LAY_Y, LAY_Z, lay_teeth, bore_r=13, clocking_deg=180.0 / lay_teeth)
    thrust_washer_l = ME.washer(main_outer - 2, 17, 2, (base_x - 2.0, MAIN_Y, MAIN_Z), (1, 0, 0))
    thrust_washer_r = ME.washer(lay_outer - 2, 15, 2, (base_x + GEAR_WIDTH, LAY_Y, LAY_Z), (1, 0, 0))
    return _U([main, lay, thrust_washer_l, thrust_washer_r]), GEAR_C, f"PRT_ManualGearbox_265_Gear_Pair_{index}"


def _gear_pairs():
    dims = (
        (1, GEAR_XS[0], 50, 38, 34, 22),
        (2, GEAR_XS[1], 46, 42, 32, 26),
        (3, GEAR_XS[2], 42, 46, 30, 30),
        (4, GEAR_XS[3], 39, 49, 28, 34),
        (5, GEAR_XS[4], 36, 52, 24, 36),
    )
    return [_gear_pair(*item) for item in dims]


def _reverse_idler():
    idler_y = -37.0
    idler_z = 366.0
    gear = ME.spur_gear_x(28, 34, 18, 1104, idler_y, idler_z, 20, bore_r=8, clocking_deg=9)
    shaft = _cyl(8, 44, (1092, idler_y, idler_z), (1, 0, 0))
    fork_pad = _rbox(1110, idler_y - 22, idler_z + 30, 24, 44, 8, 2)
    return _U([gear, shaft, fork_pad]), GEAR_C, "PRT_ManualGearbox_265_Reverse_Idler_Gear"


def _synchro_hubs():
    hubs = []
    for base_x in (1140.0, 1218.0, 1296.0):
        hubs.append(ME.dog_clutch_ring_x(31, 17, 16, base_x, MAIN_Y, MAIN_Z, dogs=6))
    return _U(hubs), GEAR_C, "PRT_ManualGearbox_265_Synchro_Hubs"


def _selector_rails_forks():
    rails = [
        _cyl(5, 220, (1092, -34, 526), (1, 0, 0)),
        _cyl(5, 220, (1092, 0, 526), (1, 0, 0)),
        _cyl(5, 220, (1092, 34, 526), (1, 0, 0)),
    ]
    forks = []
    for x, y in ((1148, -34), (1226, 0), (1304, 34)):
        neck = C.swept_tube([(x, y, 526), (x, y * 0.35, 494), (x, 0, 476)], 5, cap=True)
        prongs = [
            _rbox(x - 5, -22, 455, 10, 8, 44, 2),
            _rbox(x - 5, 14, 455, 10, 8, 44, 2),
        ]
        forks.append(_U([neck] + prongs))
    detent_balls = [
        C.cyl(6, 4, (x, y, 534), (0, 0, 1))
        for x in (1122, 1190, 1260)
        for y in (-34, 0, 34)
    ]
    return _U(rails + forks + detent_balls), SELECTOR_C, "PRT_ManualGearbox_265_Selector_Rails_Forks"


def _bearing_set():
    bearings = [
        ME.radial_ball_bearing(25, 12, 12, (1088, MAIN_Y, MAIN_Z), (1, 0, 0), ball_count=10),
        ME.radial_ball_bearing(24, 11, 12, (1292, MAIN_Y, 438), (1, 0, 0), ball_count=10),
        ME.radial_ball_bearing(22, 10, 12, (1088, LAY_Y, LAY_Z), (1, 0, 0), ball_count=9),
        ME.radial_ball_bearing(22, 10, 12, (1298, LAY_Y, LAY_Z), (1, 0, 0), ball_count=9),
    ]
    return _U(bearings), BEARING_C, "PRT_ManualGearbox_265_Bearing_Set"


def parts():
    out = [(_manualgearbox_265(), COL, "PRT_ManualGearbox_265_Transmission")]
    out.extend([_input_shaft(), _layshaft(), _output_shaft()])
    out.extend(_gear_pairs())
    out.append(_reverse_idler())
    out.append(_synchro_hubs())
    out.append(_selector_rails_forks())
    out.append(_bearing_set())
    return out

