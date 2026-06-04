"""V-model System 1000  -  engine-bay (Motorraum) enclosure.

Encloses the engine bay so it reads as a real compartment instead of an open
cavity you can see the wheels and ground through:

  * ``PRT_Radiator_Support``  -  slam / core-support panel closing the bay FRONT
    behind the grille (a picture-frame around the radiator core opening),
  * ``PRT_Inner_Fender_L/R``  -  inner-fender aprons forming the bay SIDE walls
    over the front wheel houses, tying the strut towers to the rad support,
  * ``PRT_Apron_Rail_L/R``    -  the hood-gutter rails capping the aprons.

The bay REAR is already closed by ``PRT_Firewall_Bulkhead`` (firewall.py) and the
floor by the floorpan, so this module only adds the missing front + side metal.
All panels are kept inside their packaging envelopes and clear of the engine.
"""
from __future__ import annotations
import cadquery as cq
from cadquery import Solid, Vector

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import packaging as P

COL = C.STRUCT


def _yz_prism(poly, x0, x1):
    """Extrude a (y, z) polygon along +X  -  the YZ analogue of geometry.xz_prism."""
    p = [Vector(x0, y, z) for (y, z) in poly]
    face = cq.Face.makeFromWires(cq.Wire.makePolygon(p + [p[0]]))
    return Solid.extrudeLinear(face, Vector(x1 - x0, 0, 0))


def _rad_support():
    """Front slam panel: a picture-frame at the radiator plane (behind the grille,
    below the hood), with the core opening sized to clear the radiator core so the
    radiator hangs in it.  Forward of the fan / crossmember / engine."""
    e = P.env("RAD_SUPPORT")          # x140..215
    x0, dx = e.x0, e.dx
    outer = C.box(x0 + 6, -432, 332, dx - 12, 864, 494)        # z332..826
    core = C.box(x0 - 10, -365, 420, dx + 20, 730, 380)        # opening z420..800
    frame = outer.cut(core)
    sill = C.rbox(x0 + 4, -332, 332, dx - 8, 664, 42, 8)       # lower core support
    return C.U([frame, sill])


def _inner_fender(side):
    """Slanted apron wall: bottom-inboard at the rail, rising top-outboard to the
    fender top, so the line of sight from the bay down to the wheel is blocked."""
    s = 1 if side == "L" else -1
    yb, zb = 434.0, 296.0      # bottom inboard edge (just outboard of the engine)
    yt, zt = 602.0, 896.0      # top outboard edge (fender top / hood gutter)
    th = 7.0
    poly = [(s * yb, zb), (s * (yb + th), zb), (s * (yt + th), zt), (s * yt, zt)]
    panel = _yz_prism(poly, 346.0, 1216.0)
    panel = P.clip_to(panel, P.env(f"INNER_FENDER_{side}"), margin=24)
    # strut-tower clearance bore so the strut/spring pass through the apron
    panel = panel.cut(C.cyl(92, 760, (810, s * 560, 240), (0, 0, 1)))
    return panel


def _apron_rail(side):
    """Hood-gutter rail capping the apron from the rad support back to the cowl,
    set outboard of the strut top-mount (|y|>608) so it doesn't foul it."""
    s = 1 if side == "L" else -1
    return C.rbox(346, s * 630 - 22, 872, 870, 44, 42, 10)


def parts():
    out = []
    out.append((_rad_support(), COL, "PRT_Radiator_Support"))
    for side in ("L", "R"):
        out.append((_inner_fender(side), COL, f"PRT_Inner_Fender_{side}"))
        out.append((_apron_rail(side), COL, f"PRT_Apron_Rail_{side}"))
    return out

