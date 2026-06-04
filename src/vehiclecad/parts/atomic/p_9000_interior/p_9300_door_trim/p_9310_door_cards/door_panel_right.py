"""Atomic part owner: PRT_Door_Panel_Right.

System: ASM_9000_Interior
Subsystem: ASM_9300_Door_Trim
Leaf assembly: ASM_9310_Door_Cards
Connections: CONN_CLOSURE_DOORS, CONN_OCCUPANT_TOUCH_POINTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9300_door_trim.p_9310_door_cards.door_panel_right",
    source_group="interior_door_panels",
    part_name="PRT_Door_Panel_Right",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9300_Door_Trim",
    subassembly_name="ASM_9310_Door_Cards",
    connections=('CONN_CLOSURE_DOORS', 'CONN_OCCUPANT_TOUCH_POINTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
