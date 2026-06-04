from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class BoundingBoxDimensions:
    x: float
    y: float
    z: float


def assembly_dimensions(assembly: cq.Assembly) -> BoundingBoxDimensions:
    bb = assembly.toCompound().BoundingBox()
    return BoundingBoxDimensions(bb.xlen, bb.ylen, bb.zlen)


def workplane_volume(part: cq.Workplane) -> float:
    return part.val().Volume()

