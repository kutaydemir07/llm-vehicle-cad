"""Atomic part owner: PRT_Roof_Bow_1.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1170_Roof_Headers_Bows
Connections: CONN_BIW_ROOF_SIDE, CONN_INTERIOR_HEADLINER
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1170_roof_headers_bows.roof_bow_1",
    source_group="body_roof_structure",
    part_name="PRT_Roof_Bow_1",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1170_Roof_Headers_Bows",
    connections=('CONN_BIW_ROOF_SIDE', 'CONN_INTERIOR_HEADLINER'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
