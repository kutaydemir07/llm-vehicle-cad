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
    """A-pillar  -  forward door post, raked at  - 68 -  with windshield.

    Cross-section: 40 mm box.  Runs inside the aperture frame so it no longer
    shares volume with the outer body structure shell.
    """
    poly = [
        (1505, 330),    # base at sill
        (1538, 330),    # base outer
        (1818, 1326),   # header outer
        (1784, 1326),   # header inner
    ]
    y_centre = 694.0
    half_t = 18.0
    return _xzp(poly, y_centre - half_t, y_centre + half_t)


def _b_pillar_left():
    """B-pillar  -  vertical post between door opening and rear quarter window.

    Cross-section: 40  -  36 mm box-section, z 330  -  1326.
    Located inboard of the aperture shell.
    """
    poly = [
        (2492, 330),    # sill
        (2526, 330),    # sill outer
        (2526, 1326),   # roof rail outer
        (2492, 1326),   # roof rail inner
    ]
    y_centre = 694.0
    half_t = 18.0
    return _xzp(poly, y_centre - half_t, y_centre + half_t)


def _roof_rail_left():
    """Roof side rail  -  longitudinal member connecting A, B, C pillars at roof.

    Box section running from x=1790 to x=2780 inside the greenhouse rail.
    """
    x0, x1 = 1805.0, 2745.0
    z0 = 1288.0
    y0 = 672.0
    return _box(x0, y0, z0, x1 - x0, 36, 28)


def _sill_crossmember():
    """Front sill cross-member  -  lateral tube at the base of the A-pillar.

    Runs as left/right toe-board braces and leaves the centre tunnel open.
    """
    left = C.swept_tube([(1500, 690, 350), (1500, 135, 350)], 18, cap=True)
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
