# Nav2 `opennav_docking` Integration Plan

The maintainer suggested using Nav2 docking for the state machine and simulating
IR separately. This contribution splits responsibilities that way.

## State Flow

1. **Predock navigation**
   - Use Nav2 `NavigateToPose` to drive to a known predock pose in front of the
     dock.
   - The predock pose comes from the known dock pose when localized, or from the
     find-dock reacquisition routine when localization failed.

2. **IR acquisition**
   - If the front receivers do not see the beacon, rotate/search using the
     left/right search receivers until the beacon enters the front receiver FoV.
   - If no receiver sees the beacon, use a bounded search pattern and report
     reacquisition failure after the configured timeout.

3. **Final approach**
   - Disable normal Nav2 velocity ownership for the final low-speed approach.
   - Use `front_error` from the IR model to steer toward zero differential.
   - Clamp linear and angular velocity tightly.
   - Stop immediately on bumper, cliff, wheel-drop, stale IR, or charge-contact
     mismatch.

4. **Contact confirmation**
   - Docking succeeds only when the robot is aligned and charge contact starts.
   - A simulated battery/charger state should later provide this confirmation.

5. **Service / recharge / resume**
   - While docked, wait for recharge or modeled station service completion.
   - Resume the interrupted cleaning job only after the dock-cycle reports a
     successful service result.

## Controller Inputs

- dock pose when known
- Nav2 result from predock navigation
- IR state from the logical sensor
- battery state
- charge-contact state
- safety events from recovery-safety / hardware bridge

## Controller Outputs

- Nav2 predock goal
- final low-speed velocity command during the final approach phase
- dock-cycle status
- service/recharge completion status for cleaning-jobs

## Arbitration Rule

Only one component should own motion at a time:

- Nav2 owns motion until the predock pose succeeds.
- dock-cycle owns low-speed motion only during final IR approach and undock.
- recovery-safety may preempt either one on bumper/cliff/wheel-drop/e-stop.

The first implementation can document this as launch/config discipline; later it
should become an explicit command arbiter or behavior-tree contract.
