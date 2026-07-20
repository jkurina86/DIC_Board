# Csip-OA / DIC Component Documentation Archive

This directory is the project-local documentation archive for the Csip-OA embedded-electronics design. It was assembled from the component list in `../Csip_OA_Embedded_Hardware_Firmware_2.docx`, the live KiCad/CubeMX project, and the reverse-engineering notes in `~/Documents/Obsidian/Career/Work/DIC/`.

## Archive rules

- Prefer the exact installed manufacturer part number and manufacturer document.
- A family datasheet does not close an order-code-specific electrical question.
- Candidate and bench-only devices are labeled as such in directory names.
- A missing authoritative interface document is recorded as a design blocker; it is not replaced with a guessed protocol from a similar product.
- Original PDFs and HTML pages are retained. Searchable text sidecars use the same basename with `.txt`; PDF text comes from `pdftotext -layout`, and HTML text is cleaned of scripts/styles before extraction.
- `manifest.json` is the provenance record: source URL, final URL where available, HTTP result, content type, byte size, SHA-256 checksum, retrieval method, and text-extraction status.
- `download_sources.py` rebuilds the public archive. It follows redirects, uses a `curl` fallback for public vendor CDNs that reject the Python client, safely extracts ZIP bundles, and runs `pdftotext -layout`.

> [!note] Copyright
> These documents remain the property of their publishers. They are archived here for engineering reference. Do not redistribute them outside the project without checking the publisher’s terms.

## Scope-document component coverage

| Scope component | Archive directory | Coverage | Remaining action |
|---|---|---|---|
| Bürkert `6724-S01,2FFPK-FB46-012/DC-AT-55-12* CF16` latching air valve | `Actuators/Burkert_6724/` | Current Type 6724 datasheet/product page and Type 2503 impulse-electronics page. Family data establishes 12 V ±5%, 1.25 W switching, 0 W holding and at least 500 ms polarity-reversing pulse | Obtain the exact article/inspection sheet to verify `CF16`, pin polarity, maximum pulse, resistance, materials and port mapping |
| KNF `NMP09KPDC-B 6V` air pump | `Actuators/KNF_NMP09KPDC-B/` | Current official datasheet and operating manual; exact entry is 6 V brushless and `Imax` 0.17 A | Confirm build suffix; reversed polarity damages its electronics, and KNF requires atmospheric-pressure startup and overload protection |
| Takasago/Aquatech `RP-TX` acid pump | `Actuators/Takasago_RP-TX/` | Current Takasago/Aquatech pages, 2025 catalog, outline drawing, RE-C100 controller manual, plus archived catalog | Public evidence establishes a 3 V/350 mW two-phase bipolar pump and qualified 2.6 V constant-voltage ¼-step drive, but not the phase current; obtain exact winding/pin/acceleration data |
| Sea-Bird `SBE 5P` water pump | `Actuators/Sea-Bird_SBE5P/` | Current official datasheet ZIP, extracted 5T/5P PDF, legacy official datasheet, speed-adjustment note, maintenance note, and product page | Record the installed pump’s full configuration/order code and connector |
| 2× Actuonix `P16-50-256-12-P` | `Actuators/Actuonix_P16-50-256-12-P/` | Official P16 datasheet, exact product page, LAC controller datasheet, and advanced guide; 1 A stall and 20% maximum duty are documented | Record both actuator serial/build codes and exact RC/LAC controller; preserve stall, travel-limit and fail-safe behavior |
| Sensirion SHT35 | `Sensors/Sensirion_SHT35/` | Official SHT3x-DIS datasheet and current SHT35 product page | Confirm exact SHT35 suffix/package and whether the embedded board connects directly by I²C or retains an external adapter |
| SST LuminOx `LOX-02-F` | `Sensors/SST_LuminOx_LOX-O2-F/` | Current exact-model datasheet, protocol guide, older revision and product page; official spelling is `LOX-02-F` | Record exact serial/suffix and whether an evaluation board changes the native 5 V supply/3.3 V TTL UART interface |
| LI-COR LI-830 | `Sensors/LI-COR_LI-830/` | Official LI-830/850 instruction manual, integrator’s guide, support index, and current specifications page | Record installed serial number and reconcile calibration constants labeled for another analyzer |
| LI-COR LI-7815 ship/shore variant | `Sensors/LI-COR_LI-7815_variant/` | Official instruction manual and current specifications page | Confirm whether this high-power Ethernet/MQTT variant is in the embedded CCA release; define exact connector/input pins |
| Senseair ADMONT K96 subsurface variant | `Sensors/Senseair_K96/` | Manufacturer’s public prototype-platform overview and independent JRC report page | **Blocking:** obtain the PMEL/Senseair unit-specific electrical pinout, serial protocol, commands, framing/CRC, power profile, and calibration procedure. No public integration manual was found |

All ten component lines from the source Word document are represented. Where exact integration documents are not public, the archive records that gap rather than presenting a generic document as authoritative.

## Additional project devices and critical board components

| Device | Archive directory | Why included |
|---|---|---|
| Fluke RPM4 350K | `Sensors/Fluke_RPM4_bench_reference/` | Existing leak/reference code sends `QPRR`; official operator manual and product page are archived. Treat as bench equipment until deployment inclusion is confirmed |
| Keyence FD-ECH7 candidate | `Sensors/Keyence_FD-ECH7_candidate/` | Existing notes identify it as the likely flow-sensor head; manufacturer product/specification pages are archived. The required amplifier model is still unknown |
| STM32L476ZG current target | `Board/STM32L476ZG_current/` | Exact MCU family in the live schematic/CubeMX project; official datasheet and RM0351 |
| STM32L4R5ZG candidate | `Board/STM32L4R5ZG_candidate/` | Recommended low-power/memory candidate; official family datasheet and RM0432 |
| STM32 hardware, migration and low-power guidance | `Board/STM32_hardware_guidance/` | ST hardware, L476→L4+ migration, USB, oscillator, OctoSPI, EMC, SMPS and low-power notes; silicon errata are stored with each MCU |
| Power and inductive-load guidance | `Board/Power_and_motor_guidance/` | TI primary application notes for inrush, load switching, ideal-diode protection, solenoid drive and motor bulk-capacitor sizing |
| Abracon AB-RTCMC RTC | `Board/Abracon_RTC/` | Exact RTC in the live schematic; official datasheet and application/register manual |
| Abracon HSE/LSE crystals | `Board/Abracon_clocking/` | Exact clock-family documents for the live schematic |
| Everspin EM064LX family | `Board/Everspin_EM064LXO_preferred/` | Proposed high-speed xSPI MRAM; datasheet mirror plus manufacturer exact-order-code support page |
| Everspin MR25H256A | `Board/Everspin_MR25H256A_not_32MB/` | Retained specifically to prevent a capacity error: this part is 256 Kbit/32 KiB, not 32 MB |
| ASVCO2/MAPCO2 method | `System/ASVCO2_equilibrator_references/` | PMEL requirements and open methods evidence; explicitly not a substitute for the internal Gen2/Csip-OA mechanical drawing |

## Documentation gaps that must be closed from installed hardware or PMEL records

These are not public-search problems anymore; each requires the exact installed MPN, a project/vendor document, or an engineering decision.

1. **Senseair K96** — electrical interface, pinout, protocol, commands, CRC, calibration, warm-up and current profile.
2. **CTD** — exact manufacturer/model/configuration, cable pinout, electrical level, serial command set and power profile. “CTD at 9600 baud” is insufficient for a schematic.
3. **GPS** — exact module, antenna, supply, logic levels, NMEA sentences, PPS and backup-power requirements.
4. **Flow sensor** — confirm whether FD-ECH7 is installed, identify the matching FD-EC amplifier, and record its configured output and power.
5. **SHT35 bench adapter** — identify the adapter that creates the existing serial/USB stream; decide whether it is removed in favor of native I²C.
6. **LuminOx adapter/harness** — establish whether the CCA sees native 3.3 V TTL or an external USB/RS-232 conversion board.
7. **KNF custom 6 V pump** — exact custom build sheet and measured electrical/flow curves.
8. **Takasago RP-TX** — exact motor/winding and current/microstep requirements, tubing material, pressure and calibrated dose per step.
9. **Bürkert 6724 order code** — exact latching coil/pulse characteristics, pinout/connector and certified fluid compatibility.
10. **Actuonix controller boundary** — exact LAC/RC controller model and configuration, or a decision to implement the closed-loop motor controller on the CCA.
11. **External logger interface** — electrical layer, command protocol, connector, wake behavior and data-transfer requirements.
12. **External power source** — minimum/nominal/maximum voltage, source impedance, current limit, cable length, transient environment and available deployment energy.
13. **LI-7815 inclusion** — if included, define Ethernet hardware and a dedicated high-current power-entry population; if excluded, remove it explicitly from the target release rather than leaving an ambiguous partial interface.
14. **MRAM requirement** — confirm capacity. EM064LXO is 64 Mbit (8 MB); four devices or another density are required to meet a 32 MB requirement.
15. **ASVCO2/Csip-OA equilibrator** — obtain PMEL’s internal mechanical/plumbing drawing, headspace volume, flow setpoints, pressure limits, drain/vent geometry, valve map, water-detection behavior and transient-power budget.

## Rebuilding and checking the archive

From `~/Work/DIC_Board/`, with Python packages from `Docs/requirements.txt` plus `curl` and Poppler's `pdftotext` installed:

```bash
python3 -m pip install -r Docs/requirements.txt
python3 Docs/download_sources.py
```

A successful run ends with:

```text
Downloaded 76/76 sources; failures=0
```

Review `manifest.json` after every refresh. A changed SHA-256 hash is not automatically an error—vendors revise documents—but the changed document must be reviewed before relying on previous page numbers, limits or command descriptions.

## Relationship to the design document

The complete hardware/firmware/power/bring-up plan is:

`~/Documents/Obsidian/Career/Work/DIC/New Board Design.md`

That document cites these archive directories inline at the point where each device is specified and identifies unresolved documentation as release-gate work.
