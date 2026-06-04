"""
Suspension module for Classic SportsCar ModelA.
Contains highly detailed local-origin representations of MacPherson front
and Semi-Trailing rear suspension components.
"""

import cadquery as cq
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


def build_hub_knuckle_L():
    """
    PART 3: PRT_Hub_Knuckle_L
    Steering knuckle/spindle.
    Origin at the ball joint (0,0,0).
    Contains lower ball joint receiver, upper strut clamping collar,
    axle spindle, and steering arm.
    """
    receiver = make_boss((0, 0, 0), 25, 30)
    
    collar_pos = (15, 0, 50)
    collar = cq.Workplane("XY").cylinder(height=60, radius=35).translate(collar_pos).val()
    collar_cut = cq.Workplane("XY").cylinder(height=70, radius=25.5).translate(collar_pos).val()
    
    body = make_link((0, 0, 0), collar_pos, 45, 50)
    
    spindle_base = (15, 35, 40)
    spindle = cq.Workplane("ZX").cylinder(height=100, radius=20).translate(spindle_base).val()
    spindle_hub = cq.Workplane("ZX").cylinder(height=20, radius=40).translate((15, 60, 40)).val()
    
    steer_end = (-120, -10, 20)
    steer_arm = make_link((0, 10, 30), steer_end, 20, 28)
    steer_boss = make_boss(steer_end, 16, 25)
    
    ear1 = make_boss((50, 15, 80), 12, 16)
    ear1_link = make_link(collar_pos, (50, 15, 80), 15, 20)
    ear2 = make_boss((50, 15, 20), 12, 16)
    ear2_link = make_link((10, 0, 20), (50, 15, 20), 15, 20)
    
    knuckle_solid = C.U([receiver, collar, body, spindle, spindle_hub, steer_arm, steer_boss, ear1, ear1_link, ear2, ear2_link])
    knuckle = cq.Workplane("XY").newObject([knuckle_solid]).cut(cq.Workplane("XY").newObject([collar_cut]))
    
    return knuckle.val()





def parts():
    """Re-export hub/knuckle parts from front_macpherson and rear_semitrailing."""
    from .front_macpherson import _hub_knuckle_left
    from .rear_semitrailing import _rear_hub_left
    fl = _hub_knuckle_left()
    rl = _rear_hub_left()
    return [
        (fl,              C.ARM, "PRT_Hub_Knuckle_FL"),
        (C.mirror_y(fl),  C.ARM, "PRT_Hub_Knuckle_FR"),
        (rl,              C.ARM, "PRT_Rear_Hub_RL"),
        (C.mirror_y(rl),  C.ARM, "PRT_Rear_Hub_RR"),
    ]

