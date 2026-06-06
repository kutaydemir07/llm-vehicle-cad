"""Engine bay brackets, body mounts, and misc BiW reinforcements.

Parts:
  PRT_Engine_Mount_Bracket_L/R   -  weld-on brackets for the motor mount rubbers
  PRT_Body_Mount_Front/Rear      -  sub-frame body isolator pads ( - 4 per side)
  PRT_Firewall_Stiffener         -  diagonal gusset tying firewall to floor
  PRT_Front_Rail_L/R             -  longitudinal front rails (engine cradle)

Collision-free:
  Engine mount brackets sit AT the engine mount hardpoints (y -  - 260, z - 380)  - 
  engine block is y= - 210 so brackets are clear at y=260.
  Body mounts are at floor level z=220, outside the exhaust tunnel.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference.hardpoints import POWERTRAIN as PT
from vehiclecad.geometry import machine_elements as ME

_box    = C.box
_cyl    = C.cyl
_rbox   = C.rbox
_U      = C.U
_mirror = C.mirror_y
COL     = C.STRUCT


def _rbox_center(cx, cy, cz, dx, dy, dz, r):
    return _rbox(cx - dx / 2.0, cy - dy / 2.0, cz - dz / 2.0, dx, dy, dz, r)


def _engine_mount_bracket_left():
    """Compact bolt-on engine mount stand-off, left side.

    The shelf sits below the rubber isolator and reaches outboard to the front
    subframe rail corridor without penetrating the fuel lines or chassis rail.
    """
    mx, my, mz = PT["engine_mount_L"]   # (580, 260, 380)
    shelf = _rbox(mx - 58, my - 38, mz - 62, 116, 76, 8, 4)
    outboard_web = _rbox(mx - 58, 300, mz - 78, 116, 11.5, 24, 4)
    front_web = _rbox(mx - 58, my - 38, mz - 88, 8, 76, 32, 3)
    rear_web = _rbox(mx + 48, my - 38, mz - 88, 8, 76, 32, 3)
    gus_front = C.xz_prism(
        [(mx - 48, mz - 78), (mx + 34, mz - 78), (mx - 8, mz - 62)],
        my - 34, my - 24
    )
    gus_rear = C.xz_prism(
        [(mx - 34, mz - 78), (mx + 48, mz - 78), (mx + 8, mz - 62)],
        my + 24, my + 34
    )
    bolt_bosses = [
        ME.cap_screw("M10", 12, (mx - 28, my - 18, mz - 78), (0, 0, 1)),
        ME.cap_screw("M10", 12, (mx + 28, my + 18, mz - 78), (0, 0, 1)),
    ]
    return _U([shelf, outboard_web, front_web, rear_web, gus_front, gus_rear] + bolt_bosses)


def _front_rail_left():
    """Left lower rail reinforcement strip.

    The structural chassis rail and inner fender already own the main engine-bay
    volume.  This part is the bolt-on/weld-on reinforcement strip that sits just
    outboard and below those solids, clear of the front fascia package.
    """
    spine_front = _rbox(350, 552.5, 252, 270, 47.5, 32, 6)
    spine_rear = _rbox(1000, 552.5, 252, 218, 47.5, 32, 6)
    hem_front = _rbox(372, 580, 282, 226, 16, 10, 3)
    hem_rear = _rbox(1022, 580, 282, 174, 16, 10, 3)
    bolt_pads = [
        ME.cap_screw("M8", 10, (x, 576, 238), (0, 0, 1))
        for x in (450, 580, 1060, 1160)
    ]
    return _U([spine_front, spine_rear, hem_front, hem_rear] + bolt_pads)


def _body_mounts():
    """Four body isolator pads (left side) at the corners of the body-frame interface.

    Simple rubber-sandwich pucks (r=35, h=18) at:
      Front L/R at x=1100, z=220, y= - 680
      Rear  L/R at x=3400, z=220, y= - 680
    """
    mounts = []
    for x, y in ((1240, 520), (1240, -520), (2800, 620), (2800, -620)):
        pad = _U([
            ME.bonded_bushing(32, 10, 22, (x, y, 177), (0, 0, 1)),
            ME.through_bolt("M10", 38, (x, y, 174), (0, 0, 1)),
        ])
        side = "L" if y > 0 else "R"
        pos  = "F" if x < 2000 else "R"
        mounts.append((pad, C.RUBBER, f"PRT_Body_Mount_{pos}{side}"))
    return mounts


def _firewall_stiffener_left():
    """Outboard firewall/rail stiffener, left side.

    Runs on top of the lower rail strip in the narrow corridor between the
    chassis rail and the front tire envelope, then lands on the firewall flange.
    """
    foot = _rbox(850, 560, 292, 92, 36, 24, 4)
    brace = C.swept_tube(
        [(914, 586, 316), (1040, 586, 400), (1208, 586, 500)], 9, cap=True
    )
    firewall_tab = _rbox(1206, 560, 462, 13.2, 36, 76, 4)
    return _U([foot, brace, firewall_tab])


def _engine_mount_rubbers():
    """Rubber engine-mount bushings filling the gap between each weld-on bracket
    shelf and the block's mount pad  -  so the motor sits ON its mounts, not over a
    void.  Centred on the engine-mount hardpoints."""
    out = []
    for tag, nm in (("engine_mount_L", "L"), ("engine_mount_R", "R")):
        mx, my, mz = PT[tag]
        rub = _U([
            _cyl(26, 28, (mx, my, mz - 50), (0, 0, 1)),
            ME.washer(34, 12, 4, (mx, my, mz - 56), (0, 0, 1)),
            ME.washer(32, 12, 4, (mx, my, mz - 22), (0, 0, 1)),
            ME.threaded_stud_with_nut("M12", 52, (mx, my, mz - 66), (0, 0, 1)),
        ])
        out.append((rub, C.RUBBER, f"PRT_Engine_Mount_Rubber_{nm}"))
    return out


def _trans_mount_rubber():
    """Rubber gearbox mount sitting on the EXISTING transmission crossmember
    (PRT_Trans_Crossmember in crossmembers.py) under the gearbox tail  -  fills the
    void so the gearbox is carried by its mount rather than floating."""
    tm = PT["trans_mount"]                       # (1350, 0, 370)
    pucks = []
    for y in (190, -190):
        pucks.extend([
            ME.bonded_bushing(24, 8, 16, (tm[0], y, 354), (0, 0, 1)),
            ME.threaded_stud_with_nut("M8", 20, (tm[0], y, 368), (0, 0, 1)),
        ])
    rub = _U(pucks)
    return [(rub, C.RUBBER, "PRT_Trans_Mount_Rubber")]


def parts():
    out = []
    l_bracket = _engine_mount_bracket_left()
    out.append((l_bracket,          COL, "PRT_Engine_Mount_Bracket_L"))
    out.append((_mirror(l_bracket), COL, "PRT_Engine_Mount_Bracket_R"))

    out.extend(_engine_mount_rubbers())
    out.extend(_trans_mount_rubber())

    l_rail = _front_rail_left()
    out.append((l_rail,          COL, "PRT_Front_Rail_L"))
    out.append((_mirror(l_rail), COL, "PRT_Front_Rail_R"))

    out.extend(_body_mounts())

    l_stiff = _firewall_stiffener_left()
    out.append((l_stiff,          COL, "PRT_Firewall_Stiffener_L"))
    out.append((_mirror(l_stiff), COL, "PRT_Firewall_Stiffener_R"))
    return out
