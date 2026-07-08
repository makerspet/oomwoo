# Simulate the oomwoo-one Robot Vacuum in Gazebo with ROS 2

> *Draft for makerspet.com (WordPress / Gutenberg).* Post 1 of 2: set up the OOMWOO
> software dev environment and drive `oomwoo-one` in simulation — no robot required.
> (Post 2 teaches you to write your own OOMWOO code.)

[OOMWOO](https://github.com/makerspet/oomwoo) is an open-source robot vacuum you build
yourself. *oomwoo-one* is the first model. This tutorial gets its ROS 2 simulation running
in *Gazebo* so you can develop mapping, navigation, and cleaning behaviours with *no
hardware* — everything runs in Docker on *Ubuntu or Windows*.

You'll get: SLAM mapping, autonomous Nav2 navigation, manual driving, and bumper sensors —
the same interfaces the real robot will expose.

## Prerequisites

- *Docker* — Docker Desktop on Windows/macOS, Docker Engine on Linux.
- *An X server* for the GUI windows (Gazebo, RViz):
  - *Windows:* [VcXsrv](https://sourceforge.net/projects/vcxsrv/) (XLaunch).
  - *Linux:* native X — nothing to install.
- No physical robot.

## 1. Start the X server (Windows only)

Launch *XLaunch* (from VcXsrv) and accept the defaults *except*:

> On the *"Display settings"* page, set *Display number = `0`* (not `-1`).
> The Docker container connects to `host.docker.internal:0.0`, so the display number *must
> be 0* or no GUI windows will appear.

Also tick *"Disable access control"* on the "Extra settings" page so the container can
connect. Finish the wizard — a tiny X icon appears in your tray.

On *Linux*, instead allow local Docker to reach your X server:
```bash
xhost +local:docker
```

## 2. Pull the OOMWOO Docker image

```
docker pull makerspet/oomwoo:jazzy-dev
```

## 3. Start the container

*Windows (PowerShell):*
```powershell
docker run --name makerspet -it --rm -v c:\maps:/root/maps -p 8888:8888/udp -p 5555:5555/udp -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=0 --add-host=host.docker.internal:host-gateway makerspet/oomwoo:jazzy-dev
```
(`DISPLAY=...:0.0` matches the XLaunch *display 0* from step 1.)

*Ubuntu / Linux:*
```bash
docker run --name makerspet -it --rm -v ~/maps:/root/maps -p 8888:8888/udp -p 5555:5555/udp -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --network host makerspet/oomwoo:jazzy-dev
```

Need more terminals into the same container? Open another PowerShell/terminal and run:
```
docker exec -it makerspet bash
```

## 4. Select the oomwoo-one model

Inside the container:
```
kaia config robot.model oomwoo_one
```

## 5. Launch the Gazebo world

```
ros2 launch kaiaai_gazebo world.launch.py
```
A Gazebo window opens with oomwoo-one in a living-room world.

## 6. Start SLAM mapping

In a new container shell (`docker exec -it makerspet bash`):
```
ros2 launch kaiaai_bringup navigation.launch.py use_sim_time:=true slam:=True
```

## 7. Open the RViz monitor

```
ros2 launch kaiaai_bringup monitor_robot.launch.py use_sim_time:=true
```
Watch the map build as the robot moves.

## 8. Drive it manually

```
ros2 run kaiaai_teleop teleop_keyboard
```
Use the keyboard to drive oomwoo-one around and fill in the map.

## 9. Autonomous navigation

In RViz, click *"Nav2 Goal"* and click-drag a destination — oomwoo-one plans a path and
drives there on its own.

## 10. Check the bumper sensors

```
ros2 topic echo /bumper_left
ros2 topic echo /bumper_right
```
Drive into a wall and watch the left/right contact events fire.

## 11. Save your map

```
ros2 run nav2_map_server map_saver_cli -f ~/maps/map
```
On Windows the map lands in `c:\maps`; on Linux in `~/maps`.

## What's next

You now have a full oomwoo-one simulation: SLAM, Nav2, teleop, and bumpers, exactly the
interfaces the real robot exposes. In *Post 2* you'll write your *first OOMWOO ROS 2
package* — a node that drives a coverage path *while* mapping — and launch it with
`ros2 launch`.

Want to help build OOMWOO? Grab a module from the [Requests for
Contributions](https://github.com/makerspet/oomwoo#requests-for-contributions) or say hi on
[Discord](https://discord.gg/3y2JKz5T25).
