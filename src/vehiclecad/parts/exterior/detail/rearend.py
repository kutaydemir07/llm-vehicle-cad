"""Rear-end module for the ModelA SportsCar -- built as a real, non-clashing assembly.

Same discipline as the front:
  * `body_cutters()` opens the tail-lamp apertures in the body tail face, so
    the lamps drop into real holes.  The centre trim sits on solid tail metal
    instead of cutting a see-through boot opening.
  * the lower rear (below the lamp line) is ONE coherent body-colour bumper +
    valance behind the body face -- its own clean volume, with a plate recess
    and an exhaust cut-out.
  * each tail lamp = black housing + ribbed red lens + amber + reverse sections.
  * the signature wing is owned by the aero assembly.  Exhaust parts are owned
    by the powertrain exhaust; this module only leaves the bumper cut-out.
"""
from __future__ import annotations
import cadquery as cq
from vehiclecad.core.reference import common as C

X_FACE = 4338.0     # tail-lamp face (body rear face ~4340)
TL_Z0, TL_Z1 = 600.0, 770.0
TL_Y0, TL_Y1 = 186.0, 560.0
CP_Y = 180.0        # centre-panel half-width


def body_cutters():
    """Tail-lamp apertures subtracted from the body tail face.

    The centre panel on an E30-style tail is trim mounted over solid body metal;
    cutting that area through the body makes the rear exterior cover a structural
    hole instead of mating to a supported face.
    """
    cuts = []
    for s in (1, -1):
        ylo = TL_Y0 if s > 0 else -TL_Y1
        cuts.append(C.box(4300, ylo, TL_Z0 - 4, 80, TL_Y1 - TL_Y0, (TL_Z1 - TL_Z0) + 8))
    return cuts


def _tail_lamp(s, out):
    """One tail-lamp cluster that FILLS its aperture flush -- no proud floating
    lens over a dark see-through gap.  The coloured lenses span the whole opening
    (~1.5 mm reveal) and seat at the body face; a black housing butts in behind
    them so nothing shows through into the body cavity.  ModelA layout: amber turn
    band across the top, large ribbed red brake/tail, white reverse inboard-low.
    """
    side = "L" if s > 0 else "R"
    y0 = TL_Y0 if s > 0 else -TL_Y1
    w = TL_Y1 - TL_Y0
    z0, z1 = TL_Z0, TL_Z1
    yi, wi = y0 + 1.5, w - 3.0                 # 1.5 mm reveal inside the aperture
    zi0, zi1 = z0 + 1.5, z1 - 1.5
    # black housing fills the aperture from behind up to the body face
    out.append((C.box(4306, y0 - 3, z0 - 5, 32, w + 6, (z1 - z0) + 10),
                C.BLACK, f"taillamp_housing_{side}"))
    # lens block fills the opening; front sits ~6 mm proud of the 4338 tail face
    lf0, lf1 = 4332.0, 4344.0                  # lens x-span (back butts the housing)
    amber_h = 30.0
    rev_w, rev_h = 124.0, 40.0
    rev_y = yi if s > 0 else (yi + wi - rev_w)   # reverse sits INBOARD (near plate)
    amber = C.box(lf0, yi, zi1 - amber_h, lf1 - lf0, wi, amber_h)
    reverse = C.box(lf0, rev_y, zi0, lf1 - lf0, rev_w, rev_h)
    red = (C.box(lf0, yi, zi0, lf1 - lf0, wi, zi1 - zi0)
           .cut(amber).cut(reverse))
    # shallow horizontal rib grooves on the red lens face (texture, not gaps)
    ribs = C.U([C.box(lf1 - 4, yi, zi0 + 30 + 40 * k, 8, wi, 5) for k in range(3)])
    out.append((red.cut(ribs), C.TAILR, f"taillamp_red_{side}"))
    out.append((amber, C.AMBER, f"taillamp_amber_{side}"))
    out.append((reverse, C.TAILW, f"taillamp_reverse_{side}"))
    # thin satin-black divider trim around the cluster edge (frames the lens)
    frame = (C.box(lf0 - 1, y0, z0, 6, w, z1 - z0)
             .cut(C.box(lf0 - 2, yi, zi0, 10, wi, zi1 - zi0)))
    out.append((frame, C.TRIM_BLK, f"taillamp_trim_{side}"))


def parts():
    out = []

    # Rear carrier trim is an aperture-local backing frame sitting just outside
    # the tail panel.  It avoids occupying the boot floor / spare-well structure.
    lamp_frame_l = C.rbox(4344, TL_Y0 - 12, TL_Z0 - 10, 16, TL_Y1 - TL_Y0 + 24, TL_Z1 - TL_Z0 + 20, 5)
    lamp_frame_r = C.mirror_y(lamp_frame_l)
    centre_frame = C.rbox(4344, -CP_Y - 10, TL_Z0 - 12, 16, 2 * (CP_Y + 10), TL_Z1 - TL_Z0 + 24, 5)
    rear_carrier = C.U([lamp_frame_l, lamp_frame_r, centre_frame])
    rear_carrier = rear_carrier.cut(C.box(4338, -558, TL_Z0 + 1, 28, 1116, TL_Z1 - TL_Z0 - 2))
    out.append((rear_carrier, C.BLACK, "rear_core_support"))

    # --- full-width tail lamps + black centre panel with roundel + script ---
    for s in (1, -1):
        _tail_lamp(s, out)
    out.append((C.box(X_FACE + 8, -CP_Y, TL_Z0 - 6, 18, 2*CP_Y, (TL_Z1 - TL_Z0) + 12),
                C.BLACK, "tail_centre_panel"))
    for s, rgb, nm in C.roundel((X_FACE + 34, 0, TL_Z1 - 44), "+x", r=30):
        out.append((s, rgb, "rear_" + nm))
    out.append((C.box(X_FACE + 28, -120, TL_Z0 + 14, 10, 240, 26), C.CHROME, "model_script"))

    # === ONE coherent rear bumper + valance, behind the body ===
    # A LAP FLANGE reaches FORWARD under the body's lower tail edge (z~540-600) so
    # the bumper is bolted to the body instead of touching it on a single plane.
    bumper = C.rbox(4338, -752, 366, 50, 1504, 206, 10)        # flat bumper band, x4338-4388 z366-572
    valance = C.rbox(4338, -742, 193, 38, 1484, 190, 8)        # lower valance DOWN TO the rocker (z193)
    lap = C.rbox(4312, -706, 368, 32, 1412, 80, 6)             # short return flange at tail edge
    rear = (cq.Workplane(obj=bumper).union(cq.Workplane(obj=valance))
            .union(cq.Workplane(obj=lap)).clean().val())
    rear = rear.cut(C.box(3240, -710, 292, 1080, 1420, 190))          # boot floor / spare-well relief
    rear = rear.cut(C.box(3420, -760, 585, 930, 1520, 452))           # tail-panel lamp-zone relief
    rear = rear.cut(C.box(4360, -200, 392, 80, 400, 150))               # plate recess opening
    exhaust_slot = C.rbox(4328, -398, 202, 96, 244, 120, 18)
    rear = rear.cut(exhaust_slot)                                      # twin-tip exhaust relief
    out.append((rear, C.RED, "rear_bumper"))
    out.append((C.box(4332, -742, 470, 22, 1484, 32), C.TRIM_BLK, "rear_bumper_strip"))

    # number plate (recessed) + lamp
    out.append((C.box(4392, -180, 398, 12, 360, 138), C.BLACK, "plate_recess"))
    out.append((C.box(4398, -172, 406, 8, 344, 122), (0.86, 0.86, 0.82), "number_plate"))

    # rear reflectors set into the valance
    for s in (1, -1):
        side = "L" if s > 0 else "R"
        out.append((C.box(4392, s*470 - 70, 330, 12, 140, 60), C.TAILR, f"rear_reflector_{side}"))

    # NOTE: trunk spoiler / wing / pedestals / endplates are owned by
    # Wing and deck aero are owned by their own detail modules to avoid duplicates.

    return out

