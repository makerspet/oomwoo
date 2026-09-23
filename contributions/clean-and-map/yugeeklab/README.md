# Clean-and-map — yugeeklab

Pointer to a self-hosted implementation of the `clean-and-map` RFC, aimed at the part
the [RFC board](../../README.md) lists as *not started*: **coverage while mapping**.
Sweep a floor the robot has never seen while slam_toolbox builds the map, explore
frontiers until nothing reachable is left, and know when it is done.

| Repo | What | Status |
|---|---|---|
| [oomwoo-clean-and-map](https://github.com/yugeeklab/oomwoo-clean-and-map) | ROS 2 Jazzy package: coverage-while-mapping behaviour, map-completeness meter, SLAM-mode launch, an offline planner bench | running on `living_room`, numbers below |

> **Read this first.** Nothing is proven in the target environment yet. This page is
> a claim plus a plan. Each box below flips only with a measured, reproducible run in
> the `makerspet/oomwoo:jazzy-dev` image against `oomwoo_one`.

## How this relates to the existing work

- [@Arkz-Deepak](../Arkz-Deepak) started clean-only first (coverage on a known map
  through `oomwoo_coverage`), as the maintainer suggested. This track starts from the
  other end, measurement and the mapping side, so the two meet in the middle rather
  than duplicate each other.
- Reuses rather than replaces `oomwoo_coverage` (boustrophedon + bumper peel-off) and
  `oomwoo_sim_support` (ground truth, coverage meter, regression runner) from
  [oomwoo-ros2-tools](https://github.com/makerspet/oomwoo-ros2-tools).
- Interfaces follow [SOFTWARE_INTERFACES.md](../../../docs/SOFTWARE_INTERFACES.md).
- Coordination thread: [discussion #66](https://github.com/makerspet/oomwoo/discussions/66).

## Plan

0. **Baseline.** Reproduce the maintainer's numbers in the dev image
   (`deploy/run_coverage_regression.sh`, test_room, 90 % gate) and run the interface
   checklist: `/scan`, `/odom`, `/tf`, `/bumper_left`, `/bumper_right`.
1. **Map-completeness meter.** The RFC asks for regression tests of *both* coverage
   and map completeness; the harness has only the first. A sim-only
   `map_completeness_meter` aligns the SLAM `/map` to the world-aligned reference map
   through the ground-truth pose and reports free-space agreement, false-occupied area
   and wall error over the reachable floor. Same shape as `coverage_meter`: `~/ratio`,
   a `MAP_REPORT` log line, a runner gate.
2. **SLAM-mode harness.** A `coverage_regression.launch.py` equivalent with no static
   map: slam_toolbox online async instead of `map_server` + AMCL, several start poses,
   headless.
3. **Coverage while mapping.** Incremental boustrophedon over the growing map:
   re-decompose when new free space appears, nearest frontier as the next target, and
   a documented **done condition**: no reachable frontier wider than the robot *and*
   coverage of the known reachable floor above target, both held for T s. Then save
   the map (`nav2_map_server` and slam_toolbox `serialize_map`).
4. **Robustness.** Bumper contacts mark LiDAR-invisible obstacles in a persistent
   layer. Wheel slip on contact (the open problem from discussion #48): measure map
   corruption with `odom_source:=wheel`, then try gating scans out of slam_toolbox
   while a bumper is held.
5. **Worlds and CI.** living_room, multi_room, narrow_passage; several start poses;
   GitHub Actions running the headless suite.

Dynamic-obstacle yielding stays out of scope, per the steering in discussion #39.

## Progress

- [x] Claim posted in Discussions ([#66](https://github.com/makerspet/oomwoo/discussions/66))
- [x] Baseline reproduced (test_room 96.4 %, living_room 87.7 % — the upstream
      harness, unmodified, on an arm64 rebuild of the dev image)
- [x] `map_completeness_meter` scoring the SLAM map against a reference map
- [x] SLAM-mode launch, headless (no `map_server`, no AMCL)
- [x] Coverage while mapping, with a done condition that fires, and a map save
- [x] Bumper-marked obstacles and a peel-off escape
- [x] Unit tests for the planner geometry (39, no ROS, no simulator, under a second)
- [x] An offline planner bench, so a planning change is judged in a second rather
      than an hour, across seven floor plans
- [x] Path efficiency: **0.141 -> 0.546** on `living_room`, same finished map
- [ ] Numbers re-measured on native x86-64 in CI
- [ ] Several start poses in the simulator, and a multi-room world
      (the frontier branch is still unexercised: in a single room there is always
      something left to clean, so exploration never has to be chosen)
- [ ] Videos

## Where it stands

`living_room`, headless. The first version that finished the room, against the
same task after the path work:

|  | first finishing run | now |
|---|---|---|
| coverage | 0.9642 | 0.9035 |
| path | 302.9 m | 78.0 m |
| efficiency (ideal / actual) | 0.141 | 0.546 |
| map known | 1.0000 | 1.0000 |
| free-space agreement | 0.9876 | 0.9845 |
| sim time | 3880 s | 1769 s |

Those coverage figures are not comparable as they stand, because the later run
stopped earlier. Compared at equal coverage, metres driven:

| coverage | before | now |
|---|---|---|
| 20 % | 23.4 | 10.9 |
| 40 % | 50.0 | 26.1 |
| 60 % | 79.5 | 40.8 |
| 80 % | 105.9 | 58.8 |
| 90 % | 121.7 | 76.9 |

The node's own coverage belief tracks the ground-truth grader to about a point,
which is the gap `coverage_planner`'s docstring flags as missing.

## Interfaces (planned)

| Direction | Name | Type | Note |
|---|---|---|---|
| sub | `/scan`, `/odom`, `/tf`, `/map` | standard | from urdf-gazebo-sim and slam_toolbox |
| sub | `/bumper_left`, `/bumper_right` | `ros_gz_interfaces/msg/Contacts` | behind a small adapter, per the contract |
| action | `/navigate_to_pose`, `/navigate_through_poses` | Nav2 | motion goes through Nav2; open-loop only during a bump escape, after cancelling the Nav2 goal |
| pub | `/clean_and_map/status` | `std_msgs/String` (JSON) until an OOMWOO message exists | `state`, `reason_code`, `message`, `recoverable`, `source` |
| pub | `/map_completeness_meter/ratio` | `std_msgs/Float32` | sim only, ground-truth based |

## Instructions

Install, run and test instructions land with milestone 1, in the self-hosted repo.
