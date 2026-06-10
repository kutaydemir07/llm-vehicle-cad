"""Rear LSD differential housing  -  ModelA SportsCar 210 mm LSD.

Dimensions (ManualGearbox 210 LSD):
  Housing OD:  - 280 mm  Length:  - 220 mm
  Centre: x=3320, y=0, z=300 (from POWERTRAIN hardpoints)

CAD mating notes:
  * pinion flange face is centred on POWERTRAIN["prop_rear"].
  * left/right output flanges are centred on POWERTRAIN["diff_output_L/R"].
  * the rear cover and mount pads are built around POWERTRAIN["diff_centre"].
"""
from __future__ import annotations
import math
from vehiclecad.core.reference import common as C
from vehiclecad.geometry import machine_elements as ME
from vehiclecad.parts.powertrain.detail import layout as L

_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
COL   = C.TRANS
FASTENER = (0.13, 0.13, 0.14)
RUBBER = C.RUBBER
GEAR_C = (0.48, 0.49, 0.52)


def _diff_housing():
    """Main iron carrier housing with side-bearing bosses and pinion snout.

    cyl(r, h, base, (0,1,0)): circle in XZ plane centred at base[0], base[2].
    base[1] = y-start of the cylinder.  height goes in +y direction.
    """
    cx, cy_mid, cz = L.DIFF_CENTER
    prop_x, prop_y, prop_z = L.PROPSHAFT_REAR
    out_l = L.DIFF_OUTPUT_L
    out_r = L.DIFF_OUTPUT_R

    #  -  -  central ring-gear housing (240 mm span,  - 120 mm each side)  -  - 
    body  = _cyl(126, 236, (cx, cy_mid - 118, cz), (0, 1, 0))
    inner = _cyl(106, 256, (cx, cy_mid - 128, cz), (0, 1, 0))
    body  = body.cut(inner)

    # Side bearing caps are part of the main carrier casting.  The removable rear
    # cover, pinion flange, and output flanges are separate parts below.
    cover_l = _cyl(130, 16, (cx, cy_mid + 118, cz), (0, 1, 0))
    cover_r = _cyl(130, 16, (cx, cy_mid - 134, cz), (0, 1, 0))

    # Output shafts leave the centre housing and land exactly on the inner CV
    # hardpoints.  They are slightly angled in X, like the real side flanges.
    shaft_l = C.swept_tube([(cx, 126, cz), (out_l[0], out_l[1] - 32, out_l[2])], 30, cap=True)
    shaft_r = C.swept_tube([(cx, -126, cz), (out_r[0], out_r[1] + 32, out_r[2])], 30, cap=True)

    # Pinion nose.  The removable flange is its own mated part.
    pinion = C.swept_tube([(prop_x, prop_y, prop_z), (3300, 0, 304), (cx, 0, cz)], 34, cap=True)

    # mounting ears (to rear subframe bridge)
    ear_l = _rbox(cx - 72,  76, cz - 68, 74, 42, 20, 5)
    ear_r = _rbox(cx - 72, -118, cz - 68, 74, 42, 20, 5)

    return _U([
        body,
        cover_l,
        cover_r,
        shaft_l,
        shaft_r,
        pinion,
        ear_l,
        ear_r,
    ])


def _rear_cover():
    """Finned rear cover, seated on the carrier rear face (the carrier reaches
    x=cx+126); it caps the rear instead of being buried in the housing."""
    cx, cy_mid, cz = L.DIFF_CENTER
    cover = _rbox(cx + 124, -76, cz - 92, 54, 152, 184, 20)
    ribs = [
        C.swept_tube([(cx + 152, y, cz - 76), (cx + 164, y * 0.35, cz + 72)], 6, cap=True)
        for y in (-58, -24, 24, 58)
    ]
    fill = _cyl(10, 8, (cx + 174, 52, cz + 36), (1, 0, 0))
    drain = _cyl(9, 8, (cx + 174, -52, cz - 74), (1, 0, 0))
    top_boss = _cyl(20, 72, (cx + 148, -36, cz + 88), (0, 1, 0))
    return _U([cover, fill, drain, top_boss] + ribs)


def _rear_cover_bolts():
    """Small perimeter fasteners around the removable rear cover."""
    cx, _cy, cz = L.DIFF_CENTER
    bolts = []
    for y, z in ((-66, -76), (-66, -34), (-66, 26), (-66, 68),
                 (66, -76), (66, -34), (66, 26), (66, 68)):
        bolts.append(ME.cap_screw("M8", 8, (cx + 176, y, cz + z), (1, 0, 0)))
    return _U(bolts)


def _pinion_flange():
    """Four-bolt pinion flange mated to the rear propshaft U-joint."""
    prop_x, prop_y, prop_z = L.PROPSHAFT_REAR
    flange = _cyl(48, 18, (prop_x - 18, prop_y, prop_z), (1, 0, 0))
    pilot = _cyl(24, 28, (prop_x - 6, prop_y, prop_z), (1, 0, 0))
    holes = _cyl(18, 34, (prop_x - 22, prop_y, prop_z), (1, 0, 0))
    return flange.cut(holes).fuse(pilot)


def _output_flange(point, side_name):
    """Six-bolt Lobro CV output flange centred on a diff-output hardpoint."""
    x, y, z = point
    flange = _cyl(52, 18, (x, y - 9, z), (0, 1, 0))
    boss = _cyl(27, 28, (x, y - 14, z), (0, 1, 0))
    bolt_lands = []
    for i in range(6):
        a = 2.0 * 3.141592653589793 * i / 6.0
        bolt_lands.append(ME.cap_screw("M8", 10, (x + 36 * math.cos(a), y - 18, z + 36 * math.sin(a)), (0, 1, 0)))
    return _U([flange, boss] + bolt_lands), COL, f"PRT_Rear_LSD_Output_Flange_{side_name}"


def _ring_gear_pinion_set():
    """Crown wheel and pinion visible through the hollow LSD carrier.

    Real final-drive tooth geometry: 41-tooth crown wheel with teeth set at a
    35-degree spiral angle on the gear face, driven by a 13-tooth pinion
    (3.15:1 -- the road final drive), both on the proper tooth form."""
    cx, cy, cz = L.DIFF_CENTER
    ring = _cyl(84, 16, (cx - 4, cy - 8, cz), (0, 1, 0)).cut(
        _cyl(56, 20, (cx - 6, cy - 10, cz), (0, 1, 0))
    )
    teeth = []
    for i in range(41):
        a = 360.0 * i / 41
        tooth = _rbox(cx - 6, cy - 9, cz + 79, 12, 18, 10, 1)
        # spiral angle about the local radial axis, then the polar pattern
        tooth = tooth.rotate((cx, cy, cz + 84), (cx + 1, cy, cz + 84), 35.0)
        teeth.append(tooth.rotate((cx, cy, cz), (cx, cy + 1, cz), a))
    pinion = ME.spur_gear_x(27, 34, 22, L.PROPSHAFT_REAR[0] + 22, 0, L.PROPSHAFT_REAR[2], 13, bore_r=10)
    pinion_shaft = _cyl(11, 118, (L.PROPSHAFT_REAR[0], 0, L.PROPSHAFT_REAR[2]), (1, 0, 0))
    return _U([ring, pinion, pinion_shaft] + teeth)


def _mount_bushes():
    """Rubber-isolated diff mounts seated in the carrier ears and rear cover."""
    cx, _cy, cz = L.DIFF_CENTER
    front_l = ME.bonded_bushing(16, 6, 48, (cx - 35, 72, cz - 58), (0, 1, 0))
    front_r = ME.bonded_bushing(16, 6, 48, (cx - 35, -120, cz - 58), (0, 1, 0))
    rear = ME.bonded_bushing(18, 7, 64, (cx + 148, -32, cz + 88), (0, 1, 0))   # follows the moved top boss
    return _U([front_l, front_r, rear])


def parts():
    out = [(_diff_housing(), COL, "PRT_Rear_LSD_Differential")]
    out.append((_rear_cover(), COL, "PRT_Rear_LSD_Diff_Cover"))
    out.append((_rear_cover_bolts(), FASTENER, "PRT_Rear_LSD_Cover_Bolt_Set"))
    out.append((_pinion_flange(), COL, "PRT_Rear_LSD_Pinion_Flange"))
    out.append((_ring_gear_pinion_set(), GEAR_C, "PRT_Rear_LSD_Ring_Gear_And_Pinion_Set"))
    out.append((_mount_bushes(), RUBBER, "PRT_Rear_LSD_Mount_Bushes"))
    out.append(_output_flange(L.DIFF_OUTPUT_L, "L"))
    out.append(_output_flange(L.DIFF_OUTPUT_R, "R"))
    return out
