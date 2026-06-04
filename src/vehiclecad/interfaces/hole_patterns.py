from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


HoleKind = Literal["through", "blind", "counterbore", "countersink"]


@dataclass(frozen=True)
class Hole:
    name: str
    x: float
    y: float
    diameter: float
    kind: HoleKind = "through"
    depth: float | None = None
    cbore_diameter: float | None = None
    cbore_depth: float | None = None
    csk_diameter: float | None = None
    csk_angle: float = 90.0


@dataclass(frozen=True)
class HolePattern:
    name: str
    face_selector: str
    holes: list[Hole]


def rectangular_four_bolt_pattern(
    name: str,
    x_spacing: float,
    y_spacing: float,
    diameter: float,
    face_selector: str = ">Z",
) -> HolePattern:
    hx = x_spacing / 2.0
    hy = y_spacing / 2.0
    return HolePattern(
        name=name,
        face_selector=face_selector,
        holes=[
            Hole("front_left", hx, hy, diameter),
            Hole("front_right", hx, -hy, diameter),
            Hole("rear_left", -hx, hy, diameter),
            Hole("rear_right", -hx, -hy, diameter),
        ],
    )

