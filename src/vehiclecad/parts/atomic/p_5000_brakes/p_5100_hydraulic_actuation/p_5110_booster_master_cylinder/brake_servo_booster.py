"""Atomic part owner: PRT_Brake_Servo_Booster.

System: ASM_5000_Brakes
Subsystem: ASM_5100_Hydraulic_Actuation
Leaf assembly: ASM_5110_Booster_Master_Cylinder
Connections: CONN_FIREWALL_PEDAL_BOX, CONN_BRAKE_LINE_MANIFOLD
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_5000_brakes.p_5100_hydraulic_actuation.p_5110_booster_master_cylinder.brake_servo_booster",
    source_group="brakes_booster_master",
    part_name="PRT_Brake_Servo_Booster",
    part_index=0,
    system_name="ASM_5000_Brakes",
    subsystem_name="ASM_5100_Hydraulic_Actuation",
    subassembly_name="ASM_5110_Booster_Master_Cylinder",
    connections=('CONN_FIREWALL_PEDAL_BOX', 'CONN_BRAKE_LINE_MANIFOLD'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
