#!/usr/bin/env python3
"""
make_assembly_gif.py  --  Classic SportsCar ModelA top-down assembly animation (REAL geometry).
================================================================================
This renders the *actual* tessellated CadQuery B-rep solids -- not bounding-box
cubes -- as they assemble from the master skeleton outward, following the
top-down build order defined in ``vehiclecad.core.reference.fitment.ASSEMBLY_SEQUENCE``:

    Master datums -> Chassis BiW -> Suspension -> Brakes -> Wheels ->
    Powertrain -> Driveline -> Electrical/HVAC -> Interior -> Body & closures
    -> Aero surfaces

Each functional group flies (and rotates) into place from an exploded offset
that mirrors how the real system installs -- engine craned from above, wheels
rolled in from the sides, driveline fed up from below -- then the finished car
spins through a full 360 deg orbit.

Technique
---------
Every solid is tessellated **once** into a pyvista mesh; per frame we only push
a 4x4 transform onto each actor (cheap), so ~190k triangles animate smoothly.

Usage
-----
  python make_assembly_gif.py                  # full quality
  python make_assembly_gif.py --fast           # quick preview (fewer frames)
  python make_assembly_gif.py --output path.gif
  python make_assembly_gif.py --size 1100 700  # window WxH
"""
from __future__ import annotations

import argparse
import math
import os
import sys
import time
from dataclasses import dataclass, field

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pyvista as pv  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from vehiclecad.vehicle import detailed_complete_vehicle as assembly  # noqa: E402
from vehiclecad.core.reference.fitment import ASSEMBLY_SEQUENCE  # noqa: E402
from vehiclecad.vehicle.studio import _mat, studio_environment  # noqa: E402

pv.OFF_SCREEN = True

#  -  -  output / look  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
DEFAULT_OUT = "assembly_animation.gif"
BG_BOTTOM = "#ffffff"
BG_TOP = "#ffffff"
FRAME_MS = 70                     # GIF frame delay
EXPLODE_SCALE = 1.9               # how far parts start from their final home
TESS_TOL = 0.5                    # mm, surface deviation for tessellation
TESS_ANG = 0.15                   # rad, angular deviation

#  -  -  per-stage installation motion  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
# label -> (explode-direction override or None to use fitment fly-vector,
#           rotation axis, settle angle deg, "lateral" => mirror Y by part side)
@dataclass
class Move:
    rot_axis: tuple = (1.0, 0.0, 0.0)
    rot_deg: float = 14.0
    lateral: bool = False
    spin: bool = False            # full rolling spin (wheels)


MOVES = {
    "Master Datums":   Move(rot_deg=0.0),
    "Chassis BIW":     Move(rot_axis=(0, 1, 0), rot_deg=10.0),
    "Suspension":      Move(rot_axis=(1, 0, 0), rot_deg=18.0, lateral=True),
    "Brakes":          Move(rot_axis=(0, 0, 1), rot_deg=24.0, lateral=True),
    "Wheels":          Move(rot_axis=(0, 1, 0), rot_deg=120.0, lateral=True, spin=True),
    "Powertrain":      Move(rot_axis=(0, 1, 0), rot_deg=12.0),
    "Driveline":       Move(rot_axis=(0, 1, 0), rot_deg=16.0),
    "Electrical HVAC": Move(rot_axis=(0, 0, 1), rot_deg=20.0, lateral=True),
    "Interior":        Move(rot_axis=(1, 0, 0), rot_deg=12.0),
    "Body Closures":   Move(rot_axis=(0, 1, 0), rot_deg=10.0, lateral=True),
    "Aero Surfaces":   Move(rot_axis=(0, 1, 0), rot_deg=16.0),
}


def _is_glass(name: str) -> bool:
    n = name.lower()
    return "glass" in n or "windshield" in n or "backlight" in n


#  -  -  part record  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
@dataclass
class P:
    actor: object
    centroid: np.ndarray
    explode: np.ndarray            # offset applied at progress 0
    rot_axis: np.ndarray
    rot_deg: float
    stage: int
    name: str


def _rot_matrix(axis: np.ndarray, deg: float) -> np.ndarray:
    """4x4 rotation about an axis through the origin (Rodrigues)."""
    a = axis / (np.linalg.norm(axis) + 1e-9)
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    x, y, z = a
    R = np.array([
        [c + x * x * (1 - c),     x * y * (1 - c) - z * s, x * z * (1 - c) + y * s],
        [y * x * (1 - c) + z * s, c + y * y * (1 - c),     y * z * (1 - c) - x * s],
        [z * x * (1 - c) - y * s, z * y * (1 - c) + x * s, c + z * z * (1 - c)],
    ])
    M = np.eye(4)
    M[:3, :3] = R
    return M


def _T(vec) -> np.ndarray:
    M = np.eye(4)
    M[:3, 3] = vec
    return M


def part_matrix(p: P, progress: float) -> np.ndarray:
    """Transform for a part at animation progress in [0, 1] (1 = home)."""
    e = 1.0 - (1.0 - progress) ** 3          # ease-out cubic
    offset = p.explode * (1.0 - e)
    angle = p.rot_deg * (1.0 - e)
    # rotate about the part's own centroid, then translate by the explode offset
    R = _rot_matrix(p.rot_axis, angle)
    M = _T(offset) @ _T(p.centroid) @ R @ _T(-p.centroid)
    return M


#  -  -  scene construction  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
def build_scene(pl: pv.Plotter):
    """Tessellate every solid once, add it as an actor, and return part records
    plus the list of stage labels in build order."""
    subs = assembly.subassemblies()

    # datums (skeleton markers) as stage 0 if the sequence opens with them
    skeleton = []
    try:
        skeleton = assembly._skeleton_marker()
    except Exception:
        pass

    parts: list[P] = []
    labels: list[str] = []
    t0 = time.time()
    ntri = 0
    glo = np.array([np.inf, np.inf, np.inf])
    ghi = np.array([-np.inf, -np.inf, -np.inf])

    for stage_idx, (label, keys, color, flyvec) in enumerate(ASSEMBLY_SEQUENCE):
        labels.append(label)
        mv = MOVES.get(label, Move())

        # gather this stage's (solid, rgb, name) tuples
        raw = []
        if not keys:                                   # datums stage
            raw = list(skeleton)
        else:
            for k in keys:
                raw.extend(subs.get(k, []))

        for solid, rgb, name in raw:
            try:
                v, f = solid.tessellate(TESS_TOL, TESS_ANG)
            except Exception:
                continue
            if not v or not f:
                continue
            pts = np.array([[q.x, q.y, q.z] for q in v], dtype=float)
            faces = np.hstack([[3, a, b, c] for a, b, c in f])
            mesh = pv.PolyData(pts, faces)
            ntri += len(f)
            centroid = pts.mean(axis=0)
            glo = np.minimum(glo, pts.min(axis=0))
            ghi = np.maximum(ghi, pts.max(axis=0))

            met, rough, opac, emis = _mat(rgb, name)
            color = tuple(min(1.0, c + emis) for c in rgb)
            actor = pl.add_mesh(
                mesh, color=color, pbr=True, metallic=met, roughness=rough,
                opacity=opac, smooth_shading=True, split_sharp_edges=True,
                feature_angle=32, ambient=0.16, diffuse=0.85
            )

            # explode offset: fitment fly-vector, mirrored by side for lateral stages
            fx, fy, fz = flyvec
            if mv.lateral and abs(fy) > 1 and abs(centroid[1]) > 40:
                fy = math.copysign(abs(fy), centroid[1])
            explode = np.array([fx, fy, fz], dtype=float) * EXPLODE_SCALE

            # wheels: add a big lateral pull so they roll in from outside the arches
            if mv.spin:
                explode[1] = math.copysign(950.0, centroid[1]) * EXPLODE_SCALE * 0.6

            parts.append(P(
                actor=actor, centroid=centroid, explode=explode,
                rot_axis=np.array(mv.rot_axis, dtype=float), rot_deg=mv.rot_deg,
                stage=stage_idx, name=name,
            ))

    print(f"  tessellated {len(parts)} parts / {ntri} triangles "
          f"in {time.time() - t0:.1f}s")
    return parts, labels, glo, ghi


#  -  -  camera  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
def set_camera(pl: pv.Plotter, focal, radius, az_deg, elev_deg):
    az, el = math.radians(az_deg), math.radians(elev_deg)
    pos = (
        focal[0] + radius * math.cos(el) * math.cos(az),
        focal[1] + radius * math.cos(el) * math.sin(az),
        focal[2] + radius * math.sin(el),
    )
    pl.camera.position = pos
    pl.camera.focal_point = tuple(focal)
    pl.camera.up = (0, 0, 1)
    pl.camera.view_angle = 30.0
    # Set an explicit near/far clip range wide enough to bracket the whole scene.
    # (reset_camera_clipping_range() keys off the *currently visible* actors, so an
    # early datums-only frame would lock a razor-thin clip shell and hide the car.)
    pl.camera.clipping_range = (radius * 0.15, radius * 3.0)


#  -  -  overlay (title / checklist / footer) drawn with PIL  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
def _font(size, bold=False):
    paths = ([r"C:\Windows\Fonts\arialbd.ttf"] if bold else []) + \
            [r"C:\Windows\Fonts\arial.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


@dataclass
class Fonts:
    title: object = field(default_factory=lambda: _font(45, bold=True))
    sub: object = field(default_factory=lambda: _font(22))
    item: object = field(default_factory=lambda: _font(24, bold=True))
    small: object = field(default_factory=lambda: _font(18))


def overlay(img: Image.Image, fonts: Fonts, labels, done_idx, active_idx,
            footer: str):
    d = ImageDraw.Draw(img, "RGBA")
    W, H = img.size

    # title block
    d.text((26, 20), "Classic  SportsCar  ModelA", font=fonts.title, fill=(0, 0, 0))
    d.text((28, 75), "Top-down CAD assembly  -  Inline-4 2.3L  -  Touring Car",
            font=fonts.sub, fill=(80, 80, 80))
    d.text((28, 105), "CAD by Opus 4.8 and GPT 5.5", font=fonts.sub, fill=(100, 100, 100))

    # stage checklist (top-right)
    x = W - 26
    y = 22
    for i, lab in enumerate(labels):
        if i < done_idx:
            mark, col = "v ", (0, 120, 0, 255)
        elif i == active_idx:
            mark, col = "> ", (0, 80, 200, 255)
        else:
            mark, col = "  ", (150, 150, 150, 255)
        txt = mark + lab
        w = d.textlength(txt, font=fonts.item)
        d.text((x - w, y + i * 35), txt, font=fonts.item, fill=col)

    # progress bar + footer (bottom)
    n = len(labels)
    frac = min(done_idx + (1 if active_idx >= 0 else 0), n) / n
    bx0, by0, bx1 = 28, H - 34, W - 28
    d.rectangle([bx0, by0, bx1, by0 + 8], fill=(220, 220, 220, 255))
    d.rectangle([bx0, by0, bx0 + int((bx1 - bx0) * frac), by0 + 8],
                fill=(0, 120, 215, 255))
    d.text((28, H - 75), footer, font=fonts.item, fill=(50, 50, 50))
    return img


#  -  -  main animation  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fast", action="store_true", help="fewer frames")
    ap.add_argument("--output", default=DEFAULT_OUT)
    ap.add_argument("--size", nargs=2, type=int, default=[1920, 1080],
                    metavar=("W", "H"))
    args = ap.parse_args()

    build_frames = 8 if not args.fast else 4   # motion frames per stage
    hold_frames = 3 if not args.fast else 1    # settle frames per stage
    orbit_frames = 48 if not args.fast else 20

    W, H = args.size
    pl = pv.Plotter(off_screen=True, window_size=(W, H), lighting="none")
    pl.enable_anti_aliasing("ssaa")
    pl.set_background(BG_BOTTOM, top=BG_TOP)

    try:
        pl.set_environment_texture(studio_environment())
    except Exception:
        pass

    for pos, inten, col in (((-3000, 3500, 6000), 0.9, "white"),
                            ((6000, -3500, 2500), 0.45, (0.85, 0.88, 1.0)),
                            ((7000, 1500, 1500), 0.4, "white")):
        L = pv.Light(position=pos, focal_point=(2180, 0, 500), intensity=inten, color=col)
        L.positional = False
        pl.add_light(L)

    print("Loading + tessellating real CAD geometry ...")
    parts, labels, home_lo, home_hi = build_scene(pl)
    n_stages = len(labels)

    # ground plane + scene framing
    focal = (home_lo + home_hi) / 2.0
    focal[2] = home_lo[2] + 0.42 * (home_hi[2] - home_lo[2])
    diag = float(np.linalg.norm(home_hi - home_lo))
    # radius decreased by 20% to zoom in (1.8 * 0.80 = 1.44)
    radius = diag * 1.44

    ground = pv.Plane(center=(focal[0], focal[1], home_lo[2] - 4),
                      direction=(0, 0, 1),
                      i_size=diag * 2.4, j_size=diag * 1.6)
    pl.add_mesh(ground, color=(0.9, 0.9, 0.9), pbr=True, metallic=0.0,
                roughness=0.55, ambient=0.30)

    fonts = Fonts()
    frames: list[Image.Image] = []

    def render(done_idx, active_idx, progress, az, elev, footer):
        for p in parts:
            if p.stage < active_idx or (p.stage == active_idx and progress >= 1.0):
                p.actor.SetVisibility(True)
                p.actor.user_matrix = np.eye(4)
            elif p.stage == active_idx:
                p.actor.SetVisibility(True)
                p.actor.user_matrix = part_matrix(p, progress)
            else:
                p.actor.SetVisibility(False)
        set_camera(pl, focal, radius, az, elev)
        # Force a fresh render: after toggling actor visibility / user_matrix,
        # screenshot() otherwise returns the PREVIOUS frame's buffer (one-frame lag),
        # which silently drops every part that became visible this frame.
        pl.render()
        img = Image.fromarray(pl.screenshot(return_img=True)).convert("RGB")
        overlay(img, fonts, labels, done_idx, active_idx, footer)
        frames.append(img)

    #  -  -  assembly phase  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    az = 118.0
    elev = 20.0
    print(f"Rendering {n_stages} build stages ...")
    for s in range(n_stages):
        n_in_stage = sum(1 for p in parts if p.stage == s)
        for k in range(build_frames):
            progress = (k + 1) / build_frames
            footer = f"Installing  {labels[s]}   ({n_in_stage} parts)"
            render(s, s, progress, az, elev, footer)
            az += 0.9
        
        for _ in range(hold_frames):
            render(s + 1, s, 1.0, az, elev,
                   f"Installed  {labels[s]}")
            az += 0.5
        print(f"  [{int(100*(s+1)/n_stages):3d}%]  {labels[s]}  ({n_in_stage} parts)")

    #  -  -  orbit phase  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    print(f"Rendering {orbit_frames}-frame 360 orbit ...")
    az_base = az
    for i in range(orbit_frames):
        a = az_base + 360.0 * i / orbit_frames
        el = 18.0 + 6.0 * math.sin(2 * math.pi * i / orbit_frames)
        deg = int(360 * i / orbit_frames)
        render(n_stages, n_stages, 1.0, a, el,
               f"Complete assembly   {deg:3d} deg   -   {len(parts)} parts")
        if (i + 1) % 8 == 0:
            print(f"  orbit {i + 1}/{orbit_frames}")

    pl.close()

    #  -  -  encode GIF  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - 
    # Build ONE palette from a fully-assembled frame so every frame shares colours
    # that include the red bodywork.  (Quantizing each frame independently makes
    # Pillow apply frame-0's car-less palette globally, erasing the red car.)
    print(f"Encoding {len(frames)} frames -> {args.output} ...")
    ref = frames[-1].quantize(colors=256, method=Image.Quantize.MEDIANCUT)
    pal = [f.quantize(palette=ref, dither=Image.Dither.FLOYDSTEINBERG)
           for f in frames]
    pal[0].save(args.output, save_all=True, append_images=pal[1:],
                optimize=True, duration=FRAME_MS, loop=0, disposal=1)
    mb = os.path.getsize(args.output) / 1e6
    print(f"Done!  {args.output}  ({mb:.1f} MB, {len(frames)} frames)")


if __name__ == "__main__":
    main()

