"""Write a per-atomic-part ModelA SportsCar detail audit report."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from vehiclecad.validation.atomic_detail import audit_atomic_detail


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit atomic part specs for ModelA SportsCar detail quality.")
    parser.add_argument("--root", default="src/vehiclecad", help="vehiclecad source root.")
    parser.add_argument("--report", default="reports/atomic_detail_audit.csv", help="CSV report path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    rows = audit_atomic_detail(args.root)
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with report_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].__dataclass_fields__) if rows else [])
        if rows:
            writer.writeheader()
            for row in rows:
                writer.writerow(row.__dict__)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    fail_count = counts.get("fail", 0)
    review_count = counts.get("review", 0)
    print(
        f"Atomic detail audit: {len(rows)} part(s), "
        f"{fail_count} fail, {review_count} review"
    )
    print(f"Report -> {report_path}")
    return 1 if fail_count else 0


if __name__ == "__main__":
    raise SystemExit(main())

