"""Fast front/rear END assembly check: the raw lofted shell (WITH lamp/grille
apertures already cut) + the lamp/grille/fascia inserts, so we can see whether
the inserts fill their apertures or leave 'empty space'.  Skips the 82s panel
split.

    PYTHONPATH=src python -m vehiclecad.tools.diag_ends
"""
from __future__ import annotations
import time
from pathlib import Path
from vehiclecad.core.reference import common as C
from vehiclecad.parts.exterior.detail import frontend, rearend
from vehiclecad.vehicle import studio

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = str(_PROJECT_ROOT / "exports" / "screenshots" / "diag_ends.png")


def _shell():
    outer = C.U([C.loft(C.BODY, ruled=True), C.greenhouse_solid()])
    for ax, radius in ((C.AXLE_F, 352), (C.AXLE_R, 360)):
        for side in (1, -1):
            outer = outer.cut(C.cyl(radius, 460, (ax, side * 470, 300), (0, side, 0)))
    for cutter in frontend.body_cutters() + rearend.body_cutters():
        outer = outer.cut(cutter)
    outer = outer.cut(C.window_cutters())
    return outer


def main():
    t0 = time.time()
    parts = [(_shell(), C.RED, "outer_skin")]
    parts += frontend.parts() + rearend.parts()
    print(f"built {len(parts)} parts in {time.time()-t0:.1f}s")
    views = [
        ("front", (-1.0, 0.0, 0.05), (60, 0, 690), 1.9),
        ("front 3/4", (-1.0, 0.45, 0.22), (120, 250, 660), 1.7),
        ("rear", (1.0, 0.0, 0.05), (4340, 0, 690), 1.9),
        ("rear 3/4", (1.0, 0.45, 0.22), (4280, 250, 680), 1.7),
    ]
    studio.render(parts, OUT, views, lin=0.22, ang=0.13, ground=False)
    print(f"{time.time()-t0:.1f}s total")


if __name__ == "__main__":
    main()
