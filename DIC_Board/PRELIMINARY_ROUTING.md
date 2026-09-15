# Preliminary routing — 2026-09-14

The PCB now contains **2,143 track segments and 526 through vias**.
This is an initial routing pass, with **146 connections still missing**;
it is not a finished or fabrication-ready layout.

All tracks are on the outer layers: 1,596 on F.Cu and 547 on B.Cu.
The requested Signal/Power – GND – +3V3 – Signal/Power stackup remains in
place, with filled GND and +3V3 inner-plane zones. The 254 × 50.8 mm outline,
all 297 footprint positions, and the four corner mounting holes are preserved.

## Test points

TP20–TP26 now use `TestPoint:TestPoint_Pad_D1.0mm`: **1 mm round exposed
top-copper pads, with no drilled holes**. Their references, positions, nets,
and schematic links are preserved. Separate adjacent 0.8/0.4 mm vias retain
the layer connections previously provided by the plated test-point holes.
The seven schematic Footprint properties were updated to match the PCB.

## Routing choices

The local Freerouting pass was followed by native KiCad plane-tie placement
and clearance/stub cleanup. The exchange used temporary unique names for
the duplicate R322 footprints; the actual PCB references were restored.
The existing duplicate R322 has not been resolved.

| Net class | Preferred width | Clearance |
|---|---:|---:|
| Default signals | 0.20 mm | 0.15 mm |
| Power_Backbone | 1.50 mm | 0.20 mm |
| Power_Branch | 0.60 mm | 0.20 mm |
| Plane_Connections | 0.25 mm | 0.15 mm |

Escapes may narrow locally, down to the 0.15 mm minimum. Ordinary routing
vias are 0.6/0.3 mm. These widths and vias are provisional geometry, not
current ratings. High-current paths, thermal reliefs, regulator hot loops,
USB pair geometry, clocks, decoupling and signal return paths still need
focused layout work. No impedance or timing qualification is claimed.

## Native verification

- KiCad 10.0.4 loads the board and refills both inner planes.
- The uncapped missing-connection count fell from **816 to 146**. Earlier
  reports showed 499 entries because the DRC report capped that category.
- All footprint UUIDs, positions and pad net assignments are preserved.
  Only the seven authorized test-point footprint/pad geometries changed.
- Pad nets match the fresh resolved hierarchical netlist from
  `DIC_Board.kicad_sch`. The test-point edits changed no electrical connections.
- Root schematic ERC reports the same three violations before and after;
  the complete violation records are unchanged.
- Final native PCB DRC reports **306 existing violations**, with no new
  violation identities from routing or the test-point changes. There are
  no dangling-track/via or new copper-clearance reports.
- The project settings survived the final board save unchanged.

The remaining DRC baseline comprises 149 undersized footprint drills,
147 silkscreen/copper overlaps, four USB footprint hole-clearance reports,
three valve-driver footprint shorts, and three solder-mask bridges.
The three initial 0.20 mm pad-clearance reports disappear under the restored
0.15 mm minimum; this is a rule change, not a footprint correction.

## Remaining work

Of the 146 missing connections, 28 are on +12V, 24 on GND and 15 on +3V3.
The rest include power-control, actuator, valve and other signal connections.
Complete these alongside a review of the provisional placement and power
distribution. U20/U21/U22 still have the original pad-33/pad-32 footprint
shorts, and the duplicate R322 still needs reconciliation with the schematic.

Fresh generated evidence is under `../analysis/preliminary-routing/`:
`validation.json`, `drc-after.json`, `resolved-after.xml`, `erc-before.json`,
`erc-after.json`, `testpoint-changes.json`, and `overview.png`.
Native DRC and connectivity are the basis for the counts above. This work
does not constitute a full electrical, EMC, thermal or fabrication review.
