from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClearanceEnvelope:
    name: str
    center: tuple[float, float, float]
    size: tuple[float, float, float]
    owner: str

