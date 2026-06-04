from __future__ import annotations

import cadquery as cq
from cadquery import Solid, Vector, Wire

from vehiclecad.geometry.primitives import as_workplane


def lofted_panel(
    sections: list[cq.Workplane],
    thickness: float | None = None,
    ruled: bool = False,
) -> cq.Workplane:
    if len(sections) < 2:
        raise ValueError("lofted_panel needs at least two section wires")
    panel = sections[0]
    for section in sections[1:]:
        panel = panel.add(section)
    result = panel.loft(ruled=ruled)
    if thickness is not None:
        result = result.shell(thickness)
    return result


def loft_rectangular_stations(
    stations: list[tuple[float, float, float, float]],
    ruled: bool = True,
) -> cq.Workplane:
    """Loft through stations of (x, half_width, z_bottom, z_top)."""
    if len(stations) < 2:
        raise ValueError("loft_rectangular_stations needs at least two stations")

    wires = []
    for x, half_width, z_bottom, z_top in stations:
        points = [
            Vector(x, -half_width, z_bottom),
            Vector(x, half_width, z_bottom),
            Vector(x, half_width, z_top),
            Vector(x, -half_width, z_top),
            Vector(x, -half_width, z_bottom),
        ]
        wires.append(Wire.makePolygon(points))
    return as_workplane(Solid.makeLoft(wires, ruled))


def revolved_profile(profile: cq.Workplane, angle_degrees: float = 360) -> cq.Workplane:
    return profile.revolve(angle_degrees)

