"""Atomic part owner: PRT_ModelA_SportsCar_Gauge_Cluster.

System: ASM_9000_Interior
Subsystem: ASM_9200_Cockpit_Furniture
Leaf assembly: ASM_9220_Dashboard_Instruments
Connections: CONN_FIREWALL_COWL, CONN_ELECTRICAL_INSTRUMENT_LOOM
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9200_cockpit_furniture.p_9220_dashboard_instruments.modela_sportscar_gauge_cluster",
    source_group="interior_dashboard",
    part_name="PRT_ModelA_SportsCar_Gauge_Cluster",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9200_Cockpit_Furniture",
    subassembly_name="ASM_9220_Dashboard_Instruments",
    connections=('CONN_FIREWALL_COWL', 'CONN_ELECTRICAL_INSTRUMENT_LOOM'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
