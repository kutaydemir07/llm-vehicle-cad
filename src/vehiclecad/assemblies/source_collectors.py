"""Cached source groups for atomic detailed-vehicle part files.

The detailed CAD math still lives in focused geometry modules.  This file names
the V-model ownership layer above those modules: system, subsystem, leaf
subassembly, source group, and the connection zones each group participates in.
Atomic part modules call back into these cached groups and expose exactly one
emitted part each.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib import import_module
import re
from typing import Callable

from vehiclecad.core.reference import materials as C

PartTuple = tuple

_ACRONYMS = {
    "ABS",
    "ARB",
    "Mesh",
    "BIW",
    "Classic",
    "CV",
    "DLO",
    "ECU",
    "ModelA",
    "FL",
    "FR",
    "HVAC",
    "ITB",
    "LCA",
    "LSD",
    "SportsCar",
    "PS",
    "RL",
    "RR",
    "I4_Engine",
}

_TOKEN_REPLACEMENTS = {
    "in": "Inner",
    "out": "Outer",
    "r": "Rear",
    "rr": "RR",
    "rl": "RL",
    "fr": "FR",
    "fl": "FL",
    "modela": "ModelA",
    "sportscar": "SportsCar",
    "classic": "Classic",
    "i4": "I4",
    "engine": "Engine",
    "mesh": "Mesh",
    "manualgearbox": "ManualGearbox",
    "mtech1": "MTech1",
}

_SPECIAL_NAMES = {
    ("body_closures", "hood"): "PRT_ModelA_SportsCar_Hood_Outer_Panel",
    ("body_closures", "trunk_lid"): "PRT_ModelA_SportsCar_Decklid_Outer_Panel",
    ("body_closures", "door_L"): "PRT_ModelA_SportsCar_Door_Outer_L",
    ("body_closures", "door_R"): "PRT_ModelA_SportsCar_Door_Outer_R",
    ("steering_wheel", "steering_rim"): "PRT_ModelA_SportsCar_MTech1_Steering_Wheel_Rim",
    ("steering_wheel", "steering_hub"): "PRT_ModelA_SportsCar_MTech1_Steering_Wheel_Hub",
    ("interior_dashboard", "dashboard"): "PRT_ModelA_SportsCar_Dashboard_Shell",
    ("interior_dashboard", "instrument_binnacle"): "PRT_ModelA_SportsCar_Instrument_Binnacle",
    ("interior_dashboard", "gauge_cluster"): "PRT_ModelA_SportsCar_Gauge_Cluster",
    ("interior_dashboard", "centre_vents"): "PRT_ModelA_SportsCar_Centre_Vents",
    ("interior_dashboard", "glovebox"): "PRT_ModelA_SportsCar_Glovebox_Lid",
    ("interior_roll_cage", "roll_cage"): "PRT_ModelA_SportsCar_Roll_Cage",
    ("exterior_frontend", "front_fascia"): "PRT_ModelA_SportsCar_Front_Fascia",
    ("exterior_frontend", "front_bumper_strip"): "PRT_ModelA_SportsCar_Front_Bumper_Rub_Strip",
    ("exterior_frontend", "front_splitter"): "PRT_ModelA_SportsCar_Front_Lower_Splitter",
    ("exterior_frontend", "intake_back"): "PRT_ModelA_SportsCar_Front_Lower_Air_Intake_Back",
    ("exterior_frontend", "intake_mesh"): "PRT_ModelA_SportsCar_Front_Lower_Air_Intake_Mesh",
    ("exterior_rearend", "tail_centre_panel"): "PRT_ModelA_SportsCar_Tail_Centre_Panel",
    ("exterior_rearend", "model_script"): "PRT_ModelA_SportsCar_Decklid_Model_Script",
    ("exterior_rearend", "rear_bumper"): "PRT_ModelA_SportsCar_Rear_Bumper_Cover",
    ("exterior_rearend", "rear_bumper_strip"): "PRT_ModelA_SportsCar_Rear_Bumper_Rub_Strip",
    ("exterior_rearend", "plate_recess"): "PRT_ModelA_SportsCar_Number_Plate_Recess",
    ("exterior_rearend", "number_plate"): "PRT_ModelA_SportsCar_Number_Plate",
    ("exterior_trim", "cowl_vent_back"): "PRT_ModelA_SportsCar_Cowl_Vent_Back",
    ("exterior_trim", "cowl_vent_slats"): "PRT_ModelA_SportsCar_Cowl_Vent_Slats",
    ("exterior_trim", "antenna_mast"): "PRT_ModelA_SportsCar_Antenna_Mast",
    ("exterior_trim", "antenna_base"): "PRT_ModelA_SportsCar_Antenna_Base",
    ("exterior_glazing", "windshield"): "PRT_ModelA_SportsCar_Windshield_Glass",
    ("exterior_glazing", "backlight"): "PRT_ModelA_SportsCar_Backlight_Glass",
}


def _title_token(token: str) -> str:
    if token in {"L", "R"}:
        return token
    replacement = _TOKEN_REPLACEMENTS.get(token.lower())
    if replacement:
        return replacement
    upper = token.upper()
    if upper in _ACRONYMS:
        return upper
    if token.isdigit():
        return token
    return token[:1].upper() + token[1:].lower()


def _title_name(name: str) -> str:
    tokens = [token for token in re.split(r"[^A-Za-z0-9]+", name) if token]
    return "_".join(_title_token(token) for token in tokens)


def _side_from_name(name: str) -> str | None:
    match = re.search(r"_(FL|FR|RL|RR|L|R)$", name)
    return match.group(1) if match else None


def _engineering_name(group_slug: str, raw_name: str) -> str:
    special = _SPECIAL_NAMES.get((group_slug, raw_name))
    if special:
        return special

    if raw_name.startswith("PRT_"):
        return f"PRT_{_title_name(raw_name[4:])}"

    if group_slug == "exterior_frontend":
        lamp = re.match(r"(reflector|bulb|headlamp_lens|headlamp_bezel)_(in|out)_([LR])$", raw_name)
        if lamp:
            kind, position, side = lamp.groups()
            kind_map = {
                "reflector": "Reflector",
                "bulb": "Bulb",
                "headlamp_lens": "Lens",
                "headlamp_bezel": "Bezel",
            }
            pos = "Inner" if position == "in" else "Outer"
            return f"PRT_ModelA_SportsCar_Headlamp_{pos}_{kind_map[kind]}_{side}"
        kidney = re.match(r"kidney_(frame|back|slats)_(\d+)$", raw_name)
        if kidney:
            component, index = kidney.groups()
            return f"PRT_ModelA_SportsCar_Kidney_Grille_{_title_token(component)}_{int(index) + 1}"
        roundel = re.match(r"roundel_(white|blue|band|ring)$", raw_name)
        if roundel:
            return f"PRT_ModelA_SportsCar_Hood_Roundel_{_title_token(roundel.group(1))}"
        fog = re.match(r"foglamp_ring_([LR])$", raw_name)
        if fog:
            return f"PRT_ModelA_SportsCar_Foglamp_Bezel_{fog.group(1)}"
        brake_duct = re.match(r"brake_duct_back_([LR])$", raw_name)
        if brake_duct:
            return f"PRT_ModelA_SportsCar_Brake_Duct_Backing_{brake_duct.group(1)}"
        turn_signal = re.match(r"turn_signal_([LR])$", raw_name)
        if turn_signal:
            return f"PRT_ModelA_SportsCar_Front_Turn_Signal_{turn_signal.group(1)}"
        foglamp = re.match(r"foglamp_([LR])$", raw_name)
        if foglamp:
            return f"PRT_ModelA_SportsCar_Foglamp_{foglamp.group(1)}"

    if group_slug == "exterior_rearend":
        tail = re.match(r"taillamp_(housing|red|amber|reverse)_([LR])$", raw_name)
        if tail:
            component, side = tail.groups()
            return f"PRT_ModelA_SportsCar_Taillamp_{_title_token(component)}_{side}"
        roundel = re.match(r"rear_roundel_(white|blue|band|ring)$", raw_name)
        if roundel:
            return f"PRT_ModelA_SportsCar_Decklid_Roundel_{_title_token(roundel.group(1))}"
        rear_reflector = re.match(r"rear_reflector_([LR])$", raw_name)
        if rear_reflector:
            return f"PRT_ModelA_SportsCar_Rear_Reflector_{rear_reflector.group(1)}"

    if group_slug == "exterior_trim":
        side = _side_from_name(raw_name)
        base = raw_name.rsplit("_", 1)[0] if side in {"L", "R"} else raw_name
        base_map = {
            "mirror": "Door_Mirror_Housing",
            "mirror_glass": "Door_Mirror_Glass",
            "door_handle": "Door_Handle",
            "side_rub_strip_front_fender": "Side_Rub_Strip_Front_Fender",
            "side_rub_strip_door": "Side_Rub_Strip_Door",
            "side_rub_strip_quarter": "Side_Rub_Strip_Quarter",
            "side_rub_strip_rear_quarter": "Side_Rub_Strip_Rear_Quarter",
            "b_pillar_cover": "B_Pillar_Cover",
            "dlo_belt": "DLO_Belt_Trim",
            "drip_rail": "Drip_Rail",
            "wiper": "Wiper_Arm_Blade",
        }
        mapped = base_map.get(base)
        if mapped and side:
            return f"PRT_ModelA_SportsCar_{mapped}_{side}"

    if group_slug == "exterior_glazing":
        side = _side_from_name(raw_name)
        if raw_name.startswith("door_glass_") and side:
            return f"PRT_ModelA_SportsCar_Door_Glass_{side}"
        if raw_name.startswith("quarter_glass_") and side:
            return f"PRT_ModelA_SportsCar_Quarter_Glass_{side}"

    if group_slug.startswith("corner_"):
        side = raw_name.rsplit("_", 1)[-1]
        base = raw_name[: -(len(side) + 1)]
        base_map = {
            "bearing_hub": "Wheel_Bearing_Hub",
            "brake_rotor": "Brake_Rotor",
            "brake_caliper": "Brake_Caliper",
            "tire": "Tire",
            "rim_barrel": "Mesh_Rim_Barrel",
            "rim_face": "Mesh_Rim_Face",
            "rim_lip": "Mesh_Rim_Lip",
            "hub": "Wheel_Centre_Hub",
            "lug_bolts": "Wheel_Lug_Bolts",
            "cap": "Wheel_Roundel_Cap",
            "cap_white": "Wheel_Roundel_Cap_White",
            "cap_blue": "Wheel_Roundel_Cap_Blue",
            "cap_band": "Wheel_Roundel_Cap_Band",
            "cap_ring": "Wheel_Roundel_Cap_Ring",
        }
        mapped = base_map.get(base)
        if mapped:
            return f"PRT_ModelA_SportsCar_{mapped}_{side}"

    prefix = "ModelA_SportsCar_" if group_slug.startswith(("body_closures", "exterior", "interior", "corner")) else ""
    return f"PRT_{prefix}{_title_name(raw_name)}"


def _rename_part(group_slug: str, part: PartTuple) -> PartTuple:
    raw_name = part[2]
    detailed_name = _engineering_name(group_slug, raw_name)
    if detailed_name == raw_name:
        return part
    if len(part) == 4:
        shape, color, _name, marker = part
        return shape, color, detailed_name, marker
    shape, color, _name = part[:3]
    return shape, color, detailed_name


@dataclass(frozen=True)
class SourceGroup:
    slug: str
    system_name: str
    subsystem_name: str
    subassembly_name: str
    module_path: str
    function_name: str = "parts"
    args: tuple = ()
    connections: tuple[str, ...] = ()


def _corner_fl():
    from vehiclecad.parts.exterior.detail import wheels

    return wheels.corner(C.AXLE_F, 1, C.TRACK_F)


def _corner_fr():
    from vehiclecad.parts.exterior.detail import wheels

    return wheels.corner(C.AXLE_F, -1, C.TRACK_F)


def _corner_rl():
    from vehiclecad.parts.exterior.detail import wheels

    return wheels.corner(C.AXLE_R, 1, C.TRACK_R)


def _corner_rr():
    from vehiclecad.parts.exterior.detail import wheels

    return wheels.corner(C.AXLE_R, -1, C.TRACK_R)


SOURCE_GROUPS: tuple[SourceGroup, ...] = (
    SourceGroup("body_firewall", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1110_Firewall_Bulkheads", "vehiclecad.parts.body.structure.firewall", connections=("CONN_BIW_ENGINE_BAY_REAR", "CONN_BIW_CABIN_FRONT")),
    SourceGroup("body_floorpan", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1120_Floorpan", "vehiclecad.parts.body.structure.floorpan", connections=("CONN_BIW_CABIN_FLOOR", "CONN_CHASSIS_UNDERBODY_MOUNTS")),
    SourceGroup("body_c_pillars", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1130_C_Pillar_Conversion", "vehiclecad.parts.body.structure.pillar", connections=("CONN_BIW_ROOF_SIDE", "CONN_BIW_REAR_QUARTER")),
    SourceGroup("body_pillars", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1140_A_B_Pillars", "vehiclecad.parts.body.structure.pillars", connections=("CONN_BIW_DOOR_APERTURES", "CONN_BIW_ROOF_SIDE")),
    SourceGroup("body_rockers", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1150_Rocker_Rails", "vehiclecad.parts.body.structure.rocker", connections=("CONN_BIW_DOOR_APERTURES", "CONN_CHASSIS_SIDE_MOUNTS")),
    SourceGroup("body_roof_panel", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1160_Roof_Outer", "vehiclecad.parts.body.structure.roof", connections=("CONN_BIW_ROOF_SIDE", "CONN_GLAZING_UPPER")),
    SourceGroup("body_roof_structure", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1170_Roof_Headers_Bows", "vehiclecad.parts.body.structure.roof_structure", connections=("CONN_BIW_ROOF_SIDE", "CONN_INTERIOR_HEADLINER")),
    SourceGroup("body_strut_towers_shell", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1180_Strut_Tower_Shells", "vehiclecad.parts.body.structure.strut", connections=("CONN_FRONT_SUSPENSION_TOP_MOUNTS", "CONN_REAR_SUSPENSION_TOP_MOUNTS")),
    SourceGroup("body_strut_top_plates", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1190_Strut_Top_Plates", "vehiclecad.parts.body.structure.strut_towers", connections=("CONN_FRONT_SUSPENSION_TOP_MOUNTS", "CONN_BODY_BRACE_FRONT")),
    SourceGroup("body_wheel_tubs", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1195_Wheel_Tubs", "vehiclecad.parts.body.structure.wheel_tub", connections=("CONN_WHEELHOUSE_FRONT", "CONN_WHEELHOUSE_REAR")),
    SourceGroup("body_engine_bay", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1196_Engine_Bay_Panels", "vehiclecad.parts.body.structure.engine_bay", connections=("CONN_ENGINE_BAY_FRONT", "CONN_POWERTRAIN_MOUNTS")),
    SourceGroup("body_trunk", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1197_Trunk_Structure", "vehiclecad.parts.body.structure.trunk", connections=("CONN_REAR_COMPARTMENT", "CONN_FUEL_TANK_ZONE")),
    SourceGroup("body_outer_panels", "ASM_1000_Body_Structure", "ASM_1100_Body_In_White", "ASM_1198_Outer_Sheet_Metal_Panels", "vehiclecad.parts.body.structure.body", "body_parts", connections=("CONN_BIW_OUTER_SKIN", "CONN_EXTERIOR_TRIM_CLIPS")),
    SourceGroup("body_closures", "ASM_1200_Closures", "ASM_1210_Movable_Closure_Panels", "ASM_1211_Hood_Doors_Decklid", "vehiclecad.parts.body.structure.body", "closure_parts", connections=("CONN_BIW_SHUT_LINES", "CONN_CLOSURE_HINGES_LATCHES")),
    SourceGroup("chassis_crossmembers", "ASM_2000_Chassis", "ASM_2100_Underbody_Frames", "ASM_2110_Crossmembers_And_Ties", "vehiclecad.parts.chassis.structure.crossmembers", connections=("CONN_BIW_UNDERBODY", "CONN_POWERTRAIN_REAR_SUPPORT")),
    SourceGroup("chassis_rear_subframe", "ASM_2000_Chassis", "ASM_2200_Subframes", "ASM_2210_Rear_Subframe", "vehiclecad.parts.chassis.structure.subframe", connections=("CONN_REAR_SUSPENSION_PICKUPS", "CONN_REAR_DIFF_MOUNTS")),
    SourceGroup("suspension_antiroll_bars", "ASM_3000_Suspension", "ASM_3100_Roll_Control", "ASM_3110_Antiroll_Bars", "vehiclecad.parts.suspension.detail.antiroll_bars", connections=("CONN_CHASSIS_ARB_MOUNTS", "CONN_SUSPENSION_LINKS")),
    SourceGroup("suspension_front_macpherson", "ASM_3000_Suspension", "ASM_3200_Front_Suspension", "ASM_3210_MacPherson_Corner_Hardparts", "vehiclecad.parts.suspension.detail.front_macpherson", connections=("CONN_FRONT_SUSPENSION_TOP_MOUNTS", "CONN_FRONT_HUB_CORNERS")),
    SourceGroup("suspension_rear_semitrailing", "ASM_3000_Suspension", "ASM_3300_Rear_Suspension", "ASM_3310_Semi_Trailing_Arm_Corner_Hardparts", "vehiclecad.parts.suspension.detail.rear_semitrailing", connections=("CONN_REAR_SUBFRAME_PICKUPS", "CONN_REAR_HUB_CORNERS")),
    SourceGroup("steering_rack", "ASM_4000_Steering", "ASM_4100_Steering_Gear", "ASM_4110_Rack_And_Tie_Rods", "vehiclecad.parts.steering.detail.steering_rack", connections=("CONN_FRONT_SUBFRAME", "CONN_STEERING_COLUMN_LOWER")),
    SourceGroup("steering_column", "ASM_4000_Steering", "ASM_4200_Steering_Controls", "ASM_4210_Column", "vehiclecad.parts.steering.detail.steering_column", connections=("CONN_DASH_CROSSCAR", "CONN_STEERING_RACK_INPUT")),
    SourceGroup("steering_power_assist", "ASM_4000_Steering", "ASM_4300_Power_Assist", "ASM_4310_Power_Steering_Reservoir", "vehiclecad.parts.steering.detail.power_steering", connections=("CONN_ENGINE_BAY_ACCESSORY", "CONN_STEERING_HYDRAULICS")),
    SourceGroup("steering_wheel", "ASM_4000_Steering", "ASM_4200_Steering_Controls", "ASM_4220_Steering_Wheel", "vehiclecad.parts.steering.detail.steering", connections=("CONN_STEERING_COLUMN_UPPER", "CONN_DRIVER_INTERFACE")),
    SourceGroup("brakes_booster_master", "ASM_5000_Brakes", "ASM_5100_Hydraulic_Actuation", "ASM_5110_Booster_Master_Cylinder", "vehiclecad.parts.brakes.detail.brake_booster_master", connections=("CONN_FIREWALL_PEDAL_BOX", "CONN_BRAKE_LINE_MANIFOLD")),
    SourceGroup("brakes_hard_lines", "ASM_5000_Brakes", "ASM_5200_Hydraulic_Routing", "ASM_5210_Brake_Hard_Lines", "vehiclecad.parts.brakes.detail.brake_lines", connections=("CONN_BRAKE_MASTER", "CONN_ABS_MODULATOR", "CONN_BRAKE_CORNERS")),
    SourceGroup("brakes_handbrake", "ASM_5000_Brakes", "ASM_5300_Parking_Brake", "ASM_5310_Lever_And_Cables", "vehiclecad.parts.brakes.detail.handbrake_assembly", connections=("CONN_INTERIOR_TUNNEL", "CONN_REAR_BRAKE_CORNERS")),
    SourceGroup("powertrain_cylinder_head", "ASM_6000_Powertrain", "ASM_6100_Engine", "ASM_6110_Cylinder_Head_And_Cover", "vehiclecad.parts.powertrain.detail.cylinder_head", connections=("CONN_ENGINE_BLOCK_DECK", "CONN_INTAKE_EXHAUST_PORTS")),
    SourceGroup("powertrain_engine_block", "ASM_6000_Powertrain", "ASM_6100_Engine", "ASM_6120_Crankcase_And_Accessories", "vehiclecad.parts.powertrain.detail.engine", connections=("CONN_ENGINE_MOUNTS", "CONN_TRANSMISSION_BELLHOUSING")),
    SourceGroup("powertrain_engine_internals", "ASM_6000_Powertrain", "ASM_6100_Engine", "ASM_6130_Rotating_And_Valve_Train", "vehiclecad.parts.powertrain.detail.engine_internals", connections=("CONN_CRANKCASE_INTERNALS", "CONN_CYLINDER_HEAD_TIMING")),
    SourceGroup("powertrain_exhaust", "ASM_6000_Powertrain", "ASM_6300_Air_And_Exhaust", "ASM_6310_Exhaust_Path", "vehiclecad.parts.powertrain.detail.exhaust", connections=("CONN_EXHAUST_PORTS", "CONN_UNDERBODY_HANGERS")),
    SourceGroup("powertrain_fuel_system", "ASM_6000_Powertrain", "ASM_6400_Fuel_Storage_And_Delivery", "ASM_6410_Tank_Pump_Filter_Lines", "vehiclecad.parts.powertrain.detail.fuel_system", connections=("CONN_FUEL_TANK_ZONE", "CONN_ENGINE_FUEL_RAIL")),
    SourceGroup("powertrain_intake", "ASM_6000_Powertrain", "ASM_6300_Air_And_Exhaust", "ASM_6320_Intake_Path", "vehiclecad.parts.powertrain.detail.intake", connections=("CONN_CYLINDER_HEAD_INTAKE_PORTS", "CONN_FRONT_AIRBOX_ZONE")),
    SourceGroup("powertrain_transmission", "ASM_6000_Powertrain", "ASM_6500_Transmission", "ASM_6510_Gearbox", "vehiclecad.parts.powertrain.detail.transmission", connections=("CONN_ENGINE_BELLHOUSING", "CONN_DRIVELINE_PROPSHAFT_FRONT")),
    SourceGroup("driveline_clutch", "ASM_6200_Driveline", "ASM_6210_Clutch", "ASM_6211_Flywheel_Pressure_Disc", "vehiclecad.parts.powertrain.detail.clutch_assembly", connections=("CONN_ENGINE_CRANK_FLANGE", "CONN_TRANSMISSION_INPUT")),
    SourceGroup("driveline_differential", "ASM_6200_Driveline", "ASM_6220_Final_Drive", "ASM_6221_Rear_Differential", "vehiclecad.parts.powertrain.detail.differential", connections=("CONN_REAR_SUBFRAME_DIFF_MOUNTS", "CONN_HALF_SHAFT_INNERS")),
    SourceGroup("driveline_propshaft", "ASM_6200_Driveline", "ASM_6230_Propshaft", "ASM_6231_Two_Piece_Propshaft", "vehiclecad.parts.powertrain.detail.driveshaft", connections=("CONN_TRANSMISSION_OUTPUT", "CONN_DIFFERENTIAL_INPUT")),
    SourceGroup("driveline_half_shafts", "ASM_6200_Driveline", "ASM_6240_Half_Shafts", "ASM_6241_Rear_CV_Shafts", "vehiclecad.parts.powertrain.detail.half_shafts", connections=("CONN_DIFFERENTIAL_OUTPUTS", "CONN_REAR_HUB_CORNERS")),
    SourceGroup("thermal_cooling", "ASM_7000_Thermal_HVAC", "ASM_7100_Engine_Cooling", "ASM_7110_Radiator_Fan_Hoses", "vehiclecad.parts.thermal.hvac_detail.cooling_system", connections=("CONN_FRONT_RADIATOR_SUPPORT", "CONN_ENGINE_COOLANT_PORTS")),
    SourceGroup("thermal_hvac", "ASM_7000_Thermal_HVAC", "ASM_7200_Cabin_HVAC", "ASM_7210_Heater_Box_Blower", "vehiclecad.parts.thermal.hvac_detail.hvac_blower", connections=("CONN_FIREWALL_HVAC_OPENINGS", "CONN_DASH_AIR_DISTRIBUTION")),
    SourceGroup("electrical_battery_alternator", "ASM_8000_Electrical", "ASM_8100_Power_Generation_Storage", "ASM_8110_Battery_Alternator", "vehiclecad.parts.electrical.detail.battery_alternator", connections=("CONN_ENGINE_ACCESSORY_DRIVE", "CONN_MAIN_POWER_BUS")),
    SourceGroup("electrical_ecu_fusebox", "ASM_8000_Electrical", "ASM_8200_Control_And_Protection", "ASM_8210_ECU_Fusebox", "vehiclecad.parts.electrical.detail.ecu_fusebox", connections=("CONN_FIREWALL_ELECTRICAL", "CONN_ENGINE_LOOM")),
    SourceGroup("electrical_wiring", "ASM_8000_Electrical", "ASM_8300_Wiring_Routing", "ASM_8310_Main_Looms", "vehiclecad.parts.electrical.detail.wiring_harness", connections=("CONN_ECU_FUSEBOX", "CONN_BODY_POWER_CONSUMERS")),
    SourceGroup("interior_soft_trim", "ASM_9000_Interior", "ASM_9100_Soft_Trim", "ASM_9110_Carpets_Headliner", "vehiclecad.parts.interior.detail.carpets_headliner", connections=("CONN_BIW_CABIN_FLOOR", "CONN_BIW_ROOF_INNER")),
    SourceGroup("interior_console", "ASM_9000_Interior", "ASM_9200_Cockpit_Furniture", "ASM_9210_Centre_Console", "vehiclecad.parts.interior.detail.center_console", connections=("CONN_TUNNEL_TOP", "CONN_DRIVER_CONTROLS")),
    SourceGroup("interior_dashboard", "ASM_9000_Interior", "ASM_9200_Cockpit_Furniture", "ASM_9220_Dashboard_Instruments", "vehiclecad.parts.interior.detail.dashboard", connections=("CONN_FIREWALL_COWL", "CONN_ELECTRICAL_INSTRUMENT_LOOM")),
    SourceGroup("interior_door_panels", "ASM_9000_Interior", "ASM_9300_Door_Trim", "ASM_9310_Door_Cards", "vehiclecad.parts.interior.detail.door_panels", connections=("CONN_CLOSURE_DOORS", "CONN_OCCUPANT_TOUCH_POINTS")),
    SourceGroup("interior_pedal_box", "ASM_9000_Interior", "ASM_9400_Driver_Controls", "ASM_9410_Pedal_Box", "vehiclecad.parts.interior.detail.pedal_box", connections=("CONN_FIREWALL_PEDAL_BOX", "CONN_BRAKE_BOOSTER_PUSHROD")),
    SourceGroup("interior_roll_cage", "ASM_9000_Interior", "ASM_9500_Safety_Cage", "ASM_9510_Roll_Cage", "vehiclecad.parts.interior.detail.roll_cage", connections=("CONN_BIW_CAGE_FEET", "CONN_OCCUPANT_SURVIVAL_CELL")),
    SourceGroup("interior_front_seats", "ASM_9000_Interior", "ASM_9600_Seating", "ASM_9610_Front_Seats", "vehiclecad.parts.interior.detail.seats_front", connections=("CONN_FLOOR_SEAT_RAILS", "CONN_OCCUPANT_H_POINTS")),
    SourceGroup("interior_rear_seat", "ASM_9000_Interior", "ASM_9600_Seating", "ASM_9620_Rear_Bench", "vehiclecad.parts.interior.detail.seats_rear", connections=("CONN_REAR_CABIN_FLOOR", "CONN_REAR_BULKHEAD")),
    SourceGroup("exterior_flares", "ASM_10000_Exterior", "ASM_10100_Aero_Body_Kit", "ASM_10110_Box_Flares", "vehiclecad.parts.exterior.detail.flare", connections=("CONN_BIW_WHEEL_ARCHES", "CONN_EXTERIOR_PAINTED_PANELS")),
    SourceGroup("exterior_side_skirts", "ASM_10000_Exterior", "ASM_10100_Aero_Body_Kit", "ASM_10120_Side_Skirts", "vehiclecad.parts.exterior.detail.skirt", connections=("CONN_BIW_ROCKER_OUTER", "CONN_EXTERIOR_LOWER_TRIM")),
    SourceGroup("exterior_rear_deck", "ASM_10000_Exterior", "ASM_10100_Aero_Body_Kit", "ASM_10130_Rear_Deck_Panel", "vehiclecad.parts.exterior.detail.deck", connections=("CONN_TRUNK_LID_OUTER", "CONN_REAR_WING_BASE")),
    SourceGroup("exterior_rear_wing", "ASM_10000_Exterior", "ASM_10100_Aero_Body_Kit", "ASM_10140_Rear_Wing", "vehiclecad.parts.exterior.detail.wing", connections=("CONN_REAR_DECK", "CONN_AERO_LOAD_PATH")),
    SourceGroup("exterior_frontend", "ASM_10000_Exterior", "ASM_10200_Front_End", "ASM_10210_Fascia_Grille_Lamps", "vehiclecad.parts.exterior.detail.frontend", connections=("CONN_FRONT_BODY_FACE", "CONN_FRONT_LIGHTING_LOOM")),
    SourceGroup("exterior_rearend", "ASM_10000_Exterior", "ASM_10300_Rear_End", "ASM_10310_Bumper_Tail_Lamps", "vehiclecad.parts.exterior.detail.rearend", connections=("CONN_REAR_BODY_FACE", "CONN_REAR_LIGHTING_LOOM")),
    SourceGroup("exterior_trim", "ASM_10000_Exterior", "ASM_10400_Exterior_Trim", "ASM_10410_Mirrors_Mouldings_Wipers", "vehiclecad.parts.exterior.detail.trim", connections=("CONN_BODY_CLIP_POINTS", "CONN_DRIVER_VISIBILITY")),
    SourceGroup("exterior_glazing", "ASM_10500_Glazing", "ASM_10510_Glass_Set", "ASM_10511_Windscreen_Side_Backlight", "vehiclecad.parts.exterior.detail.glazing", connections=("CONN_BIW_WINDOW_FLANGES", "CONN_WEATHERSTRIPS")),
    SourceGroup("fasteners_mounts_brackets", "ASM_14000_Fasteners_Brackets", "ASM_14100_Mounts_And_Brackets", "ASM_14110_Engine_Trans_Body_Mounts", "vehiclecad.parts.fasteners.brackets_interfaces.brackets_mounts", connections=("CONN_ENGINE_MOUNTS", "CONN_BODY_INTERFACE_MOUNTS")),
    SourceGroup("corner_fl", "ASM_15000_Road_Corners", "ASM_15100_Front_Corners", "ASM_Corner_FL", "vehiclecad.assemblies.source_collectors", "_corner_fl", connections=("CONN_FRONT_LEFT_HUB", "CONN_FRONT_LEFT_BRAKE")),
    SourceGroup("corner_fr", "ASM_15000_Road_Corners", "ASM_15100_Front_Corners", "ASM_Corner_FR", "vehiclecad.assemblies.source_collectors", "_corner_fr", connections=("CONN_FRONT_RIGHT_HUB", "CONN_FRONT_RIGHT_BRAKE")),
    SourceGroup("corner_rl", "ASM_15000_Road_Corners", "ASM_15200_Rear_Corners", "ASM_Corner_RL", "vehiclecad.assemblies.source_collectors", "_corner_rl", connections=("CONN_REAR_LEFT_HUB", "CONN_REAR_LEFT_BRAKE")),
    SourceGroup("corner_rr", "ASM_15000_Road_Corners", "ASM_15200_Rear_Corners", "ASM_Corner_RR", "vehiclecad.assemblies.source_collectors", "_corner_rr", connections=("CONN_REAR_RIGHT_HUB", "CONN_REAR_RIGHT_BRAKE")),
)


def source_groups() -> tuple[SourceGroup, ...]:
    return SOURCE_GROUPS


def source_group(slug: str) -> SourceGroup:
    for group in SOURCE_GROUPS:
        if group.slug == slug:
            return group
    raise KeyError(f"unknown source group: {slug}")


def _builder(group: SourceGroup) -> Callable:
    module = import_module(group.module_path)
    return getattr(module, group.function_name)


@lru_cache(maxsize=None)
def group_parts(slug: str) -> tuple[PartTuple, ...]:
    group = source_group(slug)
    return tuple(_rename_part(slug, part) for part in _builder(group)(*group.args))


def atomic_part(slug: str, part_name: str, part_index: int = 0) -> PartTuple:
    matches = [part for part in group_parts(slug) if part[2] == part_name]
    if part_index >= len(matches):
        raise KeyError(f"{slug}:{part_name}[{part_index}] not found")
    return matches[part_index]


def flat_source_parts() -> list[PartTuple]:
    out: list[PartTuple] = []
    for group in SOURCE_GROUPS:
        out.extend(group_parts(group.slug))
    return out
