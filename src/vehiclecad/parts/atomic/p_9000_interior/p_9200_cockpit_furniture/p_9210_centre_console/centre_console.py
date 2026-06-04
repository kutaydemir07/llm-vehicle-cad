"""Atomic part owner: PRT_Centre_Console.

System: ASM_9000_Interior
Subsystem: ASM_9200_Cockpit_Furniture
Leaf assembly: ASM_9210_Centre_Console
Connections: CONN_TUNNEL_TOP, CONN_DRIVER_CONTROLS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9200_cockpit_furniture.p_9210_centre_console.centre_console",
    source_group="interior_console",
    part_name="PRT_Centre_Console",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9200_Cockpit_Furniture",
    subassembly_name="ASM_9210_Centre_Console",
    connections=('CONN_TUNNEL_TOP', 'CONN_DRIVER_CONTROLS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
