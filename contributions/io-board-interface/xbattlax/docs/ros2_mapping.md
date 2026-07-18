# ROS2 Mapping for the I/O Board Bridge

Status: draft mapping for a future `oomwoo_mcu_bridge` node.

## Bridge role

The bridge translates between public ROS2 interfaces and the CPU/MCU serial
contract. It should be thin: ROS2 owns high-level behavior, the MCU owns hard
safety and motor IO.

```text
Nav2 / recovery / jobs / diagnostics
                |
                v
        oomwoo_mcu_bridge
                |
        CPU/MCU serial frames
                |
                v
        STM32 I/O board firmware
```

## Subscribed ROS2 inputs

| Topic/service | Type | Bridge action | MCU frame |
|---|---|---|---|
| `/cmd_vel` | `geometry_msgs/msg/Twist` | Convert linear/angular velocity to bounded setpoint. | `DRIVE_SETPOINT` |
| `/oomwoo/safety/e_stop` | `std_msgs/msg/Bool` | Latch or clear software e-stop request. | `ESTOP_SET` |
| `/oomwoo/cleaning/main_brush_pct` | `std_msgs/msg/UInt8` | Set main brush speed percent. | `CLEANING_MOTORS_SET` |
| `/oomwoo/cleaning/side_brush_pct` | `std_msgs/msg/UInt8` | Set side brush speed percent. | `CLEANING_MOTORS_SET` |
| `/oomwoo/cleaning/fan_pct` | `std_msgs/msg/UInt8` | Set suction fan speed percent. | `CLEANING_MOTORS_SET` |
| `/oomwoo/cleaning/pump_pct` | `std_msgs/msg/UInt8` | Set water pump speed percent. | `CLEANING_MOTORS_SET` |
| `/oomwoo/lidar/motor_pct` | `std_msgs/msg/UInt8` | Set LiDAR motor PWM if the MCU owns LiDAR motor control. | `LIDAR_MOTOR_SET` |
| `/oomwoo/io/clear_faults` | `std_srvs/srv/Trigger` or custom service | Clear selected latched faults after safe conditions return. | `CLEAR_LATCHED_FAULT` |

## Published ROS2 outputs

| Topic | Type | Source frame | Notes |
|---|---|---|---|
| `/odom` | `nav_msgs/msg/Odometry` | `FAST_TELEMETRY` | Optional if bridge computes wheel odometry; otherwise publish wheel data only. |
| `/joint_states` | `sensor_msgs/msg/JointState` | `FAST_TELEMETRY` | Wheel joint positions from encoder ticks. |
| `/battery_state` | `sensor_msgs/msg/BatteryState` | `POWER_TELEMETRY` | Voltage, current, charge state, dock/charging flags. |
| `/oomwoo/io/bumper` | `std_msgs/msg/UInt8` initially | `FAST_TELEMETRY`, `SAFETY_EVENT` | Bitfield until a custom message exists. |
| `/oomwoo/io/cliff` | `std_msgs/msg/UInt8` initially | `FAST_TELEMETRY`, `SAFETY_EVENT` | Bitfield for cliff sensors. |
| `/oomwoo/io/wheel_drop` | `std_msgs/msg/UInt8` initially | `FAST_TELEMETRY`, `SAFETY_EVENT` | Bitfield for wheel-drop sensors. |
| `/oomwoo/io/dock` | `std_msgs/msg/UInt8` initially | `POWER_TELEMETRY` | Dock-present and charging bits. |
| `/oomwoo/io/mcu_status` | `diagnostic_msgs/msg/DiagnosticArray` | `MCU_DIAGNOSTIC` | Watchdog, loop timing, CRC drops, reset reason. |
| `/diagnostics` | `diagnostic_msgs/msg/DiagnosticArray` | All telemetry | Standard integration with ROS tooling. |
| `/oomwoo/status` | `std_msgs/msg/String` initially | Bridge policy + safety frames | JSON status compatible with current recovery prototype. |

## QoS and rates

| Interface | QoS/rate |
|---|---|
| `/cmd_vel` input | Reliable or best-effort with small queue; stale values must not be replayed. |
| `DRIVE_SETPOINT` serial output | 20-50 Hz while active, short duration field. |
| `FAST_TELEMETRY` serial input | 50-100 Hz target. |
| Battery/power topics | 1-5 Hz. |
| Diagnostics | 1 Hz plus event bursts. |
| Safety events | Reliable where possible, repeated while latched. |

## Lifecycle behavior

The bridge should be a lifecycle node or equivalent state machine.

| State | Behavior |
|---|---|
| `unconfigured` | No serial connection, no actuator commands. |
| `inactive` | Serial may be open, but no heartbeat and no motion outputs. |
| `active` | Heartbeat running, setpoints accepted, telemetry published. |
| `error` | Heartbeat stopped, setpoints zeroed, diagnostics explain cause. |

On deactivate, shutdown, or crash, the heartbeat stops. The MCU then stops
motion independently.

## Arbitration

Only one ROS2 component should write `/cmd_vel` at a time. The bridge should not
solve high-level arbitration; it should enforce low-level safety:

- clamp max linear/angular velocity
- clamp setpoint duration
- send zero setpoints on deactivate
- stop forwarding motion while e-stop, cliff, wheel-drop, or CPU timeout is
  latched

## Message evolution

Start with standard ROS2 messages for the first bridge:

- `geometry_msgs/msg/Twist`
- `sensor_msgs/msg/BatteryState`
- `sensor_msgs/msg/JointState`
- `diagnostic_msgs/msg/DiagnosticArray`
- small `std_msgs` bitfields where custom messages are not yet worth freezing

Once the real hardware signals stabilize, promote the bitfields into an
`oomwoo_msgs` package.
