# CPU/MCU Interface Contract by xbattlax

This contribution turns the current I/O board hardware work into a concrete
software integration contract for the ROS2 bridge and STM32 firmware.

It is meant to unblock parallel work:

- the ROS2 developer can build a hardware bridge against stable topics and frame
  types
- the firmware developer can implement MCU-side safety and telemetry without
  waiting for the full robot stack
- the PCB designer can see which signals must be safety-owned by the MCU
- reviewers can spot unresolved hardware/software mismatches before layout

## What is included

| File | Purpose |
|---|---|
| [`docs/cpu_mcu_serial_contract.md`](docs/cpu_mcu_serial_contract.md) | Versioned serial framing, message catalog, watchdog rules, and payload shapes. |
| [`docs/ros2_mapping.md`](docs/ros2_mapping.md) | Mapping between serial frames and ROS2 topics/services/diagnostics. |
| [`docs/bringup_validation_plan.md`](docs/bringup_validation_plan.md) | Step-by-step validation from codec tests to bench robot bringup. |
| [`docs/hardware_contract_gaps.md`](docs/hardware_contract_gaps.md) | Open conflicts between architecture docs, I/O PCB RFC, KiCad specs, and part specs. |
| [`tools/oomwoo_mcu_frame.py`](tools/oomwoo_mcu_frame.py) | Dependency-free Python reference codec for the proposed frame format. |
| [`tools/sim_mcu.py`](tools/sim_mcu.py) | Tiny deterministic MCU-frame generator for bridge and log-parsing tests. |
| [`tests/test_oomwoo_mcu_frame.py`](tests/test_oomwoo_mcu_frame.py) | Unit tests for framing, CRC, streaming decode, and command payload validation. |

## Protocol stance

This proposal keeps the MCU safety path intentionally small:

- custom serial frames between CPU and MCU
- no micro-ROS on the safety-critical MCU path
- heartbeat-gated motion commands
- MCU-owned hard stops for bumper, cliff, wheel-drop, current faults, and stale
  CPU health
- standard ROS2 topics on the CPU side so simulation and hardware share the same
  public interface

The exact frame catalog can change, but the safety ownership should not: Linux
and ROS2 may request motion; the MCU decides whether motion is still safe.

## Quick test

From the repo root:

```bash
python3 -m unittest discover \
  -s contributions/io-board-interface/xbattlax/tests \
  -p 'test_*.py'
```

Generate sample frames:

```bash
python3 contributions/io-board-interface/xbattlax/tools/sim_mcu.py --count 3
```

## Review questions

1. Should the first implementation target UART TTL between CM4/CM5 and STM32, USB
   CDC, or support both behind the same frame format?
2. Should LiDAR UART terminate on the CPU, as the architecture text suggests, or
   on the MCU, as the current KiCad-derived notes suggest?
3. Should the bridge publish simple standard ROS messages first, then introduce
   custom OOMWOO messages after the hardware stabilizes?
4. Which timeout should be used for the MCU's hard motion stop after missed CPU
   heartbeats: 100 ms, 150 ms, or 250 ms?
