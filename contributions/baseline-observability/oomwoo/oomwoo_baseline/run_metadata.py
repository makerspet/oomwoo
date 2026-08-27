"""Capture reproducible-run metadata for OOMWOO baseline experiments.

Mirrors the ``compute-benchmark`` acceptance criteria: every run must record
ROS distro, RMW, hardware/RAM note, LiDAR rate target, scenario, random seed
and Git SHA so results are reproducible by another contributor.

``capture_run_metadata`` is pure (no ROS2) and unit-testable; ``RunMetadataNode``
writes the result to ``run_metadata.json`` at startup.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from typing import Dict, Optional


def _git_sha(repo_root: Optional[str]) -> str:
    if not repo_root:
        return "unknown"
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except (subprocess.SubprocessError, OSError):
        pass
    return "unknown"


def capture_run_metadata(
    *,
    repo_root: Optional[str] = None,
    scenario: str = "",
    seed: Optional[int] = None,
    config_file: str = "",
    hardware_note: str = "",
    extra: Optional[Dict] = None,
) -> Dict:
    """Return a JSON-serialisable dict of run metadata."""
    return {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "ros_distro": os.environ.get("ROS_DISTRO", "unknown"),
        "rmw_implementation": os.environ.get("RMW_IMPLEMENTATION", "unknown"),
        "ros_domain_id": os.environ.get("ROS_DOMAIN_ID", "unknown"),
        "use_sim_time": os.environ.get("OOmWOO_USE_SIM_TIME", "true"),
        "git_sha": _git_sha(repo_root),
        "scenario": scenario,
        "seed": seed,
        "config_file": config_file,
        "hardware_note": hardware_note or platform.platform(),
        "python_version": platform.python_version(),
        "lidar_target_hz": 5.0,
        "extra": extra or {},
    }


def main(args=None):
    import rclpy  # noqa: WPS433 - lazy import keeps module testable
    from rclpy.node import Node

    class _Node(Node):
        def __init__(self):
            super().__init__("oomwoo_baseline_metadata")
            self.declare_parameter("repo_root", "")
            self.declare_parameter("scenario", "")
            self.declare_parameter("seed", 0)
            self.declare_parameter("config_file", "")
            self.declare_parameter("output_json", "/tmp/oomwoo_run_metadata.json")
            self.declare_parameter("hardware_note", "")

            meta = capture_run_metadata(
                repo_root=self.get_parameter("repo_root").value or None,
                scenario=self.get_parameter("scenario").value,
                seed=self.get_parameter("seed").value,
                config_file=self.get_parameter("config_file").value,
                hardware_note=self.get_parameter("hardware_note").value or "",
            )
            out = self.get_parameter("output_json").value
            try:
                with open(out, "w", encoding="utf-8") as fh:
                    json.dump(meta, fh, indent=2, sort_keys=True)
                self.get_logger().info(f"run metadata written to {out} (sha={meta['git_sha']})")
            except OSError as exc:
                self.get_logger().warn(f"failed to write run metadata: {exc}")
            # Publish once then exit; launch treats it as a one-shot.
            self.get_logger().info(f"run metadata: {json.dumps(meta, sort_keys=True)}")

    rclpy.init(args=args)
    node = _Node()
    try:
        rclpy.spin_once(node, timeout_sec=1.0)
    except (KeyboardInterrupt, Exception):
        pass
    finally:
        node.destroy_node()
        try:
            if rclpy.ok():
                rclpy.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()
