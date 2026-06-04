"""Atomic part definitions used by the detailed product structure."""

from __future__ import annotations

from dataclasses import dataclass

from .source_collectors import atomic_part

PartTuple = tuple


@dataclass(frozen=True)
class AtomicPartSpec:
    module_path: str
    source_group: str
    part_name: str
    part_index: int
    system_name: str
    subsystem_name: str
    subassembly_name: str
    connections: tuple[str, ...] = ()


def build_atomic_part(spec: AtomicPartSpec) -> PartTuple:
    return atomic_part(spec.source_group, spec.part_name, spec.part_index)

