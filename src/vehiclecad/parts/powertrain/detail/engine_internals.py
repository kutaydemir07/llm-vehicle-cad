"""I4_Engine engine internals  -  crankshaft, connecting rods, pistons, cams.

These are recognisable packaging shapes inside the engine envelope.

Collision-free:
  Crankshaft centreline at z=445 (block centreline)  -  well below the
  cylinder head (z>660) and oil pan (z<380).
  Pistons travel z=445 - 660 (stroke 86 mm, diam 93.4 mm).
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

_cyl  = C.cyl
_rbox = C.rbox
_U    = C.U
METAL = (0.55, 0.56, 0.60)
COL   = (0.35, 0.36, 0.40)

# I4_Engine bore spacing = 123 mm, 4 cylinders
_PORT_X = [490, 613, 736, 859]   # cylinder centreline x-positions


def _crankshaft():
    """Steel forged crankshaft  -  main shaft + 4 rod journals + 5 mains."""
    shaft = _cyl(28, 480, (390, 0, 445), (1, 0, 0))   # main journal axis
    mains = []
    rods  = []
    for i, px in enumerate(_PORT_X):
        main = _cyl(40, 28, (px - 14, 0, 445), (1, 0, 0))
        rod_journal = _cyl(30, 26, (px - 13, 20, 445), (1, 0, 0))  # offset for throw
        mains.append(main)
        rods.append(rod_journal)
    return _U([shaft] + mains + rods)


def _pistons_and_rods():
    """4  -  piston crown + small-end rod stub (simplified)."""
    parts = []
    for px in _PORT_X:
        piston = _cyl(46, 30, (px - 15, 0, 570), (1, 0, 0))  # piston crown disc
        rod    = C.swept_tube([(px, 0, 445), (px, 0, 570)], 14, cap=True)
        parts.extend([piston, rod])
    return _U(parts)


def _camshafts():
    """Inlet + exhaust camshafts sitting in the cylinder head, z - 730."""
    cam_in  = _cyl(16, 560, (400, -50, 728), (1, 0, 0))  # intake cam
    cam_ex  = _cyl(16, 560, (400,  50, 728), (1, 0, 0))  # exhaust cam
    return _U([cam_in, cam_ex])


def parts():
    out = []
    out.append((_crankshaft(),         METAL, "PRT_I4_Engine_Crankshaft"))
    out.append((_pistons_and_rods(),   METAL, "PRT_I4_Engine_Pistons_Rods"))
    out.append((_camshafts(),          METAL, "PRT_I4_Engine_Camshafts"))
    return out

