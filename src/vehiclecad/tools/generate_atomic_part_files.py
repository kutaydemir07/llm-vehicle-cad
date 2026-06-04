"""Generate one atomic owner file for each detailed emitted engineering part."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path
import re

from vehiclecad.assemblies.source_collectors import group_parts, source_groups


HEADER = '''"""Generated atomic detailed-vehicle part package.

Run ``python -m vehiclecad.tools.generate_atomic_part_files`` after changing a
source collector or adding/removing an emitted engineering part.
"""
'''


PART_TEMPLATE = '''"""Atomic part owner: {part_name}.

System: {system_name}
Subsystem: {subsystem_name}
Leaf assembly: {subassembly_name}
Connections: {connections_text}
"""

from __future__ import annotations

from vehiclecad.assemblies.atomic import AtomicPartSpec, build_atomic_part


SPEC = AtomicPartSpec(
    module_path="{module_path}",
    source_group="{source_group}",
    part_name="{part_name}",
    part_index={part_index},
    system_name="{system_name}",
    subsystem_name="{subsystem_name}",
    subassembly_name="{subassembly_name}",
    connections={connections_repr},
)


def part():
    return build_atomic_part(SPEC)


def parts():
    return [part()]
'''


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"^prt_", "", value)
    value = re.sub(r"^asm_", "", value)
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        value = "item"
    if value[0].isdigit():
        value = f"p_{value}"
    return value


def _package_path(root: Path, *names: str) -> Path:
    return root.joinpath(*(_slug(name) for name in names))


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _ensure_packages(path: Path, stop: Path) -> None:
    current = path
    while True:
        init_file = current / "__init__.py"
        if not init_file.exists():
            _write(init_file, HEADER)
        if current == stop:
            break
        current = current.parent


def _clean_generated(root: Path) -> None:
    if not root.exists():
        return
    for path in sorted(root.rglob("*.py"), reverse=True):
        path.unlink()
    for path in sorted((p for p in root.rglob("*") if p.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def generate(root: Path) -> tuple[int, int]:
    package_root = root / "src" / "vehiclecad" / "parts" / "atomic"
    _clean_generated(package_root)
    _ensure_packages(package_root, package_root)

    specs = []
    seen_modules: Counter[str] = Counter()
    total = 0

    for group in source_groups():
        names_seen_in_group: defaultdict[str, int] = defaultdict(int)
        for part_tuple in group_parts(group.slug):
            part_name = part_tuple[2]
            part_index = names_seen_in_group[part_name]
            names_seen_in_group[part_name] += 1

            base_dir = _package_path(
                package_root,
                group.system_name,
                group.subsystem_name,
                group.subassembly_name,
            )
            module_stem = _slug(part_name)
            module_rel_key = ".".join(
                ["vehiclecad", "parts", "atomic"]
                + [_slug(group.system_name), _slug(group.subsystem_name), _slug(group.subassembly_name), module_stem]
            )
            seen_modules[module_rel_key] += 1
            if seen_modules[module_rel_key] > 1:
                module_stem = f"{module_stem}_{seen_modules[module_rel_key]}"
                module_rel_key = ".".join(
                    ["vehiclecad", "parts", "atomic"]
                    + [_slug(group.system_name), _slug(group.subsystem_name), _slug(group.subassembly_name), module_stem]
                )

            module_path = base_dir / f"{module_stem}.py"
            _ensure_packages(base_dir, package_root)
            module_import = module_rel_key
            connections_repr = repr(tuple(group.connections))
            connections_text = ", ".join(group.connections) if group.connections else "none"
            _write(
                module_path,
                PART_TEMPLATE.format(
                    part_name=part_name,
                    source_group=group.slug,
                    part_index=part_index,
                    system_name=group.system_name,
                    subsystem_name=group.subsystem_name,
                    subassembly_name=group.subassembly_name,
                    module_path=module_import,
                    connections_repr=connections_repr,
                    connections_text=connections_text,
                ),
            )
            specs.append(module_import)
            total += 1

    registry_lines = [HEADER, "from __future__ import annotations\n\n"]
    for index, module_path in enumerate(specs):
        registry_lines.append(f"from {module_path} import SPEC as SPEC_{index:04d}\n")
    registry_lines.append("\nATOMIC_PART_SPECS = (\n")
    for index in range(len(specs)):
        registry_lines.append(f"    SPEC_{index:04d},\n")
    registry_lines.append(")\n")
    _write(package_root / "registry.py", "".join(registry_lines))

    return total, len(set(specs))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate atomic part owner files.")
    parser.add_argument("--root", default=".", help="Repository root.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    total, unique = generate(Path(args.root).resolve())
    print(f"Generated {total} atomic part files ({unique} unique modules).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
