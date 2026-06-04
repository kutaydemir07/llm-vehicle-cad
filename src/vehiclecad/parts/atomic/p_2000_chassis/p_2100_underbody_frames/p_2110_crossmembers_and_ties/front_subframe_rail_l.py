"""Atomic part owner: PRT_Front_Subframe_Rail_L.

System: ASM_2000_Chassis
Subsystem: ASM_2100_Underbody_Frames
Leaf assembly: ASM_2110_Crossmembers_And_Ties
Connections: CONN_BIW_UNDERBODY, CONN_POWERTRAIN_REAR_SUPPORT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_2000_chassis.p_2100_underbody_frames.p_2110_crossmembers_and_ties.front_subframe_rail_l",
    source_group="chassis_crossmembers",
    part_name="PRT_Front_Subframe_Rail_L",
    part_index=0,
    system_name="ASM_2000_Chassis",
    subsystem_name="ASM_2100_Underbody_Frames",
    subassembly_name="ASM_2110_Crossmembers_And_Ties",
    connections=('CONN_BIW_UNDERBODY', 'CONN_POWERTRAIN_REAR_SUPPORT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
