# LLM Vehicle CAD

How far can CAD generation be pushed with modern LLMs using product development knowledge alone?

This repository explores that question with a high-detail, script-based vehicle CAD model generated as Python and CadQuery code. The model is inspired by classic sports coupe proportions, but it is built as an independent research and engineering design experiment.

No RAG. No fine-tuning. No commercial CAD software.

![Vehicle CAD preview](assembly_animation.gif)

## What This Is

- Editable CAD geometry written as Python scripts
- CadQuery B-rep solids
- A top-down vehicle product structure with systems, subassemblies, and atomic parts
- Type-annotated source code intended to be inspected, modified, and regenerated
- STEP/STL export tooling for downstream CAD, CAE, and simulation workflows
- Validation and audit tools for product-tree structure, atomic part detail, fitment, and collision checks

The generated STEP file can be used as an input for downstream workflows such as crash simulation preparation in PyLCSS or other CAE pipelines.

## Project Structure

```text
complete vehicle -> system -> subsystem -> leaf assembly -> atomic part file
```

| Path | Purpose |
|---|---|
| `src/vehiclecad/vehicle/` | Complete vehicle assembly entry points |
| `src/vehiclecad/assemblies/` | Product tree, source collectors, assembly mapping |
| `src/vehiclecad/core/` | Coordinates, datums, materials, colors, reference data |
| `src/vehiclecad/parts/` | Parametric CadQuery part and subsystem geometry |
| `src/vehiclecad/parts/atomic/` | One-file-per-part atomic leaf definitions |
| `src/vehiclecad/systems/` | System-level organization |
| `src/vehiclecad/subassemblies/` | Subassembly composition |
| `src/vehiclecad/validation/` | Fitment, export, collision, and product-structure checks |
| `src/vehiclecad/tools/` | Build, audit, export, render, and animation tools |

## Quick Start

### Requirements

- Python 3.11+
- CadQuery 2.6+
- PyYAML
- PyVista and matplotlib for optional rendering or GIF generation

### Install

```bash
pip install -e .
```

### Build

Windows PowerShell:

```powershell
.\build.ps1 build
.\build.ps1 export-step
.\build.ps1 export-stl
.\build.ps1 audit
```

Linux/macOS:

```bash
make build
make export-step
make export-stl
make audit
```

### Render Preview

```bash
python -m vehiclecad.tools.build_detailed_vehicle --no-step --no-stl --render
```

Outputs are written under `exports/`.

## Notes

This project was generated and iterated through LLM prompting, product development reasoning, and CadQuery code execution. It does not use OEM CAD data, scanned geometry, RAG, fine-tuning, or commercial CAD software.

The vehicle is an independent educational/research model inspired by classic sports car proportions. It is not affiliated with, endorsed by, or sponsored by any automotive manufacturer.