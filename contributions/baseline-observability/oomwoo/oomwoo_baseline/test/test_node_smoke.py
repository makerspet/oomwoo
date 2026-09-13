"""Node-level smoke tests for the OOMWOO baseline-observability package.

These instantiate the *real* ROS 2 nodes to catch constructor-time failures
that pure-logic unit tests cannot:

  * bad QoS constant usage (e.g. ``QoSPresetProfiles.SENSOR_DATA`` instead of
    the ``qos_profile_sensor_data`` member) -- this crashed the node on
    startup until fixed;
  * missing / mis-named message imports (``ros_gz_interfaces`` bumper);
  * subscription / timer setup errors.

They run inside the colcon test environment (a ROS 2 context is available)
and do **not** require a running Gazebo robot or any peer nodes.

Run:
    colcon test --packages-select oomwoo_baseline
(or ``scripts/colcon_validate.sh`` which sets PYTEST_DISABLE_PLUGIN_AUTOLOAD=1)
"""
from __future__ import annotations

import unittest

import rclpy
from rclpy.node import Node

from oomwoo_baseline.metrics_collector import MetricsCollectorNode
from oomwoo_baseline.run_metadata import capture_run_metadata


class NodeSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not rclpy.ok():
            rclpy.init()

    @classmethod
    def tearDownClass(cls):
        if rclpy.ok():
            rclpy.shutdown()

    def test_metrics_collector_constructs_and_subscribes(self):
        """Constructing the node must not raise (regression guard for the
        QoS / import bugs) and must set up the baseline subscriptions."""
        node = MetricsCollectorNode()
        try:
            self.assertIsInstance(node, Node)
            # scan / odom / tf / cmd_vel / map / oomwoo_status -> >= 6 subs.
            # (bumper_left/right only when ros_gz_interfaces is installed.)
            # node.subscriptions may be a list or generator across rclpy
            # versions, so materialise it first.
            self.assertGreaterEqual(len(list(node.subscriptions)), 6)
        finally:
            node.destroy_node()

    def test_run_metadata_pure(self):
        meta = capture_run_metadata(
            repo_root=".", scenario="single_room", seed=1
        )
        self.assertEqual(meta["scenario"], "single_room")
        self.assertEqual(meta["seed"], 1)
        self.assertEqual(meta["lidar_target_hz"], 5.0)
        for key in ("captured_at_utc", "ros_distro", "git_sha"):
            self.assertIn(key, meta)


if __name__ == "__main__":
    unittest.main()
