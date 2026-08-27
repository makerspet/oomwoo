"""Unit tests for the OOMWOO baseline harness (stdlib unittest only).

These exercise the framework-agnostic logic so they run without ROS2::

    python3 -m unittest oomwoo_baseline.test.test_metrics -v
"""

import math
import os
import sys
import unittest

# Make the package importable when run from this file's directory.
# __file__ is .../oomwoo/oomwoo_baseline/test/test_metrics.py -> parent of
# oomwoo_baseline is .../oomwoo, which must be on sys.path.
_PKG_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _PKG_ROOT not in sys.path:
    sys.path.insert(0, _PKG_ROOT)

from oomwoo_baseline.metrics import MetricsAggregator  # noqa: E402
from oomwoo_baseline.scenario_registry import get_scenario  # noqa: E402


class TestMetricsAggregator(unittest.TestCase):
    def _feed_constant_scan(self, agg, n=200, period=0.2, start=1000.0):
        t = start
        for i in range(n):
            agg.record_scan(header_stamp_sec=t, recv_sec=t)
            t += period

    def test_scan_rate(self):
        agg = MetricsAggregator()
        self._feed_constant_scan(agg, n=201, period=0.2)
        snap = agg.snapshot()
        # 200 intervals over 40 s => 5 Hz
        self.assertAlmostEqual(snap["scan"]["rate_hz"], 5.0, places=1)
        self.assertTrue(snap["scan"]["meets_target"])

    def test_tf_latency_percentiles(self):
        agg = MetricsAggregator()
        # feed 100 latencies 0..99 ms
        for i in range(100):
            agg.record_tf(header_stamp_sec=0.0, recv_sec=(i) / 1000.0)
        stats = agg.snapshot()["tf_latency"]
        self.assertEqual(stats["n"], 100)
        self.assertAlmostEqual(stats["p50_ms"], 49.5, places=0)
        self.assertAlmostEqual(stats["max_ms"], 99.0, places=0)

    def test_odom_drift_consistency(self):
        agg = MetricsAggregator()
        # 101 records at 0.1 m/s, dt 0.1 s => 100 intervals => 1.0 m.
        for i in range(101):
            t = i * 0.1
            x = i * 0.01
            agg.record_odom(stamp_sec=t, x=x, y=0.0, vx=0.1, vy=0.0, recv_sec=t)
        snap = agg.snapshot()["odom"]
        self.assertAlmostEqual(snap["integrated_distance_m"], 1.0, places=2)
        self.assertAlmostEqual(snap["pose_distance_m"], 1.0, places=2)
        self.assertAlmostEqual(snap["drift_ratio"], 1.0, places=2)

    def test_cmd_vel_staleness(self):
        agg = MetricsAggregator(cmd_vel_stale_sec=0.5)
        # moving at 0 and 0.7 (gap 0.7 > 0.5) -> one stale event
        agg.record_cmd_vel(recv_sec=0.0, has_motion=True)
        agg.record_cmd_vel(recv_sec=0.7, has_motion=True)
        self.assertEqual(agg.snapshot()["cmd_vel"]["stale_events"], 1)

    def test_bumper_rising_edge(self):
        agg = MetricsAggregator()
        agg.record_bumper("left", has_contact=True, recv_sec=1.0)
        agg.record_bumper("left", has_contact=True, recv_sec=1.1)  # still in contact
        agg.record_bumper("left", has_contact=False, recv_sec=1.2)
        agg.record_bumper("left", has_contact=True, recv_sec=1.3)  # new event
        self.assertEqual(agg.snapshot()["bumper"]["left_events"], 2)

    def test_map_free_ratio(self):
        agg = MetricsAggregator()
        data = [0] * 70 + [100] * 20 + [-1] * 10  # 70 free, 20 occ, 10 unknown
        agg.record_map(width=10, height=10, data=data)
        snap = agg.snapshot()["map"]
        self.assertEqual(snap["width"], 10)
        self.assertAlmostEqual(snap["free_ratio"], 0.7, places=2)
        self.assertAlmostEqual(snap["unknown_ratio"], 0.1, places=2)

    def test_recovery_latency(self):
        agg = MetricsAggregator()
        agg.record_status(recv_sec=10.0, state="RECOVERING", reason_code="RECOVERY_STARTED")
        agg.record_status(recv_sec=10.4, state="RECOVERED", reason_code="RECOVERED")
        self.assertAlmostEqual(agg.snapshot()["recovery"]["mean_ms"], 400.0, places=0)


class TestScenarioRegistry(unittest.TestCase):
    def _registry(self):
        return {
            "default_seed": 42,
            "scenarios": [
                {
                    "id": "single_room_empty",
                    "name": "单房间空旷",
                    "world": "worlds/single.world",
                    "initial_pose": {"x": 0.0, "y": 0.0, "yaw": 0.0},
                    "tags": ["mapping"],
                },
                {
                    "id": "kidnapped_random_pose",
                    "name": "被抱起",
                    "world": "worlds/single.world",
                    "initial_pose": {"x": 1.5, "y": 1.0, "yaw": 1.57},
                    "seed": 7,
                    "tags": ["localization"],
                },
            ],
        }

    def test_resolve_merges_default_seed(self):
        scen = get_scenario(self._registry(), "single_room_empty")
        self.assertIsNotNone(scen)
        self.assertEqual(scen["seed"], 42)

    def test_resolve_keeps_explicit_seed(self):
        scen = get_scenario(self._registry(), "kidnapped_random_pose")
        self.assertEqual(scen["seed"], 7)

    def test_missing_scenario_returns_none(self):
        self.assertIsNone(get_scenario(self._registry(), "does_not_exist"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
