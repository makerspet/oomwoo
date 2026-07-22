# Stack Watchdog Contract

The health monitor is the software deadman between ROS2 and the MCU. It does not
replace the MCU's hard reflexes; it decides whether the ROS2 stack is healthy
enough for the MCU to keep accepting commanded motion.

## Component Heartbeat

Topic:

```text
/oomwoo/health/component    std_msgs/msg/String
```

Temporary JSON fields:

- `component_id`: stable component id, for example `recovery_safety`.
- `health`: `ok`, `healthy`, `warn`, `degraded`, or `error`.
- `stamp_sec`: component work timestamp.
- `sequence`: optional monotonic sequence.
- `detail`: optional short diagnostic text.

Rule: publish this from the work path, not from a free-running timer. Examples:

- recovery-safety evaluated a safety/recovery cycle
- Nav2 controller produced a command decision
- localization consumed a scan and produced a pose update
- dock-cycle evaluated a fresh IR/dock state

## Roster

Topic:

```text
/oomwoo/health/roster    std_msgs/msg/String
```

QoS expectation:

- `transient_local`
- reliable
- re-published on task transitions

Temporary JSON fields:

- `task_id`: active task or mode, for example `cleaning_job`.
- `components`: list of expected components.
- each component has `component_id`, `critical`, and `max_age_sec`.

Critical components block MCU heartbeat if missing, stale, or unhealthy.
Advisory components appear in status but do not stop the robot.

## Aggregated Stack State

Topic:

```text
/oomwoo/health/stack    std_msgs/msg/String
```

Temporary JSON fields:

- `state`: `no_roster`, `arming`, `healthy`, `healthy_with_advisory_faults`, or
  `fault`.
- `task_id`: current roster task.
- `emit_mcu_heartbeat`: whether the MCU-facing heartbeat should be emitted.
- `missing_critical`, `stale_critical`, `unhealthy_critical`.
- `advisory_faults`.
- `healthy_for_sec`.
- `source`.

## MCU Heartbeat

Topic:

```text
/oomwoo/health/mcu_heartbeat    std_msgs/msg/String
```

The MCU-facing bridge should forward this as the stack watchdog heartbeat only
while `emit_mcu_heartbeat=true`.

Fail-safe rules:

- no roster: withhold heartbeat
- arming window not satisfied: withhold heartbeat
- missing critical component: withhold heartbeat
- stale critical component: withhold heartbeat
- unhealthy critical component: withhold heartbeat
- advisory component fault: report but keep heartbeat

The MCU should soft-stop motors on a short heartbeat miss and assert CPU reset
only on a sustained miss, matching the architecture draft.

## Timing Budget

Choose component freshness so:

```text
component work period < component max_age < MCU soft-stop timeout < CPU reset timeout
```

At vacuum speeds, sub-second detection keeps the travel distance small. The
exact values should be validated under sim-clock jitter and Raspberry Pi load,
because too-tight watchdogs produce false trips.
