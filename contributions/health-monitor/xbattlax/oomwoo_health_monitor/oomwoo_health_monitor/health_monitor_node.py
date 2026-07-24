from __future__ import annotations

from dataclasses import asdict
import json
from time import monotonic

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.exceptions import ROSInterruptException
from rclpy.node import Node
from std_msgs.msg import String

from oomwoo_health_monitor.core import (
    ComponentHeartbeat,
    ComponentSpec,
    HealthAggregator,
    HealthRoster,
)


class HealthMonitorNode(Node):
    def __init__(self):
        super().__init__("health_monitor")
        self._aggregator = HealthAggregator(arm_window_sec=0.25)
        self._heartbeat_sequence = 0

        self._stack_pub = self.create_publisher(String, "oomwoo/health/stack", 10)
        self._mcu_pub = self.create_publisher(String, "oomwoo/health/mcu_heartbeat", 10)

        self.create_subscription(String, "oomwoo/health/roster", self._roster_cb, 10)
        self.create_subscription(String, "oomwoo/health/component", self._component_cb, 10)
        self.create_timer(0.05, self._timer_cb)

    def _roster_cb(self, msg: String):
        try:
            self._aggregator.update_roster(_parse_roster(json.loads(msg.data)))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            self.get_logger().warn(f"Ignoring invalid health roster: {exc}")

    def _component_cb(self, msg: String):
        try:
            self._aggregator.update_heartbeat(_parse_heartbeat(json.loads(msg.data)))
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            self.get_logger().warn(f"Ignoring invalid component heartbeat: {exc}")

    def _timer_cb(self):
        now_sec = self._now_sec()
        stack_health = self._aggregator.evaluate(now_sec)
        self._stack_pub.publish(String(data=stack_health.to_json()))
        if not stack_health.emit_mcu_heartbeat:
            return

        self._heartbeat_sequence += 1
        payload = {
            "sequence": self._heartbeat_sequence,
            "source": "oomwoo_health_monitor",
            "stamp_sec": now_sec,
            "stack": asdict(stack_health),
            "task_id": stack_health.task_id,
        }
        self._mcu_pub.publish(String(data=json.dumps(payload, sort_keys=True)))

    def _now_sec(self) -> float:
        try:
            return self.get_clock().now().nanoseconds / 1_000_000_000.0
        except Exception:
            return monotonic()


def _parse_roster(payload: dict) -> HealthRoster:
    components = []
    for item in payload["components"]:
        components.append(
            ComponentSpec(
                component_id=str(item["component_id"]),
                critical=bool(item.get("critical", True)),
                max_age_sec=float(item.get("max_age_sec", 0.5)),
            )
        )
    return HealthRoster.from_components(str(payload["task_id"]), components)


def _parse_heartbeat(payload: dict) -> ComponentHeartbeat:
    return ComponentHeartbeat(
        component_id=str(payload["component_id"]),
        health=str(payload.get("health", "ok")),
        stamp_sec=float(payload["stamp_sec"]),
        detail=str(payload.get("detail", "")),
        sequence=payload.get("sequence"),
    )


def main(args=None):
    rclpy.init(args=args)
    node = HealthMonitorNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException, ROSInterruptException):
        pass
    except Exception as exc:
        if "context is not valid" not in str(exc):
            raise
    finally:
        node.destroy_node()
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception as exc:
            if "rcl_shutdown already called" not in str(exc):
                raise
