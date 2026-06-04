"""Atomic part owner: PRT_ModelA_SportsCar_Roll_Cage.

System: ASM_9000_Interior
Subsystem: ASM_9500_Safety_Cage
Leaf assembly: ASM_9510_Roll_Cage
Connections: CONN_BIW_CAGE_FEET, CONN_OCCUPANT_SURVIVAL_CELL
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9500_safety_cage.p_9510_roll_cage.modela_sportscar_roll_cage",
    source_group="interior_roll_cage",
    part_name="PRT_ModelA_SportsCar_Roll_Cage",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9500_Safety_Cage",
    subassembly_name="ASM_9510_Roll_Cage",
    connections=('CONN_BIW_CAGE_FEET', 'CONN_OCCUPANT_SURVIVAL_CELL'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
