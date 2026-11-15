# OOMWOO charging dock (charging only)

The dock the v1 robot ([`../main-phone`](../main-phone/README.md)) charges from. It has two pogo contacts (VDOCK-20V and DOCK-), an IR beacon so the robot can find it, and a small MCU. Rev 2, 2026-10-27: a full redesign of the first draft. The first draft had a 555 beacon, a third "detector" contact and a 24 V input, and its 5 V buck had no input connection.

Sheets: root (MCU, status LED, debug pads, optional IR receiver, mounting holes), **POWER** (input, 3.3 V, output switch, current sense, robot probe), **IR BEACON**.

## What it does

1. A 20 V brick plugs into J1002 (DC-044A-20A, the same jack as the robot). F1001 (5 A fuse), D1001 (SMAJ22A) and C1011 protect the input. U1003 (HT7533-1) makes 3.3 V for the MCU.
2. With the contacts off, the MCU measures the resistance across them (see [Robot detection](#robot-detection)). It switches 20 V on only when it sees the robot.
3. Q1003 (AO4407C P-FET) switches VDOCK-20V. R1012/R1015 set Vgs to -10 V, and C1017 (47 nF, gate to drain) ramps VDOCK-20V at ~30 V/ms, so the robot's input capacitors charge at ~0.5 A instead of sparking on the pogo pins. D1003 (SMAJ22A) protects the exposed contacts.
4. R1016 (50 mΩ) and U1004 (INA180A1 clone from lingxingic, C48533472, gain 20; TI's INA180A1IDBVR C122228 is the pin-compatible alternative) measure the charging current on DOCK-: I-SENSE = 1 V/A, 3.3 A full scale. The MCU switches VDOCK-20V off when the current drops to ~0 (the robot left) or on overcurrent.
5. Two IR LED strings (3x TSAL6200 each, ~100 mA peak from 20 V) send 38 kHz NEC frames for the robot's receivers.

## MCU: CH32V003F4P6

- WCH CH32V003F4P6, TSSOP-20 (LCSC C5187096, ~$0.17): 48 MHz RISC-V, 16 KB flash, 10-bit ADC, internal oscillator (no crystal).
- Toolchains: WCH's official Arduino core, [ch32fun](https://github.com/cnlohr/ch32fun) and PlatformIO.
- Programming and debug: a WCH-LinkE on the single-wire SWIO pin (PD1). J1001 (1x5, not fitted) pinout: 1 3V3, 2 SWIO, 3 TX, 4 RX, 5 GND.

| Pin | Function | Notes |
| --- | --- | --- |
| PA2 (A0) | VIN-SENSE | brick voltage x 11 (R1007/R1008) |
| PA1 (A1) | DOCK-SENSE | VDOCK-20V x 11 (R1010/R1011) |
| PD2 (A3) | PROBE-SENSE | probe node, before the diode |
| PD3 (A4) | I-SENSE | 1 V/A |
| PC2 | PROBE-DRV | push-pull, high = probe on |
| PC1 | CHARGE-EN | high = VDOCK-20V on (R1013 100k pull-down holds it off in reset) |
| PC3, PC4 | IR-L, IR-R | TIM1_CH3 / TIM1_CH4, 38 kHz PWM |
| PC0 | status LED | LED1001 through R1001 (1k) |
| PD4 | IR_RX | TIM2_CH1 capture, optional receiver U1002 |
| PD5, PD6 | UART TX, RX | debug |
| PD1 | SWIO | programming |

The ADC reference is VDD, and PROBE-DRV high is VDD too, so the probe readings are ratiometric.

## Robot detection

The v1 robot presents ~130 kΩ across its dock contacts: R175 + R194 (147k, the charger rail-hold divider) in parallel with its 1.1 MΩ DC-IN-20V sense divider. It also has ~30 µF of input capacitance.

The probe: PROBE-DRV → R1014 (100k) → PROBE-SENSE → D1002 (1N4148W) → VDOCK-20V. The diode keeps the 20 V on VDOCK-20V away from the MCU. With Q1003 off and PROBE-DRV high:

- I_probe = (V_DD - V(PROBE-SENSE)) / 100k
- R_contacts = V(VDOCK-20V) / (I_probe - V(VDOCK-20V) / 1.1M), where 1.1M is the dock's own DOCK-SENSE divider

Both sides of the diode are measured, so its drop cancels. Expected readings on VDOCK-20V: ~2.6 V with nothing docked, ~1.5 V with the robot, 0 V for a short. With the robot, VDOCK-20V stays near 1.5 V, so the robot's rail-hold FET (Q31) gate sees only ~0.5 V and stays off.

Firmware:
- check VIN first: refuse to switch on above ~22 V (an old 24 V brick would exceed the robot's limit) or below ~18.5 V (the robot can't finish a 4S charge)
- probe for a few seconds: the robot's input capacitance makes the reading settle with τ ≈ 1.6 s. Require a stable value inside a window around 130 kΩ (start with 90-180 kΩ and tune it on real robots, including one with a flat battery). The settling time itself is a second check that something capacitive, i.e. a robot, is connected.
- then PROBE-DRV low and CHARGE-EN high, and check DOCK-SENSE ≈ VIN-SENSE within ~10 ms
- while on: switch off if I-SENSE drops below ~5 mA for ~100 ms (the robot keeps its MCU on while charging, so it never draws zero), or above ~3.2 A (use the ADC analog watchdog for a fast trip). Read the INA180 zero with VDOCK-20V off; its offset is up to ~3 mA.
- after switching off, wait for VDOCK-20V to bleed down before probing again

## IR beacon

- The robot's receivers (IRM-V838M3-C, AGC type) suppress a steady 38 kHz carrier, so the beacon must send bursts: NEC frames, with the TIM1 PWM at ~1/3 duty and the frame envelope gated in firmware.
- IR-L and IR-R drive two strings, so each side of the dock can send its own code.
- The gates are AC-coupled (C1004/C1006 100 nF, R1003/R1005 100k, ~10 ms), like the robot's carpet driver. A pin stuck high turns the LEDs off within ~30 ms instead of leaving 100 mA flowing.
- R1004/R1006 are 150 Ω 2512 (1 W): 1.7 W peak, ~0.3 W average at NEC duty.
- U1002 (IRM-H638T, not fitted) is there for optional robot → dock messages later. Its symbol pinout (1, 2 GND, 3 OUT, 4 VCC) matches Everlight's IRM-H6XX/TR2 datasheet (DMO-0000004); the robot's side board uses the same part.

## PCB notes (for layout)

- Mount the three TSAL6200 of each string fanned out horizontally (they are ±17°), left string and right string to each side, overlapping in the middle.
- Route the INA180 inputs (IN+ on DOCK-, IN- on GND) as a Kelvin pair to R1016's pads.
- J1003/J1004: YZP0670-20143-01 pogo pins (4 A), rear-vertical, above the water line. VDOCK-20V / DOCK- traces sized for 4 A.
- H1001-H1004: four M3 holes (`MountingHole_3.2mm_M3_Pad`, pads to GND, not in the BOM), on the root sheet.
- Reference designators are in the dock's 1000s range (all sheets in 10xx since 2026-11-14; POWER 10xx, IR BEACON 11xx, CONTROL 12xx before); every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s.

## Parts shared with the robot

DC-044A-20A, SMAJ22A, AO4407C, AO3400, HT7533-1, 1N4148W, YLED0603B, PZ254R-11-05P, and the robot's 0603 resistor (1M, 100k, 10k, 1k, 120, 100) and capacitor lines (100nF/50V C1591, 10uF/10V C19702, 10uF/50V 1206 C13585, 47nF/50V C1622). New lines for the dock: CH32V003F4P6, INA180A1 (lingxingic clone, ~$0.09 vs ~$0.16 for TI's), TSAL6200, YZP0670 pogo pin, 220 µF/50 V electrolytic, 50 mΩ 2512 shunt, 150 Ω 2512, 5 A fuse (JFC1206-1500FS, the same family as the robot's F1).

Symbols and footprints come from the shared libraries in [`../lib`](../lib) (`JLCImport`) and the KiCad standard libraries.

## Open items

- Measure the real robot signature (resistance and settling time) on the first boards, with a full battery and a flat one, and set the firmware window from that.
