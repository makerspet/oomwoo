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

# Design direction: reactive, contact-aware recovery (recommended)

Prior art is unanimous: real robot vacuums do **not** escape wedges with
navigation-stack recoveries. Nav2's `spin` / `backup` are *collision-averse* — they
check the costmap and refuse to move into the very cells the robot is wedged
against, so they stall exactly when needed (OOMWOO's own coverage planner already
documents *"spin/backup recoveries refuse to move there"*). A vacuum is
*contact-tolerant*: it has a bumper and is meant to touch walls and furniture. The
recovery it needs is a small **reactive, bumper-driven behavior layer** that runs
*open-loop and ignores the costmap*, layered **under** the planner and overriding it
while in contact (subsumption — Brooks, 1986). Coverage plans the open floor; this
handles near-obstacle. If it grows, this reactive layer can later be split into its
own `reactive-control` module.

**Proven escape heuristics** — a starting point from iRobot's *multi-mode coverage*
patents; tune the thresholds in sim. All are keyed on the *bumper pattern*, not the
costmap:

- *Wedge — bumper held.* If a bumper stays pressed for ~5 s, rotate **away from the
  pressed side** (a "panic turn") and retry; repeat until it releases. Back off and
  turn toward the free side — not a blind straight reverse.
- *Confined pocket — frequent bumps.* Track the running distance between bumps; when
  it drops below a threshold the robot is boxed in — switch to **bumper
  edge-following** (touch, small turns into-and-away) to worm out; below a lower
  threshold, panic-turn.
- *Stuck / wheels spinning — no bumps.* If the robot travels a long distance with no
  bump at all, assume it is high-centered / spinning — **spiral**, then panic-turn if
  still no contact.
- *Don't re-enter.* Mark the escaped pocket no-go so the sweep / gap-fill doesn't
  route straight back in (OOMWOO's coverage planner already does a version of this).

The simulated bumpers now publish (`/bumper_left|right/contact`), so this is
buildable and testable **headless today** — see
[oomwoo-one sim-bumpers](https://github.com/makerspet/oomwoo-one/blob/main/docs/sim-bumpers.md).
The same bumper-contact mechanism drives edge cleaning in [floor-care](../floor-care),
and stack-liveness safety lives in [health-monitor](../health-monitor).

# Important References
- [clean-and-map RFC](../clean-and-map) and [urdf-gazebo-sim RFC](../urdf-gazebo-sim) — the *bumper* (left / right / front) and any cliff / wheel-drop sensors this package reacts to.
- [nav-localize RFC](../nav-localize) — pickup / kidnap detection ties into relocalization.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract for simulation-first modules.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- Nav2's behavior/recovery server can *compose* recoveries, but note its `spin` / `backup` are collision-averse (see *Design direction* above) — for wedges, prefer contact-aware escapes.
- *Prior art — the reactive layer everyone uses:* iRobot behavior-based vacuum control — [multi-mode coverage](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6809490) ([7173391](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7173391)) and [learned escape behaviors](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11656628); Brooks, *A Robust Layered Control System for a Mobile Robot* (subsumption, 1986).
- *Coverage-planning prior art:* [opennav_coverage](https://github.com/open-navigation/opennav_coverage) (Nav2 / Fields2Cover, open-field focused), Fraunhofer [ipa_room_exploration](https://medium.com/@jjbecomespheh/ros-coverage-path-planning-32ec97ce3c21), and online sensor-based coverage (BA\*, Morse decomposition). [VFH+](https://www.mdpi.com/2077-1312/12/3/412) is a contact-tolerant reactive alternative to costmap avoidance.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- implement a *recovery ladder*
  - a configurable, ordered set of behaviors, e.g. *back up*, *wiggle / shake free*, *rotate in place*, *clear the costmap*, *nudge*, *try an alternate path*
  - pick the right recovery for the situation (wedged, bumper-jammed, no valid path, localization lost)
  - for *wedges*, prefer *contact-aware, open-loop* escapes (see *Design direction* above) over Nav2 `spin` / `backup`, which are collision-averse and stall in the wedge; start from the bumper-pattern escape heuristics and tune them in sim
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
