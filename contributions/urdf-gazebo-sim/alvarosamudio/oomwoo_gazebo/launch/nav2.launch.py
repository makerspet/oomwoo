import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg = get_package_share_directory("oomwoo_gazebo")
    nav2_bringup = get_package_share_directory("nav2_bringup")
    nav2_params = os.path.join(pkg, "config", "navigation.yaml")
    default_map = os.path.join(pkg, "config", "map.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    map_yaml = LaunchConfiguration("map", default=default_map)

    return LaunchDescription([
        DeclareLaunchArgument(
            "map", default_value=default_map,
            description="Full path to map YAML file"
        ),
        DeclareLaunchArgument(
            "use_sim_time", default_value="true",
            description="Use simulation time"
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup, "launch", "navigation_launch.py")
            ),
            launch_arguments={
                "use_sim_time": use_sim_time,
                "params_file": nav2_params,
                "map": map_yaml,
                "autostart": "true",
            }.items(),
        ),
    ])
