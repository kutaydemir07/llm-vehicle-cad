"""Fast targeted area diagnostic: build only the named modules (NOT the full
385-part vehicle) and render tight close-ups, so we can iterate quickly on one
problem zone (springs, lamps, body) without paying the 190s full build.

    PYTHONPATH=src python -m vehiclecad.tools.diag_area springs
    PYTHONPATH=src python -m vehiclecad.tools.diag_area frontlamps
    PYTHONPATH=src python -m vehiclecad.tools.diag_area rear
"""
from __future__ import annotations
import sys, time
from importlib import import_module
from vehiclecad.vehicle import studio


def _collect(specs):
    parts = []
    for mod_path, fn in specs:
        m = import_module(mod_path)
        parts.extend(getattr(m, fn)())
    return parts


AREAS = {
    # front suspension corner: strut + spring + LCA + knuckle (+ tyre/rim context)
    "springs": (
        [("vehiclecad.parts.suspension.detail.front_macpherson", "parts"),
         ("vehiclecad.parts.suspension.detail.rear_semitrailing", "parts")],
        [("front spring 3/4", (-0.4, 1.0, 0.15), (810, 560, 600), 3.2),
         ("front spring side", (0.0, 1.0, 0.0), (810, 560, 560), 3.4),
         ("rear spring 3/4", (-0.4, 1.0, 0.15), (3300, 540, 600), 3.0),
         ("rear corner", (0.3, 1.0, 0.1), (3300, 560, 500), 2.8)],
    ),
    "frontlamps": (
        [("vehiclecad.parts.exterior.detail.frontend", "parts")],
        [("front", (-1.0, 0.0, 0.06), (60, 0, 700), 2.0),
         ("front 3/4", (-1.0, 0.35, 0.18), (60, 300, 680), 2.0),
         ("lamp L", (-1.0, 0.1, 0.05), (60, 466, 700), 3.6),
         ("grille", (-1.0, 0.0, 0.0), (60, 0, 700), 3.2)],
    ),
    "rear": (
        [("vehiclecad.parts.exterior.detail.rearend", "parts")],
        [("rear", (1.0, 0.0, 0.06), (4340, 0, 690), 1.8),
         ("rear 3/4", (1.0, 0.35, 0.18), (4340, 300, 690), 1.9),
         ("lamp L", (1.0, 0.1, 0.05), (4340, 400, 690), 3.0),
         ("centre", (1.0, 0.0, 0.0), (4340, 0, 700), 3.0)],
    ),
}


def main():
    area = sys.argv[1] if len(sys.argv) > 1 else "springs"
    specs, views = AREAS[area]
    t0 = time.time()
    parts = _collect(specs)
    print(f"built {len(parts)} parts in {time.time()-t0:.1f}s")
    for s, rgb, nm in parts:
        bb = s.BoundingBox()
        print(f"  {nm:34s} X[{bb.xmin:.0f},{bb.xmax:.0f}] Y[{bb.ymin:.0f},{bb.ymax:.0f}] Z[{bb.zmin:.0f},{bb.zmax:.0f}]")
    out = f"exports/screenshots/diag_{area}.png"
    studio.render(parts, out, views, lin=0.25, ang=0.15, ground=False)
    print(f"{time.time()-t0:.1f}s total")


if __name__ == "__main__":
    main()
