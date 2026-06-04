"""
Suspension module for Classic SportsCar ModelA.
Contains highly detailed local-origin representations of MacPherson front
and Semi-Trailing rear suspension components.
"""

import cadquery as cq
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


def build_control_arm_L():
    """
    PART 1: PRT_Control_Arm_Lower_L
    A forged aluminum V-shape control arm.
    Inner ball joint boss at origin (0,0,0).
    Outer ball joint boss at local (150, 336, 30).
    Rear pin at local (300, 0, 0).
    """
    p_inner = (0, 0, 0)
    p_outer = (150, 336, 30)
    
    boss_inner = make_boss(p_inner, 22, 35)
    hole_inner = make_boss(p_inner, 10, 40)
    
    boss_outer = make_boss(p_outer, 24, 30)
    hole_outer = make_boss(p_outer, 12, 35)
    
    boss_rear = make_boss((260, 0, 0), 18, 25)
    pin_rear = make_tube((260, 0, 0), (320, 0, 0), 10)
    
    link1 = make_link(p_inner, p_outer, 35, 18)
    link2 = make_link(p_inner, (260, 0, 0), 30, 18)
    link3 = make_link(p_outer, (260, 0, 0), 25, 15)
    
    rim1 = make_link(p_inner, p_outer, 12, 30)
    rim2 = make_link(p_inner, (260, 0, 0), 12, 30)
    risportscar = make_link(p_outer, (260, 0, 0), 10, 25)
    
    arm_solid = C.U([boss_inner, boss_outer, boss_rear, pin_rear, link1, link2, link3, rim1, rim2, risportscar])
    
    holes = C.U([hole_inner, hole_outer])
    arm = cq.Workplane("XY").newObject([arm_solid]).cut(cq.Workplane("XY").newObject([holes]))
    
    return arm.val()


def parts():
    """Re-export LCA from front_macpherson for STEP hierarchy."""
    from .front_macpherson import _lca_left
    left  = _lca_left()
    right = C.mirror_y(left)
    return [
        (left,  C.ARM, "PRT_LCA_FL"),
        (right, C.ARM, "PRT_LCA_FR"),
    ]

