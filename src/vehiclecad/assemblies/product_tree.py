"""Hierarchical detailed-vehicle product tree built from atomic part files."""

from __future__ import annotations

from collections import OrderedDict, defaultdict

import cadquery as cq

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part
from vehiclecad.parts.atomic.registry import ATOMIC_PART_SPECS

PartTuple = tuple
ProductTree = OrderedDict[str, OrderedDict[str, OrderedDict[str, list[AtomicPartSpec]]]]


def atomic_part_specs() -> tuple[AtomicPartSpec, ...]:
    return ATOMIC_PART_SPECS


def product_tree() -> ProductTree:
    tree: ProductTree = OrderedDict()
    for spec in ATOMIC_PART_SPECS:
        subsystems = tree.setdefault(spec.system_name, OrderedDict())
        subassemblies = subsystems.setdefault(spec.subsystem_name, OrderedDict())
        subassemblies.setdefault(spec.subassembly_name, []).append(spec)
    return tree


def connection_map() -> dict[str, list[str]]:
    connections: defaultdict[str, list[str]] = defaultdict(list)
    for spec in ATOMIC_PART_SPECS:
        for connection in spec.connections:
            connections[connection].append(spec.module_path)
    return dict(sorted(connections.items()))


def system_parts() -> OrderedDict[str, list[PartTuple]]:
    systems: OrderedDict[str, list[PartTuple]] = OrderedDict()
    for system_name, subsystems in product_tree().items():
        parts: list[PartTuple] = []
        for subassemblies in subsystems.values():
            for specs in subassemblies.values():
                for spec in specs:
                    parts.append(build_atomic_part(spec))
        systems[system_name] = parts
    return systems


def all_parts() -> list[PartTuple]:
    out: list[PartTuple] = []
    for parts in system_parts().values():
        out.extend(parts)
    return out


def _add_part(assembly: cq.Assembly, item: PartTuple, used_names: dict[str, int]) -> tuple:
    if len(item) == 4 and item[3] == "local":
        shape, color, name, _marker = item
    else:
        shape, color, name = item[:3]

    used_names[name] = used_names.get(name, 0) + 1
    unique_name = name if used_names[name] == 1 else f"{name}_{used_names[name]}"
    assembly.add(shape, name=unique_name, color=cq.Color(*color))
    return shape, color, unique_name


def add_to_root(root: cq.Assembly) -> list[PartTuple]:
    """Add systems/subsystems/leaf assemblies/parts to ``root`` and return flat parts."""
    flat: list[PartTuple] = []
    used_names: dict[str, int] = {}

    for system_name, subsystems in product_tree().items():
        system_assembly = cq.Assembly(name=system_name)
        for subsystem_name, subassemblies in subsystems.items():
            subsystem_assembly = cq.Assembly(name=subsystem_name)
            for subassembly_name, specs in subassemblies.items():
                leaf_assembly = cq.Assembly(name=subassembly_name)
                for spec in specs:
                    part_tuple = build_atomic_part(spec)
                    shape, color, unique_name = _add_part(leaf_assembly, part_tuple, used_names)
                    flat.append((shape, color, unique_name))
                subsystem_assembly.add(leaf_assembly, name=subassembly_name)
            system_assembly.add(subsystem_assembly, name=subsystem_name)
        root.add(system_assembly, name=system_name)

    return flat

