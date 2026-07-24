import json
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "oomwoo_health_monitor"
sys.path.insert(0, str(PACKAGE_ROOT))


class _String:
    def __init__(self, data=""):
        self.data = data


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


class _Time:
    def __init__(self, seconds):
        self.nanoseconds = int(seconds * 1_000_000_000)


class _Clock:
    def __init__(self, node):
        self._node = node

    def now(self):
        return _Time(self._node.clock_sec)


class _Node:
    def __init__(self, name):
        self.name = name
        self.clock_sec = 0.0
        self.publishers = {}
        self.subscriptions = []
        self.timers = []
        self.logger = _Logger()

    def create_publisher(self, _msg_type, topic, _qos):
        publisher = _Publisher()
        self.publishers[topic] = publisher
        return publisher

    def create_subscription(self, msg_type, topic, callback, qos):
        self.subscriptions.append((msg_type, topic, callback, qos))

    def create_timer(self, period_sec, callback):
        self.timers.append((period_sec, callback))

    def get_clock(self):
        return _Clock(self)

    def get_logger(self):
        return self.logger

    def destroy_node(self):
        pass


class _ExternalShutdownException(Exception):
    pass


class _ROSInterruptException(Exception):
    pass


def _ros_stubs():
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

    std_msgs = types.ModuleType("std_msgs")
    std_msgs_msg = types.ModuleType("std_msgs.msg")
    std_msgs_msg.String = _String

    return {
        "rclpy": rclpy,
        "rclpy.executors": rclpy_executors,
        "rclpy.exceptions": rclpy_exceptions,
        "rclpy.node": rclpy_node,
        "std_msgs": std_msgs,
        "std_msgs.msg": std_msgs_msg,
    }


class HealthMonitorNodeAdapterTest(unittest.TestCase):
    def setUp(self):
        self._module_patch = mock.patch.dict(sys.modules, _ros_stubs())
        self._module_patch.start()
        sys.modules.pop("oomwoo_health_monitor.health_monitor_node", None)

    def tearDown(self):
        self._module_patch.stop()
        sys.modules.pop("oomwoo_health_monitor.health_monitor_node", None)

    def test_node_publishes_stack_state_and_mcu_heartbeat_after_arming(self):
        from oomwoo_health_monitor.health_monitor_node import HealthMonitorNode

        node = HealthMonitorNode()
        node.clock_sec = 10.0
        node._roster_cb(
            _String(
                data=json.dumps(
                    {
                        "task_id": "dock_cycle",
                        "components": [
                            {
                                "component_id": "recovery_safety",
                                "critical": True,
                                "max_age_sec": 1.0,
                            }
                        ],
                    }
                )
            )
        )
        node._component_cb(
            _String(
                data=json.dumps(
                    {
                        "component_id": "recovery_safety",
                        "health": "ok",
                        "stamp_sec": 10.0,
                    }
                )
            )
        )

        node._timer_cb()
        node.clock_sec = 10.3
        node._timer_cb()

        stack_messages = node.publishers["oomwoo/health/stack"].messages
        mcu_messages = node.publishers["oomwoo/health/mcu_heartbeat"].messages
        self.assertEqual(json.loads(stack_messages[0].data)["state"], "arming")
        self.assertEqual(json.loads(stack_messages[-1].data)["state"], "healthy")
        self.assertEqual(len(mcu_messages), 1)
        self.assertEqual(json.loads(mcu_messages[0].data)["task_id"], "dock_cycle")

    def test_stale_critical_component_stops_mcu_heartbeat(self):
        from oomwoo_health_monitor.health_monitor_node import HealthMonitorNode

        node = HealthMonitorNode()
        node.clock_sec = 20.0
        node._roster_cb(
            _String(
                data=json.dumps(
                    {
                        "task_id": "cleaning_job",
                        "components": [
                            {
                                "component_id": "nav2_controller",
                                "critical": True,
                                "max_age_sec": 1.0,
                            }
                        ],
                    }
                )
            )
        )
        node._component_cb(
            _String(
                data=json.dumps(
                    {
                        "component_id": "nav2_controller",
                        "health": "ok",
                        "stamp_sec": 20.0,
                    }
                )
            )
        )

        node.clock_sec = 20.3
        node._timer_cb()
        node.clock_sec = 20.6
        node._timer_cb()
        node.clock_sec = 21.2
        node._timer_cb()

        stack_messages = node.publishers["oomwoo/health/stack"].messages
        self.assertEqual(len(node.publishers["oomwoo/health/mcu_heartbeat"].messages), 1)
        self.assertEqual(json.loads(stack_messages[-1].data)["state"], "fault")
        self.assertEqual(json.loads(stack_messages[-1].data)["stale_critical"], ["nav2_controller"])

    def test_invalid_roster_is_warned_and_ignored(self):
        from oomwoo_health_monitor.health_monitor_node import HealthMonitorNode

        node = HealthMonitorNode()
        node._roster_cb(_String(data="{not json"))

        self.assertEqual(len(node.logger.warnings), 1)
        node._timer_cb()
        stack = json.loads(node.publishers["oomwoo/health/stack"].messages[-1].data)
        self.assertEqual(stack["state"], "no_roster")


if __name__ == "__main__":
    unittest.main()
