# Health Monitor Prototype by xbattlax

This contribution turns the health-monitor RFC into a concrete, testable
software-watchdog contract.

It answers the follow-up from `oomwoo#33`: `/cmd_vel` holding is only one local
freshness concern. The more general safety path is a stack health aggregator that
checks all expected critical components and emits one MCU-facing stack heartbeat
only while the active task is fully healthy.

## What This Adds

- a dependency-free health aggregator core
- a roster contract for critical vs. advisory components
- freshness and health-level checks for component heartbeats
- a fail-safe arming window before MCU heartbeat emission
- immediate heartbeat withholding on missing, stale, or unhealthy critical
  components
- advisory-component reporting without stopping the robot
- a JSONL simulator for startup, stale-node, recovery, and advisory-fault traces
- unit tests covering the deadman behavior
- a proposed public ROS2 topic contract in `docs/SOFTWARE_INTERFACES.md`

## Files

| File | Purpose |
|---|---|
| [`tools/oomwoo_health_monitor.py`](tools/oomwoo_health_monitor.py) | Pure Python stack-health aggregator core. |
| [`tools/sim_health_monitor.py`](tools/sim_health_monitor.py) | Deterministic JSONL scenario runner. |
| [`tests/test_oomwoo_health_monitor.py`](tests/test_oomwoo_health_monitor.py) | Regression tests for arming, stale detection, advisory handling, and roster changes. |
| [`docs/stack_watchdog_contract.md`](docs/stack_watchdog_contract.md) | Detailed heartbeat, roster, aggregate, and MCU behavior contract. |
| [`docs/recovery_safety_integration.md`](docs/recovery_safety_integration.md) | How recovery-safety should feed the monitor without relying on `/cmd_vel` timeouts. |

## Test

```bash
python3 -m unittest discover \
  -s contributions/health-monitor/xbattlax/tests \
  -p 'test_*.py'
```

## Run the Simulator

```bash
python3 contributions/health-monitor/xbattlax/tools/sim_health_monitor.py
```

The output is JSON Lines with the current stack state, stale/missing/unhealthy
components, advisory faults, and whether the MCU heartbeat would be emitted.

## Intended ROS2 Path

Initial ROS2 integration can use JSON over `std_msgs/msg/String` while message
types are still unsettled:

- `/oomwoo/health/roster`
- `/oomwoo/health/component`
- `/oomwoo/health/stack`
- `/oomwoo/health/mcu_heartbeat`

Once the contract stabilizes, these should become typed OOMWOO messages or a
small adapter around standard diagnostics.

## Design Rule

Component heartbeats must come from the component's real work path: control
cycle completed, scan processed, recovery decision evaluated, map update
consumed, and so on. A free-running heartbeat timer is explicitly not enough,
because it can keep ticking while the component's useful work loop is wedged.
