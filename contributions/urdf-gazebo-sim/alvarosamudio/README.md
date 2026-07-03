# oomwoo URDF + Gazebo Simulation

Contribution by [alvarosamudio](https://github.com/alvarosamudio) for the `urdf-gazebo-sim` module.

ROS2 package with URDF, Gazebo simulation, and bumper sensor for the oomwoo robot vacuum.

## Package Structure

```
oomwoo_gazebo/
├── urdf/                   # Xacro URDF files
│   ├── params.xacro        # Robot dimensions and physics
│   ├── robot.urdf.xacro    # Main robot description
│   ├── plugins.xacro       # Gazebo plugins (diff-drive, LiDAR, bumper contacts)
│   ├── inertial.xacro      # Inertia calculation macros
│   └── materials.xacro     # Visual materials and friction
├── config/                 # YAML configurations
│   ├── gz_bridge.yaml      # ROS ↔ Gazebo bridge
│   ├── navigation.yaml     # Nav2 parameters
│   └── slam_toolbox.yaml   # SLAM toolbox parameters
├── launch/                 # ROS2 launch files
│   ├── sim.launch.py       # Gazebo + robot + RViz
│   ├── bumper_test.launch.py
│   ├── bump_recovery.launch.py
│   ├── slam.launch.py
│   ├── nav2.launch.py
│   └── teleop.launch.py
├── oomwoo_gazebo/     # Python nodes
│   ├── __init__.py
│   └── bump_recovery.py
├── rviz/
│   └── oomwoo.rviz
├── worlds/                 # 5 Gazebo SDF worlds
├── sdf/meshes/             # Mesh files (future)
├── CMakeLists.txt
├── package.xml
└── README.md
```

## Robot Dimensions (params.xacro)

| Parameter       | Value   | Description                  |
|-----------------|---------|------------------------------|
| base_diameter   | 0.33 m  | Chassis diameter             |
| wheel_diameter  | 0.065 m | Drive wheels diameter        |
| wheel_base      | 0.28 m  | Distance between drive wheels|
| lidar_z_offset  | 0.075 m | LiDAR height offset          |

Approximate dimensions based on the reference teardown (remakeai).

## Bumper

The URDF models a front bumper split into **left** and **right** rectangular pads:

- `bumper_left_link` / `bumper_right_link` — visual + collision bodies on the front edge.
- Each publishes contact events using Gazebo's contact sensor.
- Topics: `/bumper_left` and `/bumper_right` (`ros_gz_interfaces/msg/Contacts`).
- Bridged to ROS2 via `ros_gz_bridge`.

## Automatic Recovery (bump_recovery)

The Python node `bump_recovery.py` subscribes to the bumper topics and:

1. Detects collisions (left or right side), filtering out ground-plane contacts.
2. Publishes a backup + rotation command to `cmd_vel`.
3. Stops after 1.5 seconds.
4. Leaves the robot ready to continue navigation.

## Available Gazebo Worlds

| World             | Features                                 |
|-------------------|------------------------------------------|
| living_room.sdf   | Room with sofa, table, plant, obstacles  |
| kitchen.sdf       | Kitchen with central island, dining table|
| multi_room.sdf    | Two rooms separated by a wall            |
| narrow_passage.sdf| Narrow corridor with obstacle bottleneck |
| empty.sdf         | Empty world for basic testing            |

## How to Use

### Prerequisites

- ROS2 (Jazzy or Humble)
- Gazebo Harmonic
- Packages: `ros_gz_bridge`, `ros_gz_sim`, `slam_toolbox`, `nav2`, `teleop_twist_keyboard`

### Compile

```bash
cd /ros_ws/src
ln -s /path/to/oomwoo/contributions/urdf-gazebo-sim/alvarosamudio/oomwoo_gazebo .
cd /ros_ws
colcon build --packages-select oomwoo_gazebo
source install/setup.bash
```

### Basic Simulation

```bash
ros2 launch oomwoo_gazebo sim.launch.py
# Use a different world (default is living_room.sdf):
ros2 launch oomwoo_gazebo sim.launch.py world:=/path/to/kitchen.sdf
```

### SLAM

```bash
# In a running simulation:
ros2 launch oomwoo_gazebo slam.launch.py
```

### Navigation

```bash
# Provide a pre-built map:
ros2 launch oomwoo_gazebo nav2.launch.py map:=/path/to/map.yaml
```

### Manual Control

```bash
ros2 launch oomwoo_gazebo teleop.launch.py
```

### Test Bumper

```bash
ros2 launch oomwoo_gazebo bumper_test.launch.py
# In another terminal:
ros2 topic echo /bumper_left
ros2 topic echo /bumper_right
```

### Automatic Recovery

```bash
ros2 launch oomwoo_gazebo sim.launch.py
# In another terminal:
ros2 run oomwoo_gazebo bump_recovery.py
# Drive the robot into a wall and watch it back up and turn autonomously
```

## Acceptance Criteria

- [x] URDF matching the teardown reference design approximate dimensions
- [x] Gazebo simulation with diff-drive + LiDAR
- [x] Front bumper with left/right rectangular contact pads
- [x] Contact events published to ROS2 (distinguishing left vs right)
- [x] Gazebo worlds: living room, kitchen, multi-room, narrow passage
- [x] Automatic collision recovery node
- [x] Keyboard control (teleop)
- [x] Nav2 + SLAM parameters configured
- [x] Nav2 stack nodes all configure successfully (11 nodes tested)
- [x] SLAM Toolbox node launches with config
- [x] CPU LiDAR (CpuLidar) configured — uses physics raycasting, no GPU needed
- [x] Bumper bridge fixed — `gz.msgs.Contacts` → `ros_gz_interfaces/msg/Contacts`
- [ ] Nav2 SLAM works in Living Room world (requires CpuLidar system plugin at runtime)
- [ ] Map saved successfully (requires CpuLidar system plugin at runtime)
- [ ] Nav2 navigation works using saved map (requires CpuLidar system plugin at runtime)

### Requirements for CpuLidar

The LiDAR sensor uses `type="lidar"` with the `gz-sim-cpu-lidar-system` plugin, which performs
physics-based raycasting (no GPU required). This requires:

1. **Gazebo** built from source with CpuLidar support (PRs merged May 2026):
   - `gz-sensors` (CpuLidarSensor)
   - `gz-sim` (CpuLidar system plugin)
   - `gz-physics` (raycast support)
2. DART physics engine with **Bullet** collision detector (configured in all world SDFs)

### Fixes Applied

| Issue | Fix |
|-------|-----|
| GPU LiDAR requires hardware GPU | Switched to `type="lidar"` (CpuLidar) — physics raycasting, no GPU |
| Bumper bridge type mismatch | Changed `Contact` → `Contacts` in `gz_bridge.yaml` |
| SDF 1.8 gravity deprecation warning | Moved `gravity` from `<physics>` to `<world>` level in all SDFs |

### Testing Results (Docker, osrf/ros:jazzy-desktop)

| Component | Result |
|-----------|--------|
| Gazebo server loads living_room.sdf | ✅ |
| Robot spawns (`ros_gz_sim create`) | ✅ |
| robot_state_publisher publishes /tf, /joint_states | ✅ |
| parameter_bridge bridges /odom, /scan, /cmd_vel, /clock | ✅ |
| Odometry data flows to ROS2 | ✅ |
| SLAM Toolbox async_slam_toolbox_node starts | ✅ |
| Nav2 bringup — all 11 nodes configure | ✅ |
| LiDAR — CpuLidar configured (`type="lidar"`) | ✅ No GPU needed |
| Bumper topics bridged (`gz.msgs.Contacts` → `Contacts`) | ✅ Fixed |

## License

Apache License 2.0
