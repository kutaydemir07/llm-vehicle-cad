"""Atomic part owner: PRT_Wiring_Rear_Lighting_Loom.

System: ASM_8000_Electrical
Subsystem: ASM_8300_Wiring_Routing
Leaf assembly: ASM_8310_Main_Looms
Connections: CONN_ECU_FUSEBOX, CONN_BODY_POWER_CONSUMERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_8000_electrical.p_8300_wiring_routing.p_8310_main_looms.wiring_rear_lighting_loom",
    source_group="electrical_wiring",
    part_name="PRT_Wiring_Rear_Lighting_Loom",
    part_index=0,
    system_name="ASM_8000_Electrical",
    subsystem_name="ASM_8300_Wiring_Routing",
    subassembly_name="ASM_8310_Main_Looms",
    connections=('CONN_ECU_FUSEBOX', 'CONN_BODY_POWER_CONSUMERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
