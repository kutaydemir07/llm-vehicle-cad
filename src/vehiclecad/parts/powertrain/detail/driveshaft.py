"""Propshaft (driveshaft)  -  two-piece, centre support bearing, three U-joints.

Runs from the gearbox output (prop_front) to the diff input (prop_rear) through
the transmission tunnel.  Built as clean turned tubes placed onto their axes with
``mating.place_along`` (so each section leans along its true segment), with real
U-joint spiders and a rubber-mounted centre bearing  -  not a single fused tube.
"""
from __future__ import annotations
import math
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import mating
from vehiclecad.geometry import machine_elements as ME
from vehiclecad.parts.powertrain.detail import layout as L

COL    = C.STRUCT
YOKE   = (0.28, 0.29, 0.33)
RUBBER = (0.10, 0.10, 0.11)
FASTENER = (0.13, 0.13, 0.14)
BEARING = (0.55, 0.56, 0.60)


def _tube(p0, p1, r, name):
    """A balanced shaft tube with end yoke flanges, placed on the p0->p1 axis."""
    L = math.dist(p0, p1)
    tube = C.cyl(r, L - 28, (0, 0, 14), (0, 0, 1)).cut(
        C.cyl(max(4.0, r - 5), L - 24, (0, 0, 12), (0, 0, 1))
    )
    fl0  = C.cyl(r + 9, 16, (0, 0, 0), (0, 0, 1))
    fl1  = C.cyl(r + 9, 16, (0, 0, L - 16), (0, 0, 1))
    return mating.place_along([(C.U([tube, fl0, fl1]), COL, name)], p0, p1)


def _placed_local(shape, p0, p1, name, color=COL):
    return mating.place_along([(shape, color, name)], p0, p1)


def _bolt_circle_x(center, radius, bolt_r, bolt_len, count, name):
    """Bolt set on a YZ bolt circle with shanks along the driveline X axis."""
    cx, cy, cz = center
    bolts = []
    for i in range(count):
        a = 2.0 * math.pi * i / count
        y = cy + radius * math.cos(a)
        z = cz + radius * math.sin(a)
        designation = "M8" if bolt_r <= 4.5 else "M10"
        bolts.append(ME.through_bolt(designation, bolt_len, (cx - bolt_len / 2.0, y, z), (1, 0, 0)))
    return C.U(bolts), FASTENER, name


def _balance_weights(p0, p1, r, name):
    """Small welded balance tabs clocked on opposite sides of a shaft tube."""
    L = math.dist(p0, p1)
    weights = [
        C.rbox(-18, r - 2, L * 0.32, 36, 7, 28, 2),
        C.rbox(-15, -r - 5, L * 0.70, 30, 7, 22, 2),
    ]
    return _placed_local(C.U(weights), p0, p1, name, FASTENER)


def _ujoint(p):
    """U-joint spider  -  a cross of two needle-bearing journals in a yoke hub."""
    r = 30
    j1 = C.cyl(9, 2 * r, (p[0], p[1] - r, p[2]), (0, 1, 0))
    j2 = C.cyl(9, 2 * r, (p[0], p[1], p[2] - r), (0, 0, 1))
    hub = C.rbox(p[0] - 14, p[1] - 16, p[2] - 16, 28, 32, 32, 6)
    caps = [
        C.cyl(12, 8, (p[0], p[1] - r - 4, p[2]), (0, 1, 0)),
        C.cyl(12, 8, (p[0], p[1] + r - 4, p[2]), (0, 1, 0)),
        C.cyl(12, 8, (p[0], p[1], p[2] - r - 4), (0, 0, 1)),
        C.cyl(12, 8, (p[0], p[1], p[2] + r - 4), (0, 0, 1)),
    ]
    return C.U([j1, j2, hub] + caps)


def _propshaft():
    pf = L.PROPSHAFT_FRONT
    pr = L.PROPSHAFT_REAR
    mid = ((pf[0] + pr[0]) / 2.0, 0.0, (pf[2] + pr[2]) / 2.0)   # centre bearing
    out = []

    # Rubber flex disc (guibo) seats between the gearbox output flange and the
    # front yoke.  Its centroid is exactly on the propshaft front hardpoint.
    guibo = C.cyl(58, 26, (pf[0] - 13, pf[1], pf[2]), (1, 0, 0)).cut(
        C.cyl(24, 30, (pf[0] - 15, pf[1], pf[2]), (1, 0, 0))
    )
    bolt_pads = []
    for i in range(6):
        a = 2.0 * math.pi * i / 6
        bolt_pads.append(C.cyl(8, 30, (pf[0] - 15, pf[1] + 42 * math.cos(a), pf[2] + 42 * math.sin(a)), (1, 0, 0)))
    out.append((C.U([guibo] + bolt_pads), RUBBER, "PRT_Propshaft_Flex_Disc"))
    out.append(_bolt_circle_x((pf[0] + 18, pf[1], pf[2]), 42, 4.5, 16, 6, "PRT_Guibo_Bolt_Set"))

    out += _tube(pf, mid, 34, "PRT_Propshaft_Front")
    out += _tube(mid, pr, 32, "PRT_Propshaft_Rear")
    out += _balance_weights(pf, mid, 34, "PRT_Propshaft_Front_Balance_Weights")
    out += _balance_weights(mid, pr, 32, "PRT_Propshaft_Rear_Balance_Weights")

    # Slip spline just ahead of the centre bearing, drawn as a sleeve with raised
    # spline lands.  It is coaxial with the front shaft and lets the two-piece
    # shaft float axially without being spatially loose.
    front_len = math.dist(pf, mid)
    # hollow splined sleeve so the front shaft slides inside it (slip joint)
    spline_parts = [C.cyl(38, 94, (0, 0, front_len - 132), (0, 0, 1)).cut(
        C.cyl(35, 100, (0, 0, front_len - 135), (0, 0, 1)))]
    for i in range(8):
        a = 2.0 * math.pi * i / 8
        spline_parts.append(C.rbox(
            35 * math.cos(a) - 2.0,
            35 * math.sin(a) - 2.0,
            front_len - 122,
            4,
            4,
            74,
            1,
        ))
    out += _placed_local(C.U(spline_parts), pf, mid, "PRT_Propshaft_Slip_Spline", BEARING)

    # Rubber-mounted centre support bearing hanging from the tunnel.
    bearing = C.cyl(42, 28, (mid[0] - 14, 0, mid[2]), (1, 0, 0)).cut(
        C.cyl(36, 34, (mid[0] - 17, 0, mid[2]), (1, 0, 0))   # bore clears the r34 shaft
    )
    isolator = C.cyl(58, 34, (mid[0] - 17, 0, mid[2]), (1, 0, 0)).cut(
        C.cyl(43, 40, (mid[0] - 20, 0, mid[2]), (1, 0, 0))
    )
    out.append((bearing, BEARING, "PRT_Centre_Bearing"))
    out.append((isolator, RUBBER, "PRT_Centre_Bearing_Rubber_Isolator"))
    out.append((C.rbox(mid[0] - 22, -26, mid[2] + 30, 44, 52, 70, 6), COL, "PRT_Centre_Bearing_Bracket"))
    out.append((C.rbox(mid[0] - 70, -72, mid[2] + 86, 140, 144, 12, 4), COL, "PRT_Centre_Bearing_Tunnel_Plate"))
    out.append(_bolt_circle_x((pr[0] - 12, pr[1], pr[2]), 40, 4.5, 38, 4, "PRT_Diff_Input_Flange_Bolt_Set"))
    # three U-joints
    for jp, nm in ((pf, "PRT_UJoint_Front"), (mid, "PRT_UJoint_Centre"), (pr, "PRT_UJoint_Rear")):
        out.append((_ujoint(jp), YOKE, nm))
    return out


def parts():
    return _propshaft()
