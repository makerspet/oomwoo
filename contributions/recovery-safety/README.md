# Recovery Behaviors & Safety (ROS2 package)

Keep the robot *unstuck and safe*. This package provides a *recovery ladder*
(back up, wiggle, shake free, rotate, nudge, clear costmap, try an alternate path),
*escalation* when a recovery attempt fails, and a final *pause-and-alert* state
when everything fails. It also covers *safety*: cliff / wheel-drop / pickup
detection, an e-stop, and *status / error reporting* so a human knows what
happened. Because the physical robot isn't built yet, this is a *Gazebo
simulation*; it is later re-validated on hardware in the
[live-robot-bringup RFC](../live-robot-bringup).

> *Status — ready to start work.* No need to wait for OOMWOO hardware — develop it in the
> Gazebo sim ([urdf-gazebo-sim](../urdf-gazebo-sim)) or on the real
> [placeholder Proscenic M6 Pro](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/).
> Say so in the [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

# Important References
- [clean-and-map RFC](../clean-and-map) and [urdf-gazebo-sim RFC](../urdf-gazebo-sim) — the *bumper* (left / right / front) and any cliff / wheel-drop sensors this package reacts to.
- [nav-localize RFC](../nav-localize) — pickup / kidnap detection ties into relocalization.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract for simulation-first modules.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- Nav2's behavior/recovery server is a good starting point for composing recoveries.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- implement a *recovery ladder*
  - a configurable, ordered set of behaviors, e.g. *back up*, *wiggle / shake free*, *rotate in place*, *clear the costmap*, *nudge*, *try an alternate path*
  - pick the right recovery for the situation (wedged, bumper-jammed, no valid path, localization lost)
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- *escalation*
  - if behavior *N* fails, try *N+1*; track attempts per situation so the robot doesn't repeat a recovery forever
- *pause-and-alert*
  - when the whole ladder is exhausted, stop safely, publish a clear *error / status*, and wait for a human or a resume command — *never thrash*
- *safety sensors*
  - detect *cliffs*, *wheel drop*, *pickup / kidnap* (hand pickup detection to [nav-localize](../nav-localize)), and bumper jams; respond by stopping motors / entering a safe state
- *e-stop*
  - a software emergency stop that brings the robot to a safe state immediately
- *status & error reporting*
  - a structured robot-state / error topic, human-readable, suitable for Home Assistant, so a person knows *why* the robot paused
- test it well
  - induce wedged / stuck situations in sim: trap the robot, drop a dynamic obstacle onto it, place it at a cliff edge, lift it
  - verify the ladder runs, escalates, then pauses-and-reports; verify it never thrashes indefinitely
- regression tests (headless, CI-friendly)
  - recovery success rate across induced stuck scenarios
  - guaranteed termination — the robot always reaches *recovered* or *paused-and-reported*, never an infinite loop
  - safety responses fire on cliff / wheel-drop / pickup / e-stop
- submit a PR (pull request) to `contributions/recovery-safety/<your-github-username>/`
  - link to ROS2 package(s)
  - instructions, documentation - how to install, run, configure, troubleshoot, test results
  - videos of recovery, escalation, and pause-and-alert
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- A configurable *recovery ladder* runs the right behaviors for the situation and frees the robot in the large majority of induced stuck scenarios
- Recoveries *escalate* and are bounded — the robot never repeats a failed recovery forever
- When recovery is impossible, the robot *pauses safely and reports a clear error*, then resumes on command
- *Safety*: cliff, wheel-drop, pickup, and e-stop all bring the robot to a safe state
- *Status / error reporting* is structured and Home-Assistant-friendly
- *Regression tests* pass, including a guaranteed-termination check, runnable headless in CI
- Documented and reliably reproducible by someone else
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
