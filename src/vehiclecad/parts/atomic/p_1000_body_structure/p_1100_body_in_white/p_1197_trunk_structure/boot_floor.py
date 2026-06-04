"""Atomic part owner: PRT_Boot_Floor.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1197_Trunk_Structure
Connections: CONN_REAR_COMPARTMENT, CONN_FUEL_TANK_ZONE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1197_trunk_structure.boot_floor",
    source_group="body_trunk",
    part_name="PRT_Boot_Floor",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1197_Trunk_Structure",
    connections=('CONN_REAR_COMPARTMENT', 'CONN_FUEL_TANK_ZONE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
