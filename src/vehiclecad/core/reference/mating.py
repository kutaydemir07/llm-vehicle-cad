"""Mate-based assembly layer for cq.Assembly - locate parts by SEATING them on
each other's faces, not by hardcoded coordinates.

The rest of this project places every solid at an absolute coordinate, so any
part whose numbers are slightly off floats or interpenetrates.  This module is
the missing constraint layer: build each part in its OWN local frame, tag its
mating faces ("mate connectors"), add them to a cq.Assembly, then join them with
these helpers.  ``cq.Assembly.solve()`` then derives every position from the
mates - parts CANNOT float or collide because their placement is computed.

Recipe (verified on cadquery 2.6.1):
    Plane  -> two tagged faces become coincident, normals opposed  (seats flat)
    Point  -> the faces' centroids coincide                        (centers/concentric)
Together they fully locate a turned part onto another: "bolt this disc flat and
concentric onto that flange."
"""
from __future__ import annotations
import cadquery as cq
import numpy as np


def tag(part: cq.Workplane, **faces: str) -> cq.Workplane:
    """Tag named mate faces on a part: ``tag(wp, deck='>Z', foot='<Z')``.

    Returns the same Workplane so calls can be chained.  Reference the tag later
    as ``'<part_name>+<tag>'`` in a constraint.
    """
    for name, selector in faces.items():
        part.faces(selector).tag(name)
    return part


def _ref(r: str) -> str:
    """Normalise a mate reference to CadQuery's grammar.

    This project writes tagged-face references as ``'part+tag'`` (a readable
    convention), but ``cq.Assembly.constrain`` only accepts ``'part?tag'`` -- a
    ``+`` makes its pyparsing grammar raise ``ParseException`` and the whole solve
    aborts.  Translating here lets every caller keep the ``+`` spelling while the
    solver receives valid ``?`` references.
    """
    return r.replace("+", "?", 1) if "+" in r else r


def seat(assy: cq.Assembly, base_ref: str, top_ref: str, center: bool = True) -> cq.Assembly:
    """Seat ``top_ref`` flat onto ``base_ref`` (refs like ``'hub+deck'``).

    The two faces become coincident; with ``center=True`` the parts are also made
    concentric (the classic flush + centered bolt-up).
    """
    base_ref, top_ref = _ref(base_ref), _ref(top_ref)
    assy.constrain(base_ref, top_ref, "Plane")
    if center:
        assy.constrain(base_ref, top_ref, "Point")
    return assy


def coaxial(assy: cq.Assembly, ref_a: str, ref_b: str) -> cq.Assembly:
    """Align two parts' axes (refs to cylindrical faces) without seating."""
    assy.constrain(_ref(ref_a), _ref(ref_b), "Axis")
    return assy


def fix(assy: cq.Assembly, name: str) -> cq.Assembly:
    """Ground a part so the solver positions everything else relative to it."""
    assy.constrain(name, "Fixed")
    return assy


def build(parts: dict, mates: list, grounded: str,
          colors: dict | None = None, scatter: bool = True) -> cq.Assembly:
    """Assemble and solve.

    parts    : ``name -> Workplane`` (each with tagged mate faces)
    mates    : list of ``(base_ref, top_ref)`` seats, or ``(a, b, kind)`` for a
               raw constraint kind ('Axis', 'Plane', 'Point').
    grounded : name of the fixed part.
    scatter  : start the non-grounded parts at offset 'floating' positions so the
               solve provably does the locating (nothing is pre-placed by hand).
    """
    a = cq.Assembly()
    for i, (name, wp) in enumerate(parts.items()):
        loc = cq.Location(cq.Vector(230 * (i + 1), 140 * (-1) ** i, 80 * i)) \
            if (scatter and name != grounded) else cq.Location()
        kw = {}
        if colors and name in colors:
            kw["color"] = cq.Color(*colors[name])
        a.add(wp, name=name, loc=loc, **kw)
    fix(a, grounded)
    for m in mates:
        if len(m) == 2:
            seat(a, m[0], m[1])
        else:
            a.constrain(_ref(m[0]), _ref(m[1]), m[2])
    a.solve()
    return a


def to_flat(assy: cq.Assembly, colors: dict | None = None,
            default=(0.6, 0.61, 0.64)) -> list:
    """Flatten a solved one-level assembly to ``[(solid, rgb, name), ...]`` for
    the project's pyvista/STEP exporters."""
    out = []
    for ch in assy.children:
        shp = ch.obj.val().moved(ch.loc)
        rgb = (colors or {}).get(ch.name, default)
        out.append((shp, rgb, ch.name))
    return out


def place_along(flat, p_lo, p_up):
    """Rigidly move a Z-axis-built local assembly so local +Z maps onto the
    segment ``p_lo -> p_up`` and the base sits at ``p_lo``.

    Cartridges (strut, damper, spring) are easiest to mate-solve built straight
    up the Z axis; this drops the solved result onto its real (leaning) axis
    between two hardpoints.  ``flat`` is a ``[(solid, rgb, name), ...]`` list.
    """
    p_lo = np.array(p_lo, float)
    p_up = np.array(p_up, float)
    d = p_up - p_lo
    dirv = d / float(np.linalg.norm(d))
    z = np.array([0.0, 0.0, 1.0])
    axis = np.cross(z, dirv)
    s = float(np.linalg.norm(axis))
    ang = float(np.degrees(np.arctan2(s, float(np.dot(z, dirv)))))
    out = []
    for solid, color, name in flat:
        sp = solid
        if s > 1e-9:
            a = axis / s
            sp = sp.rotate((0, 0, 0), (float(a[0]), float(a[1]), float(a[2])), ang)
        sp = sp.translate((float(p_lo[0]), float(p_lo[1]), float(p_lo[2])))
        out.append((sp, color, name))
    return out


def seat_on_points(flat, local_pts, target_pts):
    """Locate a rigid part by SOLVING its pose from joint connections.

    Computes the rigid transform (rotation + translation, least-squares / Umeyama)
    that best maps the part's ``local_pts`` onto the ``target_pts`` hardpoints,
    then applies it.  This is the 3-point generalisation of ``place_along``: e.g.
    a steering knuckle located by its lower ball-joint, strut clamp and tie-rod
    points instead of a hardcoded translate, so it follows the hardpoints.
    """
    P = np.array(local_pts, float)
    Q = np.array(target_pts, float)
    cP = P.mean(0)
    cQ = Q.mean(0)
    H = (P - cP).T @ (Q - cQ)
    U, _, Vt = np.linalg.svd(H)
    d = 1.0 if np.linalg.det(Vt.T @ U.T) >= 0 else -1.0
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    t = cQ - R @ cP
    cos = max(-1.0, min(1.0, (np.trace(R) - 1.0) / 2.0))
    ang = float(np.degrees(np.arccos(cos)))
    out = []
    for solid, color, name in flat:
        sp = solid
        if ang > 1e-6:
            ax = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
            n = float(np.linalg.norm(ax))
            if n > 1e-9:
                ax = ax / n
                sp = sp.rotate((0, 0, 0), (float(ax[0]), float(ax[1]), float(ax[2])), ang)
        sp = sp.translate((float(t[0]), float(t[1]), float(t[2])))
        out.append((sp, color, name))
    return out
