from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="oomwoo_health_monitor",
                executable="health_monitor_node",
                name="health_monitor",
                output="screen",
            )
        ]
    )
