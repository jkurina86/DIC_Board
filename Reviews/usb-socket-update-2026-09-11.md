# USB-C receptacle update — 2026-09-11

P1 is now GCT USB4105-GF-A, DigiKey2073-USB4105-GF-ACT-ND, with standard KiCad footprint `Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal`.

- Replaced male plug symbol with USB_C_Receptacle_USB2.0_16P.
- CC1 retains R25(5.1k). Added R351(5.1k,Vishay CRCW04025K10FKED,0402) independently from CC2 to ground.
- Added D6(RClamp0582B.TCT,SOT-523) for CC2 ESD protection; unused second channel NC. Existing CC1,VBUS and data-line protection retained.
- Connected A6/B6 to USB_OTG_FS_DP and A7/B7 to USB_OTG_FS_DM. SBU1/SBU2 unused with no-connect markers.
- All prior numbered-pin connectivity is unchanged except the intentional transition of P1.B5 from unused VCONN to terminated CC2.
- Board contains292 footprints and1467 verified pads. Every schematic component has a footprint; every purchased component has an MPN. Seven fabricated test points do not require purchased MPNs.
- Existing footprint locations retained; P1,R351,D6 appended to staging. No tracks,vias,zones or outline added.
- Root ERC remains at the same3 pre-existing errors (U2 VBACKUP,J2 VTref,12V output flag),0warnings. The prior R323/C323 reset-wiring finding remains unresolved and was not altered.

Sources: [DigiKey part](https://www.digikey.com/en/products/detail/gct/USB4105-GF-A/11198441), [GCT drawing](https://gct.co/files/drawings/usb4105.pdf), [USB Type-C CC implementation guidance](https://www.ti.com/document-viewer/lit/html/SSZTC87).
