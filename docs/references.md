# References and prior art

Reference designs and related work that inform oomwoo. Add to this list as you
find good prior art (a SOTA scan is part of every module's RFM).

## Reference designs

- **oomwoo reference vacuum (maintainer)** — a working basic LiDAR vacuum (no
  mop, no auto-empty) that anchors the chassis geometry and proves feasibility.
  Teardown: [remakeai/vacuum-cleaner-teardown](https://github.com/remakeai/vacuum-cleaner-teardown)
  _(work in progress)._
- **AlieksieievYurii/vacuum-cleaner** — a DIY 3D-printed robot vacuum (Raspberry
  Pi Zero W, Fusion 360, Android control app). Useful prior art for chassis layout
  and mechanical design: [AlieksieievYurii/vacuum-cleaner](https://github.com/AlieksieievYurii/vacuum-cleaner)

## oomwoo-related projects by the maintainer

- **`kaiaai/LDS`** — open-source 2D LiDAR library supporting 23+ models
  (C++; Python equivalent `lds2d` via `pip install lds2d`).
- **`remakeai/vacuum_ros2_bridge`** — ROS2 bridge for a 3irobotix CRL-200-based
  vacuum (Proscenic), full ROS2 control.

## Ecosystem and background

- **Valetudo** — cloud-free firmware replacement for commercial vacuums
  (local control, not ROS2). Useful context on the hack-an-existing-vacuum path.
- **Dennis Giese / robotinfo.dev** — teardowns and rootability of commercial
  robot vacuums.

## Why build from scratch vs hack an existing vacuum

See the project's reasoning (LiDAR access, low-level hardware control, PCB-swap
tradeoffs, off-the-shelf compute). _TBD: promote to a short `docs/why.md`._
