from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float

    def as_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


class Side(str, Enum):
    LEFT = "left"
    RIGHT = "right"

    @property
    def sign(self) -> int:
        return 1 if self is Side.LEFT else -1

    @property
    def code(self) -> str:
        return "L" if self is Side.LEFT else "R"


class Axle(str, Enum):
    FRONT = "front"
    REAR = "rear"

    @property
    def code(self) -> str:
        return "F" if self is Axle.FRONT else "R"


X_FORWARD = Vec3(1.0, 0.0, 0.0)
Y_LEFT = Vec3(0.0, 1.0, 0.0)
Z_UP = Vec3(0.0, 0.0, 1.0)
ORIGIN = Vec3(0.0, 0.0, 0.0)

