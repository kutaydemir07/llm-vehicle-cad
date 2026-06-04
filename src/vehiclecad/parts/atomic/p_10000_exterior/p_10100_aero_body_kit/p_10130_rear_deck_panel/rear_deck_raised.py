"""Atomic part owner: PRT_Rear_Deck_Raised.

System: ASM_10000_Exterior
Subsystem: ASM_10100_Aero_Body_Kit
Leaf assembly: ASM_10130_Rear_Deck_Panel
Connections: CONN_TRUNK_LID_OUTER, CONN_REAR_WING_BASE
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10100_aero_body_kit.p_10130_rear_deck_panel.rear_deck_raised",
    source_group="exterior_rear_deck",
    part_name="PRT_Rear_Deck_Raised",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10100_Aero_Body_Kit",
    subassembly_name="ASM_10130_Rear_Deck_Panel",
    connections=('CONN_TRUNK_LID_OUTER', 'CONN_REAR_WING_BASE'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
