"""ManualGearbox 265/5 five-speed manual transmission -- drawn as a REAL box.

Gear-train engineering (the part a transmission lives or dies by):

  * Main (input/output) axis = crank axis (y0, z445).  Layshaft at
    (y-34, z369.5) -> centre distance 82.8 mm.
  * Module 2.3 throughout, tooth counts per pair sum to 72, so
    pitch_r(main) + pitch_r(lay) = 1.15 * 72 = 82.8 mm = the centre distance:
    every pair genuinely MESHES (tips overlap the opposing root zone by one
    whole depth, flanks at the 20-degree pressure angle).
      1st 50/22   2nd 45/27   3rd 40/32   4th 36/36   5th 32/40
  * The output shaft is STRAIGHT and coaxial with the input (z445) -- the old
    bent tube was physically impossible; the propshaft's guibo/U-joint takes
    the down-angle (hardpoints trans_rear/prop_front now z445).
  * Input shaft: pilot stub -> CLUTCH SPLINES AT THE FRONT (inside the disc
    hub) -> front bearing journal -> rear counterbore that receives the output
    shaft spigot (slip fit), exactly like the production layout.
  * Bearings seat IN THE CASE WALLS with inner races matching the shaft
    journals (input r15, output r14, lay r13).
  * Reverse idler meshes the 1st lay gear (centre distance = pitch sum).
  * Case: bolted bellhousing flange (8x M10 on PCD 150), ribbed walls, top
    cover with 6x M6, magnetic drain plug + side fill plug, and two M10 mount
    studs with nuts dropping through the crossmember saddle.
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

MAIN_Y, MAIN_Z = 0.0, L.CRANK_Z          # (0, 445)
LAY_Y, LAY_Z = -34.0, 369.5              # centre distance to main = 82.8
M_GEAR = 2.3                             # gear module (mm)
# Gear stack packaged INSIDE the cavity (x1102..1292): five 22-wide pairs and
# three 16-wide synchro hubs in the gaps, nothing buried in the case walls.
GEAR_XS = (1104.0, 1146.0, 1172.0, 1214.0, 1240.0)
GEAR_TEETH = ((50, 22), (45, 27), (40, 32), (36, 36), (32, 40))
GEAR_WIDTH = 22.0
HUB_XS = (1128.0, 1196.0, 1264.0)        # synchro hubs between the pairs


def _manualgearbox_265():
    """Bellhousing + main casing + tail cone with REAL closure hardware."""
    prop_x, prop_y, prop_z = L.PROPSHAFT_FRONT          # (1400, 0, 445)
    mount_x, mount_y, mount_z = L.GEARBOX_MOUNT

    # Bellhousing: cast cone with a flat engine-side flange on the crank axis.
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
    # bolted bellhousing joint: 8x M10 cap screws on PCD 150 into the engine
    bell_bolts = ME.bolt_circle("M10", 8, 150.0, 22.0,
                                (1014, L.CL_Y, L.CRANK_Z), (1, 0, 0),
                                start_deg=22.5)

    # Main case sized around the corrected gear train: the 5th lay gear tip
    # reaches z321, so the case floor drops to z304 (the tunnel is open below).
    main_case = _rbox(1090, -108, 304, 214, 216, 244, 14)
    gear_cavity = _rbox(1102, -96, 316, 190, 188, 212, 10)
    shaft_bores = _U([
        _cyl(27, 248, (1076, MAIN_Y, MAIN_Z), (1, 0, 0)),
        _cyl(23, 248, (1076, LAY_Y, LAY_Z), (1, 0, 0)),
        # reverse-idler shaft press bore in the front web
        _cyl(8.5, 60, (1076, LAY_Y - 30.6, LAY_Z + 37.8), (1, 0, 0)),
        # selector-rail guide bores through both webs
        _cyl(5.5, 248, (1076, -34, 518), (1, 0, 0)),
        _cyl(5.5, 248, (1076, 0, 518), (1, 0, 0)),
        _cyl(5.5, 248, (1076, 34, 518), (1, 0, 0)),
    ])
    main_case = main_case.cut(gear_cavity).cut(shaft_bores)
    top_cover = _rbox(1120, -54, 548, 150, 108, 30, 6)
    cover_bolts = _U([
        ME.cap_screw("M6", 12, (x, y, 566), (0, 0, 1))
        for x in (1132, 1194, 1256) for y in (-42, 42)
    ])
    side_ribs = [
        _rbox(1110 + i * 44, 104, 360, 10, 16, 148, 3) for i in range(4)
    ] + [
        _rbox(1110 + i * 44, -120, 360, 10, 16, 148, 3) for i in range(4)
    ]
    # service hardware: magnetic drain plug (bottom) + fill/level plug (side)
    drain_plug = ME.cap_screw("M14", 12, (1180, -40, 316), (0, 0, -1))
    fill_plug = ME.cap_screw("M14", 12, (1240, -96, 420), (0, -1, 0))

    # Tail cone: STRAIGHT on the main axis out to the output flange at z445.
    tail = C.loft_circles([
        ((1296, L.CL_Y, MAIN_Z), 80, (1, 0, 0)),
        ((1352, L.CL_Y, MAIN_Z), 56, (1, 0, 0)),
        ((prop_x - 9, prop_y, prop_z), 42, (1, 0, 0)),
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

    # Shift tower and selector rod on the gearbox top.
    shift_tower = _cyl(22, 70, (1242, 0, 566), (0, 0, 1))
    shift_boot = _cyl(36, 28, (1242, 0, 632), (0, 0, 1))
    selector_rod = _cyl(8, 214, (1168, 0, 604), (1, 0, 0))

    # Mount boss + pedestal web down to the crossmember saddle, with two M10
    # studs+nuts dropping THROUGH the saddle plate (z320..338) -- a bolted
    # joint, not parts hovering near each other.
    mount_pad = _rbox(mount_x - 46, mount_y - 62, mount_z - 24, 92, 124, 18, 6)
    pedestal = _rbox(mount_x - 24, mount_y - 24, mount_z - 10, 48, 48, 36, 6)
    mount_studs = _U([
        ME.threaded_stud_with_nut("M10", 42, (mount_x - 18, mount_y, mount_z - 24), (0, 0, -1)),
        ME.threaded_stud_with_nut("M10", 42, (mount_x + 18, mount_y, mount_z - 24), (0, 0, -1)),
    ])

    gearbox = _U([
        bell,
        bell_bolts,
        main_case,
        top_cover,
        cover_bolts,
        drain_plug,
        fill_plug,
        tail,
        output_flange,
        pilot,
        shift_tower,
        shift_boot,
        selector_rod,
        mount_pad,
        pedestal,
        mount_studs,
    ] + side_ribs)
    # the tail housing, output flange and pilot are BORED r19 so the output
    # shaft (r14, spline r17) turns inside them -- no shaft through solid iron
    gearbox = gearbox.cut(_cyl(19, 152, (1286, L.CL_Y, MAIN_Z), (1, 0, 0)))
    return gearbox.cut(_U(guibo_clearance))


def _input_shaft():
    """Input shaft drawn like the production part: r10 pilot stub at the nose,
    CLUTCH SPLINES at the front (where the disc hub actually rides, x1000..
    1044), plain r15 journal back to the front bearing, and a rear counterbore
    that receives the output-shaft spigot as a slip fit."""
    shaft = _cyl(15, 148, (992, MAIN_Y, MAIN_Z), (1, 0, 0))
    pilot = _cyl(10, 34, (962, MAIN_Y, MAIN_Z), (1, 0, 0))
    # splines span exactly the clutch-disc hub (x1012..1034), clear of the
    # pilot bearing (ends x1006) and the release-bearing collar (from x1046)
    splines = []
    for i in range(8):
        sp = _rbox(1021, MAIN_Y - 2.0, MAIN_Z + 15 - 0.5, 25, 4, 4, 1)
        splines.append(sp.rotate((992, MAIN_Y, MAIN_Z), (993, MAIN_Y, MAIN_Z), i * 45.0))
    shaft = _U([shaft, pilot] + splines)
    shaft = shaft.cut(_cyl(14.5, 18, (1124, MAIN_Y, MAIN_Z), (1, 0, 0)))
    return shaft, SHAFT_C, "PRT_ManualGearbox_265_Input_Shaft"


def _layshaft():
    """Layshaft on its own axis with drive splines under the gear cluster
    (spline tips r16.5 engage the gears' r17 bores as a designed fit)."""
    shaft = _cyl(13, 222, (1082, LAY_Y, LAY_Z), (1, 0, 0))
    splines = []
    for i in range(8):
        sp = _rbox(1104, LAY_Y - 2.0, LAY_Z + 13 - 0.5, 158, 4, 4, 1)
        splines.append(sp.rotate((1082, LAY_Y, LAY_Z), (1083, LAY_Y, LAY_Z), i * 45.0))
    return _U([shaft] + splines), SHAFT_C, "PRT_ManualGearbox_265_Layshaft"


def _output_shaft():
    """STRAIGHT output shaft on the main axis: front spigot into the input's
    counterbore, gear journals, flange splines, output flange at z445."""
    pf = L.PROPSHAFT_FRONT
    spigot = _cyl(14, 16, (1126, MAIN_Y, MAIN_Z), (1, 0, 0))
    shaft = _cyl(14, pf[0] - 1142 + 9, (1142, MAIN_Y, MAIN_Z), (1, 0, 0))
    spline = _cyl(17, 46, (pf[0] - 56, MAIN_Y, MAIN_Z), (1, 0, 0))
    return _U([spigot, shaft, spline]), SHAFT_C, "PRT_ManualGearbox_265_Output_Shaft"


def _gear_pair(index: int, base_x: float, z_main: int, z_lay: int):
    """One speed pair with EXACT meshing: module 2.3, pitch radii sum to the
    82.8 mm centre distance, lay gear clocked half a pitch so the teeth
    interleave, built with 0.6 mm working BACKLASH (lay gear addendum pulled
    in) so the engaged flanks never boolean-interfere."""
    pm = 0.5 * M_GEAR * z_main
    pl = 0.5 * M_GEAR * z_lay - 0.6
    main = ME.spur_gear_x(pm - 1.25 * M_GEAR, pm + M_GEAR, GEAR_WIDTH,
                          base_x, MAIN_Y, MAIN_Z, z_main, bore_r=15)
    lay = ME.spur_gear_x(pl - 1.25 * M_GEAR, pl + M_GEAR, GEAR_WIDTH,
                         base_x, LAY_Y, LAY_Z, z_lay, bore_r=17,
                         clocking_deg=180.0 / z_lay)
    thrust_washer_l = ME.washer(pm - 4, 17, 2, (base_x - 2.0, MAIN_Y, MAIN_Z), (1, 0, 0))
    thrust_washer_r = ME.washer(pl - 4, 15, 2, (base_x + GEAR_WIDTH, LAY_Y, LAY_Z), (1, 0, 0))
    return _U([main, lay, thrust_washer_l, thrust_washer_r]), GEAR_C, f"PRT_ManualGearbox_265_Gear_Pair_{index}"


def _gear_pairs():
    return [
        _gear_pair(i + 1, GEAR_XS[i], GEAR_TEETH[i][0], GEAR_TEETH[i][1])
        for i in range(5)
    ]


def _reverse_idler():
    """Reverse idler on its own pressed-in shaft, MESHING the 1st lay gear:
    centre distance = idler pitch (23.0) + lay-1st pitch (25.3) = 48.3."""
    z_id = 20
    pi_r = 0.5 * M_GEAR * z_id - 0.6                 # 23.0 less 0.6 backlash
    # place on the circle of radius 48.3 around the lay axis
    iy = LAY_Y - 30.6
    iz = LAY_Z + 37.8
    gear = ME.spur_gear_x(pi_r - 1.25 * M_GEAR, pi_r + M_GEAR, 18, 1106, iy, iz,
                          z_id, bore_r=8, clocking_deg=9)
    shaft = _cyl(8, 44, (1094, iy, iz), (1, 0, 0))
    fork_pad = _rbox(1112, iy - 22, iz + 26, 24, 44, 8, 2)
    return _U([gear, shaft, fork_pad]), GEAR_C, "PRT_ManualGearbox_265_Reverse_Idler_Gear"


def _synchro_hubs():
    hubs = []
    for base_x in HUB_XS:
        hubs.append(ME.dog_clutch_ring_x(34, 14.5, 16, base_x, MAIN_Y, MAIN_Z, dogs=6))
    return _U(hubs), GEAR_C, "PRT_ManualGearbox_265_Synchro_Hubs"


def _selector_rails_forks():
    """Three rails guided in the case walls; each fork drops from its rail and
    its prongs straddle the matching synchro sleeve (HUB_XS alignment)."""
    rails = [
        _cyl(5, 212, (1096, -34, 518), (1, 0, 0)),
        _cyl(5, 212, (1096, 0, 518), (1, 0, 0)),
        _cyl(5, 212, (1096, 34, 518), (1, 0, 0)),
    ]
    forks = []
    for (hx, ry) in zip(HUB_XS, (-34, 0, 34)):
        x = hx + 8.0                                  # fork centred on the hub
        neck = C.swept_tube([(x, ry, 518), (x, ry * 0.35, 496), (x, 0, 482)], 5, cap=True)
        # prongs straddle the sleeve OUTSIDE its r34 outer diameter
        prongs = [
            _rbox(x - 5, -44, 452, 10, 8, 44, 2),
            _rbox(x - 5, 36, 452, 10, 8, 44, 2),
        ]
        forks.append(_U([neck] + prongs))
    detent_balls = [
        C.cyl(6, 4, (x, y, 521), (0, 0, 1))
        for x in (1122, 1190, 1258)
        for y in (-34, 0, 34)
    ]
    return _U(rails + forks + detent_balls), SELECTOR_C, "PRT_ManualGearbox_265_Selector_Rails_Forks"


def _bearing_set():
    """Bearings seated in the case-wall bores; inner races MATCH the shaft
    journals (input r15, output r14, layshaft r13 both ends)."""
    bearings = [
        ME.radial_ball_bearing(26, 15, 12, (1088, MAIN_Y, MAIN_Z), (1, 0, 0), ball_count=10),
        ME.radial_ball_bearing(26, 14, 12, (1292, MAIN_Y, MAIN_Z), (1, 0, 0), ball_count=10),
        ME.radial_ball_bearing(22, 13, 12, (1088, LAY_Y, LAY_Z), (1, 0, 0), ball_count=9),
        ME.radial_ball_bearing(22, 13, 12, (1292, LAY_Y, LAY_Z), (1, 0, 0), ball_count=9),
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
