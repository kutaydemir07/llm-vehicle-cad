"""Atomic part owner: PRT_Battery.

System: ASM_8000_Electrical
Subsystem: ASM_8100_Power_Generation_Storage
Leaf assembly: ASM_8110_Battery_Alternator
Connections: CONN_ENGINE_ACCESSORY_DRIVE, CONN_MAIN_POWER_BUS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_8000_electrical.p_8100_power_generation_storage.p_8110_battery_alternator.battery",
    source_group="electrical_battery_alternator",
    part_name="PRT_Battery",
    part_index=0,
    system_name="ASM_8000_Electrical",
    subsystem_name="ASM_8100_Power_Generation_Storage",
    subassembly_name="ASM_8110_Battery_Alternator",
    connections=('CONN_ENGINE_ACCESSORY_DRIVE', 'CONN_MAIN_POWER_BUS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
