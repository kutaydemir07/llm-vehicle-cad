"""Atomic part owner: PRT_Floor_Carpet.

System: ASM_9000_Interior
Subsystem: ASM_9100_Soft_Trim
Leaf assembly: ASM_9110_Carpets_Headliner
Connections: CONN_BIW_CABIN_FLOOR, CONN_BIW_ROOF_INNER
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9100_soft_trim.p_9110_carpets_headliner.floor_carpet",
    source_group="interior_soft_trim",
    part_name="PRT_Floor_Carpet",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9100_Soft_Trim",
    subassembly_name="ASM_9110_Carpets_Headliner",
    connections=('CONN_BIW_CABIN_FLOOR', 'CONN_BIW_ROOF_INNER'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
