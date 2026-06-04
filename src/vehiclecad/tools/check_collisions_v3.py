#!/usr/bin/env python3
"""
check_collisions_v3.py  --  Hierarchical Assembly-of-Assemblies collision checker.

Mirrors professional CAD (CATIA / NX) workflow:

  Parent Group   (e.g.  DRIVETRAIN)
    Major Group  (e.g.  POWERTRAIN, DRIVELINE)
      Sub-Asm    (e.g.  ASM_Powertrain_Packaging)
        Part     (e.g.  PRT_ManualGearbox_265_Transmission)

BVH pruning  --  4 levels before expensive exact boolean:
  1. Parent-group AABB  -- skip if parent envelopes don't overlap
  2. Major-group AABB   -- skip if major envelopes don't overlap
  3. Sub-asm AABB       -- skip if sub-asm envelopes don't overlap
  4. Part AABB          -- skip if part bboxes don't overlap
  5. Exact boolean      -- CadQuery .intersect() + .Volume()

Collision severity:
  INTER_PARENT  -- parts from different parent groups (worst: e.g. DRIVETRAIN vs STRUCTURE)
  INTRA_PARENT  -- same parent, different major  (e.g. POWERTRAIN vs CHASSIS within STRUCTURE)
  INTRA_MAJOR   -- same major, different sub-asms (close-fit / interface parts)

Usage
-----
  python check_collisions_v3.py                       # full exact check
  python check_collisions_v3.py --fast                # AABB overlap estimate only
  python check_collisions_v3.py --threshold 500       # ignore < 0.5 cc
  python check_collisions_v3.py --only POWERTRAIN CHASSIS
  python check_collisions_v3.py --matrix              # show overlap matrix then exit
  python check_collisions_v3.py --output results/my.csv
"""
from __future__ import annotations

import argparse, csv, os, sys, time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# ------------------------------------------------------------------------
# Assembly hierarchy definition
# ------------------------------------------------------------------------
# Maps sub-assembly name (key from assembly.subassemblies()) -> major group.
# Any sub-assembly not listed lands in "OTHER".
SUB_TO_MAJOR: Dict[str, str] = {
    "ASM_1000_Body_Structure":      "BODY_STRUCTURE",
    "ASM_1200_Closures":            "BODY_STRUCTURE",
    "ASM_2000_Chassis":             "CHASSIS",
    "ASM_3000_Suspension":          "SUSPENSION",
    "ASM_4000_Steering":            "STEERING",
    "ASM_5000_Brakes":              "BRAKES",
    "ASM_6000_Powertrain":          "POWERTRAIN",
    "ASM_6200_Driveline":           "DRIVELINE",
    "ASM_7000_Thermal_HVAC":        "THERMAL_HVAC",
    "ASM_8000_Electrical":          "ELECTRICAL",
    "ASM_9000_Interior":            "INTERIOR",
    "ASM_10000_Exterior":           "EXTERIOR",
    "ASM_10500_Glazing":            "EXTERIOR",
    "ASM_11000_Lighting":           "EXTERIOR",
    "ASM_12000_Safety":             "SAFETY",
    "ASM_13000_Fluids_Plumbing":    "FLUIDS",
    "ASM_14000_Fasteners_Brackets": "FASTENERS",
    "ASM_Corner_FL":                "CORNER_FL",
    "ASM_Corner_FR":                "CORNER_FR",
    "ASM_Corner_RL":                "CORNER_RL",
    "ASM_Corner_RR":                "CORNER_RR",
}

# Maps major group -> parent group  (top-level assembly-of-assemblies).
MAJOR_TO_PARENT: Dict[str, str] = {
    "BODY_STRUCTURE": "STRUCTURE",
    "CHASSIS":        "STRUCTURE",
    "EXTERIOR":       "STRUCTURE",
    "SAFETY":         "STRUCTURE",
    "FASTENERS":      "STRUCTURE",
    "POWERTRAIN":     "DRIVETRAIN",
    "DRIVELINE":      "DRIVETRAIN",
    "FLUIDS":         "DRIVETRAIN",
    "SUSPENSION":     "RUNNING_GEAR",
    "STEERING":       "RUNNING_GEAR",
    "BRAKES":         "RUNNING_GEAR",
    "CORNER_FL":      "RUNNING_GEAR",
    "CORNER_FR":      "RUNNING_GEAR",
    "CORNER_RL":      "RUNNING_GEAR",
    "CORNER_RR":      "RUNNING_GEAR",
    "INTERIOR":       "CABIN",
    "ELECTRICAL":     "CABIN",
    "THERMAL_HVAC":   "CABIN",
}

try:
    from vehiclecad.core.reference.fitment import (
        MAJOR_TO_PARENT as FIT_MAJOR_TO_PARENT,
        SUB_TO_MAJOR as FIT_SUB_TO_MAJOR,
        interface_reason,
    )

    SUB_TO_MAJOR.update(FIT_SUB_TO_MAJOR)
    MAJOR_TO_PARENT.update(FIT_MAJOR_TO_PARENT)
except Exception:
    def interface_reason(a_name: str, b_name: str, a_sub: str = "", b_sub: str = ""):
        return None

# Parts whose bounding-box spans almost the whole car -- skip exact boolean.
SKIP_NAME_PREFIXES = ("PRT_Wiring_", "PRT_Fuel_", "PRT_Brake_Line_",
                      "PRT_Handbrake_Cable_", "brake_line",
                      "wiring", "fuel_line")
SPAN_VOL_MSportsCar = 2.0e9   # mm^3 -- bbox volume above this -> classify as span
MIN_VOL_MSportsCar  = 0.0     # mm^3 -- report any positive intersection volume

# ------------------------------------------------------------------------
# Geometry helpers
# ------------------------------------------------------------------------
Bbox = Tuple[float, float, float, float, float, float]  # xmin xmax ymin ymax zmin zmax


def _bvol(b: Bbox) -> float:
    return (max(0.0, b[1] - b[0])
            * max(0.0, b[3] - b[2])
            * max(0.0, b[5] - b[4]))


def _bunion(mesh: List[Bbox]) -> Bbox:
    return (min(b[0] for b in mesh), max(b[1] for b in mesh),
            min(b[2] for b in mesh), max(b[3] for b in mesh),
            min(b[4] for b in mesh), max(b[5] for b in mesh))


def _boverlap(a: Bbox, b: Bbox) -> float:
    dx = min(a[1], b[1]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[2], b[2])
    dz = min(a[5], b[5]) - max(a[4], b[4])
    return dx * dy * dz if (dx > 0 and dy > 0 and dz > 0) else 0.0


# ------------------------------------------------------------------------
# Data types
# ------------------------------------------------------------------------
@dataclass
class Part:
    solid:   object
    name:    str
    sub_asm: str
    major:   str
    parent:  str
    bbox:    Bbox
    is_span: bool = False


@dataclass
class Hit:
    a:     Part
    b:     Part
    vol:   float   # mm^3
    level: str     # INTER_PARENT | INTRA_PARENT | INTRA_MAJOR
    exact: bool    # True = exact boolean,  False = bbox estimate


def _level(a: Part, b: Part) -> str:
    if a.parent != b.parent:
        return "INTER_PARENT"
    if a.major != b.major:
        return "INTRA_PARENT"
    return "INTRA_MAJOR"


# ------------------------------------------------------------------------
# Loading
# ------------------------------------------------------------------------
def load() -> Tuple[
    Dict[str, List[Part]],   # sub-asm name  -> [Part, ...]
    Dict[str, Bbox],         # sub-asm name  -> union bbox
    Dict[str, Bbox],         # major name    -> union bbox
    Dict[str, Bbox],         # parent name   -> union bbox
]:
    print("[1/3] Loading assembly ...")
    sys.path.insert(0, os.path.dirname(__file__) or ".")
    from vehiclecad.vehicle import detailed_complete_vehicle as assembly  # noqa: PLC0415

    sub_parts:  Dict[str, List[Part]]  = defaultdict(list)
    major_mesh:  Dict[str, List[Bbox]]  = defaultdict(list)
    parent_mesh: Dict[str, List[Bbox]]  = defaultdict(list)

    for sub_name, raw_parts in assembly.subassemblies().items():
        major  = SUB_TO_MAJOR.get(sub_name, "OTHER")
        parent = MAJOR_TO_PARENT.get(major, "OTHER")
        for solid, _color, name in raw_parts:
            bb   = solid.BoundingBox()
            bbox = (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)
            span = (_bvol(bbox) > SPAN_VOL_MSportsCar
                    or any(name.startswith(s) for s in SKIP_NAME_PREFIXES))
            p = Part(solid=solid, name=name, sub_asm=sub_name,
                     major=major, parent=parent, bbox=bbox, is_span=span)
            sub_parts[sub_name].append(p)
            major_mesh[major].append(bbox)
            parent_mesh[parent].append(bbox)

    sub_bbox    = {k: _bunion([p.bbox for p in v]) for k, v in sub_parts.items()}
    major_bbox  = {m: _bunion(v) for m, v in major_mesh.items()}
    parent_bbox = {p: _bunion(v) for p, v in parent_mesh.items()}

    n_total = sum(len(v) for v in sub_parts.values())
    n_span  = sum(1 for v in sub_parts.values() for p in v if p.is_span)
    print(f"    {n_total} parts  ({n_span} span/skip)  |  "
          f"{len(sub_parts)} sub-asms  |  "
          f"{len(major_bbox)} major groups  |  "
          f"{len(parent_bbox)} parent groups")
    all_parts_flat = [p for v in sub_parts.values() for p in v]
    for par in sorted(parent_bbox):
        majors = sorted({p.major for p in all_parts_flat if p.parent == par})
        n = sum(1 for p in all_parts_flat if p.parent == par)
        print(f"      [{par:<14s}]  {n:3d} parts   groups: {', '.join(majors)}")

    return sub_parts, sub_bbox, major_bbox, parent_bbox


# ------------------------------------------------------------------------
# AABB overlap matrix
# ------------------------------------------------------------------------
def print_matrix(major_bbox: Dict[str, Bbox]) -> None:
    names = sorted(major_bbox)
    col_w = max(len(n) for n in names) + 1
    cw    = 10
    print("  Major-group bounding-box overlap  (% of smaller group's envelope)\n")
    header = " " * (col_w + 4) + "".join(n[:cw - 1].ljust(cw) for n in names)
    print(header)
    for a in names:
        row = f"  {a:<{col_w}}  "
        for b in names:
            if a == b:
                row += f"{'---':<{cw}}"
                continue
            ov = _boverlap(major_bbox[a], major_bbox[b])
            if ov <= 0:
                row += f"{'0':<{cw}}"
            else:
                pct = 100.0 * ov / min(_bvol(major_bbox[a]), _bvol(major_bbox[b]))
                row += f"{pct:.0f}%".ljust(cw)
        print(row)
    print()


# ------------------------------------------------------------------------
# Detection  (BVH top-down traversal)
# ------------------------------------------------------------------------
def detect(
    sub_parts:   Dict[str, List[Part]],
    sub_bbox:    Dict[str, Bbox],
    major_bbox:  Dict[str, Bbox],
    parent_bbox: Dict[str, Bbox],
    fast:        bool = False,
    threshold:   float = MIN_VOL_MSportsCar,
    only_majors: Optional[Tuple[str, str]] = None,
    honor_interfaces: bool = True,
) -> List[Hit]:
    results: List[Hit] = []
    pruned = dict(par=0, maj=0, sub=0, part=0, iface=0)
    n_exact = 0
    t0 = time.time()

    sub_names = sorted(sub_parts.keys())
    n_pairs   = len(sub_names) * (len(sub_names) - 1) // 2
    print(f"[3/3] Running hierarchical detection  ({n_pairs} sub-asm pairs to evaluate) ...")

    ZERO_BOX: Bbox = (0.0,) * 6

    for i, sa in enumerate(sub_names):
        parts_a = sub_parts[sa]
        if not parts_a:
            continue
        rep_a = parts_a[0]
        ma, pa = rep_a.major, rep_a.parent

        for sb in sub_names[i + 1:]:
            parts_b = sub_parts[sb]
            if not parts_b:
                continue
            rep_b = parts_b[0]
            mb, pb = rep_b.major, rep_b.parent

            # --only filter
            if only_majors:
                if frozenset([ma, mb]) != frozenset(only_majors):
                    continue

            # BVH Level 1: parent-group bbox
            if pa != pb:
                if _boverlap(parent_bbox.get(pa, ZERO_BOX),
                             parent_bbox.get(pb, ZERO_BOX)) <= 0:
                    pruned["par"] += 1
                    continue

            # BVH Level 2: major-group bbox
            if ma != mb:
                if _boverlap(major_bbox.get(ma, ZERO_BOX),
                             major_bbox.get(mb, ZERO_BOX)) <= 0:
                    pruned["maj"] += 1
                    continue

            # BVH Level 3: sub-asm bbox
            if _boverlap(sub_bbox[sa], sub_bbox[sb]) <= 0:
                pruned["sub"] += 1
                continue

            # BVH Level 4: individual part-pair bboxes
            for part_a in parts_a:
                if part_a.is_span:
                    continue
                for part_b in parts_b:
                    if part_b.is_span:
                        continue
                    if _boverlap(part_a.bbox, part_b.bbox) <= 0:
                        pruned["part"] += 1
                        continue

                    if honor_interfaces:
                        reason = interface_reason(
                            part_a.name, part_b.name, part_a.sub_asm, part_b.sub_asm
                        )
                        if reason:
                            pruned["iface"] += 1
                            continue

                    if fast:
                        vol = _boverlap(part_a.bbox, part_b.bbox)
                        if vol > threshold:
                            results.append(Hit(
                                part_a, part_b, vol,
                                _level(part_a, part_b), exact=False))
                        continue

                    # Exact boolean intersection
                    n_exact += 1
                    if n_exact % 10 == 0:
                        print(f"  ... {n_exact:4d} exact | {len(results):3d} hits | "
                              f"{time.time() - t0:.0f}s",
                              end="\r", flush=True)
                    try:
                        vol = part_a.solid.intersect(part_b.solid).Volume()
                    except Exception:
                        vol = 0.0
                    if vol > threshold:
                        lv = _level(part_a, part_b)
                        results.append(Hit(part_a, part_b, vol, lv, exact=True))
                        print(f"  [HIT] {part_a.name[:36]:36s} x "
                              f"{part_b.name[:36]:36s} = "
                              f"{vol / 1000:.2f} cc  [{lv}]")

    elapsed = time.time() - t0
    print(f"\n  {n_exact} exact checks, {len(results)} collisions, {elapsed:.1f}s")
    print(f"  Pruned: {pruned['par']} parent-level  "
          f"{pruned['maj']} major-level  "
          f"{pruned['sub']} sub-asm-level  "
          f"{pruned['part']} part-bbox-level  "
          f"{pruned['iface']} allowed-interface")
    return results


# ------------------------------------------------------------------------
# Reporting
# ------------------------------------------------------------------------
_LABELS = {
    "INTER_PARENT": "INTER-PARENT   packaging clashes between major systems",
    "INTRA_PARENT": "INTRA-PARENT   cross-system within same parent assembly",
    "INTRA_MAJOR":  "INTRA-MAJOR    close-fit / interface within same group",
}


def report(results: List[Hit]) -> None:
    if not results:
        print("\n  No collisions above threshold -- assembly is clean!")
        return

    by_level: Dict[str, List[Hit]] = defaultdict(list)
    for r in results:
        by_level[r.level].append(r)

    for level in ["INTER_PARENT", "INTRA_PARENT", "INTRA_MAJOR"]:
        bucket = by_level.get(level, [])
        if not bucket:
            continue
        print(f"\n  {'=' * 78}")
        print(f"  {_LABELS[level]}   ({len(bucket)} collisions)")
        print(f"  {'=' * 78}")

        by_pair: Dict[tuple, List[Hit]] = defaultdict(list)
        for r in bucket:
            by_pair[tuple(sorted([r.a.major, r.b.major]))].append(r)

        for pair, grp in sorted(by_pair.items(),
                                key=lambda x: -sum(h.vol for h in x[1])):
            tv = sum(h.vol for h in grp)
            print(f"\n    {pair[0]}  <->  {pair[1]}"
                  f"  ({len(grp)} hits,  {tv / 1000:.1f} cc total)")
            for r in sorted(grp, key=lambda x: -x.vol):
                tag = "" if r.exact else "  [bbox approx]"
                vs = (f"{r.vol / 1000:.2f} cc"
                      if r.vol >= 1000 else f"{r.vol:.0f} msportscar")
                print(f"      {r.a.sub_asm:28s}  {r.a.name[:38]:38s}"
                      f"  x  {r.b.sub_asm:28s}  {r.b.name[:38]:38s}"
                      f"  =  {vs}{tag}")

    tot = sum(r.vol for r in results)
    print(f"\n  {'=' * 78}")
    print(f"  TOTAL: {len(results)} collisions  |  {tot / 1e6:.3f} csportscar total interference")


def save_csv(hits: List[Hit], path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["level",
                    "parent_a", "major_a", "sub_asm_a", "part_a",
                    "parent_b", "major_b", "sub_asm_b", "part_b",
                    "vol_msportscar", "vol_cc", "exact"])
        for r in sorted(hits, key=lambda x: -x.vol):
            w.writerow([
                r.level,
                r.a.parent, r.a.major, r.a.sub_asm, r.a.name,
                r.b.parent, r.b.major, r.b.sub_asm, r.b.name,
                f"{r.vol:.1f}", f"{r.vol / 1000:.3f}", r.exact,
            ])
    print(f"  Saved  ->  {path}")


# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fast",      action="store_true",
                    help="AABB overlap only -- skip exact boolean")
    ap.add_argument("--threshold", type=float, default=MIN_VOL_MSportsCar,
                    help=f"Min interference volume msportscar (default {MIN_VOL_MSportsCar})")
    ap.add_argument("--only",      nargs=2, metavar="MAJOR",
                    help="Check only one major-group pair  e.g. --only POWERTRAIN CHASSIS")
    ap.add_argument("--matrix",    action="store_true",
                    help="Print AABB overlap matrix then exit")
    ap.add_argument("--strict",    action="store_true",
                    help="Report designed contact interfaces as collisions too")
    ap.add_argument("--output",    default="results/collisions_v3.csv",
                    help="CSV output path")
    args = ap.parse_args()

    print("\n  Classic SportsCar ModelA  --  Hierarchical Collision Checker  (v3)")
    print(f"  {'=' * 58}\n")

    sub_parts, sub_bbox, major_bbox, parent_bbox = load()

    print("\n[2/3] AABB overlap matrix:")
    print_matrix(major_bbox)

    if args.matrix:
        return

    results = detect(
        sub_parts, sub_bbox, major_bbox, parent_bbox,
        fast=args.fast,
        threshold=args.threshold,
        only_majors=tuple(args.only) if args.only else None,
        honor_interfaces=not args.strict,
    )

    print("\n[Results]")
    report(results)
    save_csv(results, args.output)
    sys.exit(1 if results else 0)


if __name__ == "__main__":
    main()
