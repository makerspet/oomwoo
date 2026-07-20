# Gazebo IR Homing Contract

Gazebo does not provide a native modulated-IR beacon/receiver sensor. This
contract defines the small logical sensor OOMWOO needs before dock-cycle work can
be tested headlessly.

## Geometry

Dock model:

- `dock_base_link`: static dock root frame.
- `dock_beacon_link`: IR emitter frame, centered on the dock face for v1.
- `charge_contact_left` / `charge_contact_right`: contact geometry for later
  docking success checks.

Robot receiver frames:

- `dock_ir_front_left_link`: baffled final-approach receiver.
- `dock_ir_front_right_link`: baffled final-approach receiver.
- `dock_ir_search_left_link`: wide-FoV side receiver for dock acquisition.
- `dock_ir_search_right_link`: wide-FoV side receiver for dock acquisition.

The model in `tools/oomwoo_dock_ir_model.py` assumes the front receivers are
slightly forward and separated laterally; search receivers sit on the left/right
sides and look outward.

## Signal Rules

For each receiver on each sim tick:

1. Transform receiver and beacon poses into the world frame.
2. Compute range and receiver-relative off-axis angle.
3. Drop the signal if range exceeds `max_range_m`.
4. Drop the signal if the beacon is outside the receiver FoV.
5. Drop the signal if line of sight is blocked.
6. Otherwise compute strength from range attenuation and angular gain.

The prototype uses circular blockers for deterministic tests. A Gazebo plugin can
replace this with physics ray checks against the world.

## Proposed Runtime Output

Initial simulation can publish JSON on a namespaced topic while message types are
still unsettled:

```text
/oomwoo/dock/ir_state    std_msgs/msg/String
```

Fields:

- `front_left`, `front_right`, `search_left`, `search_right`: strength values.
- `front_error`: normalized left/right front differential.
- `search_error`: normalized left/right search differential.
- `mode`: `final_centered`, `final_turn_left`, `final_turn_right`,
  `search_turn_left`, `search_turn_right`, or `search_pattern`.
- `angular_z_hint`: normalized steering hint, positive left.

Once stable, this should become a typed OOMWOO message package or be adapted into
the selected `opennav_docking` plugin interface.

## Failure Behavior

- If all receivers are blind, publish `mode=search_pattern` and zero steering
  hint.
- If front receivers see the beacon, final approach owns the signal.
- If front receivers are blind but side receivers see the beacon, search mode
  owns the signal.
- A stale IR frame must not keep commanding final approach. The controller should
  require fresh frames at a fixed rate.
