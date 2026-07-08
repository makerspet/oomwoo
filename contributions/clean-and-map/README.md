# First Clean: coverage cleaning with mapping and exploration (ROS2 package)

A ROS2 package for the robot's *first clean*. The vacuum starts with *no map*,
cleans the whole reachable floor using coverage path planning, builds a map with
SLAM *while* it cleans, and keeps exploring until the map is complete. Because the
physical robot isn't built yet, this is a *Gazebo simulation*.

> *Status — ready to start work.* No need to wait for OOMWOO hardware — develop it in the
> Gazebo sim ([urdf-gazebo-sim](../urdf-gazebo-sim)) or on the real
> [placeholder Proscenic M6 Pro](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/).
> Say so in the [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

> *Scope.* This RFC is only the *first clean from scratch*. Operating on a *saved* map,
> docking, recovery, floor-surface handling, and cleaning modes are deliberately *out of
> scope* and live in their own RFCs:
> [nav-localize](../nav-localize) (navigate / localize / resume a saved map),
> [dock-cycle](../dock-cycle) (undock / dock / recharge),
> [recovery-safety](../recovery-safety) (recovery & safety),
> [floor-care](../floor-care) (wall/edge following, carpet vs hardwood, mop), and
> [cleaning-jobs](../cleaning-jobs) (modes, zones, job orchestration).
> Keep this package focused on producing a *complete map* and *full first-pass coverage*;
> the others build on top of it.

# Important References
- [urdf-gazebo-sim RFC](../urdf-gazebo-sim) — provides the robot URDF, the Gazebo world(s), and the *bumper* this package depends on.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract for simulation-first modules.
- [m-explore-ros2 (kaiaai fork)](https://github.com/kaiaai/m-explore-ros2) — frontier exploration, tested and working. It maps and explores but does *not* clean — a good starting point to build on.
- [m-explore-ros2 demo + step-by-step instructions (video)](https://www.youtube.com/watch?v=81-9q7QfkHs&list=PLOSXKDW70aR8uA1IFahSKVuk5ODDfjTZV) — shows m-explore-ros2 in action and how to run it.
- [Gazebo simulation setup instructions](https://makerspet.com/blog/tutorial-map-navigate-ros2-robot-in-simulation/) — a simple differential-drive robot with a LiDAR in a Gazebo living room world; another possible starting point.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- reproduce the baseline simulation first
  - follow the [Gazebo simulation setup instructions](https://makerspet.com/blog/tutorial-map-navigate-ros2-robot-in-simulation/) to run the diff-drive + LiDAR robot in the Living Room world
  - get [m-explore-ros2](https://github.com/kaiaai/m-explore-ros2) running for frontier exploration (see the [demo video](https://www.youtube.com/watch?v=81-9q7QfkHs&list=PLOSXKDW70aR8uA1IFahSKVuk5ODDfjTZV)) — this gives you mapping + exploration *without* cleaning
  - build on the [urdf-gazebo-sim RFC](../urdf-gazebo-sim) robot model, world(s) and bumper
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- add coverage cleaning
  - the robot starts with *no prior map*
  - plan and execute a *coverage path* that cleans the whole reachable floor (e.g. boustrophedon / back-and-forth, plus corner and wall-edge handling)
  - build the map with *SLAM while cleaning* (e.g. slam_toolbox or cartographer) — mapping and cleaning happen together, not in separate passes
  - keep *exploring frontiers* until the map is complete, so no reachable area is missed
  - define and document a clear *done* condition (full coverage *and* complete map), then save the map
- make it robust
  - *dynamic obstacles:* a person, pet, or object moving into the robot's path must not break coverage or mapping — the robot should replan and continue
  - *LiDAR-invisible static obstacles:* the LiDAR may report open floor the robot cannot actually reach (glass, objects below the LiDAR plane, thresholds, ledges). Detect these via *bumper* contact, mark them as obstacles, recover, and replan around them
  - react to *bumper events* (left switch, right switch, front bumper) published by the urdf-gazebo-sim bumper
  - never get permanently stuck — recover from collisions and wedged situations (a basic local recovery here; the full recovery ladder lives in [recovery-safety](../recovery-safety))
- test it well
  - start the robot from *various initial locations* and verify it still achieves full coverage and a complete map
  - add *regression tests* (headless, CI-friendly) that verify both:
    - *map completeness* — the built map covers the whole reachable area
    - *coverage completeness* — the cleaning path covers the whole reachable floor
  - test recovery from dynamic obstacles and from bumper hits on LiDAR-invisible obstacles
- additional Gazebo worlds (highly valued)
  - create and test extra worlds: *multiple rooms, different floorplans*, narrow passages, furniture, and LiDAR-invisible obstacles
  - contribute these worlds back — they help everyone test
- submit a PR (pull request) to `contributions/clean-and-map/<your-github-username>/`
  - link to ROS2 package(s)
  - instructions, documentation - how to install, run, configure, troubleshoot, test results
  - the Gazebo worlds you added
  - videos of full clean-and-map runs from several start poses
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- Starting with no map in the Living Room world, from *multiple initial poses*, the robot:
  - achieves *full coverage* of the reachable floor
  - builds a *complete map* of the reachable area
  - detects a clear done condition and saves the map
- Robust to *dynamic obstacles* — a moving obstacle in the path does not break coverage or mapping
- Robust to *LiDAR-invisible static obstacles* — bumper contacts are detected, the obstacle is marked and avoided, the robot replans and does not get stuck
- Reacts correctly to *left / right / front bumper* events
- *Regression tests* pass and verify both map completeness and coverage completeness, runnable headless in CI
- Works in at least one *additional multi-room / different floorplan* world
- Documented and reliably reproducible by someone else
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
