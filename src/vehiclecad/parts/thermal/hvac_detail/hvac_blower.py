"""ASM_7210 cabin HVAC case, blower and air-distribution ducts.

The module is drawn as a real heater/ventilation assembly mounted to the cabin
side of the firewall.  It stays below the dashboard shell, uses a side-mounted
centrifugal blower, leaves a serviceable heater-core pocket, and routes ducts to
the centre vents, demist outlets and footwells.
"""
from __future__ import annotations
import math
from vehiclecad.core.reference import common as C

COL_HVAC  = (0.18, 0.20, 0.22)
COL_BLEND = (0.30, 0.30, 0.32)
COL_CORE = C.ALLOY_E
COL_FOAM = C.RUBBER
COL_CABLE = (0.05, 0.05, 0.055)


def _heater_box():
    """Moulded heater case with a cut pocket for the removable heater core."""
    case = C.rbox(1242, -244, 552, 206, 488, 206, 12)
    core_clearance = C.rbox(1282, -182, 610, 104, 364, 96, 6)
    blower_port = C.cyl(62, 46, (1240, -254, 680), (0, -1, 0))
    scroll_clearance = C.cyl(66, 80, (1284, -215, 675), (1, 0, 0))
    centre_port = C.cyl(24, 48, (1406, 0, 750), (0.35, 0, 1))
    return case.cut(core_clearance).cut(blower_port).cut(scroll_clearance).cut(centre_port)


def _heater_core():
    """Copper/aluminium heater matrix sitting inside the service pocket."""
    core = C.rbox(1288, -170, 620, 82, 340, 76, 4)
    fins = [C.box(1290, -160 + i * 22, 622, 3, 2, 72) for i in range(15)]
    inlet = C.cyl(8, 34, (1226, 246, 674), (1, 0, 0))
    outlet = C.cyl(8, 34, (1226, 274, 646), (1, 0, 0))
    return C.U([core, inlet, outlet] + fins)


def _blower_scroll():
    """Passenger-side centrifugal scroll housing, outside the main heater case."""
    scroll = C.cyl(58, 54, (1290, -215, 675), (1, 0, 0))
    outlet = C.rbox(1258, -284, 654, 62, 44, 48, 8)
    return scroll.fuse(outlet)


def _blower_motor():
    """DC blower motor as the recognisable component: finned can, domed brush
    end-bell with terminal spades, mounting flange ring, and the shaft stub
    into the scroll."""
    motor = C.cyl(30, 54, (1304, -215, 675), (1, 0, 0))
    for k in range(8):
        fin = C.box(1308, -216.5, 705, 44, 3, 3)
        motor = motor.fuse(fin.rotate((1304, -215, 675), (1305, -215, 675),
                                      k * 45.0))
    end_bell = C.loft_circles([
        ((1358, -215, 675), 28, (1, 0, 0)),
        ((1366, -215, 675), 22, (1, 0, 0)),
        ((1372, -215, 675), 12, (1, 0, 0)),
    ])
    terminals = C.U([C.box(1370, -212 + dy, 668, 8, 3, 8) for dy in (-8, 2)])
    flange = C.cyl(36, 5, (1304, -215, 675), (1, 0, 0)).cut(
        C.cyl(31, 9, (1302, -215, 675), (1, 0, 0)))
    shaft = C.cyl(5, 12, (1294, -215, 675), (1, 0, 0))
    return C.U([motor, end_bell, terminals, flange, shaft])


def _fresh_air_plenum():
    plenum = C.rbox(1228, -300, 770, 128, 600, 48, 10)
    flap = C.rbox(1260, -238, 784, 42, 476, 8, 2)
    return plenum.fuse(flap)


def _centre_duct():
    return C.tube_path([
        (1400, 0, 748),
        (1450, 0, 820),
        (1490, 0, 888),
    ], [20, 22, 18])


def _demist_duct(side):
    s = 1 if side == "L" else -1
    return C.tube_path([
        (1378, s * 80, 744),
        (1428, s * 220, 842),
        (1490, s * 330, 930),
    ], [15, 16, 13])


def _footwell_duct(side):
    s = 1 if side == "L" else -1
    y_mid = 318 if side == "L" else -270
    return C.tube_path([
        (1372, s * 110, 600),
        (1420, y_mid, 540),
        (1460, y_mid, 468),
    ], [14, 16, 14])


def _firewall_gasket():
    gasket = C.rbox(1222, 220, 622, 12, 72, 72, 5)
    feed_hole = C.cyl(14, 20, (1218, 246, 674), (1, 0, 0))
    return_hole = C.cyl(14, 20, (1218, 274, 646), (1, 0, 0))
    return gasket.cut(feed_hole).cut(return_hole)


def _control_cables():
    cables = [
        C.tube_path([(1408, -96, 728), (1470, -86, 784), (1542, -72, 824)], 3),
        C.tube_path([(1408, -64, 704), (1476, -28, 766), (1544, 34, 812)], 3),
        C.tube_path([(1408, 40, 692), (1478, 82, 758), (1542, 128, 804)], 3),
    ]
    return C.U(cables)


def parts():
    return [
        (_heater_box(), COL_HVAC, "PRT_HVAC_Heater_Box"),
        (_heater_core(), COL_CORE, "PRT_HVAC_Heater_Core"),
        (_blower_scroll(), COL_BLEND, "PRT_HVAC_Blower_Scroll"),
        (_blower_motor(), COL_BLEND, "PRT_HVAC_Blower_Motor"),
        (_fresh_air_plenum(), COL_HVAC, "PRT_HVAC_Fresh_Air_Plenum"),
        (_centre_duct(), COL_HVAC, "PRT_HVAC_Centre_Duct"),
        (_demist_duct("L"), COL_HVAC, "PRT_HVAC_Demist_Duct_L"),
        (_demist_duct("R"), COL_HVAC, "PRT_HVAC_Demist_Duct_R"),
        (_footwell_duct("L"), COL_HVAC, "PRT_HVAC_Footwell_Duct_L"),
        (_footwell_duct("R"), COL_HVAC, "PRT_HVAC_Footwell_Duct_R"),
        (_firewall_gasket(), COL_FOAM, "PRT_HVAC_Firewall_Foam_Gasket"),
        (_control_cables(), COL_CABLE, "PRT_HVAC_Control_Cable_Set"),
    ]
