# OOMWOO main board, phone-compute version (v1)

Fork of [`../main`](../main) for the first board: an Android phone is the compute, connected to the STM32 over USB-C. Decided 2026-10-25.

Removed compared with `main`:
- Raspberry Pi CM4/CM5 and everything only it used: SD card, M.2 slot and its 3.3 V buck, CM console header, internal USB header (mic board)
- both MIPI camera connectors
- speaker amplifier (NS4168): the phone's speaker is used
- water pump and its switch (no mopping in v1)
- front-board illumination switch (no camera in v1)
- the dedicated 5 V buck for the phone's USB-C: it now runs from the main 5 V (VCC-5V-REG)
- the board fan (FAN1, Q3, D17, R87) and the left side-proximity connector (SIDE-L1)

Moved or added:
- front ToF boards (2x VL53L7) now on the STM32: I2C on I2C4 (shared with the side boards), PC0 = VL-I2C-RESET, PD12 = VL-L-INT, PB13 = VL-L-LPn
- USB-C CC1/CC2 to the STM32 UCPD (PB6/PB4) with ESD (D7101); 5V_EN moved from PB4 to PB5
- VBUS sense divider to PA7 (ADC); Q7101/Q7102 block the phone's VBUS from back-feeding the robot 5 V (the TMI6240 doesn't block reverse current)
- the six mounting standoffs (MP1-MP6) moved to the POWER sheet

Added 2026-10-27 (details in [docs/SPEC.md](../../docs/SPEC.md#phone-compute-board-v1)):
- power control: charger rail-hold (Q7303, R7305) and a ~4-9 s hardware off timer (U7301, Q7301, Q7302); PA15 goes through R7301 (1k)
- 20 V input: SMAJ22A TVS (D7301), 10 µF/50 V 1206 DC_IN capacitors, low-profile DC-044A-20A barrel jack (7.2 mm tall)
- bumpers: 2x ITR9606 photo-interrupters on the board (BUMP-R1, BUMP-L1) in parallel with the harness bumpers (backup); Q7304 switches both emitters
- DC_IN sense: R7310/R7311 (/11) + C7304 to PB15
- VBUS lockout (Q7305, Q7306, R7312-R7314): the robot 5 V can't turn on while the phone sources VBUS
- the unused sheet files copied from `main` (CM5, M.2, MIPI camera, speaker, water pump) are deleted
- carpet: LO AC-coupled to the Q18 gate (C7303)
- LIDAR2: right-angle 1x5 header (PZ254R-11-05P)
- STM32_DEBUG1 (1x5 0.1", PZ254V-11-05P) and JTAG1 (2x7 1.27 mm SMD, STDC14 pinout, C55099228): vertical, reached from the top under a small removable cover (changed 2026-10-28)
- spare I/O pads J7301 (2x11, do not fit); R7306 1k on PB10; R7307 47k pull-up on VL-R-LPn
- pins freed (2026-10-28), details in [docs/SPEC.md](../../docs/SPEC.md#phone-compute-board-v1):
  - LiDAR rail enable joined ~VM-VBAT-EN (PE10)
  - one ToF interrupt line (PD12) for both VL53L7s and the side sensor; the right LPn is held up by R7307
  - IMU on I2C4 (R18/R72 not fitted); its FSYNC (100k pull-down R7601) and INT2 go to J7301
  - PWR_EN on PD7, so PC10/PC11 are a spare UART on J7301; R7315 pulls PA9 up (UCPD dead-battery Rd on CC1)
- BOM: all 100 nF → 100nF/50V (C1591), 10uF/6.3V → 10uF/10V (C19702)
- new DC-044A-20A footprint and 3D model in `../main/JLCImport.pretty` / `JLCImport.3dshapes`
- 3.3 V and 5 V bucks (U21, U22): TPS54560B replaces the out-of-stock AP64501, with SS56 catch diodes (D7401/D7402), RT resistors (R7401/R7402), a U21 EN divider (R7403/R7404) and new compensation; BAT-VCC input caps are now 10 µF/50 V 1206
- front IR receivers moved onto the board: U7501 (left) and U7502 (right), IRM-V838M3-C side-looking SMD, each with 100 Ω (R7501/R7502) + 10 µF (C91/C90). The IR-F1/IR-F2 connectors are gone. Place both at the board's front edge, lenses facing forward, ~10 mm apart, with a baffle between them
- VL-L1 / VL-R1: JST SH 7-pin (ZX-SH1.0-7PWT) to the [front ToF boards](../front-sensors/README.md)
- SIDE-R1: JST SH 7-pin (ZX-SH1.0-7PWT) to the [side sensor board](../side-sensors/README.md) (VL53L0X + IRM-H638T), same pinout as before

Libraries, footprints and 3D models are shared with `../main` (see `fp-lib-table`, `sym-lib-table`).

The PCB file is still the `main` layout: run *Update PCB from Schematic* before layout work.
