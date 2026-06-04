"""Battery storage and alternator package for ASM_8000 electrical.

The E30-style power package is modeled as a real CAD layout instead of a single
generic electrical block:

* battery on a raised tray in the right rear boot, clear of the spare well and
  rear wheel tub;
* hold-down, terminals, vent/ground routing and front main power post;
* Bosch-style alternator with separate pulley, brackets and B+ output stud on
  the right side of the inline-four accessory plane.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL_BAT = (0.12, 0.16, 0.20)
COL_RUBBER = (0.03, 0.03, 0.035)
COL_COPPER = (0.84, 0.48, 0.18)
COL_PLATED = (0.78, 0.78, 0.70)
COL_ALT = C.ALLOY_E
COL_STEEL = C.STEEL

BAT_POS = (3868, -596, 636)
BAT_NEG = (3788, -536, 636)
MAIN_POST = (548, -624, 620)
ALT_AXIS = (450, -500, 596)


def _battery_case():
    """DIN-size rear battery case, sitting just above the boot-floor tray."""
    case = C.rbox(3720, -620, 476, 210, 120, 160, 9)
    top_lip = C.rbox(3716, -624, 630, 218, 128, 8, 4)
    return C.U([case, top_lip])


def _battery_tray():
    """Pressed tray clears the boot floor (z=452..466) by 2 mm."""
    tray = C.rbox(3710, -632, 468, 230, 144, 8, 4)
    inboard_flange = C.rbox(3710, -492, 468, 230, 8, 32, 3)
    rear_flange = C.rbox(3932, -632, 468, 8, 144, 32, 3)
    return C.U([tray, inboard_flange, rear_flange])


def _battery_hold_down():
    cross_bar = C.rbox(3740, -626, 640, 170, 10, 8, 3)
    hook_front = C.cyl(4, 168, (3750, -621, 476), (0, 0, 1))
    hook_rear = C.cyl(4, 168, (3900, -621, 476), (0, 0, 1))
    nuts = [
        C.cyl(9, 5, (3750, -621, 644), (0, 0, 1)),
        C.cyl(9, 5, (3900, -621, 644), (0, 0, 1)),
    ]
    return C.U([cross_bar, hook_front, hook_rear, *nuts])


def _terminal(center, cable_dir=1):
    x, y, z = center
    post = C.cyl(8, 20, (x, y, z), (0, 0, 1))
    clamp = C.rbox(x - 16, y - 11, z + 10, 32, 22, 12, 3)
    lug = C.cyl(7, 28, (x + 10 * cable_dir, y, z + 16), (cable_dir, 0, 0))
    return C.U([post, clamp, lug])


def _battery_ground_strap():
    # Flexible routing starts at the negative terminal and lands on the boot side.
    return C.swept_tube([(BAT_NEG[0], BAT_NEG[1], BAT_NEG[2] + 22),
                         (3764, -648, 624),
                         (3724, -674, 584)], 6)


def _battery_vent_tube():
    return C.swept_tube([(3928, -558, 602), (3960, -660, 588), (4018, -676, 560)], 3)


def _main_power_post():
    base = C.rbox(524, -648, 612, 50, 48, 8, 3)
    insulator = C.cyl(12, 18, (548, -624, 620), (0, 0, 1))
    stud = C.cyl(6, 28, (548, -624, 638), (0, 0, 1))
    protective_cap = C.rbox(532, -638, 656, 32, 28, 22, 5)
    return C.U([base, insulator, stud, protective_cap])


def _alternator_body():
    """Bosch-style alternator body centered on the accessory plane."""
    body = C.cyl(54, 86, ALT_AXIS, (0, 1, 0))
    rear_cap = C.cyl(42, 10, (450, -420, 596), (0, 1, 0))
    stator_band = C.cyl(56, 10, (450, -468, 596), (0, 1, 0))
    return C.U([body, rear_cap, stator_band])


def _alternator_pulley():
    pulley = C.cyl(32, 16, (450, -514, 596), (0, 1, 0))
    groove = C.cyl(15, 22, (448, -517, 594), (0, 1, 0))
    hub = C.cyl(12, 24, (450, -526, 596), (0, 1, 0))
    return C.U([pulley.cut(groove), hub])


def _alternator_mounting_bracket():
    lower_ear = C.rbox(416, -506, 568, 22, 78, 18, 5)
    upper_ear = C.rbox(418, -506, 620, 18, 68, 16, 4)
    block_link = C.swept_tube([(408, -430, 592), (426, -476, 588), (426, -506, 588)], 8)
    return C.U([lower_ear, upper_ear, block_link])


def _alternator_adjuster_brace():
    slot_bar = C.rbox(396, -506, 654, 100, 12, 10, 4)
    adjuster_bolt = C.cyl(5, 26, (456, -516, 659), (0, 1, 0))
    engine_pivot = C.cyl(7, 18, (402, -506, 659), (0, 1, 0))
    return C.U([slot_bar, adjuster_bolt, engine_pivot])


def _alternator_output_stud():
    stud = C.cyl(6, 24, (492, -424, 620), (0, 1, 0))
    nut = C.cyl(10, 5, (492, -400, 620), (0, 1, 0))
    boot = C.rbox(482, -414, 610, 20, 20, 20, 4)
    return C.U([stud, nut, boot])


def parts():
    return [
        (_battery_case(),                COL_BAT,    "PRT_Battery"),
        (_battery_tray(),                COL_STEEL,  "PRT_Battery_Tray"),
        (_battery_hold_down(),           COL_STEEL,  "PRT_Battery_Hold_Down"),
        (_terminal(BAT_POS, 1),          COL_COPPER, "PRT_Battery_Terminal_Positive"),
        (_terminal(BAT_NEG, -1),         COL_PLATED, "PRT_Battery_Terminal_Negative"),
        (_battery_ground_strap(),        COL_COPPER, "PRT_Wiring_Battery_Ground_Strap"),
        (_battery_vent_tube(),           COL_RUBBER, "PRT_Wiring_Battery_Vent_Tube"),
        (_alternator_body(),             COL_ALT,    "PRT_Alternator"),
        (_alternator_pulley(),           COL_STEEL,  "PRT_Alternator_Pulley"),
        (_alternator_mounting_bracket(), COL_STEEL,  "PRT_Alternator_Mounting_Bracket"),
        (_alternator_adjuster_brace(),   COL_STEEL,  "PRT_Alternator_Adjuster_Brace"),
        (_alternator_output_stud(),      COL_COPPER, "PRT_Alternator_Output_Stud"),
    ]
