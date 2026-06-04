"""Packaging keep-out envelopes - the "reserve space for the neighbours" layer.

Real CAD is bottom-up AND packaging-aware: before you detail a part you reserve
the *space* it (and its neighbours) are allowed to occupy, so two systems can be
designed independently and still not fight over the same volume.  This project
never had that layer - every part was sized in isolation and dropped at an
absolute coordinate, so the exhaust ended up inside the floor and the rear
bulkhead box speared the differential.

This module is that missing layer.  Each major mass gets a named *envelope*
(an axis-aligned keep-out volume in the vehicle frame), all derived from the
single source of truth ``hardpoints.DT`` so they move with the design table.
Subsystems then:

  * size / clip their parts to fit inside their own envelope  (``clip_to``)
  * assert they do not poke out of it                          (``outside_volume``)
  * assert they stay clear of a neighbour's envelope           (``clearance`` / ``overlap_volume``)

Vehicle frame (see materials.py): +X = rearward (0 at front bumper tip),
+Y = leftward (0 = centreline), +Z = up (0 = ground).  Millimetres.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import cadquery as cq
from cadquery import Solid, Vector

from .hardpoints import DT


# ------------------------------------------------------------------------
#  Envelope type
# ------------------------------------------------------------------------
@dataclass(frozen=True)
class Env:
    """An axis-aligned keep-out volume, ``[x0,x1] x [y0,y1] x [z0,z1]`` (mm)."""

    name: str
    x0: float
    x1: float
    y0: float
    y1: float
    z0: float
    z1: float

    #  -  derived  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    @property
    def dx(self) -> float:
        return self.x1 - self.x0

    @property
    def dy(self) -> float:
        return self.y1 - self.y0

    @property
    def dz(self) -> float:
        return self.z1 - self.z0

    @property
    def center(self):
        return ((self.x0 + self.x1) / 2.0,
                (self.y0 + self.y1) / 2.0,
                (self.z0 + self.z1) / 2.0)

    @property
    def volume(self) -> float:
        return max(0.0, self.dx) * max(0.0, self.dy) * max(0.0, self.dz)

    def solid(self) -> Solid:
        """The envelope as a CadQuery box solid (for boolean ops / rendering)."""
        return Solid.makeBox(self.dx, self.dy, self.dz, Vector(self.x0, self.y0, self.z0))

    def contains_point(self, p, tol: float = 0.0) -> bool:
        x, y, z = p
        return (self.x0 - tol <= x <= self.x1 + tol
                and self.y0 - tol <= y <= self.y1 + tol
                and self.z0 - tol <= z <= self.z1 + tol)

    def grown(self, m: float) -> "Env":
        """Return a copy expanded by ``m`` mm on every face (clearance margin)."""
        return Env(self.name, self.x0 - m, self.x1 + m, self.y0 - m, self.y1 + m,
                   self.z0 - m, self.z1 + m)

    def mirrored(self, name: str | None = None) -> "Env":
        """Reflect across the centreline (Y -> -Y) for the opposite side."""
        return Env(name or self.name, self.x0, self.x1, -self.y1, -self.y0, self.z0, self.z1)


# ------------------------------------------------------------------------
#  Envelope definitions  - derived from the design table
# ------------------------------------------------------------------------
def _build_envelopes() -> Dict[str, Env]:
    axF = DT.axle_front_x          # 810
    axR = DT.axle_rear_x           # 3372
    L = DT.overall_length          # 4360
    tr = DT.tire_radius            # 300
    half_track_f = DT.track_front / 2.0   # 706
    half_track_r = DT.track_rear / 2.0    # 720

    FIREWALL = 1220.0              # engine bay / cabin split (DATUMS "firewall")
    REAR_BULKHEAD = 3244.0         # cabin / boot split
    FLOOR_Z = 220.0                # top of the floorpan pressing

    envs = [
        #  -  front structure / mechanicals  -  -  -  -  -  -  -  -  -  -  -  - 
        Env("ENGINE_BAY",       260, FIREWALL,  -430, 430,  235, 905),
        Env("COWL_PLENUM",      FIREWALL - 40, 1300,  -430, 430,  880, 985),
        # Radiator / slam-panel zone closing the bay front behind the grille
        # (forward of the fan x250 and the front crossmember x312).
        Env("RAD_SUPPORT",      140, 215,  -445, 445,  235, 905),
        # Inner-fender apron band: bay side wall over each front wheel house
        # (left; mirrored for right).  Ties the strut tower to the rad support.
        Env("INNER_FENDER_L",   340, FIREWALL,  395, 612,  280, 905),

        #  -  central spine  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -
        # Driveshaft tunnel: gearbox tailhousing -> diff nose, narrow + low.
        Env("TRANS_TUNNEL",     1000, 3300,  -150, 150,  150, 365),
        # Exhaust runs UNDER the floorpan (z below FLOOR_Z): collector -> tail.
        Env("EXHAUST_CORRIDOR", 950,  L,     -320, 300,  118, FLOOR_Z - 5),

        #  -  cabin  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
        Env("CABIN_FLOORPAN",   FIREWALL, REAR_BULKHEAD,  -700, 700,  200, 270),
        Env("FOOTWELL_L",       FIREWALL, 1640,   120, 660,  175, 320),
        Env("FOOTWELL_R",       FIREWALL, 1640,  -660, -120, 175, 320),

        #  -  rear structure / mechanicals  -  -  -  -  -  -  -  -  -  -  -  - -
        # Fuel tank sits ahead of the rear axle, under the rear seat (ModelA).
        Env("FUEL_TANK_WELL",   3040, 3420,  -360, 360,  225, 430),
        # Final-drive + subframe carrier zone around the diff centreline.
        Env("DIFF_SUBFRAME",    3170, 3530,  -540, 540,  170, 430),
        # Spare-wheel / boot floor recess behind the axle.
        Env("SPARE_WELL",       3540, 4150,  -420, 420,  300, 540),
        # Boot (Kofferraum) volume: floor pan above the rear running gear.
        Env("BOOT_FLOOR",       REAR_BULKHEAD, 4310,  -740, 740,  300, 575),
        # Parcel shelf under the backlight, above the rear seat.
        Env("PARCEL_SHELF",     3040, REAR_BULKHEAD,  -700, 700,  978, 1040),
        # Rear-seat bulkhead: cabin / boot divider just behind the rear-seat squab
        # (x>3140 clears the seat block; z>425 clears the diff / trailing arms).
        Env("REAR_SEAT_BULKHEAD", 3142, 3196,  -700, 700,  425, 1020),

        #  -  front strut towers (left; mirror for right)  -  -  -  -  -  -  - -
        Env("STRUT_TOWER_FL",   axF - 120, axF + 120,  455, 615,  300, 965),
    ]

    # Wheel houses: a generous keep-out around each tyre's swept volume.
    arch_r = tr + 70.0             # 370 mm radius reservation
    for tag, ax, hy in (("F", axF, half_track_f), ("R", axR, half_track_r)):
        for s in (1, -1):
            side = "L" if s > 0 else "R"
            cy = s * hy
            envs.append(Env(
                f"WHEELHOUSE_{tag}{side}",
                ax - arch_r, ax + arch_r,
                min(cy - 150.0, cy + 150.0), max(cy - 150.0, cy + 150.0),
                0.0, tr + arch_r,
            ))

    out = {e.name: e for e in envs}
    # Mirror the single-sided definitions to the right side.
    out["STRUT_TOWER_FR"] = out["STRUT_TOWER_FL"].mirrored("STRUT_TOWER_FR")
    out["INNER_FENDER_R"] = out["INNER_FENDER_L"].mirrored("INNER_FENDER_R")
    return out


ENVELOPES: Dict[str, Env] = _build_envelopes()


def env(name: str) -> Env:
    """Look up an envelope by name (KeyError if undefined)."""
    return ENVELOPES[name]


# ------------------------------------------------------------------------
#  Checks / operations  (the discipline: fit inside yours, stay clear of theirs)
# ------------------------------------------------------------------------
def clip_to(solid, e: Env, margin: float = 0.0):
    """Trim ``solid`` so it cannot exceed envelope ``e`` (optionally grown by
    ``margin``).  Returns the intersection, or the original on boolean failure."""
    try:
        box = e.grown(margin).solid() if margin else e.solid()
        result = solid.intersect(box)
        if result.Volume() > 0.1:
            return result
    except Exception:
        pass
    return solid


def outside_volume(solid, e: Env, margin: float = 0.0) -> float:
    """Volume (mm^3) of ``solid`` that pokes OUTSIDE envelope ``e``.

    0 means the part is fully contained - the test a packaging-correct part
    should pass.  Use ``margin`` to allow a small tolerance band.
    """
    try:
        box = e.grown(margin).solid() if margin else e.solid()
        return float(solid.cut(box).Volume())
    except Exception:
        return 0.0


def overlap_volume(a, b) -> float:
    """Exact interference volume (mm^3) between two solids (0 = no clash)."""
    try:
        return float(a.intersect(b).Volume())
    except Exception:
        return 0.0


def clearance(a, b) -> float:
    """Approximate gap between two solids' bounding boxes (mm).

    Negative means the boxes overlap on every axis (a likely clash - confirm with
    ``overlap_volume``).  Bounding-box based so it is fast and never throws; use
    it as a cheap first-pass packaging check, not a precise minimum distance.
    """
    ba, bb = a.BoundingBox(), b.BoundingBox()
    dx = max(ba.xmin - bb.xmax, bb.xmin - ba.xmax)
    dy = max(ba.ymin - bb.ymax, bb.ymin - ba.ymax)
    dz = max(ba.zmin - bb.zmax, bb.zmin - ba.zmax)
    # If separated on any axis, the gap is that axis' positive distance.
    gaps = [g for g in (dx, dy, dz) if g > 0]
    if gaps:
        return float(max(gaps))
    return float(max(dx, dy, dz))   # all <= 0: boxes interpenetrate


def report(parts, mapping: Dict[str, str], margin: float = 5.0) -> list:
    """Audit a flat ``[(solid, rgb, name), ...]`` list against assigned envelopes.

    ``mapping`` is ``part_name -> envelope_name``.  Returns a list of
    ``(part_name, envelope_name, outside_msportscar)`` for parts that poke out by more
    than a litre, so a subsystem can self-check its packaging during a build.
    """
    flags = []
    for item in parts:
        solid, name = item[0], item[2]
        env_name = mapping.get(name)
        if not env_name or env_name not in ENVELOPES:
            continue
        ov = outside_volume(solid, ENVELOPES[env_name], margin=margin)
        if ov > 1000.0:
            flags.append((name, env_name, ov))
    return flags
