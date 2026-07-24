# Clean-and-Map Implementation by @Arkz-Deepak

This is a pointer to my self-hosted implementation of the `clean-and-map` module. 

**Repository Link:** [https://github.com/Arkz-Deepak/oomwoo-clean-and-map-arkz](https://github.com/Arkz-Deepak/oomwoo-clean-and-map-arkz)

## Approach
Following the maintainer's recommendation, I am breaking this down into phases. I am starting with a "clean-only" MVP using a pre-existing map to ensure the coverage path planning (CPP) logic scores well on the regression tests before introducing simultaneous SLAM.

## Progress Update
- [x] Initial self-hosted repository created.
- [x] Pointer PR submitted to OOMWOO main repository.
- [ ] Establish basic coverage path planning (CPP) node on a known map.
- [ ] Pass the `coverage_regression.launch.py` harness.
- [ ] Integrate simultaneous mapping (SLAM).
- [ ] Handle bumper edge cases and LiDAR-invisible obstacles.

## Instructions
*Installation and run instructions will be updated here and in the self-hosted repo once the baseline ROS 2 node is functional.*
