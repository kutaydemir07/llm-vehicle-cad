"""Atomic part owner: PRT_Pedal_Box.

System: ASM_9000_Interior
Subsystem: ASM_9400_Driver_Controls
Leaf assembly: ASM_9410_Pedal_Box
Connections: CONN_FIREWALL_PEDAL_BOX, CONN_BRAKE_BOOSTER_PUSHROD
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9400_driver_controls.p_9410_pedal_box.pedal_box",
    source_group="interior_pedal_box",
    part_name="PRT_Pedal_Box",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9400_Driver_Controls",
    subassembly_name="ASM_9410_Pedal_Box",
    connections=('CONN_FIREWALL_PEDAL_BOX', 'CONN_BRAKE_BOOSTER_PUSHROD'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
