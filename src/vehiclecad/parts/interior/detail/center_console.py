"""Centre console with gear lever, arm rest, and handbrake recess.

The console is a tunnel-mounted trim shell: its centre spine seats on the
driveshaft tunnel top, while the side cheeks hang just outside the tunnel walls
without filling the prop-shaft envelope.  The handbrake pocket is relieved
around the ASM_5300 parking-brake lever hardpoints.
"""
from __future__ import annotations
from vehiclecad.core.reference import common as C

COL_TRIM   = (0.10, 0.10, 0.11)
COL_CHROME = (0.82, 0.82, 0.82)


def _console_body():
    # Tunnel top is at z=480, so the centre cap starts just above the carpeted
    # tunnel.  The cheeks land beside the tunnel rather than colliding with it.
    tunnel_cap = C.rbox(1540, -104, 486, 830, 208, 72, 9)
    left_cheek = C.rbox(1566, 104, 232, 760, 20, 276, 5)
    right_cheek = C.mirror_y(left_cheek)
    front_stack = C.rbox(1540, -104, 548, 250, 208, 92, 8)
    rear_armrest = C.rbox(2020, -96, 600, 310, 192, 62, 10)

    # Gearshift boot and knob are centred on the tunnel and mated to the console
    # opening; the leather boot is a raised trim feature, not a block below.
    shifter_surround = C.rbox(1724, -64, 558, 128, 128, 20, 6)
    shifter_boot = C.rbox(1746, -46, 578, 84, 92, 58, 8)
    lever = C.cyl(7, 92, (1788, 0, 628), (0, 0, 1))
    knob = C.cyl(24, 32, (1788, 0, 720), (0, 0, 1))

    # Small switch/radio details on the centre stack.
    radio = C.rbox(1656, -78, 598, 84, 156, 26, 4)
    hvac = C.rbox(1608, -80, 562, 82, 160, 22, 4)
    switch_row = C.U([
        C.rbox(1588 + i * 34, -72, 638, 18, 24, 12, 3)
        for i in range(4)
    ])

    console = C.U([
        tunnel_cap, left_cheek, right_cheek, front_stack, rear_armrest,
        shifter_surround, shifter_boot, lever, knob, radio, hvac, switch_row,
    ])

    # Clear the driveline tunnel and parking-brake lever envelope.
    tunnel_clearance = C.box(1510, -88, 300, 900, 176, 184)
    handbrake_slot = C.rbox(1815, 28, 520, 250, 122, 166, 9)
    front_footwell_clearance = C.rbox(1510, -96, 330, 120, 192, 174, 8)
    return console.cut(tunnel_clearance).cut(handbrake_slot).cut(front_footwell_clearance)


def parts():
    return [(_console_body(), COL_TRIM, "PRT_Centre_Console")]
