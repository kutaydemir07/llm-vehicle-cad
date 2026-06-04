"""Atomic part owner: PRT_Coil_Spring_FR.

System: ASM_3000_Suspension
Subsystem: ASM_3200_Front_Suspension
Leaf assembly: ASM_3210_MacPherson_Corner_Hardparts
Connections: CONN_FRONT_SUSPENSION_TOP_MOUNTS, CONN_FRONT_HUB_CORNERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_3000_suspension.p_3200_front_suspension.p_3210_macpherson_corner_hardparts.coil_spring_fr",
    source_group="suspension_front_macpherson",
    part_name="PRT_Coil_Spring_FR",
    part_index=0,
    system_name="ASM_3000_Suspension",
    subsystem_name="ASM_3200_Front_Suspension",
    subassembly_name="ASM_3210_MacPherson_Corner_Hardparts",
    connections=('CONN_FRONT_SUSPENSION_TOP_MOUNTS', 'CONN_FRONT_HUB_CORNERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
