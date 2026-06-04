"""Diagnostic renderer: build the full vehicle and render hero + close-up views
so we can SEE the reported problems (body rounding, lamp gaps, springs, flying parts).

    PYTHONPATH=src python -m vehiclecad.tools.diag_render
"""
from __future__ import annotations
import sys, time
import numpy as np
from vehiclecad.vehicle import detailed_complete_vehicle as veh
from vehiclecad.vehicle import studio


def main():
    t0 = time.time()
    parts = veh.parts()
    print(f"built {len(parts)} parts in {time.time()-t0:.1f}s")

    # overall bounding box + flag any wildly out-of-envelope parts
    import cadquery as cq
    xs = []
    flyers = []
    for s, rgb, nm in parts:
        try:
            bb = s.BoundingBox()
        except Exception:
            continue
        xs.append((bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax, nm))
    gx0 = min(b[0] for b in xs); gx1 = max(b[1] for b in xs)
    gy0 = min(b[2] for b in xs); gy1 = max(b[3] for b in xs)
    gz0 = min(b[4] for b in xs); gz1 = max(b[5] for b in xs)
    print(f"OVERALL BBOX  X[{gx0:.0f},{gx1:.0f}] Y[{gy0:.0f},{gy1:.0f}] Z[{gz0:.0f},{gz1:.0f}]")
    print(f"  length={gx1-gx0:.0f} width={gy1-gy0:.0f} height={gz1-gz0:.0f}  (target 4345 x 1680 x ~1370)")

    # parts poking outside a sane envelope (allowing margin)
    print("\n-- parts outside sane envelope (X<-60 or X>4420 or |Y|>900 or Z<-20 or Z>1500) --")
    n = 0
    for (x0, x1, y0, y1, z0, z1, nm) in xs:
        if x0 < -60 or x1 > 4420 or y0 < -900 or y1 > 900 or z0 < -20 or z1 > 1500:
            print(f"  {nm:48s} X[{x0:.0f},{x1:.0f}] Y[{y0:.0f},{y1:.0f}] Z[{z0:.0f},{z1:.0f}]")
            n += 1
            if n > 40:
                print("  ... (more)")
                break
    if n == 0:
        print("  none")

    views = [
        ("3q front", (-1.0, 0.62, 0.30), None, 1.25),
        ("side", (0.0, 1.0, 0.04), None, 1.25),
        ("3q rear", (1.0, 0.66, 0.32), None, 1.25),
        ("front", (-1.0, 0.05, 0.10), None, 1.25),
    ]
    studio.render(parts, "exports/screenshots/diag_hero.png", views, lin=0.4, ang=0.3)

    # close-ups
    close = [
        ("front lamps", (-1.0, 0.10, 0.10), (300, 0, 680), 2.6),
        ("rear lamps", (1.0, 0.10, 0.12), (4100, 0, 680), 2.6),
        ("front corner", (-0.2, 1.0, 0.05), (810, 600, 430), 2.4),
        ("rear corner", (0.2, 1.0, 0.05), (3372, 600, 430), 2.4),
    ]
    studio.render(parts, "exports/screenshots/diag_closeups.png", close, lin=0.3, ang=0.2)
    print(f"\ntotal {time.time()-t0:.1f}s")


if __name__ == "__main__":
    main()
