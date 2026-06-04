"""Atomic part owner: PRT_Rear_Coil_Spring_RR.

System: ASM_3000_Suspension
Subsystem: ASM_3300_Rear_Suspension
Leaf assembly: ASM_3310_Semi_Trailing_Arm_Corner_Hardparts
Connections: CONN_REAR_SUBFRAME_PICKUPS, CONN_REAR_HUB_CORNERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_3000_suspension.p_3300_rear_suspension.p_3310_semi_trailing_arm_corner_hardparts.rear_coil_spring_rr",
    source_group="suspension_rear_semitrailing",
    part_name="PRT_Rear_Coil_Spring_RR",
    part_index=0,
    system_name="ASM_3000_Suspension",
    subsystem_name="ASM_3300_Rear_Suspension",
    subassembly_name="ASM_3310_Semi_Trailing_Arm_Corner_Hardparts",
    connections=('CONN_REAR_SUBFRAME_PICKUPS', 'CONN_REAR_HUB_CORNERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
