"""Atomic part owner: PRT_ModelA_SportsCar_Mesh_Rim_Face_FL.

System: ASM_15000_Road_Corners
Subsystem: ASM_15100_Front_Corners
Leaf assembly: ASM_Corner_FL
Connections: CONN_FRONT_LEFT_HUB, CONN_FRONT_LEFT_BRAKE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_15000_road_corners.p_15100_front_corners.corner_fl.modela_sportscar_mesh_rim_face_fl",
    source_group="corner_fl",
    part_name="PRT_ModelA_SportsCar_Mesh_Rim_Face_FL",
    part_index=0,
    system_name="ASM_15000_Road_Corners",
    subsystem_name="ASM_15100_Front_Corners",
    subassembly_name="ASM_Corner_FL",
    connections=('CONN_FRONT_LEFT_HUB', 'CONN_FRONT_LEFT_BRAKE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
