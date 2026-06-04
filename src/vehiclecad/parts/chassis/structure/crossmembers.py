"""ASM_2110_Crossmembers_And_Ties - ModelA SportsCar chassis carrier detail.

This module models the chassis pieces the way a real CAD assembly would be
laid out: every member is already in vehicle coordinates and is kept inside a
clearance-owned envelope.  The front cradle stops forward of the LCA sweep, the
gearbox member sits directly under the transmission mount, and the rear tie is
aft of the differential/half-shaft package.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

_U      = C.U
_mirror = C.mirror_y
_box    = C.box
_cyl    = C.cyl
COL     = C.STRUCT


def _rbox_center(cx, cy, cz, dx, dy, dz, r):
    return C.rbox(cx - dx / 2.0, cy - dy / 2.0, cz - dz / 2.0, dx, dy, dz, r)


def _shell_box_center(cx, cy, cz, dx, dy, dz, wall):
    return C.shell_box(cx - dx / 2.0, cy - dy / 2.0, cz - dz / 2.0, dx, dy, dz, wall)


def _front_crossmember():
    """Stamped front axle carrier, forward of the rack/LCA envelope.

    The carrier sits at x=340, well ahead of the steering rack at x~780.  End
    horns land on the two front subframe rails, while the centre beam is low
    enough to leave oil-pan and radiator clearance.
    """
    main = C.swept_tube([(340, 548, 292), (340, -548, 292)], 26, cap=True)
    lower_flange = C.swept_tube([(366, 470, 250), (366, -470, 250)], 16, cap=True)
    horn_l = C.swept_tube([(340, 548, 292), (366, 424, 276)], 20, cap=True)
    horn_r = _mirror(horn_l)
    rack_window_stiffener = C.swept_tube([(334, 214, 314), (334, -214, 314)], 12, cap=True)

    pads = []
    for y in (430, -430):
        pads.append(_rbox_center(354, y, 286, 54, 88, 34, 7))
        pads.append(_cyl(11, 40, (354, y - 20, 286), (0, 1, 0)))

    return _U([main, lower_flange, horn_l, horn_r, rack_window_stiffener] + pads)


def _front_subframe_rails():
    """Pair of short front cradle rails tied to the front crossmember.

    A previous long rail ran back into the LCA/ARB swept volume.  The real ModelA
    carrier has short boxed fore-aft legs with separate pivot brackets; here the
    rail leaf stops at x=625, leaving a real service gap before the LCA hardpoint
    at x=660 and the ARB bend at x>=667.
    """
    parts = []
    for s in (1, -1):
        rail = _shell_box_center(480, s * 424, 278, 280, 52, 64, 3)
        front_pad = _rbox_center(356, s * 424, 290, 58, 82, 40, 7)
        rear_clevis = _rbox_center(600, s * 350, 230, 50, 76, 32, 6)
        rear_bush_sleeve = _cyl(14, 54, (600, s * 323, 230), (0, s, 0))
        diagonal = C.swept_tube([(558, s * 418, 284), (614, s * 350, 230)], 12, cap=True)
        parts.append(_U([rail, front_pad, rear_clevis, rear_bush_sleeve, diagonal]))
    return parts


def _transmission_crossmember():
    """Pressed-steel gearbox support directly under the ManualGearbox rear mount.

    The cross-car beam carries the gearbox mount on the centreline; outboard
    gusset arms then run out and DOWN to the two floor frame rails at
    ``+/-_RAIL_Y`` so the member is welded into the longitudinal frame instead
    of hanging in space under the tunnel.
    """
    beam = C.swept_tube([(1350, 356, 332), (1350, -356, 332)], 22, cap=True)
    saddle = _rbox_center(1350, 0, 348, 88, 170, 18, 6)
    leg_l = C.swept_tube([(1350, 304, 220), (1350, 304, 332)], 18, cap=True)
    leg_r = _mirror(leg_l)
    foot_l = _rbox_center(1350, 304, 224, 74, 64, 22, 6)
    foot_r = _mirror(foot_l)
    gus_l = C.swept_tube([(1350, 304, 250), (1350, 238, 326)], 12, cap=True)
    gus_r = _mirror(gus_l)
    bolt_l = _cyl(9, 16, (1350, 52, 354), (0, 0, 1))
    bolt_r = _mirror(bolt_l)
    # Outboard arms reaching the floor frame rails (y~RAIL_Y, dropping to rail z).
    arm_l = C.swept_tube([(1350, 352, 330), (1350, 452, 288), (1350, _RAIL_Y, 250)], 16, cap=True)
    arm_r = _mirror(arm_l)
    return _U([beam, saddle, leg_l, leg_r, foot_l, foot_r, gus_l, gus_r,
               bolt_l, bolt_r, arm_l, arm_r])


# Lateral offset of the main floor frame rails.  Chosen well inboard of the
# rocker sills (y~790) and outboard of the propshaft tunnel (y~100), on the ModelA
# floor longitudinal-rail line, so the rails clear the propshaft, fuel and
# exhaust runs that share the underbody.
_RAIL_Y = 490.0


def _frame_rail_left():
    """One continuous LEFT longitudinal frame rail that ties the whole chassis
    into a single connected weldment -- the way a unibody floor frame is drawn.

    The route threads the reserved package corridors (verified by the exact
    collision gate):

      * FRONT: welds into the front crossmember and the front subframe-rail leaf;
      * ENGINE BAY: rides the front-rail line ABOVE the front ARB sweep
        (z>307) and OUTBOARD of the steering pump, below the brake booster;
      * TORQUE BOX: kicks down at the firewall onto the gearbox crossmember arm;
      * FLOOR: runs just under the floorpan, outboard of the propshaft, fuel
        lines/tank and exhaust;
      * REAR: a thinner section climbs over the rear axle -- outboard of the
        diff, springs, dampers and CV joints, above the rear ARB -- to land on
        the rear subframe and the rear crossmember.

    A near-vertical shock-tower leg ties in the upper engine-bay (strut-tower)
    tie, kept aft of the brake booster (x>=1205), so nothing is left floating.
    """
    y = _RAIL_Y
    # main rail: front crossmember -> engine bay -> torque box -> floor -> subframe
    main = C.swept_tube([
        (352,  500, 296),   # weld: front crossmember (y < 553 half-width)
        (500,  488, 306),   # outboard of steering pump, kiss subframe-rail leaf
        (700,  486, 332),   # rise above the front ARB (ARB top z~307)
        (1010, 484, 360),   # engine-bay front-rail line, outboard of bellhousing
        (1185, 486, 350),   # below the brake booster, approaching the firewall
        (1262, 498, 298),   # torque-box kick-down toward the floor
        (1350, y,   250),   # weld: gearbox-crossmember outboard arm
        (1640, y,   202),   # tuck just under the floorpan
        (2250, 496, 196),   # mid-floor, clear corridor
        (2820, 494, 212),   # approach the rear subframe
        (3070, 488, 238),   # weld: rear subframe side pod
    ], 28, cap=True)
    # rear rail: rear subframe -> over the axle -> rear crossmember.  Thinner so
    # it threads the window outboard of the diff/CV and above the rear ARB.
    rear = C.swept_tube([
        (3070, 488, 238),
        (3300, 512, 286),   # outboard of diff & CV boot, above ARB, below damper eye
        (3680, 516, 322),   # climb to trunk-floor height, outboard of muffler/spare well
        (4030, 518, 346),
        (4195, 512, 360),   # weld: rear crossmember (z 304..421)
    ], 22, cap=True)
    # shock-tower leg: floor rail -> upper engine-bay (strut-tower) tie.  Kept at
    # x>=1205 (aft of the booster) and |y|>512 so it clears the brake booster.
    leg = C.swept_tube([
        (1200, 487, 342),   # branch off the main rail
        (1208, 522, 478),
        (1209, 532, 640),
        (1208, 528, 784),   # weld: into engine-bay tie firewall tab (y 466..534, z 763..797)
    ], 20, cap=True)
    return _U([main, rear, leg])


def _frame_rails():
    """Left + right longitudinal frame rails (right is the mirror of left)."""
    left = _frame_rail_left()
    return [left, _mirror(left)]


def _rear_crossmember():
    """Rear boot/bumper tie, aft of the diff and muffler front face."""
    lower = C.swept_tube([(4200, 674, 330), (4200, -674, 330)], 26, cap=True)
    upper = C.swept_tube([(4186, 604, 406), (4186, -604, 406)], 15, cap=True)
    post_l = C.swept_tube([(4200, 590, 330), (4186, 590, 406)], 14, cap=True)
    post_r = _mirror(post_l)
    tow_l = _rbox_center(4210, 472, 318, 52, 70, 18, 6)
    tow_r = _mirror(tow_l)
    return _U([lower, upper, post_l, post_r, tow_l, tow_r])


def _engine_bay_crossmember():
    """Upper firewall-side tower tie with local weld tabs.

    Long diagonal braces live in the body/tower structure.  Keeping this chassis
    leaf as a short cross-car tie prevents its part-level bounding box from
    falsely occupying the I4_Engine valve-cover and front spring envelopes.
    """
    tie = C.swept_tube([(1200, 500, 780), (1200, -500, 780)], 18, cap=True)
    firewall_tab_l = _rbox_center(1196, 500, 780, 34, 68, 34, 6)
    firewall_tab_r = _mirror(firewall_tab_l)
    centre_tab = _rbox_center(1196, 0, 762, 28, 96, 22, 5)
    return _U([tie, firewall_tab_l, firewall_tab_r, centre_tab])


def parts():
    out = []
    out.append((_front_crossmember(),      COL, "PRT_Front_Crossmember"))
    out.append((_transmission_crossmember(), COL, "PRT_Trans_Crossmember"))
    out.append((_rear_crossmember(),       COL, "PRT_Rear_Crossmember"))
    out.append((_engine_bay_crossmember(), COL, "PRT_Engine_Bay_Tie"))
    for i, rail in enumerate(_front_subframe_rails()):
        side = "L" if i == 0 else "R"
        out.append((rail, COL, f"PRT_Front_Subframe_Rail_{side}"))
    # Longitudinal frame rails: the connecting spine that makes the chassis one
    # structure (front crossmember -> subframe rails -> gearbox crossmember ->
    # rear subframe -> rear crossmember, plus the engine-bay/strut-tower tie).
    for i, rail in enumerate(_frame_rails()):
        side = "L" if i == 0 else "R"
        out.append((rail, COL, f"PRT_Frame_Rail_{side}"))
    return out
