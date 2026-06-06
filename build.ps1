param (
    [string]$Target = "build"
)

$env:PYTHONPATH = "src"

switch ($Target) {
    "test" {
        python -m pytest
    }
    "build" {
        python -m vehiclecad.tools.build_detailed_vehicle
    }

    "generate-atomic" {
        python -m vehiclecad.tools.generate_atomic_part_files
    }
    "export-step" {
        python -m vehiclecad.tools.build_detailed_vehicle --no-stl
    }
    "export-stl" {
        python -m vehiclecad.tools.build_detailed_vehicle --no-step
    }
    "make-gif" {
        python src/vehiclecad/tools/make_assembly_gif.py
    }
    "audit" {
        python -m vehiclecad.tools.audit_vehicle_contract --collisions off
        python -m vehiclecad.tools.audit_vmodel_structure
        python -m vehiclecad.tools.audit_atomic_detail
        python -m vehiclecad.tools.audit_machine_elements
        python -m vehiclecad.tools.audit_functional_mechanisms
        python -m vehiclecad.tools.audit_modela_sportscar_reference
    }
    default {
        Write-Host "Unknown target: $Target"
        Write-Host "Available targets: test, build, generate-atomic, export-step, export-stl, make-gif, audit"
    }
}
