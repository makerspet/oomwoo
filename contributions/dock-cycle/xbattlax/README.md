# Dock Cycle IR Homing Prototype by xbattlax

This contribution turns the current dock-cycle RFC into a concrete, testable
simulation contract for the first docking implementation.

It focuses on the piece Gazebo does not provide out of the box: simulated IR
homing and dock-acquisition sensors. The model is dependency-free Python so the
geometry, line-of-sight, receiver fields of view, differential steering signal,
and acceptance metrics can be reviewed before being embedded in a Gazebo plugin
or ROS2 node.

## What This Adds

- a deterministic dock IR beacon / receiver model
- four receiver roles matching the RFC:
  - front-left and front-right baffled final-approach receivers
  - left and right wider-FoV dock-search receivers
- line-of-sight occlusion using circular blockers
- range attenuation and receiver FoV filtering
- a normalized final-approach steering error
- a normalized search/acquisition steering error
- a small JSONL scenario runner for CI-friendly traces
- regression tests for centered approach, offset approach, side search, blockers,
  and range attenuation

## Files

| File | Purpose |
|---|---|
| [`tools/oomwoo_dock_ir_model.py`](tools/oomwoo_dock_ir_model.py) | Pure Python geometry and IR signal model. |
| [`tools/sim_dock_ir_scenario.py`](tools/sim_dock_ir_scenario.py) | Deterministic JSONL scenario runner. |
| [`tests/test_oomwoo_dock_ir_model.py`](tests/test_oomwoo_dock_ir_model.py) | Regression tests for the model. |
| [`docs/gazebo_ir_homing_contract.md`](docs/gazebo_ir_homing_contract.md) | Proposed Gazebo logical-sensor contract. |
| [`docs/opennav_docking_integration.md`](docs/opennav_docking_integration.md) | How this feeds Nav2 `opennav_docking`. |
| [`docs/validation_plan.md`](docs/validation_plan.md) | Headless metrics for dock, undock, and find-dock. |

## Run the Model

```bash
python3 contributions/dock-cycle/xbattlax/tools/sim_dock_ir_scenario.py
```

Example output is JSON Lines: one frame per robot pose, with receiver strengths,
range/bearing data, selected mode, and normalized steering hint.

## Test

```bash
python3 -m unittest discover \
  -s contributions/dock-cycle/xbattlax/tests \
  -p 'test_*.py'
```

## Intended ROS2/Gazebo Path

1. Add a generic dock model to the living-room world with a beacon frame.
2. Add four logical IR receivers to the robot URDF:
   - `dock_ir_front_left_link`
   - `dock_ir_front_right_link`
   - `dock_ir_search_left_link`
   - `dock_ir_search_right_link`
3. Implement a small Gazebo logical sensor/plugin using the same geometry rules
   in this prototype.
4. Publish dock IR state for the dock-cycle controller.
5. Use Nav2 to reach the predock pose, then use the front differential signal
   for the final low-speed approach.

This contribution deliberately does not rewrite `urdf-gazebo-sim` or the main
dock-cycle RFC. It is a namespaced prototype that can be folded into the
official simulation once the maintainers are happy with the contract.
