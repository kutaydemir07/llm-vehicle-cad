"""Atomic part owner: PRT_Rear_Subframe.

System: ASM_2000_Chassis
Subsystem: ASM_2200_Subframes
Leaf assembly: ASM_2210_Rear_Subframe
Connections: CONN_REAR_SUSPENSION_PICKUPS, CONN_REAR_DIFF_MOUNTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_2000_chassis.p_2200_subframes.p_2210_rear_subframe.rear_subframe",
    source_group="chassis_rear_subframe",
    part_name="PRT_Rear_Subframe",
    part_index=0,
    system_name="ASM_2000_Chassis",
    subsystem_name="ASM_2200_Subframes",
    subassembly_name="ASM_2210_Rear_Subframe",
    connections=('CONN_REAR_SUSPENSION_PICKUPS', 'CONN_REAR_DIFF_MOUNTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
