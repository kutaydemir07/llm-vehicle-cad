"""Atomic part owner: PRT_Steering_Rack.

System: ASM_4000_Steering
Subsystem: ASM_4100_Steering_Gear
Leaf assembly: ASM_4110_Rack_And_Tie_Rods
Connections: CONN_FRONT_SUBFRAME, CONN_STEERING_COLUMN_LOWER
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_4000_steering.p_4100_steering_gear.p_4110_rack_and_tie_rods.steering_rack",
    source_group="steering_rack",
    part_name="PRT_Steering_Rack",
    part_index=0,
    system_name="ASM_4000_Steering",
    subsystem_name="ASM_4100_Steering_Gear",
    subassembly_name="ASM_4110_Rack_And_Tie_Rods",
    connections=('CONN_FRONT_SUBFRAME', 'CONN_STEERING_COLUMN_LOWER'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
