"""Fast region renderer for iterating on one area of the SportsCar without a full build.

    python render_region.py body            # body structure + closures + glazing
    python render_region.py body --section   # + a y=0 cut to reveal the interior
    python render_region.py ASM_1000_Body_Structure ASM_2000_Chassis

Renders the chosen sub-assembly nodes (or the named groups below) to
out/fig_region.png using the studio renderer.  ``--section`` keeps only the
y<=0 half of every solid so you can see into the engine bay / cabin / trunk.
"""
from __future__ import annotations
import sys
sys.path.insert(0, ".")
from cadquery import Solid, Vector
from vehiclecad.vehicle.detailed_complete_vehicle import subassemblies
from vehiclecad.vehicle import studio

GROUPS = {
    "body":   ["ASM_1000_Body_Structure", "ASM_1200_Closures", "ASM_10500_Glazing"],
    "biw":    ["ASM_1000_Body_Structure"],
    "shell":  ["ASM_1000_Body_Structure", "ASM_1200_Closures"],
    "front":  ["ASM_1000_Body_Structure", "ASM_2000_Chassis", "ASM_6000_Powertrain",
               "ASM_7000_Thermal_HVAC", "ASM_14000_Fasteners_Brackets"],
    "rear":   ["ASM_1000_Body_Structure", "ASM_2000_Chassis", "ASM_3000_Suspension",
               "ASM_6200_Driveline"],
}

VIEWS = [("side", (0.0, 1.0, 0.04), None, 1.3),
         ("front", (-1.0, 0.05, 0.10), None, 1.3),
         ("three-quarter front", (-1.0, 0.6, 0.32), None, 1.2),
         ("three-quarter rear", (1.0, 0.6, 0.32), None, 1.2)]


def _section(parts, keep_y_neg=True):
    half = Solid.makeBox(9000, 4000, 5000,
                         Vector(-2500, (-4000 if keep_y_neg else 0), -500))
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
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    section = "--section" in sys.argv
    nodes = []
    for a in args:
        nodes.extend(GROUPS.get(a, [a]))
    if not nodes:
        nodes = GROUPS["body"]
    subs = subassemblies()
    parts = []
    for n in nodes:
        parts.extend(subs.get(n, []))
    print(f"region: {nodes}  ({len(parts)} parts){'  [sectioned]' if section else ''}")
    if section:
        parts = _section(parts)
    studio.render(parts, "out/fig_region.png", VIEWS)


if __name__ == "__main__":
    main()

