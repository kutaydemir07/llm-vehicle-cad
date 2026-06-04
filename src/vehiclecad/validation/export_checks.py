from __future__ import annotations

from pathlib import Path


def validate_export_file(path: str | Path) -> list[str]:
    file_path = Path(path)
    if not file_path.exists():
        return [f"export missing: {file_path}"]
    if file_path.stat().st_size <= 0:
        return [f"export is empty: {file_path}"]
    return []

