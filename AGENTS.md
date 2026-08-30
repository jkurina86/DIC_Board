# Repository Guide

## Hardware Sources

- Open `DIC_Board/DIC_Board.kicad_pro` with KiCad 10.0. The schematics and PCB use KiCad 10 formats; older KiCad releases may not read them safely.
- `DIC_Board/DIC_Board.kicad_sch` is the hierarchy root. Run ERC or schematic analysis from this file, not from an individual leaf sheet.
- The root fans out to `mcu.kicad_sch`, `Power.kicad_sch`, `Sensors.kicad_sch`, `Pump_Control.kicad_sch`, `Valve_Control.kicad_sch`, and `actuators.kicad_sch`; the power, sensor, pump, and valve sheets contain further subsheets. Most cross-sheet connectivity uses global labels rather than root-sheet pins.
- `DIC_Board/DIC_Board.kicad_pcb` is currently a two-line empty placeholder: it has no outline, footprints, nets, or routing. Do not claim PCB, DRC, layout, or fabrication readiness from it.
- Project-local libraries are wired through `sym-lib-table` and `fp-lib-table`: `DIC_Board.kicad_sym`, `LCSC.kicad_sym`, and `DIC_Board.pretty/`. Keep the tables in sync if a library is moved or renamed.
- BOM data is stored on schematic symbols (`MPN`, `Manufacturer`, and distributor properties such as `DigiKey` or `Mouser`); there is no standalone source BOM. Preserve these fields when replacing parts.
- `DIC_Board/DIC_Board-STM32 MCU.pdf` and `DIC_Board/DIC_Board.bak` predate the current schematic. Treat them as historical exports, not design sources.

## Firmware Boundary

- `Firmware/DIC/DIC.ioc` is the populated STM32CubeMX source. `Firmware/Firmware.ioc` is an older skeleton with only the MCU/SysTick configured; do not update it as though it were the live pin map.
- The current target is STM32L476ZGT6 in LQFP144, generated with STM32CubeMX 6.15.0 and STM32Cube FW_L4 V1.18.1. Keep peripheral and pin changes synchronized with `DIC_Board/mcu.kicad_sch`.
- Only CubeMX `.ioc` inputs are committed; there is no generated firmware source tree or build system to test. CubeMX is configured with `DeletePrevious=true`, so generate code only when requested and review the resulting tree carefully.

## Documentation Archive

- Read `Docs/README.md` before using component evidence. Directories marked `_candidate`, `_bench_reference`, `_variant`, or `_not_32MB` are intentionally not proof of the installed design; do not replace missing exact-order-code data with family or candidate data.
- `Docs/download_sources.py` defines the public source set, and `Docs/manifest.json` is the provenance record. Search the generated same-basename `.txt` sidecars, but verify engineering claims against the original PDF/HTML and its manifest entry.
- To refresh the archive from the repository root, install `curl` and Poppler's `pdftotext`, then run:

```bash
python3 -m pip install -r Docs/requirements.txt
python3 Docs/download_sources.py
```

- A refresh requires network access, overwrites named artifacts, extracts ZIPs, regenerates all text sidecars, and rewrites `Docs/manifest.json`. The script exits nonzero on any failed source; review changed SHA-256 values before retaining previous citations or limits.
- The two `capability_mode.json` files are analyzer run metadata, not project configuration. Their zero datasheet coverage does not mean `Docs/` is empty.

## Verification

- Use the matching `kicad-happy` skill for KiCad analysis, BOM/sourcing, datasheets, SPICE, EMC, and fabrication tasks instead of building ad hoc parsers or workflows.
- KiCad is installed as Flatpak `org.kicad.kicad`; `kicad-cli` is not on `PATH`. Invoke it as `flatpak run --command=kicad-cli org.kicad.kicad ...`.
- No CI, lint, test, or task-runner configuration is committed. For schematic changes, run KiCad 10 ERC on `DIC_Board/DIC_Board.kicad_sch`; PCB DRC is not meaningful until the placeholder PCB is populated.
