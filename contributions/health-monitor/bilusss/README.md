# Health-monitor verification kit by bilusss

Repository: [bilusss/oomwoo-health-kit](https://github.com/bilusss/oomwoo-health-kit)

A verification kit for this RFC rather than another aggregator: an MCU stand-in
(heartbeat watchdog plus `cmd_vel` gate), a work-path heartbeat helper, launch
tests that inject faults on real DDS, and load / sim-clock / stopping-distance
benchmarks in Gazebo headless. It speaks the topic contract in
[`docs/SOFTWARE_INTERFACES.md`](../../../docs/SOFTWARE_INTERFACES.md) and has been
run against [xbattlax/health-monitor](https://github.com/xbattlax/health-monitor)
at commit `b2b9796`, unmodified.

Measured results, method and limits:
[docs/FINDINGS.md](https://github.com/bilusss/oomwoo-health-kit/blob/main/docs/FINDINGS.md).

Simulation only; the stand-in is Python, not firmware.
