"""Atomic part owner: PRT_ModelA_SportsCar_Headlamp_Inner_Bezel_R.

System: ASM_10000_Exterior
Subsystem: ASM_10200_Front_End
Leaf assembly: ASM_10210_Fascia_Grille_Lamps
Connections: CONN_FRONT_BODY_FACE, CONN_FRONT_LIGHTING_LOOM
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10200_front_end.p_10210_fascia_grille_lamps.modela_sportscar_headlamp_inner_bezel_r",
    source_group="exterior_frontend",
    part_name="PRT_ModelA_SportsCar_Headlamp_Inner_Bezel_R",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10200_Front_End",
    subassembly_name="ASM_10210_Fascia_Grille_Lamps",
    connections=('CONN_FRONT_BODY_FACE', 'CONN_FRONT_LIGHTING_LOOM'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
