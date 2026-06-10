"""Roof bows and header/rear-header rails  -  BiW roof skeleton.

Parts:
  PRT_Front_Roof_Header    -  lateral tube at x=1790 (A-pillar top)
  PRT_Rear_Roof_Header     -  lateral tube at x=2780 (C-pillar top)
  PRT_Roof_Bow_1           -  mid-span bow at x=2100
  PRT_Roof_Bow_2           -  mid-span bow at x=2450

All bows run at z=1365 (just below roof skin) and are slightly arched to
follow the 8 mm roof crown.

Collision-free:
  Bows sit below the roof skin and DLO top line.
  They span y= - 650, staying clearly inboard of the glass and roof rail.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

_U      = C.U
_box    = C.box
COL     = C.STRUCT


def _bow(x, crown_mm=8):
    """Roof bow as the production part: an open-bottom hat CHANNEL (3 mm wall)
    with weld feet at the rail ends -- not a solid bar."""
    bow = _box(x - 14, -650, 1306, 28, 1300, 24).cut(
        _box(x - 11, -647, 1300, 22, 1294, 27))
    foot_l = C.rbox(x - 20, 632, 1298, 40, 26, 10, 3)
    foot_r = C.rbox(x - 20, -658, 1298, 40, 26, 10, 3)
    return C.U([bow, foot_l, foot_r])


def _header(x):
    """Lateral header as a hollow closed box section with end weld tabs."""
    hdr = _box(x - 16, -654, 1298, 32, 1308, 28).cut(
        _box(x - 13, -651, 1301, 26, 1302, 22))
    tab_l = C.rbox(x - 22, 636, 1294, 44, 24, 8, 3)
    tab_r = C.rbox(x - 22, -660, 1294, 44, 24, 8, 3)
    return C.U([hdr, tab_l, tab_r])


def parts():
    # x-positions follow the new GREEN roofline: front header BEHIND the windshield
    # top (~1772), rear header AHEAD of the backlight top (~2760); all dropped below
    # the roof skin so they no longer stab the glass.
    out = []
    out.append((_header(1805), COL, "PRT_Front_Roof_Header"))
    out.append((_header(2730), COL, "PRT_Rear_Roof_Header"))
    out.append((_bow(2080),    COL, "PRT_Roof_Bow_1"))
    out.append((_bow(2440),    COL, "PRT_Roof_Bow_2"))
    return out
