from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MountPoint:
    name: str
    xyz: tuple[float, float, float]
    normal: tuple[float, float, float] = (0.0, 0.0, 1.0)
    owner: str = ""
    target: str = ""


@dataclass(frozen=True)
class MountInterface:
    name: str
    points: list[MountPoint]

