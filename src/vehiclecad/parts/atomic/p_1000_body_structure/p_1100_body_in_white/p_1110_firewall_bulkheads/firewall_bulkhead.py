"""Atomic part owner: PRT_Firewall_Bulkhead.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1110_Firewall_Bulkheads
Connections: CONN_BIW_ENGINE_BAY_REAR, CONN_BIW_CABIN_FRONT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1110_firewall_bulkheads.firewall_bulkhead",
    source_group="body_firewall",
    part_name="PRT_Firewall_Bulkhead",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1110_Firewall_Bulkheads",
    connections=('CONN_BIW_ENGINE_BAY_REAR', 'CONN_BIW_CABIN_FRONT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
