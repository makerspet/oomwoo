# Compute Benchmark & Memory Reduction

Measure whether OOMWOO can keep ROS2/Nav2/SLAM onboard while reducing the
minimum compute target from a comfortable 4 GB class system toward a practical
2 GB class system.

This module is for repeatable measurements, not guesses. It should help compare
Python/C++ ROS2 nodes, ROS2 composable-node layouts where supported, process
layout changes, and later optional Rust experiments under the same workload.

> Status: in progress. Use the ROS2 Jazzy development container and the current
> simulation stack where possible. Hardware runs on Pi 4, CM4, CM5, or compatible
> modules are especially useful when available.

## Current Working Assumptions

- The consumer vacuum profile keeps SLAM and navigation onboard.
- The practical near-term target is Pi 4 / CM4-class compute with 4 GB RAM.
- The stretch target is to reduce the minimum memory requirement toward 2 GB
  without giving up ROS2.
- The compute-module direction is CM4/CM5 or compatible modules on a carrier
  board; ignore the older RK3562 reference path.
- The MCU owns motors, sensors, safety, battery/charging supervision, watchdogs,
  and the custom serial protocol.
- STM32G070RBT6 is a strong MCU candidate because of its GPIO/ADC count, low
  cost, and LQFP manufacturability, while the MCU choice remains reviewable.
- The MVP 2D LiDAR target is 5 Hz with no scan dropping.
- Rust/rclrs is an optional late-summer integration candidate, not a baseline
  dependency today.

Context: this module follows the compute discussion in
[issue #18](https://github.com/makerspet/oomwoo/issues/18).

## Request For Contribution

Submit a benchmark contribution under:

```text
contributions/compute-benchmark/<your-github-username>/
```

Include:

- a reproducible benchmark plan
- scripts that capture RSS/PSS/CPU/startup timing where possible
- a hardware/software run matrix
- a compute BOM table with regional price and stock fields
- clear notes on ROS distro, RMW, hardware, RAM size, LiDAR rate, and scenario
- a short decision record after measurements

## Metrics

Minimum useful metrics:

| Metric | Why it matters |
|---|---|
| RSS/PSS per process | Shows where memory is actually going. |
| CPU idle / mapping / navigation | Separates always-on cost from workload cost. |
| Startup time | Exposes heavy node initialization and launch overhead. |
| LiDAR update rate | Confirms the benchmark is not cheating by dropping scans. |
| Nav2/SLAM headroom | Determines whether 2 GB is plausible with ROS2 retained. |
| Recovery-event latency | Keeps safety-adjacent nodes honest under optimization. |

## Strategies To Compare

1. Current Python/C++ baseline.
2. ROS2 composable nodes where supported, plus launch/process layout changes.
3. C++/rclcpp for selected hot or always-on custom nodes.
4. Optional Rust/rclrs spike for selected custom nodes after dev-image setup is
   reproducible.

Rust should only move from optional to recommended if it demonstrates a useful
RSS/PSS or latency improvement and does not make the default Jazzy developer
experience fragile.

## Acceptance Criteria

- Measurements are reproducible by another contributor.
- The benchmark records hardware, RAM, ROS distro, RMW, scenario, and git SHA.
- Results distinguish process RSS from PSS when PSS is available.
- Benchmarks do not reduce LiDAR update rate below the target unless explicitly
  marked as an experiment.
- The contribution explains whether the result supports 4 GB only, 2 GB as a
  stretch target, or a different hardware class.
- BOM notes include module/board, carrier, power, cooling, storage, MCU add-ons,
  regional price, and stock status.
