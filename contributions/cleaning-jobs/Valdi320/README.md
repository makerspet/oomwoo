# Valdi320 cleaning-jobs

Experimental Apache-2.0 ROS2 cleaning jobs: [independent source](https://github.com/Valdi320/oomwoo-cleaning-jobs) at [tested commit 3f3cd7025ab2](https://github.com/Valdi320/oomwoo-cleaning-jobs/commit/3f3cd7025ab242564d9a940f15009b2edaabca63).

**Run (Linux):** checkout that commit and run `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_*.py' -q`.

**Latest:** opt-in `transit_only=True` rejects coverage/unknown Nav2 action goals before dispatch; [design and limitations](https://github.com/Valdi320/oomwoo-cleaning-jobs/blob/3f3cd7025ab242564d9a940f15009b2edaabca63/docs/NAV2_REACTIVE_TRANSIT_BOUNDARY_20261029.md).

**Tests:** focused 8/8, full 691/691, Python -O 691/691 PASS (synthetic); [exact-commit CI](https://github.com/Valdi320/oomwoo-cleaning-jobs/commit/3f3cd7025ab242564d9a940f15009b2edaabca63/checks) (inspect current status).

**Details:** [historical review log](https://github.com/Valdi320/oomwoo-cleaning-jobs/blob/3f3cd7025ab242564d9a940f15009b2edaabca63/docs/PR79_REVIEW_LOG_ARCHIVE_20261029.md); [prior real ROS2/Gazebo evidence](https://github.com/Valdi320/oomwoo-cleaning-jobs/tree/3f3cd7025ab242564d9a940f15009b2edaabca63/docs).

**Not hardware-validated:** reactive executor integration, cmd_vel arbitration, physical interlocks and ARM profiling remain pending.
