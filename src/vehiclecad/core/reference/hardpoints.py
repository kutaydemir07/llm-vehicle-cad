"""PRT_Master_Skeleton_Kinematics - the mathematical backbone of the assembly.

This module holds **no visible geometry**.  It is the single source of truth for
every hardpoint coordinate, datum plane, and parametric relationship in the
ASM_Classic_ModelA_SportsCar_MASTER assembly.  Every sub-assembly imports from here rather
than hard-coding positions.

All coordinates are in the vehicle frame defined in ``common.py``:
    +X = rearward (0 at front bumper tip)
    +Y = leftward (0 = vehicle centreline)
    +Z = upward   (0 = ground plane)
    Units: millimetres.

Real ModelA SportsCar data (from source-backed online reference checks):
    Wheelbase:  2562 mm
    Track F/R:  1412 / 1433 mm
    OAL/OAW/OAH: 4345 / 1680 / 1370 mm
    Curb weight: 1200 kg (2645 lb)
    Weight dist: 53 F / 47 R
    Front susp:  MacPherson strut, offset coil spring, lower A-arm
    Rear susp:   Semi-trailing arm, separate coil spring & damper
    Engine:      I4_EngineB23 - 2302 cc inline-4, iron block / alloy head
    Transmission: ManualGearbox 265/5 dogleg, 3.25 final drive, 25% LSD
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Tuple
import math

#  -  type alias  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -
Vec3 = Tuple[float, float, float]


# ------------------------------------------------------------------------
#  DESIGN TABLE  - top-level dimensions, adjustable as parameters
# ------------------------------------------------------------------------
@dataclass
class DesignTable:
    """Parametric master dimensions.  Change these and the whole car updates."""
    wheelbase:      float = 2562.0       # mm, front axle - rear axle
    track_front:    float = 1412.0
    track_rear:     float = 1433.0
    overall_length: float = 4345.0
    overall_width:  float = 1680.0
    overall_height: float = 1370.0
    ride_height:    float = 140.0        # ground - lowest body point (splitter)
    front_overhang: float = 810.0        # front bumper - front axle
    rear_overhang:  float = 973.0        # rear axle - rear bumper
    tire_diameter:  float = 600.0        # 205/55 R15
    tire_width:     float = 205.0
    curb_weight_kg: float = 1200.0
    weight_dist_f:  float = 0.53         # fraction on front axle

    # derived
    @property
    def axle_front_x(self) -> float:
        return self.front_overhang

    @property
    def axle_rear_x(self) -> float:
        return self.front_overhang + self.wheelbase

    @property
    def tire_radius(self) -> float:
        return self.tire_diameter / 2.0

    @property
    def wheel_centre_z(self) -> float:
        return self.tire_radius

    @property
    def cg_x(self) -> float:
        """Longitudinal CG from front bumper."""
        return self.axle_front_x + self.wheelbase * (1.0 - self.weight_dist_f)

    @property
    def cg_z(self) -> float:
        """Approximate CG height - ~460 mm for an ModelA SportsCar."""
        return 460.0


# singleton - import and read from anywhere
DT = DesignTable()


# ------------------------------------------------------------------------
#  DATUM PLANES  - named reference planes (origin point + normal)
# ------------------------------------------------------------------------
DATUMS: Dict[str, Tuple[Vec3, Vec3]] = {
    # (point_on_plane, outward_normal)
    "ground":          ((0, 0, 0),          (0, 0, 1)),
    "centreline":      ((0, 0, 0),          (0, 1, 0)),
    "front_axle":      ((DT.axle_front_x, 0, 0), (1, 0, 0)),
    "rear_axle":       ((DT.axle_rear_x,  0, 0), (1, 0, 0)),
    "firewall":        ((1220, 0, 0),       (1, 0, 0)),    # engine bay / cabin
    "cowl":            ((1500, 0, 0),       (1, 0, 0)),    # base of windshield
    "windshield":      ((1610, 0, 965),     (0.42, 0, 0.91)),  # raked
    "backlight":       ((3070, 0, 1108),    (-0.64, 0, 0.77)),
    "rear_bulkhead":   ((3450, 0, 0),       (1, 0, 0)),    # trunk / cabin
    "front_bumper":    ((0, 0, 0),          (-1, 0, 0)),
    "rear_bumper":     ((DT.overall_length, 0, 0), (1, 0, 0)),
}


# ------------------------------------------------------------------------
#  SUSPENSION HARDPOINTS  - per-side, LEFT side (+Y).  Mirror for RIGHT.
# ------------------------------------------------------------------------

#  -  Front MacPherson  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -
#  The ModelA front suspension: MacPherson strut with offset coil spring,
#  lower A-arm (control arm), and anti-roll bar.
#  Hardpoints are for the LEFT side; mirror Y for the RIGHT.
FRONT_SUSP: Dict[str, Vec3] = {
    # Lower control arm
    "lca_front_pivot":    (660,  320, 218),    # front bushing (body mount)
    "lca_rear_pivot":     (960,  320, 218),    # rear bushing (offset caster)
    "lca_outer_balljoint": (810, 656, 248),    # ball joint at knuckle

    # Strut
    "strut_lower":        (810,  620, 286),    # strut-to-knuckle attachment (inboard
                                               # of the tyre inner face ~602 & disc, so
                                               # the strut tube clears the wheel)
    "strut_upper_mount":  (810,  530, 952),    # top mount in strut tower
    "spring_lower_perch": (810,  545, 455),    # coil spring base, above rotor sweep
    "spring_upper_perch": (810,  520, 880),    # coil spring top

    # Steering
    "tie_rod_inner":      (780,  320, 230),    # rack end, low and outboard of oil pan
    "tie_rod_outer":      (720,  632, 330),    # forward/inboard steering-arm lug at knuckle

    # Anti-roll bar
    "arb_bush_body":      (650,  300, 135),    # low front D-bush, ahead of rack
    "arb_end_link":       (845,  380, 224),    # drop-link tab on the LCA forward
                                               # arm - inboard and low, well clear
                                               # of the strut foot/knuckle corner

    # Wheel centre
    "wheel_centre":       (DT.axle_front_x, DT.track_front / 2, DT.tire_radius),
}

#  -  Steering rack / column / wheel  -  -  -  -  -  -  -  -  -  -  -  -  - -
#  The rack is kept low under the I4_Engine oil-pan envelope, with its pinion on the
#  left side of the housing.  Tie rods run from rack inner pivots to the
#  MacPherson knuckle steering arms.  Column points are a mated chain from
#  steering wheel hub -> firewall bearing -> lower U-joint -> rack pinion.  The
#  wheel sits below and behind the cowl upper panel, leaving body-structure
#  clearance while staying aligned with the driver binnacle.
STEERING: Dict[str, Vec3] = {
    "rack_centre":        (780,    0, 220),
    "rack_inner_L":       (780,  320, 230),
    "rack_inner_R":       (780, -320, 230),
    "tie_rod_outer_L":    FRONT_SUSP["tie_rod_outer"],
    "tie_rod_outer_R":    (FRONT_SUSP["tie_rod_outer"][0], -FRONT_SUSP["tie_rod_outer"][1], FRONT_SUSP["tie_rod_outer"][2]),
    "pinion_base":        (760,  240, 220),
    "pinion_input":       (760,  240, 305),
    "lower_u_joint":      (895,  292, 350),
    "firewall_bearing":   (1220, 340, 550),
    "upper_u_joint":      (1552, 340, 674),
    "wheel_hub":          (1880, 340, 850),
    "wheel_axis_tip":     (1963, 340, 906),
}

#  -  Brake hydraulic / parking brake routing  -  -  -  -  -  -  -  -  -  -
#  ASM_5000 owns the actuation hardware and hydraulic/parking-brake routing.
#  Wheel-end rotors and calipers are owned by ASM_15000_Road_Corners; these
#  endpoints are the mated hose/cable targets for that corner hardware.
BRAKES: Dict[str, Vec3] = {
    "booster_centre":     (1115, 365, 650),
    "master_base":        (934, 365, 650),
    "master_rear":        (1060, 365, 650),    # master flange seats on the booster
                                               # front cap (x1065), not inside the can
    "reservoir_centre":   (1005, 365, 733),    # grommets on the body, clear of the
                                               # booster front cap behind it
    "abs_unit":           (1006, 290, 585),
    "abs_inlet":          (996, 322, 622),
    "abs_outlet_front":   (1085, 314, 598),    # front-circuit exit, dropped below
                                               # the booster shell so its lines clear it
    "abs_outlet_rear":    (1085, 286, 575),
    "firewall_tee":       (1220, 280, 555),
    "rear_tee":           (3270,   0, 255),
    "front_left_caliper": (928,  664, 330),
    "front_right_caliper": (928, -664, 330),
    "rear_left_caliper":  (3485,  686, 320),
    "rear_right_caliper": (3485, -686, 320),
    "handbrake_pivot":    (1848,   68, 520),
    "handbrake_grip":     (1930,   82, 690),
    "handbrake_equalizer": (1880,  0, 468),
}

#  -  Rear Semi-Trailing Arm  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  - -
#  The ModelA rear: semi-trailing arm with separate coil spring and damper,
#  mounted on a subframe.
REAR_SUSP: Dict[str, Vec3] = {
    # Trailing arm pivots (two bushings on the subframe)
    "sta_inner_pivot":    (2950, 280, 310),    # inner (forward) pivot
    "sta_outer_pivot":    (2950, 520, 310),    # outer (rearward) pivot

    # Hub
    "hub_centre":         (DT.axle_rear_x, DT.track_rear / 2, DT.tire_radius),

    # STOCK ModelA layout: the coil spring and the damper are SEPARATE and live at
    # different stations on the trailing arm (this is how the real car is built,
    # not a coilover).  The fat coil sits forward/upright in a body spring pocket;
    # the telescopic damper is rearward by the hub, rising near-vertically to the
    # body rear shock tower.  Keeping ~140 mm of X between the two axes guarantees
    # the spring OD and the shock tube never share space.
    "spring_lower":       (3250, 540, 360),    # coil lower seat on the trailing arm
    "spring_upper":       (3262, 540, 648),    # coil upper seat in the body pocket
    "damper_lower":       (3392, 566, 332),    # shock lower eye on the arm, by hub
    "damper_upper":       (3372, 528, 690),    # shock top mount at body shock tower

    # Anti-roll bar
    "arb_bush_body":      (3505, 300, 150),    # rear stabilizer bushing
    "arb_end_link":       (3400, 632, 332),    # tab on a post near the hub, rearward
                                               # and outboard of the damper so the bar
                                               # never crosses the shock or spar, but
                                               # inboard of the brake rotor sweep

    # Wheel centre
    "wheel_centre":       (DT.axle_rear_x, DT.track_rear / 2, DT.tire_radius),
}


# ------------------------------------------------------------------------
#  ENGINE / POWERTRAIN HARDPOINTS
# ------------------------------------------------------------------------
POWERTRAIN: Dict[str, Vec3] = {
    # I4_Engine engine - inline-4, longitudinally mounted, RWD
    "engine_front":       (380, 0, 520),       # front face of block
    "engine_rear":        (1000, 0, 520),      # flywheel / bellhousing face
    "engine_cg":          (690, 0, 540),       # centre of mass
    "engine_mount_L":     (580, 260, 380),     # left engine mount
    "engine_mount_R":     (580, -260, 380),    # right engine mount
    "engine_mount_rear":  (980, 0, 420),       # rear / trans mount

    # Valve cover top (for hood clearance)
    "valve_cover_top":    (690, 48, 790),      # highest point

    # Intake (individual throttle bodies - left side)
    "intake_plenum":      (690, 340, 700),     # plenum box centre
    "intake_runner_1":    (480, 280, 680),
    "intake_runner_4":    (900, 280, 680),

    # Exhaust (right side, tubular 4-1 header)
    "exhaust_port_1":     (480, -220, 560),
    "exhaust_port_4":     (900, -220, 560),
    "exhaust_collector":  (750, -340, 420),    # 4-1 merge
    "exhaust_exit":       (4300, -300, 280),   # tail pipe tips

    # ManualGearbox 265 transmission
    "trans_front":        (1020, 0, 460),      # bellhousing face
    "trans_rear":         (1400, 0, 420),      # output flange
    "trans_cg":           (1210, 0, 440),
    "trans_mount":        (1350, 0, 370),      # transmission crossmember mount

    # Driveshaft / propshaft
    "prop_front":         (1400, 0, 420),      # trans output
    "prop_rear":          (3280, 0, 310),      # diff input

    # Rear differential + LSD
    "diff_centre":        (3320, 0, 300),
    "diff_output_L":      (3372, 420, 300),    # half-shaft flange left
    "diff_output_R":      (3372, -420, 300),
}


# ------------------------------------------------------------------------
#  AERO DATUM PLANES  - for CFD boundary definition
# ------------------------------------------------------------------------
AERO: Dict[str, Vec3] = {
    "splitter_leading_edge":  (20, 0, 150),
    "splitter_trailing_edge": (240, 0, 150),
    "rear_wing_le":           (3840, 0, 1178),
    "rear_wing_te":           (4075, 0, 1178),
    "wing_angle_of_attack":   (8.0, 0, 0),     # degrees, adjustable
    "diffuser_start":         (3500, 0, 180),
    "diffuser_end":           (4340, 0, 260),
    "ride_height_ref":        (2180, 0, DT.ride_height),
}


# ------------------------------------------------------------------------
#  CHASSIS / STRUCTURE HARDPOINTS
# ------------------------------------------------------------------------
CHASSIS: Dict[str, Vec3] = {
    # Strut towers (top mount positions - reinforced SportsCar)
    "strut_tower_FL":     (810,  530, 700),
    "strut_tower_FR":     (810, -530, 700),
    "strut_tower_RL":     (3380, 540, 680),
    "strut_tower_RR":     (3380, -540, 680),

    # Firewall extent
    "firewall_top":       (1220, 0, 920),
    "firewall_bottom":    (1220, 0, 220),
    "firewall_width":     (1220, 780, 0),      # half-width

    # Rocker / sill rail
    "rocker_front":       (1100, 790, 180),
    "rocker_rear":        (3400, 790, 180),
    "rocker_z_top":       (0, 0, 310),         # sill height

    # Floorpan
    "floor_front":        (1220, 0, 220),
    "floor_rear":         (3450, 0, 220),
    "tunnel_width":       (0, 100, 0),         # half-width of driveshaft tunnel
    "tunnel_depth":       (0, 0, 180),         # tunnel bottom z

    # Rear wheel tubs
    "wheel_tub_RL":       (3372, 560, 300),
    "wheel_tub_RR":       (3372, -560, 300),
}


# ------------------------------------------------------------------------
#  UTILITY - mirror a hardpoint dict to the right side
# ------------------------------------------------------------------------
def mirror_hardpoints(hp: Dict[str, Vec3]) -> Dict[str, Vec3]:
    """Return a copy with all Y coordinates negated (left - right)."""
    return {k: (x, -y, z) for k, (x, y, z) in hp.items()}


def hardpoint_distance(a: Vec3, b: Vec3) -> float:
    """Euclidean distance between two hardpoints."""
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))
