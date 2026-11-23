# main-phone MCU: CH32V307 + CH32X035

Status: in the schematic since 2026-11-21 (sheet `MCU`, file `kicad/main-phone/MCU.kicad_sch`, was `STM32G473.kicad_sch`). Not yet bench-tested; dev boards are on order.

## Why

- The STM32G473VCT6 (C730121) went to $7.39 at JLC and LCSC, with 20 in stock.
- A WCH CH32V307VCT6 (C2943979, LQFP-100, $2.18, 5k+ in stock) plus a CH32X035C8T6 (C29779902, LQFP-48, $0.38) costs $2.56. Both are leaded packages.
- The CH32V307 also has a parallel camera port (DVP) and high-speed USB with a built-in PHY, so the robot can stream a camera to the phone without a bridge chip or USB hub.
- The firmware isn't written yet, so there is nothing to port.

## Split of work

**U13, CH32V307VCT6, the main MCU:** motors, encoders, LiDAR, ToF/IMU (I2C2), cliff, bumper, motor-current and carpet ADCs, IR receivers, safety and rail enables, the camera (DVP, XCLK, SCCB), and USB to the phone.
- USB to the phone is high speed (480 Mbit/s) on PB6/PB7: a composite device with CDC (robot link) and UVC (camera). No USB hub.
- 144 MHz RISC-V with FPU; 256 KB flash / 64 KB RAM, or 192 KB / 128 KB through the option bytes.

**U28, CH32X035C8T6, the power/UI companion:** USB-C PD (sink by default, power-role swap to source to charge the phone), the slow analog inputs, charger status, buttons and button LEDs, the power latch, phone-charging enable, the camera reset, the dust-bin Hall, the ToF reset/enable lines, and later the torch.
- It talks to U13 over a UART at 1 Mbit/s suggested, on its PC18/PC19 (USART3 remap 1). Those are also its SDI programming pins, so U13 can program it (see Flashing).
- U13 drives its reset (X035-NRST) and its boot pin (X035-BOOT).

**Memory:** flash need is ~75–135 KB, since the phone uploads the ToF sensor firmware at boot, plus 8–16 KB for an update loader. RAM need is ~20–40 KB plus camera line buffers. Both fit.

## U13 CH32V307VCT6 pin map

All 80 GPIO are used. Pins marked FT are 5 V tolerant; the ADC-capable pins (PA0-PA7, PB0, PB1, PC0-PC5) are **not**. Net names are the schematic's (some keep their STM32-era names).

| Pin | Function | Net | Notes |
|---|---|---|---|
| PA0 | ADC_IN0 | WHEEL-MOT-L-ADC | left wheel current |
| PA1 | ADC_IN1 | ECHO-ENV | carpet echo envelope (detector output) |
| PA2 | ADC_IN2 | BUMP-L | analog: firmware sees how fast the flag moves |
| PA3 | ADC_IN3 | BUMP-R | |
| PA4 | DVP_HSYNC | CAM-HREF | |
| PA5 | DVP_VSYNC | CAM-VSYNC | |
| PA6 | DVP_PCLK | CAM-PCLK | |
| PA7 | ADC_IN7 | WHEEL-MOT-R-ADC | |
| PA8 | MCO | CAM-MCO | camera XCLK through R248 (100 Ω); PLL2 or PLL3 set for 24 MHz, or the 8 MHz HSE |
| PA9 | DVP_D0 | CAM-Y2 | |
| PA10 | DVP_D1 | CAM-Y3 | |
| PA11 | EXTI11 | WHEEL-MOT-L-ENCODE | FT |
| PA12 | EXTI12 | WHEEL-MOT-R-ENCODE | FT |
| PA13 | SWDIO | STM32-SWDIO | 2-wire debug (WCH-LinkE) on JTAG1 |
| PA14 | SWCLK | STM32-SWCLK | |
| PA15 | GPIO | STM32-SWO-SPARE | JTAG1 pin 8, spare |
| PB0 | ADC_IN8 | MAIN-BRUSH-ADC | |
| PB1 | ADC_IN9 | SIDE-BRUSH-ADC | |
| PB2 | OPA3_CH0N | ECHO-FB | also BOOT1: R241 (1M) keeps it low |
| PB3 | DVP_D5 | CAM-Y7 | DVP_D5 moves from PB6 to PB3 when USBHS is enabled (datasheet note 8; recent lots) |
| PB4 | TIM3_CH1 (remap 2) | MAIN-FAN-FB | tach input capture, FT |
| PB5 | GPIO out | WDI | RC watchdog toggle |
| PB6 | USBHS_DM | DN | to USB-C via USBLC6 (D1); 90 Ω pair |
| PB7 | USBHS_DP | DP | |
| PB8 | DVP_D6 | CAM-Y8 | |
| PB9 | DVP_D7 | CAM-Y9 | |
| PB10 | I2C2_SCL | SCL | ToF x2, side VL53L0X, IMU; 400 kHz max (no Fast-mode Plus) |
| PB11 | I2C2_SDA | SDA | |
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
| PC13 | GPIO out (open drain) | X035-NRST | |
| PC14 | GPIO (bit-banged SCCB) | CAM-SCL | low-drive pin, 100 kHz; R246 pull-up. Separate from the sensor bus: SCCB quirks, slower clock, long flex |
| PC15 | GPIO (bit-banged SCCB) | CAM-SDA | R247 pull-up |
| PD0 | GPIO out | CLIFF_LED_EN | |
| PD1, PD3 | TIM10_CH1/CH2 (remap 2) | WHEEL-MOT-L-IN1, -IN2 | PWM |
| PD5, PD7 | TIM10_CH3/CH4 | WHEEL-MOT-R-IN1, -IN2 | PWM |
| PD2 | UART5_RX | LIDAR_TX | |
| PD4 | GPIO out | X035-BOOT | R235 (100k) pull-down |
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
| PE12 | UART7_TX (remap) | STM32-TX | debug console (J4, JTAG1) |
| PE13 | UART7_RX (remap) | STM32-RX | |
| PE14 | UART8_TX (remap) | X035-RX | to U28 PC19 (RX3 / SDI DCK) |
| PE15 | UART8_RX (remap) | X035-TX | from U28 PC18 (TX3 / SDI DIO) |
| BOOT0 | pin 94 | BOOT0 | J1 pin 2, R22 pull-down |
| OSC_IN/OUT | pins 12/13 | | X3, 8 MHz, with C42/C39 (18 pF) |
| NRST | pin 14 | ~RST | R21, C37 |
| VBAT | pin 6 | VMCU-BAT-3V3 | |
| VDD x3, VIO x2, VDDA, VREF+ | | VMCU-3V3 | VDDA must equal VIO |
| VSS x5, VSSA, VREF- | | GND | pin 73 is NC |

**Interrupt lines:** 16 EXTI lines, each line number from one port only. The edge-timed inputs use lines 3–8, 11 and 12, one each: IR x5, encoders x2, IMU INT1. Hall, wheel-drop and ~INT-SENSORS inputs are polled.

**Timer remaps:** some remaps also route a timer's unused channels, ETR or break input onto pins used for something else, e.g. TIM10 BKIN onto PE2 and TIM9 CH3/CH4 onto PD13/PD15. Firmware must leave those outputs, the break inputs and ETR disabled.

## U28 CH32X035C8T6 pin map (LQFP-48)

46 GPIO; 31 used. The ADC inputs are A0–A9 only (PA0–PA7, PB0, PB1). **A3 (PA3) and I2C don't work on lots whose 5th-from-last batch digit is 0** (datasheet note 3), so PA3 is left free.

| Pin | Port | Function | Net | Notes |
|---|---|---|---|---|
| 10 | PA0 | ADC A0 | USB_VBUS_SENSE | 100k/47k divider |
| 11 | PA1 | ADC A1 | HALL-FLOOR-L | ≥200 Hz sampling |
| 12 | PA2 | ADC A2 | HALL-FLOOR-R | |
| 14 | PA4 | ADC A4 | BAT_SENSE | |
| 15 | PA5 | ADC A5 | DC_IN_SENSE | ≥1 kHz, catches the dock's signature probe |
| 16 | PA6 | ADC A6 | BAT_NTC | battery pulled while docked: the pin sees ~4.5 V through R233 (10k), ~0.1 mA into the clamp diodes, inside the ±5 mA limit |
| 17 | PA7 | ADC A7 | NTC | board NTC (T1/R38) |
| 20 | PB0 | ADC A8 | BAT_ID | |
| 21 | PB1 | ADC A9 | LDR | wake-up sensor |
| 40 | PA8 | GPIO out | LED-HOME | |
| 41 | PA9 | GPIO out | LED-PWR | |
| 42 | PA10 | GPIO in | ~CLEAN-BTN | internal pull-up |
| 43 | PA11 | GPIO in | ~HOME-BTN | internal pull-up |
| 44 | PA12 | GPIO in | PWR-BTN-SENSE | |
| 45 | PA13 | GPIO out | STM-PWR-CTRL | power latch, next to the button sense; R172 holds the latch while U28 boots |
| 1 | PA15 | GPIO in | HALL-BIN | internal pull-up |
| 2 | PA16 | GPIO out | VL-I2C-RESET | |
| 3 | PA17 | GPIO out | ~VL-L-LPn | |
| 4 | PA18 | GPIO out | SIDE-PROXI-CE-R | VL53L0X XSHUT |
| 7 | PA21/RST | NRST | X035-NRST | from U13 PC13; R234 (10k) + C185. Enable the reset function in the option bytes |
| 23 | PB3 | GPIO in | ~STDBY | internal pull-up |
| 26 | PB6 | GPIO out | CC-RD-EN | Rd switch, see below |
| 27 | PB7 | GPIO out | CAM-RESET | camera RESETB; R244 (10k) pull-down holds the camera in reset until U28 releases it |
| 29 | PB9 | TIM1_CH1 | (free) | reserved for the torch PWM |
| 35 | PB12 | GPIO out | USB_PWR_EN | phone charging switch (TMI6240 + Q27) |
| 32 | PC16 | GPIO in | ~CHRG | internal pull-up. PC16 is bonded to PC11: keep PC11 an input |
| 33 | PC17 | GPIO in | X035-BOOT | **boot detect:** high at power-up starts the bootloader. R235 pull-down; U13 PD4 can drive it. Bonded to PC10: keep PC10 an input |
| 34 | PC18 | USART3 TX (remap 1) / SDI DIO | X035-TX | to U13 PE15 |
| 37 | PC19 | USART3 RX (remap 1) / SDI DCK | X035-RX | from U13 PE14 |
| 38 | PC14 | PD CC1 | USB_CC1 | |
| 39 | PC15 | PD CC2 | USB_CC2 | |
| 48 / 47 | VDD / GND | | VMCU-3V3 | C183 100 nF + C184 10 µF |

Free: PA3, PA14, PA19, PA20, PA22, PA23, PB2, PB4, PB5, PB8, PB9, PB10, PB11, PB13, PC6, PC7.

The CD4051B mux from the draft is gone: the LQFP-48 has enough ADC inputs.

## USB-C PD

- The CH32X035 has the PD PHY but **no Rd pull-downs** on its CC pins (WCH adds them with its CH211 companion).
- R236/R237 (4.7k; Type-C allows 5.1k ±10 %) go from CC1/CC2 to GND through Q42/Q43 (AO3400). Both gates are on CC-RD-EN, with R238 (100k) pulling up to VMCU-3V3.
- Rd is there whenever VMCU-3V3 is up: the same dead-battery behaviour as the STM32 UCPD. Firmware pulls CC-RD-EN low only to source after a power-role swap; U28 then supplies Rp from its own pull-up modes.
- R221 (the old 100k pull-up on BUMP_R_LED_EN for the UCPD dead-battery pin) isn't needed any more; it is harmless and still fitted.

## Camera (DVP) connector

**J12:** 24-pin 0.5 mm FPC socket (HanElectricity 05A20L24P, C5362158, $0.04, flip lid, bottom contact), near the front edge on the top side. It takes the 24-pin OV2640 / OV3660 / OV5640 / GC2145 modules sold for ESP32-CAM boards; the pinout follows the AI-Thinker ESP32-CAM.

| J12 pin | Signal | | J12 pin | Signal |
|---|---|---|---|---|
| 1 | NC | | 13 | XCLK (PA8 through R248) |
| 2 | AGND | | 14 | Y8 (D6, PB8) |
| 3 | SIO_D (PC15) | | 15 | DGND |
| 4 | AVDD 2.8 V | | 16 | Y7 (D5, PB3) |
| 5 | SIO_C (PC14) | | 17 | PCLK (PA6) |
| 6 | RESETB (U28 PB7, R244 to GND) | | 18 | Y6 (D4, PC11) |
| 7 | VSYNC (PA5) | | 19 | Y2 (D0, PA9) |
| 8 | PWDN (PC10, R245 to GND) | | 20 | Y5 (D3, PC9) |
| 9 | HREF (PA4) | | 21 | Y3 (D1, PA10) |
| 10 | DVDD 1.2 V | | 22 | Y4 (D2, PC8) |
| 11 | DOVDD (VSENS-3V3) | | 23 | Y1 (NC, 8-bit mode) |
| 12 | Y9 (D7, PB9) | | 24 | Y0 (NC) |

**Camera power:**
- **DOVDD** is VSENS-3V3, so the camera I/O runs at 3.3 V like the MCU and the camera is on whenever the other sensors are. No separate switch (Q44 removed 2026-11-22): PWDN (U13 PC10) is the standby, CAM-RESET (U28 PB7) the hard reset.
- **AVDD 2.8 V:** U29 (VCAM-2V8), ME6211C28M5G-N (C53099), from VSENS-3V3.
- **DVDD 1.2 V:** U30 (VCAM-1V2), ME6211C12M5G-N (C236672), from VSENS-3V3, for OV2640-class sensors. OV3660 and OV5640 regulate their own core.
- 1 µF in and out on each LDO (C188–C191), 100 nF at J12 pins 4, 10 and 11 (C192–C194).
- SCCB pull-ups R246/R247 (4.7k) go to VSENS-3V3.
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

- **U13 (CH32V307):** the built-in bootloader does USB ISP on the high-speed port. Short J1 1-2 (BOOT0) at power-up and flash from a PC over USB-C with WCH's tool or wchisp. The WCH-LinkE on JTAG1 (SWDIO/SWCLK) is only needed for debugging. Phone updates: firmware jumps to the bootloader.
- **U28 (CH32X035):** U13 bit-bangs WCH's 2-wire SDI protocol on PE14/PE15, the same wires as the UART link, holding X035-NRST as needed. Normal updates go through an update loader in U28 over the UART. Fallback: U13 holds X035-BOOT high and resets U28 to start WCH's built-in bootloader. Test the bit-banged SDI on the dev boards first; the protocol isn't officially documented.

## BOM delta (JLC, 1k pcs)

| Change | $ |
|---|---|
| − STM32G473VCT6 | −7.39 |
| + CH32V307VCT6 | +2.18 |
| + CH32X035C8T6 | +0.38 |
| + 8 MHz crystal, − 32.768 kHz crystal | ≈ −0.05 |
| + Rd switch (2x AO3400, 2x 4.7k, 100k) | +0.02 |
| + carpet amplifier and detector (passives, 1N4148) | +0.01 |
| + J12, 2x ME6211, passives | +0.14 |
| **Net** | **≈ −4.7 per board** |

New BOM lines: CH32V307, CH32X035, the 8 MHz crystal, the FPC socket and two ME6211s. Removed: STM32G473 and the 32.768 kHz crystal. JLC stock of the CH32X035C8T6 is thin (197); check LCSC before a 500–1000-piece run.

## Bench tests (dev boards)

1. USB ISP over the high-speed port with BOOT0, and a jump to the bootloader from firmware.
2. Composite CDC + UVC at high speed to the phone: GC2145 YUV at VGA (~9–18 MB/s) and OV2640 JPEG.
3. DVP at the sensor's PCLK, with DVP_D5 on PB3 and USBHS enabled (check the lot code rule).
4. The carpet amplifier and envelope detector at 290 kHz.
5. U28 PD sink with the switched Rd, and a power-role swap with the phone.
6. U13 programming U28 over bit-banged SDI on the UART pins.

## Open items

- The camera module's pinout and contact side, and the flex length (in the 3D CAD model).
- The torch circuit (front ToF board connector 2x4 → 2x5 with switched 5 V); its PWM is reserved on U28 PB9.
- PCB layout: re-route U13 for the new pin map, place U28, J12 and the camera supplies.
