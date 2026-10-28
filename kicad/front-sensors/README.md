# OOMWOO front ToF board

A small breakout for one VL53L7 8x8-zone time-of-flight sensor. The robot fits two of them, from the same design: the left board aims 30° left and the right board 30° right, which together cover ~126° in front of the robot. Each board plugs into the [main board](../main-phone/README.md) (VL-L1 or VL-R1) with a 7-pin cable. Rev 2, 2026-10-27.

Until rev 2, this project also held the two dock-homing IR receivers. They are now on the main board (U7501, U7502), since the main board sits at the very front of the robot anyway.

## Circuit

- U8301: VL53L7CH (LCSC C19183986). The VL53L7CX (C5270520) and the VL53L5CX (C3178303, narrower 63° diagonal field of view) use the same footprint and pinout. Pin handling follows the datasheet (DS13865, table 3): RSVD1-4 to GND, RSVD5 not connected, RSVD6 47k pull-up (R8301), thermal pad to GND.
- AVDD (the analog and laser supply) gets its 3.3 V through L8301 (BLM18PG121SN1D ferrite), so the laser current pulses stay off the shared 3.3 V. Each supply pin has 10 µF + 100 nF: C8301/C8302 on AVDD, C8303/C8304 on IOVDD. Place each pair right at its pins.
- No pull-ups on this board. The main board holds all of them: I2C 2.2k, INT and LPn 47k, and the I2C_RST 47k pull-down. With pull-ups on every board, the shared I2C bus would be pulled up three times over (~730 Ω).
- Both sensors start at I2C address 0x52. At start-up the firmware holds one sensor's LPn low and moves the other to a new address. The new address is lost on power-off, so this runs every boot.

## Connector J8301

ZX-SH1.0-7PWT (C7430449): JST SH compatible, 1.0 mm pitch, SMD, right angle. The main board uses the same part.

| Pin | Signal |
| --- | --- |
| 1 | 3.3 V |
| 2 | GND |
| 3 | I2C_RST |
| 4 | SDA |
| 5 | SCL |
| 6 | INT |
| 7 | LPn |
| 8, 9 | mounting pads, GND |

Use a pin 1 to pin 1 cable (pre-made SH cables are sold both ways; Qwiic cables are pin 1 to pin 1). Mark pin 1 on the silkscreen of both boards.

## PCB notes (for layout)

- The PCB file in this folder is the old combined layout. Run *Update PCB from Schematic* before layout work.
- Keep the board small. H8301/H8302: two M2 holes (`MountingHole_2.2mm_M2_Pad`, pads to GND, not in the BOM) for the 30° bracket; M2 keeps the board narrow (M3 pads would set most of its width). The sensor looks out of the board face; the connector exits behind it.
- The sensor needs a clear view through the bumper window: no copper, silkscreen or part above it, and a cover window from a material on ST's cover-glass list.
- Reference designators are 83xx, so they stay unique on the OOMWOO panel. The panel has two copies of this board; let KiKit (or the panel tool) rename references per copy so the assembly files stay unique.

## Assembly: the sensor is placed by hand

JLC assembles the passives and the connector; U8301 is left off (`in_bom no`, `in_pos_files no`) and placed and reflowed by hand. JLC's price for the sensor is high and stock is thin, while distributors are about $3 cheaper per sensor (2026-10-27, volume prices):

| Source | Part | Price |
| --- | --- | --- |
| JLC/LCSC | VL53L7CH / VL53L7CX | $11.46 (2 in stock) / $8.46 (77) |
| DigiKey | VL53L7CX / VL53L7CH | $6.06 / $6.21 at 1,000 |
| Mouser | VL53L7CX | $5.72 at 500, $5.17 at 3,600 |
| ST | VL53L7CH / VL53L5CX | $5.63 / $5.89 at 500 (tariffs not checked) |

The board is one-sided with a handful of parts, so a small home reflow oven handles it. The sensor is an LGA: use a stencil (order one with the boards) and check the pads for bridges under a magnifier before power-up.

## Open items

- Bracket angle and the cover window material.
