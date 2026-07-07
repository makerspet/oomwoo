# Floor-Surface Handling & Edge Cleaning (ROS2 package)

Clean *better* by adapting to the floor. This package adds *wall following* (to
clean tight against walls), *carpet-edge following*, recognizing *carpet vs
hardwood*, and *lifting / lowering the mop* accordingly (never wet a carpet).
Because the physical robot isn't built yet, this is a *Gazebo simulation* — you
model the surfaces and the surface sensor in Gazebo; it is later re-validated on
hardware in the [live-robot-bringup RFC](../live-robot-bringup).

> *Status — ready to start work.* No need to wait for OOMWOO hardware — develop it in the
> Gazebo sim ([urdf-gazebo-sim](../urdf-gazebo-sim)) or on the real
> [placeholder Proscenic M6 Pro](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/).
> Say so in the [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

# Important References
- [clean-and-map RFC](../clean-and-map) — coverage cleaning that this refines at edges and surface transitions.
- [urdf-gazebo-sim RFC](../urdf-gazebo-sim) — robot URDF; this package likely needs a *surface sensor* and a *mop lift/lower actuator* modeled.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract for simulation-first modules.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

> Note: this package may need new sim sensors/actuators (surface sensor, mop
> actuator). Add them inside your submission for now and propose folding the
> stable ones back into [urdf-gazebo-sim](../urdf-gazebo-sim) later — please don't
> rewrite that RFC.

# Request for Contribution - Instructions

- *wall following*
  - detect walls from the LiDAR and drive a controlled offset along them so edges get cleaned, not just the room interior
  - integrate with [clean-and-map](../clean-and-map) coverage so edges *and* interior are both covered, without re-cleaning everything
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- *carpet-edge following*
  - detect carpet boundaries and follow the edge to clean along them
- *surface recognition (carpet vs hardwood)*
  - model a plausible sensor in sim (wheel current / IMU vibration / a dedicated downward sensor) and *publish the surface type*
- *mop lift / lower*
  - actuate the mop *up on carpet, down on hardwood*; model the actuator in Gazebo; *never wet a carpet*
  - coordinate with [cleaning-jobs](../cleaning-jobs) for mop-related job constraints
- test it well
  - build worlds with *mixed carpet + hardwood* regions and walls
  - verify edge coverage, correct surface classification, and correct mop state at every transition
- regression tests (headless, CI-friendly)
  - surface-classification accuracy
  - edge-coverage percentage (walls / carpet edges actually cleaned)
  - *zero carpet-wetting events* (mop never down on carpet)
- submit a PR (pull request) to `contributions/floor-care/<your-github-username>/`
  - link to ROS2 package(s) and any sim sensor/actuator + world additions
  - instructions, documentation - how to install, run, configure, troubleshoot, test results
  - videos of wall/edge following and mop lift/lower at surface transitions
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- *Wall / carpet-edge following* cleans tight along edges and integrates with coverage (high edge-coverage %)
- *Surface recognition* classifies carpet vs hardwood accurately
- *Mop lift/lower* tracks surface type correctly with *zero carpet-wetting events*
- *Regression tests* pass (classification accuracy, edge coverage, no carpet-wetting), runnable headless in CI
- Works in at least one *mixed carpet + hardwood* world
- Documented and reliably reproducible by someone else
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
