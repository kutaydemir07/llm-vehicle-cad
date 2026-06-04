"""Atomic part owner: PRT_A_Pillar_L.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1140_A_B_Pillars
Connections: CONN_BIW_DOOR_APERTURES, CONN_BIW_ROOF_SIDE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1140_a_b_pillars.a_pillar_l",
    source_group="body_pillars",
    part_name="PRT_A_Pillar_L",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1140_A_B_Pillars",
    connections=('CONN_BIW_DOOR_APERTURES', 'CONN_BIW_ROOF_SIDE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
