"""Framework-agnostic KPI math for the OOMWOO baseline harness.

This module has **no ROS2 dependency** so it can be unit-tested with plain
``unittest`` (see ``test/test_metrics.py``). The rclpy node in
``metrics_collector.py`` converts ROS messages into the primitive values fed
here.

All times are seconds (``float``). Latency is expressed in milliseconds in the
snapshot for readability.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence


def _percentile(sorted_samples: Sequence[float], q: float) -> float:
    """Linear-interpolation percentile, numpy-style. ``q`` is 0..100."""
    if not sorted_samples:
        return float("nan")
    if len(sorted_samples) == 1:
        return float(sorted_samples[0])
    rank = (q / 100.0) * (len(sorted_samples) - 1)
    lo = int(math.floor(rank))
    hi = int(math.ceil(rank))
    if lo == hi:
        return float(sorted_samples[lo])
    frac = rank - lo
    return float(sorted_samples[lo] * (1 - frac) + sorted_samples[hi] * frac)


@dataclass
class MetricsAggregator:
    """Accumulates raw samples and derives Phase-0 KPIs.

    Thresholds are configurable so tests and scenarios can tune them.
    """

    scan_drop_gap_sec: float = 0.4
    cmd_vel_stale_sec: float = 0.5

    # --- raw counters / buffers -------------------------------------------
    _scan_stamps: List[float] = field(default_factory=list)
    _scan_recv: List[float] = field(default_factory=list)
    _tf_latency_ms: List[float] = field(default_factory=list)
    _tf_stamps: List[float] = field(default_factory=list)

    _odom_recv: List[float] = field(default_factory=list)
    _odom_x: List[float] = field(default_factory=list)
    _odom_y: List[float] = field(default_factory=list)
    _odom_integrated: float = 0.0
    _odom_pose_dist: float = 0.0
    _odom_prev: Optional[tuple] = None  # (stamp, x, y)

    _cmd_vel_recv: List[float] = field(default_factory=list)
    _cmd_vel_stale_events: int = 0
    _cmd_vel_prev_recv: Optional[float] = None

    _bumper_left_events: int = 0
    _bumper_right_events: int = 0
    _bumper_left_prev: bool = False
    _bumper_right_prev: bool = False

    _map_free_ratio: float = float("nan")
    _map_unknown_ratio: float = float("nan")
    _map_width: int = 0
    _map_height: int = 0

    _recovery_start: Optional[float] = None
    _recovery_latency_ms: List[float] = field(default_factory=list)
    _status_transitions: int = 0
    _last_status_state: Optional[str] = None

    _start_wall: Optional[float] = None
    _end_wall: Optional[float] = None

    # ------------------------------------------------------------------ #
    # recording primitives
    # ------------------------------------------------------------------ #
    def _touch(self, recv_sec: float) -> None:
        if self._start_wall is None or recv_sec < self._start_wall:
            self._start_wall = recv_sec
        if self._end_wall is None or recv_sec > self._end_wall:
            self._end_wall = recv_sec

    def record_scan(self, header_stamp_sec: float, recv_sec: float) -> None:
        self._touch(recv_sec)
        if self._scan_stamps:
            gap = header_stamp_sec - self._scan_stamps[-1]
            # Overly large time gaps indicate dropped scans.
            if gap > self.scan_drop_gap_sec:
                pass  # counted implicitly via rate; keep simple
        self._scan_stamps.append(header_stamp_sec)
        self._scan_recv.append(recv_sec)

    def record_tf(self, header_stamp_sec: float, recv_sec: float) -> None:
        self._touch(recv_sec)
        latency_ms = (recv_sec - header_stamp_sec) * 1000.0
        if latency_ms >= 0.0:  # ignore clock-ordering noise
            self._tf_latency_ms.append(latency_ms)
        self._tf_stamps.append(header_stamp_sec)

    def record_odom(
        self,
        stamp_sec: float,
        x: float,
        y: float,
        vx: float,
        vy: float,
        recv_sec: float,
    ) -> None:
        self._touch(recv_sec)
        self._odom_recv.append(recv_sec)
        self._odom_x.append(x)
        self._odom_y.append(y)
        if self._odom_prev is not None:
            p_stamp, p_x, p_y = self._odom_prev
            dt = max(0.0, stamp_sec - p_stamp)
            speed = math.hypot(vx, vy)
            self._odom_integrated += speed * dt
            seg = math.hypot(x - p_x, y - p_y)
            self._odom_pose_dist += seg
        self._odom_prev = (stamp_sec, x, y)

    def record_cmd_vel(self, recv_sec: float, has_motion: bool) -> None:
        self._touch(recv_sec)
        self._cmd_vel_recv.append(recv_sec)
        if self._cmd_vel_prev_recv is not None and has_motion:
            gap = recv_sec - self._cmd_vel_prev_recv
            if gap > self.cmd_vel_stale_sec:
                self._cmd_vel_stale_events += 1
        self._cmd_vel_prev_recv = recv_sec

    def record_bumper(self, side: str, has_contact: bool, recv_sec: float) -> None:
        self._touch(recv_sec)
        if side == "left":
            if has_contact and not self._bumper_left_prev:
                self._bumper_left_events += 1
            self._bumper_left_prev = has_contact
        elif side == "right":
            if has_contact and not self._bumper_right_prev:
                self._bumper_right_events += 1
            self._bumper_right_prev = has_contact

    def record_map(self, width: int, height: int, data: Sequence[int]) -> None:
        """``data`` is the OccupancyGrid ``data`` field (int8 values -1..100)."""
        if not data:
            return
        free = sum(1 for c in data if c == 0)
        unknown = sum(1 for c in data if c == -1)
        total = len(data)
        self._map_width = width
        self._map_height = height
        self._map_free_ratio = free / total if total else float("nan")
        self._map_unknown_ratio = unknown / total if total else float("nan")

    def record_status(self, recv_sec: float, state: str, reason_code: str) -> None:
        self._touch(recv_sec)
        if self._last_status_state is not None and state != self._last_status_state:
            self._status_transitions += 1
        if state == "RECOVERING" or reason_code in ("RECOVERY_STARTED",):
            if self._recovery_start is None:
                self._recovery_start = recv_sec
        elif (state in ("RECOVERED", "RECOVERY_ESCALATED", "READY")
              or reason_code in ("RECOVERED",)) and self._recovery_start is not None:
            latency_ms = (recv_sec - self._recovery_start) * 1000.0
            if latency_ms >= 0:
                self._recovery_latency_ms.append(latency_ms)
            self._recovery_start = None
        self._last_status_state = state

    # ------------------------------------------------------------------ #
    # derived snapshot
    # ------------------------------------------------------------------ #
    def _scan_rate_hz(self) -> float:
        if len(self._scan_stamps) < 2:
            return float("nan")
        span = self._scan_stamps[-1] - self._scan_stamps[0]
        if span <= 0:
            return float("nan")
        return (len(self._scan_stamps) - 1) / span

    def _tf_latency_stats(self) -> dict:
        s = sorted(self._tf_latency_ms)
        return {
            "n": len(s),
            "mean_ms": (sum(s) / len(s)) if s else float("nan"),
            "p50_ms": _percentile(s, 50),
            "p95_ms": _percentile(s, 95),
            "p99_ms": _percentile(s, 99),
            "max_ms": max(s) if s else float("nan"),
        }

    def _recovery_stats(self) -> dict:
        s = sorted(self._recovery_latency_ms)
        return {
            "n": len(s),
            "mean_ms": (sum(s) / len(s)) if s else float("nan"),
            "p95_ms": _percentile(s, 95),
            "max_ms": max(s) if s else float("nan"),
        }

    def snapshot(self) -> dict:
        """Return a JSON-serialisable dict of all computed KPIs."""
        odom_drift_ratio = (
            self._odom_integrated / self._odom_pose_dist
            if self._odom_pose_dist > 1e-6
            else float("nan")
        )
        wall_duration = (
            (self._end_wall - self._start_wall)
            if (self._start_wall is not None and self._end_wall is not None)
            else float("nan")
        )
        rate = self._scan_rate_hz()
        return {
            "wall_duration_sec": wall_duration,
            "scan": {
                "count": len(self._scan_stamps),
                "rate_hz": rate,
                "expected_min_rate_hz": 5.0,
                "meets_target": (
                    rate >= (5.0 - 1e-3)
                    if not math.isnan(rate)
                    else False
                ),
            },
            "tf_latency": self._tf_latency_stats(),
            "odom": {
                "count": len(self._odom_recv),
                "integrated_distance_m": self._odom_integrated,
                "pose_distance_m": self._odom_pose_dist,
                "drift_ratio": odom_drift_ratio,
            },
            "cmd_vel": {
                "samples": len(self._cmd_vel_recv),
                "stale_events": self._cmd_vel_stale_events,
                "stale_threshold_sec": self.cmd_vel_stale_sec,
            },
            "bumper": {
                "left_events": self._bumper_left_events,
                "right_events": self._bumper_right_events,
                "total_events": self._bumper_left_events + self._bumper_right_events,
            },
            "map": {
                "width": self._map_width,
                "height": self._map_height,
                "free_ratio": self._map_free_ratio,
                "unknown_ratio": self._map_unknown_ratio,
            },
            "recovery": self._recovery_stats(),
            "status_transitions": self._status_transitions,
        }
