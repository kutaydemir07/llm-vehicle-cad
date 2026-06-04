"""ASM_4220_Steering_Wheel - ModelA SportsCar M-Technic steering wheel.

The wheel is drawn around the same hub axis used by the column hardpoints, so
the rim, hub, boss and spokes stay centred and mated to the steering column.
"""
from __future__ import annotations
import numpy as np
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


DARK  = (0.09, 0.09, 0.10)
SPOKE = (0.12, 0.12, 0.13)


def _steering():
    """M-Technic wheel: torus rim, centre pad, boss and three broad spokes."""
    hub_pt = np.array(SK.STEERING["wheel_hub"], float)
    axis = np.array(SK.STEERING["wheel_axis_tip"], float) - hub_pt
    axis = axis / float(np.linalg.norm(axis))

    v_y = np.array([0.0, 1.0, 0.0])
    v_z = np.cross(axis, v_y)
    v_z = v_z / float(np.linalg.norm(v_z))

    def pt(vec):
        return tuple(float(x) for x in vec)

    rim_r = 165.0
    tube_r = 17.0
    rim = Solid.makeTorus(rim_r, tube_r, Vector(*hub_pt), Vector(*axis))
    thumb_grip = Solid.makeTorus(rim_r + 1, 6, Vector(*hub_pt), Vector(*axis))
    rim = C.U([rim, thumb_grip])

    hub_base = pt(hub_pt - axis * 34)
    hub = C.cyl(42, 68, hub_base, pt(axis))
    pad = C.cyl(62, 18, pt(hub_pt + axis * 18), pt(axis))
    boss = C.cyl(28, 52, pt(hub_pt - axis * 52), pt(axis))

    # spokes reach exactly the rim's inner surface so they meet it without
    # spearing through (rim inner radius = rim_r - tube_r).
    rim_inner = rim_r - tube_r
    spokes = []
    for deg in (90, 210, 330):
        rad = np.deg2rad(deg)
        rim_vec = np.cos(rad) * v_y + np.sin(rad) * v_z
        p0 = hub_pt + rim_vec * 38
        p1 = hub_pt + rim_vec * 130
        p2 = hub_pt + rim_vec * rim_inner
        spokes.append(C.swept_tube([pt(p0), pt(p1), pt(p2)], 10, cap=True))

    # axial bore up the boss so the splined column nose seats in the hub with
    # clearance (the wheel slides onto the column, it is not speared by it).
    column_bore = C.cyl(16, 78, pt(hub_pt - axis * 60), pt(axis))
    hub_solid = C.U([hub, pad, boss] + spokes).cut(column_bore)

    return [
        (rim, DARK, "steering_rim"),
        (hub_solid, SPOKE, "steering_hub"),
    ]


def parts():
    return _steering()
