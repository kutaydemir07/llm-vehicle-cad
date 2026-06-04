"""Atomic part owner: PRT_Release_Bearing.

System: ASM_6200_Driveline
Subsystem: ASM_6210_Clutch
Leaf assembly: ASM_6211_Flywheel_Pressure_Disc
Connections: CONN_ENGINE_CRANK_FLANGE, CONN_TRANSMISSION_INPUT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6200_driveline.p_6210_clutch.p_6211_flywheel_pressure_disc.release_bearing",
    source_group="driveline_clutch",
    part_name="PRT_Release_Bearing",
    part_index=0,
    system_name="ASM_6200_Driveline",
    subsystem_name="ASM_6210_Clutch",
    subassembly_name="ASM_6211_Flywheel_Pressure_Disc",
    connections=('CONN_ENGINE_CRANK_FLANGE', 'CONN_TRANSMISSION_INPUT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
