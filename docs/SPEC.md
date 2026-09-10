# OOMWOO I/O Board spec (work in progress)

See [vacuum BOM](https://github.com/makerspet/oomwoo/blob/main/BOM.md) for details.

## Reverse engineering data

Drive, brush and fan motors draw power directly from the 4S battery (not via a DC-DC converter). The battery is 4*3.6V=14.4V nominal, 4*2.9V=11.6V discharged and 4*4.2V=16.8V fully charged.

<table>
  <tr><th>Part</th><th>Voltage</th><th>Idle</th><th>Peak</th><th>Notes</th></tr>

  <tr>
    <td rowspan="3">Drive wheel</td><td>16.8V</td><td>0.12A</td><td>2A</td>
    <td rowspan="3">JST ZH 1.5mm 7-pin housing; RS-360-SH-15250 motor;
      pin 1 MOT+, 2 MOT-, 3 Hall GND (brown), 4 Hall signal out (blue, open collector), 5 Hall VCC (3.3-5V, orange), 6 COM wheel drop switch, 7 ON wheel drop switch;
      fits Roborock S4 Max, S45 Max, S5 Max, S50 Max, S55 Max, S6 MaxV, S6 Pure, S65 Pure, S65 MaxV, S7, S7 Pro, S7 MaxV, S7 Max Ultra, S70, S75, E4, E45, E5, E50, E55, G10, T7, T7S, Q5, Q7, Q7 Max, and Q Revo
    </td>
  </tr>
  <tr><td>14.4V</td><td>4.2A</td><td></td></tr>
  <tr><td>12V</td><td>5.25A</td><td></td></tr>
  
  <tr>
    <td rowspan="3">Fan MSD-G v1, ~20kPa</td><td>16.8V</td><td>3.65A</td><td>6A</td>
    <td rowspan="3">LHE MX3.0 4-pin (2x2) 3.0mm with latch header (aka Molex Micro-Fit 3.0); pin 1 VCC, 2 GND, 3 FG (open collector), 4 PWM (low off)</td>
  </tr>
  <tr><td>14.4V</td><td>4.2A</td><td></td></tr>
  <tr><td>12V</td><td>5.25A</td><td></td></tr>

  <tr>
    <td rowspan="3">Fan BL27302101</td><td>16.8V</td><td>1.8A</td><td>1.8A</td>
    <td rowspan="3">JST PA 2mm 6-pin shrouded header; pin 1 VCC, 2 VCC, 3 GND, 4 GND, 5 PWM (low off), 6 FG (open collector)</td>
  </tr>
  <tr><td>14.4V</td><td>2.1A</td><td></td></tr>
  <tr><td>12V</td><td>2.5A</td><td></td></tr>

  <tr>
    <td rowspan="3">Fan BL24131616 ~10kPa</td><td>16.8V</td><td>1.75A</td><td>1.75A</td>
    <td rowspan="3">JST PA 2mm 5-pin shrouded header; pin 1 ID (22k to GND), 2 FG (open collector), 3 PWM (low off), 4 GND, 5 VCC</td>
  </tr>
  <tr><td>14.4V</td><td>2.1A</td><td>2.1A</td></tr>
  <tr><td>12V</td><td>2.6A</td><td>2.6A</td></tr>

  <tr>
    <td rowspan="3">Fan 22N704V160 ~10kPa</td><td>16.8V</td><td>1.75A</td><td>3.25A</td>
    <td rowspan="3">JST PA 2mm 5-pin shrouded header; pin 1 ID (5 Ohm to GND), 2 FG (open collector), 3 PWM (low off), 4 GND, 5 VCC</td>
  </tr>
  <tr><td>14.4V</td><td>2.05A</td><td>2.7A</td></tr>
  <tr><td>12V</td><td>2.5A</td><td>2A</td></tr>

  <tr>
    <td rowspan="3">Fan 20N704R990F</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan MSD-C-3 ~6kPa</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan MSD-D ~7kPa</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan 20N709U020 ~6kPa</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan BL24131607 ~7kPa</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 5-pin shrouded header; pin 1 ID (20k to GND), 2 FG (open collector), 3 PWM (low off), 4 GND, 5 VCC</td>
  </tr>
  <tr><td>15V</td><td>1.7A</td><td>2.7A</td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Main brush</td><td></td><td></td><td></td>
    <td rowspan="3">Roborock S50 S51 S55 XIAOWA C10</td>
  </tr>
  <tr><td>16.8V</td><td>0.27A</td><td>7A</td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Side brush FlexiArm</td><td></td><td></td><td></td>
    <td rowspan="3">RC500-KW/14440/DV motor; JST ZH 1.25mm 5-pin housing, 14.4V motor nominal;
      pin 1 MOT-, 2 MOT+, 3 IR output? (Arm folded in fully -> sensor blocked), 4 IR GND? 5 IR VDD?
      fits Roborock Qrevo Master, Qrevo Slim, S8 Max V Ultra</td>
  </tr>
  <tr><td>16.8V</td><td>0.07A</td><td>1.7A</td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Side brush fixed</td><td></td><td></td><td></td>
    <td rowspan="3">RC500-KW/14440/DV motor; fits Roborock Robot Vacuum S50 S51 S52 S55 S502-00/01/02/03** S552-00 S60 S61 S65 S5 Max S6 Pure MAX S7 S70 S75</td>
  </tr>
  <tr><td>16.8V</td><td>0.07A</td><td>1.7A</td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td>Cliff sensors</td><td></td><td></td><td></td>
    <td>JST PAD 2.0mm 8x2 housing, mates JST S16B-PHDSS, JST B16B-PADSS; fits iRobot Roomba 500 600 700 800 528 552 564 595 560 570 610 615 620 625 630 650</td>
  </tr>

  <tr>
    <td>Battery</td><td></td><td></td><td></td>
    <td>4S2P 14.4V nominal BRR-2P4S-5200FL battery datasheet](https://images.thdstatic.com/catalog/pdfImages/55/55d2f7f6-2ed9-44ed-ab4e-fb20d231c897.pdf) or similar;
    4-pin 3mm pitch with latch male LHE MX3.0 (C3001-H04), Molex Micro-Fit 3.0;
    pin 4 BAT+, 3 NTC (10.7K), 2 ID (0.62M to ground), 1 GND</td>
  </tr>

  <tr>
    <td rowspan="3">Mop rotary fixed</td><td>16.8V</td><td>0.15A</td><td>5.3A</td>
    <td rowspan="3">JST PH 2.0 4-pin housing, RS-385PH-2466 motor; pin 1 VCC fixed, 2 GND fixed, 3 GND FlexiArm, 4 VCC FlexiArm;
    fits Roborock Qrevo Master, Qrevo Slim, S8 Max V Ultra, G20S, V20, P10S Pro</td>
  </tr>
  <tr><td>14.4V</td><td>0.16A</td><td>4.3A</td></tr>
  <tr><td>11.6V</td><td>0.15A</td><td>3.7A</td></tr>

  <tr>
    <td rowspan="3">Mop rotary FlexiArm</td><td>16.8V</td><td>0.2A</td><td>5A</td>
    <td rowspan="3">JST PH 2.0 4-pin housing, RS-385PH-2466 motor; pin 1 VCC fixed, 2 GND fixed, 3 GND FlexiArm, 4 VCC FlexiArm;
    fits Roborock Qrevo Master, Qrevo Slim, S8 Max V Ultra, G20S, V20, P10S Pro</td>
  </tr>
  <tr><td>14.4V</td><td>0.17A</td><td>4.3A</td></tr>
  <tr><td>11.6V</td><td>0.16A</td><td>3.6A</td></tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>55mA</td><td></td>
    <td>JSB15224025 peristaltic, 5V nominal (loud); JST ZH 2-pin housing; pin 1 MOT+, 2 MOT-</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>60mA</td><td></td>
    <td>DSB030-C peristaltic, 5V nominal (quiet); JST PH 2.0 2-pin housing; pin 1 MOT+, 2 MOT-</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>87mA</td><td></td>
    <td>JSB030-5A peristaltic, 5V nominal (loud)</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>110mA</td><td></td>
    <td>JYPDM-6B peristaltic, 5V nominal; 2mm pitch housing with a "squish" latch; pin 1 MOT+, 2 MOT-</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>330mA</td><td></td>
    <td>CJWP12-AA05A peristaltic, 5V nominal (loud); 1.25mm pitch housing mystery latch</td>
  </tr>

  <tr>
    <td>Carpet sensor</td><td></td><td></td><td></td>
    <td>290KHz piezo ultrasonic, <a href="https://htwsensor.en.made-in-china.com/product/HfMYgjwoZxVh/China-300kHz-Carpet-Material-Recognition-Sensor-for-Robotic-Vacuum-Cleaner-Ultraosinc-Sensor.html">likely this one</a>,
      12V minimum; JST ZH 2-pin housing; <a href="https://makerspet.com/blog/how-to-source-bom-for-oomwoo-open-source-vacuum-robot/#carpet-sensor">sourcing notes</a>
    </td>
  </tr>

</table>

Mop lift TBD

Mop arm actuator - Roborock FlexiArm; later replace with own design

## Compute + Camera

- 2x 15-pin ArduCam-style connectors for OV5647
- TODO add USB to I/O board
- provision an M.2 slot, route a PICe lane, populate later - to experiment with NPU accelerator(s) like Hailo

Undecided TODO 
- USB-C 3.0+, CM5 only - to experiment with accelerator(s) like Coral TPU
- Keep the compute socket able to take an integrated-NPU module too (Radxa CM5) or premium-upgradeable (CM5 + M.2 Hailo).
- Flag it to the PCB contractor as a design item: M.2 E-key (WiFi) + an M.2 M-key/PCIe (NPU or NVMe), PCIe lane routing, and the thermal path for a few-watt accelerator in a suction-cooled enclosure

### Robot

- the robot has 2 power inputs: USB-C and dock
  - robot receives 20-24V fixed DC from the dock
  - USB-C power use PD, request 20-24 V minimum (to step it down to 4S battery)
  - optional PPS
  - if a low-power USB-C 5V, 9V or 15V brick source is attached (no 20V/PPS), either charge slowly (optional) through a boost path or cleanly refuse and signal "insufficient charger" rather than misbehaving
- robot requires 65W minimum input (from the dock) with system power-path charger (a charger IC with a SYS rail)
  - support the vacuum charging and Raspberry Pi running simultaneously
  - assume Raspberry Pi is always on (to handle user access over Wi-Fi at any time)
  - Pi CM5 worst case ~15.6W
  - M.2
  - Healthy charge ~40 W (~0.5C into the 75 Wh pack)
  - ~65–70 W total
- cap charge at ~0.5C regardless of charging adapter power
- MCU reset drops everything to a safe state, so motors are off during reset, firmware upload and firmware crash
  - watchdog

### Dock

- the dock is powered from an external certified 24/25.2 V DC brick (~200–350 W)
  - use external brick for safety, the dock enclosure only ever sees 24 V DC
  - reuse a 25.2 V stick-vac motor for auto-empty, e.g. Dreame M10-E-4 25.2 V/310 W
- the dock has only 2 contacts: DOCK+ and GND
  - dock contacts feed a fixed 24V+ DC
  - the dock detects load/robot presence, energizes DOCK+ only when robot is detected (reliably, after a couple of seconds)
  - dock contacts are spring loaded, gold-coated pogo pins ≥4 A, placed rear-vertical, above water line
- ambient fan(s) for mop drying
  - no hot mop dry for now
- 2x water pumps: clean-feed + dirty-evacuate
  - diaphragm, 12–24 V
- dock PCB
  - ESP32 (WiFi + BLE + control)
  - Pump/fan drivers (brushed DC)
  - IR beacon LEDs + driver
  - robot/load presence-detect + charging contact energize FET
  - Level sensors (float/capacitive) clean-low, dirty-full
  - high-side FET for auto-empty blower
  - fuse, DC inlet, TVS
  - buck DC-DC 24V to 5V, 3.3V for ESP32, sensors

### Power path

Standard capability of power-path charger ICs - TI bq25 family and similar.

```
USB-C 20V ─► [PD sink] ─► [power-path charger] ─┬─► SYS rail ─► 14.4→5V buck ─► Pi (always-on)
                                                └─► charges 4S pack
Battery ────────────────────────────────────────┘ (supplements SYS if input insufficient)
```

- Docked: the Pi runs from the input via SYS; the battery charges from the surplus; once full, charge current → 0 and the Pi keeps running off input — no needless battery cycling while docked (also a longevity win).
- Undocked: SYS seamlessly falls back to the battery — the Pi never browns out during the handoff. This is exactly what makes "pause → return to charge → resume" and "app connects anytime" work cleanly.
- Input-limited: if only a weak brick is attached, the battery supplements SYS so the Pi stays up, and charge current backs off. Graceful degradation for free.

Details

1. 65 W = 20 V / 3.25 A → e-marked cable required. Above 3 A / 60 W, USB-C needs a 5 A e-marked cable. Unavoidable at 65 W (20 V is PD's max fixed voltage) — just document it. 65 W bricks ship with an e-marked cable anyway.
2. Dynamic power management (VIN/IIN-DPM): the charger must throttle charge current to keep total draw within the negotiated PD budget, prioritizing the Pi/SYS load. Standard on power-path chargers.
3. Cap charge current at ~0.5C (~2.6 A into the pack) for cell life, regardless of surplus — don't let a big brick fast-charge the cells.
4. Two DC inputs, one charger: the robot's own USB-C port and the dock contacts both present ~20 V DC → OR them into the charger's VBUS with priority/ideal-diode selection (both are the same voltage, so it's clean).
5. Dock side: dock has its own PD sink + 65 W brick, passes ~20 V to the contacts. At 20 V, 65 W ≈ 3.25 A over the contacts → size the pogo/spring contacts for ~4 A with margin.

Net spec

1. USB-C PD, 65 W minimum (20 V / 3.25 A), on both the robot port and the dock (each with its own PD sink); e-marked cable expected.
2. Power-path 4S charger with a SYS rail feeding the Pi's 5 V buck, so the Pi is always-on from input when docked and from battery when not, with seamless handoff and battery-supplement under load.
3. DPM + 0.5C charge-current cap; OR the two DC inputs into one VBUS; dock contacts rated ~4 A.

## How to drive carpet sensor

- 290KHz ultrasonic piezoelectric analog
- ≥12V DC stabilized per spec (not 4S battery directly)
  - make DC voltage configurable using a resistive divider
  - current consumption - calculate 300KHz driving 1300±20% pF per sensor spec
  - make it withstand shorts
- connect sensor analog I/O to MCU ADC input
- use STM32G473VCT6 internal op-amp as echo input (AC via a cap)
- clamp amplitude to 3.3V (back-to-back clamp diodes)
- add a series resistor to STM32 op-amp input (extra protection against 12V)
- (firmware) bias the MCU internal op-amp to Vref/2 using MCU internal DAC
- (firmware) configure ADC pre-amp gain, PGA mode (op-amp bandwidth is 10MHz)
- (firmware) configure op-amp to output signal to internal ADC channel
- drive sensor analog I/O using a FET half-bridge
- drive the half-bridge by MCU, one GPIO for high side, one GPIO for low side
- add pull-up/down to FET inputs, so the bridge is off when MCU GPIO is tristated
- (firmware) drive the sensor for a brief while
- (firmware) tristate both FETs
- (firmware) measure using ADC, calculate return amplitude

## LiDAR pinouts

```
X-WPFTB-V2.6.2 PCB marking - JST GH 1.25mm 4-pin shrouded housing

D-WPFTBCD-V1.0.1 PCB marking - JST GH 1.25mm 4-pin shrouded housing

LDROBOT LD14P lookalike - JST GH 1.25mm 4-pin shrouded housing

Mystery mini - JST GH 1.25mm 5-pin shrouded housing
```

## Front sensors module board

- 2x VL53L7CH (or VL53L7CX) 60° horizontal FoV each
  - each turned 30° left, right to cover 120° horizontal FoV
- 2x OV5647, 5M wide-angle for stereo depth + object recognition
  - off-the-shelf breakout boards for now
  - possibly $2 imaging ICs later
- NIR illumination LEDs with a projection pattern
- breaks into multiple PCBs using holes
  - central - 2x TSOP38238 (separated by a baffle) for dock homing
  - left - VL53L7CH pointed 30° left
  - right - VL53L7CH pointed 30° right
  - stereo depth camera 2x OV5647 with NIR illumination LEDs

## Side sensors module board

- TSOP38238 for dock detection
- consumer vacuums use analog Sharp short-range distance sensor
  - use VL6180V1NR/1 C2655167 $1.03 100pcs 18° FoV diagonal? Obsolete, similar to VL53L4CD
  - use VL53L0CX GY-530, TMF8806 or similar instead? Dust may be an issue.
  - VL53L0CXV0DH/1 C91199 $2.11 100pcs
  - VL53L4CDV0DH/1 C3178291 $2.19 100pcs

## Sensors

- VL53L7CH
  - Arduino library https://github.com/stm32duino/VL53L7CH
  - hookup schematic https://eu.mouser.com/en/new/stmicroelectronics/stm-vl53l7ch-tof-sensor
  - LPn pin sets I2C address

## Water pump

- 5V DC motor, peristaltic; ~0.6A rated, 1A max
- make DC settable by replacing resistors

## GPIO

Please see the [PCB schematic](https://github.com/makerspet/oomwoo-io-board/tree/main/kicad/PDF) for up-to-date GPIO list.

TODO before layout/fabrication: confirm whether GPIO entries 36 and 46 are intentionally separate bumper inputs or a duplicate label.

How to drive
- ≥12V DC stabilized per spec (not 4S battery directly?)
- connect to MCU ADC input
  - use STM32G473VCT6 internal op-amp as echo input (AC via a cap)
  - clamp amplitude to 3.3V (back-to-back clamp diodes, series resistor)
  - bias the MCU internal op-amp to Vref/2 using MCU internal DAC
  - configure ADC pre-amp gain, PGA mode (op-amp bandwidth is 10MHz)
  - configure op-amp to output signal to internal ADC channel
- FET half-bridge driven by MCU
  - drive the sensor for a brief while
  - tristate both FETs
  - measure using ADC, calculate return amplitude
  - calibrate return amplitude when docked
- 2-pin connector "1.25mm Y" per spec, exact model unclear
  - not Molex PicoBlade 1.25mm, not JST GH 1.25mm

## TODO

| Type | Qty | Spec |
| --- | --- | --- |
| LiDAR | 1 | 5V 0.35A max, Mabuchi-style RF-500TB-14350 or similar, low-side load switch N-FET |
| Main brush | 1 | DC 14.4-15V PRI-390SV-24100, JLS-395PH-2248A, RS-390WM-3107GCF or similar |
| Side brush | 1 | DC 14.4V RC500-KW/14440/DV, PR-500EV-14440 or similar |
| Mop | 2 | GM-RS385Y-24065 or similar, DC 14.4V |
