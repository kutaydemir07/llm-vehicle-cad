"""Atomic part owner: PRT_Front_Seat_Rails_Driver.

System: ASM_9000_Interior
Subsystem: ASM_9600_Seating
Leaf assembly: ASM_9610_Front_Seats
Connections: CONN_FLOOR_SEAT_RAILS, CONN_OCCUPANT_H_POINTS
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9600_seating.p_9610_front_seats.front_seat_rails_driver",
    source_group="interior_front_seats",
    part_name="PRT_Front_Seat_Rails_Driver",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9600_Seating",
    subassembly_name="ASM_9610_Front_Seats",
    connections=('CONN_FLOOR_SEAT_RAILS', 'CONN_OCCUPANT_H_POINTS'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
