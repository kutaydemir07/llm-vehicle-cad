"""ASM_3310_Semi_Trailing_Arm_Corner_Hardparts - ModelA SportsCar rear suspension.

Drawn the way the real car is built (and the way you would lay it up in a CAD
assembly): a cast semi-trailing arm pivots on the subframe through two large
bushings and carries the rear hub at its outboard end.  The coil spring and the
telescopic damper are SEPARATE units sitting at different stations on the arm -
NOT a coilover.  A fat, fairly upright coil sits forward in a body spring pocket;
a near-vertical damper sits rearward next to the hub and rises to the body rear
shock tower.  ~140 mm of fore/aft spacing between the two axes guarantees the
spring OD and the shock tube never share space.

Mating philosophy (so nothing floats or interpenetrates):
  * Each cartridge is built straight up a LOCAL +Z axis and dropped onto its real
    (leaning) hardpoint axis with ``mating.place_along`` - the spring is centred
    in its perches and the shock body is centred in its eyes by construction.
  * The coil's lower perch seats flush on the arm's spring pad (coincident face).
  * The damper's lower eye drops into the arm's clevis and shares the pin bore -
    a designed pin joint that touches without gross interference.
  * The hub carrier's inboard face is coincident with the arm's hub boss face,
    and the half-shaft stub passes through a clearance bore in that boss.
"""
from __future__ import annotations
import math
import cadquery as cq
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.core.reference import mating
from vehiclecad.geometry import machine_elements as ME

REAR = SK.REAR_SUSP
_cyl    = C.cyl
_rbox   = C.rbox
_U      = C.U
_mirror = C.mirror_y

DAMPER_C = (0.20, 0.21, 0.24)
PERCH_C  = (0.32, 0.33, 0.36)
SPRING_C = C.SPRING
MOUNT_C  = (0.16, 0.16, 0.18)


# ------------------------------------------------------------------------
#  TRAILING ARM  -  cast carrier that owns the spring pad, damper clevis,
#  ARB tab and hub boss so every neighbour seats onto a real feature.
# ------------------------------------------------------------------------

def _trailing_arm_left():
    ip  = REAR["sta_inner_pivot"]   # (2950, 280, 310) inner-front pivot
    op  = REAR["sta_outer_pivot"]   # (2950, 520, 310) inner-rear pivot
    hub = REAR["hub_centre"]         # (3372, 716.5, 300)
    sp  = REAR["spring_lower"]        # (3250, 540, 360)
    dm  = REAR["damper_lower"]        # (3392, 566, 332)
    arb = REAR["arb_end_link"]        # (3322, 600, 300)

    # hub boss centre sits inboard of the bearing; the spars die into it.
    boss_face = hub[1] - 20.0        # 696.5 - coincident with hub carrier face
    boss = (hub[0], hub[1] - 50.0, hub[2])

    # two heavy cast spars from the pivot bushings converging on the hub boss.
    # The forward spar stays low (z<=326) under the spring pad so its r30 tube
    # tops out below the lower perch.
    spar_f = C.swept_tube([ip, (3080, 360, 318), (3212, 468, 324),
                           (3318, 590, 312), boss], 30, cap=True)
    spar_r = C.swept_tube([op, (3072, 548, 320), (3205, 580, 330),
                           (3300, 645, 312), boss], 27, cap=True)
    web    = C.swept_tube([(3185, 472, 332), (3212, 566, 332)], 14, cap=True)

    # sleeved bonded rubber pivot bushings, axis along Y
    bush_i = ME.bonded_bushing(32, 10, 56, (ip[0] - 12, ip[1] - 28, ip[2]), (0, 1, 0))
    bush_o = ME.bonded_bushing(32, 10, 56, (op[0] - 12, op[1] - 28, op[2]), (0, 1, 0))

    # hub boss: short tube along Y, bored so the hub's seal collar clears; its
    # outboard face (boss_face) is where the hub carrier seats.
    hub_boss = _cyl(46, boss_face - (hub[1] - 80.0), (hub[0], hub[1] - 80.0, hub[2]), (0, 1, 0))
    hub_boss = hub_boss.cut(_cyl(26, 90, (hub[0], hub[1] - 90.0, hub[2]), (0, 1, 0)))

    # spring pad: low boss whose top sits just under the spring_lower seat so the
    # lower perch (which leans a couple of degrees on the spring axis) bolts down
    # onto it without its tilted underside biting into the pad.
    spring_pad = _cyl(56, 22, (sp[0], sp[1], sp[2] - 27), (0, 0, 1))

    # damper clevis: two ears straddling the lower eye in Y with a pin through.
    # Generous gap (30) absorbs the shock's slight lean so the eye never touches
    # the ears; the pin shares the eye bore so the joint reads pinned, not fused.
    ear_t, gap, ear_dx, ear_dz = 9.0, 30.0, 32.0, 44.0
    ear_z0 = dm[2] - ear_dz / 2.0 - 4.0
    ear_l = _rbox(dm[0] - ear_dx / 2, dm[1] + gap / 2,        ear_z0, ear_dx, ear_t, ear_dz, 6)
    ear_r = _rbox(dm[0] - ear_dx / 2, dm[1] - gap / 2 - ear_t, ear_z0, ear_dx, ear_t, ear_dz, 6)
    brkt  = C.swept_tube([(3300, 612, 316), (dm[0], dm[1], dm[2] - 36)], 13, cap=True)
    pin   = ME.clevis_pin(6.5, gap + 2 * ear_t + 4, (dm[0], dm[1] - gap / 2 - ear_t - 2, dm[2]), (0, 1, 0))

    # ARB drop-link tab on a short post off the hub boss (near the hub, rearward
    # and outboard of the spring/damper)
    arb_tab  = _rbox(arb[0] - 16, arb[1] - 16, arb[2] - 11, 32, 32, 22, 5)
    arb_post = C.swept_tube([(3358, 652, 308), (arb[0], arb[1], arb[2])], 11, cap=True)

    return _U([spar_f, spar_r, web, bush_i, bush_o, hub_boss, spring_pad,
               ear_l, ear_r, brkt, pin, arb_tab, arb_post])


def _rear_hub_left():
    """Rear hub carrier: wheel-bearing housing + outboard wheel flange + inboard
    half-shaft stub.  Its inboard face is coincident with the arm's hub boss."""
    hub = REAR["hub_centre"]          # (3372, 716.5, 300)
    seat_y = hub[1] - 20.0            # 696.5 - meets the arm boss face
    housing = _cyl(58, 64, (hub[0], seat_y, hub[2]),        (0, 1, 0))   # bearing housing
    flange  = _cyl(72, 14, (hub[0], seat_y + 58, hub[2]),   (0, 1, 0))   # wheel mount face
    # inboard bearing-seal collar - stays inside the arm boss bore (no protrusion
    # onto the hub axis where the cast spars converge), so arm and hub only share
    # the seat plane.
    collar  = _cyl(18, 6, (hub[0], seat_y - 6, hub[2]),     (0, 1, 0))
    bearing = ME.radial_ball_bearing(43, 20, 22, (hub[0], seat_y + 22, hub[2]), (0, 1, 0), ball_count=12)
    return _U([housing, flange, collar, bearing])


# ------------------------------------------------------------------------
#  SEPARATE COIL SPRING  (forward, fat, fairly upright)
# ------------------------------------------------------------------------

def _spring_lower_cup(z0: float):
    """Dished lower seat with a central locator inside the coil ID."""
    saucer = _cyl(70, 10, (0, 0, z0),       (0, 0, 1))
    boss   = _cyl(22, 30, (0, 0, z0 + 10),  (0, 0, 1))
    return _U([saucer, boss])


def _spring_upper_cup(z1: float):
    """Body-side upper seat, mirror of the lower cup (locator hangs into the ID)."""
    saucer = _cyl(70, 10, (0, 0, z1 - 10),  (0, 0, 1))
    boss   = _cyl(22, 30, (0, 0, z1 - 40),  (0, 0, 1))
    return _U([saucer, boss])


def _spring_stack_placed():
    lo = REAR["spring_lower"]; up = REAR["spring_upper"]
    L = math.dist(lo, up)
    lower = _spring_lower_cup(0.0)
    upper = _spring_upper_cup(L)
    # the ground end coils rest ~1 mm proud of each saucer (wire_r below the helix
    # start), so the coil touches its perches without sinking into them.
    coil  = C.coil_spring(22.0, L - 22.0, coil_r=60.0, wire_r=11.0, active_turns=5.0)
    flat = [(lower, PERCH_C,  "r_spring_lower_perch"),
            (coil,  SPRING_C, "r_coil_spring"),
            (upper, PERCH_C,  "r_spring_upper_perch")]
    return mating.place_along(flat, lo, up)


# ------------------------------------------------------------------------
#  SEPARATE TELESCOPIC DAMPER  (rearward, near-vertical)
# ------------------------------------------------------------------------

def _damper_lower_eye():
    """Bushed lower eye, centred on the local origin so it pivots about the
    lower hardpoint and drops into the arm's clevis."""
    eye = cq.Workplane("XY").box(32, 18, 40).edges("|Y").fillet(9)
    eye = eye.faces(">Y").workplane().hole(16)     # transverse bore for the pin
    return eye.val()


def _damper_body(z0: float, z1: float):
    """Shock body (lower, fat) + chromed piston rod + dust boot, axis = local Z."""
    span = z1 - z0
    body_len = span * 0.60
    body = _cyl(24, body_len, (0, 0, z0),            (0, 0, 1))
    rod  = _cyl(13, span - body_len, (0, 0, z0 + body_len), (0, 0, 1))
    boot = _cyl(20, span * 0.30, (0, 0, z0 + body_len - 6), (0, 0, 1))
    return _U([body, rod, boot])


def _damper_upper_mount(z: float):
    """Body-side shock mount: cup + rubber bush + bearing plate + stud."""
    cup    = _cyl(40, 12, (0, 0, z - 12), (0, 0, 1))
    rubber = _cyl(30, 22, (0, 0, z - 2),  (0, 0, 1))
    plate  = _cyl(44, 8,  (0, 0, z + 20), (0, 0, 1))
    stud   = ME.threaded_stud_with_nut("M8", 26, (0, 0, z + 28), (0, 0, 1))
    return _U([cup, rubber, plate, stud])


def _damper_stack_placed():
    lo = REAR["damper_lower"]; up = REAR["damper_upper"]
    L = math.dist(lo, up)
    z_mount = L - 30.0
    eye   = _damper_lower_eye()
    body  = _damper_body(22.0, z_mount - 14.0)   # rod tip stops just under the mount cup
    mount = _damper_upper_mount(z_mount)
    flat = [(eye,   DAMPER_C, "r_damper_lower_eye"),
            (body,  DAMPER_C, "r_damper"),
            (mount, MOUNT_C,  "r_damper_upper_eye")]
    return mating.place_along(flat, lo, up)


def parts():
    out = []
    # cast trailing arm + hub carrier (seated on the arm's hub boss)
    for fn, name in ((_trailing_arm_left, "PRT_Trailing_Arm"),
                     (_rear_hub_left,     "PRT_Rear_Hub")):
        left = fn()
        out.append((left, C.ARM, f"{name}_RL"))
        out.append((_mirror(left), C.ARM, f"{name}_RR"))
    # separate coil-spring stack and separate damper stack, each centred on its
    # own hardpoint axis (the 6 named parts are unchanged from the old layout).
    for solid, color, name in _damper_stack_placed() + _spring_stack_placed():
        out.append((solid, color, f"PRT_{name}_RL"))
        out.append((_mirror(solid), color, f"PRT_{name}_RR"))
    return out
