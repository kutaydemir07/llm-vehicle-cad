"""Rear bench seat.

The pan is STEPPED to follow the real under-seat package (this is how the
production bench is trimmed):

  * knee-roll lip ahead of the rear subframe        (x<2872, bottom z306)
  * pan over the trailing-arm sweep                 (arm top z358 -> bottom z362)
  * raised section over the fuel tank               (tank top z430 -> bottom z434)
  * tunnel relief through the centre                (tunnel+carpet to z486)
  * in-tank fuel-pump service hatch pocket          (pump top z450)

Backrest bottom z470 clears the tank (430), propshaft (406) and arm (358).
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL  = (0.11, 0.11, 0.13)


def _rear_bench():
    lip      = C.rbox(2765, -455, 306, 107, 910, 164, 12)   # ahead of subframe x2875
    pan      = C.rbox(2870, -455, 362, 90, 910, 108, 10)    # over the trailing arms
    overtank = C.rbox(2955, -455, 434, 80, 910, 36, 8)      # over the fuel tank
    top      = C.rbox(2765, -455, 442, 270, 910, 78, 14)    # continuous squab top
    front_roll = C.cyl(34, 880, (2778, -440, 446), (0, 1, 0))
    cushion = C.U([lip, pan, overtank, top, front_roll])
    backrest = C.rbox(3040, -438, 470, 74, 876, 380, 14)
    shoulder_roll = C.cyl(34, 840, (3036, -420, 830), (0, 1, 0))
    bol_l = C.rbox(2784, 418, 442, 240, 46, 118, 8)
    bol_r = C.mirror_y(bol_l)
    centre_seam = C.rbox(2782, -8, 508, 238, 16, 16, 3)
    bench = C.U([cushion, backrest, shoulder_roll, bol_l, bol_r, centre_seam])
    # tunnel hump relief through cushion AND backrest (the tunnel + its carpet
    # run to x3450 at z<=486): 4 mm air to the carpet sides (|y|<=108)
    bench = bench.cut(C.box(2750, -112, 290, 380, 224, 196))
    # fuel-pump service hatch pocket (pump x3004..3096, y104..196, top z450)
    bench = bench.cut(C.box(2988, 96, 424, 52, 110, 40))
    return bench


def parts():
    return [(_rear_bench(), COL, "PRT_Rear_Bench_Seat")]
