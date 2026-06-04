"""ManualGearbox 265/5 five-speed manual transmission  -  packaging geometry.

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
"""
from __future__ import annotations
import math
from vehiclecad.core.reference import common as C
from vehiclecad.parts.powertrain.detail import layout as L

_box  = C.box
_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.TRANS


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


def parts():
    out = []
    out.append((_manualgearbox_265(), COL, "PRT_ManualGearbox_265_Transmission"))
    return out

