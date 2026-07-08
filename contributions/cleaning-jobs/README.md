# Cleaning Modes, Zones & Job Orchestration (ROS2 package)

The user-facing *"what and where to clean,"* plus managing *long jobs*. This
package adds cleaning *modes* (regular whole-floor, spot), *virtual walls /
no-go zones*, *segmenting the map into rooms*, and a *job orchestrator* that
splits a clean into manageable pieces — pausing to *recharge, auto-empty, or wash
the mop*, then *resuming where it left off*. Because the physical robot isn't
built yet, this is a *Gazebo simulation*; it is later re-validated on hardware in
the [live-robot-bringup RFC](../live-robot-bringup).

> *Status — ready to start work.* No need to wait for OOMWOO hardware — develop it in the
> Gazebo sim ([urdf-gazebo-sim](../urdf-gazebo-sim)) or on the real
> [placeholder Proscenic M6 Pro](https://makerspet.com/blog/tutorial-connect-robot-vacuum-cleaner-to-ros-2-proscenic-m6-pro/).
> Say so in the [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

# Important References
- [clean-and-map RFC](../clean-and-map) — coverage cleaning and its done condition; this orchestrates and segments it.
- [nav-localize RFC](../nav-localize) — the saved map this segments and the resume-after-interruption support.
- [dock-cycle RFC](../dock-cycle) — the recharge / auto-empty / mop-wash station services a job pauses for.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract for simulation-first modules.
- [OOMWOO ROS2 development](https://github.com/makerspet/oomwoo-install) — build OOMWOO ROS2 Docker image(s) with your packages.
- Nav2 keepout/zone costmap filters are a good starting point for no-go zones.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- [Discord server](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- *map segmentation into rooms / zones*
  - split a saved map into rooms/zones (automatic segmentation plus manual labeling) and persist it
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) to let everyone know you're working on it, and post your progress
- *cleaning modes*
  - *regular* (whole map, or selected rooms), *spot* (clean a small local area), configurable
  - defer wall/edge mode to [floor-care](../floor-care); call it where useful
- *virtual walls / no-go zones*
  - define keep-out regions the planner respects (e.g. Nav2 keepout filter); editable and persisted
- *job orchestration (split a clean into manageable pieces)*
  - monitor battery / dust bin / mop state during a clean
  - *suspend* the job and dock for *recharge / auto-empty / mop-wash* (via [dock-cycle](../dock-cycle)), then *resume coverage exactly where it stopped* (coverage memory; ties to [clean-and-map](../clean-and-map) + [nav-localize](../nav-localize) resume)
  - guarantee the full job still reaches full coverage across one or more interruptions
- *job interface*
  - an action/service API to *start / pause / resume / cancel* a job and report *status*, suitable for Home Assistant
- test it well
  - multi-room worlds; verify whole-map, per-room, and spot jobs; verify no-go zones are respected
  - force a recharge / auto-empty / mop-wash mid-job and verify the job resumes to *full coverage*
- regression tests (headless, CI-friendly)
  - per-room / spot / whole-map jobs clean exactly the intended area
  - no-go zones are never entered
  - *coverage completeness is preserved across forced interruptions*
- submit a PR (pull request) to `contributions/cleaning-jobs/<your-github-username>/`
  - link to ROS2 package(s)
  - instructions, documentation - how to install, run, configure, troubleshoot, test results
  - videos of segmented/spot cleaning and a job interrupted by a dock service then resumed
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- *Modes* work: whole-map, per-room, and spot cleaning each clean exactly the intended area
- *Virtual walls / no-go zones* are defined, persisted, and never entered
- The map is *segmented into rooms* that can be targeted individually
- A long job *splits into pieces* — suspends for recharge / auto-empty / mop-wash and *resumes to full coverage*
- A *start / pause / resume / cancel / status* interface exists and is Home-Assistant-friendly
- *Regression tests* pass, including coverage-preserved-across-interruptions, runnable headless in CI
- Documented and reliably reproducible by someone else
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
