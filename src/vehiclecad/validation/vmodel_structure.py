from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from vehiclecad.assemblies.product_tree import atomic_part_specs
from vehiclecad.vehicle.detailed_complete_vehicle import subassemblies


BANNED_PART_PATTERNS = (
    re.compile(r"body_shell", re.IGNORECASE),
    re.compile(r"\bcomplete\b", re.IGNORECASE),
    re.compile(r"\benvelope\b", re.IGNORECASE),
    re.compile(r"_Lines$", re.IGNORECASE),
    re.compile(r"_Cables$", re.IGNORECASE),
    re.compile(r"_Harness$", re.IGNORECASE),
)

BANNED_SOURCE_PATTERNS = (
    re.compile(r"def\s+make_body_shell\b"),
    re.compile(r"body_shell"),
)


@dataclass(frozen=True)
class VModelIssue:
    scope: str
    item: str
    detail: str


def audit_emitted_part_names() -> list[VModelIssue]:
    issues: list[VModelIssue] = []
    for subsystem, parts in subassemblies().items():
        for _shape, _color, name, *_rest in parts:
            for pattern in BANNED_PART_PATTERNS:
                if pattern.search(name):
                    issues.append(
                        VModelIssue(
                            scope=subsystem,
                            item=name,
                            detail=f"part name matches monolithic pattern: {pattern.pattern}",
                        )
                    )
    return issues


def audit_source_structure(root: str | Path = "src/vehiclecad") -> list[VModelIssue]:
    root_path = Path(root)
    issues: list[VModelIssue] = []
    rule_files = {"vmodel_structure.py", "atomic_detail.py"}
    for path in root_path.rglob("*.py"):
        if path.name in rule_files:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in BANNED_SOURCE_PATTERNS:
            if pattern.search(text):
                issues.append(
                    VModelIssue(
                        scope="source",
                        item=str(path),
                        detail=f"source matches banned pattern: {pattern.pattern}",
                    )
                )
    return issues


def audit_atomic_file_structure(root: str | Path = "src/vehiclecad") -> list[VModelIssue]:
    root_path = Path(root)
    src_root = root_path.parent if root_path.name == "vehiclecad" else root_path
    issues: list[VModelIssue] = []
    seen_modules: set[str] = set()
    seen_parts: set[tuple[str, int]] = set()

    for spec in atomic_part_specs():
        if spec.module_path in seen_modules:
            issues.append(
                VModelIssue(
                    scope="atomic",
                    item=spec.module_path,
                    detail="duplicate atomic part module path",
                )
            )
        seen_modules.add(spec.module_path)

        part_key = (spec.part_name, spec.part_index)
        if part_key in seen_parts:
            issues.append(
                VModelIssue(
                    scope="atomic",
                    item=spec.part_name,
                    detail=f"duplicate emitted part identity at index {spec.part_index}",
                )
            )
        seen_parts.add(part_key)

        module_rel = Path(*spec.module_path.split(".")).with_suffix(".py")
        module_path = src_root / module_rel
        if not module_path.exists():
            issues.append(
                VModelIssue(
                    scope="atomic",
                    item=spec.module_path,
                    detail=f"atomic part file missing: {module_path}",
                )
            )

    emitted = {
        (name, index)
        for parts in subassemblies().values()
        for index, (_shape, _color, name, *_rest) in enumerate(parts)
    }
    spec_names = {(spec.part_name, spec.part_index) for spec in atomic_part_specs()}
    if len(spec_names) != sum(len(parts) for parts in subassemblies().values()):
        issues.append(
            VModelIssue(
                scope="atomic",
                item="ATOMIC_PART_SPECS",
                detail="atomic spec count does not match emitted detailed part count",
            )
        )
    missing = {name for name, _index in emitted if not any(spec.part_name == name for spec in atomic_part_specs())}
    for name in sorted(missing):
        issues.append(
            VModelIssue(
                scope="atomic",
                item=name,
                detail="emitted part has no atomic owner file",
            )
        )

    return issues


def audit_vmodel_structure(root: str | Path = "src/vehiclecad") -> list[VModelIssue]:
    return audit_source_structure(root) + audit_emitted_part_names() + audit_atomic_file_structure(root)
