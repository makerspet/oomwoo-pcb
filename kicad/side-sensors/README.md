# OOMWOO side sensor board

A small board on the robot's right side, for wall-following and for spotting the dock while driving past it. It plugs into the [main board](../main-phone/README.md) (SIDE-R1) with a 7-pin cable. Rev 2, 2026-10-27. There is no left side sensor on v1.

Rev 1 had a VL6180 with a 2.8 V regulator and a TSOP38238. The VL6180 is NRND at ST (obsolete at DigiKey and Future), and its 2.8 V I/O sits at its limit on the robot's 3.3 V bus.

## Circuit

- U3001: VL53L0X (VL53L0CXV0DH/1, LCSC C91199, ~$1.63): single-zone time-of-flight distance sensor, runs from 3.3 V directly.
  - It reads poorly below ~3 cm, so the board sits a little recessed in the robot's side.
  - 10 µF + 100 nF (C3001/C3002) at its supply pins.
  - R3001 (10k) pulls XSHUT up and R3002 (10k) pulls up GPIO1 (open drain, the interrupt); the datasheet asks for both, and the main board has none on these lines. The I2C pull-ups (2.2k) are on the main board.
  - Firmware: the I/Os run at 3.3 V (= AVDD), so set the ST API to 2V8 I/O mode (the API default is 1V8).
- U3002: Everlight IRM-H638T/TR2 (C91447, ~$0.13), a 38 kHz top-looking IR receiver (the lens is on its top face), the same part as the dock's U1202. It sees the dock's beacon when the robot passes alongside it. Supply filter per the datasheet: R3003 100 Ω + C3003 10 µF. The output has an internal pull-up.

Both parts look out of the board face, so the board mounts upright in the side of the robot, facing out.

## Connector J3001

ZX-SH1.0-7PWT (C7430449): JST SH compatible, 1.0 mm pitch, SMD, right angle. The main board's SIDE-R1 uses the same part.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | |
| 2 | GND | |
| 3 | IR_OUT | PD6 (USART2 RX) |
| 4 | GPIO1 (interrupt) | PD12, shared with the front ToF interrupts (open drain) |
| 5 | XSHUT | PE3 |
| 6 | SCL | I2C4 SCL (PC6) |
| 7 | SDA | I2C4 SDA (PC7) |
| 8, 9 | mounting pads, GND | |

Use a pin 1 to pin 1 cable and mark pin 1 on the silkscreen of both boards.

The VL53L0X starts at I2C address 0x52, the same as the two front VL53L7s on the same bus. Only the left VL53L7's LPn is on the MCU, so XSHUT takes part in addressing: at boot, hold the left LPn and XSHUT low, so only the right VL53L7 answers, and move it to a new address. Release the left LPn and move the left sensor, then release XSHUT; the VL53L0X can keep 0x52. XSHUT also resets a stuck sensor.

## PCB notes (for layout)

- The PCB file in this folder is the old layout. Run *Update PCB from Schematic* before layout work.
- H3001/H3002: two M2 holes (`MountingHole_2.2mm_M2_Pad`, pads to GND, not in the BOM), to keep the board small.
- Keep copper, silkscreen and parts out of the sensor's field of view, and give it a cover window (ST's cover-glass guidance applies).
- Reference designators are in this board's 3000s range: every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s.

All parts are assembled at JLC.

Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`) and the KiCad standard libraries.
