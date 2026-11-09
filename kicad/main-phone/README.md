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
- USB-C CC1/CC2 to the STM32 UCPD (PB6/PB4) with ESD (D40); 5V_EN moved from PB4 to PB5
- VBUS sense divider to PA7 (ADC); Q27/Q28 block the phone's VBUS from back-feeding the robot 5 V (the TMI6240 doesn't block reverse current)
- the six mounting standoffs (MP1-MP6) moved to the POWER sheet

Added 2026-10-27 (details in [docs/SPEC.md](../../docs/SPEC.md#phone-compute-board-v1)):
- power control: charger rail-hold (Q31, R194) and a ~4-9 s hardware off timer (U23, Q29, Q30); PA15 goes through R190 (1k)
- 20 V input: SMAJ22A TVS (D41), 10 µF/50 V 1206 DC_IN capacitors, low-profile DC-044A-20A barrel jack (7.2 mm tall)
- bumpers: 2x ITR9606 photo-interrupters on the board (BUMP-R1, BUMP-L1); Q32 switches both emitters
- DC_IN sense: R199/R200 (/11) + C175 to PB15
- VBUS lockout (Q33, Q34, R201-R203): the robot 5 V can't turn on while the phone sources VBUS
- the unused sheet files copied from `main` (CM5, M.2, MIPI camera, speaker, water pump) are deleted
- carpet: LO AC-coupled to the Q18 gate (C174)
- LIDAR2: right-angle 1x5 header (PZ254R-11-05P); replaced 2026-10-29, see below
- STM32_DEBUG1 (1x5 0.1", PZ254V-11-05P) and JTAG1 (2x7 1.27 mm SMD, STDC14 pinout, C55099228): vertical, reached from the top under a small removable cover (changed 2026-10-28)
- spare I/O pads J7301 (2x11, do not fit; now J1, see 2026-10-30); R195 1k on PB10; R196 47k pull-up on VL-R-LPn
- pins freed (2026-10-28), details in [docs/SPEC.md](../../docs/SPEC.md#phone-compute-board-v1):
  - LiDAR rail enable joined ~VM-VBAT-EN (PE10)
  - one ToF interrupt line (PD12) for both VL53L7s and the side sensor; the right LPn is held up by R196
  - IMU on I2C4 (R18/R72 not fitted, removed 2026-10-30); its FSYNC (100k pull-down R211) and INT2 go to J7301
  - PWR_EN on PD7, so PC10/PC11 are a spare UART on J7301; R204 pulls PA9 up (UCPD dead-battery Rd on CC1)
- BOM: all 100 nF → 100nF/50V (C1591), 10uF/6.3V → 10uF/10V (C19702)
- new DC-044A-20A footprint and 3D model in `JLCImport.pretty` / `JLCImport.3dshapes` (now in `../lib`)
- 3.3 V and 5 V bucks (U21, U22): TPS54560B replaces the out-of-stock AP64501, with SS56 catch diodes (D42/D43), RT resistors (R205/R206), a U21 EN divider (R207/R208) and new compensation; BAT-VCC input caps are now 10 µF/50 V 1206
- front IR receivers moved onto the board: U24 (left) and U25 (right), IRM-V838M3-C side-looking SMD, each with 100 Ω (R209/R210) + 10 µF (C91/C90). The IR-F1/IR-F2 connectors are gone. Place both at the board's front edge, lenses facing forward, ~10 mm apart, with a baffle between them
- VL-L1 / VL-R1: 2.0 mm 2x4 vertical sockets (HanElectricity 2005FV-2x4P, C18723066) on the underside since 2026-11-06; the [front ToF boards](../front-sensors/README.md) plug in directly (2005WR-2x4P right-angle header), no cable. Pinout 1 GND, 2 VSENS-3V3, 3 SCL, 4 SDA, 5 VL-I2C-RESET, 6 ~INT-SENSORS, 7 GND, 8 LPn: the mating swaps the rows, so place each socket as the ToF README says (JST SH 7-pin ZX-SH1.0-7PWT before)
- cliff sensors (2026-10-28): the Roomba harness (BUMP_CLIFF1, R30, R35) is replaced by six SH 4-pin vertical connectors (CLIFF-LF1 … CLIFF-RR1) for the [cliff sensor boards](../cliff-sensor/README.md); Q35 switches all cliff LEDs from CLIFF_LED_EN (R214 pull-down); new pull-ups R212/R213 for cliff LM (PD9) and RM (PE8)
- rear docking IR and Hall boards (2026-10-28), on the SIDE-PROXI sheet: REAR-IR1 (PC8 left, PC9 right), HALL-BIN1 (PE4) and HALL-TOWER1 (PE5) with 47k pull-ups R215/R216; all ZX-SH1.0-4PLT, connected through global labels
- SIDE-R1: JST SH 7-pin (ZX-SH1.0-7PWT) to the [side sensor board](../side-sensors/README.md) (VL53L0X + IRM-H638T), same pinout as before

Changed 2026-10-29 (details in [docs/SPEC.md](../../docs/SPEC.md#phone-compute-board-v1)):
- LIDAR2 is now 2x3 0.1" through-hole pads, not fitted: 1 LiDAR RX, 2 GND, 3 MOT-, 4 VM-5V-LIDAR, 5 LiDAR TX (shared with LIDAR1 pin 3), 6 VM-5V-LIDAR (motor + for LiDARs that don't drive their own motor)
- R113 moved to the LiDAR sheet (between LIDAR1 pin 3 and PD2); R117 removed; R66, R113, R183 are 100 Ω
- motor shunts: R15/R65 (wheels) RLH12FTCR250 1 W, R83 (side brush) RLH12FTCR300 1 W, R84 (main brush) LRBK25EFER110 2 W 2512 (new footprint)
- HALL-BIN1 and HALL-TOWER1 are 3-pin SH (ZX-SH1.0-3PLT, C7430452): 1 3.3 V, 2 OUT, 3 GND
- the mounting pads of all SH sockets go to GND (the cliff, rear IR and Hall ones were not connected)
- R7 removed: the VL-R-INT pull-up was in parallel with R61, because both INT lines are joined on PD12

Changed 2026-10-30:
- J7301 → J1: a fitted 0.1" 2x7 vertical header (PZ254V-12-14P, C492424) with spares only: 1 3.3 V, 2 5 V, 3/4 not connected (I2C4 kept off), 5/6 UART PC10/PC11, 7 PA10, 8 PE6, 9 PA8, 10 PA9, 11 PD4, 12 PE2, 13/14 GND. The rear IR, Hall and cliff LM/RM signals are off it (they have their own connectors)
- IMU INT2 goes to test pad TP1 (1.5 mm, not in the BOM) instead of the spare header; FSYNC is reachable on its pull-down R211
- IMU AP_AD0 was floating: R217 (10k) pulls it low, so the I2C address is 0x68
- R18/R72 (unfitted IMU I2C pull-ups) removed

Changed 2026-10-31:
- R19 (0 Ω in series with the 8 MHz crystal) removed: PF1-OSC_OUT goes straight to X1
- the LDR (R75) runs from VCC-3V3, not the switched sensor rail VCC-3V3-REG, so it works with the sensors off and reads against the ADC reference
- power rails drawn as power symbols; the rear IR, Hall, cliff LM/RM, DC_IN_SENSE, PWR-SW-G and WD_OK signals are hierarchical labels joined on the top sheet (were global labels)

Changed 2026-11-01:
- renamed: VM-VBAT → VMOT-14V4, BAT-VCC → VBAT-14V4, MAIN-FAN-S-CTRL → MAIN-FAN-PWM, MAIN-FAN-S-SENSE → MAIN-FAN-FB, 3.3V_STM1 → D44, 3.3V_SENSORS1 → D45; 3.3V_EN drawn active low (~{3.3V_EN})
- sensor rail switch: one AO3401 (Q16); Q17, R91, R96, R97 and D39 removed (D39 back-fed the "off" rail). R195 10k, R90 100k, C64 100 nF gate-drain (soft start), new C176 1 µF gate-source (stays off at power-on). Details in [docs/SPEC.md](../../docs/SPEC.md#phone-compute-board-v1)
- C7/C101 (unfitted 150 pF on the fan PWM/FB lines) removed; R195 moved to the power sheet

Changed 2026-11-02:
- renamed: VCC-3V3 → VMCU-3V3, VCC-3V3-REG → VSENS-3V3, VCC-5V-REG → VSENS-5V-USB, 3.3VBAT → VMCU-BAT-3V3, ~{3.3V_EN} → ~{VSENS_3V3_EN}, 5V_EN → VSENS_5V_USB_EN, VL-L-INT → VL-INT (the two ToF INT lines now join inside the front sensors sheet)
- J1 pin 1 and R204 (PA9 pull-up) on VMCU-3V3, the MCU rail
- STM32_DEBUG1: 1x6 (PZ254V-11-06P, C492405) instead of 1x5, so the TTL-234X-3V3 socket seats fully; pin 6 (RTS#) not connected
- J1: 2x6 (PZ254V-12-12P, C492423) instead of 2x7; the unused 3/4 pair is gone: 1 VMCU-3V3, 2 VSENS-5V-USB, 3/4 UART PC10/PC11, 5 PA10, 6 PE6, 7 not connected, 8 PA9, 9 PD4, 10 PE2, 11/12 GND
- R120/R121 (1k button pull-ups to the sensor rail) removed: firmware uses the internal pull-ups on PD0/PD5. On VSENS-3V3 the buttons read as pressed while the sensor rail was off
- TP1 removed: probe IMU INT2 on R92
- I2C4 pull-ups R5/R6 on the top sheet; the small hierarchical sheets merged into the top sheet
- renamed: VUS → VUSONIC-14V4, VL-INT → INT-SENSORS (not only the VL53 sensors), U12 → L4 (inductor), 5V1 → D46
- battery voltage sense: R218 (1M) / R219 (100k) + C177 (100 nF) from P+/C+ (battery side of Q14) to PA8 (ADC5_IN1); J1 pin 7 (was PA8) not connected
- bumper pull-ups R44/R48 47k → 1k, so PA4/PA5 (ADC2) see the slot opening and closing instead of a switch

Changed 2026-11-03:
- bumper emitters split: BUMP-R1 on new Q36 (PA10, BUMP_R_LED_EN, R221 pull-down; a pull-up since 2026-11-05), BUMP-L1 stays on Q32 (PC3, BUMPER_LED_EN → BUMP_L_LED_EN); each LED has its own 180 Ω (R197, new R220), so firmware can PWM-dim each one
- C178/C179 (47 nF) on BUMP-R/L to filter the LED PWM
- J1 pin 5 (was PA10) not connected
- PA9 and PE10 swapped: ~{VMOT-14V4-EN} on PA9 (also UCPD DBCC1), the J1 pin 8 spare on PE10 (no pull-up, ADC capable). One 10k pull-up (R184, was 100k) serves both; R204 and R182 removed
- bumper circuit (BUMP-L1/R1, emitter switches, pull-ups R44/R48, C178/C179) on its own sheet (bumper_sensors), moved off CLIFF; nets BUMP-L-Q+/BUMP-R-Q+ renamed BUMP-L/BUMP-R
- main fan: MAIN_FAN1 is a Micro-Fit 3.0 compatible 1x4 right angle (Lian Xin XDWF-C3030WR-1*4P, C50399536, fitted; Molex 43650-0400 also fits), so the Dreame 2x2-to-1x4 fan cables can be reused for high-power fans; pinout 1 VCC, 2 GND, 3 PWM, 4 FG (Dreame L60 Ultra PE). The old PH 4-pin SMD header is gone. MAIN_FAN2/MAIN_FAN3 (PA/PH alternatives) and the fan ID on PE10 were added and removed again the same day; PE10 is the J1 pin 8 spare. Details in [docs/SPEC.md](../../docs/SPEC.md#main-fan-connectors-v1-2026-11-03)
- Q37 (AO4407C) in parallel with Q1 on the motor rail, with its own 10 Ω gate resistor R222
- Q14 (battery disconnect while charging, in series with all battery current): AOD407 (68 mΩ) → AO4407C, plus Q38 AO4407C in parallel. Q12 stays AOD407
- LIDAR2: 1x6 0.1" right-angle header (PZ254R-11-06P, C492414), not fitted: 1/2 VLIDAR-5V, 3 GND, 4 MOT-, 5 LiDAR TX, 6 LiDAR RX; renamed VM-5V-LIDAR → VLIDAR-5V, LiDAR-M-CTRL → LIDAR-MOTOR-CTRL; PWR_FLAG on VLIDAR-5V
- R61 (47k INT-SENSORS pull-up) moved to the top sheet, since the ToF boards and the side sensor share it; the side sensor board's own GPIO1 pull-up (R3002) is removed
- side sensor board: R3001 (XSHUT pull-up) removed too (2026-11-04); PE3 drives XSHUT, firmware holds it low before the sensor rail comes up
- R2 (VL-I2C-RESET pull-down), R62 (~{VL-L-LPn} pull-up), R93 (IMU INT1 pull-up) and R215/R216 (Hall pull-ups) removed (2026-11-04): the MCU drives PC0/PB13, IMU INT1 runs push-pull, the Hall inputs use the MCU pull-ups; VL-L-LPn renamed ~{VL-L-LPn}. The cliff and wheel-drop pull-ups stay
- X1 (8 MHz crystal) with C34/C35 and R80 (10 Ω in IR-F-RX2) removed (2026-11-04): USB is crystal-less (HSI48 + CRS), PF0/PF1 not connected, both front IR receivers go straight to the MCU. Renamed: INT-SENSORS → ~{INT-SENSORS}, CLEAN/HOME/POWER-BTN → ~{…}, SIDE/MAIN-BRUSH-CURRENT-ADC → SIDE/MAIN-BRUSH-ADC, SPARE-PE10 → SPARE-PE10-ADC, STM32-SWO → STM32-SWO-SPARE
- R198 (100k BUMP_L_LED_EN pull-down) removed and R221 turned into a 100k pull-up to VMCU-3V3 (2026-11-05): the emitters run from VSENS-5V-USB, whose buck enable (PB5) R168 holds low whenever the MCU pins float, so the LEDs cannot light in reset. PA10 is also UCPD DBCC2, so the pull-up turns the dead-battery Rd on CC2 on in reset (CC1 already had it through R184): the phone attaches in either plug orientation. BUMP-R-LED-K label flipped to the right of the drain wire to make room. Front-sensors sheet parts moved to JLC symbols and footprints (JLCImport:C0603/R0603)
- DRV8870 IN pull-downs R3, R4 (main brush), R55, R57 (side brush), R11, R17, R20, R27 (wheels) removed (2026-11-04): the driver has internal ~100k pull-downs, and the motor rail is off in reset and when the watchdog stops
- USB power moved out of the Battery-Charger sheet into its own sheet, usb_power (2026-11-08); renamed USB2 → USBC2, PWR_EN → USB_PWR_EN, VBUS → VBUS_5V, VBUS_SRC → VBUS_5V_SRC, D+/D- → DP/DN
- BAT2: CJT C3030WV-4P vertical through-hole Micro-Fit 3.0 compatible 1x4 (C239441, 8.5 A; Molex 43650-0415 fits the same footprint) instead of the Molex 43650-0412 SMD right angle (2026-11-07). Fit it on the underside, facing down into the battery compartment. Pins 1-4 unchanged; the SMD solder tabs (pins 5, 6 on GND) are gone
- cliff LED resistors moved from the cliff boards (R4001) to the main board (2026-11-06): R224-R229 (150 Ω, C22808) in series with pin 1 of CLIFF-LF1, -LM1, -LR1, -RF1, -RM1, -RR1, so each cable carries a current-limited LED anode, not bare 5 V; cliff board net VLED-5V → LED_A. R214 (100k CLIFF_LED_EN pull-down) removed too: the cliff LEDs run from VSENS-5V-USB, which is off whenever PC1 floats
- cliff nets renamed LF-Q+ ... RM-Q+ → CLIFF-LF ... CLIFF-RM (cliff sensor board: VLED → VLED-5V)

Outputs (schematic PDF, BOM) are in [output/](output), regenerated with `python tools/export.py` (add `--pcb` for Gerbers, placement and STEP once the layout is done). The firmware pin header comes from this schematic: `python tools/gen_pins.py -o ../oomwoo-firmware/include/oomwoo_pins.h`.

Libraries, footprints and 3D models live in [`../lib`](../lib), shared by every board (see `fp-lib-table`, `sym-lib-table`); 3D model paths are `${KIPRJMOD}/../lib/...`, so they resolve from any board folder.

Footprints come from JLC (EasyEDA, imported with `easyeda2kicad`) or the KiCad standard libraries. Since 2026-11-04 no part uses the Altium-imported footprints: the LEDs (YLED0603B), Q16/Q20 (AO3401/AO3400), D26-D28 (SOD-123; their symbol now numbers the cathode pin 1, as the JLC footprint does), BUMP-L1/R1 (ITR9606-F), U13 (LQFP-100) and U21/U22 (SO-8 PowerPAD; add thermal vias in the layout) use JLC footprints. USBC2 (USB2 until 2026-11-08) is a Korean Hroparts TYPE-C-31-M-12 (C165948, 20 V 5 A; the GCT USB4215 had 2 in stock) on its JLC symbol and footprint. MAIN_FAN1 (Lian Xin XDWF-C3030WR-1*4P, C50399536) uses JLC's Molex 43650-0400 footprint: JLC's own XDWF footprint numbers the pins mirrored, against the datasheet; the Molex part (C277684) is the drop-in alternative.

easyeda2kicad writes absolute 3D paths: change them to `${KIPRJMOD}/../lib/JLCImport.3dshapes/...` after an import. The LCSC number lives in one field, `LCSC`, on every symbol and in `JLCImport` (since 2026-11-08). easyeda2kicad writes `LCSC Part`: rename it to `LCSC` after an import. `tools/export.py` still falls back to `LCSC Part` and warns if a part has both with different numbers.

The PCB file is still the `main` layout: run *Update PCB from Schematic* before layout work.
