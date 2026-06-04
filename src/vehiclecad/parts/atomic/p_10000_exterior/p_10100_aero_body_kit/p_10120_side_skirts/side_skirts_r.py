"""Atomic part owner: PRT_Side_Skirts_R.

System: ASM_10000_Exterior
Subsystem: ASM_10100_Aero_Body_Kit
Leaf assembly: ASM_10120_Side_Skirts
Connections: CONN_BIW_ROCKER_OUTER, CONN_EXTERIOR_LOWER_TRIM
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10100_aero_body_kit.p_10120_side_skirts.side_skirts_r",
    source_group="exterior_side_skirts",
    part_name="PRT_Side_Skirts_R",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10100_Aero_Body_Kit",
    subassembly_name="ASM_10120_Side_Skirts",
    connections=('CONN_BIW_ROCKER_OUTER', 'CONN_EXTERIOR_LOWER_TRIM'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
