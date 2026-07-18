# I/O Board Software Interface

The I/O board is where OOMWOO's ROS2 software meets the real robot: wheel
drivers, cleaning motors, cliff sensors, bumper sensors, dock sensing, power
state, battery charging, and the MCU watchdog.

This contribution area is for the CPU-to-MCU software contract that sits between
the Raspberry Pi Compute Module and the STM32 I/O board firmware.

## Why this matters

The hardware can move quickly only if the firmware and ROS2 work have a stable
interface to build against. The goal is to define the contract before the board
is fully frozen:

- which signals are owned by the MCU vs the CPU
- what commands the CPU can send to the MCU
- what telemetry the MCU publishes back
- what always stays safety-critical and independent of Linux/ROS2
- how the ROS2 hardware bridge maps serial frames into standard ROS topics
- how to validate the contract in simulation, with loopback tests, then on real
  hardware

## Scope

Included:

- CPU-to-MCU serial protocol proposals
- ROS2 topic/service/action mapping for the hardware bridge
- safety and watchdog behavior
- signal ownership tables tied back to the I/O board schematic and part specs
- simulators, parsers, replay tools, and tests that make the protocol
  reproducible

Not included:

- final STM32 firmware implementation
- final PCB layout decisions
- Linux kernel drivers
- app/cloud/Home Assistant UI

## References

- [I/O + motor-driver PCB RFC](../io-pcb)
- [I/O board repository](https://github.com/makerspet/oomwoo-io-board)
- [Architecture: CPU/MCU split](../../docs/ARCHITECTURE.md)
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md)
- [Part specs](../part-specs)

## Submit

A PR to `contributions/io-board-interface/<your-github-username>/` should include:

- a short README explaining the proposed contract
- protocol docs or schemas
- a mapping from hardware signals to ROS2 topics/services
- testable tooling where possible
- known open decisions that need maintainer or PCB-designer input

## Acceptance criteria

- The contract is versioned and can evolve without breaking old frames silently.
- Stale motion commands fail safe.
- MCU-owned safety events do not depend on ROS2 being alive.
- Message rates and payload sizes are realistic for the chosen serial link.
- The proposal links back to current hardware references and calls out conflicts
  instead of hiding them.
- At least the framing/parser pieces are testable without hardware.
