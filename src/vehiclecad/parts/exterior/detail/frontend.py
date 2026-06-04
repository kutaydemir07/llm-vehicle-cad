"""Front-end module for the ModelA SportsCar -- built as a real, non-clashing assembly.

Assembly logic (no more interpenetration):
  * `body_cutters()` returns the headlamp + grille apertures that `body.py`
    subtracts from the shell, so the lamps/grille drop into real holes.
  * the lower front (below the lamp line) is ONE coherent body-colour fascia
    (bumper + air dam) sitting FORWARD of the body face -- its own clean volume.
  * each lamp = reflector bowl + bulb + ribbed lens + chrome bezel, sized to its
    aperture; the grille fills the central aperture; fog lamps fill fascia holes.

Frame: +x rear, lower x = further forward.  Body front face sits at x~60.
"""
from __future__ import annotations
import numpy as np
import cadquery as cq
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C

Z_LAMP = 700.0
LAMPS = (("in", 248.0, 76.0), ("out", 466.0, 92.0))     # (tag, |y|, radius)
GR_Z0, GR_Z1, GR_Y = 614.0, 792.0, 150.0                # grille aperture
REFLECTOR = C.CHROME


def _cone(r1, r2, h, x, y, z):
    return Solid.makeCone(r1, r2, h, Vector(x, y, z), Vector(1, 0, 0))


def body_cutters():
    """Apertures subtracted from the body shell (so inserts fit real holes).

    Depth is just enough to clear the lamp/grille inserts; a deeper bore only
    tunnels into the solid body tool and reads as a dark hole behind the lens.
    """
    cuts = []
    for s in (1, -1):
        for _tag, yy, r in LAMPS:
            cuts.append(C.cyl(r + 8, 98, (38, s*yy, Z_LAMP), (1, 0, 0)))
    cuts.append(C.box(40, -GR_Y, GR_Z0, 96, 2*GR_Y, GR_Z1 - GR_Z0))       # grille
    return cuts


def _lamp(s, tag, yy, r, out):
    side = "L" if s > 0 else "R"
    cy = s * yy
    # reflector bowl, CLOSED at the back with a cap disc so the lens never shows
    # the dark body cavity behind it (the old open bowl was the 'empty space').
    shell = _cone(r, 0.52*r, 42, 78, cy, Z_LAMP).cut(_cone(r-8, 0.52*r-8, 46, 72, cy, Z_LAMP))
    cap = C.cyl(0.52*r + 2, 6, (118, cy, Z_LAMP), (1, 0, 0))            # bowl backing
    out.append((shell.fuse(cap), REFLECTOR, f"reflector_{tag}_{side}"))
    out.append((C.cyl(8, 24, (116, cy, Z_LAMP), (-1, 0, 0)), C.LIGHT, f"bulb_{tag}_{side}"))
    # clear ribbed lens, seated at the body face and filling the bowl mouth
    lens = C.cyl(r-1, 9, (60, cy, Z_LAMP), (1, 0, 0))
    lens = lens.cut(C.cyl(0.7*r+1.5, 12, (57, cy, Z_LAMP), (1, 0, 0)).cut(
        C.cyl(0.7*r-1.5, 14, (55, cy, Z_LAMP), (1, 0, 0))))
    out.append((lens, C.LIGHT, f"headlamp_lens_{tag}_{side}"))
    # chrome bezel ring closes the reveal between lens and aperture edge
    bez = C.cyl(r+8, 13, (55, cy, Z_LAMP), (1, 0, 0)).cut(C.cyl(r-2, 18, (51, cy, Z_LAMP), (1, 0, 0)))
    out.append((bez, C.CHROME, f"headlamp_bezel_{tag}_{side}"))


def parts():
    out = []

    # Black front carrier trim sits ahead of the BiW radiator support.  It is a
    # picture-frame carrier around the lamps/grille, not a second solid rad panel.
    carrier_outer = C.rbox(126, -700, 214, 14, 1400, 612, 6)
    radiator_relief = C.box(118, -438, 326, 32, 876, 506)
    lamp_reliefs = [
        C.cyl(r + 14, 34, (116, s * yy, Z_LAMP), (1, 0, 0))
        for s in (1, -1)
        for _tag, yy, r in LAMPS
    ]
    grille_relief = C.box(118, -(GR_Y + 18), GR_Z0 - 18, 32, 2 * (GR_Y + 18), GR_Z1 - GR_Z0 + 36)
    front_carrier = carrier_outer.cut(radiator_relief).cut(grille_relief)
    for cutter in lamp_reliefs:
        front_carrier = front_carrier.cut(cutter)
    out.append((front_carrier, C.BLACK, "front_core_support"))

    # --- quad round headlamps (fit the body apertures) ---
    for s in (1, -1):
        for tag, yy, r in LAMPS:
            _lamp(s, tag, yy, r, out)

    # --- twin-kidney grille filling the central aperture ---
    for j, (y0, y1) in enumerate(((18, GR_Y - 4), (-(GR_Y - 4), -18))):
        w = y1 - y0
        frame = (C.rbox(50, y0 - 8, GR_Z0 - 4, 30, w + 16, (GR_Z1 - GR_Z0) + 8, 10)
                 .cut(C.box(40, y0, GR_Z0 + 6, 60, w, (GR_Z1 - GR_Z0) - 12)))
        out.append((frame, C.CHROME, f"kidney_frame_{j}"))
        # Backing spans the FULL half-aperture (out to the centreline and the
        # surround edge), not just the slat block, so the nose opening is not a
        # see-through hole into the engine bay / body cavity.
        by0 = 0.0 if j == 0 else -GR_Y
        out.append((C.box(96, by0, GR_Z0, 22, GR_Y, (GR_Z1 - GR_Z0)), C.BLACK, f"kidney_back_{j}"))
        nsl = 9
        slats = [C.box(64, y0 + 6 + k*(w-12)/(nsl-1) - 1.5, GR_Z0 + 8, 30, 3, (GR_Z1 - GR_Z0) - 16)
                 for k in range(nsl)]
        out.append((C.U(slats), C.CHROME, f"kidney_slats_{j}"))

    # --- hood roundel above the grille ---
    for s, rgb, nm in C.roundel((52, 0, GR_Z1 + 48), "-x", r=26):
        out.append((s, rgb, nm))

    # === ONE coherent front fascia (bumper + air dam), forward of the body ===
    # The bumper bulge sits forward of the body face; a LAP FLANGE behind it tucks
    # up under the body's lower front edge (z~540-600) so the fascia is bolted to
    # the body, not floating on a 4 mm sliver.  The flange is hidden behind the
    # bumper / body lower front, below the headlamp line (z<600).
    bumper = C.rbox(14, -752, 366, 52, 1504, 206, 10)         # flat bumper band, x14-66 z366-572
    dam = C.rbox(26, -742, 193, 40, 1484, 190, 8)             # lower valance DOWN TO the rocker (z193)
    lip_return = C.rbox(58, -708, 366, 80, 1416, 70, 6)       # upper return, clear of radiator support
    side_mount_l = C.rbox(58, 596, 420, 78, 100, 106, 5)
    side_mount_r = C.mirror_y(side_mount_l)
    fascia = (cq.Workplane(obj=bumper).union(cq.Workplane(obj=dam))
              .union(cq.Workplane(obj=lip_return))
              .union(cq.Workplane(obj=side_mount_l))
              .union(cq.Workplane(obj=side_mount_r)).clean().val())
    fascia = fascia.cut(C.box(-12, -286, 224, 110, 572, 150))           # central intake
    fascia = fascia.cut(C.box(120, -440, 326, 50, 880, 500))            # BiW radiator-support relief
    for s in (1, -1):
        fascia = fascia.cut(C.cyl(46, 120, (-12, s*328, 300), (1, 0, 0)))     # fog apertures
        fascia = fascia.cut(C.box(-12, s*566 - 64, 250, 110, 128, 96))        # brake-duct slots
    out.append((fascia, C.RED, "front_fascia"))

    # bumper rub strip + splitter.  The splitter blade includes an upstand and
    # small bolt pads that tuck into the lower valance so it no longer reads as
    # a separate floating plate when viewed from the front.
    out.append((C.box(2, -742, 470, 22, 1484, 34), C.TRIM_BLK, "front_bumper_strip"))
    splitter_blade = C.rbox(-2, -728, 138, 50, 1456, 30, 12)
    splitter_upstand = C.rbox(34, -708, 164, 28, 1416, 42, 6)
    splitter_bolt_pads = C.U([
        C.rbox(28, -560 + i * 280, 184, 42, 82, 22, 5)
        for i in range(5)
    ])
    out.append((C.U([splitter_blade, splitter_upstand, splitter_bolt_pads]),
                C.TRIM_BLK, "front_splitter"))

    # central intake mesh (recessed black + crosshatch)
    out.append((C.box(52, -282, 228, 12, 564, 142), C.BLACK, "intake_back"))
    vbars = [C.box(46, -286 + 57*k, 230, 14, 6, 138) for k in range(11)]
    hbars = [C.box(46, -286, 230 + 46*k, 14, 572, 6) for k in range(4)]
    out.append((C.U(vbars + hbars), C.TRIM_BLK, "intake_mesh"))

    # fog lamps (fill fascia holes) + brake-duct backs
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        out.append((C.cyl(45, 16, (4, s*328, 300), (-1, 0, 0)).cut(C.cyl(37, 22, (0, s*328, 300), (-1, 0, 0))),
                    C.CHROME, f"foglamp_ring_{side}"))
        out.append((C.cyl(38, 20, (8, s*328, 300), (-1, 0, 0)), C.LIGHT, f"foglamp_{side}"))
        out.append((C.box(40, s*566 - 60, 254, 14, 120, 88), C.BLACK, f"brake_duct_back_{side}"))

    # amber corner indicators set into the bumper ends
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        out.append((C.rbox(4, s*648 - 76, 410, 56, 150, 96, 16), C.AMBER, f"turn_signal_{side}"))

    return out

