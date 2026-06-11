<div align="center">

# oomwoo

**The open-source robot vacuum you build yourself.**

Raspberry Pi · ROS2 · Home Assistant · 2D LiDAR · 3D printed

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-early%20development-orange)

</div>

> ⚠️ **Early development.** This is a placeholder. The project is just getting
> started, so there's nothing to build yet. **Star or watch** the repo to follow along.

## What is this?

oomwoo is an open-source home robot vacuum you can build yourself, made for the
Raspberry Pi, ROS2, Home Assistant, and 3D-printing communities. It uses an
affordable 2D LiDAR to map your home and navigate on its own. Local, no
cloud required, no vendor lock-in.

*(The name is a rotational ambigram - it reads the same flipped 180°, like the robot itself, roaming your floor in every direction.)*

## Goals

- Affordable, fully open hardware, software and firmware
- Home appliance product quality - not a throwaway build
- Easy to build, with step-by-step zero-to-hero instructions
- 2D LiDAR mapping and autonomous navigation (ROS2 / Nav2)
- Native Home Assistant integration for local control
- 3D-printable, documented, and hackable chassis
- Buildable from parts you source yourself
- Apps - on top of ROS2 to customize vacuum operation
- Stretch goal: LeRobot integration, OpenClaw

## Roadmap

**MVP target: 2026-08-31** — bare-bones build (ROS2 on Raspberry Pi, LiDAR,
manual SLAM, Gazebo sim, 3D-printed chassis, demo video). Scope and non-goals are
in [ARCHITECTURE.md](ARCHITECTURE.md).

- [ ] Bill of materials (BOM)
- [ ] 3D-printable chassis files
- [ ] Firmware and ROS2 packages
- [ ] Step-by-step build guide
- [ ] Home Assistant integration
- [ ] Demo videos
- [ ] Apps ecosystem

## Build one

Full build docs and a complete BOM are on the way, with the goal that you can
source every part yourself.

Full disclosure: if you'd rather skip the parts hunt, a kit (motors, PCB, brushes, gaskets, LiDAR) will be available at [makerspet.com](https://makerspet.com), from the same maker behind this project. The kit is a convenience, never a requirement. **Everything here stays open.**

## Contributing

oomwoo is built by the community, **module by module**, so people can build in
parallel without stepping on each other. New here? Welcome.

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) for how it works.
2. Browse [MODULES.md](MODULES.md) and pick a hardware or software module.
   (Software and simulation modules can start right now.)
3. Check [ARCHITECTURE.md](ARCHITECTURE.md) for the system design and interfaces.
4. Say hi on [Discord](https://discord.gg/3y2JKz5T25) or in
   [Discussions](https://github.com/makerspet/oomwoo/discussions).

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — system design, interfaces, MVP scope
- [MODULES.md](MODULES.md) — module catalog and status
- [docs/RFM-TEMPLATE.md](docs/RFM-TEMPLATE.md) — the per-module spec template
- [docs/references.md](docs/references.md) — reference designs and prior art
- [CONTRIBUTING.md](CONTRIBUTING.md) — how to contribute

## Community

- Discord: [Join the Maker's Pet server](https://discord.gg/3y2JKz5T25)
- Discussions: [GitHub Discussions](https://github.com/makerspet/oomwoo/discussions)

## License

Code is released under the [Apache License 2.0](LICENSE).
Hardware design files, once added, to be released under an open hardware
license (TBD).
