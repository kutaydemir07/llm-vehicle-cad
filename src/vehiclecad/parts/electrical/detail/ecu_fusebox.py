"""ECU, fuse and relay details for ASM_8000 electrical.

The module is packaged as mounted electrical hardware, not floating boxes:

* Motronic ECU on a small right-side engine-bay bracket;
* connector banks pointing toward the engine harness;
* under-dash fuse/relay carrier with cover, fuses and relays;
* front main junction post and fusible-link block connected to the rear battery.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL_CASE = (0.14, 0.18, 0.22)
COL_COVER = (0.07, 0.09, 0.11)
COL_RELAY = (0.05, 0.06, 0.07)
COL_FUSE = (0.78, 0.18, 0.12)
COL_BRACKET = C.STEEL
COL_COPPER = (0.84, 0.48, 0.18)


def _ecu():
    # 90 mm forward of the frame-rail tower leg (leg occupies x1176..1216 at
    # this height) on the right apron, clear of the strut tower (x<=930)
    return C.rbox(990, -520, 650, 100, 100, 54, 5)


def _ecu_bracket():
    tray = C.rbox(984, -526, 642, 112, 112, 6, 3)
    rear_tab = C.rbox(984, -526, 642, 8, 112, 64, 3)
    isolators = [
        C.cyl(5, 6, (1002, -506, 648), (0, 0, 1)),
        C.cyl(5, 6, (1078, -506, 648), (0, 0, 1)),
        C.cyl(5, 6, (1002, -434, 648), (0, 0, 1)),
        C.cyl(5, 6, (1078, -434, 648), (0, 0, 1)),
    ]
    return C.U([tray, rear_tab, *isolators])


def _ecu_connectors():
    shells = []
    for y in (-508, -484, -460):
        shells.append(C.rbox(1092, y, 662, 22, 16, 28, 3))
        shells.append(C.cyl(3, 10, (1114, y + 8, 676), (1, 0, 0)))
    loom_boot = C.rbox(1108, -510, 658, 16, 66, 38, 5)
    return C.U([*shells, loom_boot])


def _fusebox_base():
    return C.rbox(1380, 430, 800, 80, 120, 78, 6)


def _fusebox_cover():
    cover = C.rbox(1378, 428, 878, 84, 124, 8, 4)
    pull_tab = C.rbox(1406, 424, 886, 28, 12, 10, 3)
    return C.U([cover, pull_tab])


def _relay_array():
    relays = []
    for x in (1390, 1414, 1438):
        relays.append(C.rbox(x, 444, 832, 16, 28, 32, 3))
        relays.append(C.rbox(x, 484, 832, 16, 28, 32, 3))
    return C.U(relays)


def _fuse_block():
    fuses = []
    for i in range(6):
        fuses.append(C.rbox(1388 + i * 12, 524, 814, 8, 16, 16, 2))
    bus_bar = C.rbox(1386, 520, 806, 74, 4, 8, 1)
    return C.U([bus_bar, *fuses])


def _fusebox_mounting_bracket():
    rear_plate = C.rbox(1376, 422, 794, 88, 6, 96, 2)
    lower_flange = C.rbox(1376, 422, 794, 88, 130, 6, 2)
    return C.U([rear_plate, lower_flange])


def _main_junction_post():
    base = C.rbox(524, -648, 612, 50, 48, 8, 3)
    insulator = C.cyl(12, 18, (548, -624, 620), (0, 0, 1))
    stud = C.cyl(6, 28, (548, -624, 638), (0, 0, 1))
    cap = C.rbox(532, -638, 656, 32, 28, 22, 5)
    return C.U([base, insulator, stud, cap])


def _fusible_link_block():
    block = C.rbox(582, -648, 626, 54, 34, 24, 4)
    window = C.rbox(590, -650, 634, 38, 6, 8, 1)
    feed_studs = [
        C.cyl(4, 12, (596, -614, 638), (0, 1, 0)),
        C.cyl(4, 12, (622, -614, 638), (0, 1, 0)),
    ]
    return C.U([block, window, *feed_studs])


def parts():
    return [
        (_ecu(),                    COL_CASE,    "PRT_ECU_Motronic"),
        (_ecu_bracket(),            COL_BRACKET, "PRT_ECU_Mounting_Bracket"),
        (_ecu_connectors(),         COL_COVER,   "PRT_ECU_Connector_Set"),
        (_fusebox_base(),           COL_CASE,    "PRT_Fuse_Relay_Box"),
        (_fusebox_cover(),          COL_COVER,   "PRT_Fuse_Relay_Box_Cover"),
        (_relay_array(),            COL_RELAY,   "PRT_Relay_Array"),
        (_fuse_block(),             COL_FUSE,    "PRT_Fuse_Block"),
        (_fusebox_mounting_bracket(), COL_BRACKET, "PRT_Fuse_Relay_Box_Mounting_Bracket"),
        (_main_junction_post(),     COL_COPPER,  "PRT_Battery_Main_Junction_Post"),
        (_fusible_link_block(),     COL_COPPER,  "PRT_Fusible_Link_Block"),
    ]
