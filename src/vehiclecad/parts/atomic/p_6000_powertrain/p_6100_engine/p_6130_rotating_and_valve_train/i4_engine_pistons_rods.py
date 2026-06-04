"""Atomic part owner: PRT_I4_Engine_Pistons_Rods.

System: ASM_6000_Powertrain
Subsystem: ASM_6100_Engine
Leaf assembly: ASM_6130_Rotating_And_Valve_Train
Connections: CONN_CRANKCASE_INTERNALS, CONN_CYLINDER_HEAD_TIMING
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6100_engine.p_6130_rotating_and_valve_train.i4_engine_pistons_rods",
    source_group="powertrain_engine_internals",
    part_name="PRT_I4_Engine_Pistons_Rods",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6100_Engine",
    subassembly_name="ASM_6130_Rotating_And_Valve_Train",
    connections=('CONN_CRANKCASE_INTERNALS', 'CONN_CYLINDER_HEAD_TIMING'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
