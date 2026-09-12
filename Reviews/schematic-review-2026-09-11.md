> Historical review: subsequent repairs and current outstanding items are recorded in the [repair report](schematic-fixes-2026-09-11.md).

# Schematic review — 11 September 2026

**Verdict: review completed; schematic is not ready for release.** All 282 components and the resolved 343-net hierarchy were included. Definite wiring/package errors and unresolved operating requirements remain. The PCB is an empty placeholder, so there is no layout, thermal, EMC, DRC or fabrication sign-off.

## Highest-priority findings

| Priority / confidence | Circuit | Finding and next action |
|---|---|---|
| P1 / high | U34 and U39 RS-232 | MAX3226EETE TQFN parts use symbols with SSOP pin numbering. Actual TQFN pin11 is ground and pin12 is VCC; current connections differ. Replace with package-correct symbols and preserve functional connections. U40 has the correct map. |
| P1 / high | D10 input protection | Unidirectional SMBJ18A is represented by an A1/A2 symbol, with cathode-marked footprint pad1 grounded and pad2 positive. Correct its symbol and polarity before applying power. |
| P1 / high | J31 power harness | Comment says pin1 positive/pin2 ground; resolved wiring is pin1 ground/pin2 positive through F10. Resolve the harness convention and synchronize documentation and circuit. |
| P1 / medium | U10 compensation | R106=49.9Ω with C104=10nF gives a319kHz compensator zero, inappropriate relative to the stated crossover guidance. Design and validate the loop against effective capacitance and actual load; do not blindly change to49.9kΩ. |
| P1 / high, load-dependent | Input protection and budget | F10=10A exceeds J31's published8.5A contact maximum. The allowed full converter load could require11.35A at8.64V and90% efficiency before other loads. Establish source, harness, fuse and simultaneous-load limits. |
| P1 / high | Actuator interface | J5 assumes an external controller with PWM, position and current signals. The documented P16-P actuator itself provides motor and potentiometer connections. Confirm controller and cable before connection. |

## Other corrections and qualification work

- U20–U22 DRV8823 footprint has an8×4mm full-paste exposed pad versus the device's approximately3.70×3.65mm maximum thermal pad. Rework the device-specific land/stencil pattern and erroneous through-hole attribute.
- U1 VREF+ has only100nF after FB1; ST's reference network includes a local1µF capacitor. The selected ferrite does not close that gap.
- LSE6.8pF load capacitors leave little stray-capacitance allowance; verify startup, gain margin and frequency. NRST2.2nF is much smaller than ST's100nF reference. COMM_EN has no defined hardware reset state.
- CubeMX does not establish a valid48MHz USB clock. USB VBUS software handling and exact PSRAM timing/configuration need implementation verification; only IOC inputs exist. Installed PSRAM is64Mbit/8MB volatile memory, not32MB.
- LI-830 requires at least12V; switch and cable drop place a nominal12V source below that requirement. Resolve voltage headroom.
- Qualify the6.6V KNF pump rail against the exact6V pump variant, and its2.466A switch limit against the pump's stated0.17A maximum. Obtain the exact K96 electrical interface specification.
- Acid-pump RESET/EN bias can energize a phase before firmware initialization. Final487Ω selection gives a60.159–239.366mA nominal adjustment range, with110mA available near RV1=3.948kΩ. Exact winding current, calibration and maximum-fault current still require qualification.
- Verify exact latching-valve article, pulse duration, polarity and thermal duty limits. The selected0.2W0402 sense resistors cover nominal132mW at0.2A, subject to PCB derating and fault behavior.
- Q1's3.3V setting provides about−3.15V gate drive; its PMOS on-resistance is specified at stronger drive. Establish acceptable voltage drop/current experimentally or select a guaranteed device.
- Regulator nominal setpoints are consistent. Exact MLCC DC-bias capacitance, load/inrush budget, reverse-input and surge behavior remain unqualified. Make electrolytic polarity visible in C41/C100/C113 symbols.

## Changes applied

Used the maintained BOM property editor; preserved pre-existing user changes and existing property fields. Generic sensor/controller connectors now use Molex Micro-Fit3.0, with a single-row five-position part at J13. Selected rated passives and exact order codes, corrected R103 to Vishay WSL25126L800FEA, completed U1's MPN and U2's footprint, and created the exact TPS552882 RPM0026A footprint for U10, keeping pads24/25/26 electrically separate.

Applied the user's additional selections: **FB1=Murata BLM18AG601SN1D,600Ω at100MHz,0603; R329=Vishay TNPW0603487RBEEA,487Ω,0.1%.** These are the only changed component values; connectivity is unchanged. Electrical findings above remain open rather than being silently redesigned during the review.

Filled **109 missing MPNs and 43 missing footprints**. Final coverage:270/275 purchased components have MPNs;277/282 components have footprints. All assigned footprints resolve to files and contain every netlisted pin number. That pad-number check does not certify physical package geometry; the DRV8823 issue remains.

The following hardware selections remain deliberately flagged, per the user's instruction:

| Reference | Missing selection |
|---|---|
| BT1 | RTC battery and holder |
| J2 | SWD/debug header hardware |
| JP1 | Boot jumper/header hardware |
| P1 | Exact USB-C plug |
| SW1 | Reset-switch hardware |

TP20–TP26 are seven fabricated PCB test points with footprints; they have no purchasable MPN. Do not invent MPNs for these copper features.

## Verification and trust limits

- KiCad10.0.4 exported the complete hierarchy before and after edits. All343 net pin sets are unchanged. The final value diff contains only the two approved selections.
- Root ERC remains **46 errors and38 warnings (84 total)**:43 unconnected-pin errors,3 undriven-power errors,21 off-grid warnings,8 library issues,7 library mismatches and2 dangling wire endpoints. Most unconnected pins are unused MCU GPIOs, plus J2 TDI; mark deliberate omissions correctly after review. Do not globally suppress them. Existing ignored ERC categories include single-global-label, four-way-junction, simulation-model and footprint-filter checks.
- Manufacturer pin tables, dimensions and functional requirements were checked against the original documents where available, with archive provenance. The following subsystem appendices include calculations, coverage and source links. Exact PSRAM, K96, pump/winding variants, connector harness and some capacitor bias data remain evidence gaps.
- Automated schematic, BOM, cross-check, thermal and EMC tools ran. Connectivity claims use only the resolved KiCad netlist. Physical scores on the empty PCB are not meaningful. No compatible standalone SPICE simulator was found, so screening calculations are not simulations. All50 lifecycle lookups returned unknown; availability and lifecycle are not certified.
- Automated deep-review evidence validation accepted20 findings with0 quarantined;17 have partial citation checks because PDF-extraction tooling or matching files were unavailable to the gate. Anchors and computation references passed; this is not equivalent to all-datasheet automated verification.

## Prior-review corrections

The old U10 COMP/ILIM short is already absent; C106 is now10µF. The previous acid-driver0.94A estimate no longer applies. USB is intentionally a plug with a single CC resistor; do not impose receptacle CC2 wiring. RTC direction and SPI divider corrections are present. R2 is an intentional temporary battery shunt. The power input is one connected hierarchical net despite an analyzer isolation warning. TPSM53603 permitted NC grounding and unused outputs are not blockers. LI-7815 is externally powered; LOX has an intermediate harness rather than a direct sensor-header pinout.

## Detailed evidence and complete inventory

- [All282 components and final MPN/footprint ledger](component-audit-2026-09-11.md)
- [Power: every component, calculations and primary sources](power-review-2026-09-11.md)
- [Digital: all MCU pins, clocks, memory and firmware mapping](digital-review-2026-09-11.md)
- [Loads: sensors, pumps, valves and actuators](loads-review-2026-09-11.md)

The subsystem reports preserve their initial-state calculations and explicitly identify final-state overrides at the top. Final metadata and approved value selections are authoritative in the component ledger. Generated raw evidence, netlists, source hashes and validation JSON are under `analysis/review_20260911/` (ignored by Git); retain that directory with the review if independently reproducing its evidence.
