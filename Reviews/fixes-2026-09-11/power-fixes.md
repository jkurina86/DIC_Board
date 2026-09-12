> Final integration: root ERC is clean. Shared project libraries are synchronized; RTC bias labels now use global labels; fabricated TP20–TP26 are excluded from BOM; power references are unique; C100/C41/C113 now display polarity. The integrated netlist and validation in this folder supersede intermediate snapshots mentioned below.

# Power fixes — 11 September 2026

## Implemented source changes

Only the following six schematic files were changed by the power agent: `Power.kicad_sch`, `12v.kicad_sch`, `3v3.kicad_sch`, `5v.kicad_sch`, `6v6.kicad_sch`, `2v8.kicad_sch`. Existing metadata and other user changes were preserved. Backups of each file immediately before these edits are under `power-before/`; the coordinator also captured the complete baseline.

1. **D10 polarity corrected.** Replaced the bidirectional `Device:D_TVS` symbol with the standard unidirectional `Device:D_Zener` symbol and reversed its orientation. MPN remains Littelfuse SMBJ18A. The post-edit authoritative hierarchical XML shows **D10.1/cathode=P_IN and D10.2/anode=GND**. Its SMB footprint therefore assembles with the correct cathode-band polarity. BOM description now explicitly states this polarity. No alternate TVS protection behavior was substituted.
2. **J31 documentation corrected.** The BOM comment now matches existing electrical connectivity: **pin1=GND, pin2=external positive supply through F10 to P_IN**. No connector pin or harness electrical assignment was changed.
3. **U10 compensation redesigned.** Final values: **R106=10kΩ**, Vishay `CRCW040210K0FKED`; **C104=100nF**, TDK `C1608X7R1H104K080AA`,50V,X7R,10%,0603; **C105=1nF**, TDK `C1608C0G1H102J080AA`,50V,C0G,5%,0603. Original values were49.9Ω/10nF/100pF. Only values/MPNs/footprints changed, not compensation topology. An intermediate470pF candidate was rejected after broadening the modeled corner sweep; **1nF is the final source value**.
4. **Post-shunt supply declaration added.** `#FLG901` is on+12V after R103. This documents the actual source path from U10.VOUT through the passive current-sense resistor; it does not invent a supply on an undriven net. This resolves the ERC supply-type discontinuity without changing connectivity. The label was positioned clear of TP22.
5. **Module output bulk added.** C901(+3V3),C902(+5V),C903(+6V6),C904(+2V8) each use Panasonic **16SVPF180M**,180µF,16V,±20%,22mΩ maximum ESR at100kHz,3.3A ripple rating at100kHz/105°C,5000h endurance at105°C. Footprint `Capacitor_SMD:CP_Elec_6.3x5.9` explicitly represents Panasonic C6. Polarized symbols show pad1 positive/pad2 ground. Both existing47µF ceramic capacitors and100nF bypass remain on every output.

**The+6V6 net, its feedback divider and its nominal6.6V setting are unchanged**, following the user's explicit requirement. The user subsequently selected8A F10 (0451008.MRL). No shared12V setpoint, connector or electronic current-limit setting was changed.

## Connectivity and visual verification

KiCad10 exported `power-after.net.xml` from the root `DIC_Board.kicad_sch`. Comparing existing power-component pin nets with `before.net.xml` found exactly two changed entries: D10.1/GND→P_IN and D10.2/P_IN→GND. The four new capacitor positive pins are on their respective rails and all negative pins are GND. Existing power component count increased from82 to86.

The export predates the final470pF→1nF metadata-only refinement and flag-text repositioning; neither changes an electrical net. The coordinator's final export/ERC is authoritative for the integrated design. KiCad SVG output was visually inspected for the added3V3 bulk capacitor and main12V compensation circuit; all power-sheet SVGs are available in `power-svg/`. No populated PCB exists, so this work cannot establish routing, thermal paths or assembly readiness.

## Compensation design and evidence

The executable `power-loop-design.py` uses TI TPS552882 SLVSFC5 §8.2.2.8, equations19–26, with `gm=190µA/V`, internal equivalent sense resistance0.055Ω and reference1.2V. For the boost region:

```
Rload = Vout/Iout
D = max(0, 1 - Vin/Vout)
Gp(s) = Rload(1-D)/(2 Rsense)
        × (1 + s ESR Cout) × (1 - s L/[Rload(1-D)^2])
        / (1 + s Rload Cout/2)
Zcomp(s) = (Rc + 1/[s Cc]) || 1/[s Cp]
T(s) = Gp(s) × gm × Zcomp(s) × Vref/Vout × exp(-s/fsw)
```

For the buck region the script setsD=0 and removes the boost right-half-plane zero as a conservative proxy; it is not a complete switched buck/buck-boost model. One400kHz cycle of transport delay is included as sensitivity. The final compensator zero is159.2Hz; its high-frequency pole is approximately16.1kHz. This replaces the original318.9kHz compensator zero, which supplied almost no phase lead near crossover.

The final sweep includes **9216 corners**: Vin7.7/8/12/18V; Vout11.68/12.35V; Iout0.1/1/5/7.72A; Cout100/220/500µF; equivalent ESR0/10/100mΩ; resistor±1%; C104 initial±10% combined with X7R temperature±15% (0.765–1.265 multiplier), C105 independently±5%; inductor±20%; transconductance±20% engineering sensitivity. Every sampled corner has one0dB crossing. Results in `power-loop-design-results.json`:

- Minimum modeled phase margin: **60.40°**.
- Minimum modeled gain margin: **10.95dB**.
- Highest modeled crossover: **6.846kHz**, below40kHz (fsw/10).

The100µF low-Cout case is intentionally below the123.2µF result of220µF C113 at-20% initial tolerance and a further-30% endurance change, before any ceramic capacitance. The500µF upper case covers the original308µF nominal output network with generous positive tolerance and additional equivalent loading. These are **design/sensitivity bounds**, not measured capacitance across temperature. The datasheet's low-temperature ESR-after-endurance allowance for a hybrid capacitor does not reduce to a single frequency-independent ESR; actual parallel ceramic/hybrid impedance and layout parasitics still need measurement/modeling.

The model is a useful basis for the component correction, **not SPICE, a switching simulation, measured gain/phase margin or proof of performance at every operating point**. PFM/light-load behavior, control saturation, mode transitions, constant-power loads, startup and large load steps need bench validation. The source7.7–18V range comes from exploring below nominal UVLO turn-off to the TVS standoff; it is not a new declared external-source specification.

## Module bulk-capacitor rationale

TPSM53603 datasheet §6.3 specifies maximum output capacitance1000µF; Table7-1 gives rail-dependent effective minimums, and §7.3.4 permits low-ESR polymer capacitors. Its explicit requirement that20µF be ceramic applies to **input** capacitance (footnote5). The existing ceramic output network is preserved while adding polymer reserve.

Each rail now has274µF nominal output capacitance, or328.8µF at+20% tolerance, well below1000µF. The new polymer alone contributes144µF at-20% initial tolerance and115.2µF after another-20% endurance change. This exceeds the largest conservatively used58µF requirement without counting ceramic nominal capacitance. Exact temperature/frequency capacitance should still be included in hardware qualification; the change avoids relying on an unmeasured MLCC DC-bias curve to provide the entire reserve.

Panasonic's current exact product page lists22mΩ ESR and the manufacturer's catalog includes16SVPF180M/C6 dimensions. TI's recommended polymer examples include18mΩ and35mΩ devices, so this22mΩ addition lies in that practical low-ESR range while the ceramic network handles high-frequency current. No claim is made that the entire possible ESR/Cout plane is approved solely by this comparison.

At the nominal4ms module soft-start, charging the added180µF at6.6V requires about0.297A average, or0.356A for+20% capacitance. Charging the complete328.8µF upper-tolerance bank would require about0.543A. These are typical-ramp arithmetic, not guaranteed peak-input-current values. Soft-start minimum timing, simultaneous active loads and the upstream source still require startup testing. Each added polymer's specified worst-case leakage is576µA; the always-on3V3 rail can therefore gain up to that leakage budget, and all four together up to2.304mA when powered.

## Remaining external decisions and tests

- **Input protection:** F10 is now8A, Littelfuse0451008.MRL, in the existing footprint, following the user's acceptance of the standard8A alternative. Source/cable fault energy, startup and time-current qualification remain separate.
- **KNF supply confirmed by user:** retain6.6V for the installed pump. The separate overload/current-limit requirement remains open.
- **LI-830/valve supply accepted by user:** retain the existing nominal12V supply. The prior request for a supply decision is closed; no new measurement or manufacturer limit is asserted.
- **Power-source surge/reverse-polarity and fuse energy remain specification-dependent.** Corrected D10 polarity fixes normal-operation forward conduction. It does not by itself qualify a complete reverse-polarity/cable-transient protection design.
- Bench gain/phase, startup, worst-case load-step, module/output-capacitor temperature, leakage and PCB thermal/routing verification remain necessary.

## Evidence files

- Original TI PDFs and source hashes: `analysis/review_20260911/power-datasheets/manifest.json`.
- New Panasonic current catalog: `power-evidence/SVPF-English.pdf`, catalogPDFpp34–35; product dimensions/ratings and endurance are included. Source: https://industrial.panasonic.com/cdbs/www-data/pdf/AAB8000/AAB8000COL87.pdf .
- Exact polymer product: https://na.industrial.panasonic.com/products/capacitors/polymer-capacitors/lineup/os-con-aluminum-polymer/series/91057/model/91080 .
- C113 exact rating evidence: https://industrial.panasonic.com/ww/products/pt/hybrid-aluminum/models/EEHZA1E221P ; ZA endurance source https://eu.industrial.panasonic.com/sites/default/pidseu/files/downloads/files/datasheet_conductive_polymer_hybrid_aluminium_electrolytic_capacitors_-_za.pdf .
- Applied edits: `power-applied.json`, `power-added-bulk.json`, `power-final-adjustment.json`; source scripts use the maintained BOM property editor and KiCad skill S-expression parser.
