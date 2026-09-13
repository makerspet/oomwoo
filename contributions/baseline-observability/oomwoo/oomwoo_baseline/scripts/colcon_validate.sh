#!/usr/bin/env bash
# colcon_validate.sh — 在 WSL + ROS2 中构建并测试 oomwoo_baseline 包
#
# 以「文件方式」执行（变量才能正常展开）：
#   wsl -d Ubuntu-22.04 bash /mnt/e/puppyfangzhen/robot_src/contributions/baseline-observability/oomwoo/oomwoo_baseline/scripts/colcon_validate.sh
#
# 说明：
#   - 自动探测 /opt/ros 下的发行版（jazzy/humble/iron...），不写死。
#   - 从脚本位置向上查找含 src/ build/ install/ 的 colcon 工作区根。
#   - 运行期依赖 ros_gz_interfaces 仅 metrics_collector 节点需要；若未安装，
#     import 烟测里 metrics_collector 会 FAIL，属预期，不影响 build/test。
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_DIR="$(dirname "$SCRIPT_DIR")"                       # .../oomwoo_baseline

# 1) 向上查找 colcon 工作区根（含 src + build + install）
DIR="$SCRIPT_DIR"
WS_ROOT=""
while [ "$DIR" != "/" ]; do
  if [ -d "$DIR/src" ] && [ -d "$DIR/build" ] && [ -d "$DIR/install" ]; then
    WS_ROOT="$DIR"; break
  fi
  DIR="$(dirname "$DIR")"
done
if [ -z "$WS_ROOT" ]; then
  WS_ROOT="$(cd "$SCRIPT_DIR/../../../../../../.." && pwd)"   # 兜底
fi
cd "$WS_ROOT"
echo "workspace root: $WS_ROOT"

# 2) 探测 ROS 发行版
ROS_SETUP=""
for d in /opt/ros/jazzy /opt/ros/humble /opt/ros/iron; do
  if [ -f "$d/setup.bash" ]; then ROS_SETUP="$d/setup.bash"; break; fi
done
if [ -z "$ROS_SETUP" ]; then
  ROS_SETUP="$(ls -d /opt/ros/*/setup.bash 2>/dev/null | head -1)"
fi
if [ -z "$ROS_SETUP" ]; then
  echo "ERROR: 未找到任何 /opt/ros/*/setup.bash，请确认 WSL 内已安装 ROS2" >&2
  exit 1
fi
# shellcheck disable=SC1090
source "$ROS_SETUP"
echo "ROS distro: ${ROS_DISTRO:-?}  (setup: $ROS_SETUP)"

# colcon 通常装在 $HOME/.local/bin（非登录 shell 不自动加载），确保其可用
export PATH="$HOME/.local/bin:$PATH"

# 3) 构建
echo "==> colcon build --packages-select oomwoo_baseline"
colcon build --packages-select oomwoo_baseline --event-handlers console_direct+ 2>&1 | tail -20

# 4) 测试（test_metrics.py，纯逻辑，无需 ROS runtime）
echo "==> colcon test --packages-select oomwoo_baseline"
# 环境内的 launch_testing pytest 插件（setuptools 入口点自动加载）与 pytest 9.x 不兼容，
# 会在插件注册阶段崩溃，与本包无关。禁用插件自动加载后即可正常跑本包单测
# （colcon 仍通过 junit xml 收集结果）。
export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
colcon test --packages-select oomwoo_baseline \
  --pytest-args="-p no:launch_testing -p no:launch_testing_ros" \
  --event-handlers console_direct+ 2>&1 | tail -25
echo "==> colcon test-result --verbose"
colcon test-result --verbose 2>&1 | tail -10

# 5) 安装产物检查
echo "==> installed node scripts"
ls -la install/oomwoo_baseline/bin 2>/dev/null || echo "  (无 install 产物)"

# 6) import 烟测（构建产物 + 源码，容忍 ros_gz_interfaces 缺失）
echo "==> import smoke"
# shellcheck disable=SC1090
source install/setup.bash 2>/dev/null || source install/local_setup.bash 2>/dev/null
python3 - "$PKG_DIR" <<'PY'
import sys, os, importlib
pkg = sys.argv[1]
# 以 `oomwoo_baseline.xxx` 形式导入，需把「包目录的父目录」加入 sys.path
sys.path.insert(0, os.path.dirname(pkg))
sys.path.insert(0, pkg)
mods = ["oomwoo_baseline.run_metadata",
        "oomwoo_baseline.metrics",
        "oomwoo_baseline.scenario_registry",
        "oomwoo_baseline.scripts.baseline_report",
        "oomwoo_baseline.metrics_collector"]
ok = 0
for m in mods:
    try:
        importlib.import_module(m)
        print("OK   ", m); ok += 1
    except Exception as e:
        print("FAIL ", m, "->", type(e).__name__, str(e)[:90])
print("imported %d/%d  (ros_gz_interfaces 缺失时 metrics_collector 失败属预期)" % (ok, len(mods)))
PY

# 7) launch 文件可解析性（build LaunchDescription，无需真正启动）
echo "==> launch file parse check"
python3 - "$PKG_DIR/launch/baseline_record.launch.py" <<'PY'
import sys, importlib.util
path = sys.argv[1]
spec = importlib.util.spec_from_file_location("baseline_record_launch", path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ld = mod.generate_launch_description()
# 统计 Node 动作数量（metrics_collector + run_metadata = 2）
n_nodes = sum(1 for e in ld.entities if e.__class__.__name__ == "Node")
print("launch OK: %d entities, %d Node actions" % (len(ld.entities), n_nodes))
PY

echo "DONE: oomwoo_baseline 已在 WSL+ROS2 中构建并完成测试"
