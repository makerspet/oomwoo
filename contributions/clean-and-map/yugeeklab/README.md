# Clean-and-map — yugeeklab

Pointer to a self-hosted implementation of the `clean-and-map` RFC, aimed at the part
the [RFC board](../../README.md) lists as *not started*: **coverage while mapping**.
The robot starts with no map, sweeps the floor slam_toolbox has drawn so far, replans
as more of the room appears, decides it is finished and saves the map.

| Repo | What |
|---|---|
| [oomwoo-clean-and-map](https://github.com/yugeeklab/oomwoo-clean-and-map) | ROS 2 Jazzy package: the coverage-while-mapping behaviour, a map-completeness meter, a SLAM-mode launch, an offline planner bench, 50 geometry tests |

Coordination thread: [discussion #66](https://github.com/makerspet/oomwoo/discussions/66).

> Every simulated number here was measured on an **arm64 rebuild** of
> `makerspet/oomwoo:jazzy-dev`, because the published image is amd64 only and this
> work was done on Apple Silicon. The upstream baseline reproduces on it
> (`test_room` 96.4 % against 97.0 %); a GitHub Actions job runs the tests and the
> bench on x86-64 and is how that caveat gets retired.

## How this relates to the existing work

- [@Arkz-Deepak](../Arkz-Deepak) started clean-only first (coverage on a known map
  through `oomwoo_coverage`). This track starts from the other end — mapping and
  measurement — so the two meet in the middle rather than duplicate each other.
- Reuses rather than replaces `oomwoo_coverage` (boustrophedon geometry, bumper
  peel-off) and `oomwoo_sim_support` (ground truth, coverage meter, regression
  runner) from [oomwoo-ros2-tools](https://github.com/makerspet/oomwoo-ros2-tools).
- Interfaces follow [SOFTWARE_INTERFACES.md](../../../docs/SOFTWARE_INTERFACES.md).

## Against the acceptance criteria

| Criterion | State |
|---|---|
| No map at start; builds a complete map | **yes** — `known_ratio` 1.0000, free-space agreement 0.985--0.992 in every session |
| Detects a done condition and saves the map | **yes** — the behaviour ends itself and writes the map |
| Full coverage of the reachable floor | **mostly** — five sessions of six end at 0.93--0.98; one ended itself at **0.82** (see below) |
| LiDAR-invisible obstacles: bumper, mark, replan, never stuck | **yes** — contacts mark a no-go, the robot peels off and replans; no session ended wedged |
| Left / right / front bumper | **yes** — both sim contact sensors, which are the front bumper's two halves |
| Headless CI regression of coverage *and* map completeness | **partly** — `map_completeness_meter` and the tests exist, the workflow has not been run |
| Several initial poses | **no** — almost everything so far is the one spawn |
| Robust to dynamic obstacles | **no** — not tested |
| Additional multi-room / different floorplan world | **no** — the bench has drawn floor plans, but no Gazebo world |
| Documented, reproducible by someone else | yes |

The three "no" rows are the honest remaining work, and they are what I would pick up
next unless the maintainer would rather see something else.

## Where it stands on `living_room`

Six sessions, no map at start, headless, scored by `coverage_meter` at
`cleaning_radius` 0.20 — the value `coverage_regression.launch.py` uses.

| | crossing 0.90 at | efficiency there | final coverage |
|---|---|---|---|
| best | **47.6 m** | **0.716** | 0.933 |
| median | 53.4 m | 0.638 | 0.941 |
| worst that crossed | 64.2 m | 0.530 | 0.980 |
| one session | never crossed | — | **0.822** |

For comparison, on the same world and the same harness,
`deploy/run_coverage_livingroom.sh` with the stock `coverage_planner`:
**coverage 0.8772, target never crossed, `pass: false`.** This node crosses 0.90
where upstream's does not reach it.

Neither meets the runner's `efficiency_target`, and the same arithmetic explains
both — which is the part I think is worth the maintainer's time.

### Why 0.80 efficiency is out of reach on this world

Coverage per metre driven is the pass spacing, and the spacing cannot exceed the
swath. For 90 % of `living_room`'s 13.62 m² at a 0.40 m swath the floor is 30.7 m,
and the gate allows 42.6 m — 11.9 m for every overhead there is. Measured, at the
90 % crossing:

```
sweeping                            35.2 m   ← exactly 12.26 m² / 0.35 m spacing
turn-arounds, 17 of them            + 6.1 m
travel between furniture-cut pieces + 5.9 m
                                    ───────
                                     47.2 m  against a 42.6 m budget
```

The spacing is 0.35 m rather than the full 0.40 m swath because localisation error
is 11 mm mean and 26 mm at the ninetieth percentile (`localization_error`, measured
on these runs), and passes laid exactly one swath apart come apart at the seams.
Planning at 0.40 m and at 0.35 m across error levels, with contacts modelled, exactly
one configuration in the table passes — no error at all.

**Upstream takes the wide spacing (`row_overlap` 0.05, an 8-cell step, no real
overlap) and fails on coverage. This node takes the narrow one, reaches coverage,
and fails on efficiency. They are the same fact from two sides**, and it is a
property of a 0.40 m swath against a centimetre of localisation error in a room
this cluttered, not of either planner. Four planner families and twenty-odd
variants were measured against it; the working record is in
[docs/PATH_EFFICIENCY.md](https://github.com/yugeeklab/oomwoo-clean-and-map/blob/main/docs/PATH_EFFICIENCY.md).

### The session that stopped at 0.82

`DONE sweep_complete: belief_coverage=0.8166 frontiers=0 escapes=7`. The map was
complete and the node's belief agreed with the grader to half a point; it simply
found nothing left it could plan to. Seven bumper contacts that session, each
leaving a no-go. That is a real defect in the done condition, not a measurement
artefact, and it is the first thing to fix.

## Also in the repo

- `map_completeness_meter`, in the shape of `oomwoo_sim_support`'s `coverage_meter`,
  so map completeness can be gated headless the way coverage already is — the RFC
  asks for regression tests of both.
- A SLAM-mode launch: no `map_server`, no AMCL.
- An **offline planner bench**. A simulated session takes the better part of an hour
  and two sessions of identical code land 33 % apart, so planner changes are chosen
  offline and confirmed in the simulator. It imports the node's own `_plan_sweep`,
  drives the waypoints, and models what the simulator does to them — including
  hitting things, which is what finally made its numbers agree with the simulator's.
  It plans on a map slam_toolbox drew and scores against the reference map, because
  doing both on one map picks the wrong variant.
- 50 geometry tests needing neither ROS nor a simulator, in under a second.

## Interfaces

| Direction | Name | Type | Note |
|---|---|---|---|
| sub | `/scan`, `/odom`, `/tf`, `/map` | standard | from urdf-gazebo-sim and slam_toolbox |
| sub | `bumper_left/contact`, `bumper_right/contact` | `ros_gz_interfaces/msg/Contacts` | |
| action | `/navigate_to_pose` | Nav2 | long or blocked hops; short clear ones are driven on `/cmd_vel`, and the Nav2 goal is cancelled first |
| pub | `/cmd_vel` | `geometry_msgs/Twist` | pass waypoints and the bump escape |
| pub | `~/status` | `std_msgs/String` (JSON) | `state`, `reason_code`, `message`, `recoverable`, `source` |
| pub | `~/cleaning_active` | `std_msgs/Bool` | latched; what `coverage_meter` starts and stops its accounting on |
| pub | `/map_completeness_meter/ratio` | `std_msgs/Float32` | sim only, ground-truth based |

## Running it

In the `makerspet/oomwoo:jazzy-dev` container:

```bash
cd /ros_ws/src && git clone https://github.com/yugeeklab/oomwoo-clean-and-map
cd /ros_ws && colcon build --symlink-install --packages-select oomwoo_clean_and_map
source install/setup.bash
ros2 launch oomwoo_clean_and_map clean_and_map.launch.py
```

`docker/Dockerfile.arm64` rebuilds that image for Apple Silicon.
`docker/scripts/run_once.sh` runs one session to completion and prints the distance
split; `docker/scripts/run_ab.sh` runs two configurations alternately, which is what
the run-to-run spread demands.
