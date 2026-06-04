"""Atomic part owner: PRT_Front_ARB.

System: ASM_3000_Suspension
Subsystem: ASM_3100_Roll_Control
Leaf assembly: ASM_3110_Antiroll_Bars
Connections: CONN_CHASSIS_ARB_MOUNTS, CONN_SUSPENSION_LINKS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_3000_suspension.p_3100_roll_control.p_3110_antiroll_bars.front_arb",
    source_group="suspension_antiroll_bars",
    part_name="PRT_Front_ARB",
    part_index=0,
    system_name="ASM_3000_Suspension",
    subsystem_name="ASM_3100_Roll_Control",
    subassembly_name="ASM_3110_Antiroll_Bars",
    connections=('CONN_CHASSIS_ARB_MOUNTS', 'CONN_SUSPENSION_LINKS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
