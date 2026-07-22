# Stack Health Monitor & Software Watchdog (ROS2)

The *soft-fault safety layer*: detect when the ROS2 stack — or any safety-critical
component — is no longer *alive and well*, and bring the robot to a safe state
through the MCU. It sits *above* the MCU's hard reflexes (cliff / bumper /
wheel-drop / overcurrent motor cutoffs, which stay independent in firmware) and
*below* the application. It is the thing that stops the robot when a critical node
*crashes*, *deadlocks*, or *was never brought up* — the cases the MCU's raw
CPU-liveness watchdog alone cannot see (the CPU is "alive", but the stack is not
actually driving safely).

The core idea: every safety-critical node publishes an *alive-and-well* heartbeat;
a *health aggregator* checks those against the set of components that are *supposed*
to be running for the current task; and only then does it emit a *single* "stack
healthy" heartbeat to the MCU. If any expected component goes stale or unhealthy,
the aggregate heartbeat stops and the MCU fails the robot safe.

> *Status — design-first, ready to start.* The contracts (heartbeat, roster, MCU
> behavior) can be designed and prototyped now in the Gazebo sim
> ([urdf-gazebo-sim](../urdf-gazebo-sim)) or on the placeholder Proscenic; the MCU
> side lands with [mcu-io-firmware](../mcu-io-firmware) /
> [io-board-interface](../io-board-interface). Say hi in the
> [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

# Why this, not "re-publish /cmd_vel"

A dead or hung controller must stop the robot. Re-publishing `/cmd_vel` and relying
on a drive-command timeout only covers *one* consumer and *one* failure. A stack
health monitor is more general — a fault *anywhere* in the critical set (localization,
costmap, the safety node itself) trips it — and it lets the MCU keep the *simplest*
drive semantics (hold the last setpoint; controllers send explicit stops at maneuver
ends), with **one** clean safety path instead of a timeout on every topic.

# Design sketch

- *Per-component heartbeat.* Each safety-critical node publishes a small
  `alive-and-well` message (node id, health level, stamp). Assert it *from the work
  path* — e.g. "I completed a control cycle / produced a scan" — **not** from a
  free-running timer. A timer keeps ticking even when the node's real loop has
  deadlocked, so a timer-based heartbeat can lie.
- *Expected roster.* The task launch (clean, map, dock, …) declares the set of
  *critical* components it brings up — published latched (`transient_local`) and
  re-posted on task transitions. Mark *critical* vs *advisory*: a dead logger or
  RViz must not stop the robot. The roster is what lets the aggregator notice a node
  that *never started* or *died completely* (a dead node simply stops publishing).
- *Health aggregator (the deadman).* Matches live heartbeats against the roster and
  emits the single MCU heartbeat only while *every* expected critical component is
  *fresh and well*. **Fail-safe by default:** withhold the heartbeat until the roster
  is known and the full set is confirmed healthy (an *arming* window). A useful
  consequence — the robot is physically immovable until the stack is confirmed up.
- *MCU side.* The MCU consumes the aggregate heartbeat as its stack watchdog (see
  [ARCHITECTURE.md](../../docs/ARCHITECTURE.md): the MCU asserts the CPU-reset line on
  missed health packets). Two-stage response: a brief miss → *soft-stop* motors
  (recoverable); a sustained miss → assert *CPU-reset*. The hard reflex layer
  (cliff / bumper / overcurrent ISR) is independent and always on.

# Important References

- [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — the CPU↔MCU link and the MCU-asserts-CPU-reset-on-missed-health-packets contract this feeds.
- [io-board-interface](../io-board-interface) and [mcu-io-firmware](../mcu-io-firmware) — the MCU heartbeat input, soft-stop, and CPU-reset behavior. Decide *here* what the MCU does with a *stale drive setpoint* (hold vs. drive-freshness timeout); with this monitor in place, "hold the last setpoint" is the simplest choice.
- [recovery-safety](../recovery-safety) — this removes the *safety* reason for the recovery node to re-publish `/cmd_vel`; recovery still sends explicit stops at the end of each maneuver.
- Nav2 `lifecycle_manager` + *bond* — an existing "expected roster (`node_names`) + liveness (the bond breaks when a managed node dies)" mechanism you can build on or feed from. Note: we run it with `bond_timeout: 0.0` in the sim because a slow sim clock false-trips it — liveness timeouts are *jitter-sensitive*, plan margins accordingly.
- `diagnostic_updater` / `diagnostic_aggregator` (`/diagnostics`) — the standard ROS2 way for a node to publish "alive and *well*". The deadman can consume it, but keep the final MCU-facing aggregator *tiny and auditable*.
- [SOFTWARE_INTERFACES.md](../../docs/SOFTWARE_INTERFACES.md) — where the heartbeat + roster + aggregate contract should be recorded.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) · [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- *Define the contracts* (design-first; record in [SOFTWARE_INTERFACES.md](../../docs/SOFTWARE_INTERFACES.md)):
  - the per-component *heartbeat* message + topic (id, health level, stamp) and the *heartbeat-from-work* rule
  - the *roster* message + topic (critical vs. advisory, latched, per-task) and how task launches publish it
  - the *aggregate MCU heartbeat* plus the *arming / fail-safe / recovery* states
- *Build the aggregator node* — roster match, freshness + health check, fail-safe default, arming window, single-heartbeat output. Keep it small and auditable.
- *Instrument a few critical nodes* to emit work-path heartbeats (start with the recovery/safety node and the controller); optionally bridge Nav2 *bond* / `/diagnostics` into the roster.
- *Pick timing* — component-rate < aggregator-rate < MCU-timeout, with margins that survive clock/load jitter; document the *detect-to-stop* budget versus robot speed (at vacuum speeds a sub-second budget is < 0.3 m).
- *Simulate the MCU side first* — a stand-in that consumes the aggregate heartbeat and soft-stops `/cmd_vel`, so the whole loop is testable headless before firmware exists; hand the behavior to [mcu-io-firmware](../mcu-io-firmware).
- post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- iterate with review; TBD, expect the RFC to evolve

## Acceptance criteria

- A written *heartbeat + roster + aggregate* contract in SOFTWARE_INTERFACES.md.
- An aggregator that, in sim, *stops the robot* when any expected critical node is
  killed / hung / missing, and *refuses to arm* until the full roster is healthy —
  demonstrated headless.
- *No false trips* under normal startup and under load / clock jitter.
- The hard MCU reflex layer stays independent — a bumper / cliff stop must not depend
  on this path.
- TBD, expect criteria to evolve.

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and a
non-selected design is still a valid learning exercise and a fallback.
