"""Whole-vehicle CAD contract audit for the Classic SportsCar ModelA model.

This is the release-gate layer that a large CAD project needs on top of the
part generators.  The model is allowed to be built bottom-up, but every part is
checked against top-down vehicle datums:

* design-table dimensions stay synchronized with shared constants
* the complete assembly stays inside the expected vehicle envelope
* no part drops below the ground plane
* wheel centres remain on the master axle/track hardpoints
* visible lower-body pieces obey the rocker/arch trim datum
* optional hierarchical collision checks run across the complete assembly matrix

Usage:
    python audit_vehicle_contract.py --collisions off
    python audit_vehicle_contract.py --collisions fast
    python audit_vehicle_contract.py --collisions exact --threshold 0
"""
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cadquery as cq

from vehiclecad.vehicle import detailed_complete_vehicle as assembly
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.core.reference import materials as C
from vehiclecad.core.reference.fitment import SUB_TO_MAJOR


MM_TOL = 1.0


@dataclass(frozen=True)
class Flag:
    check: str
    item: str
    severity: str
    detail: str


def _bb(shape):
    bb = shape.BoundingBox()
    return bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax


def _centre(shape):
    xmin, xmax, ymin, ymax, zmin, zmax = _bb(shape)
    return (0.5 * (xmin + xmax), 0.5 * (ymin + ymax), 0.5 * (zmin + zmax))


def _compound(parts):
    solids = [p[0] for p in parts]
    return cq.Compound.makeCompound(solids)


def _dim_flags(parts) -> list[Flag]:
    flags: list[Flag] = []
    comp = _compound(parts)
    xmin, xmax, ymin, ymax, zmin, zmax = _bb(comp)
    dims = {
        "length": (xmax - xmin, SK.DT.overall_length, 150.0),
        "width_with_mirrors": (ymax - ymin, SK.DT.overall_width, 180.0),
        "height": (zmax - max(0.0, zmin), SK.DT.overall_height, 45.0),
    }
    for name, (actual, target, tol) in dims.items():
        delta = actual - target
        if abs(delta) > tol:
            flags.append(Flag(
                "assembly_bbox", name, "FAIL",
                f"actual={actual:.1f} target={target:.1f} delta={delta:+.1f} tol={tol:.1f}",
            ))
    if zmin < -MM_TOL:
        flags.append(Flag("assembly_bbox", "zmin", "FAIL", f"assembly below ground: zmin={zmin:.1f}"))
    return flags


def _design_table_flags() -> list[Flag]:
    pairs = (
        ("overall_length", C.L, SK.DT.overall_length),
        ("overall_width", C.W, SK.DT.overall_width),
        ("overall_height", C.H, SK.DT.overall_height),
        ("wheelbase", C.WB, SK.DT.wheelbase),
        ("track_front", C.TRACK_F, SK.DT.track_front),
        ("track_rear", C.TRACK_R, SK.DT.track_rear),
        ("axle_front", C.AXLE_F, SK.DT.axle_front_x),
        ("axle_rear", C.AXLE_R, SK.DT.axle_rear_x),
        ("tire_radius", C.TIRE_R, SK.DT.tire_radius),
    )
    flags = []
    for name, left, right in pairs:
        if abs(left - right) > MM_TOL:
            flags.append(Flag("design_table_sync", name, "FAIL", f"common={left:.1f} hardpoints={right:.1f}"))
    return flags


def _ground_flags(parts) -> list[Flag]:
    flags = []
    for shape, _rgb, name in parts:
        zmin = shape.BoundingBox().zmin
        if zmin < -MM_TOL:
            flags.append(Flag("ground_plane", name, "FAIL", f"zmin={zmin:.1f}"))
    return flags


def _wheel_flags(parts) -> list[Flag]:
    flags = []
    targets = {
        "FL": (C.AXLE_F, C.TRACK_F / 2.0, C.WHEEL_Z),
        "FR": (C.AXLE_F, -C.TRACK_F / 2.0, C.WHEEL_Z),
        "RL": (C.AXLE_R, C.TRACK_R / 2.0, C.WHEEL_Z),
        "RR": (C.AXLE_R, -C.TRACK_R / 2.0, C.WHEEL_Z),
    }
    by_name = {name: shape for shape, _rgb, name in parts}
    for corner, target in targets.items():
        tire_name = f"PRT_ModelA_SportsCar_Tire_{corner}"
        tire = by_name.get(tire_name) or by_name.get(f"tire_{corner}")
        if tire is None:
            flags.append(Flag("wheel_hardpoints", tire_name, "FAIL", "missing tire"))
            continue
        actual = _centre(tire)
        deltas = [actual[i] - target[i] for i in range(3)]
        if max(abs(d) for d in deltas) > 2.0:
            flags.append(Flag(
                "wheel_hardpoints", tire_name, "FAIL",
                f"actual=({actual[0]:.1f},{actual[1]:.1f},{actual[2]:.1f}) "
                f"target=({target[0]:.1f},{target[1]:.1f},{target[2]:.1f})",
            ))
    return flags


def _lower_body_flags(parts) -> list[Flag]:
    flags = []
    rules: Iterable[tuple[str, float]] = (
        (r"Arch_Lip", C.ARCH_TRIM_Z0),
        (r"Side_Skirt", C.ROCKER_Z0),
    )
    for shape, _rgb, name in parts:
        for pattern, zmin_allowed in rules:
            if re.search(pattern, name):
                zmin = shape.BoundingBox().zmin
                if zmin < zmin_allowed - MM_TOL:
                    flags.append(Flag(
                        "lower_body_datums", name, "FAIL",
                        f"zmin={zmin:.1f} below datum {zmin_allowed:.1f}",
                    ))
    return flags


def _ownership_flags() -> list[Flag]:
    flags = []
    for sub_name in assembly.subassemblies():
        if sub_name not in SUB_TO_MAJOR:
            flags.append(Flag("assembly_ownership", sub_name, "FAIL", "sub-assembly missing major-system owner"))
    rules: Iterable[tuple[str, str]] = (
        (r"PRT_Body(?!_Mount)|PRT_Front_Nose|PRT_Front_Fender|PRT_Rear_Quarter|PRT_Rear_Tail|PRT_Roof_Outer|PRT_Aperture|PRT_Beltline|PRT_Rocker_Outer|PRT_Fuel_Flap", "ASM_1000_Body_Structure"),
        (r"^hood$|^trunk_lid$|^door_[LR]$", "ASM_1200_Closures"),
        (r"windshield|backlight|door_glass|quarter_glass", "ASM_10500_Glazing"),
        (r"headlamp|^reflector_(in|out)|kidney|foglamp|turn_signal|front_fascia|front_bumper|^intake_(back|mesh)$|brake_duct", "ASM_10000_Exterior"),
        (r"taillamp|tail_centre|rear_bumper|plate_recess|number_plate|rear_reflector|model_script", "ASM_10000_Exterior"),
        (r"exhaust|muffler|tailpipe", "ASM_6000_Powertrain"),
    )
    for sub_name, parts in assembly.subassemblies().items():
        for _shape, _rgb, name in parts:
            for pattern, expected in rules:
                if re.search(pattern, name, flags=re.IGNORECASE) and sub_name != expected:
                    flags.append(Flag(
                        "assembly_ownership", name, "FAIL",
                        f"owned by {sub_name}; expected {expected}",
                    ))
    return flags


def write_flags(flags: list[Flag], path: Path) -> None:
    path.parent.mkdir(exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["check", "item", "severity", "detail"])
        for flag in flags:
            w.writerow([flag.check, flag.item, flag.severity, flag.detail])


def run_collision_gate(mode: str, threshold: float, out_dir: Path):
    if mode == "off":
        return []
    from check_collisions_v3 import detect, load, save_csv

    sub_parts, sub_bbox, major_bbox, parent_bbox = load()
    hits = detect(
        sub_parts, sub_bbox, major_bbox, parent_bbox,
        fast=(mode == "fast"),
        threshold=threshold,
        only_majors=None,
        honor_interfaces=True,
    )
    save_csv(hits, str(out_dir / f"vehicle_contract_collisions_{mode}.csv"))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--collisions", choices=("off", "fast", "exact"), default="off")
    ap.add_argument("--threshold", type=float, default=0.0, help="minimum collision volume in msportscar")
    ap.add_argument("--output-dir", default="reports")
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    _asm, parts = assembly.build()

    flags: list[Flag] = []
    flags += _design_table_flags()
    flags += _dim_flags(parts)
    flags += _ground_flags(parts)
    flags += _wheel_flags(parts)
    flags += _lower_body_flags(parts)
    flags += _ownership_flags()

    collision_hits = run_collision_gate(args.collisions, args.threshold, out_dir)
    if collision_hits:
        flags.append(Flag(
            "collision_matrix", args.collisions, "FAIL",
            f"{len(collision_hits)} collisions above {args.threshold:.0f} msportscar",
        ))

    report_path = out_dir / "vehicle_contract_audit.csv"
    write_flags(flags, report_path)

    n_fail = sum(1 for f in flags if f.severity == "FAIL")
    print(f"Vehicle contract audit: {n_fail} failure(s)")
    print(f"Report -> {report_path}")
    if args.collisions != "off":
        print(f"Collision CSV -> {out_dir / f'vehicle_contract_collisions_{args.collisions}.csv'}")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
