# Schematic repairs — 11 September 2026

**Implemented the supported circuit and library repairs. Not every review finding is closed:** remaining work concerns fuse selection/protection, motor and valve operating limits, firmware, and physical qualification. The user has confirmed the existing KNF supply,12V LI-830/valve supply, K96 interface and actuator interface. The shared **6.6V rail and its setpoint remain unchanged**, as requested.

Root KiCad10 ERC now reports **0 errors and0 warnings**, compared with46 errors and38 warnings before these repairs. Independent resolved-netlist checks found only the intended connection changes. A clean ERC does not establish hardware compatibility or fabrication readiness.

## Applied repairs

| Review finding | Final change | Status |
|---|---|---|
| U34/U39 RS-232 package mismatch | Correct TQFN symbols, all16 signal/supply pins remapped, EP17 grounded. U34/U39/U40 MPNs completed toMAX3226EETE+. | Fixed; pin/net checks passed |
| D10 reversed unidirectional TVS | Unidirectional symbol, cathode/pad1 toP_IN, anode/pad2 toGND. SMBJ18A retained. | Fixed |
| J31 contradictory pinout comment | Comment now agrees with wiring: pin1GND, pin2positive throughF10. | Fixed in design; harness must follow it |
| F10 nominal fuse rating | Changed10A to8A, Littelfuse0451008.MRL, with the existing footprint, following user selection. | Applied; ERC clean |
| U10 compensation | R10610kΩ, C104100nF, C1051nF, with corresponding MPNs and footprints. | Redesigned; bench loop/load-step test remains |
| Module effective output capacitance | Added C901–C904:180µF/16V Panasonic16SVPF180M polymer on3V3/5V/6V6/2V8, retaining the ceramics. | Capacitance reserve added; physical qualification remains |
| U20–U22 DRV8823 footprint | New device-specific land/stencil pattern:3.70×3.65mm EP,0.30×1.55mm lead lands,0.5mm pitch, correct SMD attribute. Updated placed and default library footprints. | Fixed; future PCB thermal vias still required |
| VREF+ decoupling | Added C43=1µF afterFB1 alongside100nF C27. | Fixed |
| NRST filtering | Changed C21 from2.2nF to100nF and selected matching MPN. | Fixed |
| Undefined startup states | Added100k COMM_EN, RTC_CE and RTC_CLKOE pull-downs (R348–R350). Moved acid RESET pull-down R323 toGND. | Hardware bias fixed; application sequencing still required |
| Auxiliary PMOS at3.3V | Q1 changed toAO4630 SOIC8, specified at−2.5V gate drive; existing clamp retained. | Gate-drive compatibility fixed; load/thermal limits remain |
| USB clock configuration | LiveIOC now explicitly uses8MHz HSE,16MHz mainPLL/system clock and48MHz PLLSAI1 for USB/SDMMC. Hardware VBUS sense disabled for the PE0 software-sense topology. | IOC fixed; runtime USB software remains |
| ERC/library/annotation defects | Correctly marked unused pins; declared real power feeds after resistors; repaired off-grid bends and dangling stubs; synchronized14 custom symbols; made power references unique. | Fixed, no new ERC suppressions |
| Electrolytic polarity clarity | C100/C41/C113 now use polarized symbols with unchanged numbered connections. | Fixed |

The compensation calculation covers9,216 parameter corners, including capacitor tolerance/temperature sensitivity, inductance variation and a one-cycle delay. The final averaged model gives minimum60.40° phase margin,10.95dB gain margin and maximum6.846kHz crossover. These are modeled values, not measurements or a switching simulation. See the [calculation and bounds](fixes-2026-09-11/power-fixes.md) and [executable model](fixes-2026-09-11/power-loop-design.py).

## User-confirmed operating choices

On11September2026 the user accepted6.6V for KNF, the existing12V supply for LI-830 and valves, the existing K96 interface, and the existing actuator/controller interface. These supply/interface decisions are closed on that basis and the circuits are retained. [Decision record](design-decisions-2026-09-11.md). This does not label unperformed bench tests as passed.

## Findings that remain open

| Finding | Why it is still open | Required next input/action |
|---|---|---|
| F10/J31/source coordination and reverse/transient protection | F10 changed to8A per user selection; source/fault energy and time-current coordination remain physical design checks. | Retain the selected8A fuse and validate source/cable fault and startup behavior. |
| KNF overload protection | User confirmed6.6V operation; voltage decision is closed. The present≈2.47A switch limit is not a specified pump overload limit. | Establish startup/fault-current and protection requirements; no supply change requested. |
| Acid-pump winding and valve pulses | Exact winding current/drive limits and valve maximum pulse/polarity are missing. | Installed RP-TX winding and Bürkert article sheets; qualify current, pulse timing and firmware fault behavior. |
| LSE/HSE, signal integrity, PDN and thermal performance | No populated PCB or measured parasitics exist. Changing crystal capacitors would not establish startup margin. | Layout followed by oscillator/load-step/temperature/EMC and electrical qualification. Confirm effective input capacitance and complete power budget. |
| Runtime firmware and exact PSRAM restrictions | OnlyIOC inputs exist. Software USB attach/detach, PSRAM initialization/transaction timing, actuator/pump protections and bounded valve pulses are not application code. | Implement and test when firmware generation/application work is requested; obtain the exact installed PSRAM datasheet. Memory remains8MB volatile PSRAM. |
| Deferred hardware choices | BT1,J2,JP1,P1,SW1 were explicitly left unselected. | Select battery/holder, debug header, boot header, USB-C plug and reset switch. |

These are unresolved requirements or physical tests, not successful fixes. No arbitrary external interface, winding rating, cable or power-source limit was substituted.

## Final verification

- KiCad10.0.4 root netlist and ERC completed.290 components and343 nets;8 new components, no component removals.
- Complete existing-pin connectivity comparison passed after accounting for U34/U39 package renumbering, grounded EPs, D10 polarity, R323 bias and removal of Q1's obsolete duplicate drain pads. All other existing connectivity was preserved.
- All assigned footprints exist and contain their required pin numbers.285/290 components have footprints;278/283 purchased components have MPNs. The same five deferred parts account for all missing fields. TP20–TP26 are fabricated test points and are now excluded from the purchased BOM.
- Independent digital clock arithmetic and interface pin-map checks passed. CubeMX database keys were checked; no generated firmware or runtime/build test exists.
- Final schematic analyzer ran. Edited diagrams were exported and visually inspected; whitespace checks passed. Existing four ignored ERC categories are unchanged (single global label, four-way junction, simulation-model and footprint-filter checks).
- No PCB DRC/fabrication sign-off is possible because the PCB remains an empty placeholder. Earlier EMC/thermal scores on that placeholder are not meaningful. No standalone SPICE simulator was available; the compensation calculation is an averaged analytical model. Procurement/lifecycle availability remains unverified.

## Reviewable outputs

- [Updated schematic PDF](updated-schematic-2026-09-11.pdf)
- [Every component: final MPN, footprint and pin-net map](component-audit-after-fixes-2026-09-11.md)
- [Power repair detail](fixes-2026-09-11/power-fixes.md), [digital repair detail](fixes-2026-09-11/digital-fixes.md), [load repair detail](fixes-2026-09-11/loads-fixes.md)
- [Machine-readable validation](fixes-2026-09-11/validation.json) and [source hashes](fixes-2026-09-11/source-hashes.json)

The editable sources are the live KiCad schematics/project library and `Firmware/DIC/DIC.ioc`. Pre-existing user changes were retained. Detailed baseline snapshots, intermediate netlists and original evidence remain under the ignored `analysis/fixes_20260911/` directory. This repair report supersedes the earlier review's open/closed status; the earlier reports remain historical evidence.
