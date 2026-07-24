# OOMWOO ROS2 Software Interfaces

> Status: DRAFT. This is the shared software contract for simulation-first
> contributions. It reflects the current `urdf-gazebo-sim` package and should be
> updated whenever a module needs a new public topic, service, action, frame, or
> parameter.

## Purpose

OOMWOO software modules are meant to be swappable. A contributor should be able
to build `clean-and-map`, `nav-localize`, `recovery-safety`, `dock-cycle`, or
`cleaning-jobs` without depending on another module's private implementation.

This document defines the public ROS2 surface area those modules can share while
the hardware is still evolving. It is not a final hardware API.

## Naming rules

- Public names below are shown as root topics, for example `/scan`. Launch files
  and node configs may use relative names such as `scan` when they resolve to
  the same root topic in the default launch.
- Use REP-103 frames and SI units.
- Prefer standard ROS2/Nav2 message types before adding custom OOMWOO messages.
- If a module introduces a new public interface, document the producer, consumer,
  message type, QoS expectation, and failure behavior in its README and update
  this file.
- Simulation-only details, such as Gazebo collision entity names, must not leak
  into cross-module contracts unless they are explicitly marked as simulation
  diagnostics.

## Frames

| Frame | Owner | Meaning |
|---|---|---|
| `map` | SLAM/localization | Global map frame used by SLAM, AMCL, Nav2, and saved maps. |
| `odom` | Base odometry | Locally continuous odometry frame. |
| `base_footprint` | Robot description / odometry | Planar base frame for navigation. |
| `base_link` | Robot description | Main robot body frame. Hardware modules should reference this once geometry is frozen. |
| `base_scan` | Robot description | 2D LiDAR frame. |

Open decision: `base_link` origin, reference plane, robot diameter, and height
envelope are still defined in `ARCHITECTURE.md`.

## Baseline Topics

These topics are provided by the current Gazebo simulation or standard Nav2/SLAM
bringup and should be treated as the MVP baseline.

| Topic | Type | Direction | Producer | Consumers |
|---|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Command | Teleop, Nav2 velocity smoother, recovery nodes | Gazebo diff-drive / base controller |
| `/odom` | `nav_msgs/msg/Odometry` | State | Gazebo odometry / base controller | SLAM, AMCL, Nav2, recovery and job logic |
| `/tf` | `tf2_msgs/msg/TFMessage` | State | Robot state publisher, odometry, SLAM/localization | All pose-aware modules |
| `/joint_states` | `sensor_msgs/msg/JointState` | State | Gazebo joint state publisher / hardware base | Robot state publisher, diagnostics |
| `/scan` | `sensor_msgs/msg/LaserScan` | Sensor | 2D LiDAR / Gazebo LiDAR | SLAM, AMCL, Nav2 costmaps, wall following |
| `/map` | `nav_msgs/msg/OccupancyGrid` | State | SLAM or map server | Nav2, cleaning, zones, visualization |
| `/bumper_left` | `ros_gz_interfaces/msg/Contacts` in Gazebo | Sensor | Gazebo left contact sensor | Recovery, safety, clean-and-map obstacle handling |
| `/bumper_right` | `ros_gz_interfaces/msg/Contacts` in Gazebo | Sensor | Gazebo right contact sensor | Recovery, safety, clean-and-map obstacle handling |

### Bumper events

The current simulation publishes raw Gazebo contact messages:

- Message type: `ros_gz_interfaces/msg/Contacts`
- Contact list field: `contacts`
- Per-contact fields: `collision1`, `collision2`, `positions`, `normals`,
  `depths`, `wrenches`

Consumers should treat `len(msg.contacts) > 0` as a bumper event after filtering
out ground-plane contacts. Do not read a `collisions` field; that belongs to the
single-contact message type and is not what the bridge publishes.

Hardware may eventually replace raw Gazebo contacts with a normalized bumper
message. Until that decision is made, module submissions should isolate the
Gazebo-specific parsing behind a small adapter.

## Nav2 Interfaces

Modules should reuse Nav2 actions and servers where possible.

| Interface | Type | Typical consumer |
|---|---|---|
| `/navigate_to_pose` | `nav2_msgs/action/NavigateToPose` | `nav-localize`, `cleaning-jobs`, `dock-cycle` |
| `/navigate_through_poses` | `nav2_msgs/action/NavigateThroughPoses` | Coverage, room jobs, dock approach |
| Nav2 behavior server | `spin`, `backup`, `drive_on_heading`, `wait` behaviors | Recovery and local fallback logic |
| Costmaps | Nav2 local/global costmap topics | Obstacle handling, zones, diagnostics |
| Map saver | Nav2 map saver service/CLI | `clean-and-map`, `nav-localize` |

If a module needs to command motion directly, it must define how it arbitrates
with Nav2 and recovery nodes so two nodes do not fight over `/cmd_vel`.

## Module Contracts

| Module | Inputs | Outputs / public behavior |
|---|---|---|
| `urdf-gazebo-sim` | `/cmd_vel` | Publishes `/scan`, `/odom`, `/tf`, `/joint_states`, `/bumper_left`, `/bumper_right`; provides worlds and robot description. |
| `clean-and-map` | `/scan`, `/odom`, `/tf`, bumper events, optional Nav2 actions | Drives first-pass coverage, produces a complete map, defines a done condition, saves map artifacts. |
| `nav-localize` | Saved map, `/scan`, `/odom`, `/tf`, Nav2 bringup | Provides known-map navigation, relocalization, and map-resume behavior. |
| `recovery-safety` | Bumper events, future cliff/wheel-drop/pickup/e-stop signals, Nav2 failures | Stops or gates motion, runs bounded recoveries, publishes clear pause/error status. |
| `floor-care` | `/scan`, map/coverage context, future surface sensor | Provides wall/edge following, surface classification, and mop actuator decisions. |
| `cleaning-jobs` | Saved map, zones, coverage progress, battery/bin/mop status, Nav2 actions | Provides start/pause/resume/cancel/status job behavior suitable for a future Home Assistant layer. |
| `dock-cycle` | Nav2/localization, dock marker, battery/service state | Provides undock, return-to-dock, precise docking, recharge/service completion, and find-dock fallback. |
| `live-robot-bringup` | Hardware drivers, same logical topics | Validates that hardware exposes the same public interfaces as the simulation. |

## Status and Errors

The final robot status API is still open. Until it is selected, modules that
need status reporting should document:

- `state`: short machine-readable state, for example `cleaning`, `recovering`,
  `paused`, `docked`, or `error`
- `reason_code`: stable machine-readable reason, for example `BUMPER_STUCK`,
  `LOCALIZATION_LOST`, or `LOW_BATTERY`
- `message`: human-readable explanation
- `recoverable`: whether a resume command is expected to work
- `source`: module name that produced the status

Open decision: choose the transport and type for cross-module status, likely a
standard diagnostic message or a small OOMWOO-specific message package.

## QoS and Parameters

- `use_sim_time` should be true in simulation launch files.
- Sensor streams such as `/scan` should use sensor-data QoS where configurable.
- `/map` and saved-map metadata should be available to late joiners where the
  producer supports transient-local durability.
- Command topics should use small queues and should fail safe: stale commands
  must not keep the robot moving.

## Hardware Bridge Draft

The physical robot will expose the simulation-level contract through an MCU
bridge instead of direct Gazebo plugins. The current draft lives in
[`contributions/io-board-interface`](../contributions/io-board-interface).

The bridge should translate standard ROS2 commands into the custom CPU/MCU
serial protocol and publish hardware telemetry back as standard ROS2 topics
where possible.

| ROS2 interface | Direction | Hardware source/sink |
|---|---|---|
| `/cmd_vel` | CPU -> MCU | Bounded drive setpoint with a short expiry. |
| `/joint_states` | MCU -> CPU | Wheel encoder ticks converted to wheel joint state. |
| `/odom` | MCU/bridge -> CPU | Optional wheel odometry derived from encoder ticks. |
| `/battery_state` | MCU -> CPU | Battery voltage/current and charge state. |
| `/oomwoo/io/bumper` | MCU -> CPU | Bumper bitfield or future OOMWOO message. |
| `/oomwoo/io/cliff` | MCU -> CPU | Cliff bitfield or future OOMWOO message. |
| `/oomwoo/io/wheel_drop` | MCU -> CPU | Wheel-drop bitfield or future OOMWOO message. |
| `/oomwoo/safety/e_stop` | CPU -> MCU | Software e-stop request; MCU remains final safety authority. |
| `/camera/obstacle/image_raw` | CPU -> ROS2 | Optional front obstacle camera stream, about 130 degree FoV in simulation. |
| `/camera/obstacle/camera_info` | CPU -> ROS2 | Camera calibration for the front obstacle camera. |
| `/oomwoo/dock_ir/front_left` | MCU -> CPU | Final-approach dock IR homing strength. |
| `/oomwoo/dock_ir/front_right` | MCU -> CPU | Final-approach dock IR homing strength. |
| `/oomwoo/dock_ir/search_left` | MCU -> CPU | Left-side dock beacon search strength. |
| `/oomwoo/dock_ir/search_right` | MCU -> CPU | Right-side dock beacon search strength. |
| `/oomwoo/dock/final_cmd_vel` | CPU -> MCU | Optional low-speed final-docking command after Nav2 reaches predock pose. |
| `/diagnostics` | MCU/bridge -> CPU | Watchdog, CRC drops, reset reason, fault bits. |

Hard safety events must be handled by the MCU even if ROS2 is down. ROS2 can
request motion, report state, and run recovery behaviors, but stale CPU
heartbeats or unsafe sensor states must stop motion at the MCU layer.

## Stack Health Monitor Draft

The software stack should expose one aggregate health/deadman path to the MCU
instead of relying on independent stale-command behavior for every topic.

Initial simulation-first topics can use JSON over `std_msgs/msg/String` until an
OOMWOO message package exists:

| ROS2 interface | Producer | Consumer | Purpose |
|---|---|---|---|
| `/oomwoo/health/roster` | Task launch / job manager | Health monitor | Latched expected-component roster for the active task; marks components critical or advisory. |
| `/oomwoo/health/component` | Safety-critical nodes | Health monitor | Work-path heartbeat with component id, health level, stamp, and optional detail. |
| `/oomwoo/health/stack` | Health monitor | Diagnostics / app layer | Aggregated state: no roster, arming, healthy, healthy with advisory faults, or fault. |
| `/oomwoo/health/mcu_heartbeat` | Health monitor / bridge | MCU bridge | Single stack-health heartbeat forwarded to the MCU only while all expected critical components are fresh and well. |

Fail-safe behavior:

- no roster means no MCU heartbeat
- a missing, stale, or unhealthy critical component stops the MCU heartbeat
- advisory component faults are reported but do not stop the robot
- the monitor has an arming window and withholds the MCU heartbeat until the full
  critical roster is confirmed healthy
- component heartbeats must be emitted from useful work paths, not from
  independent timers that can keep running while the component is wedged

## Validation Checklist

A module submission that depends on the MVP simulation should document how to
check the interfaces it uses. At minimum:

```bash
ros2 topic list
ros2 topic echo /scan --once
ros2 topic echo /odom --once
ros2 topic echo /bumper_left
ros2 topic echo /bumper_right
ros2 run tf2_tools view_frames
```

For Nav2-based modules, also document how to send a `NavigateToPose` goal and
how to confirm `/cmd_vel` arbitration is safe.

## Miscellaneous

- PR your packages into the official distribution [makerspet/oomwoo-install](https://github.com/makerspet/oomwoo-install)
- put your ROS2 packages under `/ros_ws/src` (don't create another colcon workspace under `~/`)
- follow conventions of being able to select a robot package using `kaia config robot.model oomwoo_one`, see [tutorial](https://makerspet.com/blog/simulate-oomwoo-one-robot-vacuum-in-gazebo-with-ros-2/)

## Open Decisions

- Final hardware bumper/cliff/wheel-drop message shape.
- Robot-wide status/error message type and topic.
- Battery, dust-bin, mop, and dock service state interfaces.
- Localization-confidence interface for relocalization and kidnap detection.
- Job action/service API for start, pause, resume, cancel, and status.
