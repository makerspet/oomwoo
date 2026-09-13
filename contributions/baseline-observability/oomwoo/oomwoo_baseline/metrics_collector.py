"""rclpy node that collects Phase-0 KPIs from the OOMWOO baseline topics.

Subscribes to the MVP baseline surface defined in
``docs/SOFTWARE_INTERFACES.md`` and feeds :mod:`oomwoo_baseline.metrics`.
Writes a JSON snapshot (on a timer and at shutdown) and a rolling CSV time
series for LiDAR rate / TF latency so drops are visible.

All topic names are relative and resolve against the default launch namespace,
matching the other OOMWOO contributions.
"""

from __future__ import annotations

import csv
import json
import os
from time import time as _wall

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.exceptions import ROSInterruptException
from rclpy.node import Node
from rclpy.qos import (
    QoSPresetProfiles,
    QoSProfile,
    DurabilityPolicy,
    HistoryPolicy,
    ReliabilityPolicy,
    qos_profile_sensor_data,
)
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, OccupancyGrid
try:
    from ros_gz_interfaces.msg import Contacts
except ImportError:  # bumper message type unavailable until ros_gz_interfaces is installed
    Contacts = None
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage

from oomwoo_baseline.metrics import MetricsAggregator


def _stamp_to_sec(stamp) -> float:
    return float(stamp.sec) + float(stamp.nanosec) / 1e9


def _has_real_contact(msg: Contacts) -> bool:
    for contact in msg.contacts:
        names = {contact.collision1.name, contact.collision2.name}
        if not any("ground_plane" in n.split("::") for n in names):
            return True
    return False


class MetricsCollectorNode(Node):
    def __init__(self):
        super().__init__("oomwoo_baseline_metrics")

        self.declare_parameter("metrics_json", "/tmp/oomwoo_baseline_metrics.json")
        self.declare_parameter("metrics_csv", "/tmp/oomwoo_baseline_timeseries.csv")
        self.declare_parameter("scan_drop_gap_sec", 0.4)
        self.declare_parameter("cmd_vel_stale_sec", 0.5)
        self.declare_parameter("write_period_sec", 5.0)

        json_path = self.get_parameter("metrics_json").value
        csv_path = self.get_parameter("metrics_csv").value
        drop_gap = float(self.get_parameter("scan_drop_gap_sec").value)
        stale = float(self.get_parameter("cmd_vel_stale_sec").value)
        period = float(self.get_parameter("write_period_sec").value)

        self._json_path = json_path
        self._csv_path = csv_path
        self._agg = MetricsAggregator(
            scan_drop_gap_sec=drop_gap, cmd_vel_stale_sec=stale
        )
        self._csv_header_written = not (csv_path and os.path.exists(csv_path))
        self._start_wall = _wall()

        # QoS: sensor-data for /scan, transient-local for /map, default for rest.
        sensor_qos = qos_profile_sensor_data
        map_qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.TRANSIENT_LOCAL,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.create_subscription(LaserScan, "scan", self._scan_cb, sensor_qos)
        self.create_subscription(Odometry, "odom", self._odom_cb, 10)
        self.create_subscription(TFMessage, "tf", self._tf_cb, 10)
        self.create_subscription(Twist, "cmd_vel", self._cmd_vel_cb, 10)
        if Contacts is not None:
            self.create_subscription(Contacts, "bumper_left", self._bumper_left_cb, 10)
            self.create_subscription(Contacts, "bumper_right", self._bumper_right_cb, 10)
        else:
            self.get_logger().warn(
                "ros_gz_interfaces not found; bumper monitoring disabled. "
                "Install ros-humble-ros-gz-interfaces to enable bumper KPIs."
            )
        self.create_subscription(OccupancyGrid, "map", self._map_cb, map_qos)
        self.create_subscription(String, "oomwoo/status", self._status_cb, 10)

        self.create_timer(period, self._write_timer_cb)
        self.get_logger().info(
            f"oomwoo_baseline metrics collector started; json={json_path} csv={csv_path}"
        )

    # ---- callbacks ---------------------------------------------------- #
    def _scan_cb(self, msg: LaserScan):
        now = self.get_clock().now().nanoseconds / 1e9
        self._agg.record_scan(_stamp_to_sec(msg.header.stamp), now)

    def _odom_cb(self, msg: Odometry):
        now = self.get_clock().now().nanoseconds / 1e9
        p = msg.pose.pose.position
        tw = msg.twist.twist
        self._agg.record_odom(
            _stamp_to_sec(msg.header.stamp),
            p.x, p.y, tw.linear.x, tw.linear.y, now,
        )

    def _tf_cb(self, msg: TFMessage):
        now = self.get_clock().now().nanoseconds / 1e9
        if not msg.transforms:
            return
        self._agg.record_tf(_stamp_to_sec(msg.transforms[0].header.stamp), now)

    def _cmd_vel_cb(self, msg: Twist):
        now = self.get_clock().now().nanoseconds / 1e9
        moving = abs(msg.linear.x) > 1e-3 or abs(msg.angular.z) > 1e-3
        self._agg.record_cmd_vel(now, moving)

    def _bumper_left_cb(self, msg: Contacts):
        now = self.get_clock().now().nanoseconds / 1e9
        self._agg.record_bumper("left", _has_real_contact(msg), now)

    def _bumper_right_cb(self, msg: Contacts):
        now = self.get_clock().now().nanoseconds / 1e9
        self._agg.record_bumper("right", _has_real_contact(msg), now)

    def _map_cb(self, msg: OccupancyGrid):
        self._agg.record_map(msg.info.width, msg.info.height, msg.data)

    def _status_cb(self, msg: String):
        now = self.get_clock().now().nanoseconds / 1e9
        try:
            payload = json.loads(msg.data)
            state = payload.get("state")
            reason = payload.get("reason_code")
        except (json.JSONDecodeError, AttributeError):
            return
        if state is not None:
            self._agg.record_status(now, str(state), str(reason) if reason else "")

    # ---- writers ------------------------------------------------------ #
    def _write_timer_cb(self):
        self._write_json()
        self._write_csv_row()

    def _write_json(self):
        try:
            with open(self._json_path, "w", encoding="utf-8") as fh:
                json.dump(self._agg.snapshot(), fh, indent=2, sort_keys=True)
        except OSError as exc:
            self.get_logger().warn(f"failed to write metrics json: {exc}")

    def _write_csv_row(self):
        if not self._csv_path:
            return
        snap = self._agg.snapshot()
        elapsed = _wall() - self._start_wall
        row = {
            "elapsed_sec": round(elapsed, 1),
            "scan_rate_hz": round(snap["scan"]["rate_hz"], 3)
            if not _isnan(snap["scan"]["rate_hz"]) else "",
            "tf_p99_ms": round(snap["tf_latency"]["p99_ms"], 2)
            if not _isnan(snap["tf_latency"]["p99_ms"]) else "",
            "odom_integrated_m": round(snap["odom"]["integrated_distance_m"], 2),
            "bumper_total": snap["bumper"]["total_events"],
            "cmd_vel_stale": snap["cmd_vel"]["stale_events"],
        }
        try:
            with open(self._csv_path, "a", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(row.keys()))
                if self._csv_header_written:
                    writer.writeheader()
                    self._csv_header_written = False
                writer.writerow(row)
        except OSError as exc:
            self.get_logger().warn(f"failed to write metrics csv: {exc}")


def _isnan(x) -> bool:
    return isinstance(x, float) and x != x


def main(args=None):
    rclpy.init(args=args)
    node = MetricsCollectorNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException, ROSInterruptException):
        pass
    except Exception as exc:
        if "context is not valid" not in str(exc):
            raise
    finally:
        try:
            node._write_json()
        except Exception:  # noqa: BLE001 - best effort on shutdown
            pass
        node.destroy_node()
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception as exc:
            if "rcl_shutdown already called" not in str(exc):
                raise


if __name__ == "__main__":
    main()
