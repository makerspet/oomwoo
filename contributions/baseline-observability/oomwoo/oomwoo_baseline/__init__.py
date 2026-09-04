"""OOMWOO Phase-0 baseline and observability harness.

Public submodules:
- ``oomwoo_baseline.metrics``: framework-agnostic KPI math (unit-testable).
- ``oomwoo_baseline.metrics_collector``: rclpy node that wires the math to topics.
- ``oomwoo_baseline.run_metadata``: capture ROS2/RMW/Git SHA/seed/scenario metadata.
- ``oomwoo_baseline.scenario_registry``: load the §5.1 scenario registry.
"""
