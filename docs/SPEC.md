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
    <td>Cliff sensors</td><td>5 V LED, 3.3 V out</td>
    <td>v1 (2026-10-28): six <a href="../kicad/cliff-sensor/README.md">cliff sensor boards</a> (IR333-A + PT333-3B, no lenses), JST SH 4-pin. Before: the Roomba 500-800 cliff/bumper harness (JST PHDR-16VS 2x8 housing)</td>
  </tr>

  <tr>
    <td>Battery</td><td></td>
    <td>4S2P 14.4V nominal <a href="https://images.thdstatic.com/catalog/pdfImages/55/55d2f7f6-2ed9-44ed-ab4e-fb20d231c897.pdf">BRR-2P4S-5200FL battery</a> or similar;
    4-pin 3mm pitch with latch male LHE MX3.0 (C3001-H04), Molex Micro-Fit 3.0;
    pin 4 BAT+, 3 NTC (10.7K), 2 ID (0.62M to ground), 1 GND</td>
  </tr>

  <tr>
    <td>Carpet sensor</td><td>14.4V (VUSONIC-14V4 boost rail)</td>
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

- Camera (changed Oct 2026): the camera moves off the Compute Module to the STM32 - one parallel-interface (DVP) RGB module, so it also works when an old smartphone is the compute. See [Front sensors module board](#front-sensors-module-board). **Open:** keep the 15-pin MIPI connectors as a Pi-only option, or drop them? The schematic's MIPI-CAMERA sheet predates this change.
- internal USB 2.0 header (JST GH 4-pin, 0.5 A polyfuse, USBLC6 ESD) for the optional mic-array board or `rpiboot`; see [USB, UART allocation](#usb-uart-allocation)
- M.2 slot provisioned, PCIe lane routed, with its own 3.3 V buck (VCC3V3_M2, enabled by the CM via PCIE_PWR_EN) - to experiment with NPU accelerator(s) like Hailo
- SD card slot, powered through an RT9742 load switch (SD_PWR_ON)

Undecided TODO 
- USB-C 3.0+, CM5 only - to experiment with accelerator(s) like Coral TPU
- Keep the compute socket able to take an integrated-NPU module too (Radxa CM5) or premium-upgradeable (CM5 + M.2 Hailo).
- Flag it to the PCB contractor as a design item: M.2 E-key (WiFi) + an M.2 M-key/PCIe (NPU or NVMe), PCIe lane routing, and the thermal path for a few-watt accelerator in a suction-cooled enclosure

### Robot

Current schematic (2026-09):
- charging input is 24 V DC, from the dock contacts (CONTACT_CHGR) or a DC-005 barrel jack, into an SLM6900 buck charger configured for 4S (about 2.2-2.6 A). The battery NTC goes straight to the charger, so over-temperature cut-off is in hardware
- the system rails run from the battery (VBAT-14V4), not from a power-path SYS rail
- USB-C is a 5 V *output* for the phone-as-compute option (AP64501 buck enabled by PWR_EN, through a TMI6240 current-limited switch), with D+/D- to the STM32 USB (PA11/PA12). **TODO:** CC1/CC2 are unconnected; a phone on a C-to-C cable will neither charge nor enumerate until CC is configured (Rp to charge, Rd for the phone-as-host data mode)
- the USB-C PD input and power-path charger below are the original plan, not in the current schematic

Original plan:
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
  - watchdog: see [Safety and power rails](#safety-and-power-rails)

### Dock

- v1 is a **charging-only dock**, [`kicad/charging-dock`](../kicad/charging-dock/README.md) (rev 2, 2026-10-27): 20 V brick, CH32V003 MCU, robot detection by resistance signature, soft-start output switch with current sense, NEC IR beacon
- the dock has only 2 contacts: DOCK+ and GND
  - DOCK+ is the 20 V brick voltage (the robot needs 18.5-22 V)
  - the dock measures the resistance across the contacts and energizes DOCK+ only when it sees the robot's signature (after a couple of seconds); it switches off when the charging current stops
  - dock contacts are spring loaded, gold-coated pogo pins ≥4 A, placed rear-vertical, above water line
- full dock (later):
  - powered from an external certified DC brick (~200–350 W); use an external brick for safety, so the dock enclosure only ever sees low-voltage DC
  - reuse a 25.2 V stick-vac motor for auto-empty, e.g. Dreame M10-E-4 25.2 V/310 W; with a 24/25.2 V brick, the dock must still make 20 V for the contacts
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
- **v1 front receivers (2026-10-27 to 2026-11-11, on the main board): Everlight IRM-V838M3-C/TR1**, C3291489, ~$0.20, ~97k in stock, SMD 6.6×3 mm, side-looking: the lenses are on the long face opposite the pins, lens axis 1.8 mm above the board, ±45°. [Datasheet](https://www.everlighteurope.com/custom/files/datasheets/DMO-0000605.pdf). Pins: 1 GND, 2 VCC, 3 OUT, 4 GND; filter 47-220 Ω + ≥ 2.2 µF (v1: 100 Ω + 10 µF)
  - the IRM-H638T is top-looking (the lens faces up from the board), so it can't look forward from a flat board
  - the 3-pin IRM-V538M3 (same family) is out of stock at JLC; the IRM-3638T is side-looking but through-hole
- **v1 front receivers since 2026-11-11: Everlight IRM-H638T/TR2** (C91447), one on each front ToF board (U2002), next to the VL53L7. The ToF boards stand upright facing forward, so the top-looking receiver looks forward too. Same part as the dock and the side board, so the IRM-V838M3 line is gone. Why: makers will print the bumper in whatever filament they have, and pigmented filament blocks NIR, so the receivers need a bumper opening like the ToF sensors; side by side, one opening (or window) serves both
  - an opaque baffle between the receiver and the VL53L7 (part of the mount or bumper) keeps reflected ToF laser light off the receiver
  - to test on the prototype: decode the dock beacon from across the room while the ToF ranges at its full rate, with and without the window. If the receiver loses range or glitches, firmware ignores IR edges during ToF integration or pauses ranging while it decodes the beacon

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
- 14.4 V DC stabilized (VUSONIC-14V4, MT3608 boost from 5 V; not the 4S battery directly)
  - DC voltage set by the MT3608 feedback divider: VUSONIC-14V4 = 0.6 V x (1 + R160/R159) = 0.6 x (1 + 232k/10k) ≈ 14.5 V
  - current consumption - calculate 300KHz driving 1300±20% pF per sensor spec
  - make it withstand shorts
- connect sensor analog I/O to MCU ADC input
- use STM32G473VCT6 internal op-amp as echo input (AC via a cap)
- clamp amplitude to 3.3V (back-to-back clamp diodes)
- add a series resistor to STM32 op-amp input (extra protection against 12V)
- (firmware) bias the MCU internal op-amp to Vref/2 using MCU internal DAC
- (firmware) configure ADC pre-amp gain, PGA mode (op-amp bandwidth is 10MHz)
- (firmware) configure op-amp to output signal to internal ADC channel
- drive sensor analog I/O with one low-side N-FET (Q18, AO3400) and a 330 Ω 1206 pull-up (R185) from VUSONIC-14V4, AC-coupled to the piezo through C18
  - the earlier P/N half-bridge was dropped: its high side turned off through a 100k pull-up, far too slow at 290 kHz, so both FETs would conduct every cycle (shoot-through)
  - one GPIO (LO) drives the gate through R60 (10 Ω); R186 (100k) pulls the gate low so the FET is off while the MCU is in reset or being flashed
  - the freed HI GPIO now enables the motor rail (~VMOT-14V4-EN)
- (firmware) drive the sensor in short bursts only: LO held high puts ~0.63 W into R185
  - v1 board: C174 (100 nF) AC-couples LO to the gate, so a stuck-high LO turns Q18 off within ~10 ms (through R186)
- (firmware) release LO (low), then measure using ADC, calculate return amplitude
- TODO get the sensor vendor's reference driver circuit to confirm drive voltage and pull-up value

## LiDAR pinouts

On the main board (current schematic):
- LIDAR1: JST GH 1.25 mm socket for the LDROBOT LD14P: 1 MOTOR-CTRL (PC2 through R183), 2 GND, 3 LiDAR TX (to PD2 through R113), 4 VLIDAR-5V
- J3 (v1; LIDAR2 until 2026-11-13): 2x3 0.1" right-angle header, fitted since 2026-11-13 (not fitted before) (XFCN PZ254R-12-06P-A40, C45384673, since 2026-11-11; 1x6 PZ254R-11-06P from 2026-11-03; a vertical header plus the cable on top would be too tall). The 2x3 takes 7.6 mm of board edge instead of 15.2 mm; odd pins are in one row, even pins in the other, so it takes a 2x3 Dupont housing or single Dupont leads, not a 1x6 housing. For other 2D LiDARs: 1 VLIDAR-5V, 2 VLIDAR-5V, 3 GND, 4 MOT- (low-side switched by Q20), 5 LiDAR TX (shared with LIDAR1 pin 3), 6 LiDAR RX (from PC12 through R66). A LiDAR that doesn't drive its own motor gets it between pins 1/2 (+) and 4 (MOT-). It was 2x3 unfitted pads (2026-10-29) with a different pin order. Connect only one LiDAR: to LIDAR1 or to J3.
- R66, R113, R183 are 100 Ω series resistors (v1, 2026-10-29; R183/R113 were 1k, R117 is gone). At 100 Ω they no longer stop the MCU from back-powering an unpowered LiDAR through its inputs, so firmware drives PC2 and PC12 low (or makes them inputs) whenever the LiDAR rail is off.
- both are powered from VLIDAR-5V, which cuts the whole LiDAR (laser included), not just its motor; see [Safety and power rails](#safety-and-power-rails)

```
X-WPFTB-V2.6.2 PCB marking - JST GH 1.25mm 4-pin shrouded housing

D-WPFTBCD-V1.0.1 PCB marking - JST GH 1.25mm 4-pin shrouded housing

LDROBOT LD14P lookalike - JST GH 1.25mm 4-pin shrouded housing

Mystery mini - JST GH 1.25mm 5-pin shrouded housing
```

## Front sensors module board

- 2x VL53L7CH (or VL53L7CX), 90° diagonal = ~63° horizontal FoV each
  - each turned ~30° left, right to cover ~126° horizontal FoV
  - JLC, 2026-10-27: VL53L7CH C19183986 $11.46, 2 in stock; VL53L7CX C5270520 $8.46, 77 in stock; VL53L5CX C3178303 $4.81, 3.8k in stock (same footprint and pinout, but 63° diagonal / 45° horizontal). Two per robot, so this is a large BOM line. **Decided:** the sensor is bought from a distributor (DigiKey VL53L7CX $6.06 at 1,000, Mouser $5.17 at 3,600, ST VL53L7CH $5.63 at 500) and placed by hand; JLC assembles the rest of the ToF board. See the [ToF board README](../kicad/front-sensors/README.md#assembly-the-sensor-is-placed-by-hand)
  - obstacle *detection*
- 1x RGB camera, parallel (DVP) interface, wide-angle, pitched down (changed Oct 2026 from
  2x OV5647 NIR stereo with structured illumination)
  - images the floor - dirty or clean, and cleaning results - and obstacles ahead, up to about
    the robot's height (privacy)
  - obstacle *recognition*; colour helps, and RGB modules are cheaper with more lens choice than NIR
  - non-MIPI and low bandwidth, read by the STM32, so it works with both a Pi CM and an old
    smartphone over USB CDC; this rules out full ToF cameras, stereo depth and structured light
  - **Open question:** the STM32G473 has **no DCMI** (camera interface) peripheral. Options:
    GPIO capture with timer-triggered DMA at low resolution; a module with its own SPI/FIFO
    buffer (ArduCAM-style); or a small bridge MCU with a camera interface
  - **Tentative:** a Raspberry Pi Pico-class MCU (RP2040, or RP2350) as the camera bridge. Its PIO
    blocks capture a DVP camera well (community OV7670/OV2640 examples exist); frames then go to
    the STM32 over SPI or UART
    - RP2040/RP2350 are QFN only, against the hand-solderable preference. A castellated module
      (Pico-style, or a smaller RP2040 board) keeps it hand-solderable and brings its own flash and
      crystal
    - bandwidth: the STM32's USB FS (12 Mbit/s) to a phone carries raw QVGA RGB565 (150 kB a
      frame) at only a few fps; a camera with hardware JPEG (e.g. OV2640) or a lower resolution
      eases this
- white torchlight LEDs for the camera (was NIR illumination with a projection pattern); many
  consumer robots use white, e.g. Dreame L60 Ultra PE and Roomba j7
- v1 (changed 2026-10-27): the dock-homing IR receivers move onto the main board, which sits at the very front of the robot anyway (some consumer robots do the same)
  - 2x IRM-V838M3-C (side-looking), U24 left and U25 right, at the board's front edge with a baffle between them, until 2026-11-11. Since then one IRM-H638T on each front ToF board (U2002), aimed 30° left or right with its ToF sensor: see [IR receiver ICs](#ir-receiver-ics)
  - two receivers, not one: when both see the dock it is straight ahead, when one does, steer to that side. With the dock's left and right codes, the robot knows both which way the dock is and which side of the dock it's on. One receiver only sees the dock or not, so it would have to turn and sweep to find the bearing
- the ToF sensors are on small boards, one design fitted twice: [`kicad/front-sensors`](../kicad/front-sensors/README.md)
  - left board aimed 30° left, right board 30° right
  - board-to-board since 2026-11-06, no cable: each ToF board hangs upright under the main board, sensor on its front face, a 2.0 mm 2x4 right-angle header (HanElectricity 2005WR-2x4P, C6837622) on its back, plugged into a 2x4 vertical socket (2005FV-2x4P, C18723066) on the main board's underside (J6 / J5); a mount screwed to the main board holds it. The mating swaps the rows, so header pin n meets socket pin n+1 / n-1: see the [front ToF README](../kicad/front-sensors/README.md#connector-j2001)
- RGB camera with white torchlight LEDs: not in v1, no board yet

## Side sensors module board

- **v1 (decided 2026-10-27): VL53L0X + IRM-H638T** on [`kicad/side-sensors`](../kicad/side-sensors/README.md), right side only, JST SH 7-pin (ZX-SH1.0-7PWT), assembled at JLC
  - VL53L0X (C91199, ~$1.63) over the VL53L4CD (~$2.07) to save cost; it is weak below ~3 cm, so the board is slightly recessed. The VL6180 is NRND/obsolete and needs 2.8 V I/O
  - IRM-H638T (top-looking, same part as the dock's U1202) replaces the TSOP38238: it catches the dock's beacon while driving past or wall-following, without stopping to spin, and helps when there is no map yet
- earlier notes:
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
- powered from VCC-5V-REG through Q8 (AO3401 high-side switch) as rail VM-5V-WATER-PUMP; on only while WD_OK is high AND WATER-PUMPU-CTRL is low (Q7004)
- the pump-side voltage is read by the STM32 ADC (WATER-PUMP-SENSE-ADC divider R81/R47)
- supply is fixed at 5 V (the old "settable by resistors" idea isn't in the schematic)

## GPIO

Please see the [PCB schematic](https://github.com/makerspet/oomwoo-pcb/tree/main/kicad/PDF) for up-to-date GPIO list.

TODO before layout/fabrication: confirm whether GPIO entries 36 and 46 are intentionally separate bumper inputs or a duplicate label.

Carpet sensor notes (see [How to drive carpet sensor](#how-to-drive-carpet-sensor) for the driver)
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

Design (current schematic)
- CM console: 0.1" 1x5 header (CM_CONSOLE1), TTL-234X-3V3 cable compatible. (A 3-pin JST-SH like the Pi 5 debug connector was considered and not used.)
  - The STM32 link uses a separate UART; the CM4 has UART2–5 available through device-tree overlays.
- STM32 debug: 0.1" 1x6 UART header (J4, STM32_DEBUG1 until 2026-11-13; TTL-234X-3V3 cable pinout: 1 GND, 4 cable TXD → STM32-RX, 5 cable RXD ← STM32-TX; 2 CTS#, 3 VCC, 6 RTS# not connected) and a 1.27 mm 2x7 STDC14 header (JTAG1) for an STLINK-V3MINIE. STDC14 pin 3 (T_VCC) is a sense input; pin 11 (GNDDetect) is not connected.
- The CM reflashes the STM32 itself (STM32 UART bootloader via BOOT0/NRST from CM GPIOs, or SWD over CM GPIOs), so normal firmware updates need no probe.
- One internal USB header, for example a 4-pin JST-GH, wired to the CM4's USB 2.0 pins.
  - Normal use: the mic board plugs in here. Or makers can plug in a USB hub, a USB stick, or a USB-audio or ReSpeaker-style array; it's their choice.
  - Flashing: unplug the mic board, set the boot jumper (nRPIBOOT), and connect a JST-GH-to-USB-A adapter cable to the PC.
  - Power (VBUS): feed the header's 5 V from the carrier through a polyfuse. Leave VBUS unconnected in the flashing adapter cable so the PC and the robot never feed power into each other; the robot powers itself while flashing. It's worth checking the CM4 datasheet for whether `rpiboot` needs to sense VBUS.
- Host mode on CM4: the CM4's USB port is off by default. Add `[cm4]` then `otg_mode=1` in `config.txt`. That turns it on in host mode using the Pi's XHCI controller, which handles USB audio better than the older `dwc2` controller. The boot ROM still enters flashing mode when the nRPIBOOT jumper is set.
- CM5: use the same header and the same mic board, so there's one design for both modules. The CM5's extra USB 3 ports stay free for whatever makers want.
- The mic board is USB full-speed (12 Mbit/s), which puts little load on the port.

## Phone-compute board (v1)

The first board drops the Raspberry Pi: an Android phone is the compute, talking to the STM32 over USB-C (CDC). Schematic: [`kicad/main-phone`](../kicad/main-phone/README.md), forked from `kicad/main` (the Pi carrier stays for later).

- dropped: CM4/CM5, SD card, M.2 + its buck, MIPI cameras, speaker amp (no buzzer; LEDs for debug), water pump, front illumination, the phone's dedicated 5 V buck, the board fan (the phone stays cool), the left side-proximity sensor (OOMWOO One has a right one only)
- kept: the IMU (gyro heading on the STM32 clock, ~$1.40); no Bluetooth/Wi-Fi in v1 (an iPhone would need one, since iOS apps can't use USB CDC)
- the six mounting standoffs (MP1-MP6) moved from the removed M.2 sheet to the POWER sheet
- spare STM32 pins (2026-10-28): PA8 (battery sense since 2026-11-02), PA9 (swapped with PE10 on 2026-11-03: PE10 is the spare now), PA10 (right bumper LED since 2026-11-03), PC10, PC11, PD4, PE2, PE6, all on J1 (J7301 until 2026-10-30) (PD9/PE8 were freed too, then went to cliff sensors 5 and 6; PC8/PC9 to the rear docking IR board; PE4/PE5 to the Hall boards); PC10/PC11 form a spare UART (UART4 or USART3). Freed by:
  - the LiDAR rail enable joined ~VMOT-14V4-EN (PE10, PA9 since 2026-11-03): the LiDAR is on whenever the motor rail is (PD9 freed)
  - IMU FSYNC and INT2 left the MCU (PD4, PD7 freed); FSYNC keeps a 100k pull-down (R211). The IMU is leadless: probe INT2 on its 10k pull-up R92 (test pad TP1 removed 2026-11-02) and FSYNC on R211. AP_AD0 is pulled low by R217 (10k), so the IMU answers at I2C address 0x68; probe AD0 on R217. Run a wire to a spare pin if INT2 or FSYNC is needed
  - one shared open-drain sensor interrupt (~{INT-SENSORS}, PD12, active low) for both VL53L7s and the side VL53L0X (PC8, PE2 freed). Since 2026-11-11 it serves only the side VL53L0X: the VL53L7 INT pins are not connected to the main board (firmware polls the sensors; each front board brings INT out to test pad TP2001), and their connector pin carries the IR receiver instead
  - only the left VL53L7 LPn on the MCU; the right one is held up by R196 (PE8 freed). Addressing uses the left LPn plus the side sensor's XSHUT
  - the IMU moved from I2C2 to I2C4; its own pull-ups R18/R72 are not fitted (PA8, PA9 freed). PA9 is also the UCPD dead-battery control for CC1. Since 2026-11-03 PA9 carries ~VMOT-14V4-EN, and one 10k pull-up (R184) holds it high in reset for both jobs: motor rail and LiDAR off, dead-battery Rd on CC1 on. R204 (the old PA9 pull-up) and R182 (a second 100k on the enable, left from the separate LiDAR enable) are removed; R184 was 100k. The spare on J1 pin 8 is PE10 instead, with no pull-up, and it has an ADC input (ADC3/4/5_IN14)
  - PWR_EN moved from PC10 to PD7, freeing the PC10/PC11 UART pair
  - SWO (PB3) on JTAG1 counts as a spare when not tracing; the cliff and bumper LED enables stay separate (cliff LEDs may be modulated, bumper LEDs stay on)
- firmware pin map and rules: [firmware spec](https://github.com/makerspet/oomwoo-firmware/blob/main/docs/SPEC.md)
- USB-C: the phone is the USB host (the STM32G4 USB is device-only). CC1/CC2 go to the STM32 UCPD (PB6/PB4): Rd by default, so the phone becomes host and source; a PD power-role swap lets the robot charge the phone while it stays host (phone support varies; phones without it alternate charging and data)
- the TMI6240 has no reverse-current blocking (body diode VOUT→VIN), so Q27 (AO3401) + Q28 (AO3400) disconnect the robot 5 V from VBUS_5V unless USB_PWR_EN is high
- VBUS lockout: USB_PWR_EN (PD7; PWR_EN until 2026-11-08) reaches the TMI6240 and Q28 only through R201 (10k) as PWR_EN_G. Q33 holds PWR_EN_G low while VBUS is above ~1.3-2.9 V (R202/R203 halve VBUS), so the robot can't drive VBUS against a phone that is already sourcing it (the TMI6240 would otherwise push up to 4 A into it). Once PWR_EN_G is high, Q34 keeps Q33 off, so the robot's own 5 V on VBUS doesn't lock it out. PD power-role swaps still work: the phone drops VBUS first, then the robot's 5 V comes on.
- VBUS sense: 100k/47k divider to PA7
- front ToF moved from the Pi to the STM32 (I2C4 + 5 GPIOs); STM32 firmware forwards ToF, LiDAR and sensor data to the phone over USB
- STM32 firmware updates from the phone: jump to the built-in USB DFU bootloader
- spare I/O header J1 (2026-10-30; was J7301, 2x11 pads): 0.1" 2x6 right-angle pin header, fitted (XFCN PZ254R-12-12P, C492434, since 2026-11-10; was the vertical PZ254V-12-12P; 2x7 until 2026-11-02). Right angle so an accessory inside the enclosure, such as a WS2812B floor-light strip, can plug in from the side. Not shrouded (a box header is ~9 mm tall and costs more), so the PCB engineer marks 3.3 V, 5 V and GND prominently on the silkscreen next to the pins. Place it at a board edge with room for the plug and cable. Spares only: 1 VMCU-3V3 (MCU rail since 2026-11-02, like the GPIOs), 2 VSENS-5V-USB, 3/4 UART PC10 TX / PC11 RX, 5 PF0 (ADC1_IN10; free since the HSE crystal went, 2026-11-04), 6 PE6, 7 PF1 (ADC2_IN10), 8 PE10 (ADC capable; was PA9 until 2026-11-03), 9 PD4, 10 PE2, 11/12 GND. No I2C: I2C4 runs at 1 MHz and is shared with the ToF, side sensor and IMU. Pin 2 is the shared 5 V sensor/USB rail, so keep accessory current low (a WS2812B draws up to ~60 mA at full white). WS2812B data wants a 3.5 V high at 5 V supply, above the 3.3 V GPIOs: put a level shifter (e.g. 74AHCT1G125) in the accessory cable
- sensor rail switch (2026-11-01): one AO3401 (Q16) from VMCU-3V3 to VSENS-3V3. PB10 (~VSENS_3V3_EN, low = on) drives the gate through R195 (10k); R90 (100k) holds it off while the MCU is in reset. C64 (100 nF, gate-drain) gives a ~2 ms soft start, so the sensor rail's ~40 µF doesn't pull VMCU-3V3 down; C176 (1 µF, gate-source) keeps Q16 off while VMCU-3V3 ramps up at power-on. Turn-on takes ~4 ms delay + ~2 ms ramp. Removed: Q17 and R91 (the rail draws a few hundred mA at most), the gate resistors R96/R97, and D39, which back-fed the "off" rail from the gate pull-up
- VL-R-LPn has a 47k pull-up (R196) and no MCU pin, so the right VL53L7 is always enabled. The main board holds every ToF resistor (I2C 2.2k, the INT 47k R2 (R61 until 2026-11-11), the right LPn 47k R196); the MCU drives the left LPn (PB13) and I2C_RST (PC0) with no resistors (R62 and the old R2 removed 2026-11-04: the sensor rail is off whenever those pins float); the ToF boards carry none, so the bus isn't pulled up twice
- front IR receivers: on the main board from 2026-10-27 (U24 left, U25 right, IRM-V838M3-C, side-looking; they replaced the IR-F1/IR-F2 connectors), on the front ToF boards since 2026-11-11 (U2002, IRM-H638T). IR-F-L → PE15 (J6 pin 6), IR-F-R → PB11 (J5 pin 6) (IR-F-RX1/IR-F-RX2 until 2026-11-11), both direct (R80 removed 2026-11-04)
- no HSE crystal (X1, C34, C35 removed 2026-11-04): USB runs crystal-less on HSI48 trimmed by the CRS to the phone's USB SOF, the system clock comes from HSI16 through the PLL; PF0/PF1 are unconnected. The RTC keeps its 32.768 kHz crystal (X3)
- J6 / J5 (VL-L1 / VL-R1 until 2026-11-13): 2.0 mm 2x4 vertical sockets (HanElectricity 2005FV-2x4P, C18723066) on the underside since 2026-11-06 (JST SH 7-pin ZX-SH1.0-7PWT before, ZH 1.5 mm before that): 1 GND, 2 VSENS-3V3, 3 SCL, 4 SDA, 5 VL-I2C-RESET, 6 IR-F-L / IR-F-R (the board's IR receiver; ~INT-SENSORS until 2026-11-11), 7 GND, 8 LPn

### Power control (v1)

- Power-on: the button pulls the Q13 (AO4407C) gate low through C14, Q13 feeds VMCU-3V3-POWER-EN and the U21 3.3 V buck turns on the MCU rail. Once the rail is up, R172 (10k from PWR-LATCH to VMCU-3V3) turns Q23 on, and Q23 holds Q13 on: the latch holds itself in hardware, so a blank or crashed MCU stays powered (useful for the first flash). Firmware only turns power off, by driving STM-PWR-CTRL (PA15 → R190 1k → PWR-LATCH) low, which puts the Q23 gate at ~0.3 V. On a blank STM32G4, PA15 comes out of reset as JTDI with its internal pull-up, so it doesn't fight R172. Power-on starts only the MCU rail; firmware enables the other rails.
  - C2 (10 µF, PWR-LATCH to GND; 10k x 10 µF = 100 ms, since 2026-11-13) stops a firmware "off" from turning itself back on. Without it, the MCU releases PA15 when the falling rail reaches its ~1.7 V reset level, while R172 still pulls the Q23 gate up to that falling rail (above the AO3400's 0.65-1.45 V threshold), which could turn Q13 back on. With C2, PA15 holds the gate at 0 V until reset, and R172 then charges C2 too slowly for the gate to reach the threshold before the rail is gone (~50 ms below 0.65 V). Turn-on still works: firmware charges C2 through R190 in ms; a blank MCU relies on R172 alone, ~60 ms to 1.45 V, well inside the ~0.25 s a button press holds Q13 on (C14 + C22 through R171). Q30 (the off timer) discharges C2 directly
  - to check at bring-up: scope VMCU-3V3 and PWR-SW-G during a firmware off (the rail must not come back) and a blank-MCU power-on (the rail must stay on); tune C2 if needed
- Off: firmware turns everything off after a 3 s press (all rails first, then PA15 low). 3 s while holding Home = factory reset, and the robot stays on.
- Hardware off timer: holding the button ~3.5-9.5 s turns the MCU rail off even if the firmware hangs. Q29 releases C172 (10 µF, charged through R193 1M, ~10 s time constant), and Q30, gated straight from C172, pulls the latch gate (PWR-LATCH) low once C172 passes Q30's threshold (~1-2 V across AO3400 parts). Q30 turns on over ~1 s rather than snapping; that's harmless because Q13 only drives U21 EN through R207/R208 (EN has hysteresis), and the latch lets go on its own once VMCU-3V3 starts falling. Until 2026-11-13 a 74LVC1G17 Schmitt buffer (U23, with C173) drove the Q30 gate (~4.5-9 s); it was removed to save a BOM line. R190 lets Q30 win against PA15 driven high (or against R172 alone).
- Charger rail-hold: DC-IN-20V (dock or barrel jack) turns Q31 on through the R175/R194 divider, which pulls the Q13 gate (PWR-SW-G) low. Charger power alone turns the MCU rail on, and nothing turns it off while charging (the off timer can't either).
- MCU rail off → every MCU pin floats → every other rail is held off by its enable pull resistor.
- Charging is in hardware (SLM6900 + battery NTC) and continues while the MCU is in reset.
- Charge current: 1.2 A since 2026-11-09, set by R106 (I = 0.12 V / R106, now 100 mΩ, RE1206F1R100, C46961734; was 50 mΩ, 2.4 A). It is low on purpose, because the first packs are no-name ones; about 5 h for a 5.2 Ah pack. Packs from a legitimate manufacturer could take more (1.8 A = 67 mΩ). Expected dock current at 20 V: ~1.1 A charging, ~2 A with the MCU on and the phone charging at 10-15 W

### DC input (v1)

- 20 V brick, through the dock contacts or the barrel jack. While charging, Q14 disconnects the battery from VBAT-14V4 and D14 feeds VBAT-14V4 from DC-IN-20V (DC-IN-20V - 0.4 V); the SLM6900's 95% maximum duty needs ≥ ~18.5 V to finish a 4S charge.
- Keep DC-IN-20V ≤ 22 V: SMAJ22A TVS (D41, C353464; not SMAJ18A, which can start conducting at 20 V. JLC has no footprint or 3D model for it yet, so its symbol borrows the SMAJ18A's SMA footprint), and the rail-hold puts the full VBAT-14V4 across Q13's gate (AO4407C, Vgs ±25 V). DC-IN-20V capacitors are 10 µF/50 V 1206 (C13585); a 10 µF/25 V 0603 keeps only ~1 µF at 20 V.
- Barrel jack: DC-044A-20A (C129006), 5.5/2.0 mm, 30 V 5 A, 7.2 mm tall (the DC-005 was 11 mm). Its switch pin disconnects the dock contacts' GND while a plug is in, so the two sources never fight.
- battery sense (2026-11-02): R218 (1M) / R219 (100k) + C177 (100 nF) from P+/C+14V4 (the battery side of Q14, after F1) to PA8 (ADC5_IN1), V_bat = V_adc x 11 (16.8 V reads 1.53 V). Not VBAT-14V4: while charging, Q14 disconnects the battery and D14 feeds VBAT-14V4 from DC-IN-20V. Always connected: ~15 µA from the battery, and ~16 µA into PA8 through its clamp diode while the MCU is off (far below the injection limit)
- DC-IN-20V sense: R199 (1M) / R200 (100k) + C175 (100 nF) to PB15 (ADC4_IN5), DC-IN-20V = V_adc x 11 (20 V reads ~1.82 V; 3.3 V full scale is 36 V). The MCU sees charger power on either input.
- Dock presence signature: ~130k from DC-IN-20V to GND (R175 + R194 = 147k in parallel with the 1.1M sense divider), plus ~30 µF of DC-IN-20V capacitance. The [charging dock](../kicad/charging-dock/README.md) measures both with a ~1.5 V probe (too low to turn Q31 on), then ramps 20 V onto its contact through a soft-start switch. Changing R175, R194, R199, R200 or the DC-IN-20V capacitors changes the signature: update the dock firmware window too.

### Bumpers (v1)

- 2x ITR9606 slotted photo-interrupters on the main board (BUMP-R1, BUMP-L1). The Roomba harness (BUMP_CLIFF1) and its backup bumpers are gone since 2026-10-28.
- ITR9606 emitters, each on its own switch since 2026-11-03 (they were in series on Q32 with R197 at 120 Ω). High = on, and both are pulled low in reset:
  - BUMP-R1: R197 (180 Ω, ~21 mA) from VSENS-5V-USB; Q36 (AO3400) switches BUMP-R-LED-K from BUMP_R_LED_EN (PA10, TIM1_CH3, R221 100k pull-up to VMCU-3V3 since 2026-11-05: PA10 is also UCPD DBCC2, so the dead-battery Rd sits on both CC1 and CC2 in reset and the phone attaches in either plug orientation; the LED stays dark because VSENS-5V-USB is off whenever the MCU pins float)
  - BUMP-L1: R220 (180 Ω) from VSENS-5V-USB; Q32 switches BUMP-L-LED-K from BUMP_L_LED_EN (PC3, TIM1_CH4; no pull-down since 2026-11-05, same reason)
  - why: firmware can PWM each emitter (~100-250 kHz, well above the detector's ~15 µs response) to bring each detector's clear-slot level into range, since IC(ON) varies 0.5-10 mA between parts. C178/C179 (47 nF) on BUMP-R/L filter the PWM ripple (47 µs with the 1k pull-ups); bumper transitions take milliseconds
- Detectors pull BUMP-L (PA4, ADC2_IN17) / BUMP-R (PA5, ADC2_IN13) low when light passes the slot. R48/R44 are 1k (47k until 2026-11-02) so firmware can sample them as analog and see how fast the flag opens or closes the slot: IC(ON) is 0.5-10 mA (IF 20 mA, VCE 5 V), and at 47k any part bottomed out at 0 V with ~70 µA, i.e. it acted as a switch. At 1k a 0.5 mA part still swings ~0.5 V and a 10 mA part saturates only once the slot is ~1/3 open; calibrate the clear-slot level per unit (LED on vs off through BUMPER_LED_EN)

### Rear docking IR and Hall sensors (v1)

- [Rear docking IR board](../kicad/rear-ir/README.md) on REAR-IR1: two top-looking IRM-H638T, left PC8 (TIM3_CH3), right PC9 (TIM3_CH4). The robot backs into the dock (like a mop or auto-empty dock): LiDAR for the approach, the two receivers for the final alignment.
- Two [Hall sensor boards](../kicad/hall-sensor/README.md) (CC6201ST, omnipolar): dust bin present on J7 (PE4), LiDAR tower bumper on J8 (PE5) (HALL-BIN1 / HALL-TOWER1 until 2026-11-13). Low = magnet near; the MCU's internal pull-ups on PE4/PE5 (R215/R216 removed 2026-11-04; either Hall output type works).
- REAR-IR1 uses the same 4-pin SH vertical connector as the cliff sensors (ZX-SH1.0-4PLT). The Hall boards use the 3-pin one (ZX-SH1.0-3PLT, C7430452; 1 3.3 V, 2 OUT, 3 GND), so a Hall cable can't be plugged into a cliff or rear IR socket (changed 2026-10-29). All three sit on the SIDE-PROXI sheet.
- The mounting pads of every SH socket on the main board go to GND (2026-10-29), as they already did on the sensor boards.

### Cliff sensors (v1)

- Six [cliff sensor boards](../kicad/cliff-sensor/README.md) on CLIFF-LF1, -RF1, -LR1, -RR1, -LM1, -RM1 (ZX-SH1.0-4PLT, SMD vertical): 1 LED anode (VSENS-5V-USB through 150 Ω on the main board), 2 CLIFF-LED-K, 3 phototransistor collector, 4 GND.
- Q35 (AO3400) sinks all six LED cathodes from CLIFF_LED_EN (PC1, high = on; R214 pull-down removed 2026-11-06: the LEDs run from VSENS-5V-USB, which is off whenever PC1 floats); ~25 mA per LED (150 Ω each, R224-R229 on the main board since 2026-11-06; was R4001 on each cliff board), ~150 mA total.
- 47k pull-ups to 3.3 V: R64 LF (PA3), R73 RF (PA1), R53 LR (PA2), R39 RR (PA0), R212 LM (PD9), R213 RM (PE8). LM/RM reach the MCU sheet through global labels.
- The cliff and bumper LED enables stay separate: modulate the cliff LEDs (LED-on minus LED-off cancels ambient light) while the bumper emitters stay on.

DRV8870 inputs: no external pull-downs (R3, R4, R11, R17, R20, R27, R55, R57 removed 2026-11-04). Each IN pin has an internal ~100 kΩ pull-down, and the motor rail is off whenever the MCU pins float (reset, flashing) or the watchdog stops (WD_OK).

### Motor current shunts (v1, 2026-10-29)

The DRV8870s limit current at I = VREF / (10 × R_ISEN), with VREF tied to 3.3 V. At that limit the old 0.5 W shunts ran at 73-99 % of their rating, so they moved up a size:

| Shunt | Motor | Part | Limit | Power at limit |
| --- | --- | --- | --- | --- |
| R15, R65 | wheels | 250 mΩ 1 W 1206, RLH12FTCR250 (C22464902) | 1.32 A | 0.44 W |
| R83 | side brush | 300 mΩ 1 W 1206, RLH12FTCR300 (C22464904) | 1.10 A | 0.36 W |
| R84 | main brush | 110 mΩ 2 W 2512, LRBK25EFER110 (C5121166) | 3.0 A | 0.99 W |

The shunt only carries current while the driver drives, not while it chops, so a stalled motor heats it less than the table shows. Firmware still stops a motor on sustained overcurrent (ADC on each shunt).

### Main fan connectors (v1, 2026-11-03)

One connector (VMOT-14V4, GND, MAIN-FAN-FB on PE9, MAIN-FAN-PWM on PD1). Fans with other connectors get an adapter cable (some Dreame MX fans are sold without a cable anyway). MAIN_FAN2 (PA 5 / PH 5 / PH 4 footprint), MAIN_FAN3 (PA 6) and the fan ID input (PE10) were tried on 2026-11-03 and removed the same day to keep the board simple:
- MAIN_FAN1, fitted: Micro-Fit 3.0 compatible 1x4 right angle, Lian Xin XDWF-C3030WR-1*4P (C50399536, ~$0.09, 5 A per contact, ~5.5 mm tall; the Molex 43650-0400, C277684, 8.5 A, ~$0.30, also fits): 1 VCC, 2 GND, 3 PWM, 4 FG, matching the Dreame L60 Ultra PE main board. A 1x4 because Dreame fans with a 2x2 MX plug often come with a 2x2-to-1x4 cable for a right-angle 1x4 board header, so those cables can be reused (the fan's 2x2 end is 1 VCC, 2 GND, 3 FG, 4 PWM; the cable maps it to the 1x4 order). History, 2026-11-03: vertical 2x2 (9.9 mm plus the plug and cable on top, too tall), then right-angle 2x2, then this 1x4. Place it with room for the plug and cable on the mating side. Stock is low for the clones (~600 Lian Xin, ~1.5k Molex at JLC); check before a production order. MSD-G fan (Dreame X50 Ultra / Master, 20 kPa, 4.2 A at 14.4 V, 6 A blocked at 16.8 V: over the clone's 5 A, so firmware stops a stalled fan by FG). Footprint JLCImport:CONN-TH_4P-P3.00_L8.9-W15.7-EH4.7, JLC's own for the Molex 43650-0400 (since 2026-11-04; the Lian Xin's JLC footprint is mirrored, so it isn't used). Vendor drawings disagree on which end is pin 1, so check the silkscreen pin 1 against the header's cavity keying on the first board
- the motor rail switch has two AO4407C in parallel (Q1, Q2 (Q37 until 2026-11-13), 10 Ω gate resistors R36/R222 from VMOT-SW-G) for the higher fan current: ~7.5 A normal is ~0.25 W in each
- the PCB engineer sizes the fan traces for ~6 A
- blowers are limited to the 20 kPa class (decided 2026-11-07): Dreame MSD-G or MSD-J, both with Micro-Fit plugs. The whole robot current (~7.5 A normal with the MSD-G) runs through J2's single P+ and GND contacts (8.5 A rated; the Roborock pack has one of each). A stronger blower would need a battery connector with doubled power pins
- Q14 is in series with all battery current when off the dock. It was an AOD407 (68 mΩ: ~2 W at 5 A, ~4-5 W at 7.5 A); since 2026-11-03 it is two AO4407C in parallel (Q14, Q38), ~0.22 W each at 7.5 A. Gate = DC-IN-20V, S = VBAT-14V4, D = P+/C+14V4 as before. Vds: about -10 V while charging, up to ~-24 V in a TVS-clamped plug-in surge; Vgs: up to ~+24 V in that surge (AO4407C: -30 V, ±25 V). Q12 stays AOD407: it is the SLM6900 buck switch, where gate charge matters more than on-resistance
- on the dock Q14/Q38 are off and the whole load runs through D14 (SS56, 5 A): firmware keeps the fan and motors off until DC-IN-20V is gone

### Component height (v1)

Goal: nothing taller than the right-angle wire-to-board connectors and the buck inductors.
- battery connector (J2, BAT2 until 2026-11-09): not on the top side since 2026-11-07. It is a vertical Micro-Fit 3.0 compatible 1x4, CJT C3030WV-4P (C239441, ~$0.26, 8.5 A, ~10 mm; Molex 43650-0415, C293547, uses the same footprint), fitted on the underside and facing down into the battery compartment, as on older Roborocks. Pinout unchanged: 1 P+ (through F1), 2 NTC, 3 ID, 4 GND. It was a Molex 43650-0412 right angle, SMD, 5.57 mm ($0.55)
- barrel jack: DC-044A-20A, 7.2 mm
- J3 (the second LiDAR header, LIDAR2 until 2026-11-13) is a 2x3 0.1" right-angle header (PZ254R-12-06P-A40), fitted
- J1 spare I/O: right-angle 2x6 0.1" header (PZ254R-12-12P, ~5 mm above the board; vertical, ~8.5 mm, until 2026-11-10)
- exception (2026-10-28): the debug headers are vertical so they can be reached from the top under a small removable cover: J4 1x6 0.1" (XFCN PZ254V-11-06P, C492405, ~8.5 mm above the board; 1x6 since 2026-11-02 so the cable socket seats fully) and JTAG1 2x7 1.27 mm SMD (PZ1.27-2x7PTP-L7.2, C55099228, ~7 mm). Same pin numbers as before
- inductors (CYA0630, SMMS0630, XRNR4030): ~3-4 mm
- exception: the ITR9606 bumper sensors (~11 mm), set by the bumper mechanism
- PCB engineer: flag any other part taller than ~7 mm

### BOM consolidation (v1, 2026-10-27)

- every 100 nF is 100nF/50V X7R 0603 (C1591): 4 lines → 1
- every 0603 10 µF rated ≤ 10 V is 10uF/10V (C19702): 2 lines → 1; the 25 V parts stay on ≥ 12 V nets
- 1uF/25V (C14, C22): C380328

### 3.3 V and 5 V bucks (v1, 2026-10-27)

- U21 (VMCU-3V3) and U22 (VSENS-5V-USB) are TPS54560BDDAR (C1850354: 4.5-60 V, 5 A, SO-8 PowerPAD, ~$0.61). The AP64501SP-13 they replace was out of stock (1 left at LCSC). Same 0.8 V reference, so the FB dividers are unchanged.
- Non-synchronous: SS56 catch diodes D42/D43 (SW to GND, same part as D12-D15). Keep the SW node, the diode and the input capacitors in a tight loop.
- fsw 418 kHz: RT R205/R206 = 232k (same part as R160), where the AP64501 soft-start caps were. Soft start is internal.
- Compensation, the same on both rails: R143/R147 4.7k + C112/C120 47 nF (crossover ~20 kHz with ~40 µF effective output capacitance). No high-frequency pole capacitor: the output capacitors are all ceramic, so there is no ESR zero to cancel.
- U21 EN: VMCU-3V3-POWER-EN is the full VBAT-14V4 (up to ~20 V while charging), and EN is rated 8.4 V. R207 (100k) / R208 (22.1k) give 3.6 V at 20 V and an input UVLO of ~6.5 V. U22 EN stays on VSENS_5V_USB_EN (3.3 V logic, R168 100k pull-down).
- VBAT-14V4 input capacitors C95, C106, C115, C116: 10 µF/50 V 1206 (C13585). The 10 µF/25 V 0603 parts kept only ~1 µF at 20 V.
- Cost of the diode: ~1 W at 5 V / 3 A. If efficiency matters later, the synchronous AP64500 (40 V, 5 A, ~$1.04) is the alternative.
- PCB engineer: new footprint (TI DDA, 2.95 x 4.9 mm thermal pad with vias).

## Safety and power rails

Rule: if the STM32 firmware hangs, is held in reset or is being flashed, every motor, the pump and the LiDAR lose power.

Power rails (current schematic):

| Rail | Made by | Feeds | Switched by |
| --- | --- | --- | --- |
| VBAT-14V4 (11.6-16.8 V) | 4S battery | everything below | power-button latch (Q13 AO4407C, STM-PWR-CTRL) |
| VMCU-3V3 | AP64501 buck (U21; TPS54560B on v1) | STM32 | VMCU-3V3-POWER-EN |
| VSENS-3V3 | from VMCU-3V3 via Q16 | sensors, IMU, driver logic | STM32 (~VSENS_3V3_EN, low = on) |
| VMCU-BAT-3V3 | HT7533 LDO | STM32 VBAT (RTC keeps time) | always on |
| VSENS-5V-USB | AP64501 buck (U22; TPS54560B on v1) | CM5, speaker amp, USB header, LiDAR and pump switches, VUSONIC-14V4 boost | STM32 (VSENS_5V_USB_EN) |
| VCC3V3_M2 | AP64501 buck (U24) | M.2 slot | CM (PCIE_PWR_EN) |
| USB-C VBUS 5 V | AP64501 buck (U25) + TMI6240 | phone (phone-as-compute option) | STM32 (USB_PWR_EN) |
| VUSONIC-14V4 (≈ 14.5 V) | MT3608 boost | carpet sensor | with VSENS-5V-USB |
| VMOT-14V4 | VBAT-14V4 via Q1 + Q2 AO4407C (parallel) | wheels, brushes, fan | WD_OK AND ~VMOT-14V4-EN |
| VLIDAR-5V | VSENS-5V-USB via Q25 AO3401 | whole LiDAR, laser included | WD_OK AND ~VMOT-14V4-EN (low = on; the same pin as the motor rail since 2026-10-28) |
| VM-5V-WATER-PUMP | VCC-5V-REG via Q8 AO3401 | water pump | WD_OK AND WATER-PUMPU-CTRL (low = on) |

RC charge-pump watchdog (WATCHDOG sheet):
- the STM32 toggles WDI in software (50-1000 Hz, ~50% duty) from a healthy control loop - never from a timer/PWM, which keeps running after the CPU hangs
- C169 passes only WDI edges to Q24 (AO3401); each falling edge tops up C170 (10 µF) through R178; R179 (10k) bleeds it
- WD_OK ≈ 2.7 V while toggling; WDI stuck high, low or floating → below 1 V in ~100 ms, below 0.4 V in ~190 ms; 0 V at power-up
- the old STWD100 (U3), its OR gate (U4) and the JTAG-presence inverter (Q25) were removed: cutting actuator power is what makes the robot safe
- STM32 recovery: internal IWDG forced on by the hardware option byte (freeze it in debug via DBGMCU); the CM pulses STM32 NRST if the STM32 heartbeat stops

Each gated rail is WD_OK AND an MCU enable, without logic ICs:
- an AO3400 N-FET has its gate on WD_OK and its source on the MCU GPIO; it pulls the rail P-FET's gate low only when WD_OK is high and the GPIO is low
- a 100k pull-up to 3V3 on each GPIO keeps the rail off while the MCU pins float (reset, flashing)
- VMOT-14V4: R165 10k gate pull-up for a fast turn-off; no soft start (a slow turn-off under motor current would overheat Q1). Q1 and Q2 (parallel since 2026-11-03) dissipate ~0.25 W each at ~7.5 A normal (with the MSD-G fan); short ~13 A stall peaks are fine with copper under the drains. TODO measure the fan controller's input capacitance (inrush)
- VM-5V-LIDAR: soft start R181 10k + C171 100 nF (≈1.5 ms on, ≈30 ms off) so the CM's 5 V doesn't dip
- VM-5V-WATER-PUMP: no soft start, so the pump can be PWM-driven
- PWM on an enable can only slow a gate-RC soft start; it can't soft-start a hard-switched FET

MOSFET line-up (consolidated 2026-09, 8 part numbers → 4):

| Role | Part | LCSC | Notes |
| --- | --- | --- | --- |
| all N-FETs | AO3400 (FOSAN) | C20628874 | 30 V, Vgs ±12 V, Vth 0.65-1.5 V, SOT-23 |
| P-FETs whose gate sees ≤ 5 V | AO3401 (FOSAN) | C20628875 | -30 V, Vgs ±12 V, SOT-23 |
| battery-side high-side switches (Q1, Q2, Q13, Q14, Q38) | AO4407C (AOS) | C469397 | -30 V, Vgs ±25 V, 11.5 mΩ, SOIC-8 |
| charger buck switch, DC-IN-20V (Q12) | AOD407 | C6396162 | -60 V for hot-plug margin, low gate charge |

Any gate or drain that can see VBAT-14V4 (up to 16.8 V) needs Vds ≥ 30 V, and a gate swing that large needs Vgs ≥ 20 V.

## TODO

| Type | Qty | Spec |
| --- | --- | --- |
| LiDAR | 1 | 5V 0.35A max (about 1 A at spin-up), Mabuchi-style RF-500TB-14350 or similar; whole LiDAR on the switched VLIDAR-5V rail, motor low-side N-FET (Q20) |
| Main brush | 1 | DC 14.4-15V PRI-390SV-24100, JLS-395PH-2248A, RS-390WM-3107GCF or similar |
| Side brush | 1 | JGA25-310 geared DC motor, 12 V, ~150 RPM, metal gearbox, no encoder; mounted vertically, drives the brush directly via a custom coupler. Runs off the 14.4-16.8 V pack, so PWM-limit to ~12 V average. (Was DC 14.4V RC500-KW/14440/DV in a Roborock-style gearbox assembly; dropped because those assemblies only mate older, non tangle-resistant brushes.) |
| Mop | 2 | GM-RS385Y-24065 or similar, DC 14.4V |
