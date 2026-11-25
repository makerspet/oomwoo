# MCU I/O Board Firmware (CH32V307 + CH32L103 — bare-metal C)

The firmware that runs on the OOMWOO [I/O board](https://github.com/makerspet/oomwoo-pcb)
MCU. In OOMWOO's CPU/MCU split ([ARCHITECTURE.md §5.4](../../docs/ARCHITECTURE.md)),
the *CPU* (CM4/CM5-class module) runs ROS2/Nav2/SLAM, and the *MCU* on the I/O
board owns *motors, encoders, sensors, battery charging, and hard safety*. This
module is that MCU firmware. Its defining constraint: *safety must never depend on
Linux/ROS2* — and, per the architecture below, it must never depend on feature code
either.

> *Update (Nov 2026):* the board's MCU is now a WCH *CH32V307VCT6* (U13) with a
> *CH32L103C8T6* companion (U28), replacing the STM32G473 for cost and stock
> ([why](https://github.com/makerspet/oomwoo-pcb/blob/main/docs/mcu-ch32v307.md)).
> Starter firmware for both, built in CI, is in
> [oomwoo-firmware/mcu](https://github.com/makerspet/oomwoo-firmware/tree/main/mcu);
> pins come from `oomwoo_pins.h`. Portable C (framing, safety policy) carries over;
> STM32 HAL code and the Nucleo-G474 plan don't.

The full design lives in the firmware repo — this RFC is the request for
contribution and the acceptance bar.

> *Status — in progress.* Host-tested framing, safety-policy, simulator, and ROS2
> bridge work now exists, plus CH32 starter firmware; motor control, ISR integration, IWDG,
> charging, and measured cutoff times remain open. Build hardware milestones on
> *CH32V307 / CH32L103 dev boards* first; move to the real board when it is fabricated. Coordinate in
> the [firmware discussion](https://github.com/makerspet/oomwoo/discussions/49).

# Important References

- *Firmware repo + full spec* — [makerspet/oomwoo-firmware](https://github.com/makerspet/oomwoo-firmware).
  The repo README is the detailed architecture, peripheral map, and milestones; read it first.
- *Active implementations* — upstream framing bring-up
  [PR #2](https://github.com/makerspet/oomwoo-firmware/pull/2), ISR-owned CPU
  watchdog [PR #3](https://github.com/makerspet/oomwoo-firmware/pull/3) (written for the
  STM32G473; its HAL layer needs retargeting to the CH32V307), and
  [Creative-Dhanush's host-tested firmware/simulator](Creative-Dhanush) with its
  ROS2 bridge. These overlap at the protocol/policy layer; hardware integration
  and maintainer selection of the canonical upstream path are still open.
- *Board spec (authoritative)* — [oomwoo-pcb SPEC.md](https://github.com/makerspet/oomwoo-pcb/blob/main/docs/SPEC.md)
  — the motors, sensors, charging, and GPIO budget the firmware must serve (work in
  progress; note its open TODOs, e.g. the GPIO 36/46 bumper-label question).
- *CPU ↔ MCU serial contract* — [io-board-interface RFC](../io-board-interface) —
  the custom serial framing, command/telemetry set, and health/watchdog handshake.
- *System architecture* — [ARCHITECTURE.md §5.4](../../docs/ARCHITECTURE.md) — the CPU/MCU split and safety rationale.
- *Simulated MCU link* — the [oomwoo-install](https://github.com/makerspet/oomwoo-install)
  serial stub lets the CPU side be developed/tested before the board exists.
- [WCH CH32V307 SDK and examples](https://github.com/openwch/ch32v307)
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) · [Discord](https://discord.gg/3y2JKz5T25)

# The architecture, in one rule

The starter firmware is *bare-metal C, no RTOS yet* (see the
[firmware plan](https://github.com/makerspet/oomwoo-firmware/blob/main/docs/firmware-plan.md)):

- A 1 kHz SysTick paces a main-loop control tick: comms, control, telemetry, and
  the charging supervisor.
- Anything with a hard deadline runs in an interrupt: cliff LED timing, encoder and
  IR edges, the fan tachometer, the UARTs, and the hard-safety cutoffs.
- FreeRTOS (WCH ships a V307 port) may come later for USB, camera and ToF work, with
  the safety tick kept in an interrupt.

*The rule:* the safety and motor-control core is *structurally isolated* from
feature code — a bug or infinite loop in a new feature *cannot* defeat a
cliff-stop, an overcurrent cutoff, or the CPU watchdog, because those live in
interrupts and a hardware watchdog the main loop can't starve. (The earlier
STM32duino + FreeRTOS layering no longer applies.)

# Request for Contribution — Instructions

Phased bring-up (details and the peripheral map are in the firmware repo README):

- *Blink + WCH-LinkE flash + serial echo* on a CH32V307 dev board.
- *CPU serial link* — implement the [io-board-interface](../io-board-interface)
  framing + health/watchdog handshake; loopback tests green.
- *One drive motor, closed loop* — H-bridge PWM + encoder capture + velocity PID in
  the real-time core (the pattern every other motor follows).
- *All actuators* — suction fan (BLDC + FG), main/side brush, LiDAR spin, water
  pump, mop motors/servos — each with current sense.
- *All sensors* — cliff / dock / side-proximity IR (ADC), bumpers, wheel-drop, IMU
  (SPI), current channels.
- *Safety layer* — ISR-level cliff/bumper/wheel-drop stop, per-motor overcurrent
  limiting, IWDG, CPU watchdog/reset; *measure and document* each cutoff's
  worst-case reaction time; include a hazard note.
- *Charging supervisor* — power-path charger control, 0.5C cap, input DPM, graceful
  "insufficient charger" handling.
- *Integration* — run end-to-end against the CPU (or the simulated MCU serial tool).
- Contribute in the firmware repo; announce progress in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=).
- iterate with review
- TBD, expect the RFC to evolve

*Safety-critical code requires maintainer safety review before merge* (over-current,
thermal, short, mechanical pinch — include a hazard note).

## Acceptance criteria

Objective, measurable. Examples:
- *Deterministic real-time core* — measured, documented worst-case reaction time for
  each safety cutoff.
- *Safety is layer-independent* — a deliberately hung feature-level loop must *not*
  defeat a cliff-stop, overcurrent cutoff, or the CPU watchdog; demonstrate it.
- *Implements the [io-board-interface](../io-board-interface) serial contract* —
  loopback + integration tested.
- *Every actuator and sensor exercised* on the bench, documented, reproducible by
  someone else.
- *Charging behaves per spec* — 0.5C cap held; graceful degradation on a weak charger.
- *Safety-critical code passed maintainer safety review* with a hazard note.
- TBD, expect criteria to evolve.

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — a non-selected design is
still a valid learning exercise and a fallback.
