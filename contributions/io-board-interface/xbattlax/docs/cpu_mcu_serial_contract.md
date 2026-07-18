# CPU/MCU Serial Contract Draft

Status: draft integration contract, not final firmware.

## Design goals

- Keep safety-critical firmware small, deterministic, and independent of Linux.
- Let the CPU run ROS2, Nav2, SLAM, mapping, docking behavior, and UI-facing
  logic.
- Let the MCU own motors, encoder counting, power switching, charger control,
  cliff/bumper/wheel-drop response, and watchdog decisions.
- Make stale or corrupt commands stop the robot rather than continue motion.
- Keep the frame format simple enough for STM32 firmware, Python tests, and a
  future C++/Rust bridge to share.

## Link

Initial target:

| Property | Draft value |
|---|---|
| Physical link | UART TTL or USB CDC, same framing |
| Baud rate | 1 Mbaud preferred, 115200 supported for early bench tests |
| Byte order | Little-endian payload fields |
| Framing | Binary fixed header + payload + CRC-16/CCITT-FALSE |
| Transport retries | None for fast setpoints; ACK/NACK for configuration only |
| Motion timeout | MCU stops drive and cleaning motors if heartbeat or setpoint expires |

## Frame format

```text
offset  size  field
0       2     magic: ASCII "OW"
2       1     protocol version: 1
3       1     flags
4       2     sequence number
6       2     message type
8       2     payload length
10      N     payload
10+N    2     CRC-16/CCITT-FALSE over header + payload
```

The magic bytes are included in the CRC. A decoder must reject frames with the
wrong version, impossible length, or bad CRC. A streaming decoder may discard
noise until the next `OW` magic.

## Message ID ranges

| Range | Direction | Meaning |
|---|---|---|
| `0x0001-0x00ff` | CPU -> MCU | control, heartbeat, reset, and configuration |
| `0x0100-0x01ff` | CPU -> MCU | actuator setpoints |
| `0x7000-0x70ff` | both | ACK/NACK and protocol diagnostics |
| `0x8000-0x80ff` | MCU -> CPU | state, telemetry, and safety events |

## Minimum message catalog

| ID | Name | Direction | Rate | Payload |
|---|---|---|---|---|
| `0x0001` | `HEARTBEAT` | CPU -> MCU | 20-50 Hz | `u32 cpu_time_ms`, `u8 cpu_mode` |
| `0x0002` | `ESTOP_SET` | CPU -> MCU | event | `u8 active`, `u16 reason` |
| `0x0003` | `CLEAR_LATCHED_FAULT` | CPU -> MCU | event | `u16 fault_mask` |
| `0x0101` | `DRIVE_SETPOINT` | CPU -> MCU | 20-50 Hz | `i16 linear_mm_s`, `i16 angular_mrad_s`, `u16 duration_ms` |
| `0x0102` | `CLEANING_MOTORS_SET` | CPU -> MCU | 1-10 Hz | `u8 main_brush_pct`, `u8 side_brush_pct`, `u8 fan_pct`, `u8 pump_pct` |
| `0x0103` | `LIDAR_MOTOR_SET` | CPU -> MCU | 1-10 Hz | `u8 pwm_pct` |
| `0x0104` | `LED_SET` | CPU -> MCU | event | `u8 led_id`, `u8 mode`, `u8 brightness_pct` |
| `0x7001` | `ACK` | both | event | `u16 acked_seq`, `u16 status` |
| `0x7002` | `NACK` | both | event | `u16 rejected_seq`, `u16 error_code` |
| `0x8000` | `MCU_HELLO` | MCU -> CPU | boot/event | `u16 firmware_major`, `u16 firmware_minor`, `u32 build_id` |
| `0x8001` | `FAST_TELEMETRY` | MCU -> CPU | 50-100 Hz | encoder ticks + fast safety flags |
| `0x8002` | `SAFETY_EVENT` | MCU -> CPU | event + latch | `u16 event`, `u8 active`, `u16 detail` |
| `0x8003` | `POWER_TELEMETRY` | MCU -> CPU | 1-5 Hz | battery, charger, current, thermal summary |
| `0x8004` | `MCU_DIAGNOSTIC` | MCU -> CPU | 1 Hz/event | watchdog, loop timing, dropped frames, fault bits |

## Safety events

The MCU should emit `SAFETY_EVENT` when a hard safety input changes and keep a
latched fault bit until the fault is cleared or explicitly acknowledged.

| Code | Event | MCU behavior |
|---|---|---|
| `1` | `BUMPER_LEFT` | Stop drive immediately; allow bounded recovery only if cliff/wheel-drop are clear. |
| `2` | `BUMPER_RIGHT` | Stop drive immediately; allow bounded recovery only if cliff/wheel-drop are clear. |
| `3` | `CLIFF_LEFT` | Stop drive and cleaning motors; require safe retreat or human intervention. |
| `4` | `CLIFF_RIGHT` | Stop drive and cleaning motors; require safe retreat or human intervention. |
| `5` | `WHEEL_DROP_LEFT` | Stop drive and cleaning motors; latch until wheel contact returns. |
| `6` | `WHEEL_DROP_RIGHT` | Stop drive and cleaning motors; latch until wheel contact returns. |
| `7` | `BRUSH_OVERCURRENT` | Stop affected brush; report detail with brush ID. |
| `8` | `FAN_OVERCURRENT` | Stop fan; keep drive under MCU policy. |
| `9` | `CPU_HEARTBEAT_TIMEOUT` | Stop all motion-capable outputs; optionally reset CPU after debounce. |
| `10` | `ESTOP` | Stop all motion-capable outputs; latch until explicit clear. |

## Timing rules

- CPU publishes `HEARTBEAT` at 20-50 Hz while the hardware bridge is active.
- CPU publishes `DRIVE_SETPOINT` with a short `duration_ms`; the MCU zeroes drive
  output when the setpoint expires.
- Draft maximum `DRIVE_SETPOINT.duration_ms`: 250 ms.
- Draft MCU hard-stop after missed heartbeat: 150 ms.
- Configuration commands can be ACKed. Fast setpoints should be replaced by newer
  setpoints rather than retried.

## Failure behavior

| Failure | Expected MCU response |
|---|---|
| Bad CRC | Drop frame, increment diagnostic counter. |
| Unknown message ID | NACK if the frame is otherwise valid. |
| Valid but out-of-range setpoint | Reject, stop affected actuator, emit diagnostic. |
| CPU heartbeat timeout | Stop drive and cleaning motors, emit `CPU_HEARTBEAT_TIMEOUT`. |
| Serial link reconnect | MCU sends `MCU_HELLO`, keeps actuators off until fresh heartbeat and setpoint arrive. |
| MCU watchdog reset | Start with all motion outputs disabled and report reset reason. |

## Reference codec

The Python reference codec in `tools/oomwoo_mcu_frame.py` implements this frame
format and a few payload helpers. It is not the final bridge, but it gives the
firmware, ROS2, and test work a shared executable reference.
