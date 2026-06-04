from __future__ import annotations

from vehiclecad.interfaces.hole_patterns import HolePattern


def validate_hole_pattern(pattern: HolePattern) -> list[str]:
    failures = []
    seen = set()
    for hole in pattern.holes:
        if hole.name in seen:
            failures.append(f"duplicate hole name: {hole.name}")
        seen.add(hole.name)
        if hole.diameter <= 0:
            failures.append(f"hole diameter must be positive: {hole.name}")
        if hole.kind == "blind" and hole.depth is None:
            failures.append(f"blind hole missing depth: {hole.name}")
    return failures

