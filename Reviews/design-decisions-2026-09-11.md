# Confirmed design decisions — 11 September 2026

The user confirmed the following existing design choices:

- Keep the6.6V rail; it is acceptable for the installed KNF pump.
- Keep the nominal12V supply for LI-830 and valves.
- Keep the existing K96 interface.
- Keep the existing actuator/controller interface.

These are recorded as user-confirmed design requirements. They close the corresponding requests for a supply/interface decision; they are not new manufacturer evidence or measured test results. Hidden Design Confirmation properties on J33,J10,J8,J5,J3/J4 preserve these decisions in the schematic.

The separate KNF overload/current-limit question, acid winding requirements, valve pulse limits, firmware behavior and physical qualification were not resolved by these confirmations.

## Input fuse

F10 is now8A, Littelfuse0451008.MRL, in the existing footprint, following the user's acceptance of the standard8A alternative.

The manufacturer lists8A and10A, with no8.5A option in the current451/453 family. The8A part preserves the existing land pattern and125V rating. A fuse's nominal current rating is not an instantaneous clamp or guaranteed opening current. [Littelfuse451/453 data and ordering table](https://www.littelfuse.com/assetdocs/fuse-451-and-453-datasheet?assetguid=533cd5cc-956c-4243-867f-6ab5a62f6ba1).

See the [current repair report](schematic-fixes-2026-09-11.md) for remaining work.
