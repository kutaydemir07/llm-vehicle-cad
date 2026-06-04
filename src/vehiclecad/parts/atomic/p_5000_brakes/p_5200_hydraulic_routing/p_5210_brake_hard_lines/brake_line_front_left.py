"""Atomic part owner: PRT_Brake_Line_Front_Left.

System: ASM_5000_Brakes
Subsystem: ASM_5200_Hydraulic_Routing
Leaf assembly: ASM_5210_Brake_Hard_Lines
Connections: CONN_BRAKE_MASTER, CONN_ABS_MODULATOR, CONN_BRAKE_CORNERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_5000_brakes.p_5200_hydraulic_routing.p_5210_brake_hard_lines.brake_line_front_left",
    source_group="brakes_hard_lines",
    part_name="PRT_Brake_Line_Front_Left",
    part_index=0,
    system_name="ASM_5000_Brakes",
    subsystem_name="ASM_5200_Hydraulic_Routing",
    subassembly_name="ASM_5210_Brake_Hard_Lines",
    connections=('CONN_BRAKE_MASTER', 'CONN_ABS_MODULATOR', 'CONN_BRAKE_CORNERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
