# Full schematic re-review — 11 September 2026

**Result:** No new electrical wiring, value, or package-assignment defect was identified in the saved schematic. Three ERC power-source declaration errors remain, along with oscillator/load-protection qualification work and four minor metadata inconsistencies. This is a read-only review, not an unconditional electrical or fabrication sign-off.

Reviewed the KiCad 10.0.4 hierarchy root across **24 sheets, 292 components, and 347 resolved nets**. All **285 purchased components have MPNs**. All **292 devices have footprints**; the seven MPN-free test points are plated PCB features excluded from the purchased BOM. The review covers every component and resolved pin, with the detailed ledgers linked below.

## Findings

| Priority | Finding | Evidence and practical consequence |
|---|---|---|
| Warning — ERC cleanup | **Three undriven-power declarations:** U2 pin9 VBACKUP, J2 pin1 VTref, and +12V/#PWR0103 after R103. | Fresh root ERC reports 3 errors, 0 warnings. The netlist has actual DC paths through R3=470Ω from BT1, R19=470Ω from3.3V, and R103=6.8mΩ from U10 output. These are missing power-source declarations after passive components, not disconnected supplies. Resolve the declarations to obtain a clean ERC; no extra power circuit is indicated. High confidence, official ERC/netlist. |
| Warning — oscillator qualification | **Y2/C25/C26 have limited stray-capacitance allowance.** | The two6.8pF capacitors contribute3.4pF series load before pin/trace parasitics. Abracon ABS06-107 specifies4.0pF effective load and4.5pF maximum: only0.6pF nominal allowance, or1.1pF to the ceiling. At both capacitors' +0.25pF tolerance, the latter is0.975pF. Check actual load and startup margin; this does not demonstrate that the oscillator fails or justify an arbitrary capacitor change. High confidence calculation; board-level outcome unmeasured. [Abracon datasheet p2](https://abracon.com/Resonators/ABS06-107-32.768kHz-T.pdf). |
| Warning — existing protection qualification | **The air-pump switch current limit is not pump-specific overload protection.** | U31/R305 and the six other TPS27S100 channels use1kΩ ILIM resistors, setting2.466A nominal; FLT is unconnected and DIAG_EN grounded. This is much higher than the archived KNF6V model's0.17A maximum current. Keep the accepted6.6V supply, but establish the installed pump's fault/startup protection and response. A switch's IC protection does not establish motor protection. High confidence circuit calculation; exact installed overload envelope remains a qualification gap. [TI current-limit equation](https://www.ti.com/lit/ds/symlink/tps27s100.pdf), project KNF documentation. |
| Low — misleading description | **R323 is described as a DC reset pull-down, but C323 is in series.** | The path is U32.14 → C323 → R323 → GND. Correct the description. **This is not a floating reset input:** STSPIN220 provides an internal36kΩ typical STBY pull-down, and standby disables outputs. This corrects the earlier overstatement about the missing external pull-down. High confidence netlist/manufacturer evidence. [ST DS11633 Rev5 pp6,9–10](https://www.st.com/resource/en/datasheet/stspin220.pdf). |
| Low — stale metadata | **Q1 alternate description still names PowerDI3333 and old ratings.** | Its actual MPN is AO4630 and its footprint is SOIC-8; the selected component and physical pin map agree. Update Description_1 to prevent a misleading later substitution. High confidence source-property observation. |
| Low — inconsistent displayed rating | **C321 displays22µF16V but specifies a25V MPN/property.** | GRM32ER71E226ME15L and Voltage Rating=25V disagree with the displayed16V. The25V component is suitable on the2.8V rail; this is documentation cleanup. High confidence source-property observation. |
| Low — stale footprint filter | **U40 retains an SSOP filter for a TQFN part.** | MAX3226EETE+, its TQFN footprint, and all17 physical pin assignments agree. The old filter can mislead future assignment, and footprint-filter ERC checking is globally ignored. High confidence library metadata observation. |

Additional drawing clarity: C100, C41 and C113 use nonpolarized capacitor symbols for polarized Panasonic parts. Their numbered pad polarity is correct; using polarized symbols would make assembly intent clearer.

## Changes since the last completed update

Compared with `analysis/usb-socket-20260911/schematic.net.xml`: **no added/removed components, no changed values/MPNs/footprints, and no changed sets of electrically connected pins**. The CC2 net name changed from `/STM32 MCU/USB_CC2` to `Net-(D6-K1)`; P1.B5, D6.1 and R351.1 remain connected together. Drawing or presentation changes do not appear as connectivity changes. This review concerns the saved files; unsaved editor changes are outside the exported evidence.

The earlier MAX3226 TQFN pin corrections, D10 polarity, U10 compensation, output bulk capacitors, reference bypass, NRST capacitor, COMM/RTC control pull-downs, AO4630 selection, high-power valve sense resistors and USB clock settings remain intact. SW1, J2, JP1, J13, BT1 and P1 retain the selected hardware and footprints. The previous floating-acid-reset allegation is withdrawn as explained above.

The accepted 6.6V KNF supply, nominal12V LI-830/valve supply, K96 interface, actuator/controller interface and8A F10 selection are preserved as design requirements.

## Full-circuit coverage

The [complete component/pin inventory](../analysis/read-only-review-20260911/component-pin-inventory.csv) contains every reference, value, MPN, footprint, sheet, pin function and resolved net. These subsystem reports document the component-by-component pass, manufacturer evidence and remaining boundaries:

- [Digital review and component groups](../analysis/read-only-review-20260911/digital-review.md): MCU all144pins, supplies/reset/reference, RTC/battery, HSE/LSE, QSPI PSRAM, SD, SWD/boot, USB and RS232. [Digital pin ledger](../analysis/read-only-review-20260911/digital-component-coverage.csv).
- [Power review](../analysis/read-only-review-20260911/power-review.md): all86 power components/243 pins, input fuse/TVS, U10 buck-boost and four module rails. [Power component/pin audit](../analysis/read-only-review-20260911/power-audit.json).
- [Sensors, pumps, valves, actuators and auxiliary review](../analysis/read-only-review-20260911/loads-review.md):126components/579pins, all driver channels, references, sense resistors, protection diodes and connector pairs. [Loads pin ledger](../analysis/read-only-review-20260911/loads-coverage.csv). Subsystem scopes overlap on auxiliary communications; their counts must not be added.

For two-terminal passives, polarity where applicable, net pair, nominal value, package and assigned order code were checked. Every individual capacitor's bias/temperature/lifetime curves were not independently requalified. Exact primary-document coverage is incomplete for the PSRAM and some installed external loads; these gaps are recorded rather than assuming a family/candidate document proves an installed variant.

## Power and signal calculations

Power flow is J31 → F10 → P_IN, with D10 shunt protection. P_IN feeds the always-on3.3V module and U10's12V converter. The12V output feeds switched loads and the5V,6.6V and2.8V modules.

| Circuit | Current nominal result | Disposition |
|---|---|---|
| U10, R104/R105 |12.011V | Consistent with nominal12V target; accepted load boundary retained. |
| U11, R109/R110 |3.315V |3.3V rail. |
| U12, R116/R117 |5.016V |5V rail. |
| U13, R119/R120 |6.618V |Intended6.6V rail retained. |
| U14, R123/R124 |2.799V |2.8V rail. |
| U10 output current limit/R103 |7.353A nominal; approximately6.989–7.724A including specified limit/resistor tolerances |Does not set allowable aggregate input current. Source/cable/fuse/connector coordination remains necessary. |
| U11–U14 output capacitance |274.1µF nominal each, including180µF polymer |Added bulk remains present; effective ceramics and startup behavior remain part of physical qualification. |
| U32 acid current adjustment |60.16–239.37mA nominal peak; about3.95kΩ trim sets110mA |0.25W sense resistors dissipate about114.6mW at maximum nominal setting. Exact winding qualification remains separate. |
| U20–U22 valve full-scale current |200mA nominal;132mW per3.3Ω sense resistor |Selected0.2W0402 parts address the earlier ordinary0402-rating issue; temperature/pulse derating still applies. |
| U35–U38 enable divider |2.870V nominal from3.3V |Above the switch's2V high threshold. |
| J6 I2C pull-ups |4.7kΩ each; about251pF for1µs rise time or75pF for300ns |Actual cable capacitance and selected bus speed require validation. |
| Q1 auxiliary PMOS |VGS≈−3.152V on3.3V selection |AO4630 has a−2.5V on-resistance specification; earlier insufficient-gate-drive selection issue is closed. |

U10's10kΩ/100nF/1nF compensation remains. The repeated averaged corner model has a minimum phase margin around60.4° and gain margin10.95dB over its assumed envelope; this is analytical evidence, not a switching simulation or measured loop response. [Power calculations](../analysis/read-only-review-20260911/power-calculations.json), [model results](../analysis/read-only-review-20260911/power-loop-design-results.json).

USB-C has separate5.1kΩ Rd resistors on CC1/CC2; A6/B6 and A7/B7 are paired correctly, SBU is unused, and VBUS is sense-only. All three MAX3226 devices have the TQFN power, charge-pump and UART/RS232 pin mapping. SW1's physical common-terminal pairs map correctly to NRST and GND; it does not short reset permanently. Header and battery-retainer drawings were checked in the digital pass.

## Remaining implementation and assembly qualifications

These are unchanged boundaries, not newly found wiring errors:

- USB/SDMMC now have the48MHz clock configuration. Future firmware must implement PE0-based USB VBUS attach/detach, PSRAM initialization/access restrictions and applicable STM32 errata, safe acid-driver startup, and bounded valve pulses. No generated firmware exists to test.
- BT1's3013 MPN specifies the holder, not the coin cell. Select the cell/chemistry and matching RTC charge settings. R2 is an intentionally temporary10kΩ shunt: at3V it draws300µA and must follow the recorded removal-after-setup instruction.
- HSE/LSE startup, ADC-reference noise, I2C cable rise time, SD hot-plug behavior, switched-device back-power behavior, source/load concurrency, motor stalls/inrush and thermal/EMC performance require hardware tests.
- J2 is the accepted2.54mm debug header; use its matching cable/adapter. JP1/J13 require controlled single-shunt population. Cable mating parts and pin orientation remain assembly documentation, not additional on-board MPN gaps.

## Analyzer results and false-positive triage

Ran KiCad10 root netlist export, ERC and PDF export; `analyze_schematic.py`; BOM-manager read-only analysis; `analyze_pcb.py --full`; `cross_analysis.py`; `analyze_thermal.py`; `analyze_emc.py`; lifecycle audit; native pcbnew component/pad/library comparison; official-netlist delta; and the deep-review evidence gate.

The schematic analyzer counted292components but353nets versus KiCad's authoritative347. Its heuristic connectivity is not used to establish electrical findings. Specifically:

- Input-power path warnings miss the hierarchy's P_IN connection; the official netlist establishes the DC path.
- Motor-driver/enable voltage-domain warnings confuse motor supply with logic-input thresholds.3.3V logic is appropriate for these interfaces.
- Sense pins do not need pull-ups; EN pins with explicit bias do not need speculative additional pull-ups. Unused PGOOD outputs may remain unconnected.
- J3/J4 carry differential bridge-output pairs; J13 is a supply selector. Missing-ground-pin warnings are not applicable to their intended function.
- DS-002 reflects lack of the analyzer's specific `datasheets/` cache, not absence of manufacturer documents. The manual pass uses original PDFs under `Docs/` and prior evidence folders with provenance; incomplete exact-document coverage is disclosed above.

The native PCB check found **292footprints,1467physical pads, no missing library footprints/pads, and no substantive value/MPN/footprint/net mismatch**. Twelve textual net-name differences were only KiCad's `{slash}` escape representation. The board remains a staging grid with **zero tracks/vias, zones or outline**. [Board audit](../analysis/read-only-review-20260911/board-audit.json).

Cross-analysis returned no findings. EMC returned57 largely staging-dependent findings; absent planes, distance-to-decoupling and connector-placement results do not describe a completed layout. Its numerical score is not a compliance result. Thermal analysis assessed only one component with an assumed load and is insufficient for thermal approval; its apparent perfect score is rejected as meaningful evidence.

Lifecycle audit attempted82unique MPNs but obtained **unknown** status for all82. This is a failed availability/lifecycle evidence check, not proof that the parts are obsolete, and its automatic replacement suggestions are rejected. It also does not override the complete MPN inventory from the official netlist.

No ngspice, LTspice or Xyce executable was found in PATH or the common installation directories checked, so SPICE was not run. No gerber/fabrication review or routed-board DRC was performed: there is no layout to evaluate. No placement, routing, source edits, code generation, build or bench tests were performed.

## Evidence and trust

High-confidence observations come from fresh official KiCad connectivity/ERC, source properties, native PCB pad checks, and the manufacturer pin/requirements evidence cited in the subsystem reports. Oscillator operation, load protection adequacy and real-world transient/thermal performance remain conditional. The deep-review gate accepted7evidence-linked entries with zero quarantined entries; that checks evidence structure/anchors, not physical circuit operation.

Read-only source hashes and final comparison are in [source-integrity.json](../analysis/read-only-review-20260911/source-integrity.json). The [fresh ERC report](../analysis/read-only-review-20260911/erc.json) and [schematic PDF](../analysis/read-only-review-20260911/schematic.pdf) correspond to this review.
