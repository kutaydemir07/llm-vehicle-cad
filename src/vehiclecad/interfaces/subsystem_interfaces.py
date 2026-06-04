from __future__ import annotations

from dataclasses import dataclass, field

from vehiclecad.interfaces.clearance_envelopes import ClearanceEnvelope
from vehiclecad.interfaces.mount_points import MountInterface


@dataclass(frozen=True)
class SubsystemInterface:
    name: str
    mounts: list[MountInterface] = field(default_factory=list)
    clearances: list[ClearanceEnvelope] = field(default_factory=list)

