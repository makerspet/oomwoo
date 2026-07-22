import unittest

from pathlib import Path
import sys


PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "oomwoo_health_monitor"
sys.path.insert(0, str(PACKAGE_ROOT))

from oomwoo_health_monitor.core import (  # noqa: E402
    ComponentHeartbeat,
    ComponentSpec,
    HealthAggregator,
    HealthRoster,
)


class HealthAggregatorTest(unittest.TestCase):
    def _roster(self):
        return HealthRoster.from_components(
            "dock_cycle",
            (
                ComponentSpec("recovery_safety", critical=True, max_age_sec=0.5),
                ComponentSpec("dock_cycle", critical=True, max_age_sec=0.5),
                ComponentSpec("logger", critical=False, max_age_sec=0.5),
            ),
        )

    def _make_armed(self):
        aggregator = HealthAggregator(arm_window_sec=0.2)
        aggregator.update_roster(self._roster())
        aggregator.update_heartbeat(ComponentHeartbeat("recovery_safety", "ok", 1.0))
        aggregator.update_heartbeat(ComponentHeartbeat("dock_cycle", "ok", 1.0))
        aggregator.update_heartbeat(ComponentHeartbeat("logger", "ok", 1.0))
        aggregator.evaluate(1.0)
        return aggregator

    def test_no_roster_withholds_mcu_heartbeat(self):
        result = HealthAggregator().evaluate(0.0)

        self.assertEqual(result.state, "no_roster")
        self.assertFalse(result.emit_mcu_heartbeat)

    def test_missing_critical_component_faults(self):
        aggregator = HealthAggregator()
        aggregator.update_roster(self._roster())
        aggregator.update_heartbeat(ComponentHeartbeat("recovery_safety", "ok", 1.0))

        result = aggregator.evaluate(1.0)

        self.assertEqual(result.state, "fault")
        self.assertEqual(result.missing_critical, ("dock_cycle",))
        self.assertFalse(result.emit_mcu_heartbeat)

    def test_full_roster_arms_before_emitting_mcu_heartbeat(self):
        aggregator = self._make_armed()

        arming = aggregator.evaluate(1.1)
        healthy = aggregator.evaluate(1.25)

        self.assertEqual(arming.state, "arming")
        self.assertFalse(arming.emit_mcu_heartbeat)
        self.assertEqual(healthy.state, "healthy")
        self.assertTrue(healthy.emit_mcu_heartbeat)

    def test_stale_critical_component_stops_mcu_heartbeat(self):
        aggregator = self._make_armed()
        aggregator.evaluate(1.25)

        result = aggregator.evaluate(1.7)

        self.assertEqual(result.state, "fault")
        self.assertEqual(result.stale_critical, ("dock_cycle", "recovery_safety"))
        self.assertFalse(result.emit_mcu_heartbeat)

    def test_unhealthy_critical_component_faults(self):
        aggregator = HealthAggregator(arm_window_sec=0.0)
        aggregator.update_roster(self._roster())
        aggregator.update_heartbeat(ComponentHeartbeat("recovery_safety", "error", 2.0))
        aggregator.update_heartbeat(ComponentHeartbeat("dock_cycle", "ok", 2.0))

        result = aggregator.evaluate(2.0)

        self.assertEqual(result.state, "fault")
        self.assertEqual(result.unhealthy_critical, ("recovery_safety",))
        self.assertFalse(result.emit_mcu_heartbeat)

    def test_advisory_fault_does_not_block_mcu_heartbeat(self):
        aggregator = HealthAggregator(arm_window_sec=0.0)
        aggregator.update_roster(self._roster())
        aggregator.update_heartbeat(ComponentHeartbeat("recovery_safety", "ok", 3.0))
        aggregator.update_heartbeat(ComponentHeartbeat("dock_cycle", "ok", 3.0))

        result = aggregator.evaluate(3.0)

        self.assertEqual(result.state, "healthy_with_advisory_faults")
        self.assertEqual(result.advisory_faults, ("logger",))
        self.assertTrue(result.emit_mcu_heartbeat)

    def test_roster_change_disarms_until_new_critical_is_healthy(self):
        aggregator = self._make_armed()
        self.assertTrue(aggregator.evaluate(1.25).emit_mcu_heartbeat)
        aggregator.update_roster(
            HealthRoster.from_components(
                "dock_cycle",
                (
                    ComponentSpec("recovery_safety", critical=True, max_age_sec=0.5),
                    ComponentSpec("dock_cycle", critical=True, max_age_sec=0.5),
                    ComponentSpec("localization", critical=True, max_age_sec=0.5),
                ),
            )
        )

        result = aggregator.evaluate(1.3)

        self.assertEqual(result.state, "fault")
        self.assertEqual(result.missing_critical, ("localization",))
        self.assertFalse(result.emit_mcu_heartbeat)


if __name__ == "__main__":
    unittest.main()
