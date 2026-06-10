"""Wheel corner subassembly (built once in a local frame, mirrored + placed x4).

Local frame: wheel axis = Y, hub centre at origin, OUTBOARD = +Y.  Everything is
modelled as real solids so the STEP carries genuine wheel geometry:

  tire      revolved 205/55 section: bead, bulged sidewall, crowned tread, with
            cut circumferential grooves + lateral tread blocks + sidewall step
  rim       deep-dish cross-spoke alloy: inner barrel, dished spoke face with
            shaped windows (see-through to the brake), polished outer lip,
            raised hub, 5 lug bolts on a 5x120 PCD (the SportsCar's signature), and a
            roundel centre cap
  brake     is mate-seated to the wheel bearing hub: rotor on the inboard flange
            face, caliper straddling the disc with a real slot, and the wheel
            face/cap/lugs stacked outboard without hidden volume clashes.

Built once for the LEFT side and cached; the RIGHT side is the mirror image.
"""
from __future__ import annotations
import numpy as np
import cadquery as cq
from cadquery import Solid, Compound, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import mating
from vehiclecad.geometry import machine_elements as ME

# ---- local dimensions ----
R_TIRE = C.TIRE_R           # 300 (tread outer)
RIM_R  = 190.0              # bead-seat radius (15")
LIP_R  = 198.0              # outer polished lip
FACE_Y = 34.0              # outboard spoke-face plane (deep dish)
LIP_Y  = 94.0              # outer lip plane
N_SPOKE = 10

# ---- local colours ----
ALLOY  = (0.60, 0.61, 0.64)
POLISH = (0.82, 0.84, 0.87)
BARREL = (0.28, 0.29, 0.32)
DISC   = (0.42, 0.43, 0.46)
HAT    = (0.20, 0.21, 0.23)
LUG    = (0.74, 0.75, 0.78)
ROUND_BLUE = (0.10, 0.22, 0.55)

_BUILD = None


def _compound(solids):
    return Compound.makeCompound(solids)


def _window(r_in, r_out, half_in, half_out, y0, y1, n=7):
    pts = [(r_in * np.sin(t), r_in * np.cos(t)) for t in np.linspace(-half_in, half_in, n)]
    pts += [(r_out * np.sin(t), r_out * np.cos(t)) for t in np.linspace(half_out, -half_out, n)]
    return C.xz_prism(pts, y0, y1)


def _tire():
    # closed section profile (radial r, axial a) revolved about Y
    # Inner bead diameter is kept just outside the rim lip/barrel OD.  The old
    # section buried the alloy inside the rubber; this behaves like a CAD tire
    # seated against the rim bead, not intersecting it.
    pts = [(206, -86), (244, -104), (290, -94), (300, -80),
           (300, 80), (290, 94), (244, 104), (206, 86)]
    tire = (cq.Workplane("XY").polyline(pts).close()
            .revolve(360, (0, 0, 0), (0, 1, 0)).val())
    # circumferential grooves
    grooves = [C.cyl(303, 13, (0, a - 6.5, 0), (0, 1, 0)).cut(C.cyl(287, 26, (0, a - 13, 0), (0, 1, 0)))
               for a in (-58, -20, 20, 58)]
    tire = tire.cut(_compound(grooves))
    # lateral tread blocks across the crown
    blocks = []
    for k in range(40):
        b = C.box(-6, -78, 286, 12, 156, 22).rotate((0, 0, 0), (0, 1, 0), k * 9.0)
        blocks.append(b)
    tire = tire.cut(_compound(blocks))
    # shallow sidewall step (lettering band) both sides
    step = (C.cyl(238, 6, (0, -106, 0), (0, 1, 0)).cut(C.cyl(214, 12, (0, -109, 0), (0, 1, 0))))
    step2 = C.mirror_y(step)
    tire = tire.cut(_compound([step, step2]))
    return tire


def _rim():
    parts = []
    # inner barrel with a REAL drop-centre well profile (revolved varying
    # radius: bead seats at r186, well dipping to r170) -- dark alloy
    prof = ((-92, 186.0), (-62, 186.0), (-46, 171.0), (4, 171.0),
            (18, 186.0), (FACE_Y, 186.0))
    outer = C.loft_circles([((0, y, 0), r, (0, 1, 0)) for y, r in prof])
    inner = C.loft_circles([((0, y, 0), r - 8.0, (0, 1, 0)) for y, r in prof])
    barrel = outer.cut(inner)
    inb_flange = C.cyl(193, 12, (0, -94, 0), (0, 1, 0)).cut(C.cyl(184, 16, (0, -96, 0), (0, 1, 0)))
    parts.append((barrel.fuse(inb_flange), BARREL, "rim_barrel"))

    # dished spoke face: disc minus shaped windows -> hub + N spokes + outer ring
    disc = C.cyl(184, 22, (0, FACE_Y, 0), (0, 1, 0))
    win = []
    hw_in, hw_out = np.radians(14.6), np.radians(15.2)
    for k in range(N_SPOKE):
        w = _window(60, 163, hw_in, hw_out, FACE_Y - 6, FACE_Y + 30)
        win.append(w.rotate((0, 0, 0), (0, 1, 0), k * 360.0 / N_SPOKE))
    face = disc.cut(_compound(win))
    parts.append((face, ALLOY, "rim_face"))

    # polished deep-dish outer lip
    lip = C.cyl(LIP_R, LIP_Y - FACE_Y, (0, FACE_Y, 0), (0, 1, 0)).cut(
        C.cyl(184, LIP_Y - FACE_Y + 12, (0, FACE_Y - 6, 0), (0, 1, 0)))
    outer_bead = C.cyl(LIP_R, 12, (0, LIP_Y - 12, 0), (0, 1, 0)).cut(
        C.cyl(188, 16, (0, LIP_Y - 14, 0), (0, 1, 0)))
    parts.append((lip.fuse(outer_bead), POLISH, "rim_lip"))

    # raised hub
    hub = C.cyl(66, 18, (0, FACE_Y + 22, 0), (0, 1, 0))
    hub = hub.cut(_compound([C.cyl(9, 30, (58 * np.cos(a), FACE_Y + 18, 58 * np.sin(a)), (0, 1, 0))
                             for a in np.linspace(0, 2 * np.pi, 5, endpoint=False)]))
    parts.append((hub, ALLOY, "hub"))

    # 5x120 lug hardware: M12 wheel bolts with washer seats and hex heads.
    lugs = [
        ME.cap_screw(
            "M12",
            22,
            (58 * np.cos(a), FACE_Y + 18, 58 * np.sin(a)),
            (0, 1, 0),
        )
        for a in np.linspace(0, 2 * np.pi, 5, endpoint=False)
    ]
    parts.append((_compound(lugs), LUG, "lug_bolts"))

    # roundel centre cap (proper four-quarter Classic roundel).  The roundel must sit
    # PROUD of the black cap disc (cap outer face at FACE_Y+36) or the cap buries
    # it and you only see a black circle  -  push it out so the logo reads.
    parts.append((C.cyl(34, 8, (0, FACE_Y + 40, 0), (0, 1, 0)), C.BLACK, "cap"))
    for s, rgb, nm in C.roundel((0, FACE_Y + 54, 0), "+y", r=29):
        parts.append((s, rgb, "cap_" + nm.split("_", 1)[1]))
    return parts


def _brake():
    parts = []
    # vented disc: outer ring face + cross-drilled holes
    disc = C.cyl(150, 26, (0, -10, 0), (0, 1, 0)).cut(C.cyl(150 - 34, 30, (0, -12, 0), (0, 1, 0)))
    hub_face = C.cyl(150 - 34 + 4, 26, (0, -10, 0), (0, 1, 0)).cut(C.cyl(78, 30, (0, -12, 0), (0, 1, 0)))
    disc = disc.fuse(hub_face)
    holes = []
    for ring_r, n in ((128, 30), (108, 26)):
        for k in range(n):
            a = 2 * np.pi * k / n + (0.1 if ring_r < 120 else 0)
            holes.append(C.cyl(5.5, 40, (ring_r * np.cos(a), -16, ring_r * np.sin(a)), (0, 1, 0)))
    disc = disc.cut(_compound(holes))
    parts.append((disc, DISC, "brake_disc"))
    # top hat connecting disc to hub
    hat = C.cyl(80, 30, (0, 6, 0), (0, 1, 0)).cut(C.cyl(60, 36, (0, 2, 0), (0, 1, 0)))
    parts.append((hat, HAT, "brake_hat"))

    # four-pot caliper straddling the disc at the rear (local +X, ~3 o'clock)
    ring = C.cyl(170, 78, (0, -39, 0), (0, 1, 0)).cut(C.cyl(138, 90, (0, -45, 0), (0, 1, 0)))
    body = ring.intersect(C.box(120, -44, -96, 80, 88, 200))     # keep +X sector
    bolts = _compound([C.box(150, s * 30, -70, 26, 16, 140) for s in (1, -1)])
    caliper = body.fuse(bolts)
    parts.append((caliper, C.CALIPER, "caliper"))
    return parts


def _build_left():
    global _BUILD
    if _BUILD is None:
        _BUILD = [(_tire(), C.TIRE, "tire")] + _rim()
    return _BUILD


# ------------------------------------------------------------------------
#  MATE-CONSTRAINED BRAKE STACK
#  Built in the wheel's local frame (axis = Y, origin = wheel centre, +Y
#  outboard).  The rotor is SEATED onto the hub by a face mate + solve  -  it is
#  not placed at a coordinate  -  so the brake disc can never float off the hub or
#  collide with it.  The corner owns the rotor + caliper; the brakes package no
#  longer emits per-wheel discs (see brakes/front_calipers_rotors.py).
# ------------------------------------------------------------------------
ROTOR_C = (0.40, 0.40, 0.42)
HUB_C   = (0.36, 0.37, 0.40)
_MATE_CORNER = {}


def _hub_local():
    """Bearing hub flange, axis = Y.  Offset OUTBOARD (+Y 30) so the rotor  -  which
    seats on the hub's inboard face  -  ends up just inboard of the wheel face,
    leaving the inboard zone clear for the strut / control arm / trailing arm
    (otherwise the disc sat too far inboard and the links speared it)."""
    hub = cq.Workplane("XZ").cylinder(26, 56).translate((0, 21, 0))
    hub = hub.faces(">Y").chamfer(3).faces("<Y").chamfer(3)
    mating.tag(hub, rotor_seat="<Y")
    return hub


def _rotor_local(r_disc=152.0):
    """Ventilated, cross-drilled disc with an outboard top-hat (axis = Y).  The
    hat face is tagged so it seats flat + concentric on the hub."""
    hat = cq.Workplane("XZ").cylinder(40, 70).translate((0, 20, 0))    # y 0..40
    disc = cq.Workplane("XZ").cylinder(26, r_disc).translate((0, -13, 0))  # y -26..0
    rotor = hat.union(disc).cut(cq.Workplane("XZ").cylinder(54, 58).translate((0, 16, 0)))
    rotor = (rotor.faces("<Y").workplane()
                  .polarArray(r_disc - 40, 0, 360, 10).hole(9))         # cross-drill
    rotor = rotor.faces("<Y").chamfer(2)
    mating.tag(rotor, seat=">Y")
    return rotor


def _caliper_local(r_disc=152.0):
    """4-pot caliper straddling the disc at the side of the rotor (rigid in the corner
    frame; the rotor it straddles is itself mate-solved)."""
    inboard = C.rbox(r_disc - 34, -76, -45, 50, 16, 90, 6)
    outboard = C.rbox(r_disc - 34, 12, -45, 50, 16, 90, 6)
    bridge_top = C.rbox(r_disc + 2, -60, 34, 14, 88, 18, 5)
    bridge_bottom = C.rbox(r_disc + 2, -60, -52, 14, 88, 18, 5)
    pistons = [
        C.cyl(18, 8, (r_disc - 16, -84, z), (0, 1, 0))
        for z in (-24, 24)
    ] + [
        C.cyl(18, 8, (r_disc - 16, 24, z), (0, 1, 0))
        for z in (-24, 24)
    ]
    through_bolts = [
        ME.through_bolt("M10", 84, (r_disc + 4, -72, z), (0, 1, 0))
        for z in (-50, 54)
    ]
    return C.U([inboard, outboard, bridge_top, bridge_bottom] + pistons + through_bolts)


def _detail_bearing_hub(solid):
    """Machined hub: the flange is BORED so the pressed-in bearing is visible
    in its seat (not fused invisibly inside solid stock), with a circlip
    groove at the bore mouth and the grease-seal ring above it."""
    solid = solid.cut(C.cyl(45, 24, (0, 6, 0), (0, 1, 0)))
    solid = solid.cut(C.cyl(47, 2.5, (0, 27, 0), (0, 1, 0)))
    bearing = ME.radial_ball_bearing(44, 20, 22, (0, 10, 0), (0, 1, 0), ball_count=12)
    seal = C.cyl(48, 4, (0, 31, 0), (0, 1, 0)).cut(C.cyl(23, 6, (0, 30, 0), (0, 1, 0)))
    return solid.fuse(bearing).fuse(seal)


def _mate_corner_flat(fr):
    """Solve the hub+rotor mate once per axle and cache the local flat parts."""
    if fr in _MATE_CORNER:
        return _MATE_CORNER[fr]
    r_disc = 140.0 if fr == "F" else 141.0   # road spec: 280 mm front, 282 mm rear
    colors = {"bearing_hub": HUB_C, "brake_rotor": ROTOR_C}
    try:
        assy = mating.build({"bearing_hub": _hub_local(), "brake_rotor": _rotor_local(r_disc)},
                            [("bearing_hub+rotor_seat", "brake_rotor+seat")],
                            grounded="bearing_hub", colors=colors)
        flat = mating.to_flat(assy, colors)
    except Exception:   # deterministic fallback keeps the build alive
        hub = _hub_local().val()
        rotor = _rotor_local(r_disc).val().moved(cq.Location(cq.Vector(0, -22, 0)))
        flat = [(hub, HUB_C, "bearing_hub"), (rotor, ROTOR_C, "brake_rotor")]
    flat = [
        (_detail_bearing_hub(solid), color, name) if name == "bearing_hub" else (solid, color, name)
        for solid, color, name in flat
    ]
    flat.append((_caliper_local(r_disc), C.CALIPER, "brake_caliper"))
    flat += list(_build_left())                              # detailed tyre + rim
    _MATE_CORNER[fr] = flat
    return flat


def corner(ax, s, track):
    """A full mate-assembled corner (tyre + rim + hub + mate-seated rotor +
    caliper), mirrored for the right side and placed at the axle hardpoint."""
    side = "L" if s > 0 else "R"
    fr = "F" if ax < 2000 else "R"
    cy = s * track / 2.0
    out = []
    for solid, color, nm in _mate_corner_flat(fr):
        sp = solid if s > 0 else C.mirror_y(solid)
        out.append((sp.translate((ax, cy, C.WHEEL_Z)), color, f"{nm}_{fr}{side}"))
    return out


def parts():
    return []
