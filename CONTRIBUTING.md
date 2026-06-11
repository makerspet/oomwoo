# Contributing to oomwoo

Thanks for your interest. oomwoo is an open-source robot vacuum you build
yourself, and it's at a very early stage. That's the best time to get involved,
the foundations are still being laid and your input can shape the direction.

The project is built **module by module** so many people can work in parallel.
Browse [MODULES.md](MODULES.md) for the catalog, and see
[ARCHITECTURE.md](ARCHITECTURE.md) for how the pieces fit together.

## Ways to help right now

You don't need to be a roboticist to contribute:

- **Ideas and feedback** — open a [Discussion](https://github.com/makerspet/oomwoo/discussions)
  about features, design choices, or what would make you build one.
- **Code** — firmware, ROS2 packages, Home Assistant integration.
- **Hardware** — 3D-printable chassis design, mechanical parts, PCB.
- **Documentation** — build guides, wiring diagrams, troubleshooting notes.
- **Testing** — once there's something to build, real-world build reports are gold.
- **Spread the word** — star the repo, share your build, post a demo.

## Getting started

1. **Pick a module.** Browse [MODULES.md](MODULES.md) and choose a hardware or
   software module. Software and simulation modules can start immediately;
   hardware modules wait on the interface specs in
   [ARCHITECTURE.md](ARCHITECTURE.md). Read the module's `RFM.md` (Request for
   Module) and the [RFM template](docs/RFM-TEMPLATE.md) so you know the contract.
2. **Start a conversation first.** Claim or ask about the module in its
   [Issue](https://github.com/makerspet/oomwoo/issues) or
   [Discussion](https://github.com/makerspet/oomwoo/discussions) before writing
   code, so we align on the approach and avoid wasted effort.
3. **Work in the module folder.** Put your attempt under
   `<module>/<your-username>/` and keep it interface-compliant. Multiple attempts
   per module are welcome — modules are swappable, and a design that isn't
   selected is still a useful exercise and a fallback.
4. **Fork** the repo and create a branch for your change.
5. **Keep pull requests focused.** One logical change per PR is easier to review
   and merge than a large mixed one.
6. **Open the PR** with a short description of what it does and why.

## Hardware contributions

For CAD and mechanical work, please include source files (not just exported STLs)
where possible, so others can modify your design. Note the tool and version you
used. If your change affects the bill of materials, mention it in the PR. Each
hardware module follows the [RFM template](docs/RFM-TEMPLATE.md) and must stay
within the mechanical/electrical interfaces in [ARCHITECTURE.md](ARCHITECTURE.md).

**Safety:** battery, charging, motor-driver, and mains-adjacent modules require a
maintainer safety review before merge. Include a hazard note in your RFM.

## Code style

Conventions are still being established. For now: keep it simple, readable, and
consistent with the surrounding code. ROS2 packages should follow standard ROS2
layout and naming. We'll formalize linting and style as the codebase grows.

## Licensing

By contributing, you agree that your contributions are licensed under the
project's [Apache License 2.0](LICENSE). Hardware design files will be released
under an open hardware license (to be finalized); contributions of hardware
files are made on that same open basis.

## Community and conduct

Be respectful, helpful, and welcoming. We want oomwoo to be an easy, friendly
place for makers of every skill level. Harassment or hostility isn't tolerated.

Questions? Open a [Discussion](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
or join us on [Discord](https://discord.gg/3y2JKz5T25).
