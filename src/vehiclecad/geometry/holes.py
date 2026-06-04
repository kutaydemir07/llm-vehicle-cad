from __future__ import annotations

import cadquery as cq

from vehiclecad.interfaces.hole_patterns import HolePattern


def apply_hole_pattern(part: cq.Workplane, pattern: HolePattern) -> cq.Workplane:
    for hole in pattern.holes:
        wp = part.faces(pattern.face_selector).workplane().center(hole.x, hole.y)

        if hole.kind == "through":
            part = wp.hole(hole.diameter)
        elif hole.kind == "blind":
            if hole.depth is None:
                raise ValueError(f"Blind hole needs depth: {hole.name}")
            part = wp.hole(hole.diameter, depth=hole.depth)
        elif hole.kind == "counterbore":
            if hole.depth is None or hole.cbore_diameter is None or hole.cbore_depth is None:
                raise ValueError(f"Counterbore hole needs depth and counterbore dimensions: {hole.name}")
            part = wp.cboreHole(hole.diameter, hole.cbore_diameter, hole.cbore_depth, depth=hole.depth)
        elif hole.kind == "countersink":
            if hole.depth is None or hole.csk_diameter is None:
                raise ValueError(f"Countersink hole needs depth and csk diameter: {hole.name}")
            part = wp.cskHole(hole.diameter, hole.csk_diameter, hole.csk_angle, depth=hole.depth)
        else:
            raise ValueError(f"Unknown hole kind: {hole.kind}")

    return part

