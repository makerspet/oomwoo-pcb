# OOMWOO I/O Board spec (work in progress)

See [vacuum BOM](https://github.com/makerspet/oomwoo/blob/main/BOM.md) for details.

## Reverse engineering data

Drive, brush and fan motors draw power directly from the 4S battery (not via a DC-DC converter). The battery is 4*3.6V=14.4V nominal, 4*2.9V=11.6V discharged and 4*4.2V=16.8V fully charged.

### DC Motors

<table>
  <tr><th>Part</th><th>Voltage</th><th>No load</th><th>Stall</th><th>Notes</th></tr>

  <tr>
    <td rowspan="3">Drive wheel</td><td>16.8V</td><td>0.12A</td><td>2A</td>
    <td rowspan="3">JST ZH 1.5mm 7-pin housing; RS-360-SH-15250 motor;
      pin 1 MOT+, 2 MOT-, 3 Hall GND (brown), 4 Hall signal out (blue, open collector), 5 Hall VCC (3.3-5V, orange), 6 COM wheel drop switch, 7 ON wheel drop switch;
      fits Roborock S4 Max, S45 Max, S5 Max, S50 Max, S55 Max, S6 MaxV, S6 Pure, S65 Pure, S65 MaxV, S7, S7 Pro, S7 MaxV, S7 Max Ultra, S70, S75, E4, E45, E5, E50, E55, G10, T7, T7S, Q5, Q7, Q7 Max, and Q Revo;
      purchased <a href="https://www.aliexpress.us/item/3256811615892849.html">here</a>; power supply current limit headroom ~1A;
      the wheel assembly appears to be identical to <a href="https://github.com/makerspet/oomwoo/tree/main/contributions/part-specs/IKsares/drive-wheel">this one</a> available
      <a href="https://www.aliexpress.us/item/3256807172774304.html">here</a> that uses GM-RS360-16248 motor with stall current possibly reaching ~3A.
    </td>
  </tr>
  <tr><td>14.4V</td><td>0.12A</td><td>1.7A</td></tr>
  <tr><td>12V</td><td></td><td></td></tr>

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
    <td rowspan="3">Mop rotary fixed</td><td>16.8V</td><td>0.15A</td><td>5.3A</td>
    <td rowspan="3">JST PH 2.0 4-pin housing, RS-385PH-2466 motor; pin 1 VCC fixed, 2 GND fixed, 3 GND FlexiArm, 4 VCC FlexiArm;
    fits Roborock Qrevo Master, Qrevo Slim, S8 Max V Ultra, G20S, V20, P10S Pro</td>
  </tr>
  <tr><td>14.4V</td><td>0.16A</td><td>4.3A</td></tr>
  <tr><td>11.6V</td><td>0.15A</td><td>3.7A</td></tr>

  <tr>
    <td rowspan="3">Mop rotary FlexiArm</td><td>16.8V</td><td>0.2A</td><td>5A</td>
    <td rowspan="3">JST PH 2.0 4-pin housing, RS-385PH-2466 motor; pin 1 VCC fixed, 2 GND fixed, 3 GND FlexiArm, 4 VCC FlexiArm;
    arm actuator likely JST GH 1.25; pin 1 black (ground?), 2 red (power?);
    fits Roborock Qrevo Master, Qrevo Slim, S8 Max V Ultra, G20S, V20, P10S Pro</td>
  </tr>
  <tr><td>14.4V</td><td>0.17A</td><td>4.3A</td></tr>
  <tr><td>11.6V</td><td>0.16A</td><td>3.6A</td></tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>55mA</td><td></td>
    <td><a href="https://www.tcstec.com">TCS Precision Technology<a>JSB1523025 peristaltic, 5V nominal (loud); JST ZH 2-pin housing; pin 1 MOT+, 2 MOT-</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>60mA</td><td></td>
    <td><a href="https://www.dyxminipump.com">ShenZhen Deyuxin Technology</a>DSB030-C peristaltic, 5V nominal (quiet); JST PH 2.0 2-pin housing; pin 1 MOT+, 2 MOT-</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>87mA</td><td></td>
    <td><a href="https://www.dgjbf.com">Dongguan Jingbofang Precision Electronics<a>JSB030-5A peristaltic, 5V nominal (loud); no connector</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>110mA</td><td></td>
    <td><a href="www.yyjiayin.com">Jiayin</a> JYPDM-6B peristaltic, 5V nominal (quiet-ish); JST XH 2.54mm 2-pin; pin 1 MOT+, 2 MOT-</td>
  </tr>

  <tr>
    <td>Water mini-pump</td><td>5V</td><td>330mA</td><td></td>
    <td><a href="https://conjoinfluid.com/">Conjoin</a> CJWP12-AA05A peristaltic, 5V nominal (loud); likely JST GH 1.25mm housing; pin 1 blue (ground?), 2 red (power?)</td>
  </tr>

</table>

### BLDC Motors

<table>
  <tr><th>Part</th><th>Voltage</th><th>Unobstructed</th><th>Fully Obstructed</th><th>Notes</th></tr>

  <tr>
    <td rowspan="3">Fan MSD-G v1</td><td>16.8V</td><td>3.65A</td><td>6A</td>
    <td rowspan="3">LHE MX3.0 4-pin (2x2) 3.0mm with latch header (aka Molex Micro-Fit 3.0); pin 1 VCC, 2 GND, 3 FG (open collector), 4 PWM (low off);
    fits Dreame X50 Ultra (20 kPa), X50 Master (20kPa)</td>
  </tr>
  <tr><td>14.4V</td><td>4.2A</td><td></td></tr>
  <tr><td>12V</td><td>5.25A</td><td></td></tr>

  <tr>
    <td rowspan="3">Fan BL27302101</td><td>16.8V</td><td>1.8A</td><td>1.8A</td>
    <td rowspan="3">JST PA 2mm 6-pin shrouded header; pin 1 VCC, 2 VCC, 3 GND, 4 GND, 5 PWM (low off), 6 FG (open collector);
    fits Roborock Saros 20 (36 kPa); </td>
  </tr>
  <tr><td>14.4V</td><td>2.1A</td><td></td></tr>
  <tr><td>12V</td><td>2.5A</td><td></td></tr>

  <tr>
    <td rowspan="3">Fan BL24131616<sup>*</sup></td><td>16.8V</td><td>1.75A</td><td>1.75A</td>
    <td rowspan="3">JST PA 2mm 5-pin shrouded header; pin 1 ID (22k to GND), 2 FG (open collector), 3 PWM (low off), 4 GND, 5 VCC;
    fits Roborock G20S P10 Pro (7 kPa), P10s Pro (11 kPa), P20, G20S S8 MaxV (10 kPa), Xiaomi S40 OV81 (10 kPa)</td>
  </tr>
  <tr><td>14.4V</td><td>2.1A</td><td>2.1A</td></tr>
  <tr><td>12V</td><td>2.6A</td><td>2.6A</td></tr>

  <tr>
    <td rowspan="3">Fan 22N704V160<sup>*</sup></td><td>16.8V</td><td>1.75A</td><td>3.25A</td>
    <td rowspan="3">JST PA 2mm 5-pin shrouded header; pin 1 ID (5 Ohm to GND), 2 FG (open collector), 3 PWM (low off), 4 GND, 5 VCC;
    fits Roborock G20S P10 Pro (7 kPa), P10s Pro (11 kPa), P20, G20S S8 MaxV (10 kPa), Xiaomi S40 OV81 (10 kPa)</td>
  </tr>
  <tr><td>14.4V</td><td>2.05A</td><td>2.7A</td></tr>
  <tr><td>12V</td><td>2.5A</td><td>2A</td></tr>

  <tr>
    <td rowspan="3">Fan 20N704R990F aka 20N704R980</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC; 20N <a href="https://www.nidec.com/en/product/search/category/B101/M102/S100/NCJ-20N-Type-4/">motor spec</a>
      ~5.1-6 kPa, fits Roborock S7 (2.5 kPa), S7 Pro (5.1 kPa), S7 MaxV (5.1 kPa), S75 MaxV (5.1 kPa), S8 (6 kPa), S8 Plus (6 kPa), S8 Pro Ultra (6 kPa), S8 MaxV Ultra (8 kPa), G20 (6 kPa), Q7 Max (4.2 kPa), Q7 Max Plus (4.2 kPa)</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan MSD-C-3</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC;
      fits Dreame L10s Prime (4 kPa), L10s Prime Ultra (5.3 kPa v1), L10s Prime Pro, D10s Plus (5 kPa), X10+ (4 kPa), X20+ (6 kPa)</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan MSD-D</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC;
      fits Dreame L20 (7 kPa), L30 Ultra (7.3 kPa), S10 (5.3 kPa), S10 Plus (7 kPa)</td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan 20N709U020</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 4-pin shrouded header; pin 1 FG (open collector), 2 PWM (low off), 3 GND, 4 VCC;
      fits Dreame L10s Ultra (5.3 kPa), L10s Pro (5.3 kPa), L10 Ultra (5.3 kPa), D10s Pro (5 kPa); Xiaomi X20+ (6 kPa), C102 B101CN, X10+ (4 kPa), S10 Plus (4 kPa)
    </td>
  </tr>
  <tr><td></td><td></td><td></td></tr>
  <tr><td></td><td></td><td></td></tr>

  <tr>
    <td rowspan="3">Fan BL24131607</td><td></td><td></td><td></td>
    <td rowspan="3">JST PH 2.0mm 5-pin shrouded header; pin 1 ID (20k to GND), 2 FG (open collector), 3 PWM (low off), 4 GND, 5 VCC;
      fits Roborock P10 Pro (7 kPa), Qrevo Maxv (7 kPa), P10S (7 kPa), Qrevo S (7 kPa), Qrevo Pro (7 kPa)</td>
  </tr>
  <tr><td>15V</td><td>1.7A</td><td>2.7A</td></tr>
  <tr><td></td><td></td><td></td></tr>

</table>

### Sensors, Battery

<table>
  <tr><th>Part</th><th>Voltage</th><th>Notes</th></tr>

  <tr>
    <td>Cliff sensors</td><td></td>
    <td>JST PHDR-16VS 2.0mm 8x2 housing, mates JST S16B-PHDSS, JST B16B-PADSS; fits iRobot Roomba 500 600 700 800 528 552 564 595 560 570 610 615 620 625 630 650</td>
  </tr>

  <tr>
    <td>Battery</td><td></td>
    <td>4S2P 14.4V nominal <a href="https://images.thdstatic.com/catalog/pdfImages/55/55d2f7f6-2ed9-44ed-ab4e-fb20d231c897.pdf">BRR-2P4S-5200FL battery</a> or similar;
    4-pin 3mm pitch with latch male LHE MX3.0 (C3001-H04), Molex Micro-Fit 3.0;
    pin 4 BAT+, 3 NTC (10.7K), 2 ID (0.62M to ground), 1 GND</td>
  </tr>

  <tr>
    <td>Carpet sensor</td><td>≥12V, 14.4V?</td>
    <td>290KHz piezo ultrasonic, <a href="https://htwsensor.en.made-in-china.com/product/HfMYgjwoZxVh/China-300kHz-Carpet-Material-Recognition-Sensor-for-Robotic-Vacuum-Cleaner-Ultraosinc-Sensor.html">likely this one</a>,
      JST ZH 2-pin housing; <a href="https://makerspet.com/blog/how-to-source-bom-for-oomwoo-open-source-vacuum-robot/#carpet-sensor">sourcing notes</a>
      pin 1 white, 2 black (driven by AC, polarity doesn't matter?)
    </td>
  </tr>

</table>

All components tested with Agilent 6653A unless mentioned otherwise. The current limit was set high enough to not be triggered.

<sup>*</sup> Appear to be interchangeable

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

### IR receiver ICs

- required to 1) find dock without map (beacon), 2) communicate with the dock (bi-directional, ~1 kbit/s)
  - Maybe we'll use LiDAR for docking (simpler mechanical, PCB design). If that fails, 3) docking.
- use 38 kHz NEC protocol receivers (56 kHz parts are Vishay-only, expensive, barely stocked)
  - firmware: time-share IR transmissions
  - dock stops 
- TSOP38238 costs ~$0.56, relatively expensive; economical IC options, sorted by preference
  - Everlight IRM-H638T/TR2	C91447 SMD 5×4 $0.168 194k Deep stock, reputable.
  - Everlight IRM-3638T	C42421366 Through-hole $0.103 206k Side-looking, cheapest reputable through-hole; [datasheet](https://www.alldatasheet.com/datasheet-pdf/view/229626/EVERLIGHT/IRM-3638T.html).
  - Yongyu GRM-4033H4C6-ET2	C51901765	SMD	$0.118	2.7k	50 µA, 2.4–5.5 V. Best SMD challenger.
  - TONYU DY-IRM383T/LP-T-20	C46682928	Through-hole	$0.068	420	100 µA, 2.7–5.5 V. Cheapest real receiver, sunlight rejection not specified; [datasheet](https://file.aichiplink.com/static/lcsc/documents/2026-01-29/18c143340b0d5fc0ffdf5ff7098aaff5.pdf).
  - TONYU DY-IRMA385-T5-W1-F1	C7433009	SMD-3P	$0.110	2.1k	200 µA, ±35°. Narrower field of view.
  - Chau Light ZSIRM-Z1QN86	C5337492	SMD 5×4.2	$0.112	1.8k	400 µA, 45°.
  - TONYU DY-IRMA386/387	C6075467/68	Through-hole	$0.128	124/660	±60° wide field of view, low stock.
  - XINGLIGHT XL-IRM0038C-38X	C42400831	SMD 5×4.2	$0.133	137	150 µA, 75°, –40 °C to +85 °C. Stock too thin.
- Deciding factors - stock depth, sunlight rejection, SMD (cheaper to assemble), angle of view (wide for dock search, narrow for docking, comms), side-looking vs straight up orientation
  - current draw battery drain is not a factor

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

## Audio IC

I2S DAC MAX98357AETE_T C910544 TQFP is expensive at $0.88 100pcs, has a built-in speaker driver.
NS4168 C910588 $0.47 is a MAX98357AETE_T clone, 7K+ stock, except in a different package (ESOP).
That happens to be advantageous because ESOP is better than TQFP for bring-up and DIY hacking.

Claude says:
- NS4168 works the same way as the MAX98357A: I²S in, mono class-D out, driving the speaker directly.
- Specs: 3.0–5.5 V supply, 2.5 W into 4 Ω at 5 V, 8–96 kHz sample rates. It has a CTRL pin that picks the left or right channel and also acts as shutdown.
- No MCLK needed. This matters because the Pi's I²S port can't output an MCLK; the MAX98357A was chosen for the same reason.
- Linux: like the MAX98357A, it has no control interface. The existing Raspberry Pi `max98357a` overlay drives any chip like this, so the software stays the same on CM4 and CM5.
- Check the CTRL-pin voltage levels against the datasheet and strap it for the left channel or the (L+R)/2 mix; either is fine for mono voice prompts.
- Power: run the amp from the 5 V rail, with 10–22 µF bulk plus 100 nF right at the power pin. Peak current into a 4 Ω, 2–3 W speaker is under 1 A.
- EMI: the outputs switch at high frequency with no filter. Keep speaker traces short, or twisted if they go through wires, and away from the IR receivers and the LiDAR data lines. Leave pads for ferrite beads on the speaker leads in case the sim or bench test shows interference.
- Shutdown: wire the CTRL pin to a GPIO so you can power the amp down when idle. That saves the ~13 mA quiescent current and avoids pops at boot.
- Pins: CM4 and CM5 both use GPIO18 (BCLK), GPIO19 (LRCK) and GPIO21 (DOUT). I²S is the one audio path both modules share. PWM audio on GPIO12/13 is cheaper on CM4, but I believe the CM5 doesn't support it, so it doesn't suit a carrier for both.

## Mic array (optional)

Claude: build it as a USB mic board. Four digital PDM MEMS mics sampled by an RP2040, which shows up as a standard 4-channel USB microphone. It needs no Pi-specific driver and costs roughly $2–3 in parts. It works the same on CM4 and CM5.

Why not wire the mics to the Pi's I²S bus?
- Not enough inputs. The CM4 has one I²S data-in pin (GPIO20). One data line carries two mics (left and right), so plain I²S tops out at 2 mics. Getting 4 means TDM-output mics, which are expensive and rare, plus fiddly TDM setup in the Linux device tree. The CM5's audio block is different again.
- Shared with the speaker. The NS4168 already uses that I²S bus's clock lines. The mics would be forced to run at the speaker's sample rate, and the mic board would inherit any CM4/CM5 differences.
- Fast clock over a cable. A ~3 MHz bit clock has to run up a flying cable to the top of the LiDAR cage, right beside the LiDAR motor.

The one real advantage of I²S is that mic and speaker share a clock, which makes echo cancellation easier. See the trade-off near the end.

Why USB with an RP2040
- Works on any compute. It looks like an ordinary USB microphone, so it works on CM4, CM5, a laptop on the bench, and possibly a phone over USB OTG.
- All four mics are sampled together. Pairs of PDM mics share a data line: one mic outputs on the rising clock edge and the other on the falling edge. So 4 mics need 1 clock line and 2 data lines, all on the same clock. That exact sample alignment is what direction-finding needs, and USB can't disturb it.
- Converting PDM to audio: the RP2040's programmable I/O captures the raw bit streams and firmware filters them down to 16 kHz audio. Four channels at 16 kHz should fit on its two cores; confirm on the first board. The pin-compatible RP2350 has more headroom if it's tight. There is existing open-source code for Pico PDM mics and for TinyUSB USB-audio to start from.
- Simple cable: 4 wires (5 V, D+, D−, GND) up to the cage.
- Easy for people to hack: the RP2040 is well known, and there are free pins for LEDs or a button.

Mic geometry
- Use 4 mics, not 3. Three is enough to find a direction on the floor plane, but 4 in a square gives better beamforming, spare measurements and simpler maths.
- Make the array as wide as the cage top allows, about 60–70 mm diameter, similar in size to ReSpeaker-type arrays. Wider spacing gives better direction accuracy.
- At 65 mm across, sound takes at most 0.19 ms to cross the array: only about 3 samples at 16 kHz.
- Frequency-domain methods such as SRP-PHAT (used by the ODAS direction-finding library) handle fractions of a sample. Capture at 48 kHz if you want finer resolution.
- Mount the mics on the underside of the board. Use bottom-port mics with the sound hole drilled through to the top. The top stays flat and the mics are protected.
- Cover each port with an acoustic mesh or membrane. It's a vacuum cleaner, so dust and hair are the main way these mics will fail.

Mechanical and electrical notes
- Isolate the board from vibration. MEMS mics pick up vibration through the structure, and the LiDAR motor sits right below. Mount on silicone grommets or foam, not rigid standoffs.
- Keep it low. The cage top is usually the robot's highest point, so the board adds directly to under-furniture clearance. If you ever add a top-contact bump switch on the cage, plan the board around it.
- Digital mics don't pick up the LiDAR motor's electrical noise. Keep the PDM traces short; a 22–33 Ω series resistor on the clock is enough.
- Power: a 3.3 V regulator on the board, and ESD protection on the USB data lines at the connector.
- Hardware mute: add a switch that cuts power to the mics, with an LED showing when they're off. People are wary of a mic that roams their home. A hardware switch is cheap and more convincing than a software mute.
- Optional: a ring of a few WS2812 LEDs to show which direction the robot is listening.

What noise cancellation can realistically do

Set expectations before promising "noise cancellation":
- The fan is loud. A running vacuum is roughly 65–75 dBA at a mic about 15 cm from the fan. Four-mic beamforming buys about 6 dB plus whatever the post-filter adds. That helps, but won't make speech clear during full-power cleaning.
- The fan never moves relative to the mics. That is the one big advantage you have. An MVDR beamformer can "learn" the fan noise while the fan runs with nobody talking, and place a fixed null toward it. That works much better than generic noise suppression.
- Plan the interaction around it. The robot hears the wake word, drops the fan to low or off, and then listens for the command. Commands at full suction would stay unreliable.
- Echo cancellation: mic and speaker are on different clocks (USB vs I²S). PipeWire's WebRTC echo-cancel module copes with clock drift, but not perfectly. If you later want solid "barge-in" (talking over the robot's own voice prompts), the clean fix is to play one of the RP2040's spare channels as a loopback of the speaker signal. That can wait.

Software
- Linux sees a 4-channel USB microphone through ALSA or PipeWire.
- ODAS (IntRoLab) handles direction-finding and sound tracking, and there is an odas_ros package for ROS 2.
- Other options: openWakeWord for the wake word, and Vosk or whisper.cpp for speech recognition on a CM5.
- Pair it with the LiDAR: the mics give the speaker's direction and the LiDAR gives the distance.

Cheaper alternative: 2 mics on I²S, no MCU
- Two I²S MEMS mics on GPIO20, sharing the NS4168's clock lines. This gets you direction-finding with front/back ambiguity, mild beamforming and easy echo cancellation.
- It's a fine "lite" option, but it's limited to 2 mics and still runs a fast clock up the cage.

## USB, UART allocation

Put the Linux console to a UART (not USB). Then the single USB port can serve the mic board in normal use and only be needed for flashing, and neither job needs extra ICs.
- UART0 on GPIO14/15 as the Linux console. This is standard on both CM4 and CM5.
- SSH and Foxglove over Wi-Fi. A cable to a moving robot is awkward anyway.
- Flashing eMMC, if available (rpiboot): Has to stay on USB; there's no UART alternative. But it's only needed for eMMC modules, rarely, and only while the robot isn't running.
  - The two remaining USB jobs never happen at the same time. For flashing, the CM4 acts as a USB device to your PC. In normal running, it acts as the host for the mic board. So they can share one port.

Proposed design
- UART debug header. Use the same 3-pin JST-SH pinout as the Pi 5's debug UART connector. Then the official Raspberry Pi Debug Probe, or any 3.3 V USB-to-serial adapter, plugs straight in. It's free apart from the connector.
  - If the STM32 link currently uses UART0, move it. The CM4 has UART2–5 available through device-tree overlays, so there are spares.
- One internal USB header, for example a 4-pin JST-GH, wired to the CM4's USB 2.0 pins.
  - Normal use: the mic board plugs in here. Or makers can plug in a USB hub, a USB stick, or a USB-audio or ReSpeaker-style array; it's their choice.
  - Flashing: unplug the mic board, set the boot jumper (nRPIBOOT), and connect a JST-GH-to-USB-A adapter cable to the PC.
  - Power (VBUS): feed the header's 5 V from the carrier through a polyfuse. Leave VBUS unconnected in the flashing adapter cable so the PC and the robot never feed power into each other; the robot powers itself while flashing. It's worth checking the CM4 datasheet for whether `rpiboot` needs to sense VBUS.
- Host mode on CM4: the CM4's USB port is off by default. Add `[cm4]` then `otg_mode=1` in `config.txt`. That turns it on in host mode using the Pi's XHCI controller, which handles USB audio better than the older `dwc2` controller. The boot ROM still enters flashing mode when the nRPIBOOT jumper is set.
- CM5: use the same header and the same mic board, so there's one design for both modules. The CM5's extra USB 3 ports stay free for whatever makers want.
- The mic board is USB full-speed (12 Mbit/s), which puts little load on the port.

## TODO

| Type | Qty | Spec |
| --- | --- | --- |
| LiDAR | 1 | 5V 0.35A max, Mabuchi-style RF-500TB-14350 or similar, low-side load switch N-FET |
| Main brush | 1 | DC 14.4-15V PRI-390SV-24100, JLS-395PH-2248A, RS-390WM-3107GCF or similar |
| Side brush | 1 | DC 14.4V RC500-KW/14440/DV, PR-500EV-14440 or similar |
| Mop | 2 | GM-RS385Y-24065 or similar, DC 14.4V |
