"""ASM_5310_Lever_And_Cables - tunnel-mounted parking brake assembly."""

from __future__ import annotations

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


COL_LEVER = (0.12, 0.12, 0.14)
COL_CABLE = (0.60, 0.60, 0.62)
BRAKE = SK.BRAKES


def _clip(point):
    x, y, z = point
    return C.rbox(x - 10, y - 5, z - 5, 20, 10, 10, 2)


def _lever():
    """Sloped handbrake lever seated in the console/tunnel bracket."""
    pivot = BRAKE["handbrake_pivot"]
    grip = BRAKE["handbrake_grip"]
    eq = BRAKE["handbrake_equalizer"]

    px, py, pz = pivot
    gx, gy, gz = grip
    base = C.rbox(px - 42, py - 34, pz - 28, 96, 76, 38, 6)
    pivot_tube = C.cyl(14, 78, (px, py - 39, pz), (0, 1, 0))
    lever = C.swept_tube([pivot, (1888, 76, 604), grip], 11, cap=True)
    grip_body = C.rbox(gx - 14, gy - 22, gz - 14, 72, 44, 28, 8)
    release_button = C.cyl(6, 18, (gx + 54, gy, gz), (1, 0, 0))
    ratchet = C.rbox(px - 30, py - 24, pz + 16, 54, 14, 32, 4)
    equalizer = C.rbox(eq[0] - 24, eq[1] - 34, eq[2] - 10, 48, 68, 20, 4)
    pull_link = C.swept_tube([(px + 10, py, pz - 10), (eq[0], eq[1], eq[2])], 6, cap=True)
    return C.U([base, pivot_tube, lever, grip_body, release_button, ratchet, equalizer, pull_link])


def _cable_left():
    eq = BRAKE["handbrake_equalizer"]
    rlc = BRAKE["rear_left_caliper"]
    # start at the equalizer's +Y end (not inside it); end at the caliper PARKING-
    # BRAKE LEVER, offset below/inboard of the hydraulic hose port so the cable
    # and the rear brake line do not share the same corner.
    path = [
        (eq[0], eq[1] + 38, eq[2]),
        (2060, 42, 330),
        (2640, 52, 278),
        (3170, 160, 258),
        (3380, 540, 278),
        (rlc[0] - 18, rlc[1] + 6, rlc[2] - 22),
    ]
    return C.U([
        C.swept_tube(path, 4, cap=True),
        _clip((2240, 44, 314)),
        _clip((2860, 70, 270)),
        _clip((3310, 360, 272)),
    ])


def _cable_right():
    eq = BRAKE["handbrake_equalizer"]
    rrc = BRAKE["rear_right_caliper"]
    path = [
        (eq[0], eq[1] - 38, eq[2]),
        (2060, -42, 330),
        (2640, -52, 278),
        (3170, -160, 258),
        (3380, -540, 278),
        (rrc[0] - 18, rrc[1] - 6, rrc[2] - 22),
    ]
    return C.U([
        C.swept_tube(path, 4, cap=True),
        _clip((2240, -44, 314)),
        _clip((2860, -70, 270)),
        _clip((3310, -360, 272)),
    ])


def parts():
    return [
        (_lever(), COL_LEVER, "PRT_Handbrake_Lever"),
        (_cable_left(), COL_CABLE, "PRT_Handbrake_Cable_Left"),
        (_cable_right(), COL_CABLE, "PRT_Handbrake_Cable_Right"),
    ]
