"""V-model System 1000 - Body / Structure.

Body-in-white (the welded structural skeleton + the welded outer skin) and the
closures (hood / doors / trunk lid / fuel flap).  ``biw_parts()`` and
``closure_parts()`` are kept separate so the assembly tree can show
``ASM_1000_Body_Structure`` and ``ASM_1200_Closures`` as distinct nodes.
"""
from __future__ import annotations

from . import (firewall, floorpan, pillar, pillars, rocker,
               roof, roof_structure, strut, strut_towers, wheel_tub,
               engine_bay, trunk, body)


def biw_parts():
    """Body-in-white: welded structural skeleton + the outer welded skin.

    The engine-bay (Motorraum) and trunk (Kofferraum) enclosures are part of the
    BiW: they are the inner sheet-metal that turns the open cavities into real
    compartments.  ``trunk`` also carries the rear-seat bulkhead that divides the
    cabin from the boot (replacing the old floating ``firewall_bulkhead`` box).
    """
    out = []
    out.extend(firewall.parts())
    out.extend(floorpan.parts())
    out.extend(pillar.parts())
    out.extend(pillars.parts())
    out.extend(rocker.parts())
    out.extend(roof.parts())
    out.extend(roof_structure.parts())
    out.extend(strut.parts())            # strut TOWERS (structure)
    out.extend(strut_towers.parts())
    out.extend(wheel_tub.parts())
    out.extend(engine_bay.parts())       # Motorraum: rad support + inner fenders
    out.extend(trunk.parts())            # Kofferraum: floor + well + bulkhead + shelf
    out.extend(body.body_parts())        # outer welded skin + fuel flap
    return out


def closure_parts():
    """Closures: hood / doors / trunk lid carved along the shut-lines."""
    return body.closure_parts()


def parts():
    return biw_parts() + closure_parts()
