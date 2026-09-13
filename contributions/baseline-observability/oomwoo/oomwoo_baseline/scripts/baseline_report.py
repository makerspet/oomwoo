#!/usr/bin/env python3
"""Generate a markdown baseline report from collected artifacts.

Aggregates:
  * metrics JSON  (from ``metrics_collector_node``)
  * run metadata JSON (from ``run_metadata_node``)
  * optional system metrics JSON (RSS/PSS/CPU/startup sampler)

Produces the Phase-0 baseline report required by the plan (§3 Phase 0 and the
``compute-benchmark`` metrics: RSS/PSS, CPU, startup, LiDAR rate, TF latency,
recovery latency). Uses only the Python standard library so it runs anywhere.

Usage::

    python3 baseline_report.py \\
        --metrics /tmp/oomwoo_baseline_metrics.json \\
        --run-metadata /tmp/oomwoo_run_metadata.json \\
        --system-metrics /tmp/oomwoo_system_metrics.json \\
        --output baseline_report.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def _load(path: str):
    if not path or not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return None


def _fmt(x, nd=3, suffix=""):
    if x is None:
        return "n/a"
    if isinstance(x, float):
        if x != x:  # NaN
            return "n/a"
        return f"{x:.{nd}f}{suffix}"
    return f"{x}{suffix}"


def _row(label, value):
    return f"| {label} | {value} |"


def build_report(metrics, meta, system) -> str:
    lines = []
    lines.append("# OOMWOO 基线报表 (Phase-0 Baseline)")
    lines.append("")
    lines.append(f"_generated: {datetime.now(timezone.utc).isoformat()}_")
    lines.append("")

    # --- run metadata ---
    lines.append("## 1. 运行元数据 (Run Metadata)")
    lines.append("")
    lines.append("| 字段 | 值 |")
    lines.append("| --- | --- |")
    if meta:
        for k in (
            "captured_at_utc", "ros_distro", "rmw_implementation",
            "ros_domain_id", "use_sim_time", "git_sha", "scenario",
            "seed", "config_file", "hardware_note", "python_version",
            "lidar_target_hz",
        ):
            if k in meta:
                lines.append(_row(k, _fmt(meta[k])))
    else:
        lines.append(_row("run metadata", "未采集 (run_metadata.json 缺失)"))
    lines.append("")

    # --- LiDAR ---
    lines.append("## 2. LiDAR / 传感器")
    lines.append("")
    scan = (metrics or {}).get("scan", {})
    lines.append("| 指标 | 值 |")
    lines.append("| --- | --- |")
    lines.append(_row("scan 帧数", scan.get("count")))
    lines.append(_row("更新率 (Hz)", _fmt(scan.get("rate_hz"))))
    lines.append(_row("目标 >= (Hz)", scan.get("expected_min_rate_hz")))
    lines.append(_row("达标", "YES" if scan.get("meets_target") else "NO"))
    lines.append("")

    # --- TF latency ---
    lines.append("## 3. TF 延迟")
    lines.append("")
    tf = (metrics or {}).get("tf_latency", {})
    lines.append("| 指标 | 值 (ms) |")
    lines.append("| --- | --- |")
    for k in ("n", "mean_ms", "p50_ms", "p95_ms", "p99_ms", "max_ms"):
        lines.append(_row(k, _fmt(tf.get(k), 2)))
    lines.append("")

    # --- odometry ---
    lines.append("## 4. 里程计一致性")
    lines.append("")
    odom = (metrics or {}).get("odom", {})
    lines.append("| 指标 | 值 |")
    lines.append("| --- | --- |")
    lines.append(_row("odom 帧数", odom.get("count")))
    lines.append(_row("积分路径长 (m)", _fmt(odom.get("integrated_distance_m"), 2)))
    lines.append(_row("位姿位移 (m)", _fmt(odom.get("pose_distance_m"), 2)))
    lines.append(_row("漂移比 (积分/位移)", _fmt(odom.get("drift_ratio"), 3)))
    lines.append("")

    # --- cmd_vel / bumper ---
    lines.append("## 5. 运动命令与碰撞")
    lines.append("")
    cmd = (metrics or {}).get("cmd_vel", {})
    bump = (metrics or {}).get("bumper", {})
    lines.append("| 指标 | 值 |")
    lines.append("| --- | --- |")
    lines.append(_row("cmd_vel 样本", cmd.get("samples")))
    lines.append(_row("陈旧事件 (stale)", cmd.get("stale_events")))
    lines.append(_row("bumper 左事件", bump.get("left_events")))
    lines.append(_row("bumper 右事件", bump.get("right_events")))
    lines.append(_row("bumper 总事件", bump.get("total_events")))
    lines.append("")

    # --- map ---
    lines.append("## 6. 地图")
    lines.append("")
    mp = (metrics or {}).get("map", {})
    lines.append("| 指标 | 值 |")
    lines.append("| --- | --- |")
    lines.append(_row("尺寸 (w x h)", f'{mp.get("width")} x {mp.get("height")}'))
    lines.append(_row("空闲率", _fmt(mp.get("free_ratio"), 3)))
    lines.append(_row("未知率", _fmt(mp.get("unknown_ratio"), 3)))
    lines.append("")

    # --- recovery ---
    lines.append("## 7. 恢复延迟")
    lines.append("")
    rec = (metrics or {}).get("recovery", {})
    lines.append("| 指标 | 值 (ms) |")
    lines.append("| --- | --- |")
    for k in ("n", "mean_ms", "p95_ms", "max_ms"):
        lines.append(_row(k, _fmt(rec.get(k), 2)))
    lines.append("")

    # --- system (compute-benchmark) ---
    lines.append("## 8. 计算资源 (compute-benchmark)")
    lines.append("")
    if system:
        lines.append("| 进程 | RSS (MB) | PSS (MB) | CPU % |")
        lines.append("| --- | --- | --- | --- |")
        for proc in system.get("processes", []):
            lines.append(
                f"| {proc.get('name','?')} | {_fmt(proc.get('rss_mb'),1)} "
                f"| {_fmt(proc.get('pss_mb'),1)} | {_fmt(proc.get('cpu_pct'),1)} |"
            )
        lines.append("")
        lines.append(_row("启动时间 (s)", _fmt(system.get("startup_sec"), 2)))
        lines.append(_row("峰值内存 (MB)", _fmt(system.get("peak_rss_mb"), 1)))
    else:
        lines.append("_system metrics 未采集 (system_metrics.json 缺失)。"
                     " 在 ROS2 机器上用 `system_sampler.py` 采集后重新生成。_")
        lines.append("")

    # --- acceptance checklist ---
    lines.append("## 9. 最低验收自查 (§5.2)")
    lines.append("")
    lines.append(f"- LiDAR 更新率维持 ~5 Hz: {'✅' if scan.get('meets_target') else '❌/未采集'}")
    lines.append("- 相同输入重复运行可复现: 需同 seed + 同 Git SHA 复跑验证")
    lines.append("- 动态障碍不导致永久中断: 见 bumper/恢复延迟指标")
    lines.append("- 断点续扫漏扫面积: 需 coverage 模块接入后测量")
    lines.append("")

    lines.append("---")
    lines.append("_Generated by oomwoo_baseline/scripts/baseline_report.py_")
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="OOMWOO baseline report generator")
    parser.add_argument("--metrics", default="/tmp/oomwoo_baseline_metrics.json")
    parser.add_argument("--run-metadata", default="/tmp/oomwoo_run_metadata.json")
    parser.add_argument("--system-metrics", default="")
    parser.add_argument("--output", default="")
    args = parser.parse_args(argv)

    metrics = _load(args.metrics)
    meta = _load(args.run_metadata)
    system = _load(args.system_metrics) if args.system_metrics else None

    if metrics is None and meta is None:
        print("ERROR: no metrics or run-metadata found; nothing to report.",
              file=sys.stderr)
        return 2

    report = build_report(metrics, meta, system)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"report written to {args.output}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
