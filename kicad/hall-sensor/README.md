# OOMWOO Hall sensor board

A tiny board with a Hall switch that detects a magnet. The robot fits two of them, from the same design: one for the dust bin (a magnet in the bin) and one for the LiDAR tower bumper (a magnet in the tower cover). Each plugs into the [main board](../main-phone/README.md) (HALL-BIN1 or HALL-TOWER1) with a 4-pin cable. Rev 1, 2026-10-28.

A separate board keeps the mechanics flexible: the bin sits between the blower and the main brush, far from any other board, and the tower cover changes with the LiDAR model.

## Circuit

- U8701: Cross Chip CC6201ST (C285995, ~$0.06): an omnipolar micropower Hall switch, so either magnet pole works. OUT goes low while the magnet is near.
  - It samples at roughly 20-45 Hz, so it reacts within ~25-50 ms. That's fine for the bin, and for the tower about as quick as a microswitch's travel.
  - The output stage isn't confirmed (push-pull or open drain), so the main board pulls OUT up (R7801/R7802, 47k). Either type works.
  - Drop-in alternative with the same pinout (1 VDD, 2 OUT, 3 GND): TI DRV5032FADBZR (C140921, ~$0.10, push-pull).
- C8701: 100 nF bypass at U8701.

## Connector J8701

ZX-SH1.0-4PLT (C7430453): the same 4-pin vertical SH part as the cliff and rear IR boards.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | VCC-3V3-REG |
| 2 | OUT (low = magnet) | PE4 (bin) / PE5 (tower) |
| 3 | not used | |
| 4 | GND | |
| 5, 6 | mounting pads, GND | |

Use a pin 1 to pin 1 cable.

## PCB notes (for layout)

- The sensing point is the centre of U8701's top face. Keep the board small so it fits next to the bin or under the tower cover.
- H8701/H8702: two M2 holes (`MountingHole_2.2mm_M2_Pad`, pads to GND, not in the BOM).
- Reference designators are 87xx, so they stay unique on the OOMWOO panel. The panel has two copies; let KiKit (or the panel tool) rename references per copy.

All parts are assembled at JLC. Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`).

## Open items

- Pick the magnet (size, distance) on the first prototype: the switch turns on at about 4 mT and off at about 3.2 mT.
