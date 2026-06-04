"""Atomic part owner: PRT_Box_Flares_Rear_L.

System: ASM_10000_Exterior
Subsystem: ASM_10100_Aero_Body_Kit
Leaf assembly: ASM_10110_Box_Flares
Connections: CONN_BIW_WHEEL_ARCHES, CONN_EXTERIOR_PAINTED_PANELS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10100_aero_body_kit.p_10110_box_flares.box_flares_rear_l",
    source_group="exterior_flares",
    part_name="PRT_Box_Flares_Rear_L",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10100_Aero_Body_Kit",
    subassembly_name="ASM_10110_Box_Flares",
    connections=('CONN_BIW_WHEEL_ARCHES', 'CONN_EXTERIOR_PAINTED_PANELS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
