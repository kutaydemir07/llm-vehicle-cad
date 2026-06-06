"""Truthful shell check: build the REAL body shell (outer loft MINUS the inner
cavity = the ~7mm sheet-metal wall, exactly like body.py), add the front/rear
end inserts, and render a y=0 SECTION so we can see the wall thickness and
whether the ends actually touch the body wall or float in a gap.

    PYTHONPATH=src python -m vehiclecad.tools.diag_section
"""
from __future__ import annotations
import time
from pathlib import Path
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.parts.body.structure import body as body_structure
from vehiclecad.parts.exterior.detail import frontend, rearend
from vehiclecad.vehicle import studio

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = str(_PROJECT_ROOT / "exports" / "screenshots" / "diag_section.png")


def real_shell():
    """Reproduce body.py's actual shell (outer tool minus inner cavity)."""
    return body_structure._panel_tool()


def section(parts, y=0.0):
    half = Solid.makeBox(9000, 4000, 5000, Vector(-2500, y - 4000, -500))
    out = []
    for s, rgb, nm in parts:
        try:
            c = s.intersect(half)
            if c.Volume() > 1.0:
                out.append((c, rgb, nm))
        except Exception:
            out.append((s, rgb, nm))
    return out


def main():
    t0 = time.time()
    shell = real_shell()
    print(f"real shell built in {time.time()-t0:.1f}s  vol={shell.Volume()/1000:.0f} cc")
    bb = shell.BoundingBox()
    print(f"shell bbox X[{bb.xmin:.0f},{bb.xmax:.0f}] Z[{bb.zmin:.0f},{bb.zmax:.0f}]")
    parts = [(shell, C.RED, "outer_skin")] + frontend.parts() + rearend.parts()
    sec = section(parts, y=40.0)       # cut just left of centre to keep the lamps
    views = [
        ("front cut", (0.0, -1.0, 0.05), (300, 0, 600), 1.7),
        ("front end cut", (0.0, -1.0, 0.0), (90, 0, 690), 3.2),
        ("rear cut", (0.0, -1.0, 0.05), (4050, 0, 600), 1.7),
        ("rear end cut", (0.0, -1.0, 0.0), (4320, 0, 690), 3.0),
    ]
    studio.render(sec, OUT, views, lin=0.2, ang=0.12, ground=False)
    print(f"{time.time()-t0:.1f}s total")


if __name__ == "__main__":
    main()
