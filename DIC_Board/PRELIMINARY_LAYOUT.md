# Preliminary 10 x 2 inch placement

This is a preliminary component placement in `DIC_Board.kicad_pcb`, dated
2026-09-14. The board outline measures **254.0 x 50.8 mm** along the
Edge.Cuts centerlines, with its upper-left corner at KiCad coordinates
(20.0, 30.0) mm. The board now has 297 footprints: the 293 original
footprints plus the four schematic mounting holes described below.

The board now has an initial routing pass. See [PRELIMINARY_ROUTING.md](PRELIMINARY_ROUTING.md)
for current counts, SMD test-point changes and remaining work. The placement
and unrouted validation below describe the earlier placement stage.

## Arrangement

From left to right, the board contains:

| Region | Placement intent |
|---|---|
| Power input and conversion | Input connector, fuse, protection, MOSFETs, inductor and supply modules grouped at the left end |
| Pumps and actuators | Driver stages near the top/bottom harness connectors; the 2.8 V module is near the acid-pump stage |
| MCU and service connections | MCU near the center, memory beside it, crystals near oscillator pins, battery and debug access nearby |
| Communications | Serial transceivers near their external connectors |
| Sensors | Sensor connectors on the two long edges, with interface and power-switch circuitry nearby |
| Valve banks | Three drivers and their bulk capacitors at the right end, near the two valve harness connectors |

Connector locations are provisional; no fixed enclosure or harness locations
were supplied. Horizontal harness connectors face the nearest long edge.
USB faces the bottom edge and microSD insertion faces the top edge. Vertical
debug and auxiliary headers remain accessible from above. Enclosure access,
plug envelopes, cable bend space and component height need mechanical review.
The four mounting holes now follow the symbols added to the schematic.

The footprint placement uses the existing footprint geometry and the resolved
hierarchical netlist exported from `DIC_Board.kicad_sch`. Nearby support
parts were arranged by connectivity and functional sheet. This is not yet a
datasheet-qualified regulator hot-loop, decoupling or signal-integrity layout.

## Stackup and copper

The requested layer allocation is retained:

1. F.Cu: Signal / Power
2. In1.Cu (`GND_L2`): GND
3. In2.Cu (`3V3_L3`): +3V3
4. B.Cu: Signal / Power

Both inner layers have filled board-spanning zones assigned to their actual
nets. Zones begin 0.5 mm inside the outline. The provisional 1.6 mm stackup
and saved DRC rules are unchanged from [PCB_SETUP.md](PCB_SETUP.md).
The zones do not connect every SMD power pin by themselves. The subsequent
preliminary routing adds local plane ties, with some connections still open.
Review plane voids, switching-node keepouts and reference transitions as
routing is completed.

## Mounting-hole update

H1-H4 use the schematic-assigned `MountingHole:MountingHole_2.5mm_Pad`
footprint: 2.5 mm plated drill, 5 mm copper pad, connected to GND. Their
schematic UUID paths are recorded on the PCB footprints for future updates.
Centers are 4 mm from both adjacent board edges, giving 1.5 mm copper-pad
clearance to the outline. The mounting pattern is 246 x 42.8 mm.

| Hole | Corner | X from left edge | Y from top edge | KiCad X / Y |
|---|---|---:|---:|---|
| H1 | Top left | 4 mm | 4 mm | 24 / 34 mm |
| H2 | Top right | 250 mm | 4 mm | 270 / 34 mm |
| H3 | Bottom right | 250 mm | 46.8 mm | 270 / 76.8 mm |
| H4 | Bottom left | 4 mm | 46.8 mm | 24 / 76.8 mm |

J31 moved 4 mm right; C214 and C224 moved 2 mm left. C101, C107, C108,
C115, C126 and C213 were repositioned to clear the new hardware and the
adjusted components. Exact offsets and rotations are recorded in
`../analysis/mounting-holes/changes.json`. The original footprint identities,
pad nets, board dimensions, stackup and project settings were preserved.

KiCad 10 DRC was rerun before and after this update: both runs reported
309 violations and 499 unconnected-item entries. No new violation identities
were introduced. All 297 footprint geometry bounding boxes fit inside the
board and none overlap. Both copper planes were refilled. The schematic
was read but not edited during this PCB update.

The fresh reports and validation are in `../analysis/mounting-holes/`:
`drc-before.json`, `drc-after.json`, `validation.json`, and `top.svg`.

## Preliminary-placement validation (before mounting-hole update)

- KiCad 10.0.4 loads the result and fills both inner-plane zones.
- Edge.Cuts centerline dimensions are exactly 254.0 x 50.8 mm.
- All 293 footprint UUIDs, library identities, values and pad/net identities
  are preserved. No components or pad assignments were added or removed.
- Every existing PCB pad net matches the resolved netlist after normalizing
  KiCad's escaped net names. The existing duplicate R322 remains an extra
  physical instance; matching pad nets does not resolve that duplication.
- All footprint geometry bounding boxes fit inside the outline, with at
  least 0.5 mm margin. No footprint bounding boxes overlap.
- Native DRC reports no courtyard overlap or invalid-outline violations.
- The saved project file retains the previously configured DRC settings.
- The actual KiCad top-copper/fabrication export was rendered and inspected.

The remaining native DRC baseline is **306 violations** and **499
unconnected-item entries**. None of the 306 violation identities is new
relative to the initial setup baseline:

| Category | Count |
|---|---:|
| Drill size | 149 |
| Hole clearance | 4 |
| Shorting items | 3 |
| Silkscreen over copper | 147 |
| Solder mask bridges | 3 |

The outline error is resolved. Footprint reference/value fields are hidden
for this placement pass, removing three prior text/silkscreen warnings;
footprint fabrication references remain available in the review export.
Silkscreen placement must be completed after routing. No DRC exclusions or
error-severity reductions were used.

## Items to resolve before detailed routing

1. Reconcile the two R322 footprints against the single resolved schematic
   component. Both were deliberately retained in this preliminary layout.
2. Resolve the three existing valve-driver footprint pad shorts.
3. Review the 0.2 mm thermal holes against the provisional 0.3 mm drill
   minimum and the connector hole-clearance violations against the chosen
   fabricator. Do not lower global limits merely to clear the report.
4. Confirm connector and enclosure constraints against the four-hole pattern.
5. Refine regulator input/output loops, feedback routing, decoupling,
   exposed-pad thermal connections and oscillator routing before fixing
   the placement. Wide power paths require current and voltage-drop sizing.
6. Route signals and power, add plane connections/stitching as appropriate,
   then repeat DRC and the electrical/layout review.

## Local generated evidence

The review image is [overview.png](../analysis/preliminary-layout/overview.png)
and the scalable version is [overview.svg](../analysis/preliminary-layout/overview.svg).
Both derive from the actual KiCad top-copper, silkscreen and fabrication export.
The colored region headings are explanatory annotations outside the board.

Generated evidence in `../analysis/preliminary-layout/` is ignored by Git:
`resolved.xml`, `validation.json`, `netlist-parity.json`, `drc-final.json`,
`before.json`, `after.json`, and the rendered exports. The pre-placement
PCB is retained there as `before-placement.kicad_pcb`. Helper scripts are
also retained for reproducibility; do not rerun the placement helper over
subsequent manual edits because it intentionally starts from that snapshot.

No schematic or firmware files were edited. ERC was not rerun for this
mechanical placement task. This is not a full electrical, EMC or thermal review.
