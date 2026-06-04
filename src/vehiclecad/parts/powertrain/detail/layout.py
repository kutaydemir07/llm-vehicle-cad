"""Shared powertrain skeleton dimensions.

The visible powertrain parts are still emitted as independent atomic solids, but
their functional interfaces come from this one layout.  This keeps the crank,
clutch, gearbox output, propshaft, differential, and half-shafts centred on the
same mated axes instead of relying on copied coordinates in each part file.
"""
from __future__ import annotations

from vehiclecad.core.reference import hardpoints as SK

PT = SK.POWERTRAIN
REAR = SK.REAR_SUSP

CL_Y = 0.0
CRANK_Z = 445.0

ENGINE_FRONT_X = PT["engine_front"][0]
ENGINE_REAR_X = PT["engine_rear"][0]
BELLHOUSING_FACE_X = ENGINE_REAR_X
TRANS_FRONT_X = PT["trans_front"][0]
TRANS_REAR_X = PT["trans_rear"][0]

CLUTCH_AXIS = (PT["trans_front"][0], CL_Y, CRANK_Z)
PROPSHAFT_FRONT = PT["prop_front"]
PROPSHAFT_REAR = PT["prop_rear"]

DIFF_CENTER = PT["diff_centre"]
DIFF_OUTPUT_L = PT["diff_output_L"]
DIFF_OUTPUT_R = PT["diff_output_R"]
REAR_HUB_L = REAR["hub_centre"]
REAR_HUB_R = (REAR_HUB_L[0], -REAR_HUB_L[1], REAR_HUB_L[2])

GEARBOX_MOUNT = PT["trans_mount"]
ENGINE_MOUNT_L = PT["engine_mount_L"]
ENGINE_MOUNT_R = PT["engine_mount_R"]
ENGINE_MOUNT_REAR = PT["engine_mount_rear"]
