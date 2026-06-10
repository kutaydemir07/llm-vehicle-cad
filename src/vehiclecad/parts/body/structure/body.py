"""Body-in-white and closures as named sheet-metal panels.

The module uses a temporary tool surface to keep the beltline, shut lines, DLO
openings, and lamp apertures consistent. That tool is never emitted as a part.
The BIW output is split into named exterior panels and frame pieces so ownership
matches the V-model structure.
"""

from __future__ import annotations

import cadquery as cq

from vehiclecad.core.reference import common as C

_CACHE = {}


def _union(a, b):
    return cq.Workplane(obj=a).union(cq.Workplane(obj=b)).clean().val()


def _volume(shape) -> float:
    if shape is None:
        return 0.0
    try:
        return shape.Volume()
    except ValueError:
        return 0.0


def _intersect_or_none(source, cutter):
    try:
        panel = source.intersect(cutter)
    except ValueError:
        return None
    return panel if _volume(panel) > 1.0 else None


def _cut_or_empty(source, cutter):
    try:
        return source.cut(cutter)
    except ValueError:
        return None


def _outer_tool():
    """Temporary outer tool surface with wheel, lamp, grille, and tail apertures."""
    from vehiclecad.parts.exterior.detail import frontend, rearend

    outer = _union(C.loft(C.BODY, ruled=True), C.greenhouse_solid())
    for ax, radius in ((C.AXLE_F, 352), (C.AXLE_R, 360)):
        for side in (1, -1):
            outer = outer.cut(C.cyl(radius, 460, (ax, side * 470, 300), (0, side, 0)))
    for cutter in frontend.body_cutters() + rearend.body_cutters():
        outer = outer.cut(cutter)
    return outer


def _panel_tool():
    """Temporary hollow sheet-metal tool with DLO openings cut through the wall."""
    from vehiclecad.parts.exterior.detail import frontend, rearend

    outer = _outer_tool().cut(C.window_cutters())
    inner = C.U([C.loft(C.BODY_INSET, ruled=True), C.loft(C.GREEN_INSET, ruled=True)])
    tool = outer.cut(inner)
    tool = _union(tool, _end_closure_caps(frontend.body_cutters(), rearend.body_cutters()))
    tool = _union(tool, _aperture_backing_caps())
    tool = tool.cut(C.box(1560, -772, 1000, 1660, 1544, 40))
    tool = tool.cut(_underbody_reliefs())
    tool = tool.cut(_cowl_plenum_slot())
    return tool


def _cowl_plenum_slot():
    """Opening in the cowl top for the slatted plenum grille (trim_molding's
    cowl_vent sits IN this slot) plus the two wiper-pivot notches."""
    slot = C.box(1496, -384, 992, 36, 768, 38)
    notches = [C.box(1496, ypiv - 24, 1000, 70, 48, 34) for ypiv in (250.0, -150.0)]
    return C.U([slot] + notches)


def _underbody_reliefs():
    """Stamped underbody clearances for the exhaust run -- the production floor
    carries exactly these reliefs: the full-length exhaust channel beside the
    tunnel (downpipe drop, mid pipe, muffler recess to z362 over the muffler
    top 348) and the twin tip cut-outs through the rear valance face."""
    downpipe = C.box(1050, -344, 136, 420, 252, 170)    # downpipe drop zone
    channel = C.box(1450, -336, 136, 1940, 244, 110)    # mid-pipe channel
    mid_muff = C.box(3380, -392, 136, 740, 270, 226)    # muffler recess
    tips = C.box(4260, -380, 206, 200, 168, 92)         # valance tip cut-outs
    # lateral channel where the rear ARB swings under the floor (x3461..3483)
    arb_channel = C.box(3448, -484, 136, 50, 968, 70)
    # open suspension bays: the rear subframe bay and the front ARB sweep are
    # not skinned over on a production underbody
    subframe_bay = C.box(2865, -552, 150, 440, 1104, 190)
    front_arb_channel = C.box(610, -400, 106, 260, 800, 96)
    return C.U([downpipe, channel, mid_muff, tips, arb_channel,
                subframe_bay, front_arb_channel])


def _end_closure_caps(front_cutters, rear_cutters):
    """Seal the hollow shell's front and rear inner openings with metal caps.

    The inner loft reaches the first and last lower-body stations, so subtracting
    it leaves rectangular through-holes at the nose and tail.  These thin caps
    overlap the surrounding sheet-metal and are re-cut for lamp/grille apertures.
    """
    front = C.rbox(60, -688, 198, 22, 1376, 670, 4)
    rear = C.rbox(4318, -702, 198, 22, 1404, 812, 4)
    for cutter in front_cutters:
        front = front.cut(cutter)
    for cutter in rear_cutters:
        rear = rear.cut(cutter)
    return C.U([front, rear])


def _aperture_backing_caps():
    """Add blind back plates to nose and tail apertures owned by the body panels."""
    from vehiclecad.parts.exterior.detail import frontend, rearend

    caps = []

    # Nose panel: the visible lamp/grille holes remain open at the face, but the
    # pockets close inside PRT_Front_Nose_Panel so the body panel is not see-through
    # when exterior insert parts are hidden.
    for side in (1, -1):
        for _tag, yy, radius in frontend.LAMPS:
            caps.append(C.cyl(radius + 8, 8, (134, side * yy, frontend.Z_LAMP), (1, 0, 0)))
    caps.append(C.box(134, -frontend.GR_Y, frontend.GR_Z0, 8, 2 * frontend.GR_Y, frontend.GR_Z1 - frontend.GR_Z0))

    # Tail panel: close the tail-lamp pockets from the body side, forward of the
    # lamp housings, so PRT_Rear_Tail_Panel is also watertight on its own.
    for side in (1, -1):
        y0 = rearend.TL_Y0 if side > 0 else -rearend.TL_Y1
        caps.append(C.box(4298, y0, rearend.TL_Z0 - 4, 10, rearend.TL_Y1 - rearend.TL_Y0, rearend.TL_Z1 - rearend.TL_Z0 + 8))

    return C.U(caps)


def _greenhouse_beltline_closures():
    """Close the visual gap between lower body, doors, and greenhouse base."""
    side_l = C.rbox(1500, 758, 1006, 1740, 48, 28, 5)
    side_r = C.mirror_y(side_l)
    cowl = C.rbox(1488, -638, 1006, 300, 1276, 22, 5)
    rear_shelf = C.rbox(2700, -638, 1008, 540, 1276, 24, 5)
    return C.U([side_l, side_r, cowl, rear_shelf])


def _compound_with(shape, additions):
    return cq.Compound.makeCompound([shape, *additions]) if additions else shape


def _augment_body_parts(parts):
    """Attach beltline fillers to existing atomic body panel names.

    Fillers are relieved of the closure shut regions and the cowl plenum slot
    so they never overlap the door/hood panels or the vent grille."""
    door_l_outer = C.box(1505, 0, 300, 980, 906, 732)
    door_r_outer = C.box(1505, -906, 300, 980, 906, 732)
    hood_outer = C.box(160, -516, 786, 1342, 1032, 244)
    additions = {
        "PRT_Left_Aperture_Frame": [
            C.rbox(1500, 758, 1006, 1000, 28, 24, 4).cut(door_l_outer),
        ],
        "PRT_Right_Aperture_Frame": [
            C.rbox(1500, -786, 1006, 1000, 28, 24, 4).cut(door_r_outer),
        ],
        "PRT_Cowl_Upper_Panel": [
            C.rbox(1488, -638, 1006, 300, 1276, 22, 5)
             .cut(hood_outer).cut(_cowl_plenum_slot()),
        ],
        "PRT_Rear_Deck_Frame": [
            C.rbox(2700, -638, 1008, 540, 1276, 24, 5),
        ],
        "PRT_Rear_Quarter_L": [
            C.rbox(2600, 758, 1006, 640, 28, 24, 4),
        ],
        "PRT_Rear_Quarter_R": [
            C.rbox(2600, -786, 1006, 640, 28, 24, 4),
        ],
    }
    return [(_compound_with(shape, additions.get(name, [])), color, name) for shape, color, name in parts]


def _door_hardware(s):
    """Hinges (two leaves + vertical pins) at the door's front edge and the
    latch striker pocket at its rear edge -- the hardware a closure needs to
    actually hang and shut.  Kept inside the door's own shut region."""
    items = []
    hinge_y0 = 760.0 if s > 0 else -790.0
    for z0 in (410.0, 630.0):
        items.append(C.rbox(1512, hinge_y0, z0, 40, 30, 58, 5))
        items.append(C.cyl(5.5, 70, (1522, s * 778, z0 - 6), (0, 0, 1)))
    # latch with claw slot at the rear shut face
    latch_y0 = 758.0 if s > 0 else -788.0
    latch = C.rbox(2428, latch_y0, 512, 30, 30, 52, 4)
    latch = latch.cut(C.box(2434, latch_y0 - 8, 528, 12, 46, 14))
    items.append(latch)
    return items


def _augment_closure_parts(parts):
    """Extend door tops to the beltline seal and add the closure HARDWARE
    (hinges, latches) without changing part names."""
    additions = {
        "door_L": [C.rbox(1509, 790, 1008, 972, 22, 20, 4)] + _door_hardware(1),
        "door_R": [C.rbox(1509, -812, 1008, 972, 22, 20, 4)] + _door_hardware(-1),
        "hood": [
            # rear-corner gooseneck hinges + front safety-catch latch plate
            C.rbox(1430, 396, 990, 64, 26, 22, 5),
            C.rbox(1430, -422, 990, 64, 26, 22, 5),
            C.cyl(5, 40, (1444, 388, 1000), (0, 1, 0)),
            C.cyl(5, 40, (1444, -428, 1000), (0, 1, 0)),
            C.rbox(196, -36, 836, 26, 72, 20, 4),
            C.cyl(6, 26, (210, 0, 818), (0, 0, 1)),
        ],
        "trunk_lid": [
            # front-corner hinge arms + rear latch
            C.rbox(3512, 392, 1008, 56, 24, 26, 5),
            C.rbox(3512, -416, 1008, 56, 24, 26, 5),
            C.cyl(5, 36, (3524, 384, 1020), (0, 1, 0)),
            C.cyl(5, 36, (3524, -424, 1020), (0, 1, 0)),
            C.rbox(4128, -32, 1000, 24, 64, 18, 4),
            C.cyl(6, 22, (4140, 0, 984), (0, 0, 1)),
        ],
    }
    return [(_compound_with(shape, additions.get(name, [])), color, name) for shape, color, name in parts]


def _closure_regions():
    return {
        "hood": (
            C.box(160, -516, 786, 1342, 1032, 244),
            C.box(164, -512, 786, 1334, 1024, 244),
        ),
        "trunk_lid": (
            C.box(3500, -548, 1006, 668, 1096, 150),
            C.box(3504, -544, 1006, 660, 1088, 150),
        ),
        "door_L": (
            C.box(1505, 0, 300, 980, 906, 732),
            C.box(1509, 0, 304, 972, 906, 724),
        ),
        "door_R": (
            C.box(1505, -906, 300, 980, 906, 732),
            C.box(1509, -906, 304, 972, 906, 724),
        ),
    }


def _body_panel_regions():
    return [
        ("PRT_Front_Nose_Panel", C.box(-40, -760, 193, 420, 1520, 677)),
        ("PRT_Front_Fender_L", C.box(280, 420, 230, 980, 520, 720)),
        ("PRT_Front_Fender_R", C.box(280, -940, 230, 980, 520, 720)),
        ("PRT_Cowl_Upper_Panel", C.box(1260, -720, 760, 430, 1440, 360)),
        ("PRT_Left_Aperture_Frame", C.box(1380, 500, 500, 1220, 430, 720)),
        ("PRT_Right_Aperture_Frame", C.box(1380, -930, 500, 1220, 430, 720)),
        ("PRT_Rocker_Outer_L", C.box(1100, 650, 230, 2040, 270, 340)),
        ("PRT_Rocker_Outer_R", C.box(1100, -920, 230, 2040, 270, 340)),
        ("PRT_Roof_Outer_Panel", C.box(1620, -610, 1040, 1540, 1220, 390)),
        ("PRT_Rear_Quarter_L", C.box(2480, 430, 340, 940, 520, 790)),
        ("PRT_Rear_Quarter_R", C.box(2480, -950, 340, 940, 520, 790)),
        ("PRT_Rear_Tail_Panel", C.box(3420, -760, 193, 1000, 1520, 837)),
        ("PRT_Rear_Deck_Frame", C.box(3200, -650, 850, 840, 1300, 260)),
        ("PRT_Left_Beltline_Rail", C.box(1450, 640, 900, 1760, 230, 220)),
        ("PRT_Right_Beltline_Rail", C.box(1450, -870, 900, 1760, 230, 220)),
        ("PRT_Fuel_Flap", C.box(3050, 720, 740, 78, 150, 130)),
    ]


def _residual_regions():
    return [
        ("PRT_Left_Body_Frame_Residual", C.box(-80, 0, 180, 4560, 1040, 1240)),
        ("PRT_Right_Body_Frame_Residual", C.box(-80, -1040, 180, 4560, 1040, 1240)),
        ("PRT_Center_Body_Frame_Residual", C.box(-80, -680, 180, 4560, 1360, 1240)),
    ]


def _cut_named_regions(source, regions):
    remaining = source
    parts = []
    for name, cutter in regions:
        if remaining is None:
            break
        panel = _intersect_or_none(remaining, cutter)
        if panel is not None:
            parts.append((panel, C.RED, name))
            remaining = _cut_or_empty(remaining, cutter)
    return parts, remaining


def _split():
    if _CACHE:
        return _CACHE["body"], _CACHE["closures"]

    tool = _panel_tool()
    closures = []
    closure_cuts = []
    for name, (outer, inner) in _closure_regions().items():
        panel = _intersect_or_none(tool, inner)
        if panel is not None:
            closures.append((panel, C.RED, name))
        shut_region = _intersect_or_none(tool, outer)
        if shut_region is not None:
            closure_cuts.append(shut_region)

    body_source = _cut_or_empty(tool, C.U(closure_cuts)) if closure_cuts else tool
    body_parts, remainder = _cut_named_regions(body_source, _body_panel_regions())
    residual_parts, remainder = _cut_named_regions(remainder, _residual_regions())
    body_parts.extend(residual_parts)
    if _volume(remainder) > 1.0:
        body_parts.append((remainder, C.RED, "PRT_Body_Unassigned_Small_Panel_Fragments"))

    body_parts = _augment_body_parts(body_parts)
    closures = _augment_closure_parts(closures)

    _CACHE["body"] = body_parts
    _CACHE["closures"] = closures
    return body_parts, closures


def body_parts():
    return _split()[0]


def closure_parts():
    return _split()[1]


def parts():
    return []
