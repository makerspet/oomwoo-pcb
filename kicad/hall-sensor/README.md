# OOMWOO Hall sensor board

A tiny board with a Hall switch that detects a magnet. The robot fits two of them, from the same design: one for the dust bin (a magnet in the bin) and one for the LiDAR tower bumper (a magnet in the tower cover). Each plugs into the [main board](../main-phone/README.md) (HALL-BIN1 or HALL-TOWER1) with a 3-pin cable. Rev 1, 2026-10-28.

A separate board keeps the mechanics flexible: the bin sits between the blower and the main brush, far from any other board, and the tower cover changes with the LiDAR model.

## Circuit

- U6001: Cross Chip CC6201ST (C285995, ~$0.06): an omnipolar micropower Hall switch, so either magnet pole works. OUT goes low while the magnet is near.
  - It samples at roughly 20-45 Hz, so it reacts within ~25-50 ms. That's fine for the bin, and for the tower about as quick as a microswitch's travel.
  - The output stage isn't confirmed (push-pull or open drain), so the main board pulls OUT up (R215/R216, 47k). Either type works.
  - Drop-in alternative with the same pinout (1 VDD, 2 OUT, 3 GND): TI DRV5032FADBZR (C140921, ~$0.10, push-pull).
- C6001: 100 nF bypass at U6001.

## Connector J6001

ZX-SH1.0-3PLT (C7430452), vertical SH. It has 3 pins on purpose (changed 2026-10-29, was 4 with one unused): a Hall cable can't go into a 4-pin cliff or rear IR socket, and the cable is cheaper.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | VCC-3V3-REG |
| 2 | OUT (low = magnet) | PE4 (bin) / PE5 (tower) |
| 3 | GND | |
| 4, 5 | mounting pads, GND | |

Use a pin 1 to pin 1 cable.

## PCB notes (for layout)

- The sensing point is the centre of U6001's top face. Keep the board small so it fits next to the bin or under the tower cover.
- H6001: one M2 hole (`MountingHole_2.2mm_M2_Pad`, pad to GND, not in the BOM). One is enough for a board this small (changed 2026-10-29, was two).
- Reference designators are in this board's 6000s range: every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s. The panel has two copies; let KiKit (or the panel tool) rename references per copy.

All parts are assembled at JLC. Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`).

## Open items

- Pick the magnet (size, distance) on the first prototype: the switch turns on at about 4 mT and off at about 3.2 mT.
