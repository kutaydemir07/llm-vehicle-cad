"""ASM_Chassis_BiW  -  Body-in-White structural module.

Creates the INTERNAL STRUCTURAL components of the ModelA SportsCar  -  the hidden
skeleton underneath the outer body shell.  These are the parts that provide
structural rigidity, mount the suspension, support the engine, and protect
the occupants.

Parts
-----
PRT_Floorpan_Main            -  floor plate + raised driveshaft tunnel
PRT_Firewall_Bulkhead        -  engine-bay / cabin divider with pass-throughs
PRT_Roof_Panel               -  roof skin (slight crown)
PRT_C_Pillar_Modified_L/R    -  SportsCar-specific wider/shallower C-pillars
PRT_Strut_Tower_Front_L/R    -  reinforced front strut towers with gussets
PRT_Strut_Tower_Rear_L/R     -  rear strut towers
PRT_Rocker_Rail_L/R          -  box-section sill members under the doors
PRT_Rear_Wheel_Tub_L/R       -  sheet-metal tubs inside the rear quarters
"""
from __future__ import annotations

import math
import cadquery as cq
from cadquery import Solid, Vector

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK

# shorthand
_box = C.box
_cyl = C.cyl
_U   = C.U
_mirror = C.mirror_y
_plate = C.thick_plate
_shell = C.shell_box
_tapered = C.tapered_box
_xzp = C.xz_prism
COL  = C.STRUCT


# ------------------------------------------------------------------------
#  1. PRT_Floorpan_Main
# ------------------------------------------------------------------------

def _floorpan():
    """Main floor structure from firewall (x - 1220) to rear seat-back (x - 3450).

    - Flat plate at z=220, 1.5 mm thick, spanning y= - 740
    - Raised centre tunnel (y= - 100) for the driveshaft, top at z - 350
    - Slightly recessed driver / passenger footwells (z=215, 5 mm drop)
    """
    # --- skeleton references ---
    x0 = SK.CHASSIS["floor_front"][0]       # 1220
    x1 = SK.CHASSIS["floor_rear"][0]        # 3450
    floor_z = SK.CHASSIS["floor_front"][2]  # 220
    t_hw = SK.CHASSIS["tunnel_width"][1]    # 100  (half-width of tunnel)
    t = 1.5   # sheet-metal thickness

    dx = x1 - x0                            # 2230
    half_w = 740.0                           # y =  - 740

    # --- main floor plate (full width) ---
    floor = _plate(x0, -half_w, floor_z, dx, 2 * half_w, t)

    # --- recessed footwells (5 mm drop, inboard of rocker) ---
    fw_drop = 5.0
    # driver footwell (left side)
    fw_l = _plate(x0, 120, floor_z - fw_drop, 650, 540, t)
    # passenger footwell (right side)
    fw_r = _plate(x0, -660, floor_z - fw_drop, 650, 540, t)

    # --- driveshaft tunnel ---
    tunnel_top_z = 480.0
    tunnel_h = tunnel_top_z - floor_z       # 130
    # left wall
    tw_l = _box(x0, t_hw - t, floor_z, dx, t, tunnel_h)
    # right wall
    tw_r = _box(x0, -t_hw, floor_z, dx, t, tunnel_h)
    # tunnel top plate
    tw_top = _plate(x0, -t_hw, tunnel_top_z, dx, 2 * t_hw, t)

    floorpan = _U([floor, fw_l, fw_r, tw_l, tw_r, tw_top])

    # Rear wheelhouse and rear-carrier clearance: the cabin floor does not run
    # as a full-width slab through the tyre, hub, rotor, or rear subframe sweep.
    rear_left_cut = _box(3035, 590, 150, 470, 270, 330)
    rear_right_cut = _mirror(rear_left_cut)
    carrier_cut = _box(2860, -565, 150, 470, 1130, 230)

    # Pedal box and toe-board clearance at the firewall.
    pedal_cut = _box(1210, -20, 235, 165, 585, 330)

    # The transmission tunnel is OPEN from below (the arch straddles the
    # gearbox/propshaft); the full-width base plate must not close its bottom.
    tunnel_bottom_cut = _box(x0 + 2, -(t_hw - t), floor_z - 10,
                             dx - 4, 2 * (t_hw - t), 12)

    for cutter in (rear_left_cut, rear_right_cut, carrier_cut, pedal_cut,
                   tunnel_bottom_cut):
        floorpan = floorpan.cut(cutter)
    return floorpan


def parts():
    out = []
    out.append((_floorpan(), COL, "PRT_Floorpan_Main"))
    return out

