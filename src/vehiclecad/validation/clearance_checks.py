from __future__ import annotations

from vehiclecad.interfaces.clearance_envelopes import ClearanceEnvelope


def validate_clearance_envelope(envelope: ClearanceEnvelope) -> list[str]:
    if min(envelope.size) <= 0:
        return [f"clearance envelope has non-positive size: {envelope.name}"]
    return []

