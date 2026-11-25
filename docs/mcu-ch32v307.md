# main-phone MCU: CH32V307 + CH32L103

Status: in the schematic since 2026-11-21 (sheet `MCU`, file `kicad/main-phone/MCU.kicad_sch`, was `STM32G473.kicad_sch`). Not yet bench-tested; dev boards are on order. U28 was a CH32X035C8T6 until 2026-11-23, then a CH32L103C8T6 (see below).

## Why

- The STM32G473VCT6 (C730121) went to $7.39 at JLC and LCSC, with 20 in stock.
- A WCH CH32V307VCT6 (C2943979, LQFP-100, $2.18, 5k+ in stock) plus a CH32L103C8T6 (C22398291, LQFP-48, $0.41, 1.2k in stock) costs $2.59. Both are leaded packages.
- U28 was first a CH32X035C8T6 (C29779902, $0.38). It was dropped on 2026-11-23: on lots whose 5th-from-last batch digit is 0, its I2C and ADC channels 3, 7, 11 and 15 don't work, and the dead channels return a neighbour's reading instead of failing (datasheet notes; [community errata](https://github.com/ch32-riscv-ug/CH32X035)). It also has no plain open-drain GPIO output. The CH32L103 has the same PD PHY without those limits.
- The CH32V307 also has a parallel camera port (DVP) and high-speed USB with a built-in PHY, so the robot can stream a camera to the phone without a bridge chip or USB hub.
- The firmware isn't written yet, so there is nothing to port.

## Split of work

**U13, CH32V307VCT6, the main MCU:** motors, encoders, LiDAR, ToF/IMU (I2C2 and the bit-banged camera bus), cliff, bumper, motor-current and carpet ADCs, IR receivers, safety and rail enables, the camera (DVP, XCLK, SCCB), and USB to the phone.
- USB to the phone is high speed (480 Mbit/s) on PB6/PB7: a composite device with CDC (robot link) and UVC (camera). No USB hub.
- 144 MHz RISC-V with FPU; 256 KB flash / 64 KB RAM, or 192 KB / 128 KB through the option bytes.

**U28, CH32L103C8T6, the power/UI companion:** USB-C (see USB-C and PD: baseline and bonus), the slow analog inputs, charger status, buttons and button LEDs, the power latch, phone-charging enable, the camera reset, the dust-bin Hall, the side ToF enable, the torch PWM, and optionally the left ToF's I2C (see I2C buses).
- It talks to U13 over USART2 (PA2/PA3) at 1 Mbit/s suggested. USART2 is also its bootloader port, so U13 can program it (see Flashing).
- U13 drives its reset (MCU2-NRST) and its BOOT0 (MCU2-BOOT).

**Memory:** flash need is ~75–135 KB, since the phone uploads the ToF sensor firmware at boot, plus 8–16 KB for an update loader. RAM need is ~20–40 KB plus camera line buffers. Both fit.

## U13 CH32V307VCT6 pin map

All 80 GPIO are used. Pins marked FT are 5 V tolerant; the ADC-capable pins (PA0-PA7, PB0, PB1, PC0-PC5) are **not**. Net names are the schematic's (some keep their STM32-era names).

| Pin | Function | Net | Notes |
|---|---|---|---|
| PA0 | ADC_IN0 | WHEEL-MOT-L-ADC | left wheel current, through R258/C204 (10k, 100 nF, 1 ms) since 2026-11-24: the ADC reads the average (I x duty) |
| PA1 | ADC_IN1 | ECHO-ENV | carpet echo envelope (detector output) |
| PA2 | ADC_IN2 | BUMP-L | analog: firmware sees how fast the flag moves |
| PA3 | ADC_IN3 | BUMP-R | |
| PA4 | DVP_HSYNC | CAM-HREF | |
| PA5 | DVP_VSYNC | CAM-VSYNC | |
| PA6 | DVP_PCLK | CAM-PCLK | |
| PA7 | ADC_IN7 | WHEEL-MOT-R-ADC | R259/C205 filter |
| PA8 | MCO | CAM-MCO | camera XCLK through R248 (100 Ω); PLL2 or PLL3 set for 24 MHz, or the 8 MHz HSE |
| PA9 | DVP_D0 | CAM-Y2 | |
| PA10 | DVP_D1 | CAM-Y3 | |
| PA11 | EXTI11 | WHEEL-MOT-L-ENCODE | FT |
| PA12 | EXTI12 | WHEEL-MOT-R-ENCODE | FT |
| PA13 | SWDIO | MCU-SWDIO | 2-wire debug (WCH-LinkE), J4 pin 7 |
| PA14 | SWCLK | MCU-SWCLK | J4 pin 8 |
| PA15 | GPIO | SPARE-PA15 | spare, J13 pin 1 (not fitted; was on JTAG1 until 2026-11-23) |
| PB0 | ADC_IN8 | MAIN-BRUSH-ADC | R260/C206 filter |
| PB1 | ADC_IN9 | SIDE-BRUSH-ADC | R261/C207 filter |
| PB2 | OPA3_CH0N | ECHO-FB | also BOOT1: R241 (1M) keeps it low |
| PB3 | DVP_D5 | CAM-Y7 | DVP_D5 moves from PB6 to PB3 when USBHS is enabled (datasheet note 8; recent lots) |
| PB4 | TIM3_CH1 (remap 2) | MAIN-FAN-FB | tach input capture, FT |
| PB5 | GPIO out | WDI | RC watchdog toggle |
| PB6 | USBHS_DM | DN | to USB-C via USBLC6 (D1); 90 Ω pair |
| PB7 | USBHS_DP | DP | |
| PB8 | DVP_D6 | CAM-Y8 | |
| PB9 | DVP_D7 | CAM-Y9 | |
| PB10 | I2C2_SCL | IMU-SCL | right VL53L7, side VL53L0X, IMU; 400 kHz max (no Fast-mode Plus) |
| PB11 | I2C2_SDA | IMU-SDA | |
| PB12 | GPIO out | ~VMOT-14V4-EN | R184 pull-up |
| PB13 | OPA3_CH0P | CARPET-SENSOR-ECHO | the biased, clamped echo node on the carpet sheet |
| PB14 | GPIO out | VSENS-5V-USB-EN | |
| PB15 | GPIO out | ~VSENS_3V3_EN | |
| PC0–PC5 | ADC_IN10–15 | CLIFF-LF, CLIFF-RF, CLIFF-LM, CLIFF-RM, CLIFF-LR, CLIFF-RR | |
| PC6 | TIM8_CH1 | CARPET-SENSOR-LO | carpet burst |
| PC7 | EXTI7 | REAR-IR-L | |
| PC8 | DVP_D2 | CAM-Y4 | |
| PC9 | DVP_D3 | CAM-Y5 | |
| PC10 | GPIO out | CAM-PWDN | R245 (10k) keeps the camera on by default |
| PC11 | DVP_D4 | CAM-Y6 | |
| PC12 | UART5_TX | LIDAR_RX | |
| PC13 | GPIO out (open drain) | MCU2-NRST | U28 reset |
| PC14 | GPIO (bit-banged I2C) | CAM-SCL | camera SCCB + left VL53L7, 400 kHz; low-drive pin (open drain, only sinks ~1.5 mA); R246 pull-up. Shared with U28 PB10 |
| PC15 | GPIO (bit-banged I2C) | CAM-SDA | R247 pull-up. Shared with U28 PB11 |
| PD0 | GPIO out | CLIFF_LED_EN | pulsed cliff LEDs, ~1.9 A total while on; AC-coupled gate, keep pulses under ~1 ms (since 2026-11-24) |
| PD1, PD3 | TIM10_CH1/CH2 (remap 2) | WHEEL-MOT-L-IN1, -IN2 | PWM |
| PD5, PD7 | TIM10_CH3/CH4 | WHEEL-MOT-R-IN1, -IN2 | PWM |
| PD2 | UART5_RX | LIDAR_TX | |
| PD4 | GPIO out | MCU2-BOOT | U28 BOOT0; R235 (100k) pull-down |
| PD6 | GPIO in | ~INT-SENSORS | polled |
| PD8 | EXTI8 | REAR-IR-R | |
| PD9 | TIM9_CH1 (remap 2) | MAIN-FAN-PWM | |
| PD10 | GPIO in | HALL-TOWER | polled; internal pull-up |
| PD11 | TIM9_CH2 (remap 2) | LIDAR-MOTOR-CTRL | PWM |
| PD12–PD15 | TIM4_CH1–CH4 (remap) | MAIN-BRUSH-IN1/IN2, SIDE-BRUSH-IN1/IN2 | PWM |
| PE0 | UART4_TX (remap 2) | SPARE-TX | J1 pin 5 |
| PE1 | UART4_RX (remap 2) | SPARE-RX | J1 pin 6 |
| PE2 | GPIO | SPARE-PE2 | J1 pin 3, dock SWIO |
| PE3 | EXTI3 | IMU-INT1 | |
| PE4 | EXTI4 | UART3_RX1 | front IR receiver (net keeps its old name) |
| PE5 | EXTI5 | UART3_RX2 | front IR receiver |
| PE6 | EXTI6 | USART2-IR-R-RX | side IR receiver |
| PE7 | OPA3_OUT1 | ECHO-AMP | carpet amplifier output |
| PE8 | GPIO in | WHEEL-MOT-R-DROP | polled |
| PE9 | TIM1_CH1 (remap 3) | BUMP_L_LED_EN | 100–250 kHz PWM; TIM1_CC3/CC4 (no pin output) trigger the ADC |
| PE10 | GPIO in | WHEEL-MOT-L-DROP | polled |
| PE11 | TIM1_CH2 (remap 3) | BUMP_R_LED_EN | |
| PE12 | UART7_TX (remap) | MCU-TX | debug console (J4) |
| PE13 | UART7_RX (remap) | MCU-RX | |
| PE14 | UART8_TX (remap) | MCU2-RX | to U28 PA3 (USART2 RX) |
| PE15 | UART8_RX (remap) | MCU2-TX | from U28 PA2 (USART2 TX) |
| BOOT0 | pin 94 | BOOT0 | J1 pin 2, R22 pull-down |
| OSC_IN/OUT | pins 12/13 | | X3, 8 MHz, with C42/C39 (18 pF) |
| NRST | pin 14 | ~RST | R21, C37 |
| VBAT | pin 6 | VMCU-3V3 | C36 100 nF. Backup domain unused (no 32 kHz crystal: PC14/PC15 are the CAM I2C; settings and time live on the phone), so VBAT is tied to VDD |
| VDD x3, VIO x2, VDDA, VREF+ | | VMCU-3V3 | VDDA must equal VIO |
| VSS x5, VSSA, VREF- | | GND | pin 73 is NC |

**Interrupt lines:** 16 EXTI lines, each line number from one port only. The edge-timed inputs use lines 3–8, 11 and 12, one each: IR x5, encoders x2, IMU INT1. Hall, wheel-drop and ~INT-SENSORS inputs are polled.

**Timer remaps:** some remaps also route a timer's unused channels, ETR or break input onto pins used for something else, e.g. TIM10 BKIN onto PE2 and TIM9 CH3/CH4 onto PD13/PD15. Firmware must leave those outputs, the break inputs and ETR disabled.

## U28 CH32L103C8T6 pin map (LQFP-48)

37 GPIO; 33 used (5 of them spares on J1), plus the dedicated NRST and BOOT0. 3.3 V part (1.8–3.6 V). The ADC inputs are channels 0–9 (PA0–PA7, PB0, PB1); pins marked FT in the datasheet are 5 V tolerant, the ADC pins are not. USART2's pins (PA2/PA3) are ADC channels too, so with the link there, 8 ADC channels are left. The board NTC (T1/R38) was dropped for that (2026-11-23): board temperature comes from the U28 and U13 internal sensors, and USB_VBUS_SENSE stays analog on PA7 (R188/R189 100k/47k, ~1.6 V at 5 V) to help diagnose the phone link and dock-mode phone charging.

| Pin | Port | Function | Net | Notes |
|---|---|---|---|---|
| 10 | PA0 | ADC_IN0 | HALL-FLOOR-L | ≥200 Hz sampling |
| 11 | PA1 | ADC_IN1 | HALL-FLOOR-R | |
| 12 | PA2 | USART2_TX | MCU2-TX | to U13 PE15; bootloader port |
| 13 | PA3 | USART2_RX | MCU2-RX | from U13 PE14 |
| 14 | PA4 | ADC_IN4 | BAT_SENSE | |
| 15 | PA5 | ADC_IN5 | DC_IN_SENSE | ≥1 kHz, catches the dock's signature probe |
| 16 | PA6 | ADC_IN6 | BAT_NTC | battery pulled while docked: the pin sees ~4.5 V through R233 (10k), ~0.1 mA into the clamp diode; check the injection limit on the dev board |
| 17 | PA7 | ADC_IN7 | USB_VBUS_SENSE | 100k/47k divider; whether the phone supplies VBUS, and the robot 5 V sag while charging it |
| 18 | PB0 | ADC_IN8 | BAT_ID | R254 (1M) to VMCU-3V3 + C203 (100 nF) since 2026-11-24: ~1.25 V with the pack's 620k ID resistor, ~3.3 V without |
| 19 | PB1 | ADC_IN9 | LDR | wake-up sensor |
| 29 | PA8 | TIM1_CH1 | LED-HOME | PWM possible |
| 30 | PA9 | TIM1_CH2 | LED-PWR | PWM possible |
| 31 | PA10 | GPIO in | ~CLEAN-BTN | internal pull-up |
| 32 | PA11 | GPIO in | ~HOME-BTN | internal pull-up (USB D- unused) |
| 33 | PA12 | GPIO in | PWR-BTN-SENSE | (USB D+ unused) |
| 38 | PA15 | GPIO in | HALL-BIN | internal pull-up |
| 20 | PB2 | BOOT1 | BOOT1 | R249 (100k) pull-down: BOOT0 = 1 with BOOT1 = 0 starts the bootloader |
| 21 | PB10 | I2C2_SCL | CAM-SCL | left VL53L7 + camera bus, in parallel with U13 PC14; input (hi-Z) when unused |
| 22 | PB11 | I2C2_SDA | CAM-SDA | in parallel with U13 PC15 |
| 26 | PB13 | GPIO out | PWR-HOLD | power latch; R172 holds the latch while U28 boots |
| 27 | PB14 | GPIO out | SIDE-PROXI-CE-R | VL53L0X XSHUT |
| 28 | PB15 | GPIO out | USB_PWR_EN | phone charging switch (TMI6240 + Q27) |
| 2 | PC13 | GPIO out | CHG-I-HI | high = ~2.2 A charging (Q45 -> Q44 puts R250 in parallel with R106); gate drive only, R252 (1M) pull-down (since 2026-11-24) |
| 39 | PB3 | GPIO in | ~STDBY | internal pull-up |
| 40 | PB4 | GPIO in | ~CHRG | internal pull-up |
| 41 | PB5 | GPIO out | CC-RD-EN | Rd switch, see below |
| 42 | PB6 | USB PD CC1 | USB_CC1 | |
| 43 | PB7 | USB PD CC2 | USB_CC2 | |
| 45 | PB8 | TIM4_CH3 | TORCH | PWM to both front boards' torch LEDs: gate of Q46 (AO3400, R257 100k pull-down), which switches both cathodes (TORCH-K) |
| 25 | PB12 | GPIO | MCU2-PB12 | spare, J1 pin 7 (5 V tolerant) |
| 5 | PD0 | GPIO | MCU2-PD0 | spare, J1 pin 8 (OSC_IN after reset: remap to PD0 in firmware). With PD1: USART3 remap 3 (TX PD0, RX PD1) for a U28 debug console |
| 6 | PD1 | GPIO | MCU2-PD1 | spare, J1 pin 9 (OSC_OUT after reset) |
| 34 | PA13 | SWDIO | MCU2-SWDIO | J1 pin 10: WCH-LinkE debug, or a spare GPIO once SDI is disabled |
| 37 | PA14 | SWCLK | MCU2-SWCLK | J1 pin 11 |
| 46 | PB9 | GPIO out | CAM-RESET | camera RESETB; R244 (10k) pull-down holds the camera in reset until U28 releases it |
| 7 | NRST | reset | MCU2-NRST | from U13 PC13 (open drain); U28's internal 30-50k pull-up and 100 ns filter, no external parts (R234/C185 removed 2026-11-23) |
| 44 | BOOT0 | boot | MCU2-BOOT | from U13 PD4; R235 (100k) pull-down |
| 1, 9, 24, 36, 48 | VBAT, VDDA, VDD x3 | | VMCU-3V3 | C183 100 nF + C184 10 µF, C196/C197 (pins 24/36), C198 (VDDA) |
| 8, 23, 35, 47 | VSSA, VSS x3 | | GND | |

PC14, PC15 (MCU2-PC14/15, U28 pins 3/4): spare, J13 pins 2/3 (weak, 2 MHz, can't source current). No free pins left on U13 or U28: every spare is on J1 or J13.

## I2C buses (since 2026-11-23)

Two buses, so both VL53L7s keep the default address and the front boards need no LPn or I2C_RST lines:

| Bus | Pins | Devices | Pull-ups |
|---|---|---|---|
| Main (IMU-SCL/IMU-SDA) | U13 I2C2, PB10/PB11 | right VL53L7 (J5), side VL53L0X, IMU | R5/R6 2.2k |
| Camera (CAM-SCL/CAM-SDA) | U13 PC14/PC15 bit-banged; U28 I2C2 (PB10/PB11) | left VL53L7 (J6), camera SCCB (J12) | R246/R247 2.2k |

- **Addresses:** the VL53L7s and the VL53L0X all start at 0x52 (0x29 7-bit). On the main bus, firmware holds the VL53L0X off with its XSHUT (SIDE-PROXI-CE-R, U28 PB14), moves the right VL53L7 to another address, then releases XSHUT, every boot. The camera is at 0x30 or 0x3C, so the camera bus has no clash.
- **Speed:** 400 kHz on both. Neither MCU does Fast-mode Plus. A VL53L7 firmware upload (~84 KB) takes ~2–3 s per sensor; the two buses can upload in parallel.
- **Camera bus, two masters on the same wires:** U13 has no free hardware I2C (I2C1's pins are taken by USB high speed and DVP), so its PC14/PC15 bit-bang. U28's I2C2 is wired in parallel on PB10/PB11. Only one drives at a time; the other keeps its pins as inputs.
  - **Bit-banged (always works):** U13 runs the bus itself. Trimmed ToF outputs cost a few % of CPU; full-size debug frames at 15 Hz keep the bus ~40 % busy, so use a lower rate or a timer-paced bit-bang for long debug runs.
  - **U28 hardware I2C (optional, offloads U13):** U28 acts as a UART-to-I2C bridge: U13 sends register reads and writes over the link and U28 runs them with DMA. The ~84 KB sensor firmware doesn't fit in U28's 64 KB flash, so U13 streams it through the bridge. Bit-banging stays the fallback.
- **Rise time:** 2.2k with the flex and two devices (~50–100 pF) gives ~100–200 ns, under the 300 ns allowed at 400 kHz.

## USB-C and PD: baseline and bonus

**Baseline (works with any phone, no PD messages): Type-C resistors only.**
- **Docked, charging, no data:** U28 puts Rp on CC (its PD block's pull-up) and turns USB_PWR_EN on, so the robot's 5 V reaches VBUS. The phone sees a charger and charges at 5 V (it takes 1.5 A or 3 A only if Rp advertises it).
- **Cleaning, data, the phone powers the link:** USB_PWR_EN off, Rp off, Rd on (CC-RD-EN high). The phone sees a device, turns VBUS on and becomes USB host; U13 enumerates on the high-speed port. The VBUS lockout (Q33/Q34) keeps the robot from driving VBUS while the phone does.
- Switching between the two is a detach and re-attach, which every Android phone handles. Firmware decides when to switch (wake-up and end-of-cleaning signals).

**Bonus (phones that support it): USB PD power-role swap.** The CH32L103's PD block does BMC, CRC and GoodCRC in hardware, so U28 can negotiate a power-role swap: the phone stays USB host while the robot supplies VBUS, so it charges and talks at the same time. Many phones, older ones in particular, don't support the swap, so nothing may depend on it.

**Rd:**
- The LQFP-48 CH32L103 has **no built-in Rd** (only its QFN versions do), so the switched Rd stays: R236/R237 (4.7k; Type-C allows 5.1k ±10 %) go from CC1/CC2 to GND through Q42/Q43 (AO3400). Both gates are on CC-RD-EN, with R238 (100k) pulling up to VMCU-3V3.
- Rd is there whenever VMCU-3V3 is up (dead-battery behaviour). Firmware pulls CC-RD-EN low only while sourcing, with Rp on.
- R221 (the old 100k pull-up on BUMP_R_LED_EN for the STM32's UCPD dead-battery pin) was removed on 2026-11-23. Q36's gate floats while U13 is in reset, but the LED runs from VSENS-5V-USB, which is off whenever the MCU pins are tristated (boot, programming); firmware configures all GPIOs before turning the sensor rails on.

## Camera (DVP) connector

**J12:** 24-pin 0.5 mm FPC socket (HanElectricity 05A20L24P, C5362158, $0.04, flip lid, bottom contact), near the front edge on the top side. It takes the 24-pin OV2640 / OV3660 / OV5640 / GC2145 modules sold for ESP32-CAM boards; the pinout follows the AI-Thinker ESP32-CAM.

| J12 pin | Signal | | J12 pin | Signal |
|---|---|---|---|---|
| 1 | NC | | 13 | XCLK (PA8 through R248) |
| 2 | AGND | | 14 | Y8 (D6, PB8) |
| 3 | SIO_D (PC15) | | 15 | DGND |
| 4 | AVDD 2.8 V | | 16 | Y7 (D5, PB3) |
| 5 | SIO_C (PC14) | | 17 | PCLK (PA6) |
| 6 | RESETB (U28 PB9, R244 to GND) | | 18 | Y6 (D4, PC11) |
| 7 | VSYNC (PA5) | | 19 | Y2 (D0, PA9) |
| 8 | PWDN (PC10, R245 to GND) | | 20 | Y5 (D3, PC9) |
| 9 | HREF (PA4) | | 21 | Y3 (D1, PA10) |
| 10 | DVDD 1.2 V | | 22 | Y4 (D2, PC8) |
| 11 | DOVDD (VSENS-3V3) | | 23 | Y1 (NC, 8-bit mode) |
| 12 | Y9 (D7, PB9) | | 24 | Y0 (NC) |

**Camera power:**
- **DOVDD** is VSENS-3V3, so the camera I/O runs at 3.3 V like the MCU and the camera is on whenever the other sensors are. No separate switch (Q44 removed 2026-11-22): PWDN (U13 PC10) is the standby, CAM-RESET (U28 PB9) the hard reset.
- **AVDD 2.8 V:** U29 (VCAM-2V8), ME6211C28M5G-N (C53099), from VSENS-3V3.
- **DVDD 1.2 V:** U30 (VCAM-1V2), ME6211C12M5G-N (C236672), from VSENS-3V3, for OV2640-class sensors. OV3660 and OV5640 regulate their own core.
- 1 µF in and out on each LDO (C188–C191), 100 nF at J12 pins 4, 10 and 11 (C192–C194).
- Bus pull-ups R246/R247 (2.2k since 2026-11-23, for the VL53L7 on the same bus) go to VSENS-3V3.
- **Reset sequence:** with VSENS-3V3 up, wait for the LDOs to settle, start XCLK, then release CAM-RESET (U13 asks U28 over the link).
- **Firmware:** keep XCLK, SCCB, PWDN and CAM-RESET low or hi-Z while VSENS-3V3 is off.
- **Budget:** ~40–150 mA from VSENS-3V3 depending on the sensor; check the U21 headroom.

## Carpet echo

- OPA3 as a non-inverting AC amplifier: input PB13 (the existing biased, clamped echo node), output PE7 (OPA3_OUT1), feedback R239 (47k) to PB2, and R240 (4.7k) + C186 (100 nF) from PB2 to GND. Gain is 11 at 290 kHz and 1 at DC, so the output sits at the echo bias. Set the gain on the bench.
- Envelope detector: D48 (1N4148) from PE7 into C187 (1.2 nF) and R242 (47k) on PA1, about 56 µs. The ADC then needs only ~20–50 kSPS. Measure the idle level with the burst off and subtract it.
- R241 (1M) on PB2 keeps BOOT1 low; it shifts the DC bias by ~5 %.

## Other circuit changes

- **Clock:** X3 is now an 8 MHz HC-49S crystal (YXC X49SM8MSD2SC, C12674) on OSC_IN/OUT, needed for high-speed USB, with the existing 18 pF caps. The load is a little under the crystal's 20 pF: a few tens of ppm, well inside USB's ±500 ppm.
- **Removed:** the 32.768 kHz crystal (the phone keeps the time; the RTC, if wanted, runs from LSI) and the STM32's UCPD dead-battery arrangement.
- **Kept:** ~INT-SENSORS goes to U13 PD6 (polled), so R2 stays.

## Flashing

- **U13 (CH32V307):** the built-in bootloader does USB ISP on the high-speed port. Short J1 1-2 (BOOT0) at power-up and flash from a PC over USB-C with WCH's tool or wchisp. A WCH-LinkE on J4 (7 SWDIO, 8 SWCLK, 9 NRST, 1 GND) is only needed for debugging. Phone updates: firmware jumps to the bootloader.
- **U28 (CH32L103):** its built-in bootloader loads over USART2 (or USB), and USART2 is the link to U13. U13 holds MCU2-BOOT (BOOT0) high, pulses MCU2-NRST, and sends the image with WCH's serial ISP protocol (the one WCH's ISP tool uses over a UART); R249 keeps BOOT1 low. Then BOOT0 low and another reset. No probe needed, so the phone can update U28 through U13. A WCH-LinkE on PA13/PA14 is only for debugging on the dev board.

## BOM delta (JLC, 1k pcs)

| Change | $ |
|---|---|
| − STM32G473VCT6 | −7.39 |
| + CH32V307VCT6 | +2.18 |
| + CH32L103C8T6 | +0.41 |
| + 8 MHz crystal, − 32.768 kHz crystal | ≈ −0.05 |
| + Rd switch (2x AO3400, 2x 4.7k, 100k) | +0.02 |
| + carpet amplifier and detector (passives, 1N4148) | +0.01 |
| + J12, 2x ME6211, passives | +0.14 |
| − R196 (47k), the right LPn pull-up (the front boards now carry their own) | ≈ 0 |
| + R249 (100k), C196–C198 (100 nF) for the CH32L103; − board NTC T1 and R38 | ≈ 0 |
| **Net** | **≈ −4.7 per board** |

New BOM lines: CH32V307, CH32L103, the 8 MHz crystal, the FPC socket and two ME6211s. Removed: STM32G473 and the 32.768 kHz crystal. JLC had 1,194 CH32L103C8T6 on 2026-11-23; check stock before a 500–1000-piece run.

## Bench tests (dev boards)

1. USB ISP over the high-speed port with BOOT0, and a jump to the bootloader from firmware.
2. Composite CDC + UVC at high speed to the phone: GC2145 YUV at VGA (~9–18 MB/s) and OV2640 JPEG.
3. DVP at the sensor's PCLK, with DVP_D5 on PB3 and USBHS enabled (check the lot code rule).
4. The carpet amplifier and envelope detector at 290 kHz.
5. U28 baseline: Rp + robot 5 V charges the phone; then Rd only, and the phone enumerates U13 as host. Then the bonus: a PD power-role swap with phones that support it.
6. U13 flashing U28 through its USART2 bootloader (BOOT0, NRST).
7. Bit-banged I2C at 400 kHz on PC14/PC15 with the VL53L7 firmware upload; and the U28 I2C2 bridge.

## Open items

- The camera module's pinout and contact side, and the flex length (in the 3D CAD model).
- PCB layout: re-route U13 for the new pin map, place U28, J12 and the camera supplies.
