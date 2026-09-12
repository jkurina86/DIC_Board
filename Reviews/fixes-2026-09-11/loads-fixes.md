> Final integration: root ERC is clean. Shared project libraries are synchronized; RTC bias labels now use global labels; fabricated TP20–TP26 are excluded from BOM; power references are unique; C100/C41/C113 now display polarity. The integrated netlist and validation in this folder supersede intermediate snapshots mentioned below.

# Load and sensor schematic repairs

Applied to the current sources on 2026-09-11. Electrical verification uses the fresh KiCad 10 hierarchical export `loads-after.net.xml`, with `before.net.xml` as baseline. The review inventory remains in `../review_20260911/loads-review.md` and `loads-pin-coverage.csv` (119 components).

## Repairs completed

- **U34 MAX3226EETE+**: corrected the package-specific TQFN pin numbering while retaining the signal wiring and drawing geometry. Exact resulting mapping is 1 C1−, 2 C2+, 3 C2−, 4 V−, 5 RIN, 6 ROUT, 7 INVALID, 8 TIN, 9 FORCEON, 10 TOUT, 11 GND, 12 VCC, 13 FORCEOFF, 14 READY, 15 V+, 16 C1+, 17 EP grounded. Removed a redundant dangling wire extending beyond TIN. U34 and U40 now use the complete lead-free order code MAX3226EETE+. [ADI Rev 11, pin configurations and ordering](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX3224E-MAX3245E.pdf).
- **U20/U21/U22 DRV8823**: assigned the new project footprint `DRV8823_DCA48_ReviewFixed`. Lead lands are 0.30 × 1.55 mm, pitch 0.5 mm; EP49 is 3.70 × 3.65 mm with the same paste opening for a 0.127 mm stencil, matching the manufacturer's example. Fixed SMD attribute and repeated legacy UUIDs. Thermal vias and copper still require PCB design, which does not yet exist. Snapped intermediate wire bends to the connection grid and replaced stale cached +12V symbols. All valve IC pin nets are unchanged in the resolved export. [TI DRV8823-Q1, DCA drawing/example land and paste pattern pp. 28–30](https://www.ti.com/lit/ds/symlink/drv8823-q1.pdf).
- **Acid pump R323**: moved the 18 kΩ resistor's pin 1 from +3V3 to ground. RESET_N now defaults low with the MCU high impedance, preventing the formerly pulled-high reset input from enabling the driver's home-phase state during startup. Existing EN pullup remains. Added a note to hold STEP=0/DIR=1 for the documented mode-selection interval when releasing reset. Exact winding current remains an external qualification requirement. [ST STSPIN220 datasheet](https://www.st.com/resource/en/datasheet/stspin220.pdf).
- **Auxiliary Q1**: replaced DMC3016LDV-13 with AO4630 and its SOIC-8 footprint. The new cached project symbol preserves pins 1–8 and all eight pin nets; obsolete exposed-pad pins 9/10 and their dead branches were removed. AO4630 specifies PMOS RDS(on) ≤78 mΩ at VGS=−2.5 V, covering the approximately −3.15 V gate drive from the 3.3 V selector setting. Its ±12 V gate rating is compatible with the existing nominal 8.2 V clamp. Unknown auxiliary load current, load transient energy and PCB thermal behavior remain to be qualified. [AOS AO4630 Rev 1.1](https://www.aosmd.com/res/datasheets/AO4630.pdf).

## Verification

`loads-fix-validation.json` records passing assertions for the U34 package mapping, U40 and valve pin-net preservation, Q1 pin-net preservation and expected deleted EPs, R323 ground connection, and all 49 DRV8823 numbered footprint pads/dimensions. The fresh export parsed successfully; annotation and final full ERC integration are handled centrally. No PCB or fabrication readiness is claimed.

## Required unresolved decisions

- **KNF supply confirmed by user:** the installed pump may retain the existing6.6V supply. No dedicated6V regulator is requested. The present≈2.47A switch limit still requires separate overload/startup qualification.
- **LI-830/valve supply accepted by user:** retain the existing nominal12V supply. The prior request for a supply decision is closed; no new measurement or manufacturer limit is asserted.
- **K96 and actuator interfaces confirmed by user:** retain both as implemented. Acid-pump winding/current/acceleration and valve article/polarity/maximum-pulse requirements remain open.
- R329 is the user-approved487Ω,0.1% Vishay TNPW0603487RBEEA; R328 is0.1% TNPW06032K87BEEA. The nominal phase-current adjustment range is60.159–239.366mA, with110mA near RV1=3.948kΩ. Exact winding qualification remains open. Valve 3.3 Ω current-sense resistors now have selected 0.2 W parts; their 132 mW nominal full-scale dissipation still needs temperature/copper derating in the eventual PCB.

Expected intentional local net changes are R323.1 +3V3→GND; U34 physical pin-number remapping and new grounded EP17; and Q1 deleted pads9/10. All other local changes are package/metadata or redundant geometry cleanup. No new U41/C44/R351/R352 components were placed.
