"""Atomic part owner: PRT_Velocity_Stack_4.

System: ASM_6000_Powertrain
Subsystem: ASM_6300_Air_And_Exhaust
Leaf assembly: ASM_6320_Intake_Path
Connections: CONN_CYLINDER_HEAD_INTAKE_PORTS, CONN_FRONT_AIRBOX_ZONE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6300_air_and_exhaust.p_6320_intake_path.velocity_stack_4",
    source_group="powertrain_intake",
    part_name="PRT_Velocity_Stack_4",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6300_Air_And_Exhaust",
    subassembly_name="ASM_6320_Intake_Path",
    connections=('CONN_CYLINDER_HEAD_INTAKE_PORTS', 'CONN_FRONT_AIRBOX_ZONE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
