import cadquery as cq
from cadquery import Solid, Vector
import numpy as np
from math import cos, sin, radians

# Import station tables from materials (avoids circular if materials doesn't import geometry)
def _get_station_tables():
    from vehiclecad.core.reference import materials as _m
    return _m.BODY, _m.GREEN

def rrect_pts(a, z0, z1, rb, rt, n=7):
    """CHAMFERED rectangle cross-section (flat sheet-metal panel, not an arc).

    The section is a rectangle of half-width ``a`` from ``z0`` to ``z1`` whose
    four corners are cut by small FLAT chamfers (``rb`` bottom, ``rt`` top).
    Ruled-lofting these sections gives a body whose sides, roof, hood, deck and
    floor are genuinely PLANAR, meeting at crisp character-line creases -- a flat
    three-box, exactly the ModelA stamped-panel look, instead of a rounded tube.
    ``n`` is accepted for signature compatibility but unused (no arc to sample).
    """
    rb = max(float(rb), 0.5)
    rt = max(float(rt), 0.5)
    rb = min(rb, 0.45 * (z1 - z0), 0.45 * a)
    rt = min(rt, 0.45 * (z1 - z0), 0.45 * a)
    # counter-clockwise, 8 vertices: up the right side, across the top, down the
    # left side, across the bottom -- each corner a single flat chamfer segment.
    return [
        ( a,         z0 + rb),
        ( a,         z1 - rt),
        ( a - rt,    z1),
        (-(a - rt),  z1),
        (-a,         z1 - rt),
        (-a,         z0 + rb),
        (-(a - rb),  z0),
        ( a - rb,    z0),
    ]

def loft(stations, ruled=True):
    """Ruled (flat-faceted) loft through chamfered-rectangle stations by default.

    ``ruled=True`` connects corresponding section vertices with straight ruled
    surfaces, so every panel between two stations is planar -- the flat-box look.
    """
    wires = []
    for x, a, z0, z1, rb, rt in stations:
        p = [Vector(x, y, z) for y, z in rrect_pts(a, z0, z1, rb, rt)]
        wires.append(cq.Wire.makePolygon(p + [p[0]]))
    return Solid.makeLoft(wires, ruled)

def box(x0, y0, z0, dx, dy, dz):
    return Solid.makeBox(dx, dy, dz, Vector(x0, y0, z0))

def cyl(r, h, base, d):
    return Solid.makeCylinder(r, h, Vector(*base), Vector(*d))

def rbox(x0, y0, z0, dx, dy, dz, r):
    """Box with all edges filleted (rounded) -> non-blocky detail parts."""
    s = box(x0, y0, z0, dx, dy, dz)
    r = min(r, 0.49*min(dx, dy, dz))
    try:
        return cq.Workplane(obj=s).edges().fillet(r).val()
    except Exception:
        return s

def fillet_edges(s, r):
    try:
        return cq.Workplane(obj=s).edges().fillet(r).val()
    except Exception:
        return s

def fillet_where(s, r, selector):
    try:
        return cq.Workplane(obj=s).edges(selector).fillet(r).val()
    except Exception:
        return s

def xz_prism(poly, y0, y1):
    p = [Vector(x, y0, z) for x, z in poly]
    face = cq.Face.makeFromWires(cq.Wire.makePolygon(p + [p[0]]))
    return Solid.extrudeLinear(face, Vector(0, y1 - y0, 0))

def U(shapes):
    s = shapes[0]
    for x in shapes[1:]:
        s = s.fuse(x)
    return s

def mirror_y(s):
    """Reflect a solid across the car centreline (Y -> -Y)."""
    return s.mirror("XZ")

# ---------------------------------------------------------------- engineering helpers

def swept_tube(path_pts, radius, cap=True):
    """Sweep a circular cross-section along a polyline path.

    ``path_pts`` is a list of (x, y, z) tuples.  Returns a Solid built by
    lofting circles at each waypoint (with optional hemispherical end-caps
    approximated as short cones).  This is used for exhaust tubes, roll-cage
    bars, anti-roll bars, driveshafts, tie-rods, etc.
    """
    if len(path_pts) < 2:
        raise ValueError("swept_tube needs  -  2 path points")
    # Simple approach: chain cylinders between consecutive points and fuse them.
    # For short segment counts this is fast and robust.
    segments = []
    for i in range(len(path_pts) - 1):
        p0 = np.array(path_pts[i])
        p1 = np.array(path_pts[i + 1])
        d = p1 - p0
        length = float(np.linalg.norm(d))
        if length < 0.1:
            continue
        direction = d / length
        segments.append(cyl(radius, length, tuple(p0), tuple(direction)))
    if not segments:
        return cyl(radius, 1, path_pts[0], (0, 0, 1))
    result = segments[0]
    for seg in segments[1:]:
        result = result.fuse(seg)
    # cap the joints with spheres for smooth transitions
    if cap and len(path_pts) > 2:
        for pt in path_pts[1:-1]:
            sph = Solid.makeSphere(radius * 1.02, Vector(*pt))
            result = result.fuse(sph)
    return result


def thick_plate(x0, y0, z, dx, dy, thickness):
    """A flat rectangular plate in the XY plane at height z, with given thickness.
    Used for floorpan sections, firewall segments, bracket plates, etc."""
    return box(x0, y0, z, dx, dy, thickness)


def shell_box(x0, y0, z0, dx, dy, dz, wall):
    """A hollow box (6-sided shell)  -  used for structural sections, engine
    envelope shells, and other packaging volumes."""
    outer = box(x0, y0, z0, dx, dy, dz)
    inner = box(x0 + wall, y0 + wall, z0 + wall,
                dx - 2 * wall, dy - 2 * wall, dz - 2 * wall)
    if dx <= 2 * wall or dy <= 2 * wall or dz <= 2 * wall:
        return outer
    return outer.cut(inner)


def coil_spring(z0, z1, coil_r, wire_r, active_turns, end_turns=0.85, seg=30):
    """A REAL coil spring: one continuous helical wire swept as a single solid.

    Built straight up the local +Z axis from ``z0`` to ``z1`` (use
    ``mating.place_along`` to drop it onto a leaning strut axis).  The wire is a
    circle of radius ``wire_r`` swept along a helix of mean radius ``coil_r``.
    The end coils are pitch-eased (``end_turns`` of nearly-flat "ground" coil at
    each end) so the spring seats FLAT on its perches instead of ending on a
    diagonal -- the production look of a closed-and-ground compression spring.

    Replaces the old stacked-torus approximation (disconnected rings).  ``z1`` is
    the seat-to-seat span; the swept wire's outer surface reaches ~``wire_r``
    beyond ``z0``/``z1`` exactly as a real spring's end wire does.
    """
    H = float(z1 - z0)
    if H <= 4 * wire_r:                       # degenerate: fall back to a stub
        return cyl(coil_r, max(H, 1.0), (coil_r, 0, z0), (0, 0, 1))
    total_turns = float(active_turns) + 2.0 * end_turns
    n = max(8, int(seg * total_turns))
    ts = np.linspace(0.0, total_turns, n)             # turn index along the wire
    rise = np.ones(n)                                 # relative pitch per turn
    rise[ts < end_turns] = 0.16                       # flattened bottom ground coils
    rise[ts > total_turns - end_turns] = 0.16         # flattened top ground coils
    dz = np.diff(ts) * rise[1:]
    z = np.concatenate([[0.0], np.cumsum(dz)])
    z = z0 + z * (H / z[-1])                           # normalise to span exactly H
    ang = 2.0 * np.pi * ts
    pts = [Vector(float(coil_r * np.cos(a)), float(coil_r * np.sin(a)), float(zz))
           for a, zz in zip(ang, z)]
    path = cq.Workplane(obj=cq.Edge.makeSpline(pts))
    prof = cq.Workplane("XZ").center(coil_r, z0).circle(wire_r)
    try:
        return prof.sweep(path, isFrenet=True).val()
    except Exception:
        # robust fallback: chain short cylinders along the helix points
        return swept_tube([(p.x, p.y, p.z) for p in pts], wire_r, cap=False)


def helix_coil(centre, radius, pitch, n_turns, wire_r, axis=(0, 0, 1)):
    """Backwards-compatible shim -> now a REAL swept helix (see ``coil_spring``).

    Kept so older call-sites keep working, but it no longer emits a stack of
    loose tori.  ``centre`` is the local base; the helix climbs ``axis`` for
    ``pitch * n_turns``.  Only the +Z axis is supported for the eased-end build;
    other axes route through the legacy torus stack for safety.
    """
    cx, cy, cz = centre
    ax = np.array(axis, dtype=float)
    ax = ax / (np.linalg.norm(ax) or 1.0)
    if abs(ax[2]) > 0.999 and cx == 0 and cy == 0:
        spring = coil_spring(cz, cz + pitch * n_turns, radius, wire_r,
                             active_turns=max(1.0, n_turns - 1.5))
        return spring if ax[2] > 0 else spring.mirror("XY")
    # legacy fallback for off-axis callers
    coils = []
    for i in range(int(n_turns)):
        offset = ax * (pitch * (i + 0.5))
        pos = Vector(cx + offset[0], cy + offset[1], cz + offset[2])
        coils.append(Solid.makeTorus(radius, wire_r, pos, Vector(*ax)))
    if not coils:
        return cyl(radius, pitch, centre, axis)
    result = coils[0]
    for c in coils[1:]:
        result = result.fuse(c)
    return result


def tapered_box(x0, y0, z0, dx, dy_base, dy_top, dz):
    """A box that tapers in width (Y) from base to top.  Used for trailing arms,
    control arms, and other forged structural shapes."""
    # build as a loft between two rectangular cross-sections
    hw_b = dy_base / 2.0
    hw_t = dy_top / 2.0
    poly_b = [(x0, y0 - hw_b, z0), (x0 + dx, y0 - hw_b, z0),
              (x0 + dx, y0 + hw_b, z0), (x0, y0 + hw_b, z0)]
    poly_t = [(x0, y0 - hw_t, z0 + dz), (x0 + dx, y0 - hw_t, z0 + dz),
              (x0 + dx, y0 + hw_t, z0 + dz), (x0, y0 + hw_t, z0 + dz)]
    w_b = cq.Wire.makePolygon([Vector(*p) for p in poly_b] + [Vector(*poly_b[0])])
    w_t = cq.Wire.makePolygon([Vector(*p) for p in poly_t] + [Vector(*poly_t[0])])
    return Solid.makeLoft([w_b, w_t], True)


# ---------------------------------------------------------------- complex tubes & surfaces
#  The helpers below build genuinely curved/skinned solids (not box-and-cylinder
#  approximations) so detail parts read as real castings, pipes and trumpets.

def loft_circles(rings, ruled=False):
    """Loft ONE continuous solid through a sequence of circular sections.

    ``rings`` is a list of ``(center, radius, normal)`` tuples.  Unlike fusing
    discrete cylinders, the radius AND direction may vary section-to-section, so
    this is the basis for velocity-stack trumpets, tapered exhaust collectors,
    grooved pulleys and smoothly bent tubes.
    """
    if len(rings) < 2:
        c, r, n = rings[0]
        return cyl(r, 1.0, c, n)
    wires = [cq.Wire.makeCircle(float(r), Vector(*c), Vector(*n)) for c, r, n in rings]
    return Solid.makeLoft(wires, ruled)


def tube_path(path_pts, radius):
    """A smooth circular tube swept along a polyline.

    A circle is oriented to the local tangent at every vertex and the circles are
    lofted, giving a continuous bent pipe with no faceting at the joints.
    ``radius`` may be a scalar or a per-vertex list, which lets a run taper  -  e.g.
    a 4-into-1 exhaust collector or a megaphone.  Falls back to fused cylinders
    if the loft is degenerate, so a tight bend never crashes the build.
    """
    pts = [np.array(p, dtype=float) for p in path_pts]
    if len(pts) < 2:
        raise ValueError("tube_path needs >= 2 points")
    if isinstance(radius, (int, float)):
        radii = [float(radius)] * len(pts)
    else:
        radii = [float(r) for r in radius]
    tangents = []
    for i in range(len(pts)):
        if i == 0:
            t = pts[1] - pts[0]
        elif i == len(pts) - 1:
            t = pts[-1] - pts[-2]
        else:
            t = pts[i + 1] - pts[i - 1]
        nrm = np.linalg.norm(t)
        tangents.append(t / nrm if nrm > 1e-9 else np.array([0.0, 0.0, 1.0]))
    rings = [(tuple(pts[i]), radii[i], tuple(tangents[i])) for i in range(len(pts))]
    try:
        return loft_circles(rings)
    except Exception:
        return swept_tube([tuple(p) for p in pts], float(np.mean(radii)))


def bellmouth(throat_center, axis, r_throat, r_mouth, length, n=7):
    """Flared velocity-stack / trumpet: a horn whose radius grows from
    ``r_throat`` to ``r_mouth`` over ``length`` along ``axis`` with a radiused
    (ease-out) flare, finished with a rolled lip at the mouth.  This is the
    defining visual of the I4_Engine's individual-throttle-body intake."""
    ax = np.array(axis, dtype=float)
    ax = ax / (np.linalg.norm(ax) or 1.0)
    base = np.array(throat_center, dtype=float)
    rings = []
    for i in range(n + 1):
        f = i / n
        r = r_throat + (r_mouth - r_throat) * (f ** 1.8)   # ease-out flare
        rings.append((tuple(base + ax * (length * f)), float(r), tuple(ax)))
    horn = loft_circles(rings)
    try:
        lip = Solid.makeTorus(r_mouth, max(2.0, (r_mouth - r_throat) * 0.12),
                              Vector(*(base + ax * length)), Vector(*ax))
        return horn.fuse(lip)
    except Exception:
        return horn


ROUNDEL_BLUE  = (0.07, 0.27, 0.62)
ROUNDEL_WHITE = (0.93, 0.94, 0.96)
CHROME        = (0.80, 0.81, 0.83)
BLACK         = (0.06, 0.06, 0.06)

# additional colours for engineering sub-assemblies
STRUCT  = (0.35, 0.37, 0.40)     # structural steel (chassis)
ENGINE  = (0.28, 0.30, 0.34)     # engine block grey
ALLOY_E = (0.52, 0.54, 0.56)     # alloy / aluminium (intake, covers)
EXHAUST_C = (0.46, 0.40, 0.32)   # exhaust header patina
TRANS   = (0.22, 0.23, 0.26)     # transmission housing
RUBBER  = (0.08, 0.08, 0.09)     # bushings, mounts
SPRING  = (0.15, 0.42, 0.18)     # coil springs (Classic green-ish)
DAMPER  = (0.20, 0.21, 0.24)     # shock absorber body
ARM     = (0.32, 0.34, 0.38)     # control arms, trailing arms


def roundel(center, normal, r=34.0):
    """Generic roundel as real solids: chrome outer ring, black band,
    and an inner disc split into a top half and bottom half to be copyright free.
    `normal` in {'+x','-x','+y','-y'} is the outward face direction. Returns [(solid, rgb, name), ...]."""
    big = 500.0
    disc = cyl(r*0.80, 9, (-5, 0, 0), (1, 0, 0))           # canonical: faces -x

    # half circle blue and half white instead of diagonal
    white = disc.intersect(box(-50, -big, 0, 100, 2*big, big))
    blue = disc.intersect(box(-50, -big, -big, 100, 2*big, big))

    band = cyl(r*0.93, 8, (-4, 0, 0), (1, 0, 0)).cut(cyl(r*0.80, 14, (-7, 0, 0), (1, 0, 0)))
    ring = cyl(r, 9, (-5, 0, 0), (1, 0, 0)).cut(cyl(r*0.93, 15, (-8, 0, 0), (1, 0, 0)))
    canon = [(white, ROUNDEL_WHITE, "roundel_white"), (blue, ROUNDEL_BLUE, "roundel_blue"),
             (band, BLACK, "roundel_band"), (ring, CHROME, "roundel_ring")]
    ang = {"-x": 0.0, "+x": 180.0, "+y": -90.0, "-y": 90.0}[normal]
    out = []
    for s, rgb, nm in canon:
        out.append((s.rotate((0, 0, 0), (0, 0, 1), ang).translate(center), rgb, nm))
    return out

# ---- greenhouse + window cutters (shared by body shell and glazing) ----
def greenhouse_solid():
    """The cabin glass-house as ONE crisp solid (ruled loft -> planar facets, not
    an organic dome).  Sits on the flat beltline so it stacks on the lower body."""
    _, GREEN = _get_station_tables()
    return loft(GREEN, ruled=True)

def greenhouse_skin():
    """A thin (~6 mm) outer skin of the cabin surface.  Glazing panes are carved
    from this so each pane lies flush on the cabin and exactly fills its DLO."""
    from vehiclecad.core.reference import materials as _m
    return loft(_m.GREEN, ruled=True).cut(loft(_m.GREEN_SKIN, ruled=True))

# The Daylight-Opening (DLO) apertures.  Each is a slab swept across the cabin;
# intersected with the cabin surface it yields a pane, and subtracted from the
# shell it opens the matching hole, so glass and hole are exact complements.
#   * windshield / backlight: rake slabs, |y| inboard of the side cutters so the
#     A / B / C-pillars (the uncut bands) survive.
#   * door / quarter side glass: |y| straddling the cabin side surface (~770 mm).
# The side-view profiles are defined ONCE here (matched to the GREEN roofline) and
# used by BOTH window_cutters() and glass_panes(), so the hole and its pane can
# never drift apart.  DLO bottom sits at z~1030 (a ~14 mm beltline band survives);
# tops run ~14-26 mm under the roof rail so the gutter/roof band survives.
_WS_POLY   = [(1500, 1020), (1600, 1020), (1795, 1366), (1695, 1366)]   # windshield
_BL_POLY   = [(2740, 1358), (2842, 1358), (3242, 1052), (3140, 1052)]   # backlight
_DOOR_POLY = [(1850, 1030), (2440, 1030), (2440, 1352), (1905, 1346)]   # door glass
_QTR_POLY  = [(2540, 1030), (2720, 1030), (2702, 1308), (2548, 1336)]   # quarter glass
_WS_Y, _BL_Y = 652.0, 664.0           # windshield/backlight |y| (inboard of pillars)
_SIDE_YLO, _SIDE_YHI = 690.0, 824.0   # side-glass |y| straddle across the cabin wall

def _windshield_cut():
    return xz_prism(_WS_POLY, -_WS_Y, _WS_Y)

def _backlight_cut():
    return xz_prism(_BL_POLY, -_BL_Y, _BL_Y)

def _side_cuts():
    out = []
    for s in (1, -1):
        ylo, yhi = sorted((s * _SIDE_YLO, s * _SIDE_YHI))
        out.append(xz_prism(_DOOR_POLY, ylo, yhi))   # door glass
        out.append(xz_prism(_QTR_POLY, ylo, yhi))    # quarter glass
    return out

def window_cutters():
    return U([_windshield_cut(), _backlight_cut()] + _side_cuts())

def glass_panes():
    """Return [(solid, name), ...] -- one flush pane per DLO, carved from the
    cabin skin so it sits on the surface and fills its hole exactly."""
    skin = greenhouse_skin()
    named = [(_windshield_cut(), "windshield"), (_backlight_cut(), "backlight")]
    for s in (1, -1):
        sd = "L" if s > 0 else "R"
        ylo, yhi = sorted((s * _SIDE_YLO, s * _SIDE_YHI))
        named.append((xz_prism(_DOOR_POLY, ylo, yhi), f"door_glass_{sd}"))
        named.append((xz_prism(_QTR_POLY, ylo, yhi), f"quarter_glass_{sd}"))
    out = []
    for cutter, name in named:
        pane = skin.intersect(cutter)
        if pane.Volume() > 1.0:
            out.append((pane, name))
    return out

