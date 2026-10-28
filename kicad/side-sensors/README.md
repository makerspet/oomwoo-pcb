# OOMWOO side sensor board

A small board on the robot's right side, for wall-following and for spotting the dock while driving past it. It plugs into the [main board](../main-phone/README.md) (SIDE-R1) with a 7-pin cable. Rev 2, 2026-10-27. There is no left side sensor on v1.

Rev 1 had a VL6180 with a 2.8 V regulator and a TSOP38238. The VL6180 is NRND at ST (obsolete at DigiKey and Future), and its 2.8 V I/O sits at its limit on the robot's 3.3 V bus.

## Circuit

- U8401: VL53L0X (VL53L0CXV0DH/1, LCSC C91199, ~$1.63): single-zone time-of-flight distance sensor, runs from 3.3 V directly.
  - It reads poorly below ~3 cm, so the board sits a little recessed in the robot's side.
  - 10 µF + 100 nF (C8401/C8402) at its supply pins.
  - R8401 (10k) pulls XSHUT up and R8402 (10k) pulls up GPIO1 (open drain, the interrupt); the datasheet asks for both, and the main board has none on these lines. The I2C pull-ups (2.2k) are on the main board.
  - Firmware: the I/Os run at 3.3 V (= AVDD), so set the ST API to 2V8 I/O mode (the API default is 1V8).
- U8402: Everlight IRM-H638T/TR2 (C91447, ~$0.13), a 38 kHz top-looking IR receiver (the lens is on its top face), the same part as the dock's U8202. It sees the dock's beacon when the robot passes alongside it. Supply filter per the datasheet: R8403 100 Ω + C8403 10 µF. The output has an internal pull-up.

Both parts look out of the board face, so the board mounts upright in the side of the robot, facing out.

## Connector J8401

ZX-SH1.0-7PWT (C7430449): JST SH compatible, 1.0 mm pitch, SMD, right angle. The main board's SIDE-R1 uses the same part.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | |
| 2 | GND | |
| 3 | IR_OUT | PD6 (USART2 RX) |
| 4 | GPIO1 (interrupt) | PE2 |
| 5 | XSHUT | PE3 |
| 6 | SCL | I2C4 SCL (PC6) |
| 7 | SDA | I2C4 SDA (PC7) |
| 8, 9 | mounting pads, GND | |

Use a pin 1 to pin 1 cable and mark pin 1 on the silkscreen of both boards.

The VL53L0X starts at I2C address 0x52, the same as the two front VL53L7s on the same bus. At boot, hold both VL53L7 LPn pins low (that turns their I2C off), move the VL53L0X to a new address, then bring the front sensors up one at a time. XSHUT isn't needed for this; it stays wired for resetting a stuck sensor and for hardware standby.

## PCB notes (for layout)

- The PCB file in this folder is the old layout. Run *Update PCB from Schematic* before layout work.
- H8401/H8402: two M2 holes (`MountingHole_2.2mm_M2_Pad`, pads to GND, not in the BOM), to keep the board small.
- Keep copper, silkscreen and parts out of the sensor's field of view, and give it a cover window (ST's cover-glass guidance applies).
- Reference designators are 84xx, so they stay unique on the OOMWOO panel.

All parts are assembled at JLC.

Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`) and the KiCad standard libraries.
