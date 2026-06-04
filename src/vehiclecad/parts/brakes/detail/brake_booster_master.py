"""ASM_5110_Booster_Master_Cylinder - firewall-mounted brake actuation.

The booster, master cylinder and reservoir are mated on a common X-axis and
kept inboard of the left inner fender.  The master ports line up with the ABS
hydraulic routes owned by ``brake_lines.py``.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

COL = (0.75, 0.75, 0.78)
BRAKE = SK.BRAKES


def _servo_dome():
    """Vacuum booster with firewall plate, studs and hose nipple."""
    x, y, z = BRAKE["booster_centre"]
    shell = C.cyl(62, 92, (x - 46, y, z), (1, 0, 0))
    front = C.cyl(66, 8, (x - 50, y, z), (1, 0, 0))
    rear = C.cyl(66, 10, (x + 42, y, z), (1, 0, 0))
    firewall_plate = C.rbox(x + 56, y - 74, z - 55, 12, 148, 110, 5)
    pushrod_socket = C.cyl(18, 22, (x + 45, y, z), (1, 0, 0))
    vacuum_nipple = C.cyl(8, 34, (x - 10, y + 34, z + 54), (0, 1, 0))
    studs = []
    for dy in (-42, 42):
        for dz in (-32, 32):
            studs.append(C.cyl(5, 18, (x + 60, y + dy, z + dz), (1, 0, 0)))
    return C.U([shell, front, rear, firewall_plate, pushrod_socket, vacuum_nipple] + studs)


def _master_cylinder():
    """Dual-circuit master cylinder with reservoir, ports and mounting flange."""
    bx, by, bz = BRAKE["master_base"]
    rx, _, _ = BRAKE["master_rear"]
    body = C.cyl(22, rx - bx, (bx, by, bz), (1, 0, 0))
    nose = C.cyl(16, 32, (bx - 24, by, bz), (1, 0, 0))
    flange = C.cyl(38, 10, (rx - 5, by, bz), (1, 0, 0))

    rcx, rcy, rcz = BRAKE["reservoir_centre"]
    reservoir = C.rbox(rcx - 48, rcy - 38, rcz - 38, 96, 76, 76, 7)
    cap_l = C.cyl(13, 12, (rcx - 22, rcy, rcz + 39), (0, 0, 1))
    cap_r = C.cyl(13, 12, (rcx + 22, rcy, rcz + 39), (0, 0, 1))
    grommet_l = C.cyl(9, 20, (rcx - 24, rcy, bz + 19), (0, 0, 1))
    grommet_r = C.cyl(9, 20, (rcx + 24, rcy, bz + 19), (0, 0, 1))

    port_front = C.cyl(5, 26, (bx + 48, by - 13, bz + 10), (0, -1, 0))
    port_rear = C.cyl(5, 26, (bx + 94, by - 13, bz - 10), (0, -1, 0))
    flare_nuts = [
        C.cyl(7, 8, (bx + 48, by - 42, bz + 10), (0, -1, 0)),
        C.cyl(7, 8, (bx + 94, by - 42, bz - 10), (0, -1, 0)),
    ]
    return C.U([
        body, nose, flange, reservoir, cap_l, cap_r,
        grommet_l, grommet_r, port_front, port_rear,
    ] + flare_nuts)


def parts():
    return [
        (_servo_dome(),     COL, "PRT_Brake_Servo_Booster"),
        (_master_cylinder(), COL, "PRT_Brake_Master_Cylinder"),
    ]
