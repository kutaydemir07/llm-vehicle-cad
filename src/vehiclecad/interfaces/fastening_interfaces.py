from __future__ import annotations

from dataclasses import dataclass

from vehiclecad.interfaces.hole_patterns import HolePattern
from vehiclecad.interfaces.mount_points import MountInterface


@dataclass(frozen=True)
class FasteningInterface:
    name: str
    mount: MountInterface
    holes: HolePattern
    fastener_diameter: float

