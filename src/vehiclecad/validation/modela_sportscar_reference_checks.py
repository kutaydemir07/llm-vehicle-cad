"""Validation against researched Classic ModelA SportsCar reference data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from vehiclecad.assemblies.product_tree import atomic_part_specs
from vehiclecad.core.reference import modela_sportscar_reference as REF
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.core.reference import materials as C



@dataclass(frozen=True)
class ReferenceAuditRow:
    check: str
    item: str
    status: str
    actual: str
    expected: str
    source_url: str
    detail: str


def _fmt(value: object) -> str:
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


def _value_row(
    check: str,
    item: str,
    actual: float,
    expected: float,
    tolerance: float,
    source_key: str,
    detail: str = "",
) -> ReferenceAuditRow:
    delta = actual - expected
    status = "pass" if abs(delta) <= tolerance else "fail"
    return ReferenceAuditRow(
        check=check,
        item=item,
        status=status,
        actual=_fmt(actual),
        expected=f"{_fmt(expected)} +/- {_fmt(tolerance)}",
        source_url=REF.source_url(source_key),
        detail=detail or f"delta={delta:+.3f}",
    )


def _bool_row(check: str, item: str, actual: bool, expected: bool, source_key: str) -> ReferenceAuditRow:
    return ReferenceAuditRow(
        check=check,
        item=item,
        status="pass" if actual is expected else "fail",
        actual=_fmt(actual),
        expected=_fmt(expected),
        source_url=REF.source_url(source_key),
        detail="",
    )


def _bom_row(label: str, pattern: str, minimum: int, source_key: str, names: tuple[str, ...]) -> ReferenceAuditRow:
    count = sum(1 for name in names if re.search(pattern, name, flags=re.IGNORECASE))
    return ReferenceAuditRow(
        check="atomic_bom_signature",
        item=label,
        status="pass" if count >= minimum else "fail",
        actual=str(count),
        expected=f">= {minimum}",
        source_url=REF.source_url(source_key),
        detail=pattern,
    )


def audit_modela_sportscar_reference() -> list[ReferenceAuditRow]:
    rows: list[ReferenceAuditRow] = []
    dims = REF.DIMENSIONS
    chassis = REF.CHASSIS

    rows.extend(
        [
            _value_row("core_materials", "overall_length", C.L, dims.overall_length, 0.1, "auto_data"),
            _value_row("core_materials", "overall_width", C.W, dims.overall_width, 0.1, "auto_data"),
            _value_row("core_materials", "overall_height", C.H, dims.overall_height, 0.1, "auto_data"),
            _value_row("core_materials", "wheelbase", C.WB, dims.wheelbase, 0.1, "modelampower"),
            _value_row("core_materials", "front_track", C.TRACK_F, dims.front_track, 0.1, "modelampower"),
            _value_row("core_materials", "rear_track", C.TRACK_R, dims.rear_track, 0.1, "modelampower"),
            _value_row("core_materials", "tire_width", C.TIRE_W, chassis.tire_width_mm, 0.1, "modelampower"),
            _value_row("core_materials", "model_tire_outer_diameter", C.TIRE_D, chassis.model_tire_outer_diameter_mm, 0.1, "modelampower"),
            _value_row("hardpoints", "overall_length", SK.DT.overall_length, dims.overall_length, 0.1, "auto_data"),
            _value_row("hardpoints", "rear_track", SK.DT.track_rear, dims.rear_track, 0.1, "modelampower"),
            _value_row("hardpoints", "tire_width", SK.DT.tire_width, chassis.tire_width_mm, 0.1, "modelampower"),
        ]
    )

    names = tuple(spec.part_name for spec in atomic_part_specs())
    rows.extend(
        [
            _bom_row("I4_EngineB23 engine detail", r"(^|_)I4_Engine(_|$)", 10, "classic_m", names),
            _bom_row("ManualGearbox 265 transmission", r"ManualGearbox_265", 1, "modelampower", names),
            _bom_row("25 percent LSD final drive", r"(^|_)LSD(_|$)", 1, "modelampower", names),
            _bom_row("15x7 Mesh wheel hardware", r"(^|_)Mesh_Rim", 12, "modelampower", names),
            _bom_row("205 section tires", r"PRT_ModelA_SportsCar_Tire_(FL|FR|RL|RR)$", 4, "modelampower", names),
            _bom_row("box flare panels", r"Box_Flares", 4, "classic_m", names),
            _bom_row("modified C-pillars", r"C_Pillar_Modified", 2, "classic_m", names),
            _bom_row("SportsCar backlight glass", r"Backlight_Glass", 1, "modelazone", names),
            _bom_row("raised rear deck", r"(Decklid_Outer|Rear_Deck_Raised)", 2, "classic_m", names),
            _bom_row("rear wing assembly", r"Rear_Wing", 5, "classic_m", names),
            _bom_row("road-car brake rotors", r"Brake_Rotor_(FL|FR|RL|RR)$", 4, "modelampower", names),
            _bom_row("road-car brake calipers", r"Brake_Caliper_(FL|FR|RL|RR)$", 4, "modelampower", names),
            _bom_row("ABS hydraulic unit", r"ABS_Hydraulic_Modulator", 1, "classic_m", names),
            _bom_row("separate brake hard lines", r"Brake_Line", 6, "classic_m", names),
        ]
    )

    return rows


def failing_modela_sportscar_reference_rows() -> list[ReferenceAuditRow]:
    return [row for row in audit_modela_sportscar_reference() if row.status == "fail"]
