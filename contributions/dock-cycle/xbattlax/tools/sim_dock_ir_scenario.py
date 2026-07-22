#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from math import pi
from pathlib import Path
import sys


if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent))

from oomwoo_dock_ir_model import (  # noqa: E402
    CircleObstacle,
    DockSpec,
    Pose2D,
    compute_homing_frame,
)


SCENARIOS = {
    "centered": (
        Pose2D(1.40, 0.00, pi),
        Pose2D(1.00, 0.00, pi),
        Pose2D(0.65, 0.00, pi),
    ),
    "offset": (
        Pose2D(1.10, 0.18, pi),
        Pose2D(1.00, 0.10, pi),
        Pose2D(0.85, -0.12, pi),
    ),
    "search": (
        Pose2D(0.35, 1.00, -pi / 2.0),
        Pose2D(0.35, -1.00, pi / 2.0),
        Pose2D(-0.80, 0.00, 0.0),
    ),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate OOMWOO dock IR frames.")
    parser.add_argument(
        "--scenario",
        choices=sorted((*SCENARIOS.keys(), "blocked", "all")),
        default="all",
    )
    args = parser.parse_args()

    scenario_names = [*SCENARIOS, "blocked"]
    if args.scenario != "all":
        scenario_names = [args.scenario]

    dock = DockSpec()
    for name in scenario_names:
        if name == "blocked":
            poses = (Pose2D(1.0, 0.0, pi),)
            obstacles = (CircleObstacle(0.50, 0.0, 0.12),)
        else:
            poses = SCENARIOS[name]
            obstacles = ()

        for index, pose in enumerate(poses):
            frame = compute_homing_frame(pose, dock, obstacles=obstacles)
            payload = {
                "scenario": name,
                "sample": index,
                "robot_pose": asdict(pose),
                **asdict(frame),
            }
            print(json.dumps(payload, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
