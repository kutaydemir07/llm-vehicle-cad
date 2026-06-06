"""ASM_3210_MacPherson_Corner_Hardparts - ModelA SportsCar front suspension.

Built like a real CAD corner sub-assembly and solved by its joints, not by hand
coordinates:

  * The strut cartridge (foot + damper + top mount) is mate-solved in a local
    +Z frame - each piece seats on the next one's tagged face - then the whole
    cartridge, plus the coil spring and lower perch, is dropped onto the real
    (leaning) strut axis with ``mating.place_along``.  Spring, perches and damper
    are therefore coaxial by construction.
  * The upright (knuckle) is located by a 3-joint solve (``seat_on_points``) from
    its lower ball-joint, strut clamp and tie-rod points, so it follows the
    hardpoints.  Its strut clamp is a BORED sleeve that slip-fits the strut tube,
    its ball-joint bore accepts the LCA stud, and its tie-rod bore accepts the
    steering stud - every neighbour meets it on a clearance bore, not a solid
    boss, so the designed joints touch without interpenetrating.
"""
from __future__ import annotations
import numpy as np
import cadquery as cq
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.core.reference import mating
from vehiclecad.geometry import machine_elements as ME

FRONT = SK.FRONT_SUSP
_cyl    = C.cyl
_rbox   = C.rbox
_U      = C.U
_mirror = C.mirror_y

DAMPER_C = (0.20, 0.21, 0.24)
PERCH_C  = (0.32, 0.33, 0.36)
MOUNT_C  = (0.16, 0.16, 0.18)
SPRING_C = C.SPRING

_TUBE_R  = 28.0     # strut damper tube radius
_BORE_R  = 30.0     # knuckle clamp / perch bore (slip-fit over the tube)


# ------------------------------------------------------------------------
#  MATE-SOLVED STRUT CARTRIDGE  (local +Z, then placed on the strut axis)
# ------------------------------------------------------------------------

def _strut_foot():
    """Machined lower spigot of the strut tube - the cartridge datum.  It is
    gripped by the knuckle clamp sleeve, so it stays a clean r28 spigot."""
    spigot = cq.Workplane("XY").cylinder(60, _TUBE_R).translate((0, 0, 30))  # z0..60
    spigot = spigot.faces("<Z").chamfer(3)
    mating.tag(spigot, top=">Z")
    return spigot


def _strut_damper():
    """Monotube damper body + piston rod as one turned part (axis = local Z)."""
    body = cq.Workplane("XY").cylinder(326, _TUBE_R).translate((0, 0, 163))   # z0..326
    rod  = cq.Workplane("XY").cylinder(236, 15).translate((0, 0, 444))        # z326..562
    d = body.union(rod).faces("<Z").chamfer(3)
    mating.tag(d, foot="<Z", rod_top=">Z")
    return d


def _strut_lower_perch(local_z: float):
    """Dished lower spring seat clamped on the damper tube.  Bore = _BORE_R so it
    slips over the r28 tube; welded well up the tube, above the knuckle/rotor."""
    saucer = _cyl(62, 12, (0, 0, local_z), (0, 0, 1)).cut(
        _cyl(_BORE_R, 16, (0, 0, local_z - 2), (0, 0, 1)))
    lip = _cyl(50, 12, (0, 0, local_z + 12), (0, 0, 1)).cut(
        _cyl(_BORE_R, 16, (0, 0, local_z + 10), (0, 0, 1)))
    return saucer.fuse(lip)


def _strut_top_mount():
    """Upper spring perch + rubber top mount + bearing plate + stud."""
    uperch = cq.Workplane("XY").cylinder(10, 68).translate((0, 0, -5))   # z -10..0
    plate  = cq.Workplane("XY").cylinder(16, 62).translate((0, 0, 8))    # z 0..16
    rubber = cq.Workplane("XY").cylinder(24, 48).translate((0, 0, 28))   # z 16..40
    stud   = cq.Workplane("XY").cylinder(24, 10).translate((0, 0, 52))   # z 40..64
    studs = [
        ME.threaded_stud_with_nut("M8", 28, (42 * np.cos(a), 42 * np.sin(a), 40), (0, 0, 1))
        for a in np.linspace(0, 2 * np.pi, 3, endpoint=False)
    ]
    m = uperch.union(plate).union(rubber).union(stud)
    for fastener in studs:
        m = m.union(fastener)
    mating.tag(m, base="<Z")
    return m


def _strut_assembly_placed():
    """Mate-solve the strut cartridge, drop in the coil spring, place on the axis."""
    colors = {"strut_foot": DAMPER_C, "strut_damper": DAMPER_C, "top_mount": MOUNT_C}
    wps = {"strut_foot": _strut_foot(), "strut_damper": _strut_damper(),
           "top_mount": _strut_top_mount()}
    mates = [("strut_foot+top", "strut_damper+foot"),     # damper seats on the foot
             ("strut_damper+rod_top", "top_mount+base")]   # top mount caps the rod
    try:
        assy = mating.build(wps, mates, grounded="strut_foot", colors=colors)
        flat = mating.to_flat(assy, colors)
    except Exception:
        flat = [(wps["strut_foot"].val(), DAMPER_C, "strut_foot")]

    # lower perch: concentric on the strut axis, seated at the skeleton's
    # spring-lower height (above the knuckle clamp and brake rotor envelope).
    axis_len = float(np.linalg.norm(np.array(FRONT["strut_upper_mount"]) - np.array(FRONT["strut_lower"])))
    lower_z = min(axis_len - 150.0, max(150.0, FRONT["spring_lower_perch"][2] - FRONT["strut_lower"][2]))
    flat.append((_strut_lower_perch(lower_z), PERCH_C, "lower_perch"))

    # one continuous coil, centred on the strut axis, resting ~2 mm proud of the
    # lower perch saucer and the top-mount under-perch (no sinking into them).
    zlo = max((s.BoundingBox().zmax for s, _, n in flat if n == "lower_perch"), default=lower_z + 24.0)
    ztop = min((s.BoundingBox().zmin for s, _, n in flat if n == "top_mount"), default=860.0)
    spring = C.coil_spring(zlo + 10.0, ztop - 10.0, coil_r=50.0, wire_r=7.5, active_turns=6.0)
    flat.append((spring, SPRING_C, "coil_spring"))
    return mating.place_along(flat, FRONT["strut_lower"], FRONT["strut_upper_mount"])


# ------------------------------------------------------------------------
#  LOWER CONTROL ARM  (forged A-arm)
# ------------------------------------------------------------------------

def _lca_left():
    """Forged lower A-arm.  Two arms from the body pivots converge on a ball-joint
    hub kept LOW (<= z248) under the knuckle, with only the slim ball stud rising
    into the upright.  A drop-link tab on the forward arm picks up the ARB."""
    fp = FRONT["lca_front_pivot"]      # (660, 320, 218)
    rp = FRONT["lca_rear_pivot"]       # (960, 320, 218)
    bj = FRONT["lca_outer_balljoint"]  # (810, 656, 248)
    arb = FRONT["arb_end_link"]         # (845, 380, 224)

    bjm = (bj[0], bj[1] - 8, bj[2] - 22)   # arm convergence, low and just inboard
    # forged arms; the last leg under the knuckle stays at z<=230 so the r16 tube
    # tops out below the upright's z248 underside.
    arm_f = C.swept_tube([fp, (745, 420, 224), (806, 616, 230), bjm], 16, cap=True)
    arm_r = C.swept_tube([rp, (900, 425, 226), (834, 616, 230), bjm], 18, cap=True)
    web   = C.swept_tube([(758, 392, 222), (892, 396, 226)], 12, cap=True)

    # bonded pivot bushings with steel sleeves, axis along X
    bush_f = ME.bonded_bushing(24, 8, 50, (fp[0] - 25, fp[1], fp[2]), (1, 0, 0))
    bush_r = ME.bonded_bushing(24, 8, 50, (rp[0] - 25, rp[1], rp[2]), (1, 0, 0))

    # ball-joint housing: cup holding the ball, its TOP face at z248 (coincident
    # with the knuckle underside); the r9.5 stud rises into the knuckle bore.
    housing = _cyl(24, 34, (bj[0], bj[1], bj[2] - 34), (0, 0, 1))   # z214..248
    stud    = _cyl(9.5, 32, (bj[0], bj[1], bj[2] - 4), (0, 0, 1))   # z244..276
    castle_nut = ME.hex_nut("M10", (bj[0], bj[1], bj[2] + 28), (0, 0, 1))
    ball_jt = _U([housing, stud, castle_nut])

    # ARB drop-link tab on the forward arm
    sway_tab = _rbox(arb[0] - 16, arb[1] - 14, arb[2] - 11, 32, 28, 22, 5)

    return _U([arm_f, arm_r, web, bush_f, bush_r, ball_jt, sway_tab])


# ------------------------------------------------------------------------
#  UPRIGHT / HUB CARRIER  (located by a 3-joint solve)
# ------------------------------------------------------------------------

def _knuckle_solved():
    """Front upright located by ``seat_on_points`` from its lower ball-joint,
    strut clamp and tie-rod points.  Modelled in a canonical local frame (origin
    = wheel centre, +Z = outboard bearing axis); every joint is a clearance bore
    so the strut tube, LCA stud and tie-rod stud insert without interference."""
    wc = FRONT["wheel_centre"]               # (810, 706, 300)
    bj = FRONT["lca_outer_balljoint"]         # (810, 656, 248)
    sl = FRONT["strut_lower"]                 # (810, 620, 286)
    su = FRONT["strut_upper_mount"]           # (810, 530, 952)
    tr = FRONT["tie_rod_outer"]               # (720, 632, 330)

    def M(p):                                 # world -> canonical (world +Y bearing -> +Z)
        return (p[0] - wc[0], -(p[2] - wc[2]), p[1] - wc[1])
    cb, cs, ct, csu = M(bj), M(sl), M(tr), M(su)
    sd = np.array(csu, float) - np.array(cs, float)
    sd = sd / float(np.linalg.norm(sd))       # local strut-axis direction

    bearing  = _cyl(60, 78, (0, 0, -22), (0, 0, 1))           # wheel bearing (axis +Z);
    #            inboard face pulled outboard (local z-22 -> world y684) so it
    #            clears the LCA ball-joint housing just below it
    hub_face = _cyl(72, 12, (0, 0, 40), (0, 0, 1))            # outboard flange
    body     = _rbox(-24, -30, -92, 48, 82, 112, 10)          # casting spanning the joints
    clamp    = _cyl(40, 84, tuple(np.array(cs) + sd * 2.0), tuple(sd))   # strut clamp sleeve
    steer    = C.swept_tube([(-18, -22, -72), (-54, -28, -74),
                             (ct[0], ct[1], ct[2])], 13, cap=True)        # steering arm
    knuckle  = _U([bearing, hub_face, body, clamp, steer])

    # clearance bores for the mating studs/tube:
    knuckle = knuckle.cut(_cyl(_BORE_R, 200, tuple(np.array(cs) + sd * -40.0), tuple(sd)))  # strut tube
    knuckle = knuckle.cut(_cyl(11, 70, (cb[0], cb[1] + 34, cb[2]), (0, -1, 0)))             # LCA stud
    knuckle = knuckle.cut(_cyl(8, 70, (ct[0], ct[1], ct[2] + 34), (0, 0, -1)))              # tie-rod stud

    return mating.seat_on_points([(knuckle, C.ARM, "PRT_Hub_Knuckle")],
                                 [cb, cs, ct], [bj, sl, tr])


def parts():
    out = []
    # mate-solved strut cartridge (foot + damper + perch + top mount + spring)
    for solid, color, name in _strut_assembly_placed():
        out.append((solid, color, f"PRT_{name}_FL"))
        out.append((_mirror(solid), color, f"PRT_{name}_FR"))
    # lower control arm (located at its pivots and ball joint)
    lca = _lca_left()
    out.append((lca, C.ARM, "PRT_LCA_FL"))
    out.append((_mirror(lca), C.ARM, "PRT_LCA_FR"))
    # upright located by its 3-joint kinematic solve (ties strut <-> LCA <-> steering)
    for solid, color, name in _knuckle_solved():
        out.append((solid, color, f"{name}_FL"))
        out.append((_mirror(solid), color, f"{name}_FR"))
    return out
