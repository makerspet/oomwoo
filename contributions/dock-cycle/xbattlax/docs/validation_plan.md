# Dock Cycle Validation Plan

This plan keeps the first dock-cycle work measurable before the full Gazebo
plugin and robot URDF are stable.

## Phase 0: Geometry Unit Tests

Run:

```bash
python3 -m unittest discover \
  -s contributions/dock-cycle/xbattlax/tests \
  -p 'test_*.py'
```

Pass criteria:

- centered predock pose gives balanced front receivers
- lateral offset gives the correct steering direction
- side receivers can reacquire a dock that front receivers cannot see
- line-of-sight blockers zero the signal
- signal attenuates with distance

## Phase 1: Headless Scenario Traces

Run:

```bash
python3 contributions/dock-cycle/xbattlax/tools/sim_dock_ir_scenario.py
```

Capture JSONL output as a CI artifact. Track:

- mode transitions
- front differential error
- search differential error
- receiver visibility
- steering hint sign

## Phase 2: Gazebo Logical Sensor

Embed the same rules in a Gazebo logical sensor/plugin:

- publish fresh IR frames at a fixed rate
- compute line of sight from world geometry
- expose receiver frames in TF/URDF
- keep dock beacon and wall-illumination modes distinguishable

Pass criteria:

- 95 percent final-dock success from seeded predock poses
- final yaw error under 5 degrees
- lateral dock-contact error under the charge-contact tolerance selected by the
  mechanical design
- stale IR frames stop final approach instead of continuing motion

## Phase 3: Dock-Cycle Behavior

Add undock, predock navigation, final IR approach, charge confirmation, recharge,
and resume hooks.

Pass criteria:

- undock reaches a known start pose
- low battery triggers return-to-dock
- job resumes after simulated recharge
- find-dock recovers from seeded lost poses when the beacon is visible
- recovery-safety preempts dock-cycle on bumper/cliff/wheel-drop/e-stop
