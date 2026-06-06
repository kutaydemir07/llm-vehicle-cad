"""ASM_2210_Rear_Subframe - ModelA semi-trailing-arm rear axle carrier.

The ModelA rear carrier is not a flat beam through the car centreline.  It has two
side pods for the semi-trailing-arm pivots, a low diff bridge, and open corridors
for the propshaft, exhaust, springs, and dampers.  The whole solid remains one
atomic leaf for the product tree, but the material is routed around the real
hardpoint envelopes instead of filling the bounding box.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.geometry import machine_elements as ME

_U      = C.U
_cyl    = C.cyl
_rbox   = C.rbox
COL     = C.STRUCT

REAR = SK.REAR_SUSP
PT = SK.POWERTRAIN


def _rbox_center(cx, cy, cz, dx, dy, dz, r):
    return C.rbox(cx - dx / 2.0, cy - dy / 2.0, cz - dz / 2.0, dx, dy, dz, r)


def _subframe_body():
    pieces = []

    for s in (1, -1):
        inner = REAR["sta_inner_pivot"]
        outer = REAR["sta_outer_pivot"]
        ip = (inner[0], s * abs(inner[1]), inner[2])
        op = (outer[0], s * abs(outer[1]), outer[2])

        # Pivot tube and two pressed side rails.  They live outboard of the
        # propshaft tunnel and stop inboard of the rear spring lower perch.
        pivot_tube = C.swept_tube([ip, op], 24, cap=True)
        lower_rail = C.swept_tube(
            [(2896, s * 236, 238), (2960, s * 468, 284), (3088, s * 438, 238)],
            22,
            cap=True,
        )
        upper_tie = C.swept_tube(
            [(2950, s * 320, 310), (3032, s * 410, 294), (3164, s * 430, 246)],
            18,
            cap=True,
        )

        # Rubber bushing housings are coaxial with the trailing-arm pivot tube.
        bush_i = ME.bonded_bushing(36, 11, 46, (ip[0] - 18, ip[1] - s * 23, ip[2] - 18), (0, s, 0))
        bush_o = ME.bonded_bushing(36, 11, 46, (op[0] - 18, op[1] - s * 23, op[2] - 18), (0, s, 0))

        # Body mounting feet attach below the floor and stay below the propshaft.
        mount_f = _rbox_center(2918, s * 286, 180, 70, 54, 22, 6)
        mount_r = _rbox_center(3010, s * 286, 180, 70, 54, 22, 6)
        drop_f = C.swept_tube([(2918, s * 286, 190), (2950, s * 320, 286)], 12, cap=True)
        drop_r = C.swept_tube([(3010, s * 286, 190), (3032, s * 410, 286)], 12, cap=True)

        # Rear pocket brace turns inward but stops before the spring/perch zone.
        spring_pocket_clear = C.swept_tube(
            [(3164, s * 430, 246), (3226, s * 418, 228), (3262, s * 386, 220)],
            17,
            cap=True,
        )

        pieces.extend([
            pivot_tube,
            lower_rail,
            upper_tie,
            bush_i,
            bush_o,
            mount_f,
            mount_r,
            drop_f,
            drop_r,
            spring_pocket_clear,
        ])

    # Low diff bridge: below the propshaft (prop rear z~310) and split around
    # the centreline, with two ears that pick up the LSD nose/rear cover mounts.
    diff = PT["diff_centre"]
    bridge_l = C.swept_tube([(3098, 188, 218), (3216, 144, 220)], 18, cap=True)
    bridge_r = C.mirror_y(bridge_l)
    diff_ear_l = _rbox_center(diff[0] - 62, 126, diff[2] - 56, 78, 48, 24, 6)
    diff_ear_r = C.mirror_y(diff_ear_l)
    diff_boss_l = _cyl(12, 26, (diff[0] - 62, 113, diff[2] - 44), (0, 1, 0))
    diff_boss_r = C.mirror_y(diff_boss_l)
    lower_bridge = C.swept_tube([(3050, 132, 198), (3188, 92, 198)], 13, cap=True)
    lower_bridge_r = C.mirror_y(lower_bridge)

    pieces.extend([
        bridge_l,
        bridge_r,
        diff_ear_l,
        diff_ear_r,
        diff_boss_l,
        diff_boss_r,
        lower_bridge,
        lower_bridge_r,
    ])

    carrier = _U(pieces)

    # Explicit service clearances.  These remove any accidental boolean bridges
    # that could appear when tubes fuse near the center tunnel or spring pockets.
    propshaft_window = C.box(2860, -122, 246, 470, 244, 190)
    exhaust_window = C.box(3040, -238, 154, 520, 122, 118)
    spring_l = C.cyl(82, 460, (REAR["spring_lower"][0], REAR["spring_lower"][1], 250), (0, 0, 1))
    spring_r = C.mirror_y(spring_l)
    damper_l = C.cyl(58, 430, (3380, 580, 270), (0, 0, 1))
    damper_r = C.mirror_y(damper_l)

    for cutter in (propshaft_window, exhaust_window, spring_l, spring_r, damper_l, damper_r):
        carrier = carrier.cut(cutter)

    return carrier


def parts():
    return [(_subframe_body(), COL, "PRT_Rear_Subframe")]


# --- legacy stubs kept for reference (not called) ---
def build_rear_subframe():
    """
    PART 5: PRT_Rear_Subframe
    Tubular/stamped steel crossmember mounting trailing arms and differential.
    Origin at vehicle centerline, between the trailing arm mounts.
    """
    t_center = make_tube((60, -150, 40), (60, 150, 40), 32)
    t_drop_L = make_tube((60, 150, 40), (0, 360, 0), 32)
    t_drop_R = make_tube((60, -150, 40), (0, -360, 0), 32)
    t_out_L  = make_tube((0, 360, 0), (0, 420, 20), 32)
    t_out_R  = make_tube((0, -360, 0), (0, -420, 20), 32)
    
    bush_L = make_boss((0, 420, 20), 45, 55)
    bush_hole_L = make_boss((0, 420, 15), 14, 70)
    
    bush_R = make_boss((0, -420, 20), 45, 55)
    bush_hole_R = make_boss((0, -420, 15), 14, 70)
    
    def make_bracket(y_pos):
        return cq.Workplane("YZ").box(50, 40, 60).translate((15, y_pos, 10)).val()
    
    b1 = make_bracket(140)  
    b2 = make_bracket(380)  
    b3 = make_bracket(-140) 
    b4 = make_bracket(-380) 
    
    diff_plate_L = make_link((60, 90, 40), (220, 90, 50), 30, 40)
    diff_plate_R = make_link((60, -90, 40), (220, -90, 50), 30, 40)
    diff_bridge = cq.Workplane("XY").box(60, 240, 15).translate((200, 0, 50)).val()
    
    subframe_solid = C.U([t_center, t_drop_L, t_drop_R, t_out_L, t_out_R, bush_L, bush_R, b1, b2, b3, b4, diff_plate_L, diff_plate_R, diff_bridge])
    holes = C.U([bush_hole_L, bush_hole_R])
    subframe = cq.Workplane("XY").newObject([subframe_solid]).cut(cq.Workplane("XY").newObject([holes]))
    
    return subframe.val()
