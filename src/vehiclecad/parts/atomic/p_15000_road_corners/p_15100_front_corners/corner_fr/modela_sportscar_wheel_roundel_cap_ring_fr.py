"""Atomic part owner: PRT_ModelA_SportsCar_Wheel_Roundel_Cap_Ring_FR.

System: ASM_15000_Road_Corners
Subsystem: ASM_15100_Front_Corners
Leaf assembly: ASM_Corner_FR
Connections: CONN_FRONT_RIGHT_HUB, CONN_FRONT_RIGHT_BRAKE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_15000_road_corners.p_15100_front_corners.corner_fr.modela_sportscar_wheel_roundel_cap_ring_fr",
    source_group="corner_fr",
    part_name="PRT_ModelA_SportsCar_Wheel_Roundel_Cap_Ring_FR",
    part_index=0,
    system_name="ASM_15000_Road_Corners",
    subsystem_name="ASM_15100_Front_Corners",
    subassembly_name="ASM_Corner_FR",
    connections=('CONN_FRONT_RIGHT_HUB', 'CONN_FRONT_RIGHT_BRAKE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
