"""V-model System 6000 - Powertrain (engine, transmission, driveline, fuel, exhaust).

``powertrain_parts()`` = engine + gearbox + intake/exhaust/fuel; ``driveline_parts()``
= clutch + propshaft + diff + half-shafts, so the assembly tree can keep
``ASM_6000_Powertrain`` and ``ASM_6200_Driveline`` as distinct nodes.
``engine_block`` is a re-export facade and is intentionally not called.
"""
from __future__ import annotations

from . import (cylinder_head, engine, engine_internals, exhaust, fuel_system,
               intake, transmission)
from . import clutch_assembly, differential, driveshaft, half_shafts


def powertrain_parts():
    out = []
    out.extend(cylinder_head.parts())
    out.extend(engine.parts())
    out.extend(engine_internals.parts())
    out.extend(exhaust.parts())
    out.extend(fuel_system.parts())
    out.extend(intake.parts())
    out.extend(transmission.parts())
    return out


def driveline_parts():
    out = []
    out.extend(clutch_assembly.parts())
    out.extend(differential.parts())
    out.extend(driveshaft.parts())
    out.extend(half_shafts.parts())
    return out


def parts():
    return powertrain_parts() + driveline_parts()
