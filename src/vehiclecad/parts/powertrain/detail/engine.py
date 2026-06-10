"""ASM_Powertrain_Packaging  -  I4_Engine engine, ManualGearbox 265, exhaust & driveline.

This module creates volumetric packaging envelopes for every powertrain
component in the Classic ModelA SportsCar.  Each shape is recognizable (not just a bounding
box) and positioned at the skeleton hardpoints in the vehicle frame.

Vehicle frame (see common.py):
    +X rearward (0 = front bumper)
    +Y leftward (0 = centreline)
    +Z upward   (0 = ground)
    Units: millimetres

Parts:
    PRT_I4_Engine_Crankcase_Casting        -  inline-4 iron block casting
    PRT_Intake_Plenum_ITB            -  individual throttle-body intake manifold
    PRT_Exhaust_Manifold_Tubular     -  4-1 tubular header + exhaust system
    PRT_ManualGearbox_265_Transmission      -  5-speed manual gearbox
    PRT_Driveshaft_LSD               -  propshaft, centre bearing, diff, half-shafts
"""
from __future__ import annotations
import math
import numpy as np

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference.hardpoints import POWERTRAIN as PT


# ------------------------------------------------------------------------
#  1.  PRT_I4_Engine_Crankcase_Casting
# ------------------------------------------------------------------------


_BORE_X = (490.0, 613.0, 736.0, 859.0)   # cylinder centreline x (123 mm bore spacing)


def _engine_block() -> list:
    """I4_EngineB23 inline-4 crankcase as a real casting, not a stack of boxes.

    The iron block is a single LOFTED section (rounded corners, lightly tapered
    nose and tail) carrying its bolt-on hardware:
         -  cast crankcase + machined head deck
         -  front timing cover, belt-driven water pump, thermostat neck
         -  grooved crank pulley / harmonic balancer (lofted, on the X axis)
         -  two-stage oil pan with sump bulge and drain plug
         -  spin-on oil filter canister
         -  bellhousing mounting flange, starter motor barrel
         -  four core (freeze) plugs down the exhaust side
         -  dipstick tube and three rubber engine-mount pads
    All geometry stays inside the 380 - 1000 mm block envelope so it never clashes
    with the head (z>660), oil pan (z<380) or rotating assembly.
    """
    parts = []

    #  -  -  cast crankcase (lofted, rounded, tapered nose & tail)  -  -  -  -  -  -  -  -  -  -  -  - 
    block = C.loft([
        (400, 196, 384, 656, 18, 14),
        (470, 208, 382, 660, 22, 16),
        (940, 208, 380, 660, 22, 16),
        (990, 204, 386, 654, 18, 14),
    ])
    deck = C.rbox(404, -210, 644, 586, 420, 16, 6)           # deck top at z660 = head seat
    block = C.U([block, deck])
    # Bore the casting so the rotating assembly runs in clearance - a real hollow
    # iron block, not a billet: a main-bearing crank tunnel on the crank axis and
    # four cylinder bores opening through the deck.
    crank_tunnel = C.cyl(52, 600, (398, 0, 445), (1, 0, 0))   # clears the offset rod journals
    cyl_bores = C.U([C.cyl(48, 210, (bx, 0, 462), (0, 0, 1)) for bx in _BORE_X])
    block = block.cut(crank_tunnel).cut(cyl_bores)
    parts.append((block, C.ENGINE, "PRT_I4_Engine_Crankcase_Casting"))

    #  -  -  front timing cover + water pump + thermostat neck  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    # timing cover seats on the block front (x400), its front face at the crank
    # pulley back (x360); bored on the crank axis so the snout passes in clearance.
    timing_cover = C.rbox(365, -150, 398, 35, 300, 252, 20).cut(
        C.cyl(31, 80, (357, 0, 445), (1, 0, 0)))
    water_pump = C.cyl(48, 64, (360, 150, 486), (-1, 0, 0))   # pump snout, +Y
    pump_pulley = C.loft_circles([((300, 150, 486), 30, (1, 0, 0)),
                                  ((316, 150, 486), 44, (1, 0, 0)),
                                  ((332, 150, 486), 30, (1, 0, 0))])
    thermo = C.cyl(28, 70, (372, -40, 612), (0, -0.3, 1))     # thermostat housing
    parts.append((C.U([timing_cover, water_pump, pump_pulley, thermo]),
                  C.ALLOY_E, "PRT_I4_Engine_Front_Cover"))

    #  -  -  grooved crank pulley / harmonic balancer (lofted on X)  -  -  -  -  -  -  -  -  -  -  - 
    pulley = C.loft_circles([
        ((360, 0, 445), 56, (1, 0, 0)), ((352, 0, 445), 86, (1, 0, 0)),
        ((342, 0, 445), 86, (1, 0, 0)), ((332, 0, 445), 64, (1, 0, 0)),
        ((322, 0, 445), 86, (1, 0, 0)), ((312, 0, 445), 60, (1, 0, 0)),
    ], ruled=True)   # faceted V-grooves; stays within x312-360 (no smooth bulge into cover)
    # hub counterbore + crank bolt with washer on the front face
    pulley = pulley.cut(C.cyl(20, 8, (310, 0, 445), (1, 0, 0)))
    pulley = pulley.fuse(C.cyl(19, 5, (313, 0, 445), (-1, 0, 0)))      # washer
    pulley = pulley.fuse(C.cyl(11, 8, (308, 0, 445), (-1, 0, 0)))      # bolt head
    parts.append((pulley, C.STEEL, "PRT_I4_Engine_Crank_Pulley"))

    #  -  -  two-stage oil pan + drain plug  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    pan_main = C.rbox(404, -176, 322, 352, 352, 57, 22)      # top at z379, under block
    pan_sump = C.rbox(712, -206, 300, 268, 412, 79, 26)      # rear pickup sump
    pan_drain = C.cyl(16, 30, (832, 0, 296), (0, 0, -1))
    parts.append((C.U([pan_main, pan_sump, pan_drain]), C.ENGINE, "PRT_I4_Engine_Oil_Pan"))

    #  -  -  spin-on oil filter canister (front, exhaust side)  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -
    # domed crimped-top can with a fluted wrench band at the base
    _fax = np.array([0.0, -0.18, 1.0]); _fax = _fax / np.linalg.norm(_fax)
    _f0 = np.array([452.0, -258.0, 404.0])
    def _fp(t):
        return tuple(_f0 + _fax * t)
    oil_filter = C.loft_circles([(_fp(0), 46, tuple(_fax)), (_fp(94), 46, tuple(_fax)),
                                 (_fp(110), 39, tuple(_fax)), (_fp(122), 28, tuple(_fax))])
    for k in range(16):
        a = 2 * np.pi * k / 16.0
        rad = np.array([np.cos(a), np.sin(a) * _fax[2], -np.sin(a) * _fax[1]])
        oil_filter = oil_filter.cut(C.cyl(3.5, 26, tuple(_f0 + rad * 47.5 - _fax * 2), tuple(_fax)))
    oil_filter = oil_filter.fuse(C.cyl(10, 6, _fp(-6), tuple(_fax)))   # thread nipple
    parts.append((oil_filter, (0.78, 0.66, 0.12), "PRT_I4_Engine_Oil_Filter"))

    #  -  -  bellhousing flange + starter motor (rear)  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    # thin rear engine plate (8 mm): the flywheel sits BEHIND it, not in it
    flange = C.cyl(150, 8, (990, 0, 455), (1, 0, 0)).cut(
        C.cyl(72, 16, (986, 0, 455), (1, 0, 0)))
    starter = C.cyl(40, 150, (838, -258, 408), (1, 0, 0))    # barrel outboard of block
    starter_nose = C.cyl(30, 40, (978, -244, 430), (1, 0, 0))
    # Bendix drive pinion: same module as the flywheel ring gear (m~2.7,
    # z10), so the tooth geometry is mesh-correct.  (The barrel keeps the
    # historic outboard position dictated by the wide block/sump castings.)
    from vehiclecad.geometry import machine_elements as _ME
    pinion = _ME.spur_gear_x(10.1, 16.1, 16, 1000, -244, 430, 10, bore_r=5)
    parts.append((C.U([flange, starter, starter_nose, pinion]), C.STEEL,
                  "PRT_I4_Engine_Bellhousing_Starter"))

    #  -  -  core (freeze) plugs down the exhaust side  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    plugs = [C.cyl(17, 8, (bx, -210, 520), (0, -1, 0)) for bx in _BORE_X]
    parts.append((C.U(plugs), C.STEEL, "PRT_I4_Engine_Core_Plugs"))

    #  -  -  dipstick tube (bent, exhaust side)  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    dip = C.tube_path([(560, -214, 520), (566, -252, 600), (548, -250, 706)], 5.0)
    parts.append((dip, C.STEEL, "PRT_I4_Engine_Dipstick"))

    #  -  -  engine mount pads  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    mount_pos = {
        "engine_mount_L": PT["engine_mount_L"],
        "engine_mount_R": PT["engine_mount_R"],
        # rear mount bracket pulled outboard of the block (the centreline is filled
        # by the block / pan / bellhousing); it carries the rear of the engine onto
        # the left mount tower instead of burying in the casting.
        "engine_mount_rear": (965, 250, 400),
    }
    for tag, (mx, my, mz) in mount_pos.items():
        pad = C.rbox(mx - 40, my - 35, mz - 20, 80, 70, 40, 8)
        parts.append((pad, C.RUBBER, f"PRT_Engine_Mount_{tag[-1]}"))

    return parts


# ------------------------------------------------------------------------
#  2.  PRT_Intake_Plenum_ITB
# ------------------------------------------------------------------------





def parts():
    out = []
    out.extend(_engine_block())
    return out
