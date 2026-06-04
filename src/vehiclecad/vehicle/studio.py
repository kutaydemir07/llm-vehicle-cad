"""Physically-based 'studio' renderer for the SportsCar assembly.

Turns the flat-shaded primitive look into a product-style render: per-material
PBR (metallic car paint with clearcoat reflections, chrome, alloy, glass, rubber,
translucent lamp lenses), a procedural studio environment for reflections, soft
shadows on a ground plane, SSAA anti-aliasing, and crisp-edge-preserving shading
(so the ModelA's sharp panel edges stay sharp while curved surfaces shade smooth).

    from vehiclecad.vehicle.studio import render
    render(flat_parts, "out/fig.png", HERO_VIEWS)
"""
from __future__ import annotations
import numpy as np
import pyvista as pv
from vehiclecad.core.reference import common as C

# ---------------------------------------------------------------- materials
# (metallic, roughness, opacity, emissive_boost) keyed by exact part colour.
_MAT = {
    C.RED:     (0.55, 0.30, 1.0, 0.0),   # body paint w/ clearcoat
    C.CHROME:  (1.00, 0.07, 1.0, 0.0),   # bright chrome
    C.RIM:     (0.88, 0.22, 1.0, 0.0),   # polished alloy
    C.STEEL:   (0.80, 0.34, 1.0, 0.0),   # bare steel / reflector
    C.TIRE:    (0.00, 0.88, 1.0, 0.0),   # rubber
    C.BLACK:   (0.05, 0.55, 1.0, 0.0),   # satin black
    C.TRIM_BLK:(0.05, 0.62, 1.0, 0.0),   # textured plastic
    C.GLASS:   (0.00, 0.04, 0.16, 0.0),  # transparent tinted glass
    C.LIGHT:   (0.05, 0.10, 0.55, 0.25), # clear lens
    C.AMBER:   (0.10, 0.14, 0.70, 0.25), # amber lens
    C.TAILR:   (0.10, 0.14, 0.74, 0.18), # red lens
    C.TAILW:   (0.05, 0.12, 0.66, 0.30), # reverse/clear lens
    C.CALIPER: (0.25, 0.38, 1.0, 0.0),   # painted caliper
    C.STEEL:   (0.80, 0.34, 1.0, 0.0),
}


def _mat(rgb, name):
    if rgb in _MAT:
        return _MAT[rgb]
    n = name.lower()
    if "glass" in n or n in ("windshield", "backlight"):
        return (0.0, 0.04, 0.16, 0.0)
    if "lens" in n or "lamp" in n or "light" in n:
        return (0.05, 0.12, 0.6, 0.2)
    if "chrome" in n or "ring" in n or "exhaust" in n:
        return (1.0, 0.08, 1.0, 0.0)
    if "tire" in n or "rubber" in n:
        return (0.0, 0.88, 1.0, 0.0)
    if "rim" in n or "wheel" in n:
        return (0.88, 0.22, 1.0, 0.0)
    return (0.2, 0.5, 1.0, 0.0)


# ---------------------------------------------------------------- environment
def studio_environment(H=320, W=640):
    """Equirectangular studio: graduated dark->light, a bright overhead band and
    two softbox panels (the highlights that read as 'car paint')."""
    v = np.linspace(1.0, 0.0, H)[:, None]               # 1 at top
    u = np.linspace(0.0, 1.0, W)[None, :]
    img = np.empty((H, W, 3), np.float32)
    img[:] = (0.18 + 0.55 * v)[..., None]               # sky gradient
    img[v[:, 0] < 0.42] = 0.16                           # darker floor half
    # overhead soft band
    img += (1.1 * np.exp(-((v - 0.92) ** 2) / (2 * 0.012)))[..., None]
    # two large softboxes left/right-front
    for cu, amp in ((0.30, 1.5), (0.72, 1.2), (0.5, 0.6)):
        panel = np.exp(-((u - cu) ** 2) / (2 * 0.0016)) * \
                np.exp(-((v - 0.7) ** 2) / (2 * 0.02))
        img += (panel * amp)[..., None]
    img = np.clip(img, 0, 1) ** 0.85
    return pv.Texture((img * 255).astype(np.uint8))


# ---------------------------------------------------------------- mesh cache
def to_meshes(parts, lin=0.3, ang=0.2):
    out = []
    for shape, rgb, name in parts:
        try:
            v, f = shape.tessellate(lin, ang)
        except Exception:
            continue
        if not v or not f:
            continue
        pts = np.array([[p.x, p.y, p.z] for p in v])
        faces = np.hstack([[3, a, b, c] for a, b, c in f])
        out.append((pv.PolyData(pts, faces), rgb, name))
    return out


# ---------------------------------------------------------------- render
#  view = (title, view_vector, focus_or_None, zoom)
HERO = [("three-quarter front", (-1.0, 0.62, 0.30), None, 1.25),
        ("side", (0.0, 1.0, 0.04), None, 1.25),
        ("three-quarter rear", (1.0, 0.66, 0.32), None, 1.25),
        ("front", (-1.0, 0.05, 0.10), None, 1.25)]


def _one_view(meshes, env, vec, focus, zoom, window, ground, zmin):
    pl = pv.Plotter(off_screen=True, window_size=window, lighting="none")
    try:
        pl.set_environment_texture(env)
    except Exception:
        pass
    try:
        pl.enable_depth_peeling(number_of_peels=8, occlusion_ratio=0.0)
    except Exception:
        pass
    if ground:
        g = pv.Plane(center=(2180, 0, zmin - 1), direction=(0, 0, 1),
                     i_size=9000, j_size=6000)
        pl.add_mesh(g, color=(0.44, 0.45, 0.47), pbr=True, metallic=0.0,
                    roughness=0.55, ambient=0.30)
    for m, rgb, name in meshes:
        met, rough, opac, emis = _mat(rgb, name)
        color = tuple(min(1.0, c + emis) for c in rgb)
        pl.add_mesh(m, color=color, pbr=True, metallic=met, roughness=rough,
                    opacity=opac, smooth_shading=True, split_sharp_edges=True,
                    feature_angle=32, ambient=0.16, diffuse=0.85)
    for pos, inten, col in (((-3000, 3500, 6000), 0.9, "white"),
                            ((6000, -3500, 2500), 0.45, (0.85, 0.88, 1.0)),
                            ((7000, 1500, 1500), 0.4, "white")):
        L = pv.Light(position=pos, focal_point=(2180, 0, 500), intensity=inten, color=col)
        L.positional = False
        pl.add_light(L)
    pl.set_background("white")
    pl.view_vector(vec, viewup=(0, 0, 1))
    if focus is not None:
        pl.set_focus(focus)
    else:
        pl.reset_camera()
    pl.camera.zoom(zoom)
    pl.enable_anti_aliasing("ssaa")
    img = pl.screenshot(return_img=True)
    pl.close()
    return img


def render(parts, png, views=None, *, lin=0.3, ang=0.2, ground=True, window=(960, 640), offsets=None):
    """Render each view in its own plotter (robust off-screen) and tile to a grid."""
    import matplotlib.pyplot as plt
    views = views or HERO
    meshes = to_meshes(parts, lin, ang)
    if offsets:
        exploded = []
        for mesh, rgb, name in meshes:
            delta = offsets.get(name)
            if delta is not None:
                mesh = mesh.copy(deep=True)
                mesh.translate(delta, inplace=True)
            exploded.append((mesh, rgb, name))
        meshes = exploded
    zmin = np.vstack([m.points for m, _, _ in meshes])[:, 2].min()
    imgs = [_one_view(meshes, studio_environment(), vec, focus, zoom, window, ground, zmin)
            for (_t, vec, focus, zoom) in views]
    ncol = 2 if len(imgs) > 1 else 1
    nrow = (len(imgs) + ncol - 1) // ncol
    h, w, _ = imgs[0].shape
    canvas = np.full((h * nrow, w * ncol, 3), 255, np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, ncol)
        canvas[r*h:(r+1)*h, c*w:(c+1)*w] = im
    plt.imsave(str(png), canvas)
    print(f"PNG  -> {png}")


def parts():
    out = []
    out.extend(_mat())
    out.extend(_one_view())
    return out

