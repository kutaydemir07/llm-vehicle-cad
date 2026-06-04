"""Atomic part owner: PRT_Strut_Tower_Rear_R.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1180_Strut_Tower_Shells
Connections: CONN_FRONT_SUSPENSION_TOP_MOUNTS, CONN_REAR_SUSPENSION_TOP_MOUNTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1180_strut_tower_shells.strut_tower_rear_r",
    source_group="body_strut_towers_shell",
    part_name="PRT_Strut_Tower_Rear_R",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1180_Strut_Tower_Shells",
    connections=('CONN_FRONT_SUSPENSION_TOP_MOUNTS', 'CONN_REAR_SUSPENSION_TOP_MOUNTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
