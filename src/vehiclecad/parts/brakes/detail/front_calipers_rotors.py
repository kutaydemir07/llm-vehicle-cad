"""Retired front brake detail reference.

The emitted road-car rotor/caliper is owned by the mate-assembled wheel corner
so it cannot duplicate the hub stack. Source-backed ModelA SportsCar road spec is a
280 mm ventilated front disc with a single-piston floating caliper.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference.materials import AXLE_F, WHEEL_Z

_cyl    = C.cyl
_rbox   = C.rbox
_U      = C.U
_mirror = C.mirror_y
COL_ROTOR   = (0.40, 0.40, 0.42)
COL_CALIPER = C.CALIPER


def _front_rotor_left():
    """280 mm ventilated reference disc, left side.

    Disc sits outboard of hub bearing face at y=720.
    Disc inner face at y=720, thickness 28 mm -> outer face y=748.
    Hat wraps bearing boss (y=680-720, r=60), hat inner r=62 gives 2 mm clearance.
    """
    ax, az = AXLE_F, WHEEL_Z   # 810, 300
    disc = _cyl(140, 28, (ax, 720, az), (0, 1, 0))            # disc face y=720-748
    hat  = _cyl(76,  40, (ax, 680, az), (0, 1, 0))            # hat bell y=680-720
    disc = disc.cut(_cyl(62, 48, (ax, 676, az), (0, 1, 0)))   # hollow hat, r=62 inner
    return _U([disc, hat])


def _front_caliper_left():
    """Single-piston floating caliper body straddling the disc (y=720-748)."""
    ax, az = AXLE_F, WHEEL_Z
    body   = _rbox(ax - 40, 716, az + 50, 80, 44, 100, 8)        # y=716-760
    piston = _cyl(28, 18, (ax - 18, 716, az + 90), (0, 1, 0))    # inboard piston
    return _U([body, piston])


def parts():
    # Front rotor + caliper are now owned by the mate-assembled wheel corner
    # (exterior/wheels.py corner()), where the rotor is SEATED onto the hub by a
    # face mate rather than placed at an absolute coordinate.  Emitting them here
    # too would duplicate/clash, so this returns nothing.
    return []
