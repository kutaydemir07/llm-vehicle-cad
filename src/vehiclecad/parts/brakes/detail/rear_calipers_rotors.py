"""Retired rear brake detail reference.

The emitted road-car rotor/caliper is owned by the mate-assembled wheel corner
so it cannot duplicate the hub stack. Source-backed ModelA SportsCar road spec is a
282 mm solid rear disc with a single-piston floating caliper.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference.materials import AXLE_R, WHEEL_Z

_cyl    = C.cyl
_rbox   = C.rbox
_U      = C.U
_mirror = C.mirror_y
COL_ROTOR   = (0.40, 0.40, 0.42)
COL_CALIPER = C.CALIPER


def _rear_rotor_left():
    """282 mm solid rear disc reference, left side.

    Left rear hub centre: (3372, 720, 300).
    Disc inner face at y=692, thickness 22 mm -> spans y=692-714.
    """
    ax, ay_inner, az = AXLE_R, 692, WHEEL_Z
    disc = _cyl(141, 22, (ax, ay_inner, az), (0, 1, 0))        # full disc
    hat  = _cyl(68,  32, (ax, ay_inner - 12, az), (0, 1, 0))   # hat bell
    disc = disc.cut(_cyl(58, 44, (ax, ay_inner - 16, az), (0, 1, 0)))
    return _U([disc, hat])


def _rear_caliper_left():
    """Single-piston floating caliper straddling the disc (y=692-714)."""
    ax, az = AXLE_R, WHEEL_Z
    body = _rbox(ax - 34, 688, az + 30, 65, 40, 100, 6)  # x=3338-3403, y=688-728, z=330-430
    return body


def parts():
    # Rear rotor + caliper are now owned by the mate-assembled wheel corner
    # (exterior/wheels.py corner()); the disc is seated onto the hub by a face
    # mate there.  Returning nothing here avoids duplicate / clashing discs.
    return []
