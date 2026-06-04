from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    name: str
    density_kg_sportscar: float
    color: tuple[float, ...]


LOW_CARBON_STEEL = Material("low_carbon_steel", 7850, (0.40, 0.42, 0.45))
ALUMINUM_6061 = Material("aluminum_6061", 2700, (0.66, 0.68, 0.70))
RUBBER = Material("rubber", 1100, (0.04, 0.04, 0.045))
LAMINATED_GLASS = Material("laminated_glass", 2500, (0.32, 0.54, 0.72, 0.42))
ABS_PLASTIC = Material("abs_plastic", 1050, (0.10, 0.10, 0.11))

