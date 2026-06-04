"""Atomic part owner: PRT_ModelA_SportsCar_MTech1_Steering_Wheel_Rim.

System: ASM_4000_Steering
Subsystem: ASM_4200_Steering_Controls
Leaf assembly: ASM_4220_Steering_Wheel
Connections: CONN_STEERING_COLUMN_UPPER, CONN_DRIVER_INTERFACE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_4000_steering.p_4200_steering_controls.p_4220_steering_wheel.modela_sportscar_mtech1_steering_wheel_rim",
    source_group="steering_wheel",
    part_name="PRT_ModelA_SportsCar_MTech1_Steering_Wheel_Rim",
    part_index=0,
    system_name="ASM_4000_Steering",
    subsystem_name="ASM_4200_Steering_Controls",
    subassembly_name="ASM_4220_Steering_Wheel",
    connections=('CONN_STEERING_COLUMN_UPPER', 'CONN_DRIVER_INTERFACE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
