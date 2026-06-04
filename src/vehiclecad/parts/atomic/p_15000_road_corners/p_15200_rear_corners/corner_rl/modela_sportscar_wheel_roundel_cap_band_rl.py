"""Atomic part owner: PRT_ModelA_SportsCar_Wheel_Roundel_Cap_Band_RL.

System: ASM_15000_Road_Corners
Subsystem: ASM_15200_Rear_Corners
Leaf assembly: ASM_Corner_RL
Connections: CONN_REAR_LEFT_HUB, CONN_REAR_LEFT_BRAKE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_15000_road_corners.p_15200_rear_corners.corner_rl.modela_sportscar_wheel_roundel_cap_band_rl",
    source_group="corner_rl",
    part_name="PRT_ModelA_SportsCar_Wheel_Roundel_Cap_Band_RL",
    part_index=0,
    system_name="ASM_15000_Road_Corners",
    subsystem_name="ASM_15200_Rear_Corners",
    subassembly_name="ASM_Corner_RL",
    connections=('CONN_REAR_LEFT_HUB', 'CONN_REAR_LEFT_BRAKE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
