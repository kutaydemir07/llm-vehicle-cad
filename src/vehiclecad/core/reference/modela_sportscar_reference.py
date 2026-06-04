"""Source-backed Classic ModelA SportsCar reference facts for the detailed seed vehicle.

The platform structure stays generic, but the current high-detail seed is an
ModelA SportsCar. Keeping researched facts here makes drift visible in validation instead
of letting generic dimensions and placeholders creep back into the model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReferenceSource:
    key: str
    title: str
    url: str
    used_for: tuple[str, ...]


@dataclass(frozen=True)
class DimensionReference:
    overall_length: float = 4345.0
    overall_width: float = 1680.0
    overall_height: float = 1370.0
    wheelbase: float = 2562.0
    wheelbase_alt: float = 2565.0
    front_track: float = 1412.0
    front_track_alt: float = 1414.0
    rear_track: float = 1433.0
    rear_track_alt: float = 1435.0
    front_overhang_model: float = 810.0
    rear_overhang_model: float = 973.0
    curb_weight_kg: float = 1200.0
    drag_coefficient: float = 0.33


@dataclass(frozen=True)
class PowertrainReference:
    engine_code: str = "I4_EngineB23"
    displacement_cc: int = 2302
    cylinder_count: int = 4
    valves_per_cylinder: int = 4
    bore_mm: float = 93.4
    stroke_mm: float = 84.0
    compression_ratio: float = 10.5
    transmission_eu: str = "ManualGearbox 265/5 dogleg 5-speed manual"
    transmission_us: str = "ManualGearbox 265/6 5-speed manual"
    final_drive_ratio: float = 3.25
    lsd_lock_percent: int = 25


@dataclass(frozen=True)
class ChassisReference:
    front_suspension: str = "MacPherson strut"
    rear_suspension: str = "semi-trailing arm"
    steering: str = "rack and pinion hydraulic assist"
    front_disc_diameter: float = 280.0
    rear_disc_diameter: float = 282.0
    front_brake_disc_type: str = "ventilated"
    rear_brake_disc_type: str = "solid"
    brake_caliper_piston_count: int = 1
    abs_standard: bool = True
    bolt_count: int = 5
    pcd_mm: float = 120.0
    center_bore_mm: float = 57.1
    wheel_width_j: float = 7.0
    wheel_diameter_in: float = 15.0
    wheel_offset_et_mm: float = 24.0
    tire_size: str = "205/55VR15"
    tire_width_mm: float = 205.0
    tire_aspect_ratio: float = 55.0
    model_tire_outer_diameter_mm: float = 600.0

    @property
    def wheel_diameter_mm(self) -> float:
        return self.wheel_diameter_in * 25.4

    @property
    def catalog_tire_outer_diameter_mm(self) -> float:
        sidewall = self.tire_width_mm * self.tire_aspect_ratio / 100.0
        return self.wheel_diameter_mm + 2.0 * sidewall


@dataclass(frozen=True)
class StructureReference:
    body_type: str = "2-door coupe"
    homologation_required_road_cars: int = 5000
    has_box_fenders: bool = True
    has_side_skirts: bool = True
    has_plastic_front_rear_bumpers: bool = True
    has_raised_rear_decklid: bool = True
    has_rear_wing: bool = True
    has_flatter_wider_c_pillar: bool = True
    has_sportscar_specific_backlight: bool = True


SOURCES: tuple[ReferenceSource, ...] = (
    ReferenceSource(
        key="classic_m",
        title="Classic M official ModelA SportsCar portrait",
        url="https://www.classic-m.com/en/topics/magazine-article-pool/classic-sportscar-modela-portraet.html",
        used_for=(
            "homologation context",
            "motorsport-derived body structure",
            "ABS and ventilated-disc brake description",
            "plastic bumpers, side skirts, decklid, spoiler, and C-pillar changes",
            "I4_Engine four-cylinder overview",
        ),
    ),
    ReferenceSource(
        key="auto_data",
        title="Auto-Data Classic SportsCar Coupe (ModelA) 2.3 CAT specifications",
        url="https://www.auto-data.net/en/classic-sportscar-coupe-modela-2.3-215hp-cat-9888",
        used_for=(
            "overall length, width, height",
            "alternate wheelbase and track values",
            "I4_EngineB23 bore, stroke, displacement, compression",
            "ABS, tire, and wheel baseline",
        ),
    ),
    ReferenceSource(
        key="modelazone",
        title="ModelA Zone SportsCar model notes",
        url="https://www.modelazone.net/modelawiki/index.php?title=SportsCar",
        used_for=(
            "SportsCar-specific panels, rear window, C-pillars, rear decklid, bumpers, wings, and sills",
            "5x120 hubs",
            "Mesh wheel and tire fitment",
            "ManualGearbox 265, LSD, ABS, and brake package notes",
        ),
    ),
    ReferenceSource(
        key="modelampower",
        title="ModelAMPOWER SportsCar tech specs",
        url="https://modelampower.com/SportsCar-techspec.html",
        used_for=(
            "master wheelbase and track datum",
            "ManualGearbox 265/5 and 265/6 transmission split",
            "3.25 final drive and 25 percent LSD",
            "280 mm front and 282 mm rear brake discs",
            "15x7J ET24 wheels and 205/55VR15 tires",
        ),
    ),
)

DIMENSIONS = DimensionReference()
POWERTRAIN = PowertrainReference()
CHASSIS = ChassisReference()
STRUCTURE = StructureReference()


def source_url(key: str) -> str:
    for source in SOURCES:
        if source.key == key:
            return source.url
    raise KeyError(f"unknown ModelA SportsCar reference source: {key}")
