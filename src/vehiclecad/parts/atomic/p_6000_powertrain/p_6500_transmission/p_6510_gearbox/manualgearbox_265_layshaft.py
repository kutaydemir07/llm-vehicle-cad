"""Atomic part owner: PRT_ManualGearbox_265_Layshaft.

System: ASM_6000_Powertrain
Subsystem: ASM_6500_Transmission
Leaf assembly: ASM_6510_Gearbox
Connections: CONN_ENGINE_BELLHOUSING, CONN_DRIVELINE_PROPSHAFT_FRONT
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_6000_powertrain.p_6500_transmission.p_6510_gearbox.manualgearbox_265_layshaft",
    source_group="powertrain_transmission",
    part_name="PRT_ManualGearbox_265_Layshaft",
    part_index=0,
    system_name="ASM_6000_Powertrain",
    subsystem_name="ASM_6500_Transmission",
    subassembly_name="ASM_6510_Gearbox",
    connections=('CONN_ENGINE_BELLHOUSING', 'CONN_DRIVELINE_PROPSHAFT_FRONT'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
