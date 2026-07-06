from __future__ import annotations

import json
from time import monotonic

from geometry_msgs.msg import Twist
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.exceptions import ROSInterruptException
from rclpy.node import Node
from ros_gz_interfaces.msg import Contacts
from std_msgs.msg import Bool, String

from oomwoo_recovery_safety.core import Decision, DecisionKind, RecoveryController, Situation


class RecoverySafetyNode(Node):
    def __init__(self):
        super().__init__("recovery_safety")
        self._controller = RecoveryController()
        self._active_deadline: float | None = None

        self._cmd_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self._status_pub = self.create_publisher(String, "oomwoo/status", 10)
        self._command_pub = self.create_publisher(String, "oomwoo/recovery/command", 10)

        self.create_subscription(Contacts, "bumper_left", self._bumper_left_cb, 10)
        self.create_subscription(Contacts, "bumper_right", self._bumper_right_cb, 10)
        self.create_subscription(String, "oomwoo/recovery/event", self._event_cb, 10)
        self.create_subscription(String, "oomwoo/recovery/behavior_result", self._behavior_result_cb, 10)
        self.create_subscription(Bool, "oomwoo/safety/e_stop", self._e_stop_cb, 10)
        self.create_subscription(Bool, "oomwoo/safety/cliff", self._cliff_cb, 10)
        self.create_subscription(Bool, "oomwoo/safety/wheel_drop", self._wheel_drop_cb, 10)
        self.create_subscription(Bool, "oomwoo/safety/pickup", self._pickup_cb, 10)
        self.create_subscription(Bool, "oomwoo/recovery/reset", self._reset_cb, 10)

        self.create_timer(0.05, self._timer_cb)
        self._publish_status(self._controller.last_status)

    def _bumper_left_cb(self, msg: Contacts):
        if self._has_real_contact(msg):
            self._execute(self._controller.trigger(Situation.BUMPER_LEFT))

    def _bumper_right_cb(self, msg: Contacts):
        if self._has_real_contact(msg):
            self._execute(self._controller.trigger(Situation.BUMPER_RIGHT))

    def _event_cb(self, msg: String):
        try:
            self._execute(self._controller.trigger(msg.data))
        except ValueError as exc:
            self.get_logger().warn(str(exc))

    def _behavior_result_cb(self, msg: String):
        outcome = self._parse_outcome(msg.data)
        if outcome == "succeeded":
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.step_succeeded())
        elif outcome == "failed":
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.step_failed("external failure result"))
        else:
            self.get_logger().warn(f"Ignoring unknown behavior outcome: {msg.data}")

    def _e_stop_cb(self, msg: Bool):
        if msg.data:
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.trigger(Situation.E_STOP))

    def _cliff_cb(self, msg: Bool):
        if msg.data:
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.trigger(Situation.CLIFF))

    def _wheel_drop_cb(self, msg: Bool):
        if msg.data:
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.trigger(Situation.WHEEL_DROP))

    def _pickup_cb(self, msg: Bool):
        if msg.data:
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.trigger(Situation.PICKUP))

    def _reset_cb(self, msg: Bool):
        if msg.data:
            self._stop_motion()
            self._active_deadline = None
            self._execute(self._controller.reset())

    def _timer_cb(self):
        if self._active_deadline is None or monotonic() < self._active_deadline:
            return

        self._stop_motion()
        self._active_deadline = None
        self._execute(self._controller.step_failed("behavior timeout"))

    def _execute(self, decision: Decision):
        self._publish_status(decision.status)
        if decision.kind != DecisionKind.START_STEP or decision.step is None:
            return

        step = decision.step
        if step.command == "twist":
            twist = Twist()
            twist.linear.x = step.linear_x
            twist.angular.z = step.angular_z
            self._cmd_pub.publish(twist)
        elif step.command == "stop":
            self._stop_motion()
        else:
            self._publish_command(step.command, step.name)

        self._active_deadline = monotonic() + step.duration_sec

    def _publish_status(self, status):
        self._status_pub.publish(String(data=status.to_json()))

    def _publish_command(self, command: str, behavior: str):
        payload = {
            "command": command,
            "behavior": behavior,
            "source": "oomwoo_recovery_safety",
        }
        self._command_pub.publish(String(data=json.dumps(payload, sort_keys=True)))

    def _stop_motion(self):
        self._cmd_pub.publish(Twist())

    @staticmethod
    def _has_real_contact(msg: Contacts) -> bool:
        for contact in msg.contacts:
            names = {contact.collision1.name, contact.collision2.name}
            if not any("ground_plane" in name.split("::") for name in names):
                return True
        return False

    @staticmethod
    def _parse_outcome(raw: str) -> str:
        value = raw.strip().lower()
        if value.startswith("{"):
            try:
                value = str(json.loads(raw).get("outcome", "")).strip().lower()
            except json.JSONDecodeError:
                return ""
        return value


def main(args=None):
    rclpy.init(args=args)
    node = RecoverySafetyNode()
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
