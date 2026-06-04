from __future__ import annotations

import cadquery as cq


def safe_fillet(part: cq.Workplane, radius: float, selector: str | None = None) -> cq.Workplane:
    try:
        edges = part.edges(selector) if selector else part.edges()
        return edges.fillet(radius)
    except Exception:
        return part


def safe_chamfer(part: cq.Workplane, distance: float, selector: str | None = None) -> cq.Workplane:
    try:
        edges = part.edges(selector) if selector else part.edges()
        return edges.chamfer(distance)
    except Exception:
        return part

