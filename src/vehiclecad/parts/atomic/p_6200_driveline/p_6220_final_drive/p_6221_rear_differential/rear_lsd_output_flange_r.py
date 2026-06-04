"""Atomic part owner: PRT_Rear_LSD_Output_Flange_R.

System: ASM_6200_Driveline
Subsystem: ASM_6220_Final_Drive
Leaf assembly: ASM_6221_Rear_Differential
Connections: CONN_REAR_SUBFRAME_DIFF_MOUNTS, CONN_HALF_SHAFT_INNERS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6200_driveline.p_6220_final_drive.p_6221_rear_differential.rear_lsd_output_flange_r",
    source_group="driveline_differential",
    part_name="PRT_Rear_LSD_Output_Flange_R",
    part_index=0,
    system_name="ASM_6200_Driveline",
    subsystem_name="ASM_6220_Final_Drive",
    subassembly_name="ASM_6221_Rear_Differential",
    connections=('CONN_REAR_SUBFRAME_DIFF_MOUNTS', 'CONN_HALF_SHAFT_INNERS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
