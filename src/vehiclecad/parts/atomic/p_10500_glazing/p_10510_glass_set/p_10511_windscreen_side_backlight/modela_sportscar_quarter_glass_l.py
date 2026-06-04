"""Atomic part owner: PRT_ModelA_SportsCar_Quarter_Glass_L.

System: ASM_10500_Glazing
Subsystem: ASM_10510_Glass_Set
Leaf assembly: ASM_10511_Windscreen_Side_Backlight
Connections: CONN_BIW_WINDOW_FLANGES, CONN_WEATHERSTRIPS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10500_glazing.p_10510_glass_set.p_10511_windscreen_side_backlight.modela_sportscar_quarter_glass_l",
    source_group="exterior_glazing",
    part_name="PRT_ModelA_SportsCar_Quarter_Glass_L",
    part_index=0,
    system_name="ASM_10500_Glazing",
    subsystem_name="ASM_10510_Glass_Set",
    subassembly_name="ASM_10511_Windscreen_Side_Backlight",
    connections=('CONN_BIW_WINDOW_FLANGES', 'CONN_WEATHERSTRIPS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
