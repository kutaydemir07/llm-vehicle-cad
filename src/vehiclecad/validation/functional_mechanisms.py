"""Whole-vehicle functional mechanism coverage checks.

This is not a dynamics simulation.  It is a CAD release gate that prevents the
assembly from sliding back into "nice exterior shell with decorative blocks".
Each critical vehicle function must have named, emitted mechanism parts.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from vehiclecad.assemblies.product_tree import atomic_part_specs


@dataclass(frozen=True)
class FunctionalMechanismRow:
    status: str
    system: str
    count: int
    requirement: str
    detail: str


REQUIRED_MECHANISMS: tuple[tuple[str, tuple[str, ...], int, str], ...] = (
    (
        "engine_rotating_assembly",
        (
            r"I4_Engine_Crankshaft$",
            r"I4_Engine_Pistons_Rods$",
            r"I4_Engine_Camshafts$",
        ),
        3,
        "crankshaft, pistons/rods, and camshafts are emitted",
    ),
    (
        "engine_services",
        (
            r"I4_Engine_Crankcase_Casting$",
            r"I4_Engine_Front_Cover$",
            r"I4_Engine_Crank_Pulley$",
            r"I4_Engine_Oil_Pan$",
            r"I4_Engine_Oil_Filter$",
            r"I4_Engine_Bellhousing_Starter$",
        ),
        6,
        "block, front accessory drive, lubrication, and starter hardware exist",
    ),
    (
        "air_fuel_delivery",
        (
            r"Fuel_Tank$",
            r"Fuel_Pump$",
            r"Fuel_Filter$",
            r"Fuel_Rail",
            r"Fuel_Feed_Line$",
            r"Fuel_Return_Line$",
            r"Intake_Head_Flange$",
            r"ITB_Runner_[1-4]$",
            r"Throttle_Body_[1-4]$",
            r"Injector_[1-4]$",
            r"Velocity_Stack_[1-4]$",
        ),
        17,
        "tank, pump/filter/lines, rail, ITBs, injectors, and velocity stacks exist",
    ),
    (
        "exhaust_path",
        (
            r"Exhaust_Primary_[1-4]$",
            r"Exhaust_Collector$",
            r"Exhaust_Mid_Pipe$",
            r"Exhaust_Muffler$",
            r"Exhaust_Tip_[12]$",
        ),
        9,
        "four primaries, collector, mid pipe, muffler, and two tips exist",
    ),
    (
        "clutch_release",
        (
            r"Flywheel$",
            r"Pressure_Plate$",
            r"Clutch_Disc$",
            r"Release_Bearing$",
            r"Clutch_Fork$",
            r"Pilot_Bearing$",
            r"Clutch_Slave_Cylinder$",
            r"Release_Fork_Pivot_Hardware$",
        ),
        8,
        "flywheel, friction pack, release bearing/fork, pilot bearing, and slave exist",
    ),
    (
        "manual_gearbox_internal_train",
        (
            r"ManualGearbox_265_Transmission$",
            r"ManualGearbox_265_Input_Shaft$",
            r"ManualGearbox_265_Layshaft$",
            r"ManualGearbox_265_Output_Shaft$",
            r"ManualGearbox_265_Gear_Pair_[1-5]$",
            r"ManualGearbox_265_Reverse_Idler_Gear$",
            r"ManualGearbox_265_Synchro_Hubs$",
            r"ManualGearbox_265_Selector_Rails_Forks$",
            r"ManualGearbox_265_Bearing_Set$",
        ),
        13,
        "gearbox casing plus shafts, five gear pairs, reverse idler, synchros, selectors, and bearings exist",
    ),
    (
        "final_drive",
        (
            r"Rear_LSD_Differential$",
            r"Rear_LSD_Diff_Cover$",
            r"Rear_LSD_Ring_Gear_And_Pinion_Set$",
            r"Rear_LSD_Pinion_Flange$",
            r"Rear_LSD_Output_Flange_[LR]$",
            r"Rear_LSD_Mount_Bushes$",
        ),
        7,
        "LSD housing, cover, ring/pinion, pinion flange, output flanges, and mounts exist",
    ),
    (
        "propshaft",
        (
            r"Propshaft_Flex_Disc$",
            r"Guibo_Bolt_Set$",
            r"Propshaft_Front$",
            r"Propshaft_Rear$",
            r"Propshaft_Slip_Spline$",
            r"Centre_Bearing$",
            r"Centre_Bearing_Rubber_Isolator$",
            r"Centre_Bearing_Bracket$",
            r"U[Jj]oint_(Front|Centre|Rear)$",
            r"Diff_Input_Flange_Bolt_Set$",
        ),
        11,
        "two-piece propshaft with guibo, slip spline, centre bearing, U-joints, and flange bolts exists",
    ),
    (
        "half_shafts",
        (
            r"Half_Shaft_R[LR]$",
            r"CV_Inner_R[LR]$",
            r"CV_Outer_R[LR]$",
            r"CV_Boot_(Inner|Outer)_R[LR]$",
            r"CV_Boot_(Inner|Outer)_Clamp_(Large|Small)_R[LR]$",
            r"CV_Axle_Nut_R[LR]$",
        ),
        20,
        "rear half-shafts include shafts, CVs, boots, clamps, and axle nuts",
    ),
    (
        "brake_system",
        (
            r"Brake_Servo_Booster$",
            r"Brake_Master_Cylinder$",
            r"ABS_Hydraulic_Modulator$",
            r"Brake_Line_",
            r"Brake_Rotor_(FL|FR|RL|RR)$",
            r"Brake_Caliper_(FL|FR|RL|RR)$",
            r"Handbrake_Lever$",
            r"Handbrake_Cable_",
        ),
        18,
        "hydraulic actuation, lines, wheel rotors/calipers, and parking brake exist",
    ),
    (
        "steering_system",
        (
            r"Steering_Rack$",
            r"Steering_Rack_Bar_Pinion_Gear$",
            r"Steering_Column$",
            r"Steering_Wheel_Rim$",
            r"Steering_Wheel_Hub$",
            r"PS_Reservoir$",
        ),
        6,
        "rack housing, rack/pinion gear, column, wheel, and assist reservoir exist",
    ),
    (
        "suspension_system",
        (
            r"Front_ARB$",
            r"Rear_ARB$",
            r"Strut_Foot_F[LR]$",
            r"Strut_Damper_F[LR]$",
            r"Top_Mount_F[LR]$",
            r"Coil_Spring_F[LR]$",
            r"LCA_F[LR]$",
            r"Hub_Knuckle_F[LR]$",
            r"Trailing_Arm_R[LR]$",
            r"Rear_Hub_R[LR]$",
            r"Rear_Coil_Spring_R[LR]$",
            r"Rear_Damper_R[LR]$",
        ),
        22,
        "front/rear suspension includes arms, hubs/uprights, springs, dampers, top mounts, and ARBs",
    ),
    (
        "thermal_cooling",
        (
            r"Radiator$",
            r"Radiator_Fan_Shroud$",
            r"Radiator_Fan_Blades$",
            r"Radiator_Fan_Motor$",
            r"Expansion_Tank$",
            r"Heater_Control_Valve$",
            r"Coolant_Hose_",
        ),
        11,
        "radiator, fan/shroud/motor, expansion tank, heater valve, and coolant hoses exist",
    ),
    (
        "electrical_power_and_control",
        (
            r"Battery$",
            r"Battery_Terminal_",
            r"Alternator$",
            r"Alternator_Pulley$",
            r"Alternator_Output_Stud$",
            r"ECU_Motronic$",
            r"Fuse",
            r"Relay",
            r"Wiring_",
        ),
        24,
        "battery, alternator, ECU/fuse/relay hardware, and wiring branches exist",
    ),
)


def _part_names() -> list[str]:
    return [spec.part_name for spec in atomic_part_specs()]


def audit_functional_mechanisms() -> list[FunctionalMechanismRow]:
    names = _part_names()
    rows: list[FunctionalMechanismRow] = []
    for system, patterns, minimum, requirement in REQUIRED_MECHANISMS:
        matched: set[str] = set()
        for pattern in patterns:
            matched.update(name for name in names if re.search(pattern, name, flags=re.IGNORECASE))
        count = len(matched)
        missing_detail = "ok"
        if count < minimum:
            missing_detail = f"matched only {count}: " + ";".join(sorted(matched)[:16])
        rows.append(
            FunctionalMechanismRow(
                status="pass" if count >= minimum else "fail",
                system=system,
                count=count,
                requirement=f">={minimum}: {requirement}",
                detail=missing_detail,
            )
        )
    return rows
