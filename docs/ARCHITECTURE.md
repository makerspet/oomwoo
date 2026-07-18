# OOMWOO Architecture Brief

> *Status: DRAFT / skeleton.* This document defines the system so that modules
> can be built in parallel without colliding. Sections marked *TBD* are the
> gating decisions; until they are filled in, hardware modules that must fit
> together cannot be finalized. Treat the interface specs as the contract every
> module agrees to.

## 1. Purpose/Goal and scope

OOMWOO is an open-source, 3D-printed, ROS2-based home robot vacuum with 2D LiDAR
and Home Assistant support. It is designed to be *built from scratch by
the community*, module by module, clean well and to double as an affordable ROS2
development and learning platform.

*North star (not MVP):* OOMWOO is also the reference hardware for a broader
robot application platform. Architectural boundaries (especially the app layer in
§6) are drawn with that future in mind, but the MVP below deliberately excludes it.

## 2. Design principles

- *Open and swappable.* Every module has a defined interface. Any compliant
  implementation can replace another. No module depends on the internals of
  another, only on its published interface.
- *Simulation-first.* Software must run in Gazebo before it runs on hardware,
  so contributors with no robot can still build and test.
- *Affordable and printable.* Target off-the-shelf parts (a CM4/CM5-class compute
  module, common vacuum LiDARs, sourced Roborock/Dreame/Xiaomi motors and wear
  parts) and FDM-printable chassis parts.
- *Safety is reviewed, not crowd-trusted.* Battery, charging, and motor-driver
  modules pass a maintainer safety review before merge (see §8).
- *Reference-design backed.* A known-working vacuum (see the references in the
  [README](../README.md)) anchors the geometry and proves feasibility.

## 3. System overview

```
   LiDAR (UART, ~5 Hz) · MIPI camera(s) · IMU · serial audio
                    |
      +-------------v-------------------------------+
      |  CPU - CM4 / CM5 (or pin-compatible module) |
      |  ROS2 · SLAM (slam_toolbox) · Nav2 · behavior |
      |  educational variant: ESP32-S3 + micro-ROS  |
      |  (SLAM offboard on a dev PC over Wi-Fi)      |
      +-------------^----------------+---------------+
       serial (cmds/telemetry) +     |  custom serial protocol
       CPU-reset / health GPIO       |  (NOT micro-ROS)
      +-------------+----------------v---------------+
      |  MCU - STM32G070 (FreeRTOS, static alloc)    |
      |  motors · encoders · sensors · charging ctrl |
      |  SAFETY (no Linux/ROS2): bumper/cliff/wheel- |
      |  drop stop · current limit · CPU watchdog    |
      +-------------+--------------------+-----------+
                    |                    |
         +----------+----+      +--------+---------+
         | L/R drive     |      | suction fan,     |
         | wheels, brush |      | bumper, cliff,   |
         |               |      | IR, wheel-drop   |
         +---------------+      +------------------+

   Power: off-the-shelf 4S2P Li-ion pack (built-in BMS).
   The CPU module + MCU sit on one carrier I/O board.
```

> The CPU/MCU split keeps *all hard safety on the MCU*, independent of Linux/ROS2.
> Interfaces are largely decided (see §5); refine as the io-pcb spec settles.

## 4. Coordinate frames and conventions

- *TBD:* Define `base_link` origin and orientation (REP-103: x-forward,
  y-left, z-up). All mechanical mounting points and URDF frames reference this.
- *TBD:* Define the reference plane (floor contact), robot diameter, and height
  envelope. *These two numbers gate every hardware module.* Source these from the *sourced
  parts* + a 3D-scanned donor (see [source-3d-models](../contributions/source-3d-models));
  the current baseline is a ~349 mm round body ([oomwoo-one URDF](https://github.com/makerspet/oomwoo-one)).
- Units: millimeters, kilograms, SI. Right-handed frames. Angles in radians.

## 5. Hardware architecture

### 5.1 Chassis and reference frame
The chassis is the *integration backbone*. It publishes the mounting interface
every other hardware module targets. Reference geometry (dimensions, wheelbase,
motor specs, mass) comes from the *sourced parts* ([BOM](../BOM.md)) + 3D scans of
a donor vacuum (see [source-3d-models](../contributions/source-3d-models)); the
[oomwoo-one URDF](https://github.com/makerspet/oomwoo-one) carries the current
~349 mm round-body baseline.

- *TBD:* Overall diameter and height budget.
- *TBD:* Mounting grid / bolt pattern standard (e.g., M3 on a defined pitch).
- *TBD:* Mass budget per module and total target mass.

### 5.2 Mechanical interface standard (the contract)
Every hardware module's RFC must specify, against this standard:
- Mounting points (bolt pattern, location relative to `base_link`).
- Bounding envelope (max size the module may occupy).
- Mass budget.
- Mating tolerances and print orientation.
- *TBD:* Define the standard connector/fastener set (screw sizes, heat-set
  inserts, etc.) so parts from different authors actually mate.

### 5.3 Electrical interface standard (the contract)
- *Battery:* off-the-shelf pack with a *built-in BMS* — *4S2P Li-ion*, ~14.4 V
  nominal, ~5200 mAh / ~75 Wh (OEM BRR-2P4S-5200 class), charged 16.8 V CC/CV with
  NTC temperature sense. Chemistry is now decided; see the [BOM](../BOM.md).
- *TBD:* Power rails distributed to modules (VBAT, 5V, 3.3V) and connector types/pinouts.
- *CPU ↔ MCU:* a *custom high-speed serial protocol* (not micro-ROS) carries
  commands/telemetry, plus discrete GPIOs (CPU power on/off, and a CPU-reset line
  the MCU asserts on missed health packets). The *MCU owns motors and sensors*; the
  CPU never drives them directly.
- *Sensors:* bumper/cliff/wheel-drop and analog IR are *MCU-side* (digital in / ADC);
  the *LiDAR (UART, ~5 Hz)*, MIPI camera(s), IMU, and serial audio attach to the *CPU*.

### 5.4 Compute (CPU) and real-time controller (MCU)

OOMWOO splits compute across two processors — mirroring how consumer vacuums are
built, and, crucially, so that *safety never depends on Linux/ROS2*.

*CPU (compute module).* The I/O board is a *carrier* that accepts a *Raspberry Pi
Compute Module 4 or 5* and — because the CM4 pinout is a de-facto standard — the
many *pin-compatible alternative modules* (Radxa CM3/CM4, Pine64 SOQuartz, LuckFox
Core3566, …), several with an *NPU* for future on-device vision. The CPU runs
*ROS2, SLAM (slam_toolbox), Nav2, LiDAR processing, and high-level behavior*. CM
modules are low-profile (helps the height budget) and swappable (hackable, cheaper,
NPU options).
- *Minimum target: a 4 GB CM4/CM5 (or Pi 4).* Realistic prior art runs
  slam_toolbox + Nav2 onboard a 4 GB Pi 4. Getting the floor to *2 GB* is a goal
  (ROS2 composable nodes; selectively rewriting heavy Python nodes in Rust/C++) —
  *no guarantee*, to be settled by the compute-benchmark. No 8–16 GB module needed.
- *Cooling:* no dedicated CPU fan — the suction fan's airflow cools the compute
  board, as in consumer vacuums.
- The earlier bespoke *RK3562* reference schematic is *dropped* in favour of the
  CM4/CM5 carrier.

*MCU (real-time / safety controller).* A dedicated microcontroller — *tentatively
the STM32G070RBT6* (~56 GPIO incl. 16 ADC channels, ~$1 at JLCPCB, LQFP not BGA) —
owns *motors, encoders, all sensors, battery-charging control, and safety*. Its
role is *fixed*: functionality does not migrate onto the CPU, and CPU work does not
migrate onto the MCU.
- Firmware is *tentatively FreeRTOS* (static allocation, watchdog, guaranteed
  reaction times, CE-oriented) speaking a *custom serial protocol — not micro-ROS*
  (the tried-and-true consumer-vacuum approach; cf. the reverse-engineered
  [3irobotix protocol](https://github.com/codetiger/VacuumRobot)).
- *Hard safety lives here, independent of Linux/ROS2:* the MCU stops all motors on
  a *bumper hit, cliff detection, or wheel-drop*, current-limits a *stuck brush*,
  and *watchdogs the CPU* — if the CPU's health packets stop, it stops the motors
  and can *reset the CPU*.
- Tentative ~60-signal pin budget: see the [io-pcb RFC](../contributions/io-pcb)
  appendix (why the MCU needs a high-GPIO part).

*CPU ↔ MCU link.* A *high-speed serial* channel carries commands/telemetry both
ways, plus discrete GPIOs — notably the *CPU-reset* line the MCU asserts on missed
health packets, and CPU power on/off. The draft protocol, ROS2 bridge mapping,
and bringup checklist live in the [io-board-interface RFC](../contributions/io-board-interface).
Any LiDAR supported by `kaiaai/LDS` / `lds2d` is interface-compatible.

### 5.5 Two build profiles

The same carrier I/O board + MCU supports two swappable compute configurations:

| | *Consumer / regular* | *Educational / lower-cost* |
|---|---|---|
| CPU-slot module | CM4 / CM5 (or pin-compatible alt) | *ESP32-S3* board in the CM4 form factor |
| Where ROS2 / SLAM runs | *onboard* (ROS2 + slam_toolbox + Nav2) | *offboard* on a local dev PC; ESP32-S3 runs *micro-ROS* |
| Link | self-contained robot | robot ↔ dev PC over *Wi-Fi* |
| Trade-off | plug-and-play for non-experts | cheaper, but Wi-Fi congestion / dead-zones — a learning platform, not a polished consumer product |

Onboard SLAM is the default for the consumer version *so non-experts can build and
use it* without setting up a separate ROS2 dev machine. The ESP32-S3 can only be
the *CPU-slot* option — it lacks the ~60 GPIO the MCU role needs, so it never
replaces the STM32.

## 6. Software architecture

### 6.1 ROS2 graph (MVP)
- Core nodes (MVP): LiDAR driver, base controller (diff-drive), odometry,
  teleop, SLAM (manual mapping), TF/URDF publisher.
- *Interface contract:* each software module's RFC declares the ROS2 topics,
  services, message types, and parameters it publishes/consumes. Modules depend
  on these interfaces, not on each other's code. See
  [SOFTWARE_INTERFACES.md](SOFTWARE_INTERFACES.md) for the current draft ROS2
  graph contract.

### 6.2 Simulation
- Gazebo + URDF, with a set of residential-layout worlds for navigation and
  coverage testing. Sim parity is a first-class requirement, not an afterthought.

### 6.3 Application layer (Phase 2 — north star, NOT in MVP)
A ROS2-agnostic layer that runs third-party apps locally in isolated *Podman*
containers, so app developers need no ROS2 expertise. Documented here only to
keep its boundary clean; *explicitly out of scope for the Aug 31 MVP.*

## 7. MVP definition (target: 2026-08-31)

*In scope:* ROS2 on a CM4/CM5-class compute module · LiDAR · manual SLAM/mapping · teleop drive ·
3D-printed chassis · Gazebo sim with URDF · evaluation + demo video. No dock,
no autonomous exploration, no Home Assistant, no app layer.

*Explicit non-goals for MVP:* autonomous coverage, docking, auto-empty, mopping,
Home Assistant, the app platform, accessories. These are later phases.

*Critical-path ownership:* the maintainer (+ small core) own the chassis,
interface specs, and integration so the MVP does not depend on volunteer delivery
timing. Community modules accelerate and improve the MVP; they do not block it.

## 8. Safety review gate

Battery, charging, motor-driver, and mains-adjacent modules require maintainer
safety review before merge. RFCs for these modules must include a hazard note
(over-current, thermal, short, mechanical pinch).

The battery risk is *reduced* by using an *off-the-shelf 4S2P Li-ion pack with a
built-in BMS* (over-charge / over-discharge / short protection); the review then
focuses on the *16.8 V CC/CV charging path + NTC temperature sense*. *Hard safety
lives on the MCU, never on Linux/ROS2* — it independently stops motors on
bumper/cliff/wheel-drop, current-limits a stuck brush, and watchdog-resets the CPU.

## 9. Roadmap (phases after MVP)

1. Rechargeable battery + basic dock + autonomous floor mapping.
2. Home Assistant integration.
3. Application layer (Podman app runtime) + first delightful apps.
4. Accessories and novel apps; integrations (e.g., LeRobot arm).

## 10. Open questions

- *Resolved:* the MCU runs a *custom serial protocol (not micro-ROS)*; the CPU runs
  *onboard ROS2/SLAM/Nav2*. micro-ROS is used only in the *educational* ESP32-S3
  profile (SLAM offboard on a dev PC). See §5.4–5.5.
- *Resolved:* battery is an off-the-shelf *4S2P Li-ion pack with a built-in BMS*,
  charged 16.8 V CC/CV. See §5.3, §8.
- Can OOMWOO's onboard ROS2 stack fit in *2 GB* (composable nodes, selective Rust)
  rather than 4 GB? To be answered by the compute-benchmark.
- MCU family: *STM32G070RBT6* is the tentative pick (GPIO/ADC count, ~$1 at JLCPCB,
  LQFP) — open to alternatives.
- One hardware-agnostic HAL covering reference vacuum + DIY builds (community idea)?
- Module selection process: who decides which competing implementation wins, and
  on what criteria? (See each module's acceptance criteria.)
