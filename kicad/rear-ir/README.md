# OOMWOO rear docking IR board

A small board at the back of the robot with two IR receivers, for backing into the dock. It plugs into the [main board](../main-phone/README.md) (REAR-IR1) with a 4-pin cable. Rev 1, 2026-10-28.

The robot backs into the dock, as a mop or auto-empty dock would need, so this board works for those docks too. LiDAR does the coarse approach; the two receivers give the final left/right alignment.

## Circuit

- U8601 (left) and U8602 (right): Everlight IRM-H638T/TR2 (C91447), 38 kHz, top-looking (the lens is on the top face). The same part as the [side sensor board](../side-sensors/README.md) and the dock's U8202.
- The board mounts upright, facing backward, so both receivers look out of the back of the robot.
- Each receiver has its own supply filter, as the datasheet asks: R8601/R8602 100 Ω and C8601/C8602 10 µF, close to the pins.
- The outputs have internal pull-ups; the main board adds nothing.

## Connector J8601

ZX-SH1.0-4PLT (C7430453): JST SH compatible, 1.0 mm pitch, SMD, vertical. The same part as the cliff and Hall boards, and REAR-IR1 on the main board.

| Pin | Signal | Main board |
| --- | --- | --- |
| 1 | 3.3 V | VCC-3V3-REG |
| 2 | IR_L | PC8 (TIM3_CH3 / TIM8_CH3) |
| 3 | IR_R | PC9 (TIM3_CH4 / TIM8_CH4) |
| 4 | GND | |
| 5, 6 | mounting pads, GND | |

Use a pin 1 to pin 1 cable.

## PCB notes (for layout)

- Put U8601 and U8602 about 10 mm apart with a baffle between them (3D-printed, in the rear window). When both see the dock it is straight behind; when one does, steer toward that side. U8601 is the left one seen from behind the robot.
- H8601/H8602: two M2 holes (`MountingHole_2.2mm_M2_Pad`, pads to GND, not in the BOM).
- Reference designators are 86xx, so they stay unique on the OOMWOO panel.

All parts are assembled at JLC. Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`).
