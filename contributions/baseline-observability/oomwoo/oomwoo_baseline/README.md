# oomwoo_baseline — Phase-0 基线 & 可观测性工具

OOMWOO 算法优化计划的 **阶段 0（建立可复现实验基线 + 可观测性）** 落地工具包。
对应 `jihua20260826.md` 的 §3 Phase 0、§5.1 测试矩阵与 §7 近期行动清单。

本包提供**可运行的 ROS2（Jazzy）代码与配置**，用于在任何一次实验中固定记录：
运行元数据、基线 topic 的 rosbag 录制、SLAM/Nav2/覆盖 KPI 采集，并生成基线报表。
所有话题/帧/状态字段对齐 `docs/SOFTWARE_INTERFACES.md`。

> ⚠️ 运行约束：本包需要 **Linux + ROS2 Jazzy + Gazebo**（及 `urdf-gazebo-sim` 提供的
> 世界与机器人描述）。在仅有 Windows 的开发机上可编写与单元测试，但**无法实际跑仿真**。
> 执行请在一台已 `colcon build` 好 workspace 的 ROS2 机器上进行。

## 目录结构

```
oomwoo_baseline/
├── package.xml
├── setup.py
├── resource/oomwoo_baseline
├── oomwoo_baseline/            # Python 包
│   ├── metrics.py              # 与 ROS 解耦的纯 KPI 计算（可单测）
│   ├── metrics_collector.py    # rclpy 节点：订阅基线 topic → JSON + CSV
│   ├── run_metadata.py         # 采集 ROS_DISTRO/RMW/Git SHA/seed/scenario
│   └── scenario_registry.py    # 加载 §5.1 场景注册表
├── launch/
│   └── baseline_record.launch.py   # rosbag 录制 + 采集节点 + 元数据节点
├── config/
│   └── scenario_registry.yaml     # 八个 §5.1 场景（固定 world/位姿/seed）
├── scripts/
│   ├── baseline_report.py     # 聚合指标 → markdown 基线报表
│   ├── system_sampler.py      # Linux /proc 采样 RSS/PSS/CPU（compute-benchmark）
│   └── run_experiment.sh      # 一键实验编排（固定 seed + scenario）
└── test/
    └── test_metrics.py        # 纯逻辑单测（unittest，无需 ROS2）
```

## 构建

```bash
cd ~/ros_ws
colcon build --packages-select oomwoo_baseline
source install/setup.bash
```

## 运行（单次实验）

先按 `SOFTWARE_INTERFACES.md` 启动 sim + Nav2 + SLAM bringup（来自
`contributions/urdf-gazebo-sim`），然后：

```bash
ros2 launch oomwoo_baseline baseline_record.launch.py \
  scenario:=single_room_empty seed:=42 \
  repo_root:=/path/to/robot_src \
  bag_dir:=/tmp/bags/sr42 \
  metrics_json:=/tmp/oomwoo_baseline_sr42.json \
  run_metadata_json:=/tmp/oomwoo_run_meta_sr42.json
```

Ctrl-C 结束后生成报表：

```bash
python3 $(ros2 pkg prefix oomwoo_baseline)/share/oomwoo_baseline/../scripts/baseline_report.py \
  --metrics /tmp/oomwoo_baseline_sr42.json \
  --run-metadata /tmp/oomwoo_run_meta_sr42.json \
  --output baseline_report_sr42.md
```

### 一键编排

```bash
./scripts/run_experiment.sh --scenario single_room_empty --seed 42 \
  --repo-root /path/to/robot_src --bag-dir /tmp/bags/sr42
```

脚本在 Ctrl-C 后自动调用 `baseline_report.py` 生成 `baseline_report_<scenario>_<seed>.md`。

## 计算资源采样（compute-benchmark）

在 ROS2 机器上，对 bringup 进程树采样 RSS/PSS/CPU：

```bash
python3 scripts/system_sampler.py --pid $BRINGUP_PID --duration-sec 120 \
  --interval-sec 2 --output /tmp/oomwoo_system_metrics.json
```

再把 `--system-metrics /tmp/oomwoo_system_metrics.json` 传给 `baseline_report.py`
即可在报表第 8 节看到进程级资源占用。

## 单元测试

纯逻辑（KPI 计算、场景解析）无需 ROS2，可在任意 Python 3.10+ 环境运行：

```bash
python3 -m unittest oomwoo_baseline.test.test_metrics -v
```
（或直接 `python3 oomwoo_baseline/test/test_metrics.py -v`）

## 采集的 KPI（对齐计划 §3 / compute-benchmark）

| 类别 | 指标 |
|---|---|
| LiDAR | 更新率 (Hz)、达标判定（≥5 Hz）、帧数 |
| TF | 延迟 mean/p50/p95/p99/max (ms) |
| 里程计 | 积分路径长、位姿位移、漂移比 |
| 运动 | cmd_vel 样本、陈旧事件（stale） |
| 碰撞 | bumper 左/右/总事件 |
| 地图 | 尺寸、空闲率、未知率 |
| 恢复 | 恢复延迟 mean/p95/max (ms) |
| 计算 | 进程 RSS/PSS/CPU、启动时间、峰值内存（system_sampler） |

## 与计划的对应关系

- **§3 Phase 0**：基线 + 可观测性 → 本包全部覆盖。
- **§5.1 测试矩阵**：8 个场景定义在 `config/scenario_registry.yaml`（固定 world/初始位姿/seed）。
- **§5.2 最低验收**：报表第 9 节给出自查项（LiDAR 率、可复现、动态障碍、断点续扫）。
- **§7 近期行动清单**：运行元数据捕获、场景注册、KPI 采集、报表生成均已落地为代码。

后续阶段（P1 SLAM/AMCL、P2 导航、P3 覆盖、P4 近场、P5 恢复、P6 资源）应在
**同一固定场景 + 固定 seed + 固定 Git SHA** 下复用本包做对照，确保每次改动可量化比较。
