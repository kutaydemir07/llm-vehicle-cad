"""Top-down assembly fitment data for the Classic SportsCar ModelA CAD model.

The model is intentionally organised from vehicle datums down to systems.  This
module keeps the non-visual assembly rules in one place: what makes an ModelA SportsCar
recognisable, how systems are grouped, in what order they assemble, and which
part contacts are valid CAD interfaces rather than packaging clashes.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


VEHICLE_CHARACTERISTICS = (
    "boxy two-door touring car coupe",
    "wide square bolt-on arches and side skirts",
    "raised rear deck with pedestal rear wing",
    "quad round headlamps with twin kidney grille",
    "black bumper rub strips and lower air dam",
    "15 inch cross-spoke wheels with 5x120 lug pattern",
    "longitudinal inline-four with ITBs and tubular exhaust",
    "MacPherson front suspension and semi-trailing-arm rear axle",
)


# Sub-assembly node (key from assembly.subassemblies()) -> major system group.
# Keyed by the V-model node names.
SUB_TO_MAJOR = {
    "ASM_1000_Body_Structure":      "BODY_STRUCTURE",
    "ASM_1200_Closures":            "BODY_STRUCTURE",
    "ASM_2000_Chassis":             "CHASSIS",
    "ASM_3000_Suspension":          "SUSPENSION",
    "ASM_4000_Steering":            "STEERING",
    "ASM_5000_Brakes":              "BRAKES",
    "ASM_6000_Powertrain":          "POWERTRAIN",
    "ASM_6200_Driveline":           "DRIVELINE",
    "ASM_7000_Thermal_HVAC":        "THERMAL_HVAC",
    "ASM_8000_Electrical":          "ELECTRICAL",
    "ASM_9000_Interior":            "INTERIOR",
    "ASM_10000_Exterior":           "EXTERIOR",
    "ASM_10500_Glazing":            "EXTERIOR",
    "ASM_11000_Lighting":           "EXTERIOR",
    "ASM_12000_Safety":             "SAFETY",
    "ASM_13000_Fluids_Plumbing":    "FLUIDS",
    "ASM_14000_Fasteners_Brackets": "FASTENERS",
    "ASM_15000_Road_Corners":       "ROAD_CORNERS",
    "ASM_Corner_FL":                "CORNER_FL",
    "ASM_Corner_FR":                "CORNER_FR",
    "ASM_Corner_RL":                "CORNER_RL",
    "ASM_Corner_RR":                "CORNER_RR",
}


MAJOR_TO_PARENT = {
    "BODY_STRUCTURE": "STRUCTURE",
    "CHASSIS":        "STRUCTURE",
    "EXTERIOR":       "STRUCTURE",
    "SAFETY":         "STRUCTURE",
    "FASTENERS":      "STRUCTURE",
    "POWERTRAIN":     "DRIVETRAIN",
    "DRIVELINE":      "DRIVETRAIN",
    "FLUIDS":         "DRIVETRAIN",
    "SUSPENSION":     "RUNNING_GEAR",
    "STEERING":       "RUNNING_GEAR",
    "BRAKES":         "RUNNING_GEAR",
    "ROAD_CORNERS":   "RUNNING_GEAR",
    "CORNER_FL":      "RUNNING_GEAR",
    "CORNER_FR":      "RUNNING_GEAR",
    "CORNER_RL":      "RUNNING_GEAR",
    "CORNER_RR":      "RUNNING_GEAR",
    "INTERIOR":       "CABIN",
    "ELECTRICAL":     "CABIN",
    "THERMAL_HVAC":   "CABIN",
}


# label, sub-assembly keys, color, fly-in vector used by the GIF generator.
ASSEMBLY_SEQUENCE = (
    ("Master Datums", (), (0.95, 0.85, 0.15), (0, 0, 420)),
    ("Chassis", ("ASM_2000_Chassis",), (0.50, 0.52, 0.60), (0, 0, 480)),
    ("Suspension", ("ASM_3000_Suspension",), (0.45, 0.62, 0.92), (-360, 0, 250)),
    ("Steering", ("ASM_4000_Steering",), (0.40, 0.55, 0.85), (-300, 0, 200)),
    ("Brakes", ("ASM_5000_Brakes",), (0.92, 0.18, 0.18), (0, 420, 240)),
    ("Wheels", ("ASM_15000_Road_Corners",), (0.22, 0.22, 0.27), (0, 620, 140)),
    ("Powertrain", ("ASM_6000_Powertrain",), (0.96, 0.47, 0.10), (-520, 0, 280)),
    ("Driveline", ("ASM_6200_Driveline",), (0.92, 0.76, 0.08), (0, 0, 380)),
    ("Thermal / HVAC", ("ASM_7000_Thermal_HVAC",), (0.10, 0.82, 0.88), (-300, -380, 260)),
    ("Electrical", ("ASM_8000_Electrical",), (0.20, 0.70, 0.90), (-300, -380, 300)),
    ("Fasteners / Brackets", ("ASM_14000_Fasteners_Brackets",), (0.14, 0.14, 0.14), (0, 0, 620)),
    ("Interior", ("ASM_9000_Interior",), (0.72, 0.54, 0.34), (0, 0, 520)),
    ("Body Structure", ("ASM_1000_Body_Structure",), (0.52, 0.55, 0.65), (0, 0, 520)),
    ("Body Closures", ("ASM_1200_Closures",), (0.70, 0.70, 0.70), (0, 500, 200)),
    ("Exterior + Glazing", ("ASM_10000_Exterior", "ASM_10500_Glazing"), (0.82, 0.85, 0.96), (0, -620, 260)),
)


@dataclass(frozen=True)
class InterfaceRule:
    """One valid contact rule used by collision validation."""

    a: tuple[str, ...]
    b: tuple[str, ...]
    reason: str

    def matches(self, left: str, right: str) -> bool:
        return (_matches_any(left, self.a) and _matches_any(right, self.b)) or (
            _matches_any(left, self.b) and _matches_any(right, self.a)
        )


def _matches_any(value: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in patterns)


ALLOWED_INTERFACES = (
    InterfaceRule(
        ("PRT_Floorpan|PRT_Rear_Bulkhead|PRT_Roof|PRT_Rocker|PRT_Sill|PRT_Wheel_Tub",),
        ("PRT_Floor_Carpet|PRT_Headliner|PRT_Door_Panel|dashboard|glovebox|instrument_binnacle",),
        "trim or carpet bonded to body-in-white",
    ),
    InterfaceRule(
        ("Roof_Header|PRT_Roof_Rail|PRT_Roof_Bow",),
        ("PRT_Headliner|dlo_belt|drip_rail|b_pillar_cover",),
        "trim/headliner seated against roof and aperture structure",
    ),
    InterfaceRule(
        ("PRT_HVAC|PRT_Blower|PRT_Fuse|PRT_ECU",),
        ("dashboard|instrument_binnacle|glovebox|centre_vents|PRT_Centre_Console",),
        "under-dash module inside dashboard package",
    ),
    InterfaceRule(
        ("PRT_Front_Rotor|PRT_Rear_Rotor|PRT_Front_Caliper|PRT_Rear_Caliper",),
        ("PRT_Hub_Knuckle|PRT_Rear_Hub|hub_|rim_|lug_bolts|cap_",),
        "wheel-end brake stack mounted to hub",
    ),
    InterfaceRule(
        ("PRT_Engine_Mount|PRT_Engine_Mount_Rubber",),
        ("PRT_Engine_Mount_Bracket|PRT_Front_Subframe|PRT_I4_Engine_Engine_Block|PRT_Engine_Mount",),
        "engine mount bolted to chassis bracket",
    ),
    InterfaceRule(
        ("PRT_Trans_Crossmember|PRT_Firewall_Bulkhead|PRT_Floorpan",),
        ("PRT_ManualGearbox|PRT_Propshaft|PRT_Rear_LSD",),
        "driveline packaged inside tunnel or mounted to crossmember",
    ),
    InterfaceRule(
        ("PRT_Trans_Mount_Rubber|PRT_Trans_Crossmember",),
        ("PRT_ManualGearbox|PRT_Centre_Bearing|PRT_Propshaft|PRT_Floor_Carpet|PRT_Pedal_Box",),
        "transmission mount and tunnel trim share designed mounting space",
    ),
    InterfaceRule(
        ("PRT_Body|PRT_Front_Nose|PRT_Front_Fender|PRT_Rear_Quarter|PRT_Rear_Tail|PRT_Roof_Outer|PRT_Aperture|PRT_Beltline|PRT_Rocker_Outer|PRT_Fuel_Flap|hood|trunk_lid|door_|windshield|backlight|quarter_glass",),
        ("PRT_Box_Flares|PRT_Side_Skirts|PRT_Rear_Deck|PRT_Rear_Wing|front_fascia|rear_bumper|front_splitter",),
        "exterior panels, closures, and aero kit share body mounting flanges",
    ),
    InterfaceRule(
        ("dlo_belt|drip_rail|b_pillar_cover|side_rub_strip|mirror_|door_handle",),
        ("PRT_A_Pillar|PRT_B_Pillar|PRT_C_Pillar|PRT_Roof_Rail|PRT_Aperture|PRT_Beltline|PRT_Rocker_Outer|door_",),
        "exterior trim clipped or bonded to body aperture flanges",
    ),
    InterfaceRule(
        ("PRT_Body|PRT_Front_Nose|PRT_Front_Fender|PRT_Rear_Quarter|PRT_Rear_Tail|PRT_Roof_Outer|PRT_Aperture|PRT_Beltline|PRT_Rocker_Outer|hood|trunk_lid",),
        ("headlamp|reflector|kidney|foglamp|turn_signal|taillamp|tail_centre|roundel|model_script|number_plate",),
        "exterior insert seated in aperture or on skin",
    ),
    InterfaceRule(
        ("PRT_Strut_Tower|PRT_Strut_Top|PRT_Rear_Wheel_Tub",),
        ("PRT_Strut_Assembly|PRT_Coil_Spring|PRT_Rear_Spring|PRT_Rear_Damper|"
         "PRT_Lower_Perch|PRT_Top_Mount|PRT_Rear_Coil_Spring|PRT_Rear_Damper_Upper_Eye",),
        "suspension top mount or spring seat contact",
    ),
    InterfaceRule(
        ("PRT_Half_Shaft|PRT_Drive_Shaft|half_shaft|PRT_CV",),
        ("PRT_Rear_Damper|PRT_Rear_Spring",),
        "rear shock / spring lower mount sits alongside the half-shaft",
    ),
    #  -  wheel-corner stack: the tyre/rim rotate concentrically around the
    #    upright, hub, strut and brake disc - these are designed nested contacts,
    #    not packaging clashes.
    InterfaceRule(
        ("tire_|rim_|PRT_Wheel|cap_|lug_|hub_",),
        ("PRT_Strut_Assembly|PRT_Front_Hub|PRT_Rear_Hub|PRT_Hub_Knuckle|"
         "PRT_Front_Rotor|PRT_Rear_Rotor|PRT_Front_Caliper|PRT_Rear_Caliper|"
         "PRT_Trailing_Arm|PRT_Coil_Spring|PRT_Rear_Spring|PRT_Rear_Damper",),
        "rotating wheel/tyre concentric with corner upright, hub and brake stack",
    ),
    #  -  CURRENT corner part names: the mate-built wheel corner emits
    #    brake_rotor / bearing_hub / brake_caliper, and suspension emits
    #    PRT_strut_foot / PRT_LCA / PRT_Trailing_Arm / PRT_Rear_Hub.  The disc/hub/
    #    caliper are BOLTED to the upright/hub/arm (a designed contact), and the
    #    tyre/rim rotate concentrically around the whole stack - not packaging
    #    clashes.  (PRT_strut_damper is deliberately omitted from the rotor rule so
    #    a real strut-tube-through-disc would still be flagged.)
    InterfaceRule(
        ("brake_rotor|bearing_hub|brake_caliper|brake_hat|brake_disc",),
        ("PRT_Hub_Knuckle|PRT_Rear_Hub|PRT_Trailing_Arm|PRT_strut_foot|"
         "PRT_LCA|PRT_lower_perch|bearing_hub",),
        "wheel-end brake stack bolted to the upright / hub / arm",
    ),
    InterfaceRule(
        ("tire_|rim_|hub_|cap_|lug_",),
        ("PRT_strut_damper|PRT_strut_foot|PRT_Hub_Knuckle|PRT_Rear_Hub|PRT_LCA|"
         "PRT_Trailing_Arm|PRT_coil_spring|PRT_r_coil_spring|PRT_r_damper|"
         "brake_rotor|brake_caliper|bearing_hub|PRT_lower_perch",),
        "rotating wheel/tyre concentric with the corner upright/hub/brake stack",
    ),
    InterfaceRule(
        ("PRT_Half_Shaft|PRT_Drive_Shaft|half_shaft|PRT_CV",),
        ("PRT_Rear_Hub|PRT_Hub_Knuckle|PRT_Rear_LSD|PRT_Differential|"
         "PRT_Trailing_Arm|PRT_Front_Rotor|PRT_Rear_Rotor|brake_rotor|hub_",),
        "half-shaft splined into the rear hub / rotor hat / diff output flange",
    ),
    #  -  flywheel / clutch bolt to the crank at the engine rear, inside the bell.
    InterfaceRule(
        ("PRT_Flywheel|PRT_Clutch|PRT_Pressure_Plate|PRT_Bellhousing",),
        ("PRT_I4_Engine_Oil_Pan|PRT_Engine_Mount|PRT_I4_Engine_Engine_Block|PRT_Crank|"
         "PRT_ManualGearbox|PRT_Rear_Main|PRT_I4_Engine_Bellhousing",),
        "flywheel / clutch bolted to the crank at the engine rear",
    ),
    InterfaceRule(
        ("PRT_Front_Rotor|PRT_Rear_Rotor|PRT_Front_Caliper|PRT_Rear_Caliper",),
        ("PRT_Trailing_Arm|PRT_Hub_Knuckle|PRT_Front_Hub|PRT_Rear_Hub|"
         "PRT_Strut_Assembly",),
        "brake rotor/caliper mounted on the upright / trailing-arm",
    ),
    #  -  driveline lives inside the transmission tunnel, under carpet/console,
    #    and the gearbox bellhousing sits against the firewall plane.
    InterfaceRule(
        ("PRT_Propshaft|PRT_ManualGearbox|PRT_Driveshaft|PRT_Half_Shaft|"
         "PRT_Rear_LSD|PRT_Differential|PRT_Diff|PRT_Guibo",),
        ("PRT_Floor_Carpet|PRT_Headliner|PRT_Rear_Bench|PRT_Rear_Seat|"
         "PRT_Centre_Console|PRT_Floorpan|PRT_Trans_Tunnel|PRT_Pedal_Box|"
         "PRT_HVAC|PRT_Heater|PRT_Handbrake|PRT_Parcel_Shelf",),
        "driveline routed inside the transmission tunnel / against the firewall",
    ),
    #  -  body isolator mounts bolt the floor structure DOWN ONTO the frame
    #    rails: the bushing/bolt stack intentionally shares the rail bore.
    InterfaceRule(
        ("PRT_Body_Mount",),
        ("PRT_Frame_Rail|PRT_Rocker|PRT_Floorpan",),
        "body isolator bolted between floor structure and frame rail",
    ),
    #  -  interior trim panels clip onto the body pillars, sills and roof.
    InterfaceRule(
        ("PRT_Door_Panel|PRT_Door_Card|PRT_Floor_Carpet|PRT_Headliner|"
         "PRT_Rear_Bench|PRT_Rear_Seat|PRT_Parcel_Shelf",),
        ("PRT_A_Pillar|PRT_B_Pillar|PRT_C_Pillar|PRT_Rocker|PRT_Sill|"
         "PRT_Roof|PRT_Wheel_Tub|PRT_Aperture|PRT_Beltline|PRT_Rocker_Outer|door_",),
        "interior trim overlaps the body pillars / sills / door it clips onto",
    ),
    #  -  closure panels (doors / hood / trunk) hang in their apertures along the
    #    shut lines and carry the door mirror.
    InterfaceRule(
        ("door_|hood|trunk_lid",),
        ("PRT_A_Pillar|PRT_B_Pillar|PRT_C_Pillar|PRT_Rocker|PRT_Sill|"
         "PRT_Roof|mirror_|PRT_Hinge",),
        "closure panel hung in its aperture along the shut line",
    ),
    #  -  aero skirts, flares and splitter bolt to the rocker, sill and body flanges.
    InterfaceRule(
        ("PRT_Side_Skirt|PRT_Side_Skirts|PRT_Box_Flares|PRT_Front_Air_Dam|"
         "PRT_Front_Splitter|PRT_Splitter",),
        ("PRT_Rocker_Rail|PRT_Rocker|PRT_Sill|PRT_Floorpan|PRT_Wheel_Tub|"
         "PRT_Body|PRT_Front_Fender|PRT_Rear_Quarter|PRT_Rocker_Outer",),
        "aero skirts / flares bolt onto the rocker, sill and body flanges",
    ),
    #  -  glass is bonded into the pillar / aperture, seating against the flange.
    InterfaceRule(
        ("glass|windshield|backlight|quarter_window|side_window",),
        ("PRT_A_Pillar|PRT_B_Pillar|PRT_C_Pillar|PRT_Roof|PRT_Cowl|"
         "PRT_Rear_Bulkhead|PRT_Aperture|PRT_Beltline|PRT_Rocker_Outer|door_",),
        "glazing bonded into the pillar / aperture flange",
    ),
    #  -  steering column passes through the dash and firewall to the rack.
    InterfaceRule(
        ("PRT_Steering_Column|PRT_Steering_Shaft|PRT_Steering_Wheel|"
         "PRT_Steering_Rack",),
        ("dashboard|PRT_Dash|instrument_binnacle|PRT_Firewall|PRT_Pedal_Box|"
         "PRT_Subframe|PRT_Crossmember|PRT_Engine_Bay_Tie",),
        "steering column routed through the dash / firewall to the rack",
    ),
    InterfaceRule(
        ("PRT_Front_ARB",),
        ("PRT_Steering_Rack",),
        "front anti-roll bar routes below and ahead of the steering rack",
    ),
    InterfaceRule(
        ("PRT_Steering_Rack",),
        ("PRT_Hub_Knuckle",),
        "tie-rod outer ball joint seated in the front upright steering arm",
    ),
    InterfaceRule(
        ("PRT_Front_ARB",),
        ("PRT_Front_Subframe_Rail|PRT_Front_Subframe|PRT_Front_Crossmember",),
        "front anti-roll bar carried in chassis bushing brackets at the subframe",
    ),
    InterfaceRule(
        ("PRT_Rear_ARB",),
        ("PRT_Rear_Subframe",),
        "rear anti-roll bar passes through subframe bushing and link clearance corridors",
    ),
    #  -  handbrake lever and boot come up through the console between the seats.
    InterfaceRule(
        ("PRT_Handbrake|handbrake",),
        ("PRT_Centre_Console|PRT_Console|PRT_Front_Seat|PRT_Seat|PRT_Floorpan|"
         "PRT_Floor_Carpet|PRT_Trans_Tunnel",),
        "handbrake lever rises through the console between the seats",
    ),
    #  -  seats and console bolt down to the floorpan / tunnel.
    InterfaceRule(
        ("PRT_Front_Seat|PRT_Rear_Bench|PRT_Rear_Seat|PRT_Seat|"
         "PRT_Centre_Console",),
        ("PRT_Floorpan|PRT_Floor_Carpet|PRT_Trans_Tunnel|PRT_Wheel_Tub|"
         "PRT_Rear_Bulkhead",),
        "seats / console bolted to the floorpan",
    ),
    #  -  solid-disc tyre model sweeps slightly into the wheel-arch structure.
    InterfaceRule(
        ("tire_|rim_",),
        ("PRT_Rocker|PRT_Strut_Tower|PRT_Wheel_Tub|PRT_Floor_Carpet|"
         "PRT_Arch|PRT_Fender|PRT_Box_Flares",),
        "tyre sweep envelope inside the wheel arch",
    ),
    #  -  exhaust is routed past the driveline / chassis with heat-shield clearance.
    InterfaceRule(
        ("PRT_Exhaust|exhaust|PRT_Downpipe|PRT_Collector",),
        ("PRT_Rear_LSD|PRT_Differential|PRT_Trans_Crossmember|PRT_Subframe|"
         "PRT_Floorpan|PRT_Rocker|PRT_Heat_Shield",),
        "exhaust routed past driveline / chassis with heat-shield clearance",
    ),
    #  -  engine-bay (Motorraum) + trunk (Kofferraum) inner BiW panels are welded
    #    to the adjacent body structure / outer skin (and to each other).
    InterfaceRule(
        ("PRT_Inner_Fender|PRT_Apron_Rail|PRT_Radiator_Support|PRT_Boot_Floor|"
         "PRT_Spare_Well|PRT_Rear_Seat_Bulkhead|PRT_Parcel_Shelf",),
        ("PRT_Front_Rail|PRT_Front_Subframe_Rail|PRT_Front_Crossmember|"
         "PRT_Strut_Tower|PRT_top_mount|PRT_Floorpan|PRT_Rocker|PRT_Wheel_Tub|"
         "PRT_Body|PRT_Front_Fender|PRT_Rear_Quarter|PRT_Inner_Fender|PRT_Apron_Rail|PRT_Radiator_Support|"
         "PRT_Parcel_Shelf|PRT_Rear_Seat_Bulkhead|PRT_Spare_Well",),
        "engine-bay / trunk inner BiW panel welded to adjacent body structure",
    ),
    #  -  trailing arm / gearbox mount / diff seated to the subframe or crossmember
    #    at their bushings (designed pivot / mount, not a packaging clash).
    InterfaceRule(
        ("PRT_Rear_Subframe|PRT_Trans_Crossmember",),
        ("PRT_Trailing_Arm|PRT_Trans_Mount_Rubber|PRT_ManualGearbox|PRT_Differential|"
         "PRT_Rear_LSD",),
        "trailing arm / gearbox mount / diff seated to subframe or crossmember",
    ),
    #  -  the rear carrier is one atomic CAD leaf with open windows for the
    #    propshaft, exhaust, rear springs and dampers.  AABB-only collision
    #    checks see the whole carrier bounding box, so these clearance corridors
    #    are registered here while exact boolean checks still verify the solid.
    InterfaceRule(
        ("PRT_Rear_Subframe",),
        ("PRT_Propshaft|PRT_UJoint|PRT_Ujoint|PRT_Exhaust_Mid_Pipe|PRT_Rear_Coil_Spring|"
         "PRT_Rear_Spring_Lower_Perch|PRT_Rear_Spring_Upper_Perch|"
         "PRT_Rear_Damper|PRT_Rear_Damper_Lower_Eye|PRT_Rear_Damper_Upper_Eye",),
        "rear subframe service window around propshaft, exhaust, spring and damper",
    ),
    #  -  gearbox output flange coupled to the propshaft front joint.
    InterfaceRule(
        ("PRT_ManualGearbox|PRT_Bellhousing|PRT_I4_Engine_Bellhousing",),
        ("PRT_Propshaft|PRT_UJoint|PRT_Centre_Bearing",),
        "gearbox output coupled to the propshaft front joint",
    ),
    #  -  saddle fuel tank packaged under the rear seat, above the floor/tunnel.
    InterfaceRule(
        ("PRT_Fuel_Tank|PRT_Fuel_Pump",),
        ("PRT_Floorpan|PRT_Rear_Seat|PRT_Rear_Bench|PRT_Rear_Subframe|"
         "PRT_Trailing_Arm|PRT_Differential|PRT_Rear_LSD|PRT_Rear_Seat_Bulkhead|"
         "PRT_Trans_Tunnel|PRT_Propshaft|PRT_Parcel_Shelf",),
        "saddle fuel tank packaged under the rear seat, above the floorpan/tunnel",
    ),
    #  -  floorpan / firewall welded to the body mounts, rails and crossmembers.
    InterfaceRule(
        ("PRT_Floorpan|PRT_Firewall",),
        ("PRT_Body_Mount|PRT_Front_Rail|PRT_Trans_Crossmember|PRT_Front_Crossmember|"
         "PRT_Rear_Crossmember|PRT_Front_Subframe_Rail",),
        "floorpan / firewall welded to body mounts, rails and crossmembers",
    ),
    #  -  the steering wheel + hub sit just in front of the instrument cluster.
    InterfaceRule(
        ("steering_rim|steering_hub|PRT_Steering_Wheel",),
        ("dashboard|instrument_binnacle|gauge_cluster|PRT_Dash",),
        "steering wheel sits just in front of the instrument binnacle / dash",
    ),
    #  -  coolant hoses + fan connect to the engine front (thermostat / water pump).
    InterfaceRule(
        ("PRT_Coolant_Hose|PRT_Radiator_Fan|PRT_Radiator",),
        ("PRT_I4_Engine_Front_Cover|PRT_I4_Engine_Engine_Block|PRT_Water_Pump|PRT_I4_Engine_Crank_Pulley|"
         "PRT_Thermostat",),
        "coolant hoses / fan shroud meet the engine front (pump / thermostat)",
    ),
    #  -  battery + alternator mount in the engine bay on the inner fender / apron.
    InterfaceRule(
        ("PRT_Battery|PRT_Alternator",),
        ("PRT_Inner_Fender|PRT_Apron_Rail|PRT_Strut_Tower|PRT_Front_Rail",),
        "battery / alternator mounted in the engine bay on the inner fender",
    ),
)


def interface_reason(a_name: str, b_name: str, a_sub: str = "", b_sub: str = "") -> str | None:
    """Return a reason when a part-pair overlap is an allowed CAD interface."""
    left = f"{a_sub}:{a_name}"
    right = f"{b_sub}:{b_name}"
    for rule in ALLOWED_INTERFACES:
        if rule.matches(left, right):
            return rule.reason
    return None
