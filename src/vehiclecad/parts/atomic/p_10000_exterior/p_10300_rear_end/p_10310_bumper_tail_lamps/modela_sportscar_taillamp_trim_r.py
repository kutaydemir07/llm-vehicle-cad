"""Atomic part owner: PRT_ModelA_SportsCar_Taillamp_Trim_R.

System: ASM_10000_Exterior
Subsystem: ASM_10300_Rear_End
Leaf assembly: ASM_10310_Bumper_Tail_Lamps
Connections: CONN_REAR_BODY_FACE, CONN_REAR_LIGHTING_LOOM
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_10000_exterior.p_10300_rear_end.p_10310_bumper_tail_lamps.modela_sportscar_taillamp_trim_r",
    source_group="exterior_rearend",
    part_name="PRT_ModelA_SportsCar_Taillamp_Trim_R",
    part_index=0,
    system_name="ASM_10000_Exterior",
    subsystem_name="ASM_10300_Rear_End",
    subassembly_name="ASM_10310_Bumper_Tail_Lamps",
    connections=('CONN_REAR_BODY_FACE', 'CONN_REAR_LIGHTING_LOOM'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
