#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "oomwoo_health_monitor"))

from oomwoo_health_monitor.core import (  # noqa: E402
    ComponentHeartbeat,
    ComponentSpec,
    HealthAggregator,
    HealthRoster,
)


def main() -> int:
    aggregator = HealthAggregator(arm_window_sec=0.25)
    roster = HealthRoster.from_components(
        "cleaning_job",
        (
            ComponentSpec("recovery_safety", critical=True, max_age_sec=0.30),
            ComponentSpec("nav2_controller", critical=True, max_age_sec=0.30),
            ComponentSpec("localization", critical=True, max_age_sec=0.50),
            ComponentSpec("telemetry_logger", critical=False, max_age_sec=1.00),
        ),
    )

    for now_sec, event in (
        (0.00, "boot_no_roster"),
        (0.05, "roster_published"),
        (0.10, "recovery_healthy"),
        (0.15, "nav2_healthy"),
        (0.20, "localization_healthy"),
        (0.30, "advisory_healthy"),
        (0.50, "armed"),
        (0.90, "nav2_stale"),
        (1.00, "nav2_recovers"),
        (1.36, "advisory_stale_only"),
    ):
        if event == "roster_published":
            aggregator.update_roster(roster)
        elif event == "recovery_healthy":
            aggregator.update_heartbeat(ComponentHeartbeat("recovery_safety", "ok", now_sec))
        elif event == "nav2_healthy":
            aggregator.update_heartbeat(ComponentHeartbeat("nav2_controller", "ok", now_sec))
        elif event == "localization_healthy":
            aggregator.update_heartbeat(ComponentHeartbeat("localization", "ok", now_sec))
        elif event == "advisory_healthy":
            aggregator.update_heartbeat(ComponentHeartbeat("telemetry_logger", "ok", now_sec))
        elif event == "armed":
            for component_id in ("recovery_safety", "nav2_controller", "localization"):
                aggregator.update_heartbeat(ComponentHeartbeat(component_id, "ok", now_sec))
        elif event == "nav2_recovers":
            aggregator.update_heartbeat(ComponentHeartbeat("nav2_controller", "ok", now_sec))
            aggregator.update_heartbeat(ComponentHeartbeat("recovery_safety", "ok", now_sec))
            aggregator.update_heartbeat(ComponentHeartbeat("localization", "ok", now_sec))
        elif event == "advisory_stale_only":
            for component_id in ("recovery_safety", "nav2_controller", "localization"):
                aggregator.update_heartbeat(ComponentHeartbeat(component_id, "ok", now_sec))

        result = aggregator.evaluate(now_sec)
        print(result.to_json())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
