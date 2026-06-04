"""Atomic part owner: PRT_Steering_Column.

System: ASM_4000_Steering
Subsystem: ASM_4200_Steering_Controls
Leaf assembly: ASM_4210_Column
Connections: CONN_DASH_CROSSCAR, CONN_STEERING_RACK_INPUT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_4000_steering.p_4200_steering_controls.p_4210_column.steering_column",
    source_group="steering_column",
    part_name="PRT_Steering_Column",
    part_index=0,
    system_name="ASM_4000_Steering",
    subsystem_name="ASM_4200_Steering_Controls",
    subassembly_name="ASM_4210_Column",
    connections=('CONN_DASH_CROSSCAR', 'CONN_STEERING_RACK_INPUT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
