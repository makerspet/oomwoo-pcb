# OOMWOO charging dock (charging only)

The dock the v1 robot ([`../main-phone`](../main-phone/README.md)) charges from. It has two pogo contacts (DOCK+ and DOCK-), an IR beacon so the robot can find it, and a small MCU. Rev 2, 2026-10-27: a full redesign of the first draft. The first draft had a 555 beacon, a third "detector" contact and a 24 V input, and its 5 V buck had no input connection.

Sheets: **POWER** (input, 3.3 V, output switch, current sense, robot probe), **IR BEACON**, **CONTROL** (MCU, status LED, debug pads, optional IR receiver).

## What it does

1. A 20 V brick plugs into J1001 (DC-044A-20A, the same jack as the robot). F1001 (5 A fuse), D1001 (SMAJ22A) and C1001 protect the input. U1001 (HT7533-1) makes 3.3 V for the MCU.
2. With the contacts off, the MCU measures the resistance across them (see [Robot detection](#robot-detection)). It switches 20 V on only when it sees the robot.
3. Q1001 (AO4407C P-FET) switches DOCK+. R1004/R1005 set Vgs to -10 V, and C1008 (47 nF, gate to drain) ramps DOCK+ at ~30 V/ms, so the robot's input capacitors charge at ~0.5 A instead of sparking on the pogo pins. D1002 (SMAJ22A) protects the exposed contacts.
4. R1007 (50 mΩ) and U1002 (INA180A1, gain 20) measure the charging current on DOCK-: I_SENSE = 1 V/A, 3.3 A full scale. The MCU switches DOCK+ off when the current drops to ~0 (the robot left) or on overcurrent.
5. Two IR LED strings (3x TSAL6200 each, ~100 mA peak from 20 V) send 38 kHz NEC frames for the robot's receivers.

## MCU: CH32V003F4P6

- WCH CH32V003F4P6, TSSOP-20 (LCSC C5187096, ~$0.17): 48 MHz RISC-V, 16 KB flash, 10-bit ADC, internal oscillator (no crystal).
- Toolchains: WCH's official Arduino core, [ch32fun](https://github.com/cnlohr/ch32fun) and PlatformIO.
- Programming and debug: a WCH-LinkE on the single-wire SWIO pin (PD1). J1201 (1x5, not fitted) pinout: 1 3V3, 2 SWIO, 3 TX, 4 RX, 5 GND.

| Pin | Function | Notes |
| --- | --- | --- |
| PA2 (A0) | VIN_SENSE | brick voltage x 11 (R1001/R1002) |
| PA1 (A1) | DOCK_SENSE | DOCK+ x 11 (R1009/R1010) |
| PD2 (A3) | PROBE_A | probe node, before the diode |
| PD3 (A4) | I_SENSE | 1 V/A |
| PC2 | PROBE_DRV | push-pull, high = probe on |
| PC1 | CHG_EN | high = DOCK+ on (R1006 100k pull-down holds it off in reset) |
| PC3, PC4 | IR_L, IR_R | TIM1_CH3 / TIM1_CH4, 38 kHz PWM |
| PC0 | status LED | D1201 through R1201 (1k) |
| PD4 | IR_RX | TIM2_CH1 capture, optional receiver U1202 |
| PD5, PD6 | UART TX, RX | debug |
| PD1 | SWIO | programming |

The ADC reference is VDD, and PROBE_DRV high is VDD too, so the probe readings are ratiometric.

## Robot detection

The v1 robot presents ~130 kΩ across its dock contacts: R175 + R194 (147k, the charger rail-hold divider) in parallel with its 1.1 MΩ DC_IN sense divider. It also has ~30 µF of input capacitance.

The probe: PROBE_DRV → R1008 (100k) → PROBE_A → D1003 (1N4148W) → DOCK+. The diode keeps the 20 V on DOCK+ away from the MCU. With Q1001 off and PROBE_DRV high:

- I_probe = (V_DD - V_PROBE_A) / 100k
- R_contacts = V_DOCK+ / (I_probe - V_DOCK+ / 1.1M), where 1.1M is the dock's own DOCK_SENSE divider

Both sides of the diode are measured, so its drop cancels. Expected readings on DOCK+: ~2.6 V with nothing docked, ~1.5 V with the robot, 0 V for a short. With the robot, DOCK+ stays near 1.5 V, so the robot's rail-hold FET (Q31) gate sees only ~0.5 V and stays off.

Firmware:
- check VIN first: refuse to switch on above ~22 V (an old 24 V brick would exceed the robot's limit) or below ~18.5 V (the robot can't finish a 4S charge)
- probe for a few seconds: the robot's input capacitance makes the reading settle with τ ≈ 1.6 s. Require a stable value inside a window around 130 kΩ (start with 90-180 kΩ and tune it on real robots, including one with a flat battery). The settling time itself is a second check that something capacitive, i.e. a robot, is connected.
- then PROBE_DRV low and CHG_EN high, and check DOCK_SENSE ≈ VIN within ~10 ms
- while on: switch off if I_SENSE drops below ~5 mA for ~100 ms (the robot keeps its MCU on while charging, so it never draws zero), or above ~3.2 A (use the ADC analog watchdog for a fast trip). Read the INA180 zero with DOCK+ off; its offset is up to ~3 mA.
- after switching off, wait for DOCK+ to bleed down before probing again

## IR beacon

- The robot's receivers (IRM-V838M3-C, AGC type) suppress a steady 38 kHz carrier, so the beacon must send bursts: NEC frames, with the TIM1 PWM at ~1/3 duty and the frame envelope gated in firmware.
- IR_L and IR_R drive two strings, so each side of the dock can send its own code.
- The gates are AC-coupled (C1101/C1102 100 nF, R1102/R1104 100k, ~10 ms), like the robot's carpet driver. A pin stuck high turns the LEDs off within ~30 ms instead of leaving 100 mA flowing.
- R1101/R1103 are 150 Ω 2512 (1 W): 1.7 W peak, ~0.3 W average at NEC duty.
- U1202 (IRM-H638T, not fitted) is there for optional robot → dock messages later. Its symbol pinout (1, 2 GND, 3 OUT, 4 VCC) matches Everlight's IRM-H6XX/TR2 datasheet (DMO-0000004); the robot's side board uses the same part.

## PCB notes (for layout)

- Mount the three TSAL6200 of each string fanned out horizontally (they are ±17°), left string and right string to each side, overlapping in the middle.
- Route the INA180 inputs (IN+ on DOCK-, IN- on GND) as a Kelvin pair to R1007's pads.
- J1002/J1003: YZP0670-20143-01 pogo pins (4 A), rear-vertical, above the water line. DOCK+ / DOCK- traces sized for 4 A.
- H1201-H1204: four M3 holes (`MountingHole_3.2mm_M3_Pad`, pads to GND, not in the BOM), on the CONTROL sheet.
- Reference designators are in the dock's 1000s range (POWER 10xx, IR BEACON 11xx, CONTROL 12xx); every board has its own reference range: main board 1-999, dock 1000s, front ToF 2000s, side sensor 3000s, cliff 4000s, rear IR 5000s, Hall 6000s.

## Parts shared with the robot

DC-044A-20A, SMAJ22A, AO4407C, AO3400, HT7533-1, 1N4148W, YLED0603B, PZ254R-11-05P, and the robot's 0603 resistor (1M, 100k, 10k, 1k, 120, 100) and capacitor lines (100nF/50V C1591, 10uF/10V C19702, 10uF/50V 1206 C13585, 47nF/50V C1622). New lines for the dock: CH32V003F4P6, INA180A1, TSAL6200, YZP0670 pogo pin, 220 µF/50 V electrolytic, 50 mΩ 2512 shunt, 150 Ω 2512, 5 A fuse (JFC1206-1500FS, the same family as the robot's F1).

Symbols and footprints come from the shared libraries in [`../main`](../main) (`JLCImport`) and the KiCad standard libraries.

## Open items

- Measure the real robot signature (resistance and settling time) on the first boards, with a full battery and a flat one, and set the firmware window from that.
