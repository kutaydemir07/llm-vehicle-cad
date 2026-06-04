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
    """Shallow arched bow at x, y= - 650, sitting under the roof skin."""
    z_end  = 1318.0
    z_mid  = z_end + crown_mm
    path   = [(x, 650, z_end), (x, 0, z_mid), (x, -650, z_end)]
    return C.swept_tube(path, 14, cap=True)


def _header(x):
    """Straight lateral header tube, inboard and below the DLO top edge."""
    return C.swept_tube([(x, 654, 1312), (x, -654, 1312)], 16, cap=True)


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
