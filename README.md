<div align="center">

# OOMWOO I/O Board

*Open-source robot vacuum you build yourself.*

STM32G473 MCU · Motor drivers · Sensors · 4S charging · Smartphone compute (v1) · Raspberry Pi CM4/CM5 (planned) · KiCad

![License](https://img.shields.io/badge/License-Apache--2.0-blue)
![Status](https://img.shields.io/badge/Status-Placement-orange)
[![Part of OOMWOO](https://img.shields.io/badge/Part%20of-OOMWOO-5eead4)](https://github.com/makerspet/oomwoo)

</div>

Part of [OOMWOO open-source robot vacuum](https://github.com/makerspet/oomwoo) project.

<img width="1335" height="815" alt="oomwoo_main_pcb_placement" src="https://github.com/user-attachments/assets/967f562d-f45b-44db-834b-56e3c3d44b5e" />

Get [MCU firmware](https://github.com/makerspet/oomwoo-firmware/).

## Two boards

I'm keeping the first board as simple as possible, so it can be built and tested sooner:

- **[`kicad/main-phone`](kicad/main-phone/README.md) - v1, in progress.** An Android phone is the compute, connected to the STM32 over USB-C. No Raspberry Pi, cameras, M.2, SD card, speaker or mopping. The STM32 runs every motor and sensor, including the LiDAR and the front ToF sensors, and forwards their data to the phone.
- **[`kicad/main`](kicad/main) - Raspberry Pi CM4/CM5 carrier, planned.** The Pi is still in the plans: cameras, an NPU and always-on Wi-Fi come with it. The notes below describe this board.

Details for both are in the [I/O board spec](docs/SPEC.md). Each board folder has its schematic as a PDF in `PDF/`, e.g. [the v1 board](kicad/main-phone/PDF/Main.pdf).

The v1 board comes with a **[charging-only dock](kicad/charging-dock/README.md)**: a 20 V brick, a CH32V003 MCU (Arduino core, ch32fun, PlatformIO), robot detection before the contacts go live, and an IR beacon. The plan is to make the v1 board, the dock and the small sensor boards (including the two [front ToF boards](kicad/front-sensors/README.md), one design fitted twice, the [side sensor board](kicad/side-sensors/README.md) six [cliff sensor boards](kicad/cliff-sensor/README.md), the [rear docking IR board](kicad/rear-ir/README.md) and two [Hall sensor boards](kicad/hall-sensor/README.md)) as one panel (V-cuts or mouse bites), so they share parts and cost less to make and ship. Dock reference designators are 8xxx so they don't collide with the main board's.

## Architecture notes

Consumer vacuums typically split compute into CPU and MCU. The MCU ([real examples](https://robotinfo.dev/)) controls
- all motors - driving wheels, suction fan, side brushes, mop motors, mop lift servos, pump and so on
- all sensors except below - IR cliff, IR side proximity, IR docking, wheel drop, bumper (IR or micro-switches), motor encoders, ultrasonic carpet sensor
- all push buttons
- 2D LiDAR motor RPM
- power - battery charging, motors power on/off
- all safety sensors - overcurrent for all motors (cheap vacuums ignore overcurrent sensing)

I/O board also provides audio encoders/decoders, amp, speaker (connector), mics (if any).

CPU receives
- 2D LiDAR data over serial port
- IMU (sometimes IMU gets forwarded via MCU) over SPI/I2C
- cameras (2x MIPI for visual obstacle avoidance)

MCU (and CPU) are usually always active. This allows the user to start cleaning at any time (especially via app remotely). Exceptions:
- no power (battery dead and no dock power)
- user explicitly shut down the vacuum by long-pressing the power button

The MCU's overarching constraint is to ensure robot safety. This is necessary to pass CE mark tests. Here is how MCU ensures safety:
- MCU firmware uses FreeRTOS or similar, static memory allocation, watchdog, guaranteed reaction time
- MCU acts as watchdog for CPU, resets CPU if CPU becomes unresponsive
- MCU connects to CPU over serial using a custom serial protocol ([concrete example](https://github.com/codetiger/VacuumRobot)). No micro-ROS to reduce dependencies, prevent bugs from updated 3rd party libraries slipping into safety-critical MCU firmware.
- MCU shuts down some (or all) motors when MCU detects overcurrent (brush stuck)
- MCU shuts down all motors (including power to all motors) when CPU becomes unresponsive (to prevent CPU sending garbage commands to MCU)
- MCU monitors battery charging, shuts it down when needed (battery too hot)
- MCU stops driving wheel motors when bumper sensors activate
- MCU tests motors, sensors
- MCU does not depend on CPU
- MCU toggles watchdog GPIO; otherwise an external-to-MCU circuit shuts down motor power

Consumer vacuums place CPU and MCU on the same PCB board. Since OOMWOO has to be hackable, it seems best to separate I/O from the compute. Therefore, this I/O board needs to have
- MCU and programming header
  - STM32G473VCT6 (LQFP-100): enough GPIOs, timers and ADCs for every motor and sensor, built-in op-amps for the carpet sensor echo, a USB device port and an RTC, in a hand-solderable package
  - see the [I/O board spec](docs/SPEC.md)
- all vacuum motor drivers (with connectors), driven by the MCU
  - cliff, side proximity, docking, bumper, carpet, water tank full/empty, dust bin present, motor overcurrent, motor encoders
- MCU connected to all sensors (except those handled by CPU like LiDAR serial, MIPI cameras I/O, IMU); sensor connectors
- control circuit for 2D LiDAR's motor (controlled by MCU)
- battery charging, power management (motors power on/off, charging on/off, power shut down), power for CPU compute module (see below)
- push buttons (home, power, etc.) and UI LEDs
- dock connector (dock power, sense dock present)
- USB power for charging; USB for serial shell, etc.
- audio encoder/decoder, audio amp, mics (if any)
- SD card for hacking, cheap large storage
- connect IMU FSYNC to MCU to synchronize MCU timestamps with IMU data streaming to CPU

Consumer vacuums usually don't have a CPU fan/heatsink because the vacuum's suction fan can (indirectly) cool the CPU/MCU PCB. Therefore, no CPU fan on this I/O board.

As far as compute - currently it seems best to use a Raspberry Pi CM4/CM5 compute module. Why?
- CM4/CM5 modules cost a bit less than a full Raspberry Pi 4/5
- CM4/CM5 have lower profile/height vs a full Raspberry Pi 4/5, important to keep vacuum cleaner slim
- there are plenty of 3rd party compute modules pin-compatible with CM4/CM5, making the compute swappable, hackable
  - 3rd party compute modules with NPUs are especially interesting because we need NPU for real-time camera-based obstacle detection

Compute module headers should expose
- 2x MIPI camera I/O
- 1x serial for CPU-MCU comms
- 1x serial for CPU-LiDAR comms
- 1x SPI (or I2C) for CPU-IMU comms
- audio (digital?) I/O
- power from I/O board to CM
- a few TBD GPIOs
  - MCU GPIO to reset CPU

This board should be designed using an open-source PCB tool (KiCad seems like a good choice).

## No manufacturing support

These designs are shared as-is, for reference and for your own work. I don't support manufacturing them: I can't help with ordering (JLCPCB or otherwise), out-of-stock parts, part substitutions, or troubleshooting boards built by others.

## License

[Apache License 2.0](LICENSE).
