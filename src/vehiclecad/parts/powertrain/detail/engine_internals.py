"""I4_Engine engine internals -- crankshaft, connecting rods, pistons, cams.

Drawn as the real rotating assembly, statically posed at a flat-plane crank
position (throws 1 and 4 up, 2 and 3 down, stroke 80):

  * crankshaft: five r28 main journals on the z445 axis, full crank WEBS
    (r48, inside the block's r52 crank tunnel), and four r24 rod journals
    offset +/-40 in Z;
  * each connecting rod runs from a BORED big-end (r24.5 over its journal --
    a bearing fit, not an embed) up to the piston pin; pistons are VERTICAL
    r46 slugs in the r48 bores with two ring grooves and a pin boss;
  * camshafts carry real egg-profile LOBES (base circle r16 + offset nose)
    per cylinder plus front drive flanges.
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
_THROW = (1, -1, -1, 1)          # flat-plane crank: 1-4 up, 2-3 down
_STROKE_HALF = 40.0
_ROD_LEN = 140.0
_CRANK_Z = 445.0


def _crankshaft():
    """Forged crank: nose, five mains, paired webs, four offset rod journals."""
    parts = [_cyl(28, 480, (390, 0, _CRANK_Z), (1, 0, 0))]          # main spine
    parts.append(_cyl(20, 36, (354, 0, _CRANK_Z), (1, 0, 0)))       # nose stub
    for px, s in zip(_PORT_X, _THROW):
        jz = _CRANK_Z + s * _STROKE_HALF
        # webs flanking the journal (r48 stays inside the r52 crank tunnel)
        for wx in (px - 29, px + 13):
            web = _cyl(48, 8, (wx, 0, _CRANK_Z), (1, 0, 0))
            # counterweight bias: trim the side opposite the throw
            web = web.cut(C.box(wx - 1, -50, _CRANK_Z + s * 18 + (0 if s > 0 else -68),
                                10, 100, 68))
            parts.append(web)
        parts.append(_cyl(24, 26, (px - 13, 0, jz), (1, 0, 0)))      # rod journal
    parts.append(_cyl(36, 12, (870, 0, _CRANK_Z), (1, 0, 0)))        # rear flange
    return _U(parts)


def _pistons_and_rods():
    """Vertical pistons with ring grooves + rods with BORED big ends riding
    their journals (r24.5 over r24 -- a bearing clearance, not a collision)."""
    parts = []
    for px, s in zip(_PORT_X, _THROW):
        jx = px - 13
        jz = _CRANK_Z + s * _STROKE_HALF
        pin_z = jz + _ROD_LEN
        # piston: r46 slug in the r48 bore, two ring grooves, dished crown
        piston = _cyl(46, 58, (px, 0, pin_z - 24), (0, 0, 1))
        for gz in (pin_z + 22, pin_z + 14):
            piston = piston.cut(
                _cyl(47.5, 3, (px, 0, gz), (0, 0, 1)).cut(
                    _cyl(43.5, 5, (px, 0, gz - 1), (0, 0, 1))))
        piston = piston.cut(_cyl(40, 4, (px, 0, pin_z + 31), (0, 0, 1)))
        pin = _cyl(11, 56, (px, -28, pin_z), (0, 1, 0))
        # connecting rod: big-end ring around the journal, I-beam shank, small end
        big_end = _cyl(31, 22, (jx + 2, 0, jz), (1, 0, 0)).cut(
            _cyl(24.5, 26, (jx, 0, jz), (1, 0, 0)))
        shank = C.swept_tube([(px - 11, 0, jz + 28), (px - 1, 0, pin_z - 12)], 9, cap=True)
        small_end = _cyl(16, 18, (px - 10, 0, pin_z), (1, 0, 0)).cut(
            _cyl(11.5, 22, (px - 12, 0, pin_z), (1, 0, 0)))
        rod_bolts = [_cyl(4, 14, (jx + 12, sy, jz - 26), (0, 0, 1)) for sy in (-16, 16)]
        parts.extend([piston, pin, big_end, shank, small_end] + rod_bolts)
    return _U(parts)


def _camshafts():
    """Twin cams with real egg-profile lobes (base r16 + offset nose) at each
    cylinder, journals between, and front drive flanges."""
    parts = []
    for cy in (-50, 50):
        parts.append(_cyl(13, 560, (400, cy, 728), (1, 0, 0)))            # spine
        for px in _PORT_X:
            base = _cyl(16, 14, (px - 7, cy, 728), (1, 0, 0))
            nose = _cyl(8, 14, (px - 7, cy, 728 + 9), (1, 0, 0))
            parts.append(base.fuse(nose))                                  # lobe
            parts.append(_cyl(16, 10, (px + 22, cy, 728), (1, 0, 0)))      # journal
        parts.append(_cyl(30, 10, (392, cy, 728), (1, 0, 0)))              # sprocket flange
        parts.append(_cyl(6, 8, (384, cy, 728), (1, 0, 0)))                # bolt boss
    return _U(parts)


def parts():
    out = []
    out.append((_crankshaft(),         METAL, "PRT_I4_Engine_Crankshaft"))
    out.append((_pistons_and_rods(),   METAL, "PRT_I4_Engine_Pistons_Rods"))
    out.append((_camshafts(),          METAL, "PRT_I4_Engine_Camshafts"))
    return out
