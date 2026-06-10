"""Fast pairwise interference probe between source groups.

Builds only the named source groups (not the whole vehicle) and reports every
exact part-pair intersection across DIFFERENT groups, so a routing change can
be iterated in seconds instead of re-running the full collision gate.

    PYTHONPATH=src python -m vehiclecad.tools.probe_pairs chassis_crossmembers body_floorpan ...
    PYTHONPATH=src python -m vehiclecad.tools.probe_pairs --within chassis_crossmembers   # intra-group too
"""
from __future__ import annotations

import argparse
import sys

from vehiclecad.assemblies.source_collectors import group_parts


def _bbox(solid):
    bb = solid.BoundingBox()
    return (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)


def _overlap(a, b):
    dx = min(a[1], b[1]) - max(a[0], b[0])
    dy = min(a[3], b[3]) - max(a[2], b[2])
    dz = min(a[5], b[5]) - max(a[4], b[4])
    return dx > 0 and dy > 0 and dz > 0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="+")
    ap.add_argument("--within", action="store_true",
                    help="also check pairs inside the same group")
    ap.add_argument("--min-cc", type=float, default=0.05)
    args = ap.parse_args()

    loaded = []   # (slug, name, solid, bbox)
    for slug in args.slugs:
        for part in group_parts(slug):
            solid, _c, name = part[:3]
            loaded.append((slug, name, solid, _bbox(solid)))
        print(f"loaded {slug}: {sum(1 for p in loaded if p[0] == slug)} parts")

    hits = 0
    for i in range(len(loaded)):
        for j in range(i + 1, len(loaded)):
            sa, na, pa, ba = loaded[i]
            sb, nb, pb, bb = loaded[j]
            if sa == sb and not args.within:
                continue
            if not _overlap(ba, bb):
                continue
            try:
                vol = pa.intersect(pb).Volume()
            except Exception:
                vol = 0.0
            if vol > args.min_cc * 1000.0:
                hits += 1
                print(f"  HIT {na:46s} x {nb:46s} = {vol / 1000:8.2f} cc")
    print(f"{hits} hits > {args.min_cc} cc")
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
