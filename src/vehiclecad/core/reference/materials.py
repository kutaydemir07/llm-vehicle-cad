import cadquery as cq

"""Shared config, dimensions, colours and geometry helpers for the SportsCar assembly.

Frame: +x rear (0 at front bumper), +y LEFT, +z up (0 = ground). Millimetres.
Every module builds its parts already located in this vehicle frame and returns
a list of (solid, rgb, name) tuples (same contract as cadsim.aircraft.a400m_parts).

The ModelA SportsCar is a SHARP, BOXY, three-box coupe, NOT an organic blob.  The station
tables below are deliberately slab-sided with small corner radii so the loft
reads as crisp sheet-metal.  Its signature box flares are NOT in these tables --
they are separate proud blisters built in `flares.py`; the body sides stay at
~1615 mm wide and the flares define the 1680 mm overall width.
"""

# ---------------------------------------------------------------- dimensions
L, W, H = 4345.0, 1680.0, 1370.0
WB, TRACK_F, TRACK_R = 2562.0, 1412.0, 1433.0
AXLE_F, AXLE_R = 810.0, 810.0 + 2562.0
# Catalog 205/55VR15 OD is about 606.5 mm; the detailed mesh keeps 600 mm as
# its ground-stable model datum while retaining the researched 205 mm width.
TIRE_D, TIRE_W = 600.0, 205.0
TIRE_R = TIRE_D / 2.0
WHEEL_Z = TIRE_R
BELT = 1016.0          # beltline / shoulder height (top of doors, base of glass)
ROOF = 1368.0          # roof crown height
FLARE_Y = 840.0        # outer half-width at the flares  => W = 1680
SIDE_Y = 808.0         # body-side (door-skin) half-width => ~1616 wide
ROCKER_Z0 = 214.0      # nominal lower body / rocker lower datum
ROCKER_Z1 = 340.0      # nominal rocker top / lower door datum
ARCH_TRIM_Z0 = 222.0   # visible arch lips/liners should not hang below this

# ---------------------------------------------------------------- colours
RED   = (0.74, 0.05, 0.06)
GLASS = (0.11, 0.14, 0.19)
TIRE  = (0.06, 0.06, 0.07)
RIM   = (0.62, 0.63, 0.66)
CHROME= (0.80, 0.81, 0.83)
LIGHT = (0.90, 0.93, 0.97)
BLACK = (0.06, 0.06, 0.06)
TRIM_BLK = (0.12, 0.12, 0.13)     # satin-black plastic trim (bumpers / skirts)
TAILR = (0.62, 0.02, 0.02)
TAILW = (0.92, 0.92, 0.94)        # reverse-lamp white
STEEL = (0.40, 0.41, 0.44)
AMBER = (0.86, 0.46, 0.06)
CALIPER = (0.74, 0.08, 0.05)
SEAM  = (0.09, 0.09, 0.10)

# ---------------------------------------------------------------- station tables
# (x, a=half-width, z0=bottom, z1=top, rb=bottom-corner radius, rt=top-corner radius)
# LOWER BODY: a SHARP three-box (ModelA SportsCar is slab-sided and crisp, not a wedge).
#   * z0 (lower edge) stays LOW and nearly FLAT -- a horizontal rocker line ~z195
#     along the sides -- and the FRONT and REAR faces drop almost vertically to
#     bumper-top height (~z400).  The body is NOT held high at the overhangs:
#     the bumpers OVERLAP the lower body face (a real bolted lap), so the fascia
#     cannot float and the silhouette reads as a box instead of a boat hull.
#   * z1 (upper edge) is a long, gently-sloping hood -> a FLAT beltline (BELT=1016)
#     across the whole cabin -> a RAISED flat trunk deck -> near-vertical Kamm tail.
#   * corner radii are SMALL (crisp character-line edges, not an organic blob).
# z0 is held DEAD FLAT (~z193) from the front face all the way to the tail: the
# rocker/lower-body line is one straight horizontal edge, and the FRONT and REAR
# faces drop vertically the full height to that line (no wedge / trapezoid in the
# overhangs).  The bumpers are then flush panels ON this vertical face, not blocks
# stuck onto a receding edge.
_Z0 = 193.0
BODY = [
 (60,   698, _Z0,  876, 10, 18),   # FRONT FACE: full-height vertical panel
 (215,  750, _Z0,  952, 12, 22),   # hood leading edge / headlamp brow / fender start
 (470,  794, _Z0,  980, 14, 26),   # front fender over the wheel arch
 (810,  808, _Z0, 1006, 16, 22),   # front axle / fender top
 (1180, 812, _Z0, 1014, 18, 16),   # cowl approach (rear of hood)
 (1500, 812, _Z0, 1016, 18, 12),   # cowl / beltline -- CABIN BEGINS (flat top, flat rocker)
 (2150, 812, _Z0, 1016, 18, 12),   # mid door (flat beltline + flat rocker)
 (2780, 812, _Z0, 1016, 18, 12),   # rear door -> quarter (flat beltline)
 (3240, 810, _Z0, 1016, 16, 12),   # rear quarter / backlight base (flat beltline)
 (3660, 802, _Z0, 1030, 14, 20),   # trunk deck start (FLAT, ~level with beltline -- no hump)
 (4150, 770, _Z0, 1028, 12, 22),   # trunk deck (flat)
 (4340, 712, _Z0, 1022, 10, 20),   # TAIL FACE: full-height vertical panel, flat deck
]
# GREENHOUSE: a long, low ModelA glass-house.  z0 is CONSTANT at the beltline (BELT)
# so the whole cabin sits on the flat body top on one shared plane.  z1 traces the
# DLO roofline: a fairly UPRIGHT windshield (header pulled forward) -> a LONG, near-
# flat roof -> the SportsCar's laid-back backlight feeding the raised trunk deck.  The base
# is held WIDE (a~806, only ~2-6 mm inboard of the body side) and the tumblehome is
# GENTLE (crown a~770) so the cabin grows out of the body instead of perching on it
# like a separate box.  Small top radii keep the roof rails crisp; the thin
# windshield-base station uses tiny radii to avoid self-intersection.  10 stations
# give a smoother ruled loft than the old 8.
GREEN = [
 (1500, 806, BELT, 1022,  2,  2),  # cowl / windshield base (sits on the beltline)
 (1605, 798, BELT, 1150, 12, 16),  # windshield lower
 (1715, 786, BELT, 1318, 14, 20),  # windshield upper
 (1772, 780, BELT, 1364, 14, 20),  # header (top of windshield) -- fairly upright
 (2090, 772, BELT, 1366, 16, 18),  # front roof
 (2440, 770, BELT, 1366, 16, 18),  # roof crown (long flat roof)
 (2760, 772, BELT, 1358, 16, 20),  # rear roof / top of backlight
 (2980, 780, BELT, 1238, 14, 22),  # backlight upper
 (3130, 790, BELT, 1120, 12, 20),  # backlight mid
 (3240, 800, BELT, 1050, 10, 16),  # backlight base (meets the trunk deck)
]
# inset copy of the lower body -> subtract to get a ~7 mm sheet-metal shell.  The
# cabin-region top (z1 == BELT) is held UNCHANGED so the lower-body cavity reaches
# the beltline and joins the greenhouse cavity cleanly (no z1-7 lip there).
BODY_INSET = [(x, a - 7, z0 + 7, (z1 if abs(z1 - BELT) < 1.0 else z1 - 7),
               max(rb - 2, 2), max(rt - 2, 2))
              for (x, a, z0, z1, rb, rt) in BODY]
# inset copy of the greenhouse -> subtract so the cabin/roof is a shell too, not a
# solid block.  The cavity FLOOR stays on the beltline (z0 kept) so it joins the
# body cavity; the roof is inset by 9, clamped so the thin windshield-base section
# can never invert (z1 < z0).  Together with BODY_INSET this hollows the body to a wall.
GREEN_INSET = [(x, a - 9, z0, max(z1 - 9, z0 + 4), max(rb - 2, 2), max(rt - 2, 2))
               for (x, a, z0, z1, rb, rt) in GREEN]
# thin (~6 mm) outer skin of the greenhouse -> the glazing panes are cut from this
# so each pane lies FLUSH on the cabin surface and exactly fills its DLO opening.
GREEN_SKIN = [(x, a - 6, z0, max(z1 - 6, z0 + 3), max(rb - 2, 2), max(rt - 2, 2))
              for (x, a, z0, z1, rb, rt) in GREEN]

# ---------------------------------------------------------------- helpers
