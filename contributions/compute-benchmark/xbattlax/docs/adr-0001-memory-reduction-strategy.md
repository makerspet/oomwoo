# ADR 0001: Memory-Reduction Strategy

## Status

Proposed.

## Context

OOMWOO should remain approachable for builders, so the first consumer vacuum
profile should run SLAM and navigation onboard. Requiring a separate workstation
for mapping would make the regular product harder to build and use.

The maintainer has clarified these current assumptions:

- Pi 4 / CM4-class compute with 4 GB RAM is a realistic near-term baseline.
- Reducing toward 2 GB while keeping ROS2 would be valuable.
- CM4/CM5 or compatible modules are the compute-module direction.
- The older RK3562 reference schematic should be ignored for new compute-module
  planning.
- The MCU role is fixed around motors, sensors, safety, battery/charging
  control, watchdogs, and custom serial protocol.
- ESP32/micro-ROS is better suited to an educational/offboard profile than to
  the consumer safety/controller role.

## Decision

Use this priority order for memory-reduction work:

1. Measure the current Python/C++ ROS2 baseline.
2. Try ROS2 composable nodes where supported, plus launch/process layout
   improvements first.
3. Consider C++/rclcpp for selected memory-heavy or latency-sensitive custom
   nodes when composable layout is insufficient.
4. Keep Rust/rclrs as an optional late-summer 2026 spike for selected custom
   nodes, not as a baseline dependency today.

Rust/rclrs should be evaluated seriously, but only promoted if:

- RSS/PSS or latency wins are meaningful against Python and C++ baselines
- the Jazzy build/setup is reproducible in the OOMWOO dev image
- contributor onboarding remains reasonable
- the node selected for porting is small enough to keep the experiment bounded

## Consequences

- The first benchmark contribution can avoid adding Rust dependencies.
- The benchmark still leaves a clear path for a later rclrs experiment.
- The project can pursue the 4 GB -> 2 GB target with lower dependency risk.
- Results should identify whether memory pressure comes from custom Python
  nodes, ROS2 process layout, Nav2/SLAM, or other runtime overhead.

## Open Questions

- Which launch graph should be the canonical benchmark workload?
- Which ROS2 RMW should be the baseline for memory measurements?
- Which node is the best first Rust/rclrs candidate if measurements justify it?
- How should PSS be collected on target hardware when permissions differ?
- What minimum headroom should qualify a 2 GB target as realistic?
