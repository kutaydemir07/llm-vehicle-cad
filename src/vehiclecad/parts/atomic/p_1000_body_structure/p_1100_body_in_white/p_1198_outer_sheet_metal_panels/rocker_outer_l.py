"""Atomic part owner: PRT_Rocker_Outer_L.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1198_Outer_Sheet_Metal_Panels
Connections: CONN_BIW_OUTER_SKIN, CONN_EXTERIOR_TRIM_CLIPS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1198_outer_sheet_metal_panels.rocker_outer_l",
    source_group="body_outer_panels",
    part_name="PRT_Rocker_Outer_L",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1198_Outer_Sheet_Metal_Panels",
    connections=('CONN_BIW_OUTER_SKIN', 'CONN_EXTERIOR_TRIM_CLIPS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
