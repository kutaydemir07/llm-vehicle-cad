"""Glazing: windshield, backlight and side glass, named by position.

Each pane is carved from the same thin greenhouse skin that cuts the body DLO,
then detailed as a real installed glazing component: eased glass edges,
bonded/frit witness grooves, side run channels, and heated rear-window traces.
The six named panes are kept as the atomic BOM surface for ASM_10500.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C


def _cut_many(solid, cutters):
    out = solid
    for cutter in cutters:
        try:
            out = out.cut(cutter)
        except Exception:
            continue
    return out


def _soften(solid):
    return C.fillet_edges(solid, 1.2)


def _windshield_detail(solid):
    edge_grooves = [
        C.xz_prism([(1518, 1040), (1604, 1040), (1608, 1052), (1522, 1052)], -606, 606),
        C.xz_prism([(1694, 1337), (1782, 1337), (1786, 1349), (1698, 1349)], -596, 596),
        C.xz_prism([(1518, 1048), (1782, 1340), (1774, 1350), (1510, 1058)], 598, 618),
        C.xz_prism([(1518, 1048), (1782, 1340), (1774, 1350), (1510, 1058)], -618, -598),
    ]
    return _soften(_cut_many(solid, edge_grooves))


def _backlight_detail(solid):
    edge_grooves = [
        C.xz_prism([(3120, 1064), (3222, 1064), (3217, 1076), (3115, 1076)], -612, 612),
        C.xz_prism([(2760, 1338), (2862, 1338), (2857, 1350), (2755, 1350)], -604, 604),
        C.xz_prism([(3120, 1070), (2760, 1342), (2750, 1336), (3110, 1064)], 606, 624),
        C.xz_prism([(3120, 1070), (2760, 1342), (2750, 1336), (3110, 1064)], -624, -606),
    ]
    heater_lines = []
    for z in (1100, 1130, 1160, 1190, 1220, 1250, 1280, 1310):
        f = (z - 1052.0) / (1358.0 - 1052.0)
        x0 = 3140.0 + (2740.0 - 3140.0) * f + 36.0
        heater_lines.append(C.xz_prism([(x0, z), (x0 + 32, z), (x0 + 32, z + 3), (x0, z + 3)], -548, 548))
    return _soften(_cut_many(solid, edge_grooves + heater_lines))


def _side_detail(solid, side, quarter=False):
    y0, y1 = (748, 786) if side == "L" else (-786, -748)
    if quarter:
        profile = [(2550, 1046), (2706, 1046), (2704, 1058), (2550, 1058)]
        top = [(2552, 1316), (2696, 1292), (2694, 1304), (2552, 1328)]
        front = [(2550, 1046), (2556, 1326), (2544, 1326), (2538, 1046)]
        rear = [(2710, 1046), (2696, 1298), (2686, 1296), (2700, 1046)]
        grooves = [
            C.xz_prism(profile, y0, y1),
            C.xz_prism(top, y0, y1),
            C.xz_prism(front, y0, y1),
            C.xz_prism(rear, y0, y1),
        ]
    else:
        belt = [(1872, 1046), (2420, 1046), (2420, 1058), (1872, 1058)]
        top = [(1908, 1332), (2420, 1338), (2420, 1350), (1908, 1344)]
        front_run = [(1860, 1046), (1908, 1338), (1898, 1340), (1850, 1048)]
        rear_run = [(2430, 1044), (2430, 1346), (2418, 1346), (2418, 1044)]
        grooves = [
            C.xz_prism(belt, y0, y1),
            C.xz_prism(top, y0, y1),
            C.xz_prism(front_run, y0, y1),
            C.xz_prism(rear_run, y0, y1),
        ]
    return _soften(_cut_many(solid, grooves))


def _detail_pane(solid, name):
    if name == "windshield":
        return _windshield_detail(solid)
    if name == "backlight":
        return _backlight_detail(solid)
    if name.startswith("door_glass_"):
        return _side_detail(solid, name[-1], quarter=False)
    if name.startswith("quarter_glass_"):
        return _side_detail(solid, name[-1], quarter=True)
    return _soften(solid)


def parts():
    # C.glass_panes() uses the same DLO cutters as the body shell, so each pane
    # stays mated to the aperture instead of being placed by loose coordinates.
    raw = {name: sld for sld, name in C.glass_panes()}
    windshield = _detail_pane(raw["windshield"], "windshield")
    backlight = _detail_pane(raw["backlight"], "backlight")
    door_l = _detail_pane(raw["door_glass_L"], "door_glass_L")
    quarter_l = _detail_pane(raw["quarter_glass_L"], "quarter_glass_L")

    return [
        (windshield, C.GLASS, "windshield"),
        (door_l, C.GLASS, "door_glass_L"),
        (C.mirror_y(door_l), C.GLASS, "door_glass_R"),
        (backlight, C.GLASS, "backlight"),
        (quarter_l, C.GLASS, "quarter_glass_L"),
        (C.mirror_y(quarter_l), C.GLASS, "quarter_glass_R"),
    ]
