# Provisional four-layer PCB setup

Configured 2026-09-14 for KiCad 10, using user-approved provisional defaults.
This is a starting point for layout, not a fabrication-qualified stackup.
Layer allocation updated to the user's requested Signal/Power - GND -
3.3 V Power - Signal/Power arrangement.

## Layer plan

| Layer | Intended use | Nominal thickness |
|---|---|---:|
| F.Cu | Components, signals, local power pours | 0.035 mm |
| Prepreg | FR-4 | 0.200 mm |
| In1.Cu / GND_L2 | Continuous GND reference for top routing | 0.035 mm |
| Core | FR-4 | 1.060 mm |
| In2.Cu / 3V3_L3 | Dedicated 3.3 V power plane; reference for bottom routing | 0.035 mm |
| Prepreg | FR-4 | 0.200 mm |
| B.Cu | Signals and power distribution | 0.035 mm |

Copper plus dielectric totals 1.600 mm. Copper is modeled as approximately
1 oz on all four layers. FR-4 relative permittivity 4.3, loss tangent 0.02,
and 0.010 mm solder mask per side are placeholders. Mask is additional to
the nominal copper/dielectric thickness. Finish is unspecified (`None`).
The fabricator must supply actual copper, dielectric, mask, material and
finished-thickness tolerances before impedance calculations or ordering.

Keep L2 as a continuous GND plane and L3 as a continuous 3.3 V plane.
Distribute other power rails with suitably sized outer-layer copper.
Top routing references GND; bottom routing references the 3.3 V plane.
Review plane continuity beneath bottom signals and the return-current
transfer between GND and 3.3 V at signal layer changes during layout.
The former two-GND-plane stitching guidance no longer applies to L3:
GND stitching vias must clear the 3.3 V plane.
Layer names and the `power` layer type express intent: they do not create
copper or enforce net membership. The preliminary layout now includes a
254 x 50.8 mm outline, a GND zone on In1.Cu and a +3V3 zone on In2.Cu.
See [the preliminary layout notes](PRELIMINARY_LAYOUT.md) for current status.

## Rules and routing defaults

All dimensions below are mm. Global constraints live in
`DIC_Board.kicad_pro`; the through-via-only rule lives in `DIC_Board.kicad_dru`.

| Setting | Value |
|---|---:|
| Minimum copper clearance; Default netclass clearance | 0.15 |
| Minimum track width | 0.15 |
| Default routing width | 0.20 |
| Minimum/default via diameter | 0.60 |
| Minimum/default drilled hole | 0.30 |
| Minimum via annular ring | 0.15 |
| Hole-to-other-net copper clearance | 0.25 |
| Hole-to-hole clearance | 0.25 |
| Copper-to-board-edge clearance | 0.50 |
| Silkscreen item clearance | 0.15 |
| Minimum silkscreen text height / stroke | 1.00 / 0.15 |

Track presets: 0.15, 0.20, 0.25, 0.30, 0.50, 0.60, 0.75, 1.00, 1.50, 2.00.
Via diameter/drill presets: 0.60/0.30, 0.80/0.40, 1.00/0.50.
The zero entries in the project preset arrays are KiCad's default entries,
not permitted zero-size routing geometry.

Microvias, blind vias and buried vias are prohibited by custom DRC.
Hole-to-hole violations are errors; missing courtyards are warnings.
Existing short, clearance, unconnected and outline checks remain enabled.
Silkscreen defaults apply to newly created graphics; existing library
graphics have not been resized. The retained solder mask and paste
expansions are zero; via tenting is enabled on both sides. Tenting is not
filled/capped via-in-pad fabrication. Mask web capabilities remain a
fabricator-specific follow-up.

The preliminary routing uses 0.20 mm for ordinary signals and a 0.15 mm minimum where escape routing
requires it. The minimum clearance is a geometric baseline, not a voltage
isolation or creepage qualification. Power, motor, pump and valve paths
need current, temperature-rise, voltage-drop and thermal-relief sizing;
the wider presets are not current ratings. The routing pass adds 1.50 mm
Power_Backbone, 0.60 mm Power_Branch and 0.25 mm Plane_Connections classes.
Power_Backbone and Power_Branch use 0.20 mm clearance; Default and
Plane_Connections use 0.15 mm. These are provisional routing choices,
with no changes to pad net assignments.

Existing differential-pair width/gap defaults are unqualified placeholders.
Select the fabricator stackup, calculate the required impedance and assign
net-specific geometry/timing rules before routing impedance-sensitive nets.

KiCad's distinction between stackup metadata, constraints, netclasses and
custom rules is documented in the [KiCad 10 PCB Editor manual](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html).

## Initial setup validation (before preliminary placement)

KiCad 10.0.4 loaded and round-tripped the edited board, retaining four copper
layers and the physical stackup. All original footprint content, UUIDs,
positions, pad nets and subsequent board content were preserved exactly.
The KiCad skill PCB analyzer found 293 footprints, no routed tracks, no
vias, no copper zones and no Edge.Cuts outline. The repository guide's
empty-placeholder description predates the current board.

Native DRC ran before and after setup. Both runs reported 310 violations
and 499 unconnected-item entries. Three prior 0.20 mm clearance reports
disappeared with the 0.15 mm baseline; one silk overlap, one text-height
and one text-stroke report appeared under the new silkscreen limits.

| Remaining violation category | Count |
|---|---:|
| Drill size | 149 |
| Hole clearance | 4 |
| Shorting items | 3 |
| Missing/invalid outline | 1 |
| Silkscreen over copper | 147 |
| Silkscreen overlap | 1 |
| Solder mask bridges | 3 |
| Text height | 1 |
| Text stroke | 1 |

The drill and hole-clearance violations already existed under the retained
0.30 mm drill / 0.25 mm hole-clearance limits. Resolve footprint-specific
requirements against the selected process before changing these limits.
Investigate the three footprint pad shorts before placement/routing.
No violations were excluded or waived. These are DRC observations, not a
resolved-netlist electrical design review or a claim of fabrication readiness.

Generated local evidence (ignored by Git) is in `../analysis/pcb-setup/`:
`before.json`, `drc-before.json`, `drc-after.json`, and `roundtrip.kicad_pcb`.
No schematic or firmware changes were made, so ERC was not rerun.
