"""ASM_DETAILED_COMPLETE_VEHICLE_MASTER - Top-level assembly with engineering-grade hierarchy.

This root assembly contains very little actual geometry.  Instead, it organises
the car into functional sub-assemblies that mirror a real automotive product
structure:

    ASM_DETAILED_COMPLETE_VEHICLE_MASTER (V-model systems 1000-14000)
     -  PRT_Master_Skeleton          (reference: hardpoints & datums)
     -  ASM_1000_Body_Structure      (BiW: structural skeleton + outer skin)
     -  ASM_1200_Closures            (hood / doors / trunk lid)
     -  ASM_2000_Chassis             (subframes + underbody crossmembers)
     -  ASM_3000_Suspension          (MacPherson front, semi-trailing rear, ARBs)
     -  ASM_4000_Steering            (rack, column, EPS, wheel)
     -  ASM_5000_Brakes              (discs, calipers, lines, handbrake)
     -  ASM_6000_Powertrain          (engine, gearbox, intake, exhaust, fuel)
     -  ASM_6200_Driveline           (clutch, propshaft, diff, half-shafts)
     -  ASM_7000_Thermal_HVAC        (radiator, cooling, heater / blower)
     -  ASM_8000_Electrical          (battery, ECU, fusebox, harness)
     -  ASM_9000_Interior            (dash, console, seats, cage, carpets)
     -  ASM_10000_Exterior           (aero kit, fascia, bumper, trim)
     -  ASM_10500_Glazing            (windscreen, backlight, side glass)
     -  ASM_14000_Fasteners_Brackets (engine / trans mounts, brackets)
     -  ASM_Corner_{FL,FR,RL,RR}     (4x wheel / brake corner assemblies)

build() returns (root_assembly, flat_parts) where flat_parts is the
[(solid, rgb, name), ...] list used for rendering / mesh export.
"""
from __future__ import annotations
import cadquery as cq
from vehiclecad.assemblies.product_tree import add_to_root, system_parts
from vehiclecad.core.reference import hardpoints as SK
from vehiclecad.core.reference import materials as C


# ------------------------------------------------------------------------
#  ASSEMBLY TREE DEFINITION
# ------------------------------------------------------------------------

def subassemblies():
    """name -> [(solid, rgb, name), ...] organised by the V-model systems.

    The data is sourced from atomic leaf part files and grouped at top-level
    system nodes for audit/report compatibility.
    """
    return system_parts()


def _skeleton_marker():
    """Create small datum markers at key hardpoints for visual reference.

    These are tiny spheres (r=8mm) coloured bright yellow, placed at the
    CG, axle centres, and engine mounts - just enough to see the skeleton
    in renders without cluttering the assembly.
    """
    from cadquery import Solid, Vector
    DATUM = (0.95, 0.85, 0.15)  # bright yellow
    markers = []
    # CG marker
    markers.append((
        Solid.makeSphere(12, Vector(SK.DT.cg_x, 0, SK.DT.cg_z)),
        DATUM, "datum_CG"
    ))
    # Axle centre markers
    markers.append((
        Solid.makeSphere(8, Vector(SK.DT.axle_front_x, 0, SK.DT.tire_radius)),
        DATUM, "datum_front_axle"
    ))
    markers.append((
        Solid.makeSphere(8, Vector(SK.DT.axle_rear_x, 0, SK.DT.tire_radius)),
        DATUM, "datum_rear_axle"
    ))
    return markers


def build():
    """Build the full hierarchical assembly.

    Returns (root_assembly, flat_parts) where root_assembly is a nested
    cq.Assembly and flat_parts is the flat list for rendering.
    """
    root = cq.Assembly(name="ASM_DETAILED_COMPLETE_VEHICLE_MASTER")

    # Add skeleton datum markers to root
    skel_asm = cq.Assembly(name="PRT_Master_Skeleton")
    for shp, rgb, nm in _skeleton_marker():
        skel_asm.add(shp, name=nm, color=cq.Color(*rgb))
    root.add(skel_asm, name="PRT_Master_Skeleton")

    flat = add_to_root(root)

    return root, flat


def print_tree(root=None, indent=0):
    """Print the assembly tree for debugging / verification."""
    if root is None:
        root, _ = build()
    prefix = "  " * indent
    name = root.name or "(unnamed)"
    n_children = len(root.children) if hasattr(root, 'children') else 0
    print(f"{prefix}{'+-- ' if indent > 0 else ''}{name}  [{n_children} children]")
    if hasattr(root, 'children'):
        for child in root.children:
            if hasattr(child, 'name'):
                print_tree(child, indent + 1)


def parts():
    """Return the flat [(solid, rgb, name), ...] list for rendering / mesh export."""
    _, flat = build()
    return flat
