"""Door inner panels (trim panels)  -  left and right.

Left: y=+708-734, x=1530-2470, z=330-1002.
Right: y=-734 to -708, same x/z range.

Collision-free:
   -  Panels are thin (26 mm) and sit inboard of the aperture/door shell.
   -  x range 1500-2490 is between A and B pillars.
   -  z 310-1010 stays below door glass (z=1010+) and above sill (z=310).
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL = (0.10, 0.10, 0.12)


def _door_panel_left():
    """Left door trim panel."""
    panel = C.rbox(1530, 708, 330, 940, 26, 672, 6)
    lower_pocket = C.rbox(1595, 704, 390, 320, 22, 176, 5)
    armrest = C.rbox(1768, 700, 690, 440, 40, 92, 8)
    pull_handle = C.rbox(2088, 698, 718, 190, 42, 50, 5)
    window_crank = C.cyl(26, 14, (1930, 694, 792), (0, 1, 0))
    crank_knob = C.cyl(8, 42, (1930, 680, 792), (0, 1, 0))
    lock_pull = C.cyl(6, 54, (2395, 700, 966), (0, 0, 1))
    speaker_grille = C.cyl(62, 10, (1650, 702, 515), (0, 1, 0))
    panel = panel.cut(C.rbox(1608, 712, 406, 294, 24, 144, 5))
    return C.U([
        panel, lower_pocket, armrest, pull_handle, window_crank,
        crank_knob, lock_pull, speaker_grille,
    ])


def parts():
    left  = _door_panel_left()
    right = C.mirror_y(left)
    return [
        (left,  COL, "PRT_Door_Panel_Left"),
        (right, COL, "PRT_Door_Panel_Right"),
    ]
