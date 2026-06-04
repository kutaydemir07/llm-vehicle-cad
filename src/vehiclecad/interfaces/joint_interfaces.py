from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


JointType = Literal["fixed", "revolute", "spherical", "slider"]


@dataclass(frozen=True)
class JointInterface:
    name: str
    joint_type: JointType
    origin: tuple[float, float, float]
    axis: tuple[float, float, float]

