# OOMWOO front ToF board

A small breakout for one VL53L7 8x8-zone time-of-flight sensor, one dock-homing IR receiver and a white torch LED. The robot fits two of them, from the same design: the left board aims 30° left and the right board 30° right, which together cover ~126° in front of the robot. Each board plugs into the [main board](../main-phone/README.md) (J6 or J5) through a 2x4 board-to-board connector, no cable (a 7-pin cable until 2026-11-06). Rev 2, 2026-10-27.

The dock-homing IR receivers were on this project until rev 2, then on the main board (U24, U25) from 2026-10-27. Since 2026-11-11 they are back here, one per board (U2002), so the receiver and the ToF sensor share one bumper opening: a bumper printed in pigmented filament blocks NIR, so both need an opening, and one is smaller than two.

## Circuit

- U2001: VL53L7CH (LCSC C19183986). The VL53L7CX (C5270520) and the VL53L5CX (C3178303, narrower 63° diagonal field of view) use the same footprint and pinout. Pin handling follows the datasheet (DS13865, table 3): RSVD1-4 to GND, RSVD5 not connected, RSVD6 47k pull-up (R2001), thermal pad to GND.
- AVDD (the analog and laser supply, rail VAA-3V3) gets its 3.3 V from VDD-3V3 through L2001 (BLM18PG121SN1D ferrite), so the laser current pulses stay off the shared 3.3 V. Each supply pin has 10 µF + 100 nF: C2001/C2002 on AVDD, C2003/C2004 on IOVDD. Place each pair right at its pins.
- U2002: Everlight IRM-H638T/TR2 (C91447), a 38 kHz IR receiver for the dock beacon, the same part as on the side board and the dock. It is top-looking (the lens is on its top face), and this board stands upright facing forward, so it looks forward too. Supply filter per the datasheet: R2002 100 Ω + C2005 10 µF. The output has an internal pull-up and goes straight to the MCU (U13: left board PE4, right board PE5).
- The VL53L7 INT pin is not wired to the connector (since 2026-11-11): firmware polls the sensor for new data, and J2001 pin 5 carries the IR receiver output instead. INT goes to test pad TP2001 (1 mm), since the sensor is leadless, for anyone who wants to experiment with it. It is open drain, so add a pull-up (for example 47k to 3.3 V) when you use it.
- LPn and I2C_RST stay on this board (since 2026-11-23): R2003 (47k) pulls LPn up to IOVDD and R2004 (47k) pulls I2C_RST down, as the datasheet asks, so the sensor is always enabled and its I2C interface never in reset. Firmware recovers a stuck bus with 9 clocks and a STOP, or by switching VSENS-3V3 off and on (the sensor firmware then has to be uploaded again).
- The I2C pull-ups stay on the main board (2.2k); with pull-ups on every board, a shared bus would be pulled up several times over.
- Each board has its own I2C bus (since 2026-11-23): the left board is on the main board's camera bus (CAM-SCL/CAM-SDA), the right board on the main bus (SCL/SDA). Both sensors start at the default address 0x52 and the left one keeps it. On the main bus the side VL53L0X also starts at 0x52, so at boot firmware holds it off with its XSHUT and moves the right VL53L7 to another address (lost on power-off, so every boot).
- Torch: LED2001, a XINGLIGHT XL-3030UWC-1W-3V white LED (C2843891, 6500K, 1 W 3030, 300 mA max), from the main board's switched 5 V (VSENS-5V-USB) through R2005 (10 Ω, 1 W 2512, C16861), switched low-side by Q2001 (AO3400) on TORCH (main board U28 PB9, PWM). About 190 mA at full duty (VF ~3.0–3.2 V): ~0.6 W in the LED and ~0.36 W in R2005, so give both copper. R2006 (100k) keeps the gate low in reset and with the board unplugged; C2006 (10 µF) bypasses the 5 V at the LED. Firmware sets the brightness by PWM duty. A white LED puts out almost nothing at 940 nm, so it shouldn't disturb the ToF or the IR receiver.
- Parts use the JLC library symbols and footprints (JLCImport:C0603/R0603, 2026-11-05); LPn is named ~{LPn} (active low); a PWR_FLAG on VAA-3V3 clears the ERC error behind the ferrite.

## Connector J2001

Board-to-board, no cable (since 2026-11-06). The board hangs under the main board, upright, and plugs straight into it:

- J2001 (this board): HanElectricity 2005WR-2x4P (C6837622), 2.0 mm 2x4 right-angle pin header, through hole, on the **back** of the board. The sensor is on the front, so the board can sit right at the main board's front edge and the main board stays out of the sensor's 60° x 60° field of view.
- J6 / J5 (main board): HanElectricity 2005FV-2x4P (C18723066), 2.0 mm 2x4 vertical socket, 4.3 mm tall, through hole, fitted on the main board's **underside**.
- A small mount screwed to the main board holds the ToF board upright and takes the load; the header only makes the contact.

| J2001 pin | Signal | Mates with socket pin |
| --- | --- | --- |
| 1 | 3.3 V | 2 |
| 2 | GND | 1 |
| 3 | SDA | 4 |
| 4 | SCL | 3 |
| 5 | IR_OUT (IR receiver; INT until 2026-11-11) | 6 |
| 6 | 5 V (VSENS-5V-USB, torch supply; I2C_RST until 2026-11-23) | 5 |
| 7 | TORCH (torch PWM, active high; ~LPn until 2026-11-23) | 8 |
| 8 | GND | 7 |

**Pin numbers don't match across the mating, on purpose.** On the right-angle header the odd row (1, 3, 5, 7) is the upper row, farther from the board face; mated with a socket on the main board's underside, the rows swap. The schematics already account for this, so this only holds if the socket is placed this way round:

- the socket's pin 1-2 end on the same side as the header's pin 1-2 end
- the socket's odd row (1, 3, 5, 7) toward the ToF board, the even row away from it

Rotated 180°, 3.3 V would meet GND, and 5 V would reach the sensor's I2C lines. Check both boards together in the 3D CAD before ordering, and mark pin 1 on both silkscreens.

## PCB notes (for layout)

- The PCB file in this folder is the old combined layout. Run *Update PCB from Schematic* before layout work.
- Keep the board small. No mounting holes (removed 2026-10-29): a mount screwed to the main board holds it upright, under the main board (designed with the 3D CAD; until 2026-11-06 the board slid into a holder by its long edges). The sensor looks out of the front face; J2001 sits on the back, at the edge that meets the main board.
- The sensor needs a clear view through the bumper window: no copper, silkscreen or part above it, and a cover window from a material on ST's cover-glass list.
- Put TP2001 on the back, away from the sensor's view. It has no paste and stays off the BOM.
- Torch LED2001: on the front face, aimed forward, outside the ToF's 60° x 60° field of view and away from U2002, behind its own bumper opening or diffuser. Light from it must not reach the ToF cover window from inside the bumper. Give LED2001's pads and R2005 copper for heat.
- LED2001's footprint (`JLCImport:LED-3030_XL-3030UWC`) is ours, not JLC's: the datasheet's land pattern and JLC's footprint disagree on which of the LED's two terminals (0.7 mm and 2.0 mm wide) is which, and the wrong guess would let the wide terminal bridge both pads. Both pads are 1.13 mm wide with a 1.3 mm gap, so the LED solders safely either way; pad 1 is the cathode (the chamfered corner, pin 1 in the datasheet). Check a real part's terminals before ordering and, if confirmed, widen the pad under the wide terminal for heat.
- Place U2002 on the front face right next to the sensor, so one bumper opening covers both, and keep it and the baffle out of the sensor's 60° x 60° field of view. An opaque baffle between them (part of the mount or bumper) keeps the ToF laser off the receiver.
- Reference designators are in this board's 2000s range: every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s, wake-up sensor 7000s. The panel has two copies of this board; let KiKit (or the panel tool) rename references per copy so the assembly files stay unique.

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
