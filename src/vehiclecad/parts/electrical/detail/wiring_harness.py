"""Main wiring harness branches as routed electrical solids.

Every route is defined by real vehicle hardpoints rather than a loose line in
space.  The long branches are emitted with the ``PRT_Wiring_`` prefix so the
collision checker treats them as flexible harness/cable paths while exact
clearance is still enforced on the mounted boxes, brackets and terminals.
"""

from __future__ import annotations

from vehiclecad.core.reference import common as C

COL = (0.08, 0.08, 0.08)
COL_CLIP = (0.02, 0.02, 0.022)
COL_RED = (0.72, 0.04, 0.03)
COL_BROWN = (0.30, 0.18, 0.10)

BAT_POS = (3868, -596, 658)
BAT_NEG = (3788, -536, 658)
MAIN_POST = (548, -624, 666)
ALT_STUD = (492, -400, 620)
STARTER = (990, -210, 430)
ECU_CONN = (1210, -476, 676)
FUSEBOX = (1420, 490, 850)


def _clip_set(points, axis="x"):
    clips = []
    for x, y, z in points:
        if axis == "x":
            clips.append(C.rbox(x - 10, y - 6, z - 6, 20, 12, 12, 3))
        elif axis == "y":
            clips.append(C.rbox(x - 6, y - 10, z - 6, 12, 20, 12, 3))
        else:
            clips.append(C.rbox(x - 6, y - 6, z - 10, 12, 12, 20, 3))
    return C.U(clips)


def _harness_parts():
    sw = C.swept_tube
    return [
        (
            sw([BAT_POS, (3840, -682, 556), (3420, -704, 470),
                (2320, -704, 304), (1240, -704, 318), (760, -660, 520), MAIN_POST], 7),
            COL_RED,
            "PRT_Wiring_Battery_Positive_Cable",
        ),
        (
            sw([BAT_NEG, (3764, -648, 624), (3724, -674, 584)], 6),
            COL_BROWN,
            "PRT_Wiring_Battery_Negative_Ground",
        ),
        (
            sw([MAIN_POST, (610, -602, 650), (850, -360, 520), STARTER], 5),
            COL_RED,
            "PRT_Wiring_Starter_Main_Cable",
        ),
        (
            sw([MAIN_POST, (530, -540, 654), ALT_STUD], 4),
            COL_RED,
            "PRT_Wiring_Alternator_Charge_Lead",
        ),
        (
            sw([ECU_CONN, (1110, -430, 704), (900, -300, 720), (620, -220, 690),
                (520, -180, 760), (455, 80, 790)], 4),
            COL,
            "PRT_Wiring_Engine_Sensor_Loom",
        ),
        (
            sw([ECU_CONN, (1218, -160, 700), (1280, 0, 830), FUSEBOX], 4),
            COL,
            "PRT_Wiring_ECU_To_Fusebox_Loom",
        ),
        (
            sw([(1218, -160, 700), (700, -470, 720), (330, -585, 620),
                (210, -250, 620), (210, 250, 620), (330, 585, 620)], 4),
            COL,
            "PRT_Wiring_Front_Lighting_Loom",
        ),
        (
            sw([(1220, 740, 320), (2000, 760, 300), (3140, 736, 330),
                (3450, 700, 520), (4230, 650, 610)], 4),
            COL,
            "PRT_Wiring_Body_Loom_Left",
        ),
        (
            sw([(1220, -740, 320), (2000, -760, 300), (3140, -736, 330),
                (3450, -700, 520), (4230, -650, 610)], 4),
            COL,
            "PRT_Wiring_Body_Loom_Right",
        ),
        (
            sw([FUSEBOX, (1490, 260, 860), (1490, 0, 870), (1490, -300, 858),
                (1390, -500, 820)], 4),
            COL,
            "PRT_Wiring_Instrument_Loom",
        ),
        (
            sw([(3450, 700, 520), (3800, 700, 590), (4230, 650, 610),
                (4230, -650, 610), (3800, -700, 590), (3450, -700, 520)], 3),
            COL,
            "PRT_Wiring_Rear_Lighting_Loom",
        ),
        (
            sw([(1218, -160, 700), (1208, -164, 700)], 22, cap=False),
            COL_CLIP,
            "PRT_Wiring_Firewall_Grommet",
        ),
        (
            _clip_set([(330, -585, 620), (760, -660, 520), (1240, -704, 318),
                       (2320, -704, 304), (3420, -704, 470)], axis="x"),
            COL_CLIP,
            "PRT_Wiring_Right_Side_Clip_Set",
        ),
        (
            _clip_set([(1490, 260, 860), (1490, 0, 870), (1490, -300, 858)], axis="y"),
            COL_CLIP,
            "PRT_Wiring_Dash_Clip_Set",
        ),
    ]


def parts():
    return [(loom, color, name) for loom, color, name in _harness_parts()]
