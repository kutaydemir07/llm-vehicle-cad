"""ASM_5210_Brake_Hard_Lines - ABS unit, hard lines and corner hose ends."""

from __future__ import annotations

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


COL = (0.80, 0.80, 0.80)
BRAKE = SK.BRAKES


def _fitting(point, axis=(1, 0, 0), r=7):
    return C.cyl(r, 10, point, axis)


def _clip(point):
    x, y, z = point
    return C.rbox(x - 9, y - 5, z - 6, 18, 10, 12, 2)


def _tube(path, radius=3):
    return C.swept_tube(path, radius, cap=True)


def _line_with_clips(path, clips=(), radius=3):
    return C.U([_tube(path, radius)] + [_clip(p) for p in clips])


def _line_parts():
    # start the hard lines at the master flare-nut tips (y315) so they connect at
    # the fittings instead of running through the master body
    master_front = (982, 315, 661)
    master_rear = (1028, 315, 641)
    abs_inlet = BRAKE["abs_inlet"]
    abs_front = BRAKE["abs_outlet_front"]
    abs_rear = BRAKE["abs_outlet_rear"]
    firewall_tee = BRAKE["firewall_tee"]
    rear_tee = BRAKE["rear_tee"]

    master_to_abs = C.U([
        _tube([master_front, (958, 322, 632), abs_inlet], 3),
        _tube([master_rear, (1015, 306, 620), (abs_inlet[0] + 20, abs_inlet[1], abs_inlet[2] - 12)], 3),
        _fitting(master_front, (0, -1, 0)),
        _fitting(master_rear, (0, -1, 0)),
    ])

    abs_to_firewall = _line_with_clips(
        [abs_front, (1122, 312, 592), firewall_tee],
        clips=((1135, 315, 596),),
    )

    front_left = C.U([
        _line_with_clips(
            [firewall_tee, (1140, 350, 520), (955, 425, 455), (820, 545, 370), BRAKE["front_left_caliper"]],
            clips=((1080, 365, 500), (900, 470, 420)),
        ),
        _tube([(820, 545, 370), (870, 620, 342), BRAKE["front_left_caliper"]], 5),
        _fitting(BRAKE["front_left_caliper"], (0, 1, 0), 6),
    ])

    front_right = C.U([
        _line_with_clips(
            [abs_front, (1150, 110, 560), (1020, -320, 500), (820, -545, 370), BRAKE["front_right_caliper"]],
            clips=((1135, 80, 548), (930, -410, 435)),
        ),
        _tube([(820, -545, 370), (870, -620, 342), BRAKE["front_right_caliper"]], 5),
        _fitting(BRAKE["front_right_caliper"], (0, -1, 0), 6),
    ])

    rear_main = _line_with_clips(
        [abs_rear, (1135, 210, 470), (1270, 90, 310), (1850, 38, 282),
         (2700, 22, 265), rear_tee],
        clips=((1280, 92, 310), (2050, 35, 280), (2860, 18, 264)),
    )

    rear_left = C.U([
        _line_with_clips(
            [rear_tee, (3330, 180, 258), (3400, 520, 292), BRAKE["rear_left_caliper"]],
            clips=((3340, 180, 258),),
        ),
        _tube([(3400, 520, 292), (3440, 630, 310), BRAKE["rear_left_caliper"]], 5),
        _fitting(BRAKE["rear_left_caliper"], (0, 1, 0), 6),
    ])

    rear_right = C.U([
        _line_with_clips(
            [rear_tee, (3330, -180, 258), (3400, -520, 292), BRAKE["rear_right_caliper"]],
            clips=((3340, -180, 258),),
        ),
        _tube([(3400, -520, 292), (3440, -630, 310), BRAKE["rear_right_caliper"]], 5),
        _fitting(BRAKE["rear_right_caliper"], (0, -1, 0), 6),
    ])

    return [
        (master_to_abs, "PRT_Brake_Line_Master_To_ABS_Modulator"),
        (abs_to_firewall, "PRT_Brake_Line_ABS_To_Firewall_Tee"),
        (front_left, "PRT_Brake_Line_Front_Left"),
        (front_right, "PRT_Brake_Line_Front_Right"),
        (rear_main, "PRT_Brake_Line_Rear_Main"),
        (rear_left, "PRT_Brake_Line_Rear_Left"),
        (rear_right, "PRT_Brake_Line_Rear_Right"),
    ]


def _abs_modulator():
    """Rubber-isolated ABS hydraulic unit with pump, valve caps and pipe ports."""
    x, y, z = BRAKE["abs_unit"]
    block = C.rbox(x - 56, y - 36, z - 37, 112, 72, 74, 6)
    bracket = C.rbox(x - 66, y - 48, z - 51, 132, 12, 26, 3)
    pump = C.cyl(18, 88, (x - 38, y - 44, z - 2), (0, 1, 0))
    ports = [
        C.cyl(6, 14, (x + 36, y + 38, z + 22), (0, 1, 0)),
        C.cyl(6, 14, (x + 36, y + 38, z + 2), (0, 1, 0)),
        C.cyl(6, 14, (x + 36, y + 38, z - 18), (0, 1, 0)),
    ]
    solenoids = [
        C.cyl(8, 28, (x - 36 + i * 24, y - 22, z + 36), (0, 0, 1))
        for i in range(4)
    ]
    mounts = [
        C.cyl(8, 12, (x - 44, y - 54, z - 38), (0, 1, 0)),
        C.cyl(8, 12, (x + 44, y - 54, z - 38), (0, 1, 0)),
    ]
    return C.U([block, bracket, pump] + ports + solenoids + mounts)


def parts():
    return [(_abs_modulator(), COL, "PRT_ABS_Hydraulic_Modulator")] + [
        (line, COL, name) for line, name in _line_parts()
    ]
