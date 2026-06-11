# oomwoo Architecture Brief

> **Status: DRAFT / skeleton.** This document defines the system so that modules
> can be built in parallel without colliding. Sections marked **TBD** are the
> gating decisions; until they are filled in, hardware modules that must fit
> together cannot be finalized. Treat the interface specs as the contract every
> module agrees to.

## 1. Purpose and scope

oomwoo is an open-source, 3D-printed, ROS2-based home robot vacuum with 2D LiDAR
and (later) Home Assistant support. It is designed to be **built from scratch by
the community**, module by module, and to double as an affordable ROS2
development and learning platform.

**North star (not MVP):** oomwoo is also the reference hardware for a broader
robot application platform. Architectural boundaries (especially the app layer in
§6) are drawn with that future in mind, but the MVP below deliberately excludes it.

## 2. Design principles

- **Open and swappable.** Every module has a defined interface. Any compliant
  implementation can replace another. No module depends on the internals of
  another, only on its published interface.
- **Simulation-first.** Software must run in Gazebo before it runs on hardware,
  so contributors with no robot can still build and test.
- **Affordable and printable.** Target off-the-shelf parts (Raspberry Pi 5,
  common LiDARs, hobby motors) and FDM-printable chassis parts.
- **Safety is reviewed, not crowd-trusted.** Battery, charging, and motor-driver
  modules pass a maintainer safety review before merge (see §8).
- **Reference-design backed.** A known-working vacuum (see `docs/references.md`)
  anchors the geometry and proves feasibility.

## 3. System overview

```
            ┌─────────────────────────────────────────────┐
            │                  Compute (RPi 5)             │
            │   ROS2 graph  ·  SLAM  ·  Nav  ·  (app layer)│
            └───────▲───────────────┬──────────────────────┘
                    │               │
        ┌───────────┴───┐   ┌───────┴────────┐
        │   2D LiDAR    │   │ Motor driver / │
        │               │   │ power PCB      │
        └───────────────┘   └───┬────────┬───┘
                                 │        │
                    ┌────────────┴──┐  ┌──┴───────────┐
                    │ L/R drive     │  │ Suction fan, │
                    │ wheels, brush │  │ sensors,     │
                    │               │  │ bumper       │
                    └───────────────┘  └──────────────┘
```

*(Replace with a real block diagram once §5 interfaces are frozen.)*

## 4. Coordinate frames and conventions

- **TBD:** Define `base_link` origin and orientation (REP-103: x-forward,
  y-left, z-up). All mechanical mounting points and URDF frames reference this.
- **TBD:** Define the reference plane (floor contact), robot diameter, and height
  envelope. *These two numbers gate every hardware module.* Source these from the
  [reference vacuum teardown](https://github.com/remakeai/vacuum-cleaner-teardown)
  (see [docs/references.md](docs/references.md)).
- Units: millimeters, kilograms, SI. Right-handed frames. Angles in radians.

## 5. Hardware architecture

### 5.1 Chassis and reference frame
The chassis is the **integration backbone**. It publishes the mounting interface
every other hardware module targets. Reference geometry (dimensions, wheelbase,
motor specs, mass) comes from the
[reference vacuum teardown](https://github.com/remakeai/vacuum-cleaner-teardown).

- **TBD:** Overall diameter and height budget.
- **TBD:** Mounting grid / bolt pattern standard (e.g., M3 on a defined pitch).
- **TBD:** Mass budget per module and total target mass.

### 5.2 Mechanical interface standard (the contract)
Every hardware module's RFM must specify, against this standard:
- Mounting points (bolt pattern, location relative to `base_link`).
- Bounding envelope (max size the module may occupy).
- Mass budget.
- Mating tolerances and print orientation.
- **TBD:** Define the standard connector/fastener set (screw sizes, heat-set
  inserts, etc.) so parts from different authors actually mate.

### 5.3 Electrical interface standard (the contract)
- **TBD:** Battery nominal voltage and chemistry (e.g., Li-ion 3S/4S).
- **TBD:** Power rails distributed to modules (e.g., VBAT, 5V, 3.3V) and connector
  types/pinouts.
- **TBD:** Motor-driver-to-compute interface (USB serial? micro-ROS over UART?).
- **TBD:** Sensor bus(es): bumper/cliff signal levels, LiDAR power + data (USB/UART).

### 5.4 Compute and sensing
- Compute: Raspberry Pi 5 (MVP). Mount is a module.
- LiDAR: LDROBOT LD14P for the reference build; any model supported by the
  `kaiaai/LDS` / `lds2d` library is interface-compatible.

## 6. Software architecture

### 6.1 ROS2 graph (MVP)
- **TBD:** Node list and the topic/service/action interfaces between them.
- Core nodes (MVP): LiDAR driver, base controller (diff-drive), odometry,
  teleop, SLAM (manual mapping), TF/URDF publisher.
- **Interface contract:** each software module's RFM declares the ROS2 topics,
  services, message types, and parameters it publishes/consumes. Modules depend
  on these interfaces, not on each other's code.

### 6.2 Simulation
- Gazebo + URDF, with a set of residential-layout worlds for navigation and
  coverage testing. Sim parity is a first-class requirement, not an afterthought.

### 6.3 Application layer (Phase 2 — north star, NOT in MVP)
A ROS2-agnostic layer that runs third-party apps locally in isolated **Podman**
containers, so app developers need no ROS2 expertise. Documented here only to
keep its boundary clean; **explicitly out of scope for the Aug 31 MVP.**

## 7. MVP definition (target: 2026-08-31)

**In scope:** ROS2 on RPi 5 · LiDAR · manual SLAM/mapping · teleop drive ·
3D-printed chassis · Gazebo sim with URDF · evaluation + demo video. No dock,
no autonomous exploration, no Home Assistant, no app layer.

**Explicit non-goals for MVP:** autonomous coverage, docking, auto-empty, mopping,
Home Assistant, the app platform, accessories. These are later phases.

**Critical-path ownership:** the maintainer (+ small core) own the chassis,
interface specs, and integration so the MVP does not depend on volunteer delivery
timing. Community modules accelerate and improve the MVP; they do not block it.

## 8. Safety review gate

Battery, charging, motor-driver, and mains-adjacent modules require maintainer
safety review before merge. RFMs for these modules must include a hazard note
(over-current, thermal, short, mechanical pinch).

## 9. Roadmap (phases after MVP)

1. Rechargeable battery + basic dock + autonomous floor mapping.
2. Home Assistant integration.
3. Application layer (Podman app runtime) + first delightful apps.
4. Accessories and novel apps; integrations (e.g., LeRobot arm).

## 10. Open questions

- Onboard ROS2 vs micro-ROS on an MCU for the base controller?
- One hardware-agnostic HAL covering reference vacuum + DIY builds (community idea)?
- Battery chemistry and charging approach?
- Module selection process: who decides which competing implementation wins, and
  on what criteria? (See `docs/RFM-TEMPLATE.md` acceptance criteria.)
