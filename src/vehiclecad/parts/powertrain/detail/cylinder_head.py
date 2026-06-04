"""I4_Engine cylinder head and valve cover  -  detailed geometry."""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference.hardpoints import POWERTRAIN as PT

_box    = C.box
_cyl    = C.cyl
_rbox   = C.rbox
_U      = C.U
COL_H   = C.ALLOY_E


def _cylinder_head():
    """Alloy cylinder head  -  slightly wider than block, 60 mm tall.

    16-valve DOHC head.  Two cam towers at front and rear, four cam
    bearing caps, spark-plug bosses on top.
    """
    # main head casting: x=400 - 980, y= - 230, z=660 - 720
    head = _rbox(400, -230, 660, 580, 460, 60, 8)

    # cam cover interface rail (raised 4 mm lip around the head top)
    rail = _box(408, -228, 720, 564, 456, 4)
    head = _U([head, rail])

    # cam towers: front (x=420, r=30) and rear (x=960, r=30), z=720 - 760
    cam_front = _cyl(30, 42, (420, 0, 720), (0, 0, 1))
    cam_rear  = _cyl(30, 42, (960, 0, 720), (0, 0, 1))

    # 4 cam bearing caps (x evenly spaced)
    caps = []
    for i in range(4):
        cx = 480 + i * 140
        c = _box(cx - 20, -230, 720, 40, 460, 18)
        caps.append(c)

    # 4 spark-plug bosses on top, angled slightly rearward
    import math
    plugs = []
    for i in range(4):
        px = 490 + i * 140
        plug = _cyl(14, 22, (px, -20, 740), (0, 0, 1))
        plugs.append(plug)

    head = _U([head, cam_front, cam_rear] + caps + plugs)
    # bore the cam journals (towers + caps) so the two camshafts run in clearance
    cam_bores = _U([_cyl(18, 580, (398, dy, 728), (1, 0, 0)) for dy in (-50, 50)])
    return head.cut(cam_bores)


def _valve_cover():
    """Valve cover / cam cover  -  rounded box, highest engine point  -  z=790.

    Modelled as a hollow casting (open at the bottom where it bolts to the head
    rail) so the camshafts run inside it in clearance instead of being speared by
    a solid lid.
    """
    # x=420 - 980, y= - 200, z=722 - 790
    cover = _rbox(420, -200, 722, 560, 400, 68, 20)
    # hollow it full-length (open ends + bottom) so the cam towers, bearing caps
    # and spark-plug bosses on the head top all sit inside it in clearance.
    cavity = _box(414, -192, 716, 572, 384, 68)
    cover = cover.cut(cavity)

    # raised Classic / M Power text bump (approximate as a ridge)
    badge = _rbox(620, -60, 790, 100, 120, 6, 4)

    # oil filler cap boss at front
    filler = _cyl(22, 20, (450, 100, 790), (0, 0, 1))

    return _U([cover, badge, filler])


def parts():
    out = []
    out.append((_cylinder_head(), COL_H, "PRT_I4_Engine_Cylinder_Head_Detailed"))
    out.append((_valve_cover(),   COL_H, "PRT_I4_Engine_Valve_Cover_Detailed"))
    return out

