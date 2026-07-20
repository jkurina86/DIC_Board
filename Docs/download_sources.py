#!/usr/bin/env python3
"""Rebuild the Csip-OA/DIC primary-source documentation archive.

Downloads only public documents/pages.  The generated manifest records HTTP
status, final URL, content type, size, SHA-256, and retrieval time.  Re-running
is safe and overwrites each named artifact with the current upstream version.
"""
from __future__ import annotations

import hashlib
import json
import mimetypes
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from urllib.parse import urlparse
from zipfile import ZipFile

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (X11; Linux x86_64) Csip-OA documentation archive/1.0"

SOURCES = [
    # Sensors / analyzers
    ("Sensors/LI-COR_LI-830", "LI-830_LI-850_instruction_manual.pdf", "https://licor.app.boxenterprise.net/shared/static/gz8gaf0ls5vhvpl52xtmyr8mfoh5kwe8.pdf", "LI-COR instruction manual"),
    ("Sensors/LI-COR_LI-830", "LI-830_LI-850_integrators_guide.pdf", "https://licor.app.boxenterprise.net/shared/static/945g90zvrem6z4tzlf5dk2ujl3g6hp46.pdf", "LI-COR command/control integration guide"),
    ("Sensors/LI-COR_LI-830", "LI-830_LI-850_support_manuals.html", "https://www.licor.com/support/LI-850/manuals.html", "Current manufacturer support/manual index"),
    ("Sensors/LI-COR_LI-830", "LI-830_LI-850_specifications.html", "https://www.licor.com/support/LI-850/topics/specifications.html", "Current manufacturer specifications page"),
    ("Sensors/LI-COR_LI-830", "LI-830_connecting_power_pinout.html", "https://www.licor.com/support/LI-850/topics/connecting.html", "Official power, connector, and connection instructions"),
    ("Sensors/LI-COR_LI-830", "LI-830_XML_configuration_grammar.html", "https://www.licor.com/support/LI-850/topics/grammar-01.html", "Official XML configuration grammar"),
    ("Sensors/LI-COR_LI-830", "LI-830_XML_element_descriptions.html", "https://www.licor.com/support/LI-850/topics/grammar-02.html", "Official XML element reference"),
    ("Sensors/LI-COR_LI-830", "LI-830_XML_full_grammar.html", "https://www.licor.com/support/LI-850/topics/grammar-03.html", "Official complete XML grammar"),
    ("Sensors/LI-COR_LI-7815_variant", "LI-7815_instruction_manual.pdf", "https://licor.app.boxenterprise.net/shared/static/e4hb4ls264ddcmhcb735jthj2plz91rf.pdf", "LI-COR LI-7815 instruction manual; ship/shore variant only"),
    ("Sensors/LI-COR_LI-7815_variant", "LI-7815_specifications.html", "https://www.licor.com/support/LI-7815/topics/specifications.html", "Manufacturer specifications; variant only"),
    ("Sensors/Senseair_K96", "K96_manufacturer_public_overview.html", "https://senseair.com/k96-is-senseairs-prototype-multi-gas-ndir-sensor-core-platform/", "Public overview only; integration manual is not public"),
    ("Sensors/Senseair_K96", "K96_JRC_test_report.html", "https://publications.jrc.ec.europa.eu/repository/handle/JRC132309", "Independent JRC report; not an electrical integration manual"),
    ("Sensors/Senseair_K96", "K96_JRC_test_report.pdf", "https://publications.jrc.ec.europa.eu/repository/bitstream/JRC132309/JRC132309_01.pdf", "Independent JRC technical report with prototype interface/current evidence"),
    ("Sensors/Senseair_K96", "K96_Senseair_authored_research_paper.html", "https://doi.org/10.3390/atmos13111789", "Manufacturer-authored primary research paper; still not the confidential user guide"),
    ("Sensors/Sensirion_SHT35", "SHT3x_DIS_datasheet.pdf", "https://sensirion.com/media/documents/213E6A3B/63A5A569/Datasheet_SHT3x_DIS.pdf", "Official SHT30/SHT31/SHT35 I2C datasheet"),
    ("Sensors/Sensirion_SHT35", "SHT35_product_page.html", "https://sensirion.com/products/catalog/SHT35-DIS-B", "Current manufacturer product page"),
    ("Sensors/SST_LuminOx_LOX-O2-F", "LOX-02-F_datasheet.pdf", "https://sstsensing.com/wp-content/uploads/2019/07/DS0030rev14_LuminOx.pdf", "Official flow-through LuminOx datasheet"),
    ("Sensors/SST_LuminOx_LOX-O2-F", "LuminOx_user_guide.pdf", "https://sstsensing.com/wp-content/uploads/2025/05/UG-001_LuminOx_UserGuide_rev2.pdf", "Official UART commands and integration guide"),
    ("Sensors/SST_LuminOx_LOX-O2-F", "LOX-02-F_product_page.html", "https://sstsensing.com/product/luminox-optical-oxygen-flow-through-sensors/", "Current manufacturer product page"),
    ("Sensors/SST_LuminOx_LOX-O2-F", "LOX-02-F_current_datasheet_rev5.pdf", "https://sstsensing.com/wp-content/uploads/2025/06/SST-DS-0145-Rev5.pdf", "Current exact-model official datasheet"),
    ("Sensors/SST_LuminOx_LOX-O2-F", "LuminOx_current_user_guide_rev3.pdf", "https://sstsensing.com/wp-content/uploads/2026/06/SST-UG-001-Rev3.pdf", "Current official protocol guide"),
    ("Sensors/Keyence_FD-ECH7_candidate", "FD-ECH7_product_page.html", "https://www.keyence.com/products/process/flow/fd-ec/models/fd-ech7/", "Candidate flow-sensor head; exact installed assembly must be confirmed"),
    ("Sensors/Keyence_FD-ECH7_candidate", "FD-EC_series_specifications.html", "https://www.keyence.com/products/process/flow/fd-ec/specs/", "Candidate series specifications; requires amplifier model selection"),
    ("Sensors/Fluke_RPM4_bench_reference", "RPM4_operation_manual.pdf", "https://media.fluke.com/f3ccac9c-a63d-4630-bf1c-b10800c08f09_original%20file.pdf", "Bench/leak-test reference pressure monitor manual"),
    ("Sensors/Fluke_RPM4_bench_reference", "RPM4_product_page.html", "https://eu.flukecal.com/products/pressure-calibration/pressure-monitors/rpm4-reference-pressure-monitor", "Current manufacturer product page"),
    ("Sensors/Fluke_RPM4_bench_reference", "RPM4_datasheet.pdf", "https://media.fluke.com/2a7ff015-9c72-441e-a7bf-b10600735903_original%20file.pdf", "Official family datasheet"),

    # Valves, pumps, actuators
    ("Actuators/Burkert_6724", "Burkert_Type_6724_datasheet.pdf", "https://www.burkert.com/en/Media/plm/DTS/DS/ds6724-standard-eu-en.pdf", "Official Type 6724 family datasheet; verify order-code-specific coil/connector"),
    ("Actuators/Burkert_6724", "Burkert_Type_6724_product_page.html", "https://www.burkert.com/en/type/6724", "Current manufacturer product page"),
    ("Actuators/Burkert_6724", "Burkert_Type_2503_impulse_accessory.html", "https://www.burkert.com/en/type/2503", "Official optional impulse electronics/accessory page"),
    ("Actuators/KNF_NMP09KPDC-B", "KNF_NMP09_datasheet.pdf", "https://knf.com/fileadmin/Global_files/Downloads/Product_OEM_Process/Datasheets/DB_NMP09_EN_27052025.pdf", "Official NMP09 series datasheet; verify custom 6 V suffix"),
    ("Actuators/KNF_NMP09KPDC-B", "KNF_NMP05_09_015_operating_manual.pdf", "https://knf.com/fileadmin/Global_files/Downloads/Product_OEM_Process/Operating_manuals/BA121551-121553_NMP05_09_015-EN_1225.pdf", "Official installation, polarity, startup, and safety manual"),
    ("Actuators/Actuonix_P16-50-256-12-P", "Actuonix_P16_datasheet.pdf", "https://www.actuonix.com/assets/images/datasheets/ActuonixP16Datasheet.pdf", "Official P16 actuator datasheet"),
    ("Actuators/Actuonix_P16-50-256-12-P", "Actuonix_LAC_controller_datasheet.pdf", "https://www.actuonix.com/assets/images/datasheets/ActuonixLACDatasheet.pdf", "Official feedback-actuator controller datasheet"),
    ("Actuators/Actuonix_P16-50-256-12-P", "Actuonix_LAC_advanced_configuration.pdf", "https://www.actuonix.com/assets/images/datasheets/ActuonixLACAdvancedConfigurationDatasheet.pdf", "Official LAC control/configuration guide"),
    ("Actuators/Actuonix_P16-50-256-12-P", "P16_exact_product_page.html", "https://www.actuonix.com/p16-50-256-12-p", "Exact actuator order-code page"),
    ("Actuators/Sea-Bird_SBE5P", "SBE5_datasheets.zip", "https://www.seabird.com/hubfs/Product%20Assets/SBE%205/Datasheets/SBE%205_Datasheets.zip?hsLang=en", "Official SBE 5T/5P datasheet bundle"),
    ("Actuators/Sea-Bird_SBE5P", "SBE5_legacy_datasheet.pdf", "https://www.seabird.com/asset-get.download.jsa?code=251175", "Official legacy SBE 5T/5P datasheet retained alongside the current ZIP bundle"),
    ("Actuators/Sea-Bird_SBE5P", "AN40_SBE5_speed_adjustment.pdf", "https://www.seabird.com/hubfs/Resources/Application%20Notes/AN40-SBE5SpeedAdjust.pdf?hsLang=en", "Official pump-speed adjustment note"),
    ("Actuators/Sea-Bird_SBE5P", "AN75_pump_maintenance.pdf", "https://www.seabird.com/hubfs/Resources/Application%20Notes/AN75-PumpMaintenance.pdf?hsLang=en", "Official maintenance note"),
    ("Actuators/Sea-Bird_SBE5P", "SBE5_product_page.html", "https://www.seabird.com/sbe-5t-5p-submersible-pump/product-downloads?id=60762467710", "Current manufacturer product/download page"),
    ("Actuators/Takasago_RP-TX", "Takasago_RP-TX_catalog_page.html", "https://pdf.directindustry.com/pdf/takasago-fluidic-systems/micro-peristaltic-pump-rp-tx-series/7120-480667.html", "Scraped copy of the archived one-page manufacturer brochure; current manufacturer URL has moved"),
    ("Actuators/Takasago_RP-TX", "Takasago_catalog_2021.pdf", "https://www.images.pumpen-ventile.de/fileadmin/datenblaetter/kataloge/Takasago-catalog-2021.pdf", "Archived manufacturer catalog containing RP-TX; use until exact current motor sheet is obtained"),
    ("Actuators/Takasago_RP-TX", "Takasago_current_product_page.html", "https://www.takasago-fluidics.com/products/rp-tx-1", "Current Takasago product page"),
    ("Actuators/Takasago_RP-TX", "Aquatech_RP-TX_product_page.html", "https://ringpump-aquatech.co.jp/english/commodity/rp-tx.html", "Current actual-manufacturer product page"),
    ("Actuators/Takasago_RP-TX", "Aquatech_RP-TX_catalog_2025.pdf", "https://ringpump-aquatech.co.jp/english/download/catalog_e_rp-tx_250513.pdf", "Current official RP-TX catalog"),
    ("Actuators/Takasago_RP-TX", "Aquatech_RP-TX_outline_drawing.pdf", "https://ringpump-aquatech.co.jp/english/download/drawing_data/rp-tx_drw-e.pdf", "Official outline drawing"),
    ("Actuators/Takasago_RP-TX", "Aquatech_RE-C100_controller_manual.pdf", "https://ringpump-aquatech.co.jp/english/download/re-c100_manual-e_20230809.pdf", "Official qualified controller reference for 2.6 V constant-voltage microstepping"),

    # Measurement-method/equilibrator references (not substitutes for PMEL internal drawings)
    ("System/ASVCO2_equilibrator_references", "PMEL_MAPCO2_ASVCO2_requirements.pdf", "https://www.pmel.noaa.gov/co2//files/map-asvsopsonepager2022.pdf", "PMEL measurement/calibration requirements one-pager"),
    ("System/ASVCO2_equilibrator_references", "MAPCO2_methods_paper.html", "https://doi.org/10.5194/essd-6-353-2014", "Open-access MAPCO2 methods/performance paper"),

    # MCU, clocking, storage
    ("Board/STM32L476ZG_current", "STM32L476xx_datasheet.pdf", "https://www.st.com/resource/en/datasheet/stm32l476zg.pdf", "Official datasheet for live schematic/CubeMX target"),
    ("Board/STM32L476ZG_current", "RM0351_reference_manual.pdf", "https://www.st.com/resource/en/reference_manual/dm00083560-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf", "Official reference manual"),
    ("Board/STM32L4R5ZG_candidate", "STM32L4R5xx_datasheet.pdf", "https://www.st.com/resource/en/datasheet/stm32l4r5zg.pdf", "Official candidate-family datasheet for the ZG order code"),
    ("Board/STM32L4R5ZG_candidate", "RM0432_reference_manual.pdf", "https://www.st.com/resource/en/reference_manual/rm0432-stm32l4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf", "Official L4+ reference manual"),
    ("Board/STM32L476ZG_current", "ES0250_errata.pdf", "https://www.st.com/resource/en/errata_sheet/es0250-stm32l476xxstm32l486xx-device-errata-stmicroelectronics.pdf", "Official L476/L486 silicon errata"),
    ("Board/STM32L4R5ZG_candidate", "ES0393_errata.pdf", "https://www.st.com/resource/en/errata_sheet/es0393-stm32l4rxxx-and-stm32l4sxxx-device-errata-stmicroelectronics.pdf", "Official L4R/L4S silicon errata"),
    ("Board/STM32_hardware_guidance", "AN5017_L476_to_L4plus_migration.pdf", "https://www.st.com/resource/en/application_note/an5017-migrating-between-stm32l476xx486xx-and-stm32l4-series-microcontrollers-stmicroelectronics.pdf", "Official migration guide; establishes that L476 and L4R5 are not transparent substitutions"),
    ("Board/STM32_hardware_guidance", "AN4555_hardware_development.pdf", "https://www.st.com/resource/en/application_note/an4555-getting-started-with-stm32l4-series-and-stm32l4-series-hardware-development-stmicroelectronics.pdf", "Official hardware-design guidance"),
    ("Board/STM32_hardware_guidance", "AN4746_power_performance.pdf", "https://www.st.com/resource/en/application_note/an4746-optimizing-power-and-performance-with-stm32l4-and-stm32l4-series-microcontrollers-stmicroelectronics.pdf", "Official low-power guidance"),
    ("Board/STM32_hardware_guidance", "AN4879_USB_hardware_PCB.pdf", "https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf", "Official USB hardware and PCB guidance"),
    ("Board/STM32_hardware_guidance", "AN4621_ultralow_power_overview.pdf", "https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf", "Official low-power mode overview"),
    ("Board/STM32_hardware_guidance", "AN4978_external_SMPS.pdf", "https://www.st.com/resource/en/application_note/an4978-design-recommendations-for-stm32l4xxxx-with-external-smps-for-ultra-low-power-applications-with-high-performance-stmicroelectronics.pdf", "Official external-SMPS design guidance"),
    ("Board/STM32_hardware_guidance", "AN2867_oscillator_design.pdf", "https://www.st.com/resource/en/application_note/an2867-guidelines-for-oscillator-design-on-stm8afals-and-stm32-mcusmpus-stmicroelectronics.pdf", "Official HSE/LSE gain-margin and drive guidance"),
    ("Board/STM32_hardware_guidance", "AN5050_OctoSPI_xSPI.pdf", "https://www.st.com/resource/en/application_note/an5050-getting-started-with-octospi-hexadecaspi-and-xspi-interface-on-stm32-mcus-stmicroelectronics.pdf", "Official OctoSPI/xSPI implementation guidance"),
    ("Board/STM32_hardware_guidance", "AN1709_EMC_design.pdf", "https://www.st.com/resource/en/application_note/an1709-emc-design-guide-for-stm8-stm32-and-legacy-mcus-stmicroelectronics.pdf", "Official STM32 EMC design guidance"),

    # Power and inductive-load application notes
    ("Board/Power_and_motor_guidance", "TI_SLVA670A_inrush_current.pdf", "https://www.ti.com/lit/an/slva670a/slva670a.pdf", "Inrush-current management"),
    ("Board/Power_and_motor_guidance", "TI_SLVA652A_load_switch_fundamentals.pdf", "https://www.ti.com/lit/an/slva652a/slva652a.pdf", "Load-switch fundamentals"),
    ("Board/Power_and_motor_guidance", "TI_SLVAE57B_ideal_diode_basics.pdf", "https://www.ti.com/lit/an/slvae57b/slvae57b.pdf", "Ideal-diode/reverse-current fundamentals"),
    ("Board/Power_and_motor_guidance", "TI_SLVAE59A_solenoid_motor_drivers.pdf", "https://www.ti.com/lit/an/slvae59a/slvae59a.pdf", "Driving solenoids with motor drivers"),
    ("Board/Power_and_motor_guidance", "TI_SLVAFT0_motor_bulk_capacitor_sizing.pdf", "https://www.ti.com/lit/an/slvaft0/slvaft0.pdf", "Motor-drive bulk-capacitor sizing"),
    ("Board/Abracon_RTC", "AB-RTCMC-EOA9-S3_datasheet.pdf", "https://abracon.com/realtimeclock/AB-RTCMC-32.768kHz-EOA9-S3.pdf", "Official RTC datasheet"),
    ("Board/Abracon_RTC", "AB-RTCMC-EOA9-S3_application_manual.pdf", "https://abracon.com/realtimeclock/AB-RTCMC-32.768kHz-EOA9-S3-Application-Manual.pdf", "Official RTC register/application manual"),
    ("Board/Abracon_clocking", "ABM8AAIG_datasheet.pdf", "https://abracon.com/datasheets/ABM8AAIG.pdf", "Official 8 MHz crystal datasheet"),
    ("Board/Abracon_clocking", "ABS06-107_datasheet.pdf", "https://abracon.com/Resonators/ABS06-107-32.768kHz-T.pdf", "Official 32.768 kHz crystal datasheet"),
    ("Board/Everspin_EM064LXO_preferred", "EMxxLX_datasheet_rev3_2.pdf", "https://download.mikroe.com/documents/datasheets/EM064LXQADG13IS1R_datasheet.pdf", "Everspin datasheet mirror; verify exact EM064LXO package/order code"),
    ("Board/Everspin_EM064LXO_preferred", "EM064LXQ_support_page.html", "https://www.everspin.com/supportdocs/EM064LXQADG13IS1T?npath=3843", "Manufacturer support-document page for the exact 64-Mbit EM064LXQ family ordering code"),
    ("Board/Everspin_MR25H256A_not_32MB", "MR25H256A_product_page.html", "https://www.everspin.com/family/mr25h256", "Manufacturer page: this is 256 Kbit/32 KiB, not 32 MB"),
]


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_extract_zip(path: Path, destination: Path) -> list[str]:
    extracted = []
    destination.mkdir(parents=True, exist_ok=True)
    with ZipFile(path) as zf:
        for info in zf.infolist():
            parts = Path(info.filename).parts
            if "__MACOSX" in parts or any(part.startswith("._") for part in parts):
                continue
            out = (destination / info.filename).resolve()
            if destination.resolve() not in out.parents and out != destination.resolve():
                raise RuntimeError(f"unsafe ZIP path: {info.filename}")
            zf.extract(info, destination)
            if not info.is_dir():
                extracted.append(str(out.relative_to(ROOT)))
    return extracted


def main() -> int:
    session = requests.Session()
    session.headers.update({"User-Agent": UA, "Accept": "*/*"})
    records = []
    for category, filename, url, note in SOURCES:
        target_dir = ROOT / category
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / filename
        rec: dict[str, object] = {"category": category, "file": str(target.relative_to(ROOT)), "source_url": url, "note": note}
        try:
            with session.get(url, timeout=90, allow_redirects=True, stream=True) as response:
                rec.update({"http_status": response.status_code, "final_url": response.url, "content_type": response.headers.get("content-type", "")})
                response.raise_for_status()
                tmp = target.with_suffix(target.suffix + ".part")
                with tmp.open("wb") as f:
                    for chunk in response.iter_content(1024 * 256):
                        if chunk:
                            f.write(chunk)
                tmp.replace(target)
            head = target.read_bytes()[:8]
            rec["detected_format"] = "pdf" if head.startswith(b"%PDF-") else "zip" if head.startswith(b"PK\x03\x04") else "html" if b"<" in head else "other"
            rec["size_bytes"] = target.stat().st_size
            rec["sha256"] = digest(target)
            rec["status"] = "downloaded"
            if target.suffix.lower() == ".zip" and rec["detected_format"] == "zip":
                rec["extracted_files"] = safe_extract_zip(target, target.with_suffix(""))
        except Exception as exc:
            # Some vendor CDNs (notably Actuonix) reject requests' browser-like
            # header but serve the identical public artifact to curl.  Retry
            # with curl before recording a real failure.
            tmp = target.with_suffix(target.suffix + ".part")
            curl = subprocess.run(
                ["curl", "-L", "-sS", "--fail", "--max-time", "90", "-o", str(tmp), url],
                capture_output=True,
                text=True,
            )
            if curl.returncode == 0 and tmp.exists() and tmp.stat().st_size:
                tmp.replace(target)
                head = target.read_bytes()[:8]
                rec["detected_format"] = "pdf" if head.startswith(b"%PDF-") else "zip" if head.startswith(b"PK\x03\x04") else "html" if b"<" in head else "other"
                rec["size_bytes"] = target.stat().st_size
                rec["sha256"] = digest(target)
                rec["status"] = "downloaded-curl-fallback"
                rec["primary_client_error"] = f"{type(exc).__name__}: {exc}"
                if target.suffix.lower() == ".zip" and rec["detected_format"] == "zip":
                    rec["extracted_files"] = safe_extract_zip(target, target.with_suffix(""))
            else:
                rec["status"] = "failed"
                rec["error"] = f"{type(exc).__name__}: {exc}; curl: {curl.stderr.strip()}"
        records.append(rec)
        print(f"{rec['status']:10s} {rec['file']}")

    text_records: list[dict[str, object]] = []
    for pdf in sorted(ROOT.rglob("*.pdf")):
        if "__MACOSX" in pdf.parts:
            continue
        text_path = pdf.with_suffix(".txt")
        result = subprocess.run(
            ["pdftotext", "-layout", str(pdf), str(text_path)],
            capture_output=True,
            text=True,
        )
        text_records.append({
            "pdf": str(pdf.relative_to(ROOT)),
            "text": str(text_path.relative_to(ROOT)),
            "status": "extracted" if result.returncode == 0 else "failed",
            "size_bytes": text_path.stat().st_size if text_path.exists() else 0,
            "error": result.stderr.strip() if result.returncode else "",
        })

    html_text_records: list[dict[str, object]] = []
    for html_path in sorted(ROOT.rglob("*.html")):
        text_path = html_path.with_suffix(".txt")
        try:
            soup = BeautifulSoup(html_path.read_bytes(), "html.parser")
            for element in soup(["script", "style", "noscript", "template"]):
                element.decompose()
            lines = [" ".join(line.split()) for line in soup.get_text("\n").splitlines()]
            clean = "\n".join(line for line in lines if line) + "\n"
            text_path.write_text(clean, encoding="utf-8")
            html_text_records.append({
                "html": str(html_path.relative_to(ROOT)),
                "text": str(text_path.relative_to(ROOT)),
                "status": "extracted",
                "size_bytes": text_path.stat().st_size,
                "error": "",
            })
        except Exception as exc:
            html_text_records.append({
                "html": str(html_path.relative_to(ROOT)),
                "text": str(text_path.relative_to(ROOT)),
                "status": "failed",
                "size_bytes": text_path.stat().st_size if text_path.exists() else 0,
                "error": f"{type(exc).__name__}: {exc}",
            })

    generated = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    manifest = {
        "generated_utc": generated,
        "source_count": len(records),
        "records": records,
        "pdf_text_extraction": text_records,
        "html_text_extraction": html_text_records,
    }
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    failures = [r for r in records if not str(r["status"]).startswith("downloaded")]
    print(f"\nDownloaded {len(records)-len(failures)}/{len(records)} sources; failures={len(failures)}")
    for r in failures:
        print(f"FAILED {r['file']}: {r.get('error')}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
