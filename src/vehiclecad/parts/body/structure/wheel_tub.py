"""Rear wheelhouse tubs for the body-in-white."""
from __future__ import annotations

from cadquery import Solid, Vector

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

_box = C.box
_mirror = C.mirror_y
COL = C.STRUCT


def _wheel_tub_left():
    """Thin outboard upper wheelhouse skin for the left rear arch.

    The tub must sit around the wheelhouse, not through the central rear package.
    Keeping the shell outboard clears the tank, diff, rear bench, spring, and
    damper package volumes.
    """
    cx, cy, cz = SK.CHASSIS["wheel_tub_RL"]
    r = 360.0
    wall = 1.2

    outer = Solid.makeSphere(r, Vector(cx, cy, cz))
    inner = Solid.makeSphere(r - wall, Vector(cx, cy, cz))
    shell = outer.cut(inner)

    clip_outboard = _box(cx - 290, cy + 95, cz + 315, 580, 230, 130)
    return shell.intersect(clip_outboard)


def parts():
    left = _wheel_tub_left()
    return [
        (left, COL, "PRT_Rear_Wheel_Tub_L"),
        (_mirror(left), COL, "PRT_Rear_Wheel_Tub_R"),
    ]

