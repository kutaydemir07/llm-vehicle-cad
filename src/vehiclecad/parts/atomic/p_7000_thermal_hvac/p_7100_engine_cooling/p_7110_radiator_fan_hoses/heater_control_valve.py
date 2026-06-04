"""Atomic part owner: PRT_Heater_Control_Valve.

System: ASM_7000_Thermal_HVAC
Subsystem: ASM_7100_Engine_Cooling
Leaf assembly: ASM_7110_Radiator_Fan_Hoses
Connections: CONN_FRONT_RADIATOR_SUPPORT, CONN_ENGINE_COOLANT_PORTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_7000_thermal_hvac.p_7100_engine_cooling.p_7110_radiator_fan_hoses.heater_control_valve",
    source_group="thermal_cooling",
    part_name="PRT_Heater_Control_Valve",
    part_index=0,
    system_name="ASM_7000_Thermal_HVAC",
    subsystem_name="ASM_7100_Engine_Cooling",
    subassembly_name="ASM_7110_Radiator_Fan_Hoses",
    connections=('CONN_FRONT_RADIATOR_SUPPORT', 'CONN_ENGINE_COOLANT_PORTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
