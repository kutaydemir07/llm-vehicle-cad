"""Atomic part owner: PRT_Handbrake_Cable_Right.

System: ASM_5000_Brakes
Subsystem: ASM_5300_Parking_Brake
Leaf assembly: ASM_5310_Lever_And_Cables
Connections: CONN_INTERIOR_TUNNEL, CONN_REAR_BRAKE_CORNERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_5000_brakes.p_5300_parking_brake.p_5310_lever_and_cables.handbrake_cable_right",
    source_group="brakes_handbrake",
    part_name="PRT_Handbrake_Cable_Right",
    part_index=0,
    system_name="ASM_5000_Brakes",
    subsystem_name="ASM_5300_Parking_Brake",
    subassembly_name="ASM_5310_Lever_And_Cables",
    connections=('CONN_INTERIOR_TUNNEL', 'CONN_REAR_BRAKE_CORNERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
