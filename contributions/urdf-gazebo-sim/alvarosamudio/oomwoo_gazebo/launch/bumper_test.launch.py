import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.substitutions import Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory("oomwoo_gazebo")

    world = os.path.join(pkg, "worlds", "empty.sdf")

    gz_server = ExecuteProcess(
        cmd=["gz", "sim", "-r", world],
        output="screen",
        additional_env={"GZ_SIM_RESOURCE_PATH": os.path.join(pkg, "sdf")},
    )

    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        parameters=[os.path.join(pkg, "config", "gz_bridge.yaml")],
        output="screen",
    )

    robot_state_pub = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{
            "robot_description": Command(
                ["xacro ", os.path.join(pkg, "urdf", "robot.urdf.xacro")]
            )
        }],
    )

    spawn_entity = TimerAction(
        period=2.0,
        actions=[
            Node(
                package="ros_gz_sim",
                executable="create",
                arguments=["-name", "oomwoo", "-topic", "robot_description"],
                output="screen",
            )
        ],
    )

    bump_recovery = Node(
        package="oomwoo_gazebo",
        executable="bump_recovery.py",
        name="bump_recovery",
        output="screen",
    )

    return LaunchDescription([
        gz_server,
        bridge,
        robot_state_pub,
        spawn_entity,
        bump_recovery,
    ])
