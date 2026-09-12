# Hardware selections and board sync — 2026-09-11

| Ref | Manufacturer / MPN | Mounting |
|---|---|---|
| SW1 | E-Switch TL6330AF200Q | SMD, exact recommended land pattern |
| J2 | Wurth 61201021621; DigiKey 732-2094-ND | Shrouded 2x5 male,2.54mm pitch,PTH |
| JP1 | Wurth 61300311121 | Vertical 1x3 male,2.54mm pitch,PTH |
| J13 | Wurth 61300511121 | Vertical 1x5 male,2.54mm pitch,PTH; replaces Micro-Fit |
| BT1 | Keystone 3013; DigiKey 36-3013-ND | 16mm coin-cell retainer,PTH |

All five have MPN,manufacturer,source, datasheet and footprint properties in the schematic. Board has289 footprints; only P1 (USB-C plug) remains unselected. All1440 pads and schematic association paths verified. Existing positions retained, four footprints added to staging and J13 replaced. No routing,vias,zones or outline added.

## Exact mounting checks

- [SW1 drawing](https://configured-product-images.s3.amazonaws.com/2D/specs/TL6330AF200Q.pdf): four0.9x1.0mm lands at x=+/-2.05,y=+/-0.8. Physical terminals1/2 are internally common and mapped to schematic pin1; physical3/4 map to schematic pin2. The two symbol pins remain the two switched contacts.
- [J2 drawing](https://www.we-online.com/components/products/datasheet/61201021621.pdf):2.54mm pitch,1.1mm recommended holes,20.36x9.0mm body. This is the user-selected2.54mm connector, with existing ARM SWD electrical numbering; matching cable/adapter required.
- [JP1](https://www.we-online.com/components/products/datasheet/61300311121.pdf) and [J13](https://www.we-online.com/components/products/datasheet/61300511121.pdf): exact order codes,2.54mm pitch,0.64mm square pins,1.1mm recommended holes. Local footprints derive from KiCad standard headers with drill corrected to manufacturer recommendation.
- [BT1 drawing, catalog p6](https://beta.keyelco.com/userAssets/file/M60p4-6-7.pdf): 0.664in(16.8656mm) hole pitch,0.073in(1.8542mm) drill; bothretainer tabs are positive pad1. A4x4mm exposed PCB contact is negative pad2, exceeding the0.156in square minimum, with no solder paste. Battery itself is separate and its exact order code remains unselected.

Manufacturer PDFs,text sidecars and provenance hashes: `Docs/Board/Selected_Hardware_20260911/`.

## Existing source changes detected during sync

Latest source differs electrically from the preceding board sync: R323 now runs from C323 pin2 to ground, while C323 pin1 remains on ACID_PUMP_RESET_N. This puts the resistor and capacitor in series and removes the previously reviewed direct DC reset pull-down. The latest wiring was preserved and synchronized; it was not introduced by these property edits.

Root ERC reports3 errors,0warnings: undriven power-input nets at U2 pin9 VBACKUP,J2 pin1 VTref,and the12V-sheet power symbol after R103. Previously documented power flags are absent in the latest source. These are outstanding, not a clean ERC result. No electrical edits or ERC rule suppressions were made in this update.
