"""Atomic part owner: PRT_C_Pillar_Modified_L.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1130_C_Pillar_Conversion
Connections: CONN_BIW_ROOF_SIDE, CONN_BIW_REAR_QUARTER
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1130_c_pillar_conversion.c_pillar_modified_l",
    source_group="body_c_pillars",
    part_name="PRT_C_Pillar_Modified_L",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1130_C_Pillar_Conversion",
    connections=('CONN_BIW_ROOF_SIDE', 'CONN_BIW_REAR_QUARTER'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
