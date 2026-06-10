"""Exterior body moldings & fine trim  -  the high-contrast details that sharpen
the surfacing: side rub strips, blacked-out B-pillars, DLO beltline trim, roof
drip rails, cowl-vent grille, windscreen wipers and the fender antenna.

All parts are satin-black / chrome so they read against the red body.  They are
routed into ASM_Trim via ``exterior/trim.py`` (which calls ``parts()`` here).
Frame: +x rear, +y left, +z up, millimetres (see core/common.py).
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C


def _rub_strips():
    """Satin-black side rubbing strips broken at real panel/wheel openings."""
    out = []
    segments = (
        ("front_fender", 1188.0, 265.0),
        ("door", 1518.0, 912.0),
        ("quarter", 2538.0, 438.0),
        ("rear_quarter", 3754.0, 304.0),
    )
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        y0 = 814.0 if s > 0 else -832.0
        for label, x0, dx in segments:
            out.append((C.rbox(x0, y0, 560, dx, 18, 30, 6),
                        C.TRIM_BLK, f"side_rub_strip_{label}_{side}"))
    return out


def _b_pillars():
    """Blacked-out B-pillar covers between the door and quarter glass."""
    out = []
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        y0 = 718.0 if s > 0 else -734.0
        out.append((C.rbox(2470, y0, 1024, 70, 16, 312, 5),
                    C.BLACK, f"b_pillar_cover_{side}"))
    return out


def _beltline_trim():
    """Thin black DLO trim along the base of the side glass.

    One moulding per side in two seated segments, each clipped onto ITS panel:
    the door segment rides the door's beltline channel (outer face |y|=812)
    and the quarter segment sits just above the body's beltline shoulder
    (which bulges to |y|~802 at z1014..1016)."""
    out = []
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        door_seg = C.rbox(1640, 813.0, 1014, 838, 12, 12, 4)
        qtr_seg = C.rbox(2487, 795.0, 1017, 433, 12, 12, 4)
        strip = C.U([door_seg, qtr_seg])
        if s < 0:
            strip = C.mirror_y(strip)
        out.append((strip, C.TRIM_BLK, f"dlo_belt_{side}"))
    return out


def _drip_rails():
    """Roof drip rails along each side of the greenhouse."""
    out = []
    # clipped onto the gutter seam just below the roof-edge band (z>=1342)
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        y0 = 722.0 if s > 0 else -734.0
        out.append((C.rbox(1820, y0, 1332, 920, 12, 14, 4),
                    C.BLACK, f"drip_rail_{side}"))
    return out


def _cowl_vent():
    """Black slatted cowl/plenum grille seated in the cowl panel's plenum slot
    (body.py cuts the matching opening at x1496..1532)."""
    back = C.rbox(1502, -380, 996, 26, 760, 20, 5)
    for k in range(3):
        back = back.cut(C.box(1500, -300 + k * 280, 1000, 8, 40, 10))   # drains
    out = [(back, C.BLACK, "cowl_vent_back")]
    slats = [C.box(1506, -376, 999 + k * 5, 20, 752, 2) for k in range(4)]
    out.append((C.U(slats), C.TRIM_BLK, "cowl_vent_slats"))
    return out


def _wipers():
    """Two black wiper arms + blades resting at the windscreen base."""
    out = []
    for ypiv in (250.0, -150.0):
        tag = "L" if ypiv > 0 else "R"
        arm = C.tube_path([(1516, ypiv, 1012), (1600, ypiv - 40, 1070),
                           (1660, ypiv - 90, 1112)], 5.0)
        blade = C.tube_path([(1648, ypiv - 40, 1098), (1692, ypiv - 150, 1142)], 6.0)
        out.append((C.U([arm, blade]), C.BLACK, f"wiper_{tag}"))
    return out


def _antenna():
    """Thin raked fender antenna (rear-left quarter)."""
    mast = C.cyl(4, 280, (3500, 800, 1038), (0.05, 0.08, 1))
    base = C.rbox(3486, 792, 1030, 28, 24, 16, 6)
    return [(mast, C.BLACK, "antenna_mast"), (base, C.BLACK, "antenna_base")]


def parts():
    out = []
    out += _rub_strips()
    out += _b_pillars()
    out += _beltline_trim()
    out += _drip_rails()
    out += _cowl_vent()
    out += _wipers()
    out += _antenna()
    return out
