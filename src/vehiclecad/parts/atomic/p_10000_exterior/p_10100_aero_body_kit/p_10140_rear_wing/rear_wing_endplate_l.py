"""Atomic part owner: PRT_Rear_Wing_Endplate_L.

System: ASM_10000_Exterior
Subsystem: ASM_10100_Aero_Body_Kit
Leaf assembly: ASM_10140_Rear_Wing
Connections: CONN_REAR_DECK, CONN_AERO_LOAD_PATH
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10100_aero_body_kit.p_10140_rear_wing.rear_wing_endplate_l",
    source_group="exterior_rear_wing",
    part_name="PRT_Rear_Wing_Endplate_L",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10100_Aero_Body_Kit",
    subassembly_name="ASM_10140_Rear_Wing",
    connections=('CONN_REAR_DECK', 'CONN_AERO_LOAD_PATH'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
