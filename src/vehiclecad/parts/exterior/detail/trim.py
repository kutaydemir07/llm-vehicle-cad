"""Exterior trim: door mirrors (stalk + housing + glass), door handles, and the
fine body moldings (rub strips, B-pillars, cowl vent, wipers, drip rails,
antenna) which live in ``trim_molding.py``.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from . import trim_molding


def parts():
    out = []
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        mirror_base_l = C.rbox(1810, 814, 990, 40, 24, 48, 5)
        mirror_stalk_l = C.swept_tube([(1828, 832, 1012), (1848, 858, 1020)], 9, cap=True)
        mirror_shell_l = C.rbox(1844, 858, 982, 98, 58, 68, 12)
        mirror_l = C.U([mirror_base_l, mirror_stalk_l, mirror_shell_l])
        mirror = mirror_l if s > 0 else C.mirror_y(mirror_l)

        glass_l = C.rbox(1936, 864, 994, 7, 46, 44, 4)
        glass = glass_l if s > 0 else C.mirror_y(glass_l)

        handle_l = C.U([
            C.rbox(2266, 820, 970, 106, 16, 24, 5),
            C.rbox(2294, 816, 978, 48, 8, 8, 3),
        ])
        handle = handle_l if s > 0 else C.mirror_y(handle_l)

        out.append((mirror, C.RED, f"mirror_{side}"))
        out.append((glass, C.GLASS, f"mirror_glass_{side}"))
        out.append((handle, C.RED, f"door_handle_{side}"))
    out.extend(trim_molding.parts())         # rub strips, B-pillars, cowl, wipers - 
    return out
