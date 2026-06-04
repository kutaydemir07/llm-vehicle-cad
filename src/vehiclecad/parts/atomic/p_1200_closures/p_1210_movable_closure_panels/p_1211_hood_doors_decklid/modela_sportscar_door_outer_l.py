"""Atomic part owner: PRT_ModelA_SportsCar_Door_Outer_L.

System: ASM_1200_Closures
Subsystem: ASM_1210_Movable_Closure_Panels
Leaf assembly: ASM_1211_Hood_Doors_Decklid
Connections: CONN_BIW_SHUT_LINES, CONN_CLOSURE_HINGES_LATCHES
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_1200_closures.p_1210_movable_closure_panels.p_1211_hood_doors_decklid.modela_sportscar_door_outer_l",
    source_group="body_closures",
    part_name="PRT_ModelA_SportsCar_Door_Outer_L",
    part_index=0,
    system_name="ASM_1200_Closures",
    subsystem_name="ASM_1210_Movable_Closure_Panels",
    subassembly_name="ASM_1211_Hood_Doors_Decklid",
    connections=('CONN_BIW_SHUT_LINES', 'CONN_CLOSURE_HINGES_LATCHES'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
