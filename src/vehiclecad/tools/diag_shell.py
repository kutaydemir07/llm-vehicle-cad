"""Fast body-shell shape check: render the raw lofted outer shell + greenhouse
(BEFORE the expensive panel split) so we can judge boxiness vs rounding quickly.

    PYTHONPATH=src python -m vehiclecad.tools.diag_shell
"""
from __future__ import annotations
import time
from pathlib import Path
from vehiclecad.core.reference import common as C
from vehiclecad.parts.exterior.detail import frontend, rearend
from vehiclecad.vehicle import studio

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = str(_PROJECT_ROOT / "exports" / "screenshots" / "diag_shell.png")


def main():
    t0 = time.time()
    outer = C.U([C.loft(C.BODY, ruled=True), C.greenhouse_solid()])
    for ax, radius in ((C.AXLE_F, 352), (C.AXLE_R, 360)):
        for side in (1, -1):
            outer = outer.cut(C.cyl(radius, 460, (ax, side * 470, 300), (0, side, 0)))
    for cutter in frontend.body_cutters() + rearend.body_cutters():
        outer = outer.cut(cutter)
    outer = outer.cut(C.window_cutters())
    print(f"shell built in {time.time()-t0:.1f}s")
    parts = [(outer, C.RED, "outer_skin")]
    views = [
        ("side", (0.0, 1.0, 0.02), None, 1.3),
        ("3q front", (-1.0, 0.6, 0.28), None, 1.25),
        ("3q rear", (1.0, 0.6, 0.30), None, 1.25),
        ("top", (0.0, 0.05, 1.0), None, 1.3),
    ]
    studio.render(parts, OUT, views, lin=0.25, ang=0.15, ground=False)
    print(f"{time.time()-t0:.1f}s total")


if __name__ == "__main__":
    main()
