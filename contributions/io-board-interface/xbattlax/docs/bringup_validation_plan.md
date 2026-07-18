# Bringup and Validation Plan

Status: draft test plan for the CPU/MCU bridge and STM32 firmware.

## Phase 0: protocol tests, no hardware

Goal: make the frame format boring before anyone debugs it on a bench.

Checks:

- codec round-trips every message type
- corrupted CRC is rejected
- streaming decoder resynchronizes after noise
- out-of-range actuator payloads are rejected
- sample MCU logs can be replayed into the bridge

Command:

```bash
python3 -m unittest discover \
  -s contributions/io-board-interface/xbattlax/tests \
  -p 'test_*.py'
```

## Phase 1: serial loopback

Goal: prove the Linux side can sustain the target rate.

Setup:

- USB UART loopback or pseudo-terminal pair
- bridge writes `HEARTBEAT` and `DRIVE_SETPOINT`
- loopback process returns `FAST_TELEMETRY`

Measurements:

- frame drop rate
- CRC reject count
- end-to-end decode latency
- CPU percent and memory using the compute benchmark sampler
- behavior on cable unplug/replug

Pass criteria:

- no stale `/cmd_vel` command keeps moving after bridge stop
- bridge enters error state when telemetry disappears
- diagnostics expose serial errors and reconnect attempts

## Phase 2: STM32 development board

Goal: test firmware task timing before the real I/O board is ready.

Firmware stubs:

- heartbeat watchdog
- command parser
- safety-event publisher
- fake encoder counters
- fake ADC/status values
- GPIO output stubs for motor enables

Failure injection:

- stop heartbeat
- send bad CRC
- send unknown command
- send out-of-range drive setpoint
- trigger bumper/cliff/wheel-drop GPIO inputs

Pass criteria:

- motor-enable GPIO returns safe/off after heartbeat timeout
- safety events are emitted and latched
- boot starts with all motion outputs disabled
- firmware loop timing stays below the chosen real-time budget

## Phase 3: I/O board bench test

Goal: validate the actual board with loads disabled or current-limited.

Checks:

- power rails stable with CPU attached
- MCU reset and CPU reset lines work as intended
- bumper, cliff, wheel-drop, and dock inputs toggle expected bits
- fan/brush/wheel PWM outputs are present but current-limited
- charger and dock flags report sane values

Do not connect full motor loads until e-stop, heartbeat timeout, and current
limit behavior are verified.

## Phase 4: rolling base, no cleaning load

Goal: drive safely with wheels only.

Checks:

- `/cmd_vel` forward/reverse/rotate produces expected wheel direction
- encoder sign and scale match odometry
- `joint_states` and `/odom` are monotonic and plausible
- bumpers stop motion before ROS2 recovery reacts
- wheel-drop and cliff inputs stop motion immediately

Pass criteria:

- stale command timeout stops the base
- CPU process kill stops the base via MCU watchdog
- emergency stop remains latched until explicit clear

## Phase 5: cleaning loads

Goal: add fan, brushes, pump, and LiDAR motor one at a time.

Checks:

- current sense values are plausible
- brush overcurrent stops affected output
- fan tach/FG feedback changes with speed
- LiDAR RPM control stays in usable range if the MCU owns the motor
- thermal behavior is logged

Pass criteria:

- no cleaning actuator can remain on after heartbeat timeout or e-stop
- overcurrent produces a visible ROS2 diagnostic and status reason
- recovery and dock-cycle modules can subscribe to the same public interfaces

## Artifacts to collect

- firmware build ID and protocol version
- bridge version and git SHA
- serial log sample
- ROS2 bag with `/cmd_vel`, `/odom`, `/joint_states`, `/battery_state`,
  `/diagnostics`, and OOMWOO safety topics
- compute benchmark CSV from the target SBC
- short written decision note for any changed message field or timeout
