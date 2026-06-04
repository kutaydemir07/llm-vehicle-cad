"""Atomic part owner: PRT_PS_Reservoir.

System: ASM_4000_Steering
Subsystem: ASM_4300_Power_Assist
Leaf assembly: ASM_4310_Power_Steering_Reservoir
Connections: CONN_ENGINE_BAY_ACCESSORY, CONN_STEERING_HYDRAULICS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_4000_steering.p_4300_power_assist.p_4310_power_steering_reservoir.ps_reservoir",
    source_group="steering_power_assist",
    part_name="PRT_PS_Reservoir",
    part_index=0,
    system_name="ASM_4000_Steering",
    subsystem_name="ASM_4300_Power_Assist",
    subassembly_name="ASM_4310_Power_Steering_Reservoir",
    connections=('CONN_ENGINE_BAY_ACCESSORY', 'CONN_STEERING_HYDRAULICS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
