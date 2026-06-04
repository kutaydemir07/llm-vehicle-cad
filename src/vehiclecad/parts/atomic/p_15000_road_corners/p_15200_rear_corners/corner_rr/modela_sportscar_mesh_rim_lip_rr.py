"""Atomic part owner: PRT_ModelA_SportsCar_Mesh_Rim_Lip_RR.

System: ASM_15000_Road_Corners
Subsystem: ASM_15200_Rear_Corners
Leaf assembly: ASM_Corner_RR
Connections: CONN_REAR_RIGHT_HUB, CONN_REAR_RIGHT_BRAKE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_15000_road_corners.p_15200_rear_corners.corner_rr.modela_sportscar_mesh_rim_lip_rr",
    source_group="corner_rr",
    part_name="PRT_ModelA_SportsCar_Mesh_Rim_Lip_RR",
    part_index=0,
    system_name="ASM_15000_Road_Corners",
    subsystem_name="ASM_15200_Rear_Corners",
    subassembly_name="ASM_Corner_RR",
    connections=('CONN_REAR_RIGHT_HUB', 'CONN_REAR_RIGHT_BRAKE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
