"""Launch file: record baseline topics + collect KPIs + capture run metadata.

Brings up (for a single experiment run):
  * ``ros2 bag record`` of the MVP baseline surface from SOFTWARE_INTERFACES.md
  * the ``metrics_collector_node`` (writes JSON snapshot + CSV time series)
  * the ``run_metadata_node`` (writes run_metadata.json at startup)

Topic names are relative and resolve in the default namespace, matching the
other OOMWOO contributions. ``use_sim_time`` should be set on the bringup
launch that includes this file.

Example::

    ros2 launch oomwoo_baseline baseline_record.launch.py \\
        scenario:=single_room_empty seed:=42 \\
        repo_root:=/path/to/robot_src \\
        bag_dir:=/tmp/bags/single_room_empty_42
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    scenario = LaunchConfiguration("scenario")
    seed = LaunchConfiguration("seed")
    repo_root = LaunchConfiguration("repo_root")
    config_file = LaunchConfiguration("config_file")
    bag_dir = LaunchConfiguration("bag_dir")
    metrics_json = LaunchConfiguration("metrics_json")
    run_metadata_json = LaunchConfiguration("run_metadata_json")
    hardware_note = LaunchConfiguration("hardware_note")

    topics = [
        "/scan", "/odom", "/tf", "/joint_states", "/map",
        "/cmd_vel", "/bumper_left", "/bumper_right", "/oomwoo/status",
    ]

    return LaunchDescription(
        [
            DeclareLaunchArgument("scenario", default_value="single_room_empty"),
            DeclareLaunchArgument("seed", default_value="42"),
            DeclareLaunchArgument("repo_root", default_value=""),
            DeclareLaunchArgument("config_file", default_value=""),
            DeclareLaunchArgument("bag_dir", default_value="/tmp/oomwoo_bag"),
            DeclareLaunchArgument(
                "metrics_json", default_value="/tmp/oomwoo_baseline_metrics.json"
            ),
            DeclareLaunchArgument(
                "run_metadata_json", default_value="/tmp/oomwoo_run_metadata.json"
            ),
            DeclareLaunchArgument("hardware_note", default_value=""),

            ExecuteProcess(
                cmd=["ros2", "bag", "record", "-o", bag_dir] + topics,
                output="screen",
                name="baseline_bag_record",
            ),
            Node(
                package="oomwoo_baseline",
                executable="metrics_collector_node",
                name="oomwoo_baseline_metrics",
                output="screen",
                parameters=[{"metrics_json": metrics_json}],
            ),
            Node(
                package="oomwoo_baseline",
                executable="run_metadata_node",
                name="oomwoo_baseline_metadata",
                output="screen",
                parameters=[
                    {"repo_root": repo_root},
                    {"scenario": scenario},
                    {"seed": seed},
                    {"config_file": config_file},
                    {"output_json": run_metadata_json},
                    {"hardware_note": hardware_note},
                ],
            ),
        ]
    )
