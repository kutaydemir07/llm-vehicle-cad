"""Production-readiness audit across ALL emitted parts.

For every part in the complete vehicle it records bbox, volume, solid count and
FACE COUNT (a good proxy for geometric detail: a plain box=6, cylinder=3, while a
real casting/forging has dozens).  It then flags likely PLACEHOLDERS (low face
count but non-trivial size) so we can target which parts still need real geometry.

    PYTHONPATH=src python -m vehiclecad.tools.audit_quality
"""
from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path
from vehiclecad.vehicle import detailed_complete_vehicle as veh

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = str(_PROJECT_ROOT / "reports" / "quality_audit.csv")


def nfaces(s):
    try:
        return len(s.Faces())
    except Exception:
        return -1


def main():
    # system ownership: walk the product tree so each part keeps its system tag
    from vehiclecad.assemblies.product_tree import product_tree, build_atomic_part
    rows = []
    by_system = defaultdict(lambda: [0, 0])   # system -> [count, placeholders]
    for system, subsystems in product_tree().items():
        for subsystem, subas in subsystems.items():
            for sub, specs in subas.items():
                for spec in specs:
                    s, _c, name = build_atomic_part(spec)
                    bb = s.BoundingBox()
                    f = nfaces(s)
                    vol = 0.0
                    try:
                        vol = s.Volume()
                    except Exception:
                        pass
                    dx, dy, dz = bb.xlen, bb.ylen, bb.zlen
                    # placeholder heuristic: few faces but a real-sized solid that
                    # should be a detailed part (skip thin plates/strips & tiny bits)
                    mindim = min(dx, dy, dz)
                    is_strip = mindim < 12 and f <= 6      # genuine flat plate/strip/trim
                    placeholder = (0 <= f <= 8) and vol > 30_000 and not is_strip
                    rows.append((system, name, f, round(vol/1000, 1),
                                 round(dx), round(dy), round(dz),
                                 round(bb.xmin), round(bb.xmax),
                                 round(bb.ymin), round(bb.ymax),
                                 round(bb.zmin), round(bb.zmax),
                                 "PLACEHOLDER" if placeholder else ""))
                    by_system[system][0] += 1
                    by_system[system][1] += 1 if placeholder else 0

    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["system", "part", "n_faces", "vol_cc", "dx", "dy", "dz",
                    "xmin", "xmax", "ymin", "ymax", "zmin", "zmax", "flag"])
        w.writerows(rows)

    print(f"audited {len(rows)} parts -> {OUT}\n")
    print(f"{'SYSTEM':<34s} parts  placeholders")
    for sysn in sorted(by_system):
        c, p = by_system[sysn]
        print(f"{sysn:<34s} {c:4d}   {p:3d}{'  <--' if p else ''}")
    ph = [r for r in rows if r[-1]]
    print(f"\n{len(ph)} flagged placeholders (low face-count, real size):")
    for r in sorted(ph, key=lambda r: -r[3])[:40]:
        print(f"  {r[1]:<44s} faces={r[2]:<3d} vol={r[3]:>7}cc  {r[0]}")


if __name__ == "__main__":
    main()
