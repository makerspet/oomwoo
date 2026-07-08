# Localization & Navigation on a Known Map (ROS2 package)

Once the [first clean](../clean-and-map) has produced a map, the robot must be able
to *operate on that saved map*: localize itself, navigate to any goal with Nav2,
recover its pose when it gets *lost* or is picked up and moved (the *kidnapped
robot* problem), and *resume an unfinished map*. Because the physical robot isn't
built yet, this is a *Gazebo simulation*; it is later re-validated on hardware in
the [live-robot-bringup RFC](../live-robot-bringup).

> *Status — ready to start work.* No need to wait for OOMWOO hardware — develop it in the
> Gazebo sim ([urdf-gazebo-sim](../urdf-gazebo-sim)) or on the real
> [placeholder Proscenic M6 Pro](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/).
> Say so in the [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

# Important References
- [clean-and-map RFC](../clean-and-map) — produces the saved/partial map this package consumes.
- [urdf-gazebo-sim RFC](../urdf-gazebo-sim) — robot URDF, Gazebo world(s), bumper.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract for simulation-first modules.
- [Gazebo + Nav2 simulation tutorial](https://makerspet.com/blog/tutorial-map-navigate-ros2-robot-in-simulation/) — baseline diff-drive + LiDAR robot in a Gazebo world.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- Nav2 (navigation), AMCL (localization), and slam_toolbox (localization mode / serialized session continue) are the expected building blocks.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- reproduce the baseline first
  - load a map saved by [clean-and-map](../clean-and-map) and bring up Nav2 + a localizer (AMCL or slam_toolbox localization mode) on the [urdf-gazebo-sim](../urdf-gazebo-sim) robot
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- localization on a known map
  - *global initial localization at startup* without being given a pose (e.g. AMCL global init / scan-matching) — the robot figures out where it is on the saved map
  - track pose reliably during navigation; expose a localization-confidence signal (covariance / scan-match score)
- navigation
  - Nav2 navigate-to-pose and navigate-through-poses to arbitrary goals on the saved map
  - obey dynamic obstacles via the local costmap
- lost / kidnapped recovery
  - *detect* when localization confidence drops (low score, high covariance, or a detected pickup/kidnap)
  - *relocalize*: rotate in place and/or drive to gather scans until the pose re-converges
  - define a clear *"relocalized" success condition*, and what happens if it *fails* — hand off to the [dock-cycle](../dock-cycle) *find-the-dock-when-lost* fallback
- resume an unfinished map
  - load a *partial / serialized SLAM session* (e.g. slam_toolbox serialization) and *continue mapping where it left off*, merging newly seen areas into the existing map without corrupting it
- test it well
  - start from *many initial poses*, including a wrong or unknown initial pose
  - *kidnap* the robot mid-run (teleport it in sim) and verify it recovers
  - resume from several partial maps and verify the merged map is correct
- regression tests (headless, CI-friendly)
  - relocalization success rate from random poses
  - navigation success rate to random reachable goals
  - map-resume correctness (resumed + continued map matches a from-scratch map of the same world)
- submit a PR (pull request) to `contributions/nav-localize/<your-github-username>/`
  - link to ROS2 package(s)
  - instructions, documentation - how to install, run, configure, troubleshoot, test results
  - videos of relocalization-when-lost and map-resume runs
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- On a saved map, from an *unknown initial pose*, the robot performs global localization and converges to the correct pose
- Nav2 navigation reaches arbitrary reachable goals reliably, avoiding dynamic obstacles
- When *lost / kidnapped*, the robot detects it, relocalizes, and resumes — or cleanly hands off to the find-the-dock fallback when relocalization fails
- An *unfinished map* can be loaded and mapping continued, producing a complete, uncorrupted map
- *Regression tests* pass and verify relocalization, navigation, and map-resume, runnable headless in CI
- Documented and reliably reproducible by someone else
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
