from __future__ import annotations

import cadquery as cq


def solid_volume_msportscar(model: cq.Assembly | cq.Workplane) -> float:
    if isinstance(model, cq.Assembly):
        return model.toCompound().Volume()
    return model.val().Volume()

