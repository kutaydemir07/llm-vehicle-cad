"""V-model System 10000 - Exterior (aero kit, front fascia, rear bumper, trim, glazing, wheels).

``parts()`` returns the aero kit + front fascia + rear bumper + exterior trim.
Glazing is exposed via ``glazing_parts()`` and the road wheels via ``wheels.corner``
so the assembly tree can keep them as their own nodes.  Lamp assemblies will be
extracted from ``frontend``/``rearend`` into System 11000 in a later phase.
"""
from __future__ import annotations

from . import flare, skirt, splitter, deck, wing, misc
from . import frontend, rearend, trim, glazing, wheels


def aero_parts():
    out = []
    out.extend(flare.parts())
    out.extend(skirt.parts())
    out.extend(splitter.parts())
    out.extend(deck.parts())
    out.extend(wing.parts())
    out.extend(misc.parts())
    return out


def parts():
    out = aero_parts()
    out.extend(frontend.parts())     # front fascia + (for now) headlamps + grille
    out.extend(rearend.parts())      # rear bumper + (for now) tail lamps
    out.extend(trim.parts())         # rub strips, mouldings, mirrors, drip rails
    return out


def glazing_parts():
    return glazing.parts()
