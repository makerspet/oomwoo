<div align="center">

# oomwoo

**The open-source robot vacuum you build yourself.**

Raspberry Pi · ROS2 · Home Assistant · 2D LiDAR · 3D printed · ESP32 · Arduino

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-early%20development-orange)

</div>

## What is this?

oomwoo is an **open-source home robot vacuum** you can build yourself, made for the
Raspberry Pi, ROS2, Home Assistant, and 3D-printing communities. It uses an
affordable 2D LiDAR to map your home and navigate on its own. Local, no
cloud required for regular functionality, no vendor lock-in.

Reference design images - this is approximately how the finished design will look:

![Reference robot vacuum cleaner top](./assets/vacuum_model_top.webp)
![Reference robot vacuum cleaner bottom](./assets/vacuum_model_bottom.webp)

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

## v0 Goal

**MVP target: 2026-08-31** — bare-bones build:

- ROS2 on Raspberry Pi 5 OR (decision TBD) ESP32 running micro-ROS with ROS2 on local PC
- LiDAR with manual SLAM
- Gazebo sim
- 3D-printed chassis

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

Open Source Deliverables:

- [ ] Bill of materials (BOM)
- [ ] 3D-printable files
- [ ] ROS2 packages
- [ ] Firmware
- [ ] Motor drivers and sensors PCB
- [ ] Build, setup, bringup and troubleshooting instructions
- [ ] Demo video(s)

## Build one

Full build docs and a complete BOM are on the way, with the goal that you can
source every part yourself.

## Contributing

oomwoo is organized to built by the community, massively **in parallel**.
The vacuum and its software are subdivided into **modules**.
The list of modules is published in the **Request for Contributions** [RFC_MASTER_LIST.md](RFC_MASTER_LIST.md) document.

A volunteer picks whatever module she wants, works on that module whenever she wants,
submits her contribution as a PR under contibutions/module_name/github_username.

Multiple developers are welcome to work on the same module.
The best solution for each module surfaces for over time, with the project master having the last call.

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for how it works.
2. Browse [RFC_MASTER_LIST.md](RFC_MASTER_LIST.md) and pick a contribution to make, usually a hardware or software module.
   (Software and simulation modules can start right now.)
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for the system design and interfaces.
4. Say hi on [Discord](https://discord.gg/3y2JKz5T25) or in
   [Discussions](https://github.com/makerspet/oomwoo/discussions).

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — system design, interfaces, MVP scope
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute

## Community

- Discord: [Join the Maker's Pet server](https://discord.gg/3y2JKz5T25)
- Discussions: [GitHub Discussions](https://github.com/makerspet/oomwoo/discussions)
- Reddit: build-in-public home at [r/ArduinoAndRobotics](https://www.reddit.com/r/ArduinoAndRobotics/)
- YouTube: [build-in-public channel](https://www.youtube.com/@makerspet)
- X: [@0OMWO0](https://x.com/@0OMWO0)

## Requests for Contributions

Would you like to contribute?

Pick a contribution from the list below and [let me know](https://github.com/makerspet/oomwoo/discussions) you're working on it and your progress.

| Module | ID | Phase | Notes |
|---|---|---|---|
| ROS2 URDF + Gazebo sim | [urdf-gazebo-sim](./contributions/urdf-gazebo-sim) | Ready to start work | Design URDF, TF, simulate in Gazebo |
| Dust bin 3D design | [dust-bin](./contributions/dust-bin) | Ready to start work | Design, 3D print, test dust bin |

## Source Code

- [oomwoo ROS2 and Ubuntu installation](https://github.com/makerspet/oomwoo-install/) source code
- [oomwoo ROS2 URDF package and config](https://github.com/makerspet/oomwoo_urdf/) source code
- [remakeai reference vacuum teardown](https://github.com/remakeai/vacuum-cleaner-teardown) — a consumer LiDAR vacuum with a basic dock and stationary mop.

## Related prior art you should know about

- [AlieksieievYurii/vacuum-cleaner](https://github.com/AlieksieievYurii/vacuum-cleaner) — a DIY 3D-printed robot vacuum (Raspberry
  Pi Zero W, gyroscope-based, Fusion 360, Android control app, no dock)
- [kaiaai/LDS](https://github.com/kaiaai/LDS), [kaiaai/lds2d](https://github.com/kaiaai/lds2d) — open-source 2D LiDAR libraries (C++, Python) supporting 23+ LiDAR models
- [remakeai/vacuum_ros2_bridge](https://github.com/remakeai/vacuum_ros2_bridge) — ROS2 bridge for a 3irobotix CRL-200-based vacuum (Proscenic), full ROS2 control
- [Valetudo](https://github.com/Hypfer/Valetudo) — cloud-free firmware replacement for commercial vacuums (local app-level control, not ROS2)
- [Dennis Giese / robotinfo.dev](https://robotinfo.dev) — teardowns and rootability of commercial robot vacuums.
- [codetiger/VacuumTiger](https://github.com/codetiger/VacuumTiger) - 3irobotix CRL-200-based vacuum low-level control reverse engineered
- [Build a ROS2/LiDAR robot crash course](https://makerspet.com/blog/build-arduino-self-driving-robot-video-instructions/) - watch this if you have no robotics experience

## About

The project name "oomwoo" is a rotational ambigram - it reads the same flipped 180°, like the robot itself, roaming your floor in every direction.

The project is sponsored by makerspet.com and remake.ai. We are reusing their open-source solutions as templates.
- If you'd rather skip the parts hunt, a kit (motors, PCB, brushes, gaskets, LiDAR) will be available at [makerspet.com](https://makerspet.com), from the same maker behind this project. The kit is a convenience, never a requirement. **Everything here stays open.**
- When we get to apps, [remake.ai](https://remake.ai) will be providing its robot apps platform and app store. Using the app store will be entirely optional. The vacuum will **always support cloud-free, local operation for regular functionality out-of-the-box**. 

## License

Code is released under the [Apache License 2.0](LICENSE).

Hardware design files, once added, to be released under an open hardware
license (TBD).
