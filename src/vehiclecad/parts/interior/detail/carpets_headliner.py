"""Carpets and headliner panels.

Floor carpet: thin fitted panels above the floorpan (z=227), x=1228-3105.
Driveshaft tunnel carpet: follows tunnel walls/top without filling the tunnel.
Headliner: thin plate below roof panel, relieved inboard of the cage side bars.

Collision-free:
   -  Carpet at z=225 (2 mm above floor at z=220)  -  negligible thickness.
   -  Headliner is kept below the DLO top line and inboard of the roof rails.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL_CARPET   = (0.08, 0.07, 0.07)
COL_HEADLIN  = (0.22, 0.22, 0.24)


def _floor_carpet():
    # Floor mats are thin surface layers, not solid blocks filling the tunnel.
    cabin_x0 = 1228.0
    # all floor trim stops at the floorpan carrier cut (x2860): nothing floats
    # over the open subframe bay (the bench covers it from above)
    cabin_dx = 2860.0 - cabin_x0
    left  = C.box(cabin_x0, 124, 227, cabin_dx, 568, 4)
    right = C.mirror_y(left)
    # rear mats stop at the floorpan carrier cut (x2860): no carpet floating
    # over the open subframe bay
    rear_left = C.box(2580, 124, 227, 278, 420, 4)
    rear_right = C.mirror_y(rear_left)
    # tunnel trim also stops at the carrier cut (x2860); the bench covers it aft
    tunnel_dx = 2860.0 - cabin_x0
    tunnel_top = C.box(cabin_x0, -96, 482, tunnel_dx, 192, 4)
    tunnel_left = C.box(cabin_x0, 104, 231, tunnel_dx, 4, 251)
    tunnel_right = C.mirror_y(tunnel_left)
    heel_pad_l = C.rbox(1330, 78, 232, 210, 450, 5, 2)
    heel_pad_r = C.mirror_y(heel_pad_l)
    return C.U([left, right, rear_left, rear_right, tunnel_top,
                tunnel_left, tunnel_right, heel_pad_l, heel_pad_r])


def _headliner():
    shell = C.rbox(1848, -640, 1308, 812, 1280, 7, 3)
    cage_relief_l = C.rbox(1840, 566, 1302, 760, 98, 22, 4)
    cage_relief_r = C.mirror_y(cage_relief_l)
    return shell.cut(cage_relief_l).cut(cage_relief_r)


def parts():
    return [
        (_floor_carpet(), COL_CARPET,  "PRT_Floor_Carpet"),
        (_headliner(),    COL_HEADLIN, "PRT_Headliner"),
    ]
