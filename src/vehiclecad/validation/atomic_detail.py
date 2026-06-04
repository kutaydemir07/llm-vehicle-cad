"""Per-part audit for ModelA SportsCar detailed atomic part specs."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from vehiclecad.assemblies.product_tree import atomic_part_specs


@dataclass(frozen=True)
class AtomicDetailRow:
    status: str
    part_name: str
    system_name: str
    subsystem_name: str
    subassembly_name: str
    source_group: str
    module_path: str
    connections: str
    detail_tags: str
    notes: str


GROUP_DETAIL_TAGS = {
    "body_": ("ModelA_SportsCar_BIW_HARDPOINTS",),
    "chassis_": ("ModelA_SportsCar_CHASSIS_LAYOUT",),
    "suspension_front_": ("ModelA_SportsCar_FRONT_MACPHERSON",),
    "suspension_rear_": ("ModelA_SportsCar_REAR_SEMI_TRAILING_ARM",),
    "suspension_antiroll_": ("ModelA_SportsCar_ANTIROLL_BAR_LAYOUT",),
    "steering_": ("ModelA_SportsCar_STEERING_LAYOUT",),
    "brakes_": ("ModelA_SportsCar_BRAKE_ROUTING",),
    "powertrain_cylinder_head": ("I4_EngineB23_ENGINE",),
    "powertrain_engine_block": ("I4_EngineB23_ENGINE",),
    "powertrain_engine_internals": ("I4_EngineB23_ENGINE",),
    "powertrain_exhaust": ("I4_EngineB23_EXHAUST",),
    "powertrain_fuel_system": ("I4_EngineB23_FUEL_DELIVERY",),
    "powertrain_intake": ("I4_EngineB23_ITB_INTAKE",),
    "powertrain_transmission": ("MANUALGEARBOX_265",),
    "driveline_clutch": ("ModelA_SportsCar_CLUTCH",),
    "driveline_differential": ("ModelA_SportsCar_LSD",),
    "driveline_propshaft": ("ModelA_SportsCar_TWO_PIECE_PROPSHAFT",),
    "driveline_half_shafts": ("ModelA_SportsCar_REAR_CV_HALFSHAFTS",),
    "thermal_": ("ModelA_SportsCar_THERMAL_PACKAGE",),
    "electrical_": ("ModelA_SportsCar_ELECTRICAL_PACKAGE",),
    "interior_": ("ModelA_SportsCar_INTERIOR",),
    "exterior_flares": ("ModelA_SportsCar_BOX_FLARES",),
    "exterior_side_skirts": ("ModelA_SportsCar_AERO_KIT",),
    "exterior_rear_deck": ("ModelA_SportsCar_RAISED_REAR_DECK",),
    "exterior_rear_wing": ("ModelA_SportsCar_REAR_WING",),
    "exterior_frontend": ("ModelA_SportsCar_FRONT_FASCIA_LIGHTING",),
    "exterior_rearend": ("ModelA_SportsCar_REAR_FASCIA_LIGHTING",),
    "exterior_trim": ("ModelA_SportsCar_EXTERIOR_TRIM",),
    "exterior_glazing": ("ModelA_SportsCar_GLAZING",),
    "fasteners_": ("ModelA_SportsCar_MOUNTING_INTERFACES",),
    "corner_": ("ModelA_SportsCar_ROAD_WHEEL_CORNER",),
}

BANNED_DETAIL_TERMS = (
    "body_shell",
    "complete",
    "envelope",
    "generic",
    "unknown",
    "misc",
)


def _module_file(module_path: str, root: str | Path) -> Path:
    root_path = Path(root)
    src_root = root_path.parent if root_path.name == "vehiclecad" else root_path
    return src_root / Path(*module_path.split(".")).with_suffix(".py")


def _group_tags(source_group: str) -> list[str]:
    tags: list[str] = []
    for prefix, group_tags in GROUP_DETAIL_TAGS.items():
        if source_group.startswith(prefix):
            tags.extend(group_tags)
    return tags


def _name_tags(part_name: str) -> list[str]:
    tags: list[str] = []
    checks = {
        "ModelA_SportsCar": r"ModelA_SportsCar",
        "I4_EngineB23_ENGINE": r"\bI4_Engine\b",
        "MANUALGEARBOX_265": r"ManualGearbox_265",
        "ITB": r"\bITB\b",
        "MOTRONIC": r"Motronic",
        "LSD": r"\bLSD\b",
        "Mesh_WHEEL": r"\bMesh\b",
        "BOX_FLARE": r"Box_Flares?",
        "Classic_ROUNDEL": r"Roundel",
    }
    for tag, pattern in checks.items():
        if re.search(pattern, part_name):
            tags.append(tag)
    return tags


def audit_atomic_detail(root: str | Path = "src/vehiclecad") -> list[AtomicDetailRow]:
    rows: list[AtomicDetailRow] = []
    seen_names: set[str] = set()
    seen_modules: set[str] = set()

    for spec in atomic_part_specs():
        notes: list[str] = []
        status = "pass"

        if not spec.part_name.startswith("PRT_"):
            status = "fail"
            notes.append("part name must start with PRT_")
        if spec.part_name in seen_names:
            status = "fail"
            notes.append("duplicate engineering part name")
        seen_names.add(spec.part_name)

        if spec.module_path in seen_modules:
            status = "fail"
            notes.append("duplicate atomic module path")
        seen_modules.add(spec.module_path)

        if not spec.connections:
            status = "fail"
            notes.append("missing connection zone ownership")

        if any(term in spec.part_name.lower() for term in BANNED_DETAIL_TERMS):
            status = "fail"
            notes.append("name contains banned generic/monolithic term")

        module_file = _module_file(spec.module_path, root)
        if not module_file.exists():
            status = "fail"
            notes.append("atomic owner file is missing")

        tags = sorted(set(_group_tags(spec.source_group) + _name_tags(spec.part_name)))
        if not tags:
            status = "review"
            notes.append("no ModelA/SportsCar detail tag inferred")

        rows.append(
            AtomicDetailRow(
                status=status,
                part_name=spec.part_name,
                system_name=spec.system_name,
                subsystem_name=spec.subsystem_name,
                subassembly_name=spec.subassembly_name,
                source_group=spec.source_group,
                module_path=spec.module_path,
                connections=";".join(spec.connections),
                detail_tags=";".join(tags),
                notes=";".join(notes),
            )
        )

    return rows


def failing_atomic_detail_rows(root: str | Path = "src/vehiclecad") -> list[AtomicDetailRow]:
    return [row for row in audit_atomic_detail(root) if row.status == "fail"]

