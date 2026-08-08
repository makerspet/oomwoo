# MCU I/O Firmware attempt by Creative-Dhanush

Code lives in its own repo, per this module's contribution model:
**[Creative-Dhanush/oomwoo-io-firmware](https://github.com/Creative-Dhanush/oomwoo-io-firmware)**

This is bring-up work on the CPU↔MCU link and the MCU-side safety logic from
[the io-board-interface contract](https://github.com/makerspet/oomwoo/tree/main/contributions/io-board-interface),
built and tested on a laptop before any board is involved.

## What is included

| File (in the linked repo) | Purpose |
|---|---|
| [`src/ow_frame.{h,cpp}`](https://github.com/Creative-Dhanush/oomwoo-io-firmware/blob/main/src/ow_frame.h) | CRC-16/CCITT-FALSE, little-endian byte helpers, and header/payload encode-decode for the wire format's 12 defined message types. |
| [`src/ow_stream_decoder.{h,cpp}`](https://github.com/Creative-Dhanush/oomwoo-io-firmware/blob/main/src/ow_stream_decoder.h) | Fixed-buffer streaming decoder: buffers partial frames across reads, resyncs one byte at a time after corruption. |
| [`docs/design-safety-core.md`](https://github.com/Creative-Dhanush/oomwoo-io-firmware/blob/main/docs/design-safety-core.md) | Design doc for the safety state machine: how sensor state gets in, how outbound frames get out, how reconnect/watchdog-reset are represented. |
| [`src/ow_safety_core.{h,cpp}`](https://github.com/Creative-Dhanush/oomwoo-io-firmware/blob/main/src/ow_safety_core.h) | The safety state machine itself — heartbeat timeout, setpoint expiry, bumper/cliff/wheel-drop/overcurrent/e-stop handling, with latched faults. |
| `test/`, `fuzz/` | Unity test suites per module, plus a differential fuzz harness for the stream decoder against the vendored Python reference. |

## Protocol / safety stance

MCU-owned safety stays MCU-owned, and stays dumb on purpose:

- the safety core only **stops** actuators (drive, cleaning motors) on a fault —
  it does not back up, scan, replan, or otherwise decide where the robot goes next
- latched faults (cliff, wheel-drop, e-stop) do not self-clear when the trigger
  condition goes away; only an explicit clear input releases them
- every entry point (`tick`, `on_frame`, `on_sensor_input`) takes the current time
  as an argument instead of reading a clock, so timeout behaviour is tested at
  exact millisecond boundaries with no sleeping
- no heap, no exceptions, no Arduino headers in the core — it has to build and run
  as plain hosted C++17 as well as on-target

Navigation, mapping, and anything that needs "complete" context (virtual walls,
path plan, IMU fusion) is explicitly left to the CPU side, not this module.

## Quick test

From the root of the linked repo:

```bash
git clone https://github.com/Creative-Dhanush/oomwoo-io-firmware
cd oomwoo-io-firmware
pip install -U platformio
pio test -e native
```

That runs the frame-codec, stream-decoder, and safety-core suites under
AddressSanitizer/UndefinedBehaviorSanitizer. CI in that repo also cross-builds
for `nucleo_g474re` and differentially fuzzes the stream decoder against the
vendored Python reference.

## What is not implemented

- No STM32 HAL/board bring-up yet — everything above is host-testable logic, not
  running on a Nucleo or the real I/O board.
- No motor PWM, motor-power-enable GPIO, charging, or IWDG integration — the
  safety core emits intents (stop, `SAFETY_EVENT`, `NACK`), a caller wires those
  to hardware.
- No measured worst-case reaction time under load — that needs the physical
  board and is a separate, maintainer-reviewed milestone (bring-up milestone 6
  in this module's [top-level README](../README.md)).

## Open questions

- The CPU-heartbeat timeout is implemented as a configurable value (not
  hardcoded), tracking the open "100, 150, or 250 ms?" question in the
  [io-board-interface contract](https://github.com/makerspet/oomwoo/tree/main/contributions/io-board-interface).
  No answer is assumed yet.
- Whether the timeout stop fires at exactly the deadline or strictly after it is
  currently a documented, tested choice in this repo, not a resolved spec answer.

Follow-up and status updates in [discussion #49](https://github.com/makerspet/oomwoo/discussions/49).
