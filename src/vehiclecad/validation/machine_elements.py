"""Machine-element coverage checks for production-oriented vehicle CAD."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re

from vehiclecad.assemblies.product_tree import all_parts, atomic_part_specs
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.core.reference import materials as C
from vehiclecad.parts.powertrain.detail import layout as L


@dataclass(frozen=True)
class MachineElementRow:
    status: str
    category: str
    count: int
    requirement: str
    detail: str


REQUIRED_EMITTED_PATTERNS: tuple[tuple[str, str, int], ...] = (
    ("wheel_lug_bolts", r"Wheel_Lug_Bolts_(FL|FR|RL|RR)$", 4),
    ("wheel_bearing_hubs", r"Wheel_Bearing_Hub_(FL|FR|RL|RR)$", 4),
    ("brake_calipers", r"Brake_Caliper_(FL|FR|RL|RR)$", 4),
    ("front_strut_top_mounts", r"Top_Mount_F[LR]$", 2),
    ("rear_hubs", r"Rear_Hub_R[LR]$", 2),
    ("engine_mount_rubbers", r"Engine_Mount_Rubber_[LR]$", 2),
    ("body_mounts", r"Body_Mount_[FR][LR]$", 4),
    ("propshaft_u_joints", r"U[Jj]oint_(Front|Centre|Rear)$", 3),
    ("propshaft_bolt_sets", r"(Guibo|Diff_Input_Flange)_Bolt_Set$", 2),
    ("centre_support_bearing", r"Centre_Bearing$", 1),
    ("cv_axle_nuts", r"CV_Axle_Nut_R[LR]$", 2),
    ("differential_cover_bolts", r"Rear_LSD_Cover_Bolt_Set$", 1),
)

CRITICAL_MACHINE_ELEMENT_MODULES: tuple[str, ...] = (
    "src/vehiclecad/parts/exterior/detail/wheels.py",
    "src/vehiclecad/parts/suspension/detail/front_macpherson.py",
    "src/vehiclecad/parts/suspension/detail/rear_semitrailing.py",
    "src/vehiclecad/parts/fasteners/brackets_interfaces/brackets_mounts.py",
    "src/vehiclecad/parts/powertrain/detail/transmission.py",
    "src/vehiclecad/parts/powertrain/detail/driveshaft.py",
    "src/vehiclecad/parts/powertrain/detail/differential.py",
    "src/vehiclecad/parts/powertrain/detail/half_shafts.py",
    "src/vehiclecad/parts/steering/detail/steering_rack.py",
    "src/vehiclecad/parts/chassis/structure/subframe.py",
)


def _part_names() -> list[str]:
    return [spec.part_name for spec in atomic_part_specs()]


def _emitted_rows() -> list[MachineElementRow]:
    names = _part_names()
    rows: list[MachineElementRow] = []
    for category, pattern, minimum in REQUIRED_EMITTED_PATTERNS:
        count = sum(1 for name in names if re.search(pattern, name))
        status = "pass" if count >= minimum else "fail"
        rows.append(
            MachineElementRow(
                status=status,
                category=category,
                count=count,
                requirement=f">={minimum} emitted part(s) matching {pattern}",
                detail="product tree machine-element coverage",
            )
        )
    return rows


def _source_rows(root: str | Path) -> list[MachineElementRow]:
    root_path = Path(root)
    rows: list[MachineElementRow] = []
    for rel in CRITICAL_MACHINE_ELEMENT_MODULES:
        path = root_path / rel
        if not path.exists():
            rows.append(MachineElementRow("fail", rel, 0, "source file exists", "missing source file"))
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        uses = len(re.findall(r"\bME\.", text))
        has_import = "machine_elements" in text
        status = "pass" if has_import and uses >= 1 else "fail"
        rows.append(
            MachineElementRow(
                status=status,
                category=rel,
                count=uses,
                requirement="imports shared machine_elements and calls ME.*",
                detail="critical interface uses catalog-style hardware primitives",
            )
        )
    return rows


def _centre(shape) -> tuple[float, float, float]:
    bb = shape.BoundingBox()
    return (
        0.5 * (bb.xmin + bb.xmax),
        0.5 * (bb.ymin + bb.ymax),
        0.5 * (bb.zmin + bb.zmax),
    )


def _dist_xy(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _row(status: str, category: str, count: int, requirement: str, detail: str) -> MachineElementRow:
    return MachineElementRow(status, category, count, requirement, detail)


def _contact_rows() -> list[MachineElementRow]:
    parts = {name: solid for solid, _color, name in all_parts()}
    rows: list[MachineElementRow] = []

    wheel_targets = {
        "FL": (C.AXLE_F, C.TRACK_F / 2.0, C.WHEEL_Z),
        "FR": (C.AXLE_F, -C.TRACK_F / 2.0, C.WHEEL_Z),
        "RL": (C.AXLE_R, C.TRACK_R / 2.0, C.WHEEL_Z),
        "RR": (C.AXLE_R, -C.TRACK_R / 2.0, C.WHEEL_Z),
    }
    for corner, target in wheel_targets.items():
        for label in ("Wheel_Bearing_Hub", "Wheel_Lug_Bolts", "Brake_Rotor", "Brake_Caliper"):
            name = f"PRT_ModelA_SportsCar_{label}_{corner}"
            shape = parts.get(name)
            if shape is None:
                rows.append(_row("fail", f"contact:{name}", 0, "part exists at wheel corner", "missing contact part"))
                continue
            c = _centre(shape)
            radial_error = math.hypot(c[0] - target[0], c[2] - target[2])
            outboard_offset = abs(c[1]) - abs(target[1])
            if label == "Brake_Caliper":
                ok = 95.0 <= radial_error <= 180.0 and -55.0 <= outboard_offset <= 25.0
                requirement = "caliper body offset to rotor radius and straddling disc near hub face"
            else:
                ok = radial_error <= 12.0 and -55.0 <= outboard_offset <= 90.0
                requirement = "axis concentric with wheel hardpoint; stack stays near hub face"
            rows.append(_row(
                "pass" if ok else "fail",
                f"contact:{name}",
                1,
                requirement,
                f"radial_error={radial_error:.1f}mm outboard_offset={outboard_offset:.1f}mm",
            ))

    front_top_targets = {
        "PRT_Top_Mount_FL": SK.FRONT_SUSP["strut_upper_mount"],
        "PRT_Top_Mount_FR": (
            SK.FRONT_SUSP["strut_upper_mount"][0],
            -SK.FRONT_SUSP["strut_upper_mount"][1],
            SK.FRONT_SUSP["strut_upper_mount"][2],
        ),
    }
    for name, target in front_top_targets.items():
        shape = parts.get(name)
        if shape is None:
            rows.append(_row("fail", f"contact:{name}", 0, "top mount exists at strut tower hardpoint", "missing contact part"))
            continue
        c = _centre(shape)
        ok = _dist_xy(c, target) <= 18.0 and abs(c[2] - target[2]) <= 35.0
        rows.append(_row(
            "pass" if ok else "fail",
            f"contact:{name}",
            1,
            "top mount centred on strut tower contact plane",
            f"centre=({c[0]:.1f},{c[1]:.1f},{c[2]:.1f}) target=({target[0]:.1f},{target[1]:.1f},{target[2]:.1f})",
        ))

    rear_hub_targets = {
        "PRT_Rear_Hub_RL": SK.REAR_SUSP["hub_centre"],
        "PRT_Rear_Hub_RR": (
            SK.REAR_SUSP["hub_centre"][0],
            -SK.REAR_SUSP["hub_centre"][1],
            SK.REAR_SUSP["hub_centre"][2],
        ),
        "PRT_CV_Axle_Nut_RL": SK.REAR_SUSP["hub_centre"],
        "PRT_CV_Axle_Nut_RR": (
            SK.REAR_SUSP["hub_centre"][0],
            -SK.REAR_SUSP["hub_centre"][1],
            SK.REAR_SUSP["hub_centre"][2],
        ),
    }
    for name, target in rear_hub_targets.items():
        shape = parts.get(name)
        if shape is None:
            rows.append(_row("fail", f"contact:{name}", 0, "rear hub/axle nut exists at rear hub hardpoint", "missing contact part"))
            continue
        c = _centre(shape)
        radial_error = math.hypot(c[0] - target[0], c[2] - target[2])
        y_offset = abs(c[1]) - abs(target[1])
        ok = radial_error <= 12.0 and -8.0 <= y_offset <= 35.0
        rows.append(_row(
            "pass" if ok else "fail",
            f"contact:{name}",
            1,
            "rear hub hardware concentric with hub hardpoint and seated outboard",
            f"radial_error={radial_error:.1f}mm y_offset={y_offset:.1f}mm",
        ))

    mount_targets = {
        "PRT_Engine_Mount_Rubber_L": SK.POWERTRAIN["engine_mount_L"],
        "PRT_Engine_Mount_Rubber_R": SK.POWERTRAIN["engine_mount_R"],
        "PRT_Trans_Mount_Rubber": SK.POWERTRAIN["trans_mount"],
        "PRT_Body_Mount_FL": (1240.0, 520.0, 194.0),
        "PRT_Body_Mount_FR": (1240.0, -520.0, 194.0),
        "PRT_Body_Mount_RL": (2800.0, 620.0, 194.0),
        "PRT_Body_Mount_RR": (2800.0, -620.0, 194.0),
    }
    for name, target in mount_targets.items():
        shape = parts.get(name)
        if shape is None:
            rows.append(_row("fail", f"contact:{name}", 0, "mount exists at its skeleton hardpoint", "missing contact part"))
            continue
        c = _centre(shape)
        xy_error = _dist_xy(c, target)
        z_error = c[2] - target[2]
        z_ok = abs(z_error) <= 28.0 if "Body_Mount" in name or "Trans_Mount" in name else -65.0 <= z_error <= 10.0
        ok = xy_error <= 12.0 and z_ok
        rows.append(_row(
            "pass" if ok else "fail",
            f"contact:{name}",
            1,
            "mount hardware centred on load-path hardpoint with correct vertical stack",
            f"xy_error={xy_error:.1f}mm z_error={z_error:+.1f}mm",
        ))

    propshaft_mid = (
        (L.PROPSHAFT_FRONT[0] + L.PROPSHAFT_REAR[0]) / 2.0,
        0.0,
        (L.PROPSHAFT_FRONT[2] + L.PROPSHAFT_REAR[2]) / 2.0,
    )
    driveline_targets = {
        "PRT_Ujoint_Front": L.PROPSHAFT_FRONT,
        "PRT_Ujoint_Centre": propshaft_mid,
        "PRT_Ujoint_Rear": L.PROPSHAFT_REAR,
        "PRT_Centre_Bearing": propshaft_mid,
        "PRT_Rear_LSD_Pinion_Flange": L.PROPSHAFT_REAR,
        "PRT_Rear_LSD_Output_Flange_L": L.DIFF_OUTPUT_L,
        "PRT_Rear_LSD_Output_Flange_R": L.DIFF_OUTPUT_R,
    }
    for name, target in driveline_targets.items():
        shape = parts.get(name)
        if shape is None:
            rows.append(_row("fail", f"contact:{name}", 0, "driveline contact element exists at skeleton joint", "missing contact part"))
            continue
        c = _centre(shape)
        error = math.dist(c, target)
        ok = error <= 38.0
        rows.append(_row(
            "pass" if ok else "fail",
            f"contact:{name}",
            1,
            "driveline machine element centred on shared joint hardpoint",
            f"centre=({c[0]:.1f},{c[1]:.1f},{c[2]:.1f}) target=({target[0]:.1f},{target[1]:.1f},{target[2]:.1f}) error={error:.1f}mm",
        ))

    return rows


def audit_machine_elements(root: str | Path = ".") -> list[MachineElementRow]:
    return _emitted_rows() + _source_rows(root) + _contact_rows()
