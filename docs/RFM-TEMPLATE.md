# Request for Module (RFM): <Module Name>

> Copy this file into the module folder as `RFM.md` and fill it in.
> Hardware: `hardware/<module>/RFM.md` · Software: `software/<module>/RFM.md`.
> Contributors submit attempts under `hardware/<module>/<github-username>/`.

| Field | Value |
|---|---|
| **Module ID** | e.g. `hw-wheel-left` / `sw-odometry` |
| **Type** | Hardware / Software |
| **Status** | Open · In progress · Has candidates · Selected · Blocked |
| **Maintainer** | @username |
| **Depends on interface spec** | ARCHITECTURE.md §<n> (version/date) |
| **Phase** | MVP / Phase 2 / later |
| **Safety review required** | Yes / No |

## 1. Purpose
What this module does, in two or three sentences. Why it exists.

## 2. Requirements
Use MoSCoW. Be testable.
- **Must:** ...
- **Should:** ...
- **Could:** ...
- **Won't (this phase):** ...

## 3. Interfaces (the contract — fill in precisely)

### Hardware modules
- **Mechanical:** mounting points / bolt pattern (relative to `base_link`),
  bounding envelope (max W×D×H), mass budget, mating tolerances, print
  orientation, fasteners used.
- **Electrical:** connectors and pinouts, voltage rail(s), max current,
  signal levels, data bus.
- **Kinematic (if moving):** range of motion, forces/torques, speeds.

### Software modules
- **ROS2 published:** topics / services / actions (name, message type, rate).
- **ROS2 consumed:** topics / services / actions it subscribes to.
- **Parameters:** name, type, default, meaning.
- **Frames/TF:** frames published or required.

## 4. Constraints
- Cost target (per unit, low volume).
- Printability (FDM, no supports if possible, material e.g. PETG/PLA).
- Off-the-shelf parts preferred; list any required COTS part + source.
- Compute/memory budget (software).

## 5. State of the art / prior art (please research)
List the best existing solutions you found (commercial and DIY), with links, and
note what we can learn or reuse. A short SOTA scan is part of the contribution.

## 6. Acceptance criteria (how candidates are judged)
Objective, measurable. Examples:
- Passes the defined test (link to test in `software/regression-tests/` or a
  hardware test procedure).
- Meets mass/size/cost budget.
- Fits the reference chassis without modification to other modules.
- Documented and reproducible by someone else.

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.

## 7. Deliverables
- Source files (CAD source + exported STL; or source code + tests).
- BOM additions/changes.
- Build/run docs so others can reproduce it.
- Test results / evidence.
- Optional: a short demo photo or video (encouraged — good for the project).

## 8. How to contribute to this module
1. Comment on the module's issue/Discussion to claim or co-work it.
2. Read this RFM and `ARCHITECTURE.md`. Ask questions early.
3. Work under `hardware/<module>/<your-username>/` (or `software/...`).
4. Keep it interface-compliant. If the interface is wrong, raise it — don't
   silently diverge.
5. Open a focused PR. Iterate with review.

## 9. References
Links, datasheets, related modules, prior discussions.
