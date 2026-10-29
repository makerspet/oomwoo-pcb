# OOMWOO cliff sensor board

A small board with an IR LED and a phototransistor that looks down at the floor. The robot fits six of them, from the same design, each plugged into the [main board](../main-phone/README.md) (CLIFF-LF1 … CLIFF-RR1) with a 4-pin cable. Rev 1, 2026-10-28. They replace the old Roomba cliff and bumper harness.

## How it works

- The LED and the phototransistor sit 18 mm apart and are tilted toward each other, so their beams cross at the floor. The floor sends the LED's light back into the phototransistor; over a cliff the floor is gone and the signal drops.
- The beams are narrow, so there are no lenses: D8501 IR333-A (940 nm, 5 mm, 20° beam) and Q8501 PT333-3B (5 mm black lens, which blocks visible light).
- **The tilt sets the reference distance.** The beams cross at depth = (spacing / 2) / tan(tilt). With 18 mm spacing:

  | Tilt (each part, from vertical) | Beams cross at |
  | --- | --- |
  | 20° | 24.7 mm |
  | 25° | 19.3 mm |
  | 30° | 15.6 mm |
  | 35° | 12.9 mm |

  Aim the crossing at the normal floor distance. Past the crossing point the beams diverge, so a far floor returns little light even when it is white. This is what lets the sensor tell a dark floor (close, weak) from a cliff (far).
- R8501 (150 Ω) sets the LED current: (5 V − 1.25 V) / 150 Ω ≈ 25 mA, 94 mW in the resistor if the LED is left on.
- The main board switches all six LED cathodes at once (Q7701, `CLIFF_LED_EN` on PC1) and pulls each phototransistor collector up to 3.3 V (47k). Firmware should modulate the LEDs and use LED-on minus LED-off, so sunlight and lamps cancel out.

## Connector J8501

ZX-SH1.0-4PLT (C7430453): JST SH compatible, 1.0 mm pitch, SMD, vertical (top entry). The main board uses the same part.

| Pin | Signal |
| --- | --- |
| 1 | VLED: 5 V from the main board (VCC-5V-REG) |
| 2 | LED cathode, switched on the main board |
| 3 | OUT: phototransistor collector, to an ADC pin |
| 4 | GND: phototransistor emitter |
| 5, 6 | mounting pads, GND |

The LED current returns on pin 2, not on the signal ground, so it doesn't shift the reading. Use a pin 1 to pin 1 cable.

## Main-board channels

| Connector | ADC pin |
| --- | --- |
| CLIFF-LF1 | PA3 |
| CLIFF-RF1 | PA1 |
| CLIFF-LR1 | PA2 |
| CLIFF-RR1 | PA0 |
| CLIFF-LM1 | PD9 |
| CLIFF-RM1 | PE8 |

The names (front, middle, rear) are placeholders; put the six sensors wherever the chassis needs them.

## Assembly (JLC)

- D8501 and Q8501 are through-hole. Order them with JLC's **assembly standoff** (about 2 mm, so the leads have room to bend) and **pin bending** to the tilt angle, or bend them by hand to fit the 3D-printed housing.
- Polarity: LED flat side = cathode (pad 2); phototransistor flat side and square pad = emitter (pad 1).
- Housing: give each part its own bore at the tilt angle, with a wall between them. Many black PLA/PETG filaments pass 940 nm light, so check yours with a phone camera, or line the bores (black paper or tape). The cover can be clear; no lenses are needed.

## PCB notes (for layout)

- About 8 × 27 mm: D8501 and Q8501 18 mm apart centre to centre, J8501 between them, R8501 next to the LED. No mounting holes; the housing holds the board.
- Reference designators are 85xx, so they stay unique on the OOMWOO panel. The panel has six copies; let KiKit (or the panel tool) rename references per copy.

Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`).

## Open items

- Pick the tilt and the LED current on the first boards: measure OUT over a white floor, a black floor and a 20 mm drop, and set the firmware threshold from that.
