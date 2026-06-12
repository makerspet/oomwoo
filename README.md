<div align="center">

# oomwoo

**The open-source robot vacuum you build yourself.**

Raspberry Pi · ROS2 · Home Assistant · 2D LiDAR · 3D printed · ESP32 · Arduino

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-early%20development-orange)

</div>

> ⚠️ **Early development.** This is a placeholder. The project is just getting
> started, so there's nothing to build yet. **Star or watch** the repo to follow along.

## What is this?

oomwoo is an **open-source home robot vacuum** you can build yourself, made for the
Raspberry Pi, ROS2, Home Assistant, and 3D-printing communities. It uses an
affordable 2D LiDAR to map your home and navigate on its own. Local, no
cloud required for regular functionality, no vendor lock-in.

*(The name is a rotational ambigram - it reads the same flipped 180°, like the robot itself, roaming your floor in every direction.)*

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

## Full disclosure:

if you'd rather skip the parts hunt, a kit (motors, PCB, brushes, gaskets, LiDAR) will be available at [makerspet.com](https://makerspet.com), from the same maker behind this project. The kit is a convenience, never a requirement. **Everything here stays open.**

When we get to apps, [remake.ai](https://remake.ai) will be providing its robot app store and apps platform. Using the app store will be optional. The vacuum will **always support cloud-free, local operation for regular functionality out-of-the-box**. 

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
- [RFC_MASTER_LIST.md](RFC_MASTER_LIST.md) — module catalog and status
- [docs/RFC-TEMPLATE.md](docs/RFC-TEMPLATE.md) — the per-module spec template
- [docs/references.md](docs/references.md) — reference designs and prior art
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute

## Community

- Discord: [Join the Maker's Pet server](https://discord.gg/3y2JKz5T25)
- Discussions: [GitHub Discussions](https://github.com/makerspet/oomwoo/discussions)
- Reddit: build-in-public home at [r/ArduinoAndRobotics](https://www.reddit.com/r/ArduinoAndRobotics/)
- YouTube: [build-in-public channel](https://www.youtube.com/@makerspet)
- X: [@0OMWO0](https://x.com/@0OMWO0)

## License

Code is released under the [Apache License 2.0](LICENSE).

Hardware design files, once added, to be released under an open hardware
license (TBD).
