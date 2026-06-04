from __future__ import annotations

from vehiclecad.interfaces.mount_points import MountInterface


def validate_mount_interface(interface: MountInterface) -> list[str]:
    failures = []
    seen = set()
    for point in interface.points:
        if point.name in seen:
            failures.append(f"duplicate mount point: {point.name}")
        seen.add(point.name)
        if point.normal == (0.0, 0.0, 0.0):
            failures.append(f"mount point has zero normal: {point.name}")
    return failures

