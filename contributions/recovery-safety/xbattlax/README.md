# Recovery Safety Prototype by xbattlax

This contribution provides a first ROS2 recovery-and-safety package for the
OOMWOO recovery-safety RFC. It is deliberately small, deterministic, and
simulation-first:

- a bounded recovery ladder for bumper, wedged, no-path, and lost-localization
  situations
- immediate safe stop for e-stop, cliff, wheel-drop, and pickup events
- pause-and-alert when the ladder is exhausted
- a structured JSON status topic suitable for later Home Assistant integration
- unit tests for guaranteed termination and safety responses

The core ladder lives in pure Python, so it can be regression-tested without a
running ROS graph. The ROS2 node is a thin adapter around that core.

## Package

`oomwoo_recovery_safety`

Location:

```text
contributions/recovery-safety/xbattlax/oomwoo_recovery_safety
```

## Interfaces

### Subscribed topics

| Topic | Type | Purpose |
|---|---|---|
| `/bumper_left` | `ros_gz_interfaces/msg/Contacts` | Trigger left-bumper recovery after filtering ground-plane contacts. |
| `/bumper_right` | `ros_gz_interfaces/msg/Contacts` | Trigger right-bumper recovery after filtering ground-plane contacts. |
| `/oomwoo/recovery/event` | `std_msgs/msg/String` | Manual/test trigger. Payload examples: `wedged`, `no_valid_path`, `localization_lost`, `bumper_front`. |
| `/oomwoo/recovery/behavior_result` | `std_msgs/msg/String` | Optional external result for the current behavior: `succeeded`, `failed`, or JSON `{"outcome":"succeeded"}`. |
| `/oomwoo/safety/e_stop` | `std_msgs/msg/Bool` | Immediate non-recoverable pause. |
| `/oomwoo/safety/cliff` | `std_msgs/msg/Bool` | Immediate safety pause. |
| `/oomwoo/safety/wheel_drop` | `std_msgs/msg/Bool` | Immediate safety pause. |
| `/oomwoo/safety/pickup` | `std_msgs/msg/Bool` | Immediate safety pause for pickup/kidnap handoff. |
| `/oomwoo/recovery/reset` | `std_msgs/msg/Bool` | Reset a paused/recovered controller when true. |

### Published topics

| Topic | Type | Purpose |
|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Short bounded motion commands for recovery. |
| `/oomwoo/status` | `std_msgs/msg/String` | JSON status with `state`, `reason_code`, `message`, `recoverable`, `source`, and recovery metadata. |
| `/oomwoo/recovery/command` | `std_msgs/msg/String` | JSON command for non-motion actions such as `clear_costmap`. |

## Build

From the OOMWOO ROS2 container:

```bash
source /opt/ros/jazzy/setup.bash
cd /workspace
colcon build \
  --base-paths contributions/recovery-safety/xbattlax/oomwoo_recovery_safety \
  --packages-select oomwoo_recovery_safety
```

## Test

```bash
source /opt/ros/jazzy/setup.bash
cd /workspace
colcon test \
  --base-paths contributions/recovery-safety/xbattlax/oomwoo_recovery_safety \
  --packages-select oomwoo_recovery_safety
colcon test-result --verbose
```

The tests cover:

- bounded escalation to pause-and-alert
- successful recovery stopping the ladder
- e-stop and safety events entering safe pause
- ignored duplicate triggers while already recovering
- JSON status shape

## Run

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 launch oomwoo_recovery_safety recovery_safety.launch.py
```

Manual trigger example:

```bash
ros2 topic pub --once /oomwoo/recovery/event std_msgs/msg/String "{data: bumper_front}"
```

Mark the current behavior as successful:

```bash
ros2 topic pub --once /oomwoo/recovery/behavior_result std_msgs/msg/String "{data: succeeded}"
```

Trigger e-stop:

```bash
ros2 topic pub --once /oomwoo/safety/e_stop std_msgs/msg/Bool "{data: true}"
```

## Current limitations

- This is a first integration scaffold, not a full Nav2 behavior-server plugin.
- `clear_costmap` is published as an intent on `/oomwoo/recovery/command`; a
  future adapter should call Nav2 costmap clear services directly.
- Success detection is external for now. If no `succeeded` result arrives before
  a behavior's timeout, the node escalates to the next behavior and eventually
  pauses.
- Cliff, wheel-drop, and pickup are represented as boolean topics until the
  hardware/simulation message contract is finalized.
