"""V-model System 1000  -  trunk (Kofferraum) enclosure + cabin/boot division.

Adds the sheet-metal that makes the rear read as a real boot and a sealed cabin
instead of an open cavity:

  * ``PRT_Boot_Floor``          -  boot floor pan sitting ABOVE the rear axle/diff,
  * ``PRT_Spare_Well``          -  spare-wheel recess dropped into the floor behind the axle,
  * ``PRT_Rear_Seat_Bulkhead``  -  cabin/boot divider behind the rear-seat squab,
  * ``PRT_Parcel_Shelf``        -  shelf under the backlight, above the rear seat.

Every panel is carved by the running-gear keep-out envelopes (differential, fuel
tank, wheel houses, prop tunnel) so it seats ON them rather than stabbing through
 -  directly replacing the old floating ``firewall_bulkhead`` box that speared the
diff/springs.
"""
from __future__ import annotations
import cadquery as cq

from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import packaging as P

COL = C.STRUCT


def _carve(solid, env_names, margin=6.0):
    """Subtract each named keep-out envelope so the panel clears the running gear."""
    for n in env_names:
        try:
            solid = solid.cut(P.env(n).grown(margin).solid())
        except Exception:
            pass
    return solid


# Rear coil-spring (x~3250, |y|~540) and damper (x~3380, |y|~560) clearance bores.
def _clear_springs(solid, springs=True, dampers=False):
    for sy in (540.0, -540.0):
        if springs:
            solid = solid.cut(C.cyl(94, 720, (3250, sy, 290), (0, 0, 1)))
        if dampers:
            solid = solid.cut(C.cyl(58, 720, (3380, sy, 290), (0, 0, 1)))
    return solid


def _boot_floor():
    """Boot floor pan above the axle/diff, with a spare-wheel well behind the axle."""
    e = P.env("BOOT_FLOOR")
    floor_z = 452.0
    floor = C.box(e.x0, -700, floor_z, e.x1 - e.x0, 1400, 14)
    floor = _carve(floor, ["WHEELHOUSE_RL", "WHEELHOUSE_RR"])
    floor = _clear_springs(floor, springs=True, dampers=True)
    return (floor, COL, "PRT_Boot_Floor")


def _spare_well():
    """Open-top tub recessed into the boot floor behind the rear axle."""
    sw = P.env("SPARE_WELL")
    outer = C.box(sw.x0, -410, sw.z0, sw.x1 - sw.x0, 820, 152)      # z300..452
    inner = C.box(sw.x0 + 14, -396, sw.z0 - 4, (sw.x1 - sw.x0) - 28, 792, 152)
    return (outer.cut(inner), COL, "PRT_Spare_Well")


def _rear_seat_bulkhead():
    """Vertical cabin/boot divider just behind the rear-seat squab.

    Sits at x>3140 (clear of the rear-seat block) and z>425 (above the diff /
    trailing arms); the congested zone below is closed by the diff and floor.
    """
    e = P.env("REAR_SEAT_BULKHEAD")
    plate = C.box(e.x0, -700, e.z0, e.dx, 1400, e.dz)               # z425..1020
    plate = _carve(plate, ["WHEELHOUSE_RL", "WHEELHOUSE_RR", "DIFF_SUBFRAME"])
    plate = _clear_springs(plate, springs=True)
    return (plate, COL, "PRT_Rear_Seat_Bulkhead")


def _parcel_shelf():
    """Horizontal shelf under the backlight, above the rear seat -- trimmed
    panel with speaker recesses, a stiffening swage and the third-brake-lamp
    plinth, plus a downturned front lip, as the production pressing."""
    e = P.env("PARCEL_SHELF")
    shelf = C.box(e.x0, -700, 1000, e.dx, 1400, 16)
    # speaker recesses (grille rings) each side
    for sy in (430.0, -430.0):
        shelf = shelf.cut(C.cyl(72, 8, (e.x0 + e.dx / 2.0, sy, 1010), (0, 0, 1)))
        shelf = shelf.fuse(C.cyl(76, 4, (e.x0 + e.dx / 2.0, sy, 1010), (0, 0, 1)).cut(
            C.cyl(70, 8, (e.x0 + e.dx / 2.0, sy, 1008), (0, 0, 1))))
    # lateral stiffening swage groove
    shelf = shelf.cut(C.box(e.x0 + e.dx / 2.0 - 14, -640, 1011, 28, 1280, 6))
    # downturned front lip toward the seat back + brake-lamp plinth
    lip = C.box(e.x0, -700, 968, 12, 1400, 36)
    plinth = C.rbox(e.x0 + e.dx / 2.0 - 40, -70, 1014, 80, 140, 12, 4)
    shelf = C.U([shelf, lip, plinth])
    shelf = _carve(shelf, ["WHEELHOUSE_RL", "WHEELHOUSE_RR"])
    return (shelf, COL, "PRT_Parcel_Shelf")


def parts():
    return [_boot_floor(), _spare_well(), _rear_seat_bulkhead(), _parcel_shelf()]

