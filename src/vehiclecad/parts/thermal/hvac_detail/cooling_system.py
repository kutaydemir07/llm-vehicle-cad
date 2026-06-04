"""ASM_7110 radiator, fan, expansion tank, heater valve and coolant hoses.

The ModelA-style cooling package is treated like a real CAD module: the radiator
hangs in the front core-support opening, the fan lives in the air gap behind it,
the expansion tank is mounted in the left-front bay corner, and each hose has a
clear swept route to a functional coolant port instead of cutting through the
engine block.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

_box  = C.box
_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.ALLOY_E
STEEL = C.STEEL
RUBBER = C.RUBBER
PLASTIC = (0.08, 0.09, 0.10)
FASTENER = (0.13, 0.13, 0.14)

RAD_X0 = 176.0
RAD_Y0 = -320.0
RAD_Z0 = 430.0
RAD_CY = 0.0
RAD_CZ = 615.0
FAN_X = 272.0


def _radiator():
    """Aluminium cross-flow radiator with visible fin pack and end tanks."""
    core = _rbox(RAD_X0 + 18, -300, 448, 58, 600, 322, 4)
    fins = []
    for i in range(15):
        z = 462 + i * 20
        fins.append(_box(RAD_X0 + 10, -292, z, 6, 584, 3))
    tank_l = _rbox(RAD_X0 + 4, -348, 438, 28, 42, 344, 8)
    tank_r = _rbox(RAD_X0 + 4, 306, 438, 28, 42, 344, 8)
    top_hdr = _rbox(RAD_X0 + 4, -306, 774, 86, 612, 18, 5)
    bot_hdr = _rbox(RAD_X0 + 4, -306, 430, 86, 612, 18, 5)
    filler_neck = _cyl(13, 14, (RAD_X0 + 46, 286, 774), (0, 0, 1))
    upper_neck = _cyl(16, 34, (RAD_X0 + 80, 286, 748), (0, 1, 0))
    lower_neck = _cyl(15, 34, (RAD_X0 + 80, -286, 454), (0, -1, 0))
    return _U([core, tank_l, tank_r, top_hdr, bot_hdr, filler_neck, upper_neck, lower_neck] + fins)


def _radiator_mount_brackets():
    """Stamped upper/lower straps that sit just aft of the core support."""
    brackets = []
    for y in (-330, 330):
        brackets.append(_rbox(222, y - 18, 420, 18, 36, 58, 4))
        brackets.append(_rbox(222, y - 18, 772, 18, 36, 46, 4))
    return _U(brackets)


def _radiator_isolators():
    pads = []
    for y in (-332, 332):
        pads.append(_cyl(10, 10, (240, y, 438), (1, 0, 0)))
        pads.append(_cyl(9, 10, (240, y, 790), (1, 0, 0)))
    return _U(pads)


def _fan_shroud():
    """Plastic shroud ring with a real circular blade opening."""
    shell = _rbox(246, -286, 442, 24, 572, 346, 8)
    aperture = _cyl(178, 42, (238, RAD_CY, RAD_CZ), (1, 0, 0))
    ears = []
    for y, z in ((-238, 468), (238, 468), (-238, 760), (238, 760)):
        ears.append(_rbox(260, y - 18, z - 14, 18, 36, 28, 5))
    return _U([shell.cut(aperture)] + ears)


def _fan_blades():
    """Six axial fan blades and hub, centred in the shroud aperture."""
    cx = FAN_X
    blade0 = _rbox(cx, 22, RAD_CZ - 8, 10, 126, 16, 4)
    blades = [
        blade0.rotate((cx, 0, RAD_CZ), (cx + 1, 0, RAD_CZ), i * 60.0)
        for i in range(6)
    ]
    hub = _cyl(34, 12, (cx - 2, 0, RAD_CZ), (1, 0, 0))
    return _U([hub] + blades)


def _fan_motor():
    motor = _cyl(32, 46, (286, 0, RAD_CZ), (1, 0, 0))
    plug = _rbox(326, -10, RAD_CZ + 26, 20, 20, 12, 3)
    return motor.fuse(plug)


def _expansion_tank():
    """Translucent expansion bottle in the left-front engine-bay corner."""
    tank = _rbox(278, 438, 680, 76, 94, 134, 10)
    seam = _rbox(276, 436, 744, 80, 98, 5, 2)
    return tank.fuse(seam)


def _expansion_tank_cap():
    return _cyl(17, 14, (290, 486, 814), (0, 0, 1))


def _coolant_hoses():
    """Hoses routed outside the engine casting, then aimed at coolant ports."""
    upper = C.tube_path([
        (RAD_X0 + 96, 300, 748),
        (292, 276, 772),
        (340, 118, 760),
        (370, -34, 628),
    ], [17, 18, 18, 14])
    lower = C.tube_path([
        (RAD_X0 + 96, -300, 454),
        (292, -286, 430),
        (338, -190, 438),
        (360, 134, 486),
    ], [16, 17, 17, 14])
    bleed = C.tube_path([
        (222, 300, 786),
        (248, 390, 810),
        (286, 486, 828),
    ], 5)
    heater_feed = C.tube_path([
        (972, 264, 724),
        (1060, 250, 720),
        (1162, 232, 704),
    ], 10)
    heater_return = C.tube_path([
        (930, 244, 704),
        (1045, 248, 700),
        (1162, 246, 674),
    ], 10)
    return [
        (upper, "PRT_Coolant_Hose_Upper_Radiator"),
        (lower, "PRT_Coolant_Hose_Lower_Radiator"),
        (bleed, "PRT_Coolant_Hose_Expansion_Bleed"),
        (heater_feed, "PRT_Coolant_Hose_Heater_Feed"),
        (heater_return, "PRT_Coolant_Hose_Heater_Return"),
    ]


def _heater_control_valve():
    body = _rbox(1170, 172, 642, 42, 110, 78, 7)
    feed_stub = _cyl(11, 22, (1160, 232, 704), (1, 0, 0))
    return_stub = _cyl(11, 22, (1160, 246, 674), (1, 0, 0))
    firewall_stubs = [
        _cyl(9, 20, (1192, 246, 674), (1, 0, 0)),
        _cyl(9, 20, (1192, 274, 646), (1, 0, 0)),
    ]
    return _U([body, feed_stub, return_stub] + firewall_stubs)


def _radiator_drain_plug():
    return _cyl(7, 14, (RAD_X0 + 70, -340, 436), (0, -1, 0))


def parts():
    out = [
        (_radiator(), COL, "PRT_Radiator"),
        (_radiator_mount_brackets(), STEEL, "PRT_Radiator_Mount_Brackets"),
        (_radiator_isolators(), RUBBER, "PRT_Radiator_Rubber_Isolators"),
        (_fan_shroud(), PLASTIC, "PRT_Radiator_Fan_Shroud"),
        (_fan_blades(), STEEL, "PRT_Radiator_Fan_Blades"),
        (_fan_motor(), STEEL, "PRT_Radiator_Fan_Motor"),
        (_expansion_tank(), COL, "PRT_Expansion_Tank"),
        (_expansion_tank_cap(), FASTENER, "PRT_Expansion_Tank_Cap"),
        (_heater_control_valve(), STEEL, "PRT_Heater_Control_Valve"),
        (_radiator_drain_plug(), FASTENER, "PRT_Radiator_Drain_Plug"),
    ]
    for hose, name in _coolant_hoses():
        out.append((hose, RUBBER, name))
    return out

