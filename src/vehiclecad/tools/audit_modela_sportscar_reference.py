"""Write the source-backed Classic ModelA SportsCar reference audit report."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from vehiclecad.validation.modela_sportscar_reference_checks import audit_modela_sportscar_reference


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit config, datums, and BOM signatures against ModelA SportsCar source data.")

    parser.add_argument("--report", default="reports/modela_sportscar_reference_audit.csv", help="CSV report path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    rows = audit_modela_sportscar_reference()
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with report_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].__dataclass_fields__) if rows else [])
        if rows:
            writer.writeheader()
            for row in rows:
                writer.writerow(row.__dict__)

    fail_count = sum(1 for row in rows if row.status == "fail")
    print(f"ModelA SportsCar reference audit: {len(rows)} check(s), {fail_count} fail")
    print(f"Report -> {report_path}")
    return 1 if fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
