"""Synthetic OOMWOO baseline topic publisher for local Phase-0 verification.

Publishes at 5 Hz (unless noted) on the MVP baseline surface the
``metrics_collector`` node subscribes to:

  /scan           sensor_msgs/LaserScan
  /odom           nav_msgs/Odometry (constant-velocity straight-line motion)
  /tf             tf2_msgs/TFMessage (odom->base_link, stamped 12 ms in the past)
  /cmd_vel        geometry_msgs/Twist (matches the motion)
  /map            nav_msgs/OccupancyGrid (published once; mostly free space)
  /oomwoo/status  std_msgs/String ("RUNNING", once)

This lets ``metrics_collector`` exercise its KPI pipeline against *real* ROS 2
messages without a Gazebo robot. It is a local validation aid, not shipped.
"""
from __future__ import annotations

import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from builtin_interfaces.msg import Time
from geometry_msgs.msg import Twist, TransformStamped
from nav_msgs.msg import Odometry, OccupancyGrid
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Header, String
from tf2_msgs.msg import TFMessage

try:
    from ros_gz_interfaces.msg import Contacts, Contact
except ImportError:  # bumper message type; only available after ros_gz_interfaces is installed
    Contacts = None
    Contact = None


def _to_time(fsec: float) -> Time:
    sec = int(fsec)
    nanosec = int((fsec - sec) * 1e9)
    return Time(sec=sec, nanosec=nanosec)


class DemoPublisher(Node):
    def __init__(self):
        super().__init__("oomwoo_demo_publisher")
        qos = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
            history=rclpy.qos.HistoryPolicy.KEEP_LAST,
            depth=10,
        )
        self.pub_scan = self.create_publisher(LaserScan, "scan", qos)
        self.pub_odom = self.create_publisher(Odometry, "odom", qos)
        self.pub_tf = self.create_publisher(TFMessage, "tf", qos)
        self.pub_cmd = self.create_publisher(Twist, "cmd_vel", qos)
        self.pub_status = self.create_publisher(String, "oomwoo/status", qos)
        map_qos = rclpy.qos.QoSProfile(
            reliability=rclpy.qos.ReliabilityPolicy.RELIABLE,
            durability=rclpy.qos.DurabilityPolicy.TRANSIENT_LOCAL,
            history=rclpy.qos.HistoryPolicy.KEEP_LAST,
            depth=1,
        )
        self.pub_map = self.create_publisher(OccupancyGrid, "map", map_qos)

        self.timer = self.create_timer(0.2, self._tick)  # 5 Hz
        self.t = 0.0
        self.x = 0.0
        self.speed = 0.2  # m/s along +x
        self._published_map = False
        self._published_status = False
        self._tick_count = 0
        self.pub_bumper = None
        if Contacts is not None:
            # Publish a synthetic bumper contact on /bumper_left so the collector's
            # bumper KPI path is exercised once ros_gz_interfaces is installed.
            self.pub_bumper = self.create_publisher(Contacts, "bumper_left", 10)
        self.get_logger().info("demo publisher started: /scan /odom /tf /cmd_vel @5Hz")

    def _tick(self):
        now = self.get_clock().now()
        now_sec = now.nanoseconds / 1e9
        stamp = _to_time(now_sec)

        # advance constant-velocity motion (+x)
        self.x += self.speed * 0.2
        self.t += 0.2

        # /scan
        scan = LaserScan()
        scan.header = Header(stamp=stamp, frame_id="base_scan")
        scan.angle_min = -math.pi
        scan.angle_max = math.pi
        scan.angle_increment = 2.0 * math.pi / 360.0
        scan.time_increment = 0.0
        scan.scan_time = 0.2
        scan.range_min = 0.05
        scan.range_max = 10.0
        scan.ranges = [1.0 + 0.1 * math.sin(self.t + i * 0.05) for i in range(361)]
        scan.intensities = [1.0] * 361
        self.pub_scan.publish(scan)

        # /odom (consistent with motion so odom drift ~1.0)
        odom = Odometry()
        odom.header = Header(stamp=stamp, frame_id="odom")
        odom.child_frame_id = "base_link"
        odom.pose.pose.position.x = self.x
        odom.twist.twist.linear.x = self.speed
        self.pub_odom.publish(odom)

        # /cmd_vel
        cmd = Twist()
        cmd.linear.x = self.speed
        self.pub_cmd.publish(cmd)

        # /tf (stamped 12 ms in the past -> realistic ~12ms latency)
        tf = TFMessage()
        ts = TransformStamped()
        ts.header = Header(stamp=_to_time(now_sec - 0.012), frame_id="odom")
        ts.child_frame_id = "base_link"
        ts.transform.translation.x = self.x
        ts.transform.rotation.w = 1.0
        tf.transforms.append(ts)
        self.pub_tf.publish(tf)

        if not self._published_map:
            self._publish_map(now_sec)
            self._published_map = True

        if not self._published_status:
            s = String()
            s.data = "RUNNING"
            self.pub_status.publish(s)
            self._published_status = True

        # synthetic bumper contact every ~2 s (only when Contacts type is available)
        self._tick_count += 1
        if self.pub_bumper is not None and self._tick_count % 10 == 0:
            c = Contacts()
            c.contacts = [self._make_contact()]
            self.pub_bumper.publish(c)

    def _make_contact(self) -> "Contacts":
        contact = Contact()
        # names must NOT contain "ground_plane" or the collector ignores the contact
        contact.collision1.name = "robot::base_link"
        contact.collision2.name = "obstacle::box"
        return contact

    def _publish_map(self, now_sec):
        m = OccupancyGrid()
        m.header = Header(stamp=_to_time(now_sec), frame_id="map")
        m.info.resolution = 0.05
        m.info.width = 100
        m.info.height = 100
        m.info.origin.position.x = -2.5
        m.info.origin.position.y = -2.5
        data = []
        for r in range(100):
            for c in range(100):
                if r == 0 or c == 0 or r == 99 or c == 99:
                    data.append(100)
                elif (r * 7 + c * 13) % 53 == 0:
                    data.append(-1)
                else:
                    data.append(0)
        m.data = data
        self.pub_map.publish(m)


def main(args=None):
    rclpy.init(args=args)
    node = DemoPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
