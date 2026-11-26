# OOMWOO wake-up sensor board

A tiny board with a GL5537 photoresistor (LDR) for the robot's wake-up sensor. It plugs into the [main board](../main-phone/README.md) (J9) with a 2-pin cable. Rev 1, 2026-11-15.

A separate board lets the sensor sit wherever the enclosure needs it, away from the main board at the front of the robot. Until 2026-11-15 the LDR was R75 on the main board.

## Circuit

- R7001: Senba GL5537-1 (C125628), through-hole, 5 mm: about 20-30 kΩ at 10 lux, 2 MΩ in the dark.
- No other parts. The main board holds the rest of the divider: R103 (10k) pulls the LDR side down to GND, and C1 (100 nF) on PB12 filters noise picked up on the cable. More light reads a higher voltage on PB12 (ADC); an unplugged board reads ~0 V, the same as dark.

## Connector J7001

ZX-SH1.0-2PWT (C7430444), right-angle SH since 2026-11-26 (the vertical ZX-SH1.0-2PLT, C7430451, before), to keep the board compact; J9 on the main board stays vertical, and the pinout and cable are the same. The same family as the other sensor boards. It has 2 pins, so no other sensor cable fits it.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | VMCU-3V3 |
| 2 | LDR | PB12, R103 to GND, C1 |
| 3, 4 | mounting pads, GND | |

Use a pin 1 to pin 1 cable.

## PCB notes (for layout)

- The sensing point is the LDR's top face. Keep the board small.
- H7001: one M2 hole (`MountingHole_2.2mm_M2_Pad`, pad to GND, not in the BOM), like the Hall boards.
- Reference designators are in this board's 7000s range: every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s, wake-up sensor 7000s.

All parts are assembled at JLC. Symbols and footprints come from the shared libraries in [`../lib`](../lib) (`JLCImport`).
