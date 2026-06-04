"""Atomic part owner: PRT_ModelA_SportsCar_Antenna_Base.

System: ASM_10000_Exterior
Subsystem: ASM_10400_Exterior_Trim
Leaf assembly: ASM_10410_Mirrors_Mouldings_Wipers
Connections: CONN_BODY_CLIP_POINTS, CONN_DRIVER_VISIBILITY
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10400_exterior_trim.p_10410_mirrors_mouldings_wipers.modela_sportscar_antenna_base",
    source_group="exterior_trim",
    part_name="PRT_ModelA_SportsCar_Antenna_Base",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10400_Exterior_Trim",
    subassembly_name="ASM_10410_Mirrors_Mouldings_Wipers",
    connections=('CONN_BODY_CLIP_POINTS', 'CONN_DRIVER_VISIBILITY'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
