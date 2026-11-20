# OOMWOO Hall sensor board

A tiny board with a Hall sensor that detects a magnet. The robot fits four of them, from the same design: one for the dust bin (a magnet in the bin), one for the LiDAR tower bumper (a magnet in the tower cover), and two floor boards that sense magnetic barrier strips (since 2026-11-18). Each plugs into the [main board](../main-phone/README.md) (J7, J8, J10 or J11) with a 3-pin cable. Rev 1, 2026-10-28.

A separate board keeps the mechanics flexible: the bin sits between the blower and the main brush, far from any other board, and the tower cover changes with the LiDAR model.

## Circuit

- U6001: Cross Chip CC6201ST (C285995, ~$0.06): an omnipolar micropower Hall switch, so either magnet pole works. OUT goes low while the magnet is near.
  - It samples at roughly 20-45 Hz, so it reacts within ~25-50 ms. That's fine for the bin, and for the tower about as quick as a microswitch's travel.
  - The output stage isn't confirmed (push-pull or open drain). The main board has no pull-up since 2026-11-04: firmware enables the MCU's internal pull-ups (PE4/PE5), so either type works.
  - Drop-in alternative with the same pinout (1 VDD, 2 OUT, 3 GND): TI DRV5032FADBZR (C140921, ~$0.10, push-pull).
- C6001: 100 nF bypass at U6001.

## Floor variant (magnetic barrier strips)

The same PCB with U6001 fitted as a TI DRV5055A1QDBZR (C962987, ~$0.29), a ratiometric linear Hall sensor with the same SOT-23 pinout (1 VCC, 2 OUT, 3 GND). Two of these go on the underside, front left and right, facing the floor.

- Output at 3.3 V: VCC/2 (~1.65 V) with no field, ±60 mV/mT (100 mV/mT at 5 V), linear to about ±22 mT; either pole shows, with opposite signs. 1 mT is ~75 ADC counts at 12 bits.
- ~6 mA each (the switch draws µA), 20 kHz bandwidth. C6001 (100 nF) is fine as the bypass; no output capacitor needed.
- Firmware reads it as analog and picks the threshold, so the margin over a real strip can be measured. Zero it at start-up away from magnets; the wheel and brush motors have magnets of their own.
- The sensing point is the centre of the package's top face, so mount the board with U6001 facing down, as low as the shell allows: a barrier strip's field falls off within millimetres.
- Fallback if the TI part is short: Hallwee HAL49ESO (C7420984, ~$0.07, ~13 mV/mT at 3.3 V); check its pinout before fitting it.
- A panel of the Hall board now needs two copies of each variant (BOM variant: U6001 only).

## Connector J6001

ZX-SH1.0-3PLT (C7430452), vertical SH. It has 3 pins on purpose (changed 2026-10-29, was 4 with one unused): a Hall cable can't go into a 4-pin cliff or rear IR socket, and the cable is cheaper.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | VSENS-3V3 |
| 2 | OUT (low = magnet; floor variant: analog) | PE4 (bin) / PE5 (tower) / PE10 (floor left) / PF0 (floor right) |
| 3 | GND | |
| 4, 5 | mounting pads, GND | |

Use a pin 1 to pin 1 cable.

## PCB notes (for layout)

- The sensing point is the centre of U6001's top face. Keep the board small so it fits next to the bin or under the tower cover.
- H6001: one M2 hole (`MountingHole_2.2mm_M2_Pad`, pad to GND, not in the BOM). One is enough for a board this small (changed 2026-10-29, was two).
- Reference designators are in this board's 6000s range: every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s, wake-up sensor 7000s. The panel has two copies; let KiKit (or the panel tool) rename references per copy.

All parts are assembled at JLC. Symbols and footprints come from the shared libraries in [`../lib`](../lib) (`JLCImport`).

## Open items

- Pick the magnet (size, distance) on the first prototype: the switch turns on at about 4 mT and off at about 3.2 mT.
