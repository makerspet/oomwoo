#!/usr/bin/env bash
# End-to-end local real-run of the oomwoo_baseline metrics collector against
# synthetic baseline topics (no Gazebo required). Runs the collector as a real
# ROS 2 node fed by demo_publisher, then generates a baseline report.
#
# Executed as a FILE (bash <this>) because `bash -c` drops variable expansion
# on this WSL. Best-effort installs ros_gz_interfaces if passwordless sudo works.
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

# auto-detect ROS2 setup
ROS_SETUP=""
for d in /opt/ros/*; do
  [ -f "$d/setup.bash" ] && ROS_SETUP="$d/setup.bash"
done
[ -z "$ROS_SETUP" ] && { echo "no ROS2 setup.bash under /opt/ros"; exit 1; }

echo "==> ROS setup: $ROS_SETUP"
export PATH="$HOME/.local/bin:$PATH"
# shellcheck disable=SC1090
source "$ROS_SETUP"

# best-effort: install ros_gz_interfaces (only if passwordless sudo available)
echo "==> attempt install ros_gz_interfaces (non-interactive; skipped if password needed)"
sudo -n apt-get install -y ros-humble-ros-gz-interfaces 2>&1 | tail -2 || \
  echo "    (skipped: needs sudo password; bumper KPIs disabled until installed)"

cd "$WS"
echo "==> colcon build oomwoo_baseline"
colcon build --packages-select oomwoo_baseline --event-handlers console_direct+ 2>&1 | tail -8
# shellcheck disable=SC1090
source install/setup.bash

# The ament index marker for this package is not generated on the cross-mounted
# /mnt/e workspace, so `setup.bash` / the develop-install do not make
# `oomwoo_baseline` importable. We run the node modules directly from source and
# put the package parent on PYTHONPATH (robust regardless of install quirks).
export PYTHONPATH="$PKG_DIR/..:$PYTHONPATH"
echo "==> PYTHONPATH includes package parent: $PKG_DIR/.."

METRICS_JSON=/tmp/oomwoo_demo_metrics.json
METRICS_CSV=/tmp/oomwoo_demo_timeseries.csv
META_JSON=/tmp/oomwoo_demo_run_metadata.json
REPORT_OUT="$PKG_DIR/DEMO_BASELINE_REPORT.md"
rm -f "$METRICS_JSON" "$METRICS_CSV" "$META_JSON"

echo "==> run_metadata_node -> $META_JSON"
python3 "$PKG_DIR/run_metadata.py" --ros-args \
  -p output_json:="$META_JSON" -p repo_root:=/mnt/e/puppyfangzhen/robot_src &
PID_META=$!
# run_metadata_node is a one-shot: it writes metadata in __init__ then
# spin_once(~1s) and self-exits. Wait for it instead of killing, so the
# metadata JSON is always flushed even if DDS cold-start makes rclpy.init() slow.
wait $PID_META 2>/dev/null

echo "==> demo publisher + metrics_collector (12 s)"
python3 "$PKG_DIR/scripts/demo_publisher.py" &
PID_PUB=$!
python3 "$PKG_DIR/metrics_collector.py" --ros-args \
  -p metrics_json:="$METRICS_JSON" -p metrics_csv:="$METRICS_CSV" \
  -p write_period_sec:=3.0 &
PID_COL=$!
sleep 12
kill $PID_PUB $PID_COL 2>/dev/null; wait $PID_PUB $PID_COL 2>/dev/null

echo ""
echo "=== METRICS JSON ($METRICS_JSON) ==="
cat "$METRICS_JSON"
echo ""
echo "=== TIMESERIES CSV (head) ==="
head -5 "$METRICS_CSV" 2>/dev/null

echo ""
echo "==> generate baseline report -> $REPORT_OUT"
python3 "$PKG_DIR/scripts/baseline_report.py" \
  --metrics "$METRICS_JSON" --run-metadata "$META_JSON" \
  --output "$REPORT_OUT" 2>&1 | tail -4

# copy artifacts next to the package for inspection
cp "$METRICS_JSON" "$PKG_DIR/DEMO_METRICS.json"
cp "$METRICS_CSV" "$PKG_DIR/DEMO_TIMESERIES.csv"
cp "$META_JSON" "$PKG_DIR/DEMO_RUN_METADATA.json"
echo "==> done. artifacts in $PKG_DIR"
