"""Atomic part owner: PRT_Strut_Top_Plate_FL.

System: ASM_1000_Body_Structure
Subsystem: ASM_1100_Body_In_White
Leaf assembly: ASM_1190_Strut_Top_Plates
Connections: CONN_FRONT_SUSPENSION_TOP_MOUNTS, CONN_BODY_BRACE_FRONT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1000_body_structure.p_1100_body_in_white.p_1190_strut_top_plates.strut_top_plate_fl",
    source_group="body_strut_top_plates",
    part_name="PRT_Strut_Top_Plate_FL",
    part_index=0,
    system_name="ASM_1000_Body_Structure",
    subsystem_name="ASM_1100_Body_In_White",
    subassembly_name="ASM_1190_Strut_Top_Plates",
    connections=('CONN_FRONT_SUSPENSION_TOP_MOUNTS', 'CONN_BODY_BRACE_FRONT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
