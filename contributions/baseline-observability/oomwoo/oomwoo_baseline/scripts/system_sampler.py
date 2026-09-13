#!/usr/bin/env python3
"""Sample RSS/PSS/CPU of a ROS2 process tree (Linux /proc, stdlib only).

Supports the ``compute-benchmark`` metrics (RSS/PSS per process, CPU,
startup time) without external dependencies. Run on the Linux ROS2 machine
alongside the bringup; pass the PID of the top-level ``ros2 launch`` process.

Usage::

    python3 system_sampler.py --pid $BRINGUP_PID --duration-sec 120 \\
        --interval-sec 2 --output /tmp/oomwoo_system_metrics.json
"""

from __future__ import annotations

import argparse
import os
import time


PAGE_SIZE = os.sysconf("SC_PAGE_SIZE") if hasattr(os, "sysconf") else 4096


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as fh:
        return fh.read()


def _children(pids: set[int]) -> set[int]:
    """Expand a PID set with all descendants found in /proc."""
    result = set(pids)
    try:
        for entry in os.listdir("/proc"):
            if not entry.isdigit():
                continue
            pid = int(entry)
            if pid in result:
                continue
            try:
                ppid = int(_read(f"/proc/{pid}/status").split("PPid:")[1].split()[0])
            except (OSError, IndexError):
                continue
            if ppid in result:
                result.add(pid)
    except OSError:
        pass
    return result


def _proc_sample(pid: int):
    try:
        statm = _read(f"/proc/{pid}/statm").split()
        rss_pages = int(statm[1])
        status = _read(f"/proc/{pid}/status")
        name = status.split("Name:")[1].split("\n")[0].strip()
        pss_mb = 0.0
        try:
            for line in _read(f"/proc/{pid}/smaps").splitlines():
                if line.startswith("Pss:"):
                    pss_mb += float(line.split()[1]) / 1024.0
        except OSError:
            pss_mb = float(rss_pages) * PAGE_SIZE / (1024.0 * 1024.0)
        return {
            "pid": pid,
            "name": name,
            "rss_mb": rss_pages * PAGE_SIZE / (1024.0 * 1024.0),
            "pss_mb": pss_mb,
        }
    except OSError:
        return None


def _cpu_pct(pid: int, interval: float) -> float:
    def _jiffies(p: int) -> int:
        try:
            parts = _read(f"/proc/{p}/stat").split()
            # utime=14, stime=15 (1-indexed fields in `stat`)
            return int(parts[13]) + int(parts[14])
        except (OSError, IndexError):
            return 0

    j0 = _jiffies(pid)
    t0 = time.time()
    time.sleep(interval)
    j1 = _jiffies(pid)
    t1 = time.time()
    dt = max(1e-6, t1 - t0)
    return max(0.0, (j1 - j0) / os.sysconf("SC_CLK_TCK") / dt * 100.0)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Linux /proc system sampler")
    parser.add_argument("--pid", type=int, required=True)
    parser.add_argument("--duration-sec", type=float, default=60.0)
    parser.add_argument("--interval-sec", type=float, default=2.0)
    parser.add_argument("--output", default="/tmp/oomwoo_system_metrics.json")
    args = parser.parse_args(argv)

    tree = _children({args.pid})
    end = time.time() + args.duration_sec
    samples = []
    while time.time() < end:
        snap = []
        for pid in list(tree):
            s = _proc_sample(pid)
            if s is None:
                tree.discard(pid)
                continue
            s["cpu_pct"] = _cpu_pct(pid, min(args.interval_sec, 0.5))
            snap.append(s)
        if snap:
            samples.append(snap)
        time.sleep(max(0.1, args.interval_sec - 0.5))

    # Aggregate mean RSS/PSS/CPU per process name across samples.
    agg = {}
    for snap in samples:
        for s in snap:
            a = agg.setdefault(s["name"], {"rss_mb": [], "pss_mb": [], "cpu_pct": []})
            a["rss_mb"].append(s["rss_mb"])
            a["pss_mb"].append(s["pss_mb"])
            a["cpu_pct"].append(s["cpu_pct"])

    processes = []
    peak_rss = 0.0
    for name, vals in agg.items():
        rss = max(vals["rss_mb"])
        peak_rss = max(peak_rss, rss)
        processes.append({
            "name": name,
            "rss_mb": round(rss, 1),
            "pss_mb": round(max(vals["pss_mb"]), 1),
            "cpu_pct": round(sum(vals["cpu_pct"]) / len(vals["cpu_pct"]), 1),
        })

    out = {
        "sampled_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_sec": args.duration_sec,
        "interval_sec": args.interval_sec,
        "processes": processes,
        "peak_rss_mb": round(peak_rss, 1),
        "note": "RSS/PSS sampled from /proc; CPU is mean over interval.",
    }
    with open(args.output, "w", encoding="utf-8") as fh:
        import json
        json.dump(out, fh, indent=2, sort_keys=True)
    print(f"system metrics written to {args.output} ({len(processes)} processes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
