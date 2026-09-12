> Final-state override: this appendix records the initial electrical review. Metadata gaps for U1/U2/U10, passive parts and Micro-Fit connectors are now resolved except BT1/J2/JP1/P1/SW1. R103 is WSL25126L800FEA; FB1 is BLM18AG601SN1D; R329 is now487Ω,0.1%, giving60.159–239.366mA nominal phase-current range. R328 is also0.1%. Valve sense resistors are0.2W. These changes do not close the outstanding electrical findings. See the main review and final ledger.

# Power schematic review — 2026-09-11

## Scope and verdict

Reviewed every component in `/Power/`, `/Power/12V/`, `/Power/3V3/`, `/Power/5V/`, `/Power/6V6/`, and `/Power/2V8/`. This report is based on the initial `resolved.net.xml`; the parent review may subsequently enrich BOM fields. Connectivity exclusively follows that KiCad hierarchical export, not analyzer geometry. The power circuit is **not ready for hardware release**. Input TVS polarity, connector pin documentation, and the main converter compensation require correction or resolution. No populated PCB exists, so thermal, return-path, current-density and assembly performance remain open.

New manufacturer PDFs are in `power-datasheets/`: TI TPS552882 SLVSFC5, TPSM53603 SNVSB77B, CSD18542KTT SLPS316B; Bourns CSS2H-2512; Coilcraft XAL1010; Vishay WSL. Existing `Docs/README.md` and manifest were consulted: the power-component datasheets are not part of that prior archive. A separate local provenance manifest records new evidence; **the two downloaded SMBJ PDFs are Access Denied responses and must not be treated as component evidence**. The Littelfuse manufacturer indexed table was readable online, but successful original-PDF retrieval remains a gap.

## Blockers and important risks

| ID | Priority / confidence | Finding and required action |
|---|---|---|
| PWR-01 | P1 / deterministic netlist + installed footprint; manufacturer MPN polarity | D10 is instantiated with a bidirectional `A1/A2` symbol but specified as unidirectional SMBJ18A. Netlist pad1=GND, pad2=P_IN. Installed KiCad D_SMB places its cathode bar at pad1. Normal assembly therefore connects the real TVS cathode to ground and anode to positive input, forward-biasing it and likely blowing F10 or current-limiting the source. Use a correctly pinned unidirectional symbol and connect cathode to P_IN, anode to GND; recheck netlist and assembly polarity. Choosing SMBJ18CA instead changes protection behavior and is not an equivalent metadata repair. |
| PWR-02 | P1 / deterministic | J31 BOM comment specifies pin1=positive, pin2=GND, but netlist is **pin1=GND, pin2=F10.1**. A harness made to the comment reverses supply. Resolve the intended harness convention, then synchronize comment, schematic and assembly instructions. Do not silently make a cable assumption. |
| PWR-03 | P1 / equation-backed design concern | U10 compensation uses R106=49.9Ω, C104=10nF in series to ground, with C105=100pF directly COMP-ground. The compensator zero is `1/(2π·49.9·10nF)=319kHz`, above the converter's 400kHz/10 upper crossover guideline. This provides very little phase lead at normal loop crossover. TI §8.2.2.8 requires design of R/C from the actual output capacitance/load and at least 45° phase margin/10dB gain margin. The present network needs an averaged/switching-model Bode design and load-step validation. A typical first-order estimate at 8.64V input,12V/5A output,308µF gives approximately 1.3kHz crossover and only ~18° margin before ESR effects; this is a screening calculation, **not a simulation or proof of oscillation**. Do not merely replace 49.9Ω by 49.9kΩ without designing the loop. |
| PWR-04 | P1 / manufacturer ratings + conditional load calculation | F10=10A exceeds J31's published 8.5A maximum per contact; actual cable/wire/temperature rating may be lower. U10 settings allow 7.35A output and 13.25A average inductor current. Delivering 12V×7.35A at 8.64V input and an illustrative 90% efficiency requires ~11.35A input, before 3V3 load. A 10A fuse does not cap continuous current at 8.5A. Establish simultaneous load budget, startup/stall current, source voltage range, wire gauge and fuse time-current/I²t coordination; then change connector/protection/current limits as needed. |
| PWR-05 | P1 / manufacturer part-number evidence | Initial R103 MPN CSS2H-2512R-L0068F is not a valid documented 6.8mΩ member of the Bourns CSS2H-2512 family. The datasheet lists 0.3–5mΩ and encodes L500=0.500mΩ. Actual fitted resistance cannot be inferred from this string. A lead-free candidate is Vishay WSL25126L800FEA,6.8mΩ,1%,1W,2512; manufacturer WSL ordering table supports the code. At 7.35A nominal, power=.368W. Parent handles assignment. |
| PWR-06 | P2 / deterministic initial BOM | U10 initially has no footprint. A generic QFN footprint would be dangerous because pads24,25,26 are distinct PGND,SW2,VOUT conductors. An isolated project footprint was created from the exact RPM0026A land/stencil drawing; details below. |
| PWR-07 | P2 / rating/design gap | U11–U14 output capacitors are nominal 94µF each pair, but capacitance must be evaluated after DC bias,tolerance,temperature and aging. U11 requires43µF effective at3.3V; U12 requires28µF at5V; U13 around21µF at6.5–6.6V; U14 needs the intermediate requirement between48µF at3V and58µF at2.5V (use58µF conservatively until vendor confirmation). Murata GRM32ER61A476ME20L is a10V X5R family choice; in particular 6.6V bias can remove substantial capacitance. No exact DC-bias curves were captured. Nominal-value arithmetic is not a stability signoff. |
| PWR-08 | P2 / design gap | External source min/max/transients, reverse-polarity requirement and source impedance are unspecified (`Docs/README.md` gap12). No series reverse-polarity element appears between J31 and the rails. Even after D10 correction, relying on a TVS/fuse crowbar requires a source and pulse-energy specification. SMBJ18A standoff18V and clamp29.2V at20.6A do not authorize unrestricted surge exposure; a source above18V continuously is incompatible. |

## Power input and protection, every part

J31.2 → F10.1; F10.2 → P_IN. J31.1 → GND. TP20 probes pre-fuse input and TP21 probes P_IN. D10/C100/C101 span P_IN-ground. U10 and U11 draw directly from P_IN; U12–14 draw from regulated+12V.

- **J31:** exact 0430450200 footprint family matches a 2-position dual-row Micro-Fit3.0 right-angle header, despite the generic connector symbol's1×N footprint filter. The filter mismatch alone is not a physical error. Manufacturer lists8.5A maximum, application-dependent. Pin convention conflict is real.
- **F10:** 0451010.MRL/10A and Littelfuse451/453 package are consistent. Fuse interrupt rating, opening time, pulse survival and connector/wiring coordination cannot be closed without source current and startup energy.
- **D10:** see PWR-01. Its18V standoff is a source constraint. TVS clamping must remain below controller and capacitor ratings under the actual surge waveform and wiring inductance.
- **C100:** EEHZA1V101P,100µF/35V hybrid electrolytic,8×10.5mm footprint selection; positive numbered pad1 is P_IN but symbol is nonpolarized, so polarity should be made visible. No local manufacturer ripple/ESR evidence was acquired; source hot-plug/inrush and ripple qualification remain open.
- **C101:**100nF GRM155R71H104ME14D/0402,50V class; correct shunt topology. Part-level DC-bias/temperature details not independently captured.
- **TP20/TP21:** bare plated holes, not purchased components. Treat as explicitly non-BOM copper features or assign actual test hardware if that is the intended assembly.

## U10 main12V buck-boost, every part

The topology matches TI's four-switch converter architecture with two external buck-side MOSFETs and internal boost leg. U10.1 DR1L→R115→Q101.1; U10.2 DR1H→R114→Q100.1. Q100.2 is P_IN,Q100.3 is SW1; Q101.2 is SW1,Q101.3 is GND. L10 connects SW1 to SW2. U10.23=SW1;21/25=SW2. C102 is BOOT1(22)-SW1; C103 is BOOT2(20)-SW2. U10.11/26 and ISP12 join pre-shunt output; R103 connects that node to+12V/ISN13. Feedback senses downstream of R103, so shunt loss is compensated. Grounds9,10,24 join GND. This mapping agrees with TI's pin table and CSD18542KTT pin1=G,pin2/tab=D,pin3=S.

| Parts | Function / reviewed result |
|---|---|
| U10 | TPS552882RPMR,2.7–36V input;12V output within range. PG5/CC6 open are unused status outputs. CDC16 open disables added cable compensation; no CDC resistor is required for the basic regulator. |
| R100150k,R10124.9k | UVLO: `1.23×(1+150/24.9)=8.640V` turn-on; nominal hysteresis `5µA×150k=.750V`, turn-off≈7.89V. 1% resistor-only ratio range gives approximately8.49–8.79V before IC threshold tolerance. Appropriate only if the selected supply can support the corresponding boost input current. |
| R10249.9k | FSW≈400kHz; below TI's recommended500kHz bound for high-current applications. |
| R11224.9k | MODE selects internal VCC and PFM at light load; does not leave VCC dependent on an absent external5V source. |
| R11324.9k | Average inductor limit≈330000/24900=13.25A for12V output. This is not a precise input-current fuse or system load budget. |
| R1036.8mΩ |50mV sense threshold gives7.353A typical output limit;48–52mV with1% resistor gives6.99–7.72A before thermal drift. Dissipation at nominal limit=.368W; Kelvin sensing necessary. Initial MPN defective, see PWR-05. |
| R104100k,R10511.1k | Vout=`1.2×(1+100/11.1)=12.0108V`. With1% reference and1% resistors, worst-case approximately11.679–12.352V; nominally suitable for a12V±5% load, but transient/ripple margin remains. Feedback divider power is small (<2mW). |
| R106,C104,C105 | Compensation network exists, but49.9Ω is suspect by pole-zero calculation; see PWR-03. C10410nF/C105100pF are not general bypass capacitors. |
| C11910nF | DITH/SYNC toGND enables frequency dithering; its MPN initially missing. Not a floating sync-input error. |
| Q100/Q101,R114/R115 | CSD18542KTTT60V logic-level TO263,1Ω gate resistors. Gate/pad mapping matches manufacturer. Datasheet guarantees RDS at4.5V, compatible with controller5.2V drive; using MOSFET threshold alone would not establish this. Conduction,gate-drive,switching and junction-temperature losses still need load/PCB evidence. |
| L104.7µH | XAL1010-472MEB: manufacturer table4.7µH,5.7mΩ max DCR,25.4A saturation reference,17.5A RMS for20°C rise. Meets controller minimum `L>1.2/fSW=3µH` nominally; at-20% initial tolerance3.76µH still exceeds3µH, but hot DC-bias inductance also matters. At8.64→12V/400kHz ripple≈1.29App; at13.25A DC winding loss≈1W before core loss. No PCB thermal conclusion. |
| C102/C103100nF | Bootstrap capacitors across the correct boot-switch nodes; nonpolar capacitor terminal reversal is harmless. Qg~22nC class at4.5V implies ~.22V droop per100nF before bias/parasitics; no missing external bootstrap diode is inferred because TI describes the internal charge path. |
| C10610µF | VCC-ground bypass,25V1206. Controller reference uses4.7µF;10µF nominal is a reasonable topology match pending effective capacitance/startup confirmation. |
| C107/C10810µF,C41100µF,C42100nF | Input capacitor network on P_IN. C41/C42 initially lack MPN/footprint. TI example uses4×10µF ceramic; actual required ripple/hot-plug performance needs source/load analysis.100µF bulk is not an automatic replacement for close high-frequency ceramics. |
| C109–11222µF,C113220µF,C40100nF | All connect pre-shunt output toGND. Nominal total308.1µF. C109–112 initial MPN GRM32ER71E226M lacks full suffix; GRM32ER71E226ME15L is manufacturer-listed22µF±20%,25V,X7R1210. C113 EEHZA1E221P is25V hybrid electrolytic,8×10.5mm; pin1 positive net matches. Nonpolar symbol hides physical polarity. Exact ESR,DC bias and ripple needed for compensation. C40 initially missing metadata. |
| TP22 |+12V copper test hole. Non-BOM feature unless actual hardware is specified. |

## U11–U14 module converters, every part

All modules use TPSM53603RDAR and the installed Texas_B3QFN14+EP footprint family. Pins1/14=VIN,7/8=VOUT,9=FB,2=EN,12=AGND,15=PGND. Pins3/10/11 NC tied ground are recommended by TI for shielding/thermal; pins4/5 DNC are separately unconnected as required. Pin6 PGOOD may be open when unused. Pin13 V5V open is acceptable: the datasheet does not require an external bypass there. Avoid elevating analyzer warnings for these pins into defects.

| Stage / all remaining components | Results |
|---|---|
| U11;R10910k/R1104.32k;C115/C11610µF,C117/C11847µF,C34/C350.1µF;TP23 | Direct P_IN→3V3,EN directly tiedVIN is explicitly allowed. Nominal3.3148V; with±1% resistors and±1.5% reference, conservative3.220–3.412V. C115/116/C35=input;C117/118/C34=output. Always-on3V3 permits MCU to enable other rails; no circular startup dependency is present. |
| U12;R11610k/R1172.49k;R21100k;C121/C12210µF,C123/C12447µF,C38/C390.1µF;TP24 |12V→5V,nominal5.0161V; tolerance estimate4.863–5.174V. EN=MCU PF1(U1.11),R21 pulldown ensures disabled reset state. C121/122/C39=input;C123/124/C38=output. |
| U13;R11910k/R1201.78k;R22100k;C126/C12710µF,C128/C12947µF,C32/C330.1µF;TP25 |12V→6V6,nominal6.6180V; tolerance estimate6.409–6.832V. EN=PF2(U1.12),R22 pulldown. C126/127/C32=input;C128/129/C33=output. A nominal6V external load cannot automatically be approved at6.6V; pump-specific limits belong in actuator review. |
| U14;R12310k/R1245.56k;R20100k;C130/C13110µF,C133/C13447µF,C36/C370.1µF;TP26 |12V→2V8,nominal2.7986V; tolerance estimate2.722–2.878V. EN=PF0(U1.10),R20 pulldown. C130/131/C36=input;C133/134/C37=output. External pump/controller evidence must establish whether2.8V is the right rail. |

The tolerance estimates combine min/max divider ratios with the1V reference's±1.5% design envelope; use exact load/line/temperature conditions when creating requirements. Each module's3A maximum is not an approved simultaneous operating point. Driving5V,6.6V and2.8V at3A simultaneously would require43.2W before conversion losses, plus12V-direct loads and MCU supply. Every10k feedback top resistor and associated bottom resistor has negligible steady-state dissipation at its rail. All 100k EN pull-downs dissipate0.109mW at3.3V; EN thresholds accommodate3.3V logic. Input two10µF/50V1206 capacitors match the nominal TI minimum20µF but tolerance/bias margin must be checked. Add local nonceramic bulk if required by line/load transient tests; TI recommends47µF for transient-load applications.

## New U10 footprint

Created `DIC_Board:Texas_RPM0026A_TPS552882` using TI SLVSFC5 pp39–40 drawing4224618/A,RPM0026A. It has26 unique pad numbers,4×3.5mm body,custom L-shaped corner pads1/7/13/19,manufacturer land-pattern centers and widths,and0.05mm typical corner radii. Center pads24/25/26 are separate0.375×1.425mm strips atx=-.625/0/+.625mm. Copper/paste/mask apertures follow the1:1 example for0.1mm stencil. KiCad10 CLI exported SVG successfully and the output was visually compared to the manufacturer land/stencil pages. `rpm-pad-audit.json` records dimensions and hash. No vias are inserted; SW2 and VOUT thermal pads **must never be blindly joined to GND**. Footprint assignment is left to the parent. PCB-placement/routing and stencil-process review remain required.

## Review limits / false positives

This subreview did not run a separate geometry parser or infer missing connections from drawings. Root review owns ERC, analyzer triage and simulator availability; no SPICE simulation was performed here. DNC isolation,NC-ground,V5V open,PGOOD unused,CDC open and directVIN→EN were explicitly checked against TI documentation and are not defects. Missing copper/thermal vias on the two-line PCB placeholder are a project-stage limitation, not hundreds of independent layout errors. Lifecycle/distributor stock was not established for every passive. All exact capacitor bias/ESR/ripple and input-source transient questions remain open; this report does not claim every physical component is electrically qualified.

## Sources

- TI TPS552882: https://www.ti.com/lit/ds/symlink/tps552882.pdf (pin tablespp3–4;limitspp5–8;settingspp14–18;design/compensationpp21–25;packagepp38–40).
- TI TPSM53603: https://www.ti.com/lit/ds/symlink/tpsm53603.pdf (pin tablep3;ratingspp4–6;feedback/capacitancepp12–14;enablep15).
- TI CSD18542KTT: https://www.ti.com/lit/ds/symlink/csd18542ktt.pdf (pinoutp1,electrical/gate chargep3).
- Bourns CSS2H-2512: https://www.bourns.com/docs/product-datasheets/css2h-2512.pdf (available resistances and ordering,p1).
- Vishay WSL: https://www.vishay.com/docs/30100/wsl.pdf (ratings and ordering,p1).
- Coilcraft XAL1010: https://www.coilcraft.com/getmedia/dd74e670-e705-456a-9a69-585fe02eaf3c/xal1010.pdf (4.7µH entry,p1).
- Molex0430450200 manufacturer product data: https://www.molex.com/en-us/products/part-detail/0430450200?display=pdf&download=true ; current derating application note/specification https://www.molex.com/content/dam/molex/molex-dot-com/products/automated/en-us/productspecificationpdf/430/43045/PS-43045-001.pdf?inline= .
- MurataGRM32ER71E226ME15L official exact part listing: https://www.murata.com/en-us/products/productdetail.aspx?partno=GRM32ER71E226ME15%23 .
- LittelfuseSMBJ manufacturer indexed electrical table: https://www.littelfuse.com/~/media/electronics/datasheets/tvs_diodes/littelfuse_tvs_diode_smbj_datasheet.pdf.pdf (original download blocked).
