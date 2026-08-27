#!/usr/bin/env bash
#
# OOMWOO Phase-0 一键实验编排。
#
# 在 Linux + ROS2 Jazzy + Gazebo 机器上运行：先启动 sim+nav 的 bringup
# （由 contributions/urdf-gazebo-sim 提供），再本脚本启动基线录制与采集，
# Ctrl-C 结束后自动生成基线报表。
#
# 用法:
#   ./run_experiment.sh --scenario single_room_empty --seed 42 \
#       --repo-root /path/to/robot_src --bag-dir /tmp/bags/sr42
#
# 前置:
#   - 已 source ROS2 (Jazzy) 与 workspace (colcon build 过 oomwoo_baseline)
#   - 已按 SOFTWARE_INTERFACES.md 启动 sim + Nav2 + SLAM bringup
#   - use_sim_time=true 由 bringup 设置

set -euo pipefail

SCENARIO="single_room_empty"
SEED="42"
REPO_ROOT=""
CONFIG_FILE=""
BAG_DIR="/tmp/oomwoo_bag"
HARDWARE_NOTE=""
ROS_DOMAIN_ID="${ROS_DOMAIN_ID:-42}"
RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_cyclonedds_cpp}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scenario) SCENARIO="$2"; shift 2;;
    --seed) SEED="$2"; shift 2;;
    --repo-root) REPO_ROOT="$2"; shift 2;;
    --config-file) CONFIG_FILE="$2"; shift 2;;
    --bag-dir) BAG_DIR="$2"; shift 2;;
    --hardware-note) HARDWARE_NOTE="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

export ROS_DOMAIN_ID
export RMW_IMPLEMENTATION
export OOmWOO_USE_SIM_TIME="true"

METRICS_JSON="/tmp/oomwoo_baseline_${SCENARIO}_${SEED}.json"
RUN_META_JSON="/tmp/oomwoo_run_meta_${SCENARIO}_${SEED}.json"
REPORT_MD="baseline_report_${SCENARIO}_${SEED}.md"

cleanup() {
  echo ""
  echo "=== experiment interrupted; generating report ==="
  python3 "$(dirname "$0")/baseline_report.py" \
    --metrics "$METRICS_JSON" \
    --run-metadata "$RUN_META_JSON" \
    --output "$REPORT_MD" || true
}
trap cleanup INT TERM

echo "=== OOMWOO baseline experiment: scenario=$SCENARIO seed=$SEED ==="
echo "=== ROS_DOMAIN_ID=$ROS_DOMAIN_ID RMW=$RMW_IMPLEMENTATION ==="

ros2 launch oomwoo_baseline baseline_record.launch.py \
  scenario:="$SCENARIO" \
  seed:="$SEED" \
  repo_root:="$REPO_ROOT" \
  config_file:="$CONFIG_FILE" \
  bag_dir:="$BAG_DIR" \
  metrics_json:="$METRICS_JSON" \
  run_metadata_json:="$RUN_META_JSON" \
  hardware_note:="$HARDWARE_NOTE"

# Normal exit (launch terminated): generate report.
python3 "$(dirname "$0")/baseline_report.py" \
  --metrics "$METRICS_JSON" \
  --run-metadata "$RUN_META_JSON" \
  --output "$REPORT_MD"
echo "=== report: $REPORT_MD ==="
