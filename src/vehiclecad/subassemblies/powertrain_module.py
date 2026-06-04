from __future__ import annotations

import cadquery as cq

from vehiclecad.parts.powertrain.blockouts import make_battery_pack, make_differential, make_driveshaft, make_engine_or_motor, make_transmission
from vehiclecad.params.vehicle import VehicleParams


def make_powertrain_module(params: VehicleParams) -> cq.Assembly:
    assy = cq.Assembly(name="powertrain_module")
    if params.powertrain.is_ev:
        assy.add(make_battery_pack(params), name="battery_pack")
    assy.add(make_engine_or_motor(params), name="engine_or_motor")
    assy.add(make_transmission(params), name="transmission_or_reduction_drive")
    assy.add(make_driveshaft(params), name="driveshaft")
    assy.add(make_differential(params), name="differential")
    return assy

