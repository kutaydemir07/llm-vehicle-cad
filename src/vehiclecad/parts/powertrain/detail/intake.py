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


def _intake_itb() -> list:
    """Individual Throttle Body (ITB) intake  -  the I4_Engine's defining feature.

    No shared plenum: each cylinder gets its own curved runner  -  throttle-body
    barrel (with a butterfly plate)  -  flared velocity-stack trumpet.  A fuel rail
    feeds four injectors and a throttle linkage shaft ties the bodies together.
    The whole stack sits on the LEFT (+Y) head face and stays clear of the hood.
    """
    parts = []
    bore_x = (490.0, 613.0, 736.0, 859.0)     # cylinder centrelines (123 mm spacing)
    y_port, z_port = 232.0, 690.0             # head intake-face port
    y_tb           = 332.0                    # throttle-body axis (outboard of head)
    z_tb0, z_tb1   = 716.0, 820.0             # barrel base / stack throat
    tb_r           = 25.0

    # manifold flange bolted ON the head intake face (y230), bored at each port so
    # the runners pass through in clearance instead of jamming into the plate
    flange = C.rbox(470, 230, 660, 410, 30, 62, 6).cut(
        C.U([C.cyl(30, 40, (bx, 226, 694), (0, 1, 0)) for bx in bore_x]))
    parts.append((flange, C.ALLOY_E, "PRT_Intake_Head_Flange"))

    for i, bx in enumerate(bore_x):
        # curved runner: head port -> throttle-body base, BORED HOLLOW (5 mm
        # wall) so the intake tract is a real open duct, not a solid slug
        path = [
            (bx, y_port, z_port),
            (bx, (y_port + y_tb) / 2.0, z_port + 16),
            (bx, y_tb, z_tb0),
        ]
        runner = C.tube_path(path, [tb_r + 3, tb_r + 3, tb_r]).cut(
            C.tube_path([(bx, y_port - 4, z_port - 2),
                         path[1], (bx, y_tb, z_tb0 + 4)],
                        [tb_r - 2, tb_r - 2, tb_r - 5]))
        parts.append((runner, C.ALLOY_E, f"PRT_ITB_Runner_{i+1}"))

        # throttle-body barrel: BORED, with the angled butterfly plate visible
        # in the bore and the throttle-shaft bosses crossing it
        barrel = C.cyl(tb_r, z_tb1 - z_tb0, (bx, y_tb, z_tb0), (0, 0, 1)).cut(
            C.cyl(tb_r - 4, z_tb1 - z_tb0 + 8, (bx, y_tb, z_tb0 - 4), (0, 0, 1)))
        plate = C.cyl(tb_r - 4.5, 3, (bx, y_tb, (z_tb0 + z_tb1) / 2.0), (0.32, 0, 1))
        shaft = C.cyl(4.5, 2 * tb_r + 14, (bx - tb_r - 7, y_tb, (z_tb0 + z_tb1) / 2.0), (1, 0, 0))
        parts.append((C.U([barrel, plate, shaft]), C.ALLOY_E, f"PRT_Throttle_Body_{i+1}"))

        # flared velocity-stack trumpet -- a HOLLOW horn with a rolled lip
        stack = C.bellmouth((bx, y_tb, z_tb1), (0, 0, 1), tb_r, tb_r + 16, 36).cut(
            C.bellmouth((bx, y_tb, z_tb1 - 2), (0, 0, 1), tb_r - 4, tb_r + 12, 40))
        parts.append((stack, C.ALLOY_E, f"PRT_Velocity_Stack_{i+1}"))

        # fuel injector dropping from the rail into the runner
        inj = C.tube_path([(bx, 300, 770), (bx, 320, 726)], 6.0)
        parts.append((inj, C.BLACK, f"PRT_Injector_{i+1}"))

    # fuel rail spanning the four injectors: extruded spine with injector
    # bosses, an inlet banjo at the front and the pressure-regulator end cap
    rail = C.cyl(12, 420, (462, 300, 770), (1, 0, 0))
    bosses = [C.cyl(9, 16, (bx, 304, 758), (0, 0.22, 1)) for bx in bore_x]
    banjo = C.cyl(9, 18, (456, 300, 770), (1, 0, 0))
    reg = C.cyl(15, 22, (882, 300, 770), (1, 0, 0))
    reg_vac = C.cyl(4, 14, (904, 300, 770), (1, 0, 0))
    rail = C.U([rail, banjo, reg, reg_vac] + bosses)
    parts.append((rail, (0.62, 0.63, 0.66), "PRT_Fuel_Rail"))

    # throttle linkage shaft + bellcrank levers tying the four bodies together
    link = C.cyl(5, 430, (458, 360, 768), (1, 0, 0))
    levers = [C.rbox(bx - 4, 348, z_tb0 + 20, 8, 26, 30, 3) for bx in bore_x]
    parts.append((C.U([link] + levers), C.STEEL, "PRT_Throttle_Linkage"))

    return parts


# ------------------------------------------------------------------------
#  3.  PRT_Exhaust_Manifold_Tubular
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_intake_itb())
    return out
