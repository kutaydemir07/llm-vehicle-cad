"""Atomic part owner: PRT_CV_Boot_Outer_Clamp_Small_RL.

System: ASM_6200_Driveline
Subsystem: ASM_6240_Half_Shafts
Leaf assembly: ASM_6241_Rear_CV_Shafts
Connections: CONN_DIFFERENTIAL_OUTPUTS, CONN_REAR_HUB_CORNERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6200_driveline.p_6240_half_shafts.p_6241_rear_cv_shafts.cv_boot_outer_clamp_small_rl",
    source_group="driveline_half_shafts",
    part_name="PRT_CV_Boot_Outer_Clamp_Small_RL",
    part_index=0,
    system_name="ASM_6200_Driveline",
    subsystem_name="ASM_6240_Half_Shafts",
    subassembly_name="ASM_6241_Rear_CV_Shafts",
    connections=('CONN_DIFFERENTIAL_OUTPUTS', 'CONN_REAR_HUB_CORNERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
