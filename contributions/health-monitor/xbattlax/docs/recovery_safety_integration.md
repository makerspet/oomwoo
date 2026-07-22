# Recovery Safety Integration

The recovery-safety node already sends bounded motion and explicit stops. The
health monitor adds the more general failure path: if recovery-safety, Nav2,
localization, or dock-cycle stops doing real work, the MCU stack heartbeat stops.

## Recovery-Safety Heartbeat

`recovery_safety` should publish a component heartbeat after real work events:

- safety input handled
- recovery event accepted or ignored
- active recovery step evaluated
- active recovery step succeeded/failed/timed out
- status publication completed

It should not publish the health heartbeat from a timer that is independent of
the recovery controller. A timer could continue ticking while the useful recovery
state machine is wedged.

## Relationship to `/cmd_vel`

The `/cmd_vel` hold fix remains useful for motion quality: recovery maneuvers
longer than a base controller's command timeout should not be truncated.

The health monitor is different. It is the robot-wide fail-safe:

- if `recovery_safety` dies, MCU heartbeat stops
- if `dock_cycle` dies during final approach, MCU heartbeat stops
- if `localization` is stale during navigation, MCU heartbeat stops
- if an advisory logger dies, the stack reports it but the robot keeps moving

## Proposed Critical Rosters

Mapping:

- `recovery_safety`
- `nav2_controller`
- `localization`
- `slam_toolbox` or map/localization equivalent

Known-map navigation:

- `recovery_safety`
- `nav2_controller`
- `localization`
- `map_server`

Dock final approach:

- `recovery_safety`
- `dock_cycle`
- `dock_ir_sensor`
- `health_monitor`

The exact roster should be owned by the task launch files once those packages
exist.
