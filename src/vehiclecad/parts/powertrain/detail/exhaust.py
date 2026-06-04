"""ASM_Powertrain_Packaging  -  I4_Engine engine, ManualGearbox 265, exhaust & driveline.

This module creates volumetric packaging envelopes for every powertrain
component in the Classic ModelA SportsCar.  Each shape is recognizable (not just a bounding
box) and positioned at the skeleton hardpoints in the vehicle frame.

Vehicle frame (see common.py):
    +X rearward (0 = front bumper)
    +Y leftward (0 = centreline)
    +Z upward   (0 = ground)
    Units: millimetres

Parts:
    PRT_I4_Engine_Crankcase_Casting        -  inline-4 iron block casting
    PRT_Intake_Plenum_ITB            -  individual throttle-body intake manifold
    PRT_Exhaust_Manifold_Tubular     -  4-1 tubular header + exhaust system
    PRT_ManualGearbox_265_Transmission      -  5-speed manual gearbox
    PRT_Driveshaft_LSD               -  propshaft, centre bearing, diff, half-shafts
"""
from __future__ import annotations
import math
import numpy as np

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference.hardpoints import POWERTRAIN as PT


# ------------------------------------------------------------------------
#  1.  PRT_I4_Engine_Crankcase_Casting
# ------------------------------------------------------------------------


def _exhaust_system() -> list:
    """Tubular 4-into-1 header + cat-back, as smoothly bent pipes.

    Four equal-length primaries leave the head exhaust face (RIGHT, -Y), each
    individually bent and nested into a tapered collector.  A single under-floor
    midpipe runs aft into the rear silencer and exits as twin chrome tips beneath
    the rear bumper.  Pipes are continuous swept tubes (``tube_path``), so the
    bends read as mandrel-bent stainless rather than chained cylinders.
    """
    parts = []
    bore_x = (490.0, 613.0, 736.0, 859.0)     # cylinder centrelines
    y_port, z_port = -232.0, 680.0            # head exhaust-face port
    col = (820.0, -360.0, 430.0)              # 4-1 merge point
    prim_r = 21.0

    # four primary tubes, each kept in its own lane and entering the collector
    # mouth at a DISTINCT position (left/upper/lower/right) so they merge into the
    # cone instead of blobbing through one another.
    # spread the entries around the mouth (mostly in z) but keep them INBOARD of
    # the front strut tower that sits just outboard on the exhaust side
    merge = [(-24, 8), (-9, 26), (9, -26), (24, -8)]   # (dy, dz) around the mouth
    for i, bx in enumerate(bore_x):
        dy, dz = merge[i]
        end = (col[0], col[1] + dy, col[2] + dz)
        path = [
            (bx, y_port, z_port),
            (bx + 8, y_port - 64, z_port - 72),
            ((bx + col[0]) / 2.0, -332.0 + dy * 0.6, (z_port + col[2]) / 2.0 - 20 + dz * 0.4),
            (col[0] - 30, end[1], end[2]),
            end,
        ]
        parts.append((C.tube_path(path, prim_r), C.EXHAUST_C, f"PRT_Exhaust_Primary_{i+1}"))

    # tapered 4-into-1 collector
    collector = C.tube_path([col, (980, -342, 404), (1086, -300, 372)],
                            [48, 36, 30])
    parts.append((collector, C.STEEL, "PRT_Exhaust_Collector"))

    # under-floor mid/down pipe  -  drops from the collector to BELOW the floorpan
    # (floor top z220; corridor z<215) before the cabin floor begins (x1220), then
    # runs aft under the floor.  Was routed at z258-372 -> straight through the
    # carpet (199cc); now it clears the floor.
    midpipe_path = [(1086, -300, 372), (1150, -298, 244), (1208, -294, 176),
                    (2100, -260, 172), (2850, -150, 174),
                    (3260, -120, 176), (3680, -300, 198)]
    midpipe = C.swept_tube(midpipe_path, 26.0)
    parts.append((midpipe, C.STEEL, "PRT_Exhaust_Mid_Pipe"))

    # rear silencer / muffler box
    muffler = C.rbox(3700, -378, 196, 400, 236, 152, 44)
    parts.append((muffler, C.STEEL, "PRT_Exhaust_Muffler"))

    # twin chrome tailpipe tips pass through the rear bumper exhaust relief.
    for k, ty in enumerate((-332.0, -260.0)):
        tip = C.cyl(34, 336, (4096, ty, 250), (1, 0, 0)).cut(
              C.cyl(28, 340, (4094, ty, 250), (1, 0, 0)))
        parts.append((tip, C.CHROME, f"PRT_Exhaust_Tip_{k+1}"))

    return parts


# ------------------------------------------------------------------------
#  4.  PRT_ManualGearbox_265_Transmission
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_exhaust_system())
    return out
