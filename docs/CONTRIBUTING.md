# Contributing to OOMWOO

Thanks for your interest. OOMWOO is an open-source robot vacuum you build
yourself, and it's at a very early stage. That's the best time to get involved,
the foundations are still being laid and your input can shape the direction.

The project is built *module by module* so many people can work in parallel.
Browse the [module list in the README](../README.md#requests-for-contributions),
and see [ARCHITECTURE.md](ARCHITECTURE.md) for how the pieces fit together.

## Ways to help right now

You don't need to be a roboticist to contribute:

- *Ideas and feedback* — open a [Discussion](https://github.com/makerspet/oomwoo/discussions)
  about features, design choices, or what would make you build one.
- *Code* — firmware, ROS2 packages, Home Assistant integration.
- *Hardware* — 3D-printable chassis design, mechanical parts, PCB.
- *Documentation* — build guides, wiring diagrams, troubleshooting notes.
- *Testing* — once there's something to build, real-world build reports are gold.
- *Spread the word* — star the repo, share your build, post a demo.

## Getting started

1. *Pick a module.* Browse the
   [module list in the README](../README.md#requests-for-contributions) and choose a
   hardware or software module. Software and simulation modules can start
   immediately; hardware modules wait on the interface specs in
   [ARCHITECTURE.md](ARCHITECTURE.md). Read the module's `README.md` so you know
   the contract.
2. *Start a conversation first.* Claim or ask about the module in its
   [Issue](https://github.com/makerspet/oomwoo/issues) or
   [Discussion](https://github.com/makerspet/oomwoo/discussions) before writing
   code, so we align on the approach and avoid wasted effort.
3. *Build it in your own repo.* For code and simulation modules, develop your
   package in your **own public repository** — you own it, version it, and keep the
   credit. Build against the ROS2 interface contract in
   [SOFTWARE_INTERFACES.md](SOFTWARE_INTERFACES.md) so your work stays interoperable
   with other modules. (Docs and small reference material are handled differently —
   see below.)
4. *Submit a pointer PR.* Add a link to your repo in the module's entry with a
   one-line description. It's small, easy to review, and lets several
   implementations of the same module sit side by side. Keep the PR focused.
5. *Iterate in the open.* Modules are swappable — the best implementation surfaces
   over time, with the maintainer having the last call. A design that isn't
   selected is still a useful fallback.

## How contributions are structured

OOMWOO keeps the core small and lets the community grow around it:

- *Canonical / reference code stays first-party.* [oomwoo-one](https://github.com/makerspet/oomwoo-one)
  (robot description + sim), [oomwoo-install](https://github.com/makerspet/oomwoo-install)
  (dev environment), and the `kaiaai_*` packages are maintained by the project so the
  out-of-the-box build always works.
- *Module implementations (code) live in your repo.* You build a competing
  implementation of a module — a sim, a navigation stack, a behavior — in your own
  repository and submit a *link*. The project features accepted work from the
  module's page, credited to you. When a contribution is *featured*, we pin a
  specific commit or tag (and may fork it into the makerspet org) so the reference
  build stays reproducible even if the upstream repo moves.
- *Docs, specs and small reference material stay in-tree.* Part specifications,
  datasheets, STEP-model sourcing notes, PCB notes, and benchmarks are lightweight
  and best kept alongside the project — contribute those under
  `contributions/<module>/<your-username>/` as files in a PR.

Why links for code? You keep ownership, credit, and freedom to iterate; the project
stays lean and avoids absorbing third-party code and its licensing; and multiple
implementations of a module can coexist and be compared. The shared
[SOFTWARE_INTERFACES.md](SOFTWARE_INTERFACES.md) contract is what keeps
independently-built modules compatible.

## Hardware contributions

For CAD and mechanical work, please include source files (not just exported STLs)
where possible, so others can modify your design. Note the tool and version you
used. If your change affects the bill of materials, mention it in the PR. Each
hardware module must stay within the mechanical/electrical interfaces in
[ARCHITECTURE.md](ARCHITECTURE.md).

*Safety:* battery, charging, motor-driver, and mains-adjacent modules require a
maintainer safety review before merge. Include a hazard note in your submission.

## Code style

Conventions are still being established. For now: keep it simple, readable, and
consistent with the surrounding code. ROS2 packages should follow standard ROS2
layout and naming. We'll formalize linting and style as the codebase grows.

## Licensing

By contributing, you agree that your contributions are licensed under the
project's [Apache License 2.0](../LICENSE). Hardware design files will be released
under an open hardware license (to be finalized); contributions of hardware
files are made on that same open basis.

## Community and conduct

Be respectful, helpful, and welcoming. We want OOMWOO to be an easy, friendly
place for makers of every skill level. Harassment or hostility isn't tolerated.

Questions? Open a [Discussion](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
or join us on [Discord](https://discord.gg/3y2JKz5T25).
