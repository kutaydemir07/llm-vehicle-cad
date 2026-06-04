"""Atomic part owner: PRT_Floorpan_Main.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1120_Floorpan
Connections: CONN_BIW_CABIN_FLOOR, CONN_CHASSIS_UNDERBODY_MOUNTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1120_floorpan.floorpan_main",
    source_group="body_floorpan",
    part_name="PRT_Floorpan_Main",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1120_Floorpan",
    connections=('CONN_BIW_CABIN_FLOOR', 'CONN_CHASSIS_UNDERBODY_MOUNTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
