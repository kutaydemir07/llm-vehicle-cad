"""True BIW cutaway: build the REAL hollow body shell (outer flat-panel loft
MINUS inner cavity = the sheet-metal wall) with door/window/lamp openings, keep
the near half, and render it so the flat panels and wall thickness are visible.

    PYTHONPATH=src python -m vehiclecad.tools.diag_biw
"""
from __future__ import annotations
import time
from pathlib import Path
from cadquery import Solid, Vector
from vehiclecad.core.reference import common as C
from vehiclecad.parts.body.structure import body as body_shell
from vehiclecad.parts.exterior.detail import frontend, rearend
from vehiclecad.vehicle import studio

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = str(_PROJECT_ROOT / "exports" / "screenshots" / "diag_biw.png")


def real_shell():
    # door apertures so the BIW reads as a real shell with openings
    door = C.box(1505, -905, 300, 980, 1810, 716)
    return body_shell._panel_tool().cut(door)


def half(parts, keepy=0.0):
    cut = Solid.makeBox(9000, 4000, 5000, Vector(-2500, keepy - 4000, -700))
    out = []
    for s, rgb, nm in parts:
        try:
            c = s.intersect(cut)
            if c.Volume() > 1.0:
                out.append((c, rgb, nm))
        except Exception:
            out.append((s, rgb, nm))
    return out


def main():
    t0 = time.time()
    shell = real_shell()
    print(f"real BIW shell built in {time.time()-t0:.1f}s  vol={shell.Volume()/1000:.0f} cc")
    parts = [(shell, C.RED, "biw_shell")] + frontend.parts() + rearend.parts()
    cut = half(parts, keepy=0.0)        # keep y<=0 half -> see the hollow interior
    views = [
        ("cutaway 3/4", (-0.9, -0.5, 0.30), None, 1.25),
        ("cutaway side", (0.0, -1.0, 0.03), None, 1.3),
        ("full side", (0.0, 1.0, 0.03), None, 1.3),
        ("cutaway rear 3/4", (0.9, -0.5, 0.30), None, 1.25),
    ]
    # full side uses the un-cut parts so we see the outer skin too
    full = [(shell, C.RED, "biw_shell")] + frontend.parts() + rearend.parts()
    studio.render(cut[: -0] or cut, OUT, views[:2] + views[3:], lin=0.2, ang=0.12, ground=False)
    studio.render(full, OUT.replace(".png", "_outer.png"),
                  [("side", (0.0, 1.0, 0.03), None, 1.3),
                   ("3/4 front", (-1.0, 0.55, 0.16), None, 1.25)],
                  lin=0.25, ang=0.15, ground=True)
    print(f"{time.time()-t0:.1f}s total")


if __name__ == "__main__":
    main()
