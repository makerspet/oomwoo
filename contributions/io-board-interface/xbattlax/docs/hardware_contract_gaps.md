# Hardware/Software Contract Gaps

Status: review ledger for integration decisions that affect firmware and ROS2.

This file does not try to settle hardware design decisions. It records conflicts
or stale text found while comparing:

- `docs/ARCHITECTURE.md`
- `docs/SOFTWARE_INTERFACES.md`
- `contributions/io-pcb/README.md`
- `contributions/part-specs/OsakaTX/*`
- `makerspet/oomwoo-io-board/docs/SPEC.md`
- KiCad-derived notes from the I/O board repository

## Decision ledger

| ID | Topic | Current conflict | Why it matters | Suggested next action |
|---|---|---|---|---|
| `HW-SW-001` | MCU protocol | Project docs include both an educational micro-ROS path and a safety-critical custom serial path. | Firmware architecture and bridge tooling diverge if this is not settled. | Treat custom serial as the safety path; keep micro-ROS only for non-safety experiments. |
| `HW-SW-002` | Drive wheel connector | `io-pcb` references a 6-pin JST PH2.0 pinout; part specs show the physical Roborock wheel has a 7-pin cable, while the current OOMWOO I/O board schematic uses a 5-pin signal connector and on-board H-bridge. | Connector choice affects PCB layout, harnessing, and encoder/motor ownership. | Reconcile the selected wheel module connector before layout and document the final board-side connector. |
| `HW-SW-003` | LiDAR UART owner | Architecture text says the CPU receives LiDAR serial; KiCad-derived notes describe LiDAR serial routed to the STM32. | ROS2 driver placement, timestamping, and serial bandwidth differ by owner. | Decide whether the MCU controls only LiDAR motor power/RPM or also forwards LiDAR scan data. |
| `HW-SW-004` | Bumper naming and type | Some specs still say "bumper switch"; schematic notes identify ITR9606 optical interrupters. The I/O board GPIO list also repeats `Bumper switch 1`. | Safety events and mechanical integration need left/right semantics and sensor polarity. | Rename to bumper optical interrupter where confirmed; fix duplicate GPIO label after schematic review. |
| `HW-SW-005` | Side brush quantity | Some text says side brush quantity 1; KiCad-derived notes show left/right side brush connectors. | Firmware payload should know whether one or two channels are independently controlled. | Decide whether v1 has one physical side brush or two independently driven side brushes. |
| `HW-SW-006` | Fan driver capability | Specs say suction fan BLDC with PWM/FG; schematic notes show a high-side P-MOSFET and tach feedback. | The bridge needs to know whether fan percent maps to a power switch, PWM input, or external ESC. | Bench-test fan module pinout and confirm whether MCU PWM controls fan electronics or only supply power. |
| `HW-SW-007` | Charger/dock contact semantics | I/O board spec says dock contacts provide about 20 V DC, but dock-present sensing is not fully specified. | Dock-cycle and battery status need reliable dock-present vs charging-active flags. | Add explicit dock-present and charging-active signals to the power telemetry contract. |

## Proposed bridge policy while decisions are open

- Keep serial message fields generic enough to support either one or two side
  brush channels later.
- Publish bitfields for bumper/cliff/wheel-drop until custom messages are worth
  freezing.
- Do not expose raw GPIO numbering as a ROS2 public interface.
- Use firmware-reported capability flags during bridge startup so hardware
  variants can differ without breaking the ROS2 graph.
- Require each hardware-affecting decision to update this ledger, the I/O board
  spec, and the ROS2 mapping together.
