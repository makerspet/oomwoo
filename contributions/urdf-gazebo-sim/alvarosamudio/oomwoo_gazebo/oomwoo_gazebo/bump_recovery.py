#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from ros_gz_interfaces.msg import Contacts
from geometry_msgs.msg import Twist


class BumpRecovery(Node):
    def __init__(self):
        super().__init__("bump_recovery")
        self._cmd_pub = self.create_publisher(Twist, "cmd_vel", 10)
        self._left_sub = self.create_subscription(
            Contacts, "bumper_left", self._left_cb, 10
        )
        self._right_sub = self.create_subscription(
            Contacts, "bumper_right", self._right_cb, 10
        )
        self._recovering = False
        self._timer = None

    def _left_cb(self, msg):
        if self._recovering or not msg.contacts:
            return
        if self._is_real_contact(msg):
            self._recover("left")

    def _right_cb(self, msg):
        if self._recovering or not msg.contacts:
            return
        if self._is_real_contact(msg):
            self._recover("right")

    def _is_real_contact(self, msg):
        for contact in msg.contacts:
            if not self._is_ground_contact(contact):
                return True
        return False

    @staticmethod
    def _is_ground_contact(contact):
        return (
            BumpRecovery._is_ground_entity(contact.collision1.name)
            or BumpRecovery._is_ground_entity(contact.collision2.name)
        )

    @staticmethod
    def _is_ground_entity(name):
        return "ground_plane" in name.split("::")

    def _recover(self, side):
        self._recovering = True
        self.get_logger().info(f"Bump detected on {side} — recovering")

        twist = Twist()
        twist.linear.x = -0.15
        twist.angular.z = 0.4 if side == "left" else -0.4
        self._cmd_pub.publish(twist)

        self._timer = self.create_timer(1.5, self._stop_recovery)

    def _stop_recovery(self):
        self._cmd_pub.publish(Twist())
        if self._timer:
            self._timer.cancel()
        self._recovering = False
        self.get_logger().info("Recovery complete")


def main(args=None):
    rclpy.init(args=args)
    node = BumpRecovery()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
