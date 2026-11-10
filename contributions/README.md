# OOMWOO Contributions — RFC board

Each folder here is a **Request for Contribution (RFC)** — a self-contained module
(software, firmware, hardware, or procurement) you can pick up and build. Submit
your work under `contributions/<rfc>/<your-github-username>/`. New here? Read
[CONTRIBUTING](../docs/CONTRIBUTING.md), and see the
[RFC lifecycle](../docs/CONTRIBUTING.md#rfc-lifecycle) for how RFCs progress and
retire.

**Status legend** — *Active:* `exploratory` → `ready to start work` /
`design-first` → `in progress`. *Retired* (closed to new contributions, but
**kept in place** for provenance): `completed` · `superseded` · `descoped` ·
`merged`.

**This board is canonical** for every RFC's status and progress. An RFC's own
README describes its scope and how to get started; where its `> Status —` line
disagrees with the row below, the row below wins. Update this board when you land
work.

**Progress** is a rough, self-reported percentage of the RFC's scope — a sense of
"how much is left", not a promise:
![>=75%](https://img.shields.io/badge/%3E%3D75%25-brightgreen) nearly there ·
![25-74%](https://img.shields.io/badge/25--74%25-yellow) under way ·
![<25%](https://img.shields.io/badge/%3C25%25-red) barely started / open.

| RFC | What it is | Progress | Status |
|-----|------------|:--------:|--------|
| [clean-and-map](clean-and-map) | First clean: coverage + SLAM + exploration | ![15%](https://img.shields.io/badge/15%25-red) | coverage meter + regression harness + drive-to-goal cleaning; coverage-while-mapping not started |
| [nav-localize](nav-localize) | Localization & navigation on a known map | ![75%](https://img.shields.io/badge/75%25-brightgreen) | AMCL to slam_toolbox (~3x accuracy), custom lost-detection + Cartographer-style global relocalizer (96/96 in sim), stress-tested; needs real-robot validation |
| [floor-care](floor-care) | Wall/edge following, surfaces, mop lift | ![45%](https://img.shields.io/badge/45%25-yellow) | LiDAR contour follower v1 follows walls and concave/convex boundaries (line-fit surface estimate replaced nearest-beam: 0.5 deg vs +-20 deg bearing error); bump-out wall clean; side ToF sensors, mop + FlexiArm modules modelled; loop-closure and bumper handoff still open |
| [cleaning-jobs](cleaning-jobs) | Cleaning modes, zones, job orchestration | ![0%](https://img.shields.io/badge/0%25-red) | ready to start work |
| [recovery-safety](recovery-safety) | Recovery behaviors & safety | ![10%](https://img.shields.io/badge/10%25-red) | lost-detect to relocalize recovery + one escape reflex; recovery ladder, e-stop, reporting open |
| [dock-cycle](dock-cycle) | Undock, dock, recharge & station services | ![30%](https://img.shields.io/badge/30%25-yellow) | dock mechanical design started; two docks modelled in sim (basic charging pad + auto-empty/mop-wash), manual undocking demoed; teardown, schematic, sensors + fans sourced; docking behaviours not started |
| [obstacle-avoidance](obstacle-avoidance) | Near-field camera + ToF avoidance | ![20%](https://img.shields.io/badge/20%25-red) | front ToF + stereo modelled in sim, transient-obstacle detection demoed, scan rays marked static/dynamic for downstream ML |
| [control-app](control-app) | Control app & UX | ![0%](https://img.shields.io/badge/0%25-red) | ready to start work (design track) |
| [live-robot-bringup](live-robot-bringup) | Live robot bring-up & validation | ![10%](https://img.shields.io/badge/10%25-red) | Proscenic M6 Pro to ROS2 tutorials; 3irobotix Delta-2C Pro LiDAR driver implemented and validated |
| [health-monitor](health-monitor) | Stack health monitor & software watchdog | ![35%](https://img.shields.io/badge/35%25-yellow) | in progress: aggregator (xbattlax) + MCU stand-in and fault-injection kit (bilusss) stop `cmd_vel` in every injected fault in sim; draft timing and QoS values in SOFTWARE_INTERFACES.md; real nodes not yet instrumented, task launches don't publish rosters, MCU side pending firmware |
| [compute-benchmark](compute-benchmark) | Compute benchmark & memory reduction | ![70%](https://img.shields.io/badge/70%25-yellow) | tentatively fits 2 GB Pi CM4/CM5; an old smartphone is now a supported compute option (no Pi needed); repeatable Pi benchmark CLI + guide |
| [mcu-io-firmware](mcu-io-firmware) | MCU I/O board firmware (STM32G473) | ![5%](https://img.shields.io/badge/5%25-red) | host-tested framing/safety prototypes + simulated CPU/MCU loop; real STM32 HAL, motor and safety bring-up open |
| [io-board-interface](io-board-interface) | I/O board software interface | ![30%](https://img.shields.io/badge/30%25-yellow) | SPEC.md (GPIO/pinout contract) drafted; ROS2 bridge mapping + validation open |
| [urdf-gazebo-sim](urdf-gazebo-sim) | oomwoo URDF + Gazebo simulation | ![90%](https://img.shields.io/badge/90%25-brightgreen) | sim model essentially complete: full sensor suite, living-room + kitchen worlds, docks, GPU rendering |
| [mac-dev-env](mac-dev-env) | macOS (Apple Silicon) dev environment (pixi) | ![40%](https://img.shields.io/badge/40%25-yellow) | initial working pixi recipe (experimental) |
| [io-pcb](io-pcb) | I/O + motor-driver PCB (KiCad) | ![55%](https://img.shields.io/badge/55%25-yellow) | smartphone-as-compute option designed; schematic ~50% hand-checked (first review round); carpet sensor driver; drive wheels brought up on the bench; front + side sensor boards, watchdog + motor shutoff, charging dock; not validated, do not fabricate |
| [dust-bin](dust-bin) | Dust bin (mechanical module) | ![5%](https://img.shields.io/badge/5%25-red) | base port added to the chassis CAD; bin design still ahead |
| [vacuum-fan](vacuum-fan) | Blower fan assembly (mechanical module) | ![50%](https://img.shields.io/badge/50%25-yellow) | suction fan digitized to STEP, fans sourced and ordered, main fan brought up on the bench |
| [part-specs](part-specs) | Procure part specs & datasheets | ![85%](https://img.shields.io/badge/85%25-brightgreen) | drive-wheel and 4 suction-fan pinouts, voltages and no-load/stall currents confirmed by measurement; cliff/bumper/wheel pinouts reverse-engineered; dock fans, PSU, dock sensors, micro-switches, mop disk, VL6180 sourced |
| [source-3d-models](source-3d-models) | Source 3D models (STEP) for BOM parts | ![85%](https://img.shields.io/badge/85%25-brightgreen) | parts scanning mostly complete: battery, brushes, wheels, mop/FlexiArm, fan, carpet sensor, camera, switches |
| [stair-climbing](stair-climbing) | Multi-floor: stair climbing (drive-in exoskeleton) | ![0%](https://img.shields.io/badge/0%25-red) | exploratory, for later |
| [esp32-p4](esp32-p4) | ESP32-P4 experimental compute + safety track | ![0%](https://img.shields.io/badge/0%25-red) | exploratory, for later |

> **Two builds.** OOMWOO comes in a *basic* version (vacuum only, simple to
> assemble, charging-only dock) and a *full-featured* one (mop, auto-empty,
> extendable side brush). Some RFCs serve only the full build - mop lift in
> floor-care, the auto-empty dock in dock-cycle - so check which you are
> targeting before you start.

> **Core mechanical design is not an RFC.** The chassis, brushes, mop, wheel
> mounts and shell are designed in-house and tracked in
> [oomwoo-one-cad](https://github.com/makerspet/oomwoo-one-cad) — a tightly-coupled
> reference design is slow and messy to settle by consensus. Planned hardware
> modules are listed in the [RFC backlog](../docs/RFC_BACKLOG.md); a well-defined,
> standalone piece (a mount, a spec, a part model) graduates to an RFC here.
