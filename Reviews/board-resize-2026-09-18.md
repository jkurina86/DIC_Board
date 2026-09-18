# Board resize — 2026-09-18

Changed the overall outline from 254 × 50.8 mm to **241.3 × 50.8 mm (9.5 × 2 inches)**. The left edge remains at X = 21.5 mm; the right edge is now X = 262.8 mm. Top and bottom are Y = 79.6 and 130.4 mm.

The MCU group and existing SD-card notch moved left together by 12.7 mm. The right mounting holes and their keepouts moved by the same amount, retaining 5 mm center-to-edge offsets. Both internal-plane outlines were shortened. Central placement was tightened to accommodate the shorter board; 190 footprint origins moved in total. The far-left valve group remains in place. Silkscreen references were repositioned, with 32 references retained on F.Fab where space was insufficient.

All 291 footprint identities, assignments, orientations and pad nets are preserved. The four-layer stack and custom design rules are unchanged. There are no routed tracks or vias, and the zones remain unfilled. Existing schematic edits were left untouched.

## Verification

KiCad 10 PCB analyzer confirms the exact 241.3 × 50.8 mm outline. Native KiCad 10 DRC with schematic parity reports 305 violations versus 306 before the resize, 499 unconnected items, and the same 26 pre-existing schematic parity issues. Comparison by violation type, severity and affected item UUIDs found no new DRC or parity findings. No new outline, copper-edge or courtyard-overlap issues were introduced. This remains a preliminary, unrouted board with existing design issues.

Generated evidence is under ignored `analysis/`: `resize-before.json`, `resize-after.json`, `resize-drc-before.json`, `resize-drc-final.json`, `resize-moves.json`, and `resize-labels.json`. The pre-edit board is backed up in `analysis/resize-backup/`.
