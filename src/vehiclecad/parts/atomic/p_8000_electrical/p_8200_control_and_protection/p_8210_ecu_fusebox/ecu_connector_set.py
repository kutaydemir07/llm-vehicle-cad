"""Atomic part owner: PRT_ECU_Connector_Set.

System: ASM_8000_Electrical
Subsystem: ASM_8200_Control_And_Protection
Leaf assembly: ASM_8210_ECU_Fusebox
Connections: CONN_FIREWALL_ELECTRICAL, CONN_ENGINE_LOOM
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_8000_electrical.p_8200_control_and_protection.p_8210_ecu_fusebox.ecu_connector_set",
    source_group="electrical_ecu_fusebox",
    part_name="PRT_ECU_Connector_Set",
    part_index=0,
    system_name="ASM_8000_Electrical",
    subsystem_name="ASM_8200_Control_And_Protection",
    subassembly_name="ASM_8210_ECU_Fusebox",
    connections=('CONN_FIREWALL_ELECTRICAL', 'CONN_ENGINE_LOOM'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
