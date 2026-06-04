"""Atomic part owner: PRT_HVAC_Footwell_Duct_L.

System: ASM_7000_Thermal_HVAC
Subsystem: ASM_7200_Cabin_HVAC
Leaf assembly: ASM_7210_Heater_Box_Blower
Connections: CONN_FIREWALL_HVAC_OPENINGS, CONN_DASH_AIR_DISTRIBUTION
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_7000_thermal_hvac.p_7200_cabin_hvac.p_7210_heater_box_blower.hvac_footwell_duct_l",
    source_group="thermal_hvac",
    part_name="PRT_HVAC_Footwell_Duct_L",
    part_index=0,
    system_name="ASM_7000_Thermal_HVAC",
    subsystem_name="ASM_7200_Cabin_HVAC",
    subassembly_name="ASM_7210_Heater_Box_Blower",
    connections=('CONN_FIREWALL_HVAC_OPENINGS', 'CONN_DASH_AIR_DISTRIBUTION'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
