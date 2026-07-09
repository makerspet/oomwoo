<div align="center">

# OOMWOO

*Open-source robot vacuum you build yourself.*

Clean well · Hackable · Raspberry Pi · ROS2 · Home Assistant · 2D LiDAR · 3D printed · ESP32 · Arduino

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-early%20development-orange)

</div>

## What is this?

OOMWOO is an *open-source home robot vacuum* you can build yourself, made for the
Raspberry Pi, ROS2, Home Assistant, and 3D-printing communities. It uses an
affordable 2D LiDAR to map your home and navigate on its own. Local, no
cloud required for regular functionality, no vendor lock-in. Follow us building in public
[Discord](https://discord.gg/3y2JKz5T25) | [X](https://x.com/@0OMWO0) | [Reddit](https://www.reddit.com/r/oomwoo/) | [newsletter](https://stats.sender.net/forms/bo2rAK/view) | [YouTube](https://www.youtube.com/@makerspet) | [oomwoo.com](oomwoo.com) | [Tutorials](https://makerspet.com/learn/)

Reference design images - this is approximately how the finished design will look:

![Reference robot vacuum cleaner top](./assets/vacuum_model_top.webp)
![Reference robot vacuum cleaner bottom](./assets/vacuum_model_bottom.webp)
![Reference robot vacuum cleaner - top cover removed](https://github.com/makerspet/oomwoo/blob/main/assets/vacuum-no-top-back.webp)

## Goals

- Affordable, fully open hardware, software and firmware
- Home appliance product quality - not a throwaway build
- Easy to build, with step-by-step zero-to-hero instructions
- 2D LiDAR mapping and autonomous navigation (ROS2 / Nav2)
- Native Home Assistant integration for local control
- 3D-printable, documented, and hackable chassis
- Buildable from parts you source yourself
- Local, no cloud required for regular functionality
- Optional extra functionality when connected cloud
- Apps on top of ROS2 to customize vacuum operation
- Stretch goal: App store
- Stretch goal: LeRobot integration, OpenClaw

*v0 target: bare-bones build:*

- 3D-printed chassis
- ROS2 Gazebo sim
- LiDAR with manual SLAM
- ROS2 on Raspberry Pi 5 AND/OR ESP32 running micro-ROS with ROS2 on local PC - decision TBD

Open Source Deliverables:

- [x] [Software development environment](https://github.com/makerspet/oomwoo-install), robot [description package](https://github.com/makerspet/oomwoo-one/) and [tutorials](https://makerspet.com/blog/simulate-oomwoo-one-robot-vacuum-in-gazebo-with-ros-2/) (ROS2)
- [x] Placeholder real [vacuum cleaner](https://github.com/makerspet/proscenic-m6pro) and [tutorials](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/) (temporary while OOMWOO is being designed)
- [ ] [Bill of materials (BoM)](BOM.md) (in progress)
- [ ] 3D-printable files
- [ ] Firmware
- [ ] Motor drivers and sensors [I/O PCB](https://github.com/makerspet/oomwoo-io-board)
- [ ] Build, setup, bringup and troubleshooting [instructions](BUILD_INSTRUCTIONS.md)
- [ ] Demo video(s)

## Contributing

Would you like to contribute? See [CONTRIBUTING](docs/CONTRIBUTING.md) for the full guide.

OOMWOO is organized to built by the community, massively *in parallel*.
The vacuum and its software are subdivided into [modules](#requests-for-contributions), see list below.

A volunteer picks whatever module she wants and works on it whenever she wants.
For *code and simulation* modules she builds her package in her *own repo* and sends
a short PR *linking* it from the module; for *docs and specs* she contributes files
in-tree under `contributions/module-name/<her-github-username>`. See
[CONTRIBUTING](docs/CONTRIBUTING.md) for how this works.

Multiple developers are welcome to work on the same module.
The best solution for each module surfaces over time, with the project master having the last call.

1. Pick a contribution from the [list below](#requests-for-contributions).
2. [Let us know](https://github.com/makerspet/oomwoo/discussions) you're working on it and your progress.
3. Check [ARCHITECTURE.md](docs/ARCHITECTURE.md) and
   [SOFTWARE_INTERFACES.md](docs/SOFTWARE_INTERFACES.md) for the system design
   and ROS2 interfaces.

## Requests for Contributions

Every module below is *actionable now* — build it against the Gazebo simulation
([oomwoo-one](https://github.com/makerspet/oomwoo-one)) or a real *placeholder robot*
(a [Proscenic M6 Pro connected to ROS2](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/)),
until OOMWOO hardware is ready. Pick one, tell us in
[Discussions](https://github.com/makerspet/oomwoo/discussions), build it in your own
repo (docs and specs go in-tree), and send a short PR linking it from the module.

| Module | ID | Status | Notes |
|---|---|---|---|
| ROS2 URDF + Gazebo sim | [urdf-gazebo-sim](./contributions/urdf-gazebo-sim) | In progress | Placeholder URDF + Gazebo sim (reference: [oomwoo-one](https://github.com/makerspet/oomwoo-one); [@alvarosamudio](./contributions/urdf-gazebo-sim/alvarosamudio) merged), refined when hardware lands |
| First clean: coverage + mapping + exploration | [clean-and-map](./contributions/clean-and-map) | Ready to start work | Coverage cleaning while SLAM-mapping and exploring |
| Localization & navigation on a known map | [nav-localize](./contributions/nav-localize) | Ready to start work | Nav2 nav, AMCL localization, relocalize when lost, resume map |
| Dock cycle: undock, dock, recharge | [dock-cycle](./contributions/dock-cycle) | Ready to start work | Undock, return-to-dock, precise docking, station services, find dock when lost |
| Recovery behaviors & safety | [recovery-safety](./contributions/recovery-safety) | Ready to start work | Recovery ladder, escalation, pause-and-alert, safety sensors, status reporting |
| Compute benchmark & memory reduction | [compute-benchmark](./contributions/compute-benchmark) | In progress | Measure ROS2/Nav2/SLAM memory, compare composable nodes, and track the 4 GB -> 2 GB target |
| Floor-surface handling & edge cleaning | [floor-care](./contributions/floor-care) | Ready to start work | Wall/edge following, carpet vs hardwood, mop lift/lower |
| Cleaning modes, zones & job orchestration | [cleaning-jobs](./contributions/cleaning-jobs) | Ready to start work | Modes (regular/spot), virtual walls, room segmentation, job splitting + resume |
| Live robot bring-up & validation | [live-robot-bringup](./contributions/live-robot-bringup) | Ready to start work | Connect the placeholder Proscenic M6 Pro to ROS2, re-run sim tests on hardware |
| Source 3D models (STEP) for BOM parts | [source-3d-models](./contributions/source-3d-models) | In progress | Obtain / measure / model STEP files of off-the-shelf parts (wheels, fans, caster…) so mounts fit |
| Procure part specs & datasheets | [part-specs](./contributions/part-specs) | In progress | Find/measure/reverse-engineer specs (pinouts, encoder PPR, torque, how to drive fans…) for sourced parts |
| I/O + motor-driver PCB | [io-pcb](./contributions/io-pcb) | In progress | I/O board with CM4/CM5 socket, STM32G070 MCU - motors, sensors, 4S2P charging, safety, FreeRTOS, custom serial to CM4/CM5, 2D LiDAR header, IMU, audio serial/amp/speaker, MIPI camera(s) i/f; KiCad, JLCPCB |

> Planned and on-hold modules (mechanical design, later-phase software) live in the
> [RFC backlog](docs/RFC_BACKLOG.md).

## Source code reference

- [OOMWOO ROS2 and Ubuntu installation](https://github.com/makerspet/oomwoo-install/) source code
- [OOMWOO ROS2 URDF package and config](https://github.com/makerspet/oomwoo_urdf/) source code
- [remakeai reference vacuum teardown](https://github.com/remakeai/vacuum-cleaner-teardown) — a consumer LiDAR vacuum with a basic dock and stationary mop.

## Related prior art

- [AlieksieievYurii/vacuum-cleaner](https://github.com/AlieksieievYurii/vacuum-cleaner) — a DIY 3D-printed robot vacuum (Raspberry
  Pi Zero W, gyroscope-based, Fusion 360, Android control app, no dock)
- [kaiaai/LDS](https://github.com/kaiaai/LDS), [kaiaai/lds2d](https://github.com/kaiaai/lds2d) — open-source 2D LiDAR libraries (C++, Python) supporting 23+ LiDAR models
- [remakeai/vacuum_ros2_bridge](https://github.com/remakeai/vacuum_ros2_bridge) — ROS2 bridge for a 3irobotix CRL-200-based vacuum (Proscenic), full ROS2 control
- [Valetudo](https://github.com/Hypfer/Valetudo) — cloud-free firmware replacement for commercial vacuums (local app-level control, not ROS2)
- [Dennis Giese / robotinfo.dev](https://robotinfo.dev) — teardowns and rootability of commercial robot vacuums.
- [codetiger/VacuumTiger](https://github.com/codetiger/VacuumTiger) - 3irobotix CRL-200-based vacuum low-level control reverse engineered
- [Build a ROS2/LiDAR robot crash course](https://makerspet.com/blog/build-arduino-self-driving-robot-video-instructions/) - watch this if you have no robotics experience
- [Open Mower](openmower.de) - open-source outdoor lawn mower

## Design research

We reviewed the 2025–2026 consumer robot vacuum landscape (global + China-sourceable
brands, all price tiers) to decide which solutions to copy and which to skip. Key
takeaways for the build:

- *Suction is a sourcing problem, not an engineering one.* Real-world cleaning does
  *not* track advertised suction (Pa); ~$500 mid-tier models beat flagships. A
  moderate *sealed* sourced motor + a good brush + tight airflow sealing matches
  flagships — *no custom impeller needed.*
- *"Never gets stuck" needs camera + AI sensor fusion*, not LiDAR alone — LiDAR is
  blind below its ~10 cm turret (cables, socks). v1 leans on the *bumper* for low
  obstacles; vision-based avoidance is a later / experimental goal, not an MVP promise.
- *Anti-tangle brush:* a *tapered rubber roller* resists hair-wrap best (a top user
  complaint) and is easy to 3D-print.
- *Mop:* a 3D-printed *dual-spinning* mop is competitive; the self-washing roller
  mop's edge is overstated and hard to replicate — skip it for now.

*Well-loved models worth studying:* Eufy Omni S2 (obstacle avoidance), Narwal Flow
(roller mop), Ecovacs Deebot T90 Pro Omni (~$499 all-rounder), Dreame X40 Ultra
(dual-spinning mop). *Dreame* is also the most [Valetudo](https://github.com/Hypfer/Valetudo)-rootable
brand — the safest donor to study. *(Per-model rankings are directional, from
single-run reviewer tests.)*

## About

The project name "OOMWOO" is a rotational ambigram - it reads the same flipped 180°, like the robot itself, roaming your floor in every direction.

The project is sponsored by makerspet.com and remake.ai. We are reusing their open-source solutions.
- If you'd rather skip the parts hunt, a kit (motors, PCB, brushes, gaskets, LiDAR) will be available at [makerspet.com](https://makerspet.com), from the same maker behind this project. The kit is a convenience, never a requirement. *Everything here stays open.*
- When we get to apps, [remake.ai](https://remake.ai) will be providing its robot apps platform and app store. Using the app store will be entirely optional. The vacuum will *always support cloud-free, local operation for regular functionality out-of-the-box*. 

## License

Code is released under the [Apache License 2.0](LICENSE).

Hardware design files, once added, to be released under an open hardware
license (TBD).

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=makerspet/oomwoo&type=Date)](https://star-history.com/#makerspet/oomwoo&Date)
