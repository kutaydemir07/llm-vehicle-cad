"""Atomic part owner: PRT_Rear_Wheel_Tub_L.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1195_Wheel_Tubs
Connections: CONN_WHEELHOUSE_FRONT, CONN_WHEELHOUSE_REAR
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1195_wheel_tubs.rear_wheel_tub_l",
    source_group="body_wheel_tubs",
    part_name="PRT_Rear_Wheel_Tub_L",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1195_Wheel_Tubs",
    connections=('CONN_WHEELHOUSE_FRONT', 'CONN_WHEELHOUSE_REAR'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
