"""Atomic part owner: PRT_Fuel_Rail_ITB.

System: ASM_6000_Powertrain
Subsystem: ASM_6400_Fuel_Storage_And_Delivery
Leaf assembly: ASM_6410_Tank_Pump_Filter_Lines
Connections: CONN_FUEL_TANK_ZONE, CONN_ENGINE_FUEL_RAIL
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6400_fuel_storage_and_delivery.p_6410_tank_pump_filter_lines.fuel_rail_itb",
    source_group="powertrain_fuel_system",
    part_name="PRT_Fuel_Rail_ITB",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6400_Fuel_Storage_And_Delivery",
    subassembly_name="ASM_6410_Tank_Pump_Filter_Lines",
    connections=('CONN_FUEL_TANK_ZONE', 'CONN_ENGINE_FUEL_RAIL'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
