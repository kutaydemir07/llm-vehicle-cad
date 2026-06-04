"""
Suspension module for Classic SportsCar ModelA.
Contains highly detailed local-origin representations of MacPherson front
and Semi-Trailing rear suspension components.
"""

import cadquery as cq
from vehiclecad.core.reference import common as C
from vehiclecad.core.reference import hardpoints as SK


def make_boss(p, r, h):
    """Creates a simple cylindrical boss centered at point p, aligned with Z."""
    plane = cq.Plane(origin=p, normal=(0, 0, 1))
    return cq.Workplane(plane).cylinder(height=h, radius=r).val()



def make_link(p1, p2, w, t):
    """Creates a rectangular box linking two points, acting as a forged web."""
    v = cq.Vector(p2) - cq.Vector(p1)
    L = v.Length
    mid = cq.Vector(p1) + v * 0.5
    plane = cq.Plane(origin=mid, normal=v)
    return cq.Workplane(plane).box(w, t, L).val()



def make_tube(p1, p2, r):
    """Creates a cylindrical tube connecting two points."""
    v = cq.Vector(p2) - cq.Vector(p1)
    L = v.Length
    mid = cq.Vector(p1) + v * 0.5
    plane = cq.Plane(origin=mid, normal=v)
    return cq.Workplane(plane).cylinder(height=L, radius=r).val()





def parts():
    return []

