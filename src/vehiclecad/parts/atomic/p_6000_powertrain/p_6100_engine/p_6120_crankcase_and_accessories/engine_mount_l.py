"""Atomic part owner: PRT_Engine_Mount_L.

System: ASM_6000_Powertrain
Subsystem: ASM_6100_Engine
Leaf assembly: ASM_6120_Crankcase_And_Accessories
Connections: CONN_ENGINE_MOUNTS, CONN_TRANSMISSION_BELLHOUSING
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6100_engine.p_6120_crankcase_and_accessories.engine_mount_l",
    source_group="powertrain_engine_block",
    part_name="PRT_Engine_Mount_L",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6100_Engine",
    subassembly_name="ASM_6120_Crankcase_And_Accessories",
    connections=('CONN_ENGINE_MOUNTS', 'CONN_TRANSMISSION_BELLHOUSING'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
