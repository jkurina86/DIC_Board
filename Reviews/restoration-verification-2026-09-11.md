# Restored schematic verification — 2026-09-11

Saved schematic sources contain 290 components and 343 resolved nets. All values, MPNs, footprints, and numbered-pin connectivity match the last accepted design. Later existing drawing placement changes were preserved.

- 285 of 290 components have assigned footprints; all assigned library footprints exist and cover every numbered symbol pin.
- 278 of 283 purchased components have MPNs. Seven fabricated test points have footprints and are excluded from the purchased BOM.
- Five explicitly deferred hardware selections remain flagged: BT1 battery/holder, J2 SWD header, JP1 boot header, P1 USB-C plug, SW1 reset switch.
- F10 is 8 A Littelfuse 0451008.MRL. The 6.6 V setpoint and accepted supply/interface decisions are preserved.
- KiCad 10 root ERC: zero errors, zero warnings with existing project rule configuration unchanged.

The complete saved source checkpoint is `restored-design-2026-09-11.zip`. The PCB remains an empty placeholder; footprint assignment is in the schematic, not PCB placement. Existing bench qualification items remain documented in the schematic review.
