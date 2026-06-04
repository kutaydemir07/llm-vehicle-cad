"""Atomic part owner: PRT_I4_Engine_Cylinder_Head_Detailed.

System: ASM_6000_Powertrain
Subsystem: ASM_6100_Engine
Leaf assembly: ASM_6110_Cylinder_Head_And_Cover
Connections: CONN_ENGINE_BLOCK_DECK, CONN_INTAKE_EXHAUST_PORTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6100_engine.p_6110_cylinder_head_and_cover.i4_engine_cylinder_head_detailed",
    source_group="powertrain_cylinder_head",
    part_name="PRT_I4_Engine_Cylinder_Head_Detailed",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6100_Engine",
    subassembly_name="ASM_6110_Cylinder_Head_And_Cover",
    connections=('CONN_ENGINE_BLOCK_DECK', 'CONN_INTAKE_EXHAUST_PORTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
