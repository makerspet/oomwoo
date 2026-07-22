import importlib
import sys
import types


class _Vector:
    def __init__(self):
        self.x = 0.0
        self.z = 0.0


class _Twist:
    def __init__(self):
        self.linear = _Vector()
        self.angular = _Vector()


class _String:
    def __init__(self, data=""):
        self.data = data


class _Bool:
    def __init__(self, data=False):
        self.data = data


class _Contacts:
    def __init__(self):
        self.contacts = []


class _Publisher:
    def __init__(self):
        self.messages = []

    def publish(self, msg):
        self.messages.append(msg)


class _Logger:
    def __init__(self):
        self.warnings = []

    def warn(self, message):
        self.warnings.append(message)


class _Node:
    def __init__(self, name):
        self.name = name
        self.publishers = {}
        self.timers = []
        self.subscriptions = []
        self.logger = _Logger()

    def create_publisher(self, _msg_type, topic, _qos):
        publisher = _Publisher()
        self.publishers[topic] = publisher
        return publisher

    def create_subscription(self, msg_type, topic, callback, qos):
        self.subscriptions.append((msg_type, topic, callback, qos))

    def create_timer(self, period_sec, callback):
        self.timers.append((period_sec, callback))

    def get_logger(self):
        return self.logger

    def destroy_node(self):
        pass


class _ExternalShutdownException(Exception):
    pass


class _ROSInterruptException(Exception):
    pass


def _install_ros_stubs(monkeypatch):
    geometry_msgs = types.ModuleType("geometry_msgs")
    geometry_msgs_msg = types.ModuleType("geometry_msgs.msg")
    geometry_msgs_msg.Twist = _Twist

    rclpy = types.ModuleType("rclpy")
    rclpy.init = lambda args=None: None
    rclpy.spin = lambda node: None
    rclpy.ok = lambda: False
    rclpy.shutdown = lambda: None

    rclpy_executors = types.ModuleType("rclpy.executors")
    rclpy_executors.ExternalShutdownException = _ExternalShutdownException

    rclpy_exceptions = types.ModuleType("rclpy.exceptions")
    rclpy_exceptions.ROSInterruptException = _ROSInterruptException

    rclpy_node = types.ModuleType("rclpy.node")
    rclpy_node.Node = _Node

    ros_gz_interfaces = types.ModuleType("ros_gz_interfaces")
    ros_gz_interfaces_msg = types.ModuleType("ros_gz_interfaces.msg")
    ros_gz_interfaces_msg.Contacts = _Contacts

    std_msgs = types.ModuleType("std_msgs")
    std_msgs_msg = types.ModuleType("std_msgs.msg")
    std_msgs_msg.Bool = _Bool
    std_msgs_msg.String = _String

    modules = {
        "geometry_msgs": geometry_msgs,
        "geometry_msgs.msg": geometry_msgs_msg,
        "rclpy": rclpy,
        "rclpy.executors": rclpy_executors,
        "rclpy.exceptions": rclpy_exceptions,
        "rclpy.node": rclpy_node,
        "ros_gz_interfaces": ros_gz_interfaces,
        "ros_gz_interfaces.msg": ros_gz_interfaces_msg,
        "std_msgs": std_msgs,
        "std_msgs.msg": std_msgs_msg,
    }
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)


def _load_node_module(monkeypatch):
    _install_ros_stubs(monkeypatch)
    monkeypatch.delitem(sys.modules, "oomwoo_recovery_safety.recovery_node", raising=False)
    return importlib.import_module("oomwoo_recovery_safety.recovery_node")


def test_twist_step_is_republished_while_deadline_is_active(monkeypatch):
    recovery_node = _load_node_module(monkeypatch)
    node = recovery_node.RecoverySafetyNode()

    node._event_cb(_String(data="wedged"))

    assert len(node._cmd_pub.messages) == 1
    held_twist = node._cmd_pub.messages[-1]
    assert held_twist.linear.x == -0.12
    assert held_twist.angular.z == 0.0

    node._timer_cb()

    assert len(node._cmd_pub.messages) == 2
    assert node._cmd_pub.messages[-1] is held_twist
    assert node._active_twist is held_twist


def test_delegated_command_uses_completion_timeout(monkeypatch):
    recovery_node = _load_node_module(monkeypatch)
    node = recovery_node.RecoverySafetyNode()

    start = recovery_node.monotonic()
    node._event_cb(_String(data="no_valid_path"))

    assert len(node._command_pub.messages) == 1
    assert 1.5 < node._active_deadline - start <= 2.1
    assert node._active_twist is None
