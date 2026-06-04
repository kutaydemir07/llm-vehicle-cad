"""Trailing arm stub - geometry is in rear_semitrailing.py.

The trailing arm geometry is fully implemented in
`suspension/rear_semitrailing.py`.  This module just re-exports it so
the old `trailing_arm.py` import still resolves.
"""
from .rear_semitrailing import parts  # noqa: F401


# --- legacy function kept for reference ---
def build_trailing_arm_L():
    """
    PART 4: PRT_Trailing_Arm_L
    Semi-trailing arm for the rear.
    Origin at the inner pivot (0,0,0).
    Outer pivot at local (0, 240, 0).
    Wheel hub at local (422, 440, -10).
    Spring seat at local (300, 280, 20).
    Shock mount at local (430, 300, 30).
    """
    p_hub = (422, 440, -10)
    p_spring = (300, 280, 20)
    p_shock = (430, 300, 30)
    
    pivot = make_tube((0, -20, 0), (0, 260, 0), 22)
    
    hub_housing = cq.Workplane("ZX").cylinder(height=70, radius=48).translate(p_hub).val()
    hub_hole = cq.Workplane("ZX").cylinder(height=80, radius=30).translate(p_hub).val()
    
    arm1 = make_link((0, 30, 0), p_hub, 60, 45)
    arm2 = make_link((0, 210, 0), p_hub, 55, 40)
    
    web1 = make_link((0, 120, 0), p_hub, 180, 15)
    web2 = make_link((150, 120, 0), (250, 300, 0), 200, 15)
    
    seat = make_boss(p_spring, 65, 8)
    seat_lip = make_boss(p_spring, 40, 25)
    seat_support = make_tube((300, 280, -30), p_spring, 30)
    
    shock_boss = make_boss(p_shock, 22, 35)
    shock_hole = make_boss(p_shock, 10, 45)
    
    rib1 = make_link((0, 30, 20), (400, 400, 10), 12, 35)
    rib2 = make_link((0, 210, 20), (400, 440, 10), 12, 35)
    
    arm_solid = C.U([pivot, hub_housing, arm1, arm2, web1, web2, seat, seat_lip, seat_support, shock_boss, rib1, rib2])
    holes = C.U([hub_hole, shock_hole])
    arm = cq.Workplane("XY").newObject([arm_solid]).cut(cq.Workplane("XY").newObject([holes]))
    
    return arm.val()





def parts():
    return []
