"""Atomic part owner: PRT_Front_Rail_L.

System: ASM_14000_Fasteners_Brackets
Subsystem: ASM_14100_Mounts_And_Brackets
Leaf assembly: ASM_14110_Engine_Trans_Body_Mounts
Connections: CONN_ENGINE_MOUNTS, CONN_BODY_INTERFACE_MOUNTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_14000_fasteners_brackets.p_14100_mounts_and_brackets.p_14110_engine_trans_body_mounts.front_rail_l",
    source_group="fasteners_mounts_brackets",
    part_name="PRT_Front_Rail_L",
    part_index=0,
    system_name="ASM_14000_Fasteners_Brackets",
    subsystem_name="ASM_14100_Mounts_And_Brackets",
    subassembly_name="ASM_14110_Engine_Trans_Body_Mounts",
    connections=('CONN_ENGINE_MOUNTS', 'CONN_BODY_INTERFACE_MOUNTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
