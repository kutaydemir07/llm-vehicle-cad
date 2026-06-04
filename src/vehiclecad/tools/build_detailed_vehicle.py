"""Build the migrated high-detail vehicle assembly.

This uses the detailed subsystem modules now stored in the generic platform
areas under ``vehiclecad.parts`` and ``vehiclecad.core.reference``.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import cadquery as cq

from vehiclecad.assemblies.product_tree import connection_map, product_tree
from vehiclecad.vehicle.detailed_complete_vehicle import build


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the high-detail complete vehicle assembly.")
    parser.add_argument("--name", default="detailed_complete_vehicle", help="Base filename for exports.")
    parser.add_argument("--no-step", action="store_true", help="Skip STEP export.")
    parser.add_argument("--no-stl", action="store_true", help="Skip STL export.")
    parser.add_argument("--render", action="store_true", help="Render preview PNGs with PyVista.")
    return parser


def _print_tree(elapsed: float) -> None:
    tree = product_tree()
    total_parts = sum(
        len(specs)
        for subsystems in tree.values()
        for subassemblies in subsystems.values()
        for specs in subassemblies.values()
    )
    print(f"\n{'=' * 70}")
    print("  ASM_DETAILED_COMPLETE_VEHICLE")
    print(
        f"  {total_parts} atomic part files in {len(tree)} systems "
        f"({len(connection_map())} connection zones, {elapsed:.1f}s)"
    )
    print(f"{'=' * 70}")
    for system_name, subsystems in tree.items():
        system_count = sum(
            len(specs)
            for subassemblies in subsystems.values()
            for specs in subassemblies.values()
        )
        print(f"  +-- {system_name:<34} {system_count:>3} parts")
        for subsystem_name, subassemblies in subsystems.items():
            subsystem_count = sum(len(specs) for specs in subassemblies.values())
            print(f"  |   +-- {subsystem_name:<32} {subsystem_count:>3}")
            for subassembly_name, specs in subassemblies.items():
                print(f"  |   |   +-- {subassembly_name:<28} {len(specs):>3}")
                for spec in specs[:3]:
                    print(f"  |   |       * {spec.part_name}")
                if len(specs) > 3:
                    print(f"  |   |       ... +{len(specs) - 3} more")
    print(f"{'=' * 70}\n")


def _render(flat, output_dir: Path, name: str) -> None:
    from vehiclecad.vehicle.studio import render

    views = [
        ("three-quarter front", (-1.0, 0.8, 0.45), None, 1.25),
        ("side", (0.0, 1.0, 0.05), None, 1.25),
        ("front", (-1.0, 0.05, 0.12), None, 1.25),
        ("three-quarter rear", (1.0, 0.8, 0.42), None, 1.25),
    ]
    render(flat, output_dir / f"{name}.png", views)

    explode = {
        "PRT_ModelA_SportsCar_Hood_Outer_Panel": (0, 0, 360),
        "PRT_ModelA_SportsCar_Decklid_Outer_Panel": (230, 0, 300),
        "PRT_ModelA_SportsCar_Door_Outer_L": (0, 430, 0),
        "PRT_ModelA_SportsCar_Door_Outer_R": (0, -430, 0),
        "PRT_ModelA_SportsCar_Door_Glass_L": (0, 430, 0),
        "PRT_ModelA_SportsCar_Door_Glass_R": (0, -430, 0),
    }
    render(
        flat,
        output_dir / f"{name}_exploded.png",
        [("exploded closures", (-1.0, 0.7, 0.45), None, 1.05)],
        offsets=explode,
    )


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    t0 = time.time()
    asm, flat = build()
    elapsed = time.time() - t0
    _print_tree(elapsed)

    compound = asm.toCompound()
    bb = compound.BoundingBox()
    print(f"bbox(mm): {bb.xlen:.0f} x {bb.ylen:.0f} x {bb.zlen:.0f}")

    root = Path.cwd()
    step_dir = root / "exports" / "step"
    stl_dir = root / "exports" / "stl"
    screenshot_dir = root / "exports" / "screenshots"
    for output_dir in (step_dir, stl_dir, screenshot_dir):
        output_dir.mkdir(parents=True, exist_ok=True)

    if not args.no_step:
        step = step_dir / f"{args.name}.step"
        asm.export(str(step))
        print(f"STEP -> {step} ({step.stat().st_size / 1024:.0f} KB)")

    if not args.no_stl:
        stl = stl_dir / f"{args.name}.stl"
        cq.exporters.export(compound, str(stl), tolerance=0.4, angularTolerance=0.3)
        print(f"STL  -> {stl} ({stl.stat().st_size / 1024:.0f} KB)")

    if args.render:
        try:
            _render(flat, screenshot_dir, args.name)
        except Exception as exc:
            print(f"render failed ({exc}); exports are still valid")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
