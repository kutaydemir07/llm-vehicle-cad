"""Atomic part owner: PRT_Roof_Panel.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1160_Roof_Outer
Connections: CONN_BIW_ROOF_SIDE, CONN_GLAZING_UPPER
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1160_roof_outer.roof_panel",
    source_group="body_roof_panel",
    part_name="PRT_Roof_Panel",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1160_Roof_Outer",
    connections=('CONN_BIW_ROOF_SIDE', 'CONN_GLAZING_UPPER'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
