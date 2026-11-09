# OOMWOO front ToF board

A small breakout for one VL53L7 8x8-zone time-of-flight sensor. The robot fits two of them, from the same design: the left board aims 30° left and the right board 30° right, which together cover ~126° in front of the robot. Each board plugs into the [main board](../main-phone/README.md) (VL-L1 or VL-R1) through a 2x4 board-to-board connector, no cable (a 7-pin cable until 2026-11-06). Rev 2, 2026-10-27.

Until rev 2, this project also held the two dock-homing IR receivers. They are now on the main board (U24, U25), since the main board sits at the very front of the robot anyway.

## Circuit

- U2001: VL53L7CH (LCSC C19183986). The VL53L7CX (C5270520) and the VL53L5CX (C3178303, narrower 63° diagonal field of view) use the same footprint and pinout. Pin handling follows the datasheet (DS13865, table 3): RSVD1-4 to GND, RSVD5 not connected, RSVD6 47k pull-up (R2001), thermal pad to GND.
- AVDD (the analog and laser supply, rail VAA-3V3) gets its 3.3 V from VDD-3V3 through L2001 (BLM18PG121SN1D ferrite), so the laser current pulses stay off the shared 3.3 V. Each supply pin has 10 µF + 100 nF: C2001/C2002 on AVDD, C2003/C2004 on IOVDD. Place each pair right at its pins.
- No pull-ups on this board. The main board holds them: I2C 2.2k, the shared INT 47k (R61) and the right LPn 47k (R196). The MCU drives the left LPn and I2C_RST directly (no resistors since 2026-11-04). With pull-ups on every board, the shared I2C bus would be pulled up three times over (~730 Ω).
- Both sensors start at I2C address 0x52. At start-up the firmware holds one sensor's LPn low and moves the other to a new address. The new address is lost on power-off, so this runs every boot.
- Parts use the JLC library symbols and footprints (JLCImport:C0603/R0603, 2026-11-05); LPn is named ~{LPn} (active low); a PWR_FLAG on VAA-3V3 clears the ERC error behind the ferrite.

## Connector J2001

Board-to-board, no cable (since 2026-11-06). The board hangs under the main board, upright, and plugs straight into it:

- J2001 (this board): HanElectricity 2005WR-2x4P (C6837622), 2.0 mm 2x4 right-angle pin header, through hole, on the **back** of the board. The sensor is on the front, so the board can sit right at the main board's front edge and the main board stays out of the sensor's 60° x 60° field of view.
- VL-L1 / VL-R1 (main board): HanElectricity 2005FV-2x4P (C18723066), 2.0 mm 2x4 vertical socket, 4.3 mm tall, through hole, fitted on the main board's **underside**.
- A small mount screwed to the main board holds the ToF board upright and takes the load; the header only makes the contact.

| J2001 pin | Signal | Mates with socket pin |
| --- | --- | --- |
| 1 | 3.3 V | 2 |
| 2 | GND | 1 |
| 3 | SDA | 4 |
| 4 | SCL | 3 |
| 5 | INT | 6 |
| 6 | I2C_RST | 5 |
| 7 | ~LPn (active low) | 8 |
| 8 | GND | 7 |

**Pin numbers don't match across the mating, on purpose.** On the right-angle header the odd row (1, 3, 5, 7) is the upper row, farther from the board face; mated with a socket on the main board's underside, the rows swap. The schematics already account for this, so this only holds if the socket is placed this way round:

- the socket's pin 1-2 end on the same side as the header's pin 1-2 end
- the socket's odd row (1, 3, 5, 7) toward the ToF board, the even row away from it

Rotated 180°, 3.3 V would meet GND. Check both boards together in the 3D CAD before ordering, and mark pin 1 on both silkscreens.

## PCB notes (for layout)

- The PCB file in this folder is the old combined layout. Run *Update PCB from Schematic* before layout work.
- Keep the board small. No mounting holes (removed 2026-10-29): a mount screwed to the main board holds it upright, under the main board (designed with the 3D CAD; until 2026-11-06 the board slid into a holder by its long edges). The sensor looks out of the front face; J2001 sits on the back, at the edge that meets the main board.
- The sensor needs a clear view through the bumper window: no copper, silkscreen or part above it, and a cover window from a material on ST's cover-glass list.
- Reference designators are in this board's 2000s range: every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s. The panel has two copies of this board; let KiKit (or the panel tool) rename references per copy so the assembly files stay unique.

## Assembly: the sensor is placed by hand

JLC assembles the passives and the connector; U2001 is left off (`in_bom no`, `in_pos_files no`) and placed and reflowed by hand. JLC's price for the sensor is high and stock is thin, while distributors are about $3 cheaper per sensor (2026-10-27, volume prices):

| Source | Part | Price |
| --- | --- | --- |
| JLC/LCSC | VL53L7CH / VL53L7CX | $11.46 (2 in stock) / $8.46 (77) |
| DigiKey | VL53L7CX / VL53L7CH | $6.06 / $6.21 at 1,000 |
| Mouser | VL53L7CX | $5.72 at 500, $5.17 at 3,600 |
| ST | VL53L7CH / VL53L5CX | $5.63 / $5.89 at 500 (tariffs not checked) |

The board is one-sided with a handful of parts, so a small home reflow oven handles it. The sensor is an LGA: use a stencil (order one with the boards) and check the pads for bridges under a magnifier before power-up.

## Open items

- Holder angle and the cover window material.
