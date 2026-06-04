from __future__ import annotations

import argparse
import csv
from pathlib import Path

from vehiclecad.validation.vmodel_structure import audit_vmodel_structure


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit emitted CAD parts and source structure for V-model violations.")
    parser.add_argument("--root", default="src/vehiclecad")
    parser.add_argument("--out", default="reports/vmodel_structure_audit.csv")
    args = parser.parse_args(argv)

    issues = audit_vmodel_structure(args.root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["scope", "item", "detail"])
        for issue in issues:
            writer.writerow([issue.scope, issue.item, issue.detail])

    print(f"V-model structure audit: {len(issues)} issue(s)")
    print(f"Report -> {out}")
    for issue in issues[:40]:
        print(f"- {issue.scope}: {issue.item} ({issue.detail})")
    if len(issues) > 40:
        print(f"... +{len(issues) - 40} more")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

