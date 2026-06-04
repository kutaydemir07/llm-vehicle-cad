"""ASM_4210_Column - steering column tube, bearings and U-joints.

The column is a mated chain from the wheel hub through the dashboard/firewall
bearing and down to the rack pinion.  It is routed down the left side of the
engine bay so it clears the oil pan, brake booster and dashboard package.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.STRUCT
STEER = SK.STEERING


def _u_joint(point, axis="x"):
    """Compact cross-style universal joint at a steering shaft bend."""
    x, y, z = point
    if axis == "z":
        fork_a = _rbox(x - 18, y - 12, z - 22, 36, 24, 44, 5)
        fork_b = _rbox(x - 12, y - 18, z - 14, 24, 36, 28, 5)
        pin = _cyl(9, 44, (x, y - 22, z), (0, 1, 0))
    else:
        fork_a = _rbox(x - 22, y - 14, z - 14, 44, 28, 28, 5)
        fork_b = _rbox(x - 14, y - 22, z - 12, 28, 44, 24, 5)
        pin = _cyl(9, 44, (x, y - 22, z), (0, 1, 0))
    return _U([fork_a, fork_b, pin])


def _column():
    """Tubular upper column, collapsible sleeve, lower shaft, bearings and joints."""
    hub = STEER["wheel_hub"]
    axis_tip = STEER["wheel_axis_tip"]
    axis_vec = (
        axis_tip[0] - hub[0],
        axis_tip[1] - hub[1],
        axis_tip[2] - hub[2],
    )
    axis_len = (axis_vec[0] ** 2 + axis_vec[1] ** 2 + axis_vec[2] ** 2) ** 0.5
    axis = tuple(v / axis_len for v in axis_vec)
    upper = STEER["upper_u_joint"]
    firewall = STEER["firewall_bearing"]  # (1220, 340, 550)
    lower = STEER["lower_u_joint"]  # (895, 292, 350)
    pinion = STEER["pinion_input"]  # (760, 240, 305) - rack spline base
    px, py, pz = pinion

    # Outer column tube stops ~60 mm below the wheel hub so only the thin splined
    # nose of the inner shaft reaches up into the wheel-hub bore (clearance fit).
    nose_base = tuple(hub[i] - axis[i] * 60 for i in range(3))
    upper_outer = C.swept_tube([nose_base, upper, firewall], 22, cap=True)
    inner_shaft = C.swept_tube([hub, upper, firewall], 11, cap=True)

    # Two-piece intermediate shaft down the left side of the bay to the rack,
    # stopping just ABOVE the rack pinion so it never enters the housing.
    lower_shaft = C.swept_tube([firewall, (1080, 326, 478), lower, (px, py, pz + 60)], 15, cap=True)

    collapsible_start = tuple(upper[i] + (hub[i] - upper[i]) * 0.30 for i in range(3))
    collapsible = C.swept_tube([collapsible_start, upper], 28, cap=True)
    firewall_bearing = _cyl(38, 18, (firewall[0] - 9, firewall[1], firewall[2]), (1, 0, 0))
    dash_bracket = _rbox(1465, 304, 664, 72, 72, 34, 6)

    uj_upper = _u_joint(upper)
    uj_firewall = _u_joint(firewall)
    uj_lower = _u_joint(lower)

    # Rack coupler: a pinch-clamp yoke whose bore slip-fits the protruding rack
    # input spline and sits on it ABOVE the pinion housing, so the column meets
    # the rack on a clearance bore instead of spearing the tower.
    coupler = _cyl(18, 42, (px, py, pz + 14), (0, 0, 1)).cut(
        _cyl(13, 54, (px, py, pz + 6), (0, 0, 1)))
    # pinch ear + bolt sit on the +Y side of the sleeve, clear of the spline bore
    # AND of the engine oil pan that sits just inboard (y<=206), so the clamp
    # reads pinched without skewering the spline or clipping the pan.
    pinch = _rbox(px - 9, py + 18, pz + 20, 18, 18, 26, 4)
    pinch_bolt = _cyl(4, 26, (px - 13, py + 22, pz + 33), (1, 0, 0))
    rack_coupler = _U([coupler, pinch, pinch_bolt])

    return _U([
        upper_outer, inner_shaft, lower_shaft, collapsible,
        firewall_bearing, dash_bracket,
        uj_upper, uj_firewall, uj_lower, rack_coupler,
    ])


def parts():
    return [(_column(), COL, "PRT_Steering_Column")]
