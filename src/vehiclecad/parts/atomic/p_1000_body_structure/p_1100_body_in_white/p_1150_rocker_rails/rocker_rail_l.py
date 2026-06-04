"""Atomic part owner: PRT_Rocker_Rail_L.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1150_Rocker_Rails
Connections: CONN_BIW_DOOR_APERTURES, CONN_CHASSIS_SIDE_MOUNTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1150_rocker_rails.rocker_rail_l",
    source_group="body_rockers",
    part_name="PRT_Rocker_Rail_L",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1150_Rocker_Rails",
    connections=('CONN_BIW_DOOR_APERTURES', 'CONN_CHASSIS_SIDE_MOUNTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
