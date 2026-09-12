> Final-state override: this appendix records the initial electrical review. Metadata gaps for U1/U2/U10, passive parts and Micro-Fit connectors are now resolved except BT1/J2/JP1/P1/SW1. R103 is WSL25126L800FEA; FB1 is BLM18AG601SN1D; R329 is now487Ω,0.1%, giving60.159–239.366mA nominal phase-current range. R328 is also0.1%. Valve sense resistors are0.2W. These changes do not close the outstanding electrical findings. See the main review and final ledger.

# MCU, memory, clocking, USB, SD, debug and communications review

Date: 2026-09-11. Scope: all 67 physical components on `/STM32 MCU/`, seven on `/Comms/`, and the U40 communications circuitry on `/Comms/Aux/`. Auxiliary Q1/D5/R345-R347/J13 power selection is covered by the loads review. No schematic or firmware edits made by this reviewer.

## Evidence and verdict

Connectivity below comes exclusively from `resolved.net.xml`, exported by Eeschema 10.0.4 from the hierarchy root on this review date. Component properties were cross-checked against that export and the current source. The geometric schematic analyzer is not electrical authority. References to data sheets below are limited to parts for which exact-family primary evidence was read. Remaining passive selections, connector mechanics, startup behavior and layout require closure; this is not an assertion that every component is electrically qualified.

The digital section is **not ready for layout release**: U39 has a package/pinout mismatch, firmware has no demonstrated USB clock, and VREF+ lacks its recommended local bulk decoupling. Most functional MCU assignments agree with the live CubeMX file. Existing design decisions in `analysis/schematic-design-review-2026-08-31.md` were preserved: P1 is intentionally a plug, R2 is an intentional temporary battery shunt, and the earlier RTC GPIO corrections remain valid.

## Findings

### DG-01 — P1 / critical: U39 pin numbering is incompatible with its TQFN part

Confidence: datasheet-backed package mismatch + deterministic connectivity.

U39 is specified as MAX3226EETE, with `Package_DFN_QFN:TQFN-16-1EP_5x5mm_P0.8mm_EP3.1x3.1mm`, but uses the SSOP pin numbers: pin15 +3V3, pin14 GND, pin13 J11 TX, pin8 J11 RX, pin11 MCU TX, pin9 MCU RX, pins12/16 COMM_EN. The EETE TQFN uses VCC12, GND11, TOUT10, RIN5, TIN8, ROUT6, FORCEON9 and FORCEOFF13. Thus this is a physical wiring error, not merely an inaccurate footprint filter. U40 already uses the TQFN assignment. U34 shares U39's incorrect assignment and is discussed in the loads review.

Repair U39 using the exact TQFN pin map and preserve functional nets; a footprint-only or MPN-only update cannot correct it. Re-export the hierarchical netlist and compare every signal, supply and charge-pump capacitor endpoint. Analog Devices MAX3224E–MAX3245E Rev11, pp11–12 and ordering information p24: [primary PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/max3224e-max3245e.pdf). Do not use the older non-E-family URL currently on U39. U40's stale SSOP footprint filter is metadata, separate from its correct numbering.

### DG-02 — P1 / functional release gap: USB clock and software VBUS handling incomplete

Confidence: deterministic IOC inconsistency; implementation gap.

`Firmware/DIC/DIC.ioc` enables USB CDC and USB_OTG_FS, yet retains MSI=4MHz and PLLQ=16MHz and no explicit valid 48MHz USB clock configuration. The committed tree has no generated implementation to supply an alternative configuration. Configure the dedicated domain and validate it in CubeMX before claiming USB operation. ST AN4879 section2.4 specifies the USB clock requirement; the existing 8MHz HSE can support an appropriate clock-tree design.

The resolved USB_VBUS_SENSE net is PE0/pin141 via R23=33k high leg and R24=82k low leg, as intended by the prior review. PA9 is occupied by COMM_TX. Therefore firmware must disable the embedded PA9 VBUS detector and use PE0 to gate USB attach/detach; the IOC currently records only `USB_OTG_FS.VirtualMode=Device_Only`, without a demonstrated implementation of that handling. Check SDMMC kernel clock concurrently. These are requirements on the future generated firmware, not a claim that software absent from this repository has been tested.

### DG-03 — P2 / warning: VREF+ only has 100nF downstream of an unspecified ferrite

Confidence: datasheet-backed recommendation and deterministic net.

The entire reference net is U1.32, FB1.1, C27.1; C27=100nF returns to GND. FB1.2 connects +3V3. No 1uF exists on the reference side. ST AN4555 p17 recommends 100nF plus1uF for externally supplied VREF+, and the MCU datasheet power-supply figure also depicts 100nF+1uF. Add the local effective1uF and specify FB1 impedance, DCR/current capability and damping as part of the analog-reference design. Other +3V3 bulk capacitors are across the ferrite and do not replace local reference decoupling. Do not enable VREFBUF output into this externally driven net.

### DG-04 — P2 / warning: LSE loading has little unallocated capacitance margin

Confidence: exact crystal data plus calculated constraint; not a measured oscillator failure.

Y2 ABS06-107 uses C25=C26=6.8pF, yielding 3.4pF series load before pin/trace/stray capacitance. Abracon ABS06-107 datasheet p2 calls for effective4.0pF and no more than4.5pF for its stated gain margin. This leaves approximately0.6pF for nominal total parasitics and1.1pF to the stated ceiling. Establish the actual load/gain budget and select capacitor values accordingly; measure startup over voltage/temperature and use ST AN2867 methods. Do not assume 6.8pF is correct because it is a familiar LSE value. Y2 pin1 joins PC15/C25, pin2 PC14/C26; crystal interchange symmetry means this ordering itself is not a fault.

### DG-05 — P2 / warning: COMM_EN has no defined hardware reset state

Confidence: deterministic net, startup-risk inference.

COMM_EN consists only of U1.PA8/pin100 and U39.FORCEON/FORCEOFF. With MCU pins in reset, there is no external bias on the transceiver controls. `PA8.PinState=GPIO_PIN_RESET` establishes a software initialization level after startup, not a hardware reset state. Provide a suitable hardware pull-down if the intended safe state is off. U40 AUX_EN already has R346=100k to GND and is not affected by this finding.

### DG-06 — P2 / warning: NRST filtering is much smaller than ST's reference network

Confidence: deterministic values and manufacturer recommendation; susceptibility not tested.

R1=47k, C21=2.2nF, SW1 and R15=22ohm connect to U1.25 NRST. The nominal external RC is about103us before the MCU's internal pull-up. The STM32L476xx datasheet Figure32 recommends100nF close to NRST. Consider changing C21 to that reference value for this motor/pump environment, with a reset timing/debug check. The direct switch-to-ground and SWD reset connectivity are sensible; no reset short or missing path was found.

### DG-07 — P2 / release gap: exact PSRAM operating restrictions need full primary PDF and firmware implementation

Confidence: connectivity consistency and indexed exact-family manufacturer information; incomplete datasheet coverage.

U3 APS6404L-3SQRX-SN connects CE1 to PE11 with R6=10k pull-up, SCLK6 to PE10, SIO0/1/2/3 pins5/2/3/7 to PE12/13/14/15, VDD8 to3V3 and VSS4 toGND. The pin functions agree with the intended serial PSRAM interface and IOC. C30=100nF/C31=10uF provide the intended supply bypass/bulk network.

The official indexed ordering table establishes64Mbit (8MB),3V, SOP8, extended-temperature order code, not32MB and not nonvolatile MRAM. The legacy AP Memory PDF URLs currently redirect to the home page; a publicly cited new download instead returned APS6404L-SQN (1.8V, not installed), explicitly saved as `APS6404L-SQN_NOT_INSTALLED.pdf` and excluded from signoff. The exact installed PDF's full electrical/timing and package drawing remain a gap. [Indexed exact-family source](https://www.apmemory.com/wp-content/uploads/APM_PSRAM_QSPI-APS6404L-3SQR-v2.3-PKG.pdf).

Record startup/reset commands, maximum continuous CE assertion, row/wrap crossing limits, frequency vs voltage/temperature, refresh opportunities and standby/half-sleep retention behavior before firmware use. STM32 ES0250 Rev13 sections2.6.1,2.6.4–2.6.6 also require implementation review: command-only QPI transactions and memory-mapped timeout/transition cases have silicon limitations. There is no PSRAM driver in the repository to check. A general-purpose memory-mapped writable RAM assumption is not established merely by wiring QSPI.

### DG-08 — P2 / layout release gap: missing or incomplete exact metadata

Initial resolved export has60 missing MPN fields and25 missing footprints among67 MCU-sheet components, plus J11, J12 and J13 missing both in the communications sheets. Root review owns metadata enrichment; recount against its final export.

U1 value is a family/package symbol name STM32L476ZGTx; populate exact `STM32L476ZGT6` from the live IOC. U2's footprint can use installed `Package_SON:RTC_SMD_MicroCrystal_C3_2.5x3.7mm`: its 0.8x0.5mm lands on0.8mm pitch with x=±1.1mm match Abracon p7's0.5x0.8mm lands and1.4mm inner/3.0mm outer row span after90° rotation and bottom-view conversion. Datasheet rendered as `rtc-dimensions.png`. P1 must retain a mechanically compatible **plug** footprint, not an arbitrary receptacle. BT1 must identify chemistry, voltage, holder/battery MPN and polarity. FB1 presently has value `~`, so merely adding a footprint would not close its electrical selection.

## Coverage ledger and positive observations

| Components | Review disposition |
|---|---|
| U1 all144 pins | All supply, functional and explicitly unconnected nets inspected in resolved netlist. LQFP144 part selection is consistent; no conflicting digital alternate-function assignments found. No layout pad placement/routing exists to qualify. |
| C1–C20 | All connect +3V3/GND. Nine100nF general VDD bypasses plus C10=4.7uF; C11/C12/C13 and C14–C20 provide other domain bypass/bulk values. VDDA, both VDDIO2, VDDUSB and VBAT pins are connected to3V3; VSS/VSSA/VREF− are grounded. Local placement and exact effective capacitance remain untested. |
| R1,C21,SW1,R15 | Reset topology correct; see reduced filter recommendation DG-06. |
| U2,C22,R5 | All ten RTC pins match Abracon p7: CLKOE1, VDD2, CLKOUT3, SCL4, SDO5, VSS6, INT7, CE8, VBACKUP9, SDI10. C22=10nF is recommended bypass. R5=10k provides INT pull-up. |
| BT1,R2,R3 | R3=470ohm protection falls within Abracon application-manual p57's100–1000ohm recommendation. R2=10k is intentionally temporary; at3V it draws300uA. Setup documentation must record removal. Do not silently remove it or count battery life with it installed. Trickle-charge settings must match selected battery chemistry. |
| Y1,R4,C23,C24 | PH0/Y1.1/C23 and PH1/R4/Y1.2/C24 topology correct.8MHz agrees with IOC HSE.12pF pair gives6pF plus parasitics versus crystal nominal8pF load. R4=0ohm permits future drive tuning. Worst-case ESR/gain, drive and layout still require oscillator qualification. |
| Y2,C25,C26 | PH0/PH1 versus PC14/PC15 oscillator nets not cross-connected; see LSE constraint DG-04. |
| FB1,C27 | See DG-03; unspecified bead needs real electrical selection. |
| U3,R6,C30,C31 | QSPI connectivity and chip-select reset pull-up consistent; see exact PDF/firmware gap DG-07. |
| J1,R7–R13,C28,C29 | Four-bit SD signals correct: D0 PC8,D1 PC9,D2 PC10,D3 PC11,CMD PD2,CLK PC12 through33ohm R7;47k pull-ups on CMD and D0–D3. DET_A pin10 reaches PC13 through pull-up R8=10k; DET_B pin9/GND and shield grounded. C28=100nF/C29=1uF supply bypass. Exact card current/hot-plug behavior and connector ESD protection require qualification. |
| JP1,R14 | BOOT0 U1.138 has10k pulldown and selectable GND/3V3 header. Define single-shunt population and verify intended nBOOT option bits during programming. |
| J2,R15–R19 | ARM10pin SWD mapping correct: pin1 VTref via470ohm R19,2 SWDIO via22ohm R17,4 SWCLK via22ohm R16,6 SWO via22ohm R18,10 reset via22ohm R15;3/5/9 GND,7 key NC,8 unused.470ohm is a sense-path impedance, not a debugger power feed; verify chosen probe loading. |
| P1,D1,D2,R23–R25 | Intentional USB2 plug: D+ A6 toPA12, D− A7 toPA11, CC A5 via5.1k R25 toGND, VCONN NC, VBUS isolated to high-impedance sense divider. D1 protects D+/D−, D2 CC/VBUS with common grounded anodes. No missing CC2 finding for this plug. PE0 five-volt-tolerant sense divider is prior accepted ST topology;3.565V nominal at5V is not evidence of an overvoltage fault. No bulk-VBUS-capacitor blocker for a self-powered sense-only port. |
| U39,C331,C333,C334,C336,C337,J11 | Charge-pump topology has two flying100nF capacitors, positive/negative reservoir100nF and3V3 bypass100nF. Functional block topology is sensible, but the physical pin mapping must be corrected (DG-01). J11.4 is intentionally NC. |
| U40,C332,C338,C339,C341,C342,J12 | Exact TQFN pin map agrees with manufacturer. Flying capacitors16↔1 and2↔3, negative reservoir4→GND, positive reservoir15→GND, VCC12 bypass and GND11/EP17 grounded. MCU PG7 TX→TIN8, ROUT6→PG8 RX; J12.2 TOUT10 and J12.3 RIN5. FORCE pins9/13 share AUX_EN and its hardware pulldown. Interface ESD is built into transceiver; complete cable surge environment remains unspecified. |
| Q1,D5,R345–R347,J13,J12.4 | Auxiliary power path handed to loads reviewer, avoiding a duplicate or partial claim. |

## Firmware synchronization matrix

All following functions were compared between U1 resolved pin names/nets, current `Firmware/DIC/DIC.ioc`, and ST alternate-function tables17/18 (datasheet pp88–101). No simple pin-swapping discrepancy was found.

| Function | MCU assignment |
|---|---|
| RTC SPI / GPIO | PA5/PA6/PA7 SPI1 SCK/MISO/MOSI; PA4 CE output; PB0 INT input; PB1 CLKOUT input; PB2 CLKOE output |
| QSPI | PE10 CLK;PE11 NCS;PE12–PE15 IO0–IO3 |
| SDMMC | PC8–PC11 data;PC12 clock;PD2 CMD;PC13 detect input |
| USB / debug | PA11/PA12 DM/DP;PE0 software VBUS input;PA13/PA14 SWD;PB3 SWO |
| UARTs | PA0/PA1 UART4 ADMONT;PA2/PA3 USART2 LICOR;PC4/PC5 USART3 O2;PA9/PA10 USART1 COMM;PG7/PG8 LPUART1 AUX |
| I2C | PG13 SDA;PG14 SCL |
| ADC / PWM | PC0–PC3 ADC1 IN1–IN4;PF6/PF7 TIM5 CH1/CH2;PD12 TIM4 CH1 |
| Valve interface | PG9 SPI3 SCK;PG11 SPI3 MOSI;PB10–PB12 CS;PB13 latch;PB14 reset;PB15 sleep |
| Enables / direction | PF0–PF5 regulators/sensors;PF9 water;PF10 air;PF11 acid direction;PF12 acid enable/fault open-drain;PF13 acid reset;PF14/PF15 actuators;PA8 comm;PG6 aux |

RTC SPI prescaler128 gives125kbit/s at present16MHz and625kbit/s at80MHz, below its1MHz limit. CE/CLKOE default low software state is preserved. Both have no external bias before GPIO initialization; adding suitable pull-downs is a startup robustness option. RTC mode0 data sampling matches default SPI idle-low/first-edge behavior, but explicit generated initialization remains to be checked.

## Review boundaries and prior delta

- Prior RTC direction/speed fixes, USB plug circuitry and intentional R2 removal disposition remain closed/controlled; they were not re-opened as false faults.
- U39's physical pinout mismatch is newly identified by netlist-to-exact-package comparison; prior generic transceiver block plausibility was insufficient.
- VREF+ bulk, USB clocks and connector identity remain open from prior review.
- No PCB implementation exists; oscillator stray capacitance, ESD placement, reference noise, USB impedance, SD/QSPI SI and local decoupling placement cannot be assessed.
- Exact passive MPN/rating/DC-bias/derating checks depend on root's enrichment. A nonempty property is not itself proof of package compatibility or electrical rating.
- Root owns ERC, analyzer execution/disposition, lifecycle review, electrical load boundaries and aggregate report. No source-generation, compile or runtime firmware test was possible because only IOC input exists.
