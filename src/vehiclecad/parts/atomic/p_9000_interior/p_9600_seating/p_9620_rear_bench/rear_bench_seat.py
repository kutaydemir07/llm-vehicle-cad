"""Atomic part owner: PRT_Rear_Bench_Seat.

System: ASM_9000_Interior
Subsystem: ASM_9600_Seating
Leaf assembly: ASM_9620_Rear_Bench
Connections: CONN_REAR_CABIN_FLOOR, CONN_REAR_BULKHEAD
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="vehiclecad.parts.atomic.p_9000_interior.p_9600_seating.p_9620_rear_bench.rear_bench_seat",
    source_group="interior_rear_seat",
    part_name="PRT_Rear_Bench_Seat",
    part_index=0,
    system_name="ASM_9000_Interior",
    subsystem_name="ASM_9600_Seating",
    subassembly_name="ASM_9620_Rear_Bench",
    connections=('CONN_REAR_CABIN_FLOOR', 'CONN_REAR_BULKHEAD'),
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
