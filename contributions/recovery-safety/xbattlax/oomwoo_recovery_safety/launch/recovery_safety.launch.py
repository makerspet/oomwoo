from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="oomwoo_recovery_safety",
                executable="recovery_safety_node",
                name="recovery_safety",
                output="screen",
            )
        ]
    )
