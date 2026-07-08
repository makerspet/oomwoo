# Compute Benchmark Plan by xbattlax

This contribution turns the compute discussion in issue #18 into a concrete
benchmark scaffold for OOMWOO.

The immediate goal is to measure whether OOMWOO can keep onboard ROS2, Nav2, and
SLAM while reducing the practical memory target from 4 GB toward 2 GB. The first
optimization path should be ROS2 composable nodes where supported, plus
launch/process layout. Rust with rclrs is kept as a serious optional spike for
late August / September 2026, gated by measurements and dev-image
reproducibility.

## Scope

Included:

- a Linux `/proc`-based process sampler for RSS/PSS/CPU
- a run matrix template for repeatable benchmark scenarios
- a compute BOM template for board/module, carrier, power, cooling, storage,
  MCU add-ons, regional pricing, and stock status
- a short architecture decision record for the current memory-reduction plan

Not included yet:

- a Rust/rclrs node implementation
- a C++/rclcpp equivalent node
- physical Pi 4 / CM4 / CM5 results
- automated launch files for full SLAM/Nav2 runs

## Hardware Profiles To Record

| Profile | Purpose | Notes |
|---|---|---|
| Dev machine | Reference only | Useful for repeatability, not a robot target. |
| Pi 4 4 GB | Minimum prior-art target | Validate onboard SLAM/Nav2 feasibility. |
| CM4 4 GB | Consumer carrier-board target | Low profile and product-friendly. |
| CM5 4 GB+ | Higher headroom target | Useful if camera/NPU alternatives are evaluated. |
| 2 GB class SBC/module | Stretch target | Requires real measured headroom, not assumptions. |
| ESP32 educational profile | Offboard ROS2/SLAM learning setup | Not a consumer autonomous vacuum profile. |

## Measurement Scenarios

Start with these scenarios:

1. ROS2 graph idle after launch.
2. SLAM running with 5 Hz LiDAR input and no scan dropping.
3. Nav2 navigating on a known map.
4. Recovery/safety node idle.
5. Recovery/safety event burst.
6. Same workload after composable-node or process-layout changes.
7. Later: same selected custom node in Python, C++/rclcpp, and Rust/rclrs.

## Using The Sampler

Run this inside the Linux ROS2 environment while the target workload is already
running:

```bash
bash contributions/compute-benchmark/xbattlax/scripts/measure_ros_processes.sh \
  --pattern 'ros2|component_container|python3|slam_toolbox|nav2' \
  --duration 60 \
  --interval 2 \
  --label slam_5hz_baseline \
  --output /tmp/oomwoo-slam-5hz-baseline.csv
```

The script writes CSV with:

- timestamp
- sample index
- label
- PID
- process name
- CPU percent
- RSS KiB
- PSS KiB when `/proc/<pid>/smaps_rollup` is available
- command line

PSS is usually more useful than RSS for ROS2 systems because shared libraries and
middleware pages can make RSS look worse than the actual proportional memory
pressure.

## Templates

- `templates/run_matrix.csv`: planned benchmark runs and environment details.
- `templates/compute_bom.csv`: compute BOM and regional stock/price snapshot.

Copy the templates into a results folder for real benchmark submissions. Do not
edit old result rows after a run; add a new row for a new measurement.

## Expected Decision Output

Each benchmark batch should end with a short note:

- current measured minimum RAM class
- biggest memory users
- whether composable nodes helped
- whether any Python node is worth porting to C++ or Rust
- whether Rust/rclrs setup is reproducible enough to keep testing
- what hardware profile the result supports
