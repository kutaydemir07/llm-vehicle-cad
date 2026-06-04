"""ASM_3110_Antiroll_Bars - ModelA SportsCar stabilizer bars.

Both bars are complete bent torsion bars with D-bush clamps at the body pickups
and drop links out to the suspension.  Each bar is routed to stay well clear of
its corner hardparts and to land its drop-link eye flush on the tab that the
control arm / trailing arm provides for it (a designed pin joint, not a clash):

  * Front 18 mm bar: torsion section low and ahead of the steering rack, lever
    arms swept rearward INBOARD of the strut/knuckle corner, rising to a vertical
    drop link onto the LCA forward-arm tab.
  * Rear 16 mm bar: torsion section behind the subframe, lever arms forward to a
    short drop link onto the trailing-arm tab.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

FRONT = SK.FRONT_SUSP
REAR  = SK.REAR_SUSP


def _front_arb():
    """Front 18 mm stabilizer; lever arms stay inboard of the corner and drop a
    link onto the LCA tab at ``arb_end_link``."""
    bx, by, bz = FRONT["arb_bush_body"]   # (650, 300, 135)
    ex, ey, ez = FRONT["arb_end_link"]    # (845, 380, 224)  - LCA drop-link tab
    tab_top = ez + 11                      # 235 - top face of the LCA tab
    link_top = (ex, ey, tab_top + 70)      # (845, 380, 305)

    # torsion section across the front, low and ahead of the rack
    centre = C.swept_tube([(bx, -by, bz), (bx, by, bz)], 9, cap=True)
    # lever arm: rearward and gently up, kept inboard (y<=380) and clear of the
    # strut/knuckle corner (which lives at y>580), then up to the drop-link top
    arm_l = C.swept_tube([(bx, by, bz), (740, 330, 150), (800, 358, 238),
                          (840, 378, 288), link_top], 9, cap=True)
    arm_r = C.mirror_y(arm_l)

    # D-bush clamps at the subframe pickups
    bush_l  = C.cyl(15, 30, (bx - 5, by - 15, bz), (0, 1, 0))
    bush_r  = C.mirror_y(bush_l)
    clamp_l = C.rbox(bx - 26, by - 26, bz - 20, 52, 52, 18, 5)
    clamp_r = C.mirror_y(clamp_l)

    # vertical drop link + lower eye seated on the LCA tab top (eye tangent to the
    # tab face, joined by the link bolt)
    drop_l = C.swept_tube([link_top, (ex, ey, tab_top + 13)], 6, cap=True)
    drop_r = C.mirror_y(drop_l)
    eye_l  = C.cyl(13, 24, (ex, ey - 12, tab_top + 13), (0, 1, 0))
    eye_r  = C.mirror_y(eye_l)
    return C.U([centre, arm_l, arm_r, bush_l, bush_r, clamp_l, clamp_r,
                drop_l, drop_r, eye_l, eye_r])


def _rear_arb():
    """Rear 16 mm stabilizer behind the subframe with short forward lever arms and
    drop links onto the trailing-arm tabs."""
    bx, by, bz = REAR["arb_bush_body"]    # (3505, 300, 150)
    ex, ey, ez = REAR["arb_end_link"]     # (3322, 600, 300) - trailing-arm tab
    tab_top = ez + 11                      # 311
    link_top = (ex, ey, tab_top + 60)      # (3322, 600, 371)

    centre = C.swept_tube([(bx, -by, bz), (bx, by, bz)], 8, cap=True)
    # lever arm forward and outboard to above the trailing-arm tab, kept inboard
    # of the hub (y<=600) and rising clear of the arm
    arm_l = C.swept_tube([(bx, by, bz), (3478, 430, 185), (3445, 565, 250),
                          (3410, 630, 366), link_top], 8, cap=True)
    arm_r = C.mirror_y(arm_l)

    bush_l  = C.cyl(14, 28, (bx - 4, by - 14, bz), (0, 1, 0))
    bush_r  = C.mirror_y(bush_l)
    clamp_l = C.rbox(bx - 24, by - 26, bz - 18, 48, 52, 16, 5)
    clamp_r = C.mirror_y(clamp_l)

    drop_l = C.swept_tube([link_top, (ex, ey, tab_top + 13)], 6, cap=True)
    drop_r = C.mirror_y(drop_l)
    eye_l  = C.cyl(13, 24, (ex, ey - 12, tab_top + 13), (0, 1, 0))
    eye_r  = C.mirror_y(eye_l)
    return C.U([centre, arm_l, arm_r, bush_l, bush_r, clamp_l, clamp_r,
                drop_l, drop_r, eye_l, eye_r])


def parts():
    return [
        (_front_arb(), C.STRUCT, "PRT_Front_ARB"),
        (_rear_arb(),  C.STRUCT, "PRT_Rear_ARB"),
    ]
