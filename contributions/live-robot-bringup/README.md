# Live Robot Bring-up & Validation (ROS2 integration)

Take the behaviors validated in *simulation* and run them on a *real robot
vacuum*. Connect an off-the-shelf vacuum to ROS2 following the Proscenic M6 Pro
tutorial, then *re-run the acceptance tests from the simulation RFCs on
hardware*. This is the *single home for live validation* across all behaviors,
so the many sim contributors aren't blocked on hardware and the bring-up / bridge
cost is paid once.

> *Note:* the Proscenic / 3irobotix CRL-200S here is an *interim real-hardware test mule*
> for the ROS2 software stack — it is *not* the OOMWOO hardware design (which is built from
> sourced Roborock/Dreame/Xiaomi parts). This RFC eventually re-runs the same tests on real
> OOMWOO hardware.

> *Status — ready to start work.* The bring-up itself is doable now — connect the
> [placeholder Proscenic M6 Pro to ROS2](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/)
> with the [bridge](https://github.com/remakeai/vacuum_ros2_bridge). Re-running each behavior's
> acceptance tests follows as those behaviors land, but doing the bring-up / bridge now unblocks
> everyone else's hardware testing.

# Important References
- [Connect a robot vacuum (Proscenic M6 Pro) to ROS2 — tutorial](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/) — the primary how-to for getting a real vacuum onto ROS2.
- [remakeai/vacuum_ros2_bridge](https://github.com/remakeai/vacuum_ros2_bridge) — ROS2 bridge for a 3irobotix CRL-200-based vacuum (Proscenic), full ROS2 control.
- [codetiger/VacuumTiger](https://github.com/codetiger/VacuumTiger) — 3irobotix CRL-200-based low-level control, reverse engineered.
- The behavior RFCs whose tests you re-run on hardware: [clean-and-map](../clean-and-map), [nav-localize](../nav-localize), [dock-cycle](../dock-cycle), [recovery-safety](../recovery-safety), [floor-care](../floor-care), [cleaning-jobs](../cleaning-jobs).
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract that hardware bring-up should validate.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- connect a real vacuum to ROS2
  - follow the [tutorial](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/) on a Proscenic M6 Pro or compatible 3irobotix CRL-200-based vacuum
  - bring up the real sensors and actuators on ROS2: LiDAR, odometry, motors, bumper, battery, dock signals
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- match the simulation interfaces
  - map the sim topics / actions to the real robot so the behavior packages run *unchanged* wherever possible; document every gap
  - bring-up checklist: teleop, sensor sanity checks, e-stop verified before any autonomous run
- re-run the sim acceptance tests on hardware
  - run each behavior's acceptance tests on the real robot: [clean-and-map](../clean-and-map), [nav-localize](../nav-localize), [dock-cycle](../dock-cycle), [recovery-safety](../recovery-safety), [floor-care](../floor-care) (as the hardware allows), [cleaning-jobs](../cleaning-jobs)
  - record real-world results; document *sim-to-real gaps*, hardware-specific issues, and tuning changes
- be explicit about coverage
  - if a behavior *can't* be tested on a given robot (e.g. no mop or no auto-empty dock), *log it* — do not silently skip it
- submit a PR (pull request) to `contributions/live-robot-bringup/<your-github-username>/`
  - link to the bring-up / bridge package(s) and config
  - instructions, documentation - exact hardware, how to connect, run, troubleshoot
  - test results per behavior, videos, logs, and a sim-to-real notes write-up
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- A real vacuum is *connected to ROS2* with LiDAR, odometry, motors, bumper, battery, and dock signals working
- The sim interfaces are matched so behavior packages run on hardware with minimal changes; gaps are documented
- Each simulated behavior is *reproduced on the real robot* — or there is a *documented reason* it couldn't be (no silent skips)
- Real-world test results, videos, and a *sim-to-real gap* write-up are included
- Reproducible by someone else with the same hardware
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
