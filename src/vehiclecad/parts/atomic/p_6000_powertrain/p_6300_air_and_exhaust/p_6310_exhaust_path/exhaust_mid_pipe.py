"""Atomic part owner: PRT_Exhaust_Mid_Pipe.

System: ASM_6000_Powertrain
Subsystem: ASM_6300_Air_And_Exhaust
Leaf assembly: ASM_6310_Exhaust_Path
Connections: CONN_EXHAUST_PORTS, CONN_UNDERBODY_HANGERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6300_air_and_exhaust.p_6310_exhaust_path.exhaust_mid_pipe",
    source_group="powertrain_exhaust",
    part_name="PRT_Exhaust_Mid_Pipe",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6300_Air_And_Exhaust",
    subassembly_name="ASM_6310_Exhaust_Path",
    connections=('CONN_EXHAUST_PORTS', 'CONN_UNDERBODY_HANGERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
