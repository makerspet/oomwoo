#!/usr/bin/env bash
# Run the oomwoo_baseline collector against the LIVE OOMWOO Gazebo simulation.
#
# Prerequisites (set up by the user on the Windows host, per
# docs/blog/oomwoo-one-simulate-in-gazebo.md):
#   1. Docker Desktop installed and running.
#   2. VcXsrv (XLaunch) running with Display number = 0 and "Disable access control".
#   3. In the oomwoo jazzy-dev container:
#        docker pull makerspet/oomwoo:jazzy-dev
#        docker run --name makerspet -it --rm -v "$PWD":/root/workspace \
#          -e DISPLAY=host.docker.internal:0.0 -e LIBGL_ALWAYS_INDIRECT=0 \
#          --add-host=host.docker.internal:host-gateway makerspet/oomwoo:jazzy-dev
#   4. Inside the container (this script assumes the workspace is mounted at
#      /root/workspace and oomwoo_baseline lives under contributions/...):
#        kaia config robot.model oomwoo_one
#        ros2 launch kaiaai_gazebo world.launch.py        # start the sim
#      then in another shell:  bash scripts/run_in_gazebo.sh
#
# This script builds oomwoo_baseline and launches baseline_record.launch.py with
# use_sim_time:=true so the collector records the live /scan /odom /tf /cmd_vel
# /bumper_left /bumper_right /map /oomwoo/status topics from the simulation.
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_DIR="$(dirname "$SCRIPT_DIR")"

# locate colcon workspace root (src/ build/ install/ all present)
DIR="$PKG_DIR"
WS=""
while [ "$DIR" != "/" ]; do
  if [ -d "$DIR/src" ] && [ -d "$DIR/build" ] && [ -d "$DIR/install" ]; then
    WS="$DIR"; break
  fi
  DIR="$(dirname "$DIR")"
done
[ -z "$WS" ] && { echo "colcon workspace not found from $PKG_DIR"; exit 1; }

# auto-detect ROS2 setup (jazzy in the official container; humble also works)
ROS_SETUP=""
for d in /opt/ros/*; do
  [ -f "$d/setup.bash" ] && ROS_SETUP="$d/setup.bash"
done
[ -z "$ROS_SETUP" ] && { echo "no ROS2 setup.bash under /opt/ros"; exit 1; }

echo "==> ROS setup: $ROS_SETUP"
export PATH="$HOME/.local/bin:$PATH"
# shellcheck disable=SC1090
source "$ROS_SETUP"

cd "$WS"
echo "==> colcon build oomwoo_baseline"
colcon build --packages-select oomwoo_baseline --event-handlers console_direct+ 2>&1 | tail -8
# shellcheck disable=SC1090
source install/setup.bash

echo "==> launch baseline_record against the live sim (use_sim_time:=true)"
echo "    (keep the Gazebo world running in another shell)"
ros2 launch oomwoo_baseline baseline_record.launch.py use_sim_time:=true
