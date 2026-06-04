"""
Suspension module for Classic SportsCar ModelA.
Contains highly detailed local-origin representations of MacPherson front
and Semi-Trailing rear suspension components.
"""

import cadquery as cq
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


def build_strut_tube_L():
    """
    PART 2: PRT_Strut_Tube_L
    MacPherson strut housing.
    Origin at the lower mount point (0,0,0).
    51mm thick tube going up to local (0, -126, 672).
    Lower spring perch at local (0, -96, 60).
    """
    p_base = (0, 0, 0)
    p_top  = (0, -126, 672)
    p_rod_top = (0, -150, 800)
    p_perch = (0, -96, 60)
    
    tube = make_tube(p_base, p_top, 25.5)
    
    plate1 = cq.Workplane("YZ").box(40, 8, 60).translate((15, 20, 20)).val()
    plate2 = cq.Workplane("YZ").box(40, 8, 60).translate((15, -20, 20)).val()
    back_plate = cq.Workplane("XZ").box(40, 60, 8).translate((15, 0, 50)).val()
    
    v_strut = cq.Vector(p_top) - cq.Vector(p_base)
    plane_perch = cq.Plane(origin=p_perch, normal=v_strut)
    perch_base = cq.Workplane(plane_perch).cylinder(height=5, radius=85).val()
    perch_cut = cq.Workplane(plane_perch).cylinder(height=20, radius=80).val()
    perch_lip = cq.Workplane(plane_perch).cylinder(height=15, radius=85).val()
    
    rod = make_tube(p_top, p_rod_top, 11)
    collar = make_tube(p_base, (0, -18, 96), 30)

    strut_solid = C.U([tube, plate1, plate2, back_plate, perch_base, perch_lip, rod, collar])
    strut = cq.Workplane("XY").newObject([strut_solid]).cut(cq.Workplane("XY").newObject([perch_cut]))
    
    return strut.val()


def parts():
    """Re-export strut + spring from front_macpherson for STEP hierarchy."""
    from .front_macpherson import _strut_tube_left, _spring_left
    st_l = _strut_tube_left()
    sp_l = _spring_left()
    return [
        (st_l,              C.DAMPER, "PRT_Strut_Assembly_FL"),
        (C.mirror_y(st_l),  C.DAMPER, "PRT_Strut_Assembly_FR"),
        (sp_l,              C.SPRING, "PRT_Coil_Spring_FL"),
        (C.mirror_y(sp_l),  C.SPRING, "PRT_Coil_Spring_FR"),
    ]

