"""Atomic part owner: PRT_Inner_Fender_L.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1196_Engine_Bay_Panels
Connections: CONN_ENGINE_BAY_FRONT, CONN_POWERTRAIN_MOUNTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1196_engine_bay_panels.inner_fender_l",
    source_group="body_engine_bay",
    part_name="PRT_Inner_Fender_L",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1196_Engine_Bay_Panels",
    connections=('CONN_ENGINE_BAY_FRONT', 'CONN_POWERTRAIN_MOUNTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
