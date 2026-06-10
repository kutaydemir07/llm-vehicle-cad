"""A, B and C-pillar box-section members (BiW).

All pillars are modelled as XZ prisms extruded in Y and positioned in the
vehicle frame.  Left (+Y) pillar defined first; right side is mirror_y.

Collision-free zones:
  A-pillar: x - 1500-1800, y -  - 675-715, z - 330-1326  (inside the outer shell)
  B-pillar: x - 2490-2530, y -  - 675-715, z - 330-1326   (between door and quarter)
  C-pillar: already implemented in pillar.py; here we add B-pillar
"""
from __future__ import annotations
import cadquery as cq
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

_box    = C.box
_cyl    = C.cyl
_U      = C.U
_mirror = C.mirror_y
_xzp    = C.xz_prism
COL     = C.STRUCT


def _a_pillar_left():
    """A-pillar -- forward door post, raked with the windshield, drawn as a
    real HOLLOW box-section weldment (3 mm wall) rather than solid billet."""
    poly = [
        (1505, 330),    # base at sill
        (1538, 330),    # base outer
        (1818, 1326),   # header outer
        (1784, 1326),   # header inner
    ]
    inner = [
        (1509, 336),
        (1534, 336),
        (1813, 1320),
        (1789, 1320),
    ]
    y_centre = 694.0
    half_t = 18.0
    section = _xzp(poly, y_centre - half_t, y_centre + half_t).cut(
        _xzp(inner, y_centre - half_t + 3, y_centre + half_t - 3))
    # base foot flange welding to the sill / rocker
    foot = C.rbox(1498, y_centre - 24, 326, 52, 48, 10, 3)
    return _U([section, foot])


def _b_pillar_left():
    """B-pillar -- hollow hat-section post with the door-striker reinforcement
    plate (z500..580, behind the latch) and a seat-belt anchor boss."""
    poly = [
        (2492, 330),    # sill
        (2526, 330),    # sill outer
        (2526, 1326),   # roof rail outer
        (2492, 1326),   # roof rail inner
    ]
    inner = [
        (2495, 336),
        (2523, 336),
        (2523, 1320),
        (2495, 1320),
    ]
    y_centre = 694.0
    half_t = 18.0
    section = _xzp(poly, y_centre - half_t, y_centre + half_t).cut(
        _xzp(inner, y_centre - half_t + 3, y_centre + half_t - 3))
    striker_plate = C.rbox(2496, y_centre + half_t, 500, 28, 6, 80, 2)
    belt_boss = _cyl(14, 8, (2509, y_centre - half_t - 8, 900), (0, 1, 0))
    belt_bolt = _cyl(5.5, 14, (2509, y_centre - half_t - 12, 900), (0, 1, 0))
    foot = C.rbox(2486, y_centre - 24, 326, 50, 48, 10, 3)
    return _U([section, striker_plate, belt_boss, belt_bolt, foot])


def _roof_rail_left():
    """Roof side rail -- hollow closed box section (3 mm wall) tying the
    pillar tops together, as the production rail is rolled."""
    x0, x1 = 1805.0, 2745.0
    z0 = 1288.0
    y0 = 672.0
    rail = _box(x0, y0, z0, x1 - x0, 36, 28).cut(
        _box(x0 + 3, y0 + 3, z0 + 3, x1 - x0 - 6, 30, 22))
    return rail


def _sill_crossmember():
    """Front sill cross-member -- toe-board braces with WELD FLANGE PLATES at
    the rocker and tunnel ends, so the member visibly lands on its joints."""
    left = C.swept_tube([(1500, 690, 350), (1500, 135, 350)], 18, cap=True)
    flange_rocker = C.rbox(1478, 684, 322, 44, 12, 56, 4)
    flange_tunnel = C.rbox(1478, 124, 322, 44, 12, 56, 4)
    left = _U([left, flange_rocker, flange_tunnel])
    right = C.mirror_y(left)
    return C.U([left, right])


def parts():
    out = []
    for fn, name in (
        (_a_pillar_left,   "PRT_A_Pillar"),
        (_b_pillar_left,   "PRT_B_Pillar"),
        (_roof_rail_left,  "PRT_Roof_Rail"),
    ):
        left = fn()
        right = _mirror(left)
        out.append((left,  COL, f"{name}_L"))
        out.append((right, COL, f"{name}_R"))
    out.append((_sill_crossmember(), COL, "PRT_Sill_Crossmember_Front"))
    return out
