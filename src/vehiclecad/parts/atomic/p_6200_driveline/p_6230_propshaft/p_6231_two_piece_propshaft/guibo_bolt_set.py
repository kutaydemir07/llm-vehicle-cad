"""Atomic part owner: PRT_Guibo_Bolt_Set.

System: ASM_6200_Driveline
Subsystem: ASM_6230_Propshaft
Leaf assembly: ASM_6231_Two_Piece_Propshaft
Connections: CONN_TRANSMISSION_OUTPUT, CONN_DIFFERENTIAL_INPUT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6200_driveline.p_6230_propshaft.p_6231_two_piece_propshaft.guibo_bolt_set",
    source_group="driveline_propshaft",
    part_name="PRT_Guibo_Bolt_Set",
    part_index=0,
    system_name="ASM_6200_Driveline",
    subsystem_name="ASM_6230_Propshaft",
    subassembly_name="ASM_6231_Two_Piece_Propshaft",
    connections=('CONN_TRANSMISSION_OUTPUT', 'CONN_DIFFERENTIAL_INPUT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
