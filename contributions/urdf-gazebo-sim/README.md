# URDF with Gazebo Simulation (ROS2 package)

The OOMWOO robot description (URDF) + a Gazebo simulation with a front bumper, so the
software modules (mapping, navigation, cleaning) can be developed *without hardware*.

> *Design basis:* OOMWOO is a *round* LiDAR vacuum with the LiDAR turret *centered* on
> top. The old teardown reference vacuum is no longer used. Rather than model from scratch,
> *fork the tested Proscenic M6 Pro sim package* and adapt it — the fastest path to a working
> OOMWOO sim. Exact geometry (from the sourced parts + the 3D design) is refined later;
> nav/SLAM doesn't need exact geometry.

# Important References
- [Simulate the Proscenic M6 Pro in Gazebo with ROS2](https://makerspet.com/blog/simulate-the-proscenic-m6-pro-robot-vacuum-in-gazebo-with-ros-2/) — the tested sim this forks from, and the template for the new OOMWOO write-up.
- [makerspet/oomwoo_urdf](https://github.com/makerspet/oomwoo_urdf) — OOMWOO URDF package + config.
- [ROS2 software interfaces](../../docs/SOFTWARE_INTERFACES.md) — shared topic/action/service contract this simulation should provide.
- [makerspet/oomwoo-install](https://github.com/makerspet/oomwoo-install) — builds the OOMWOO ROS2 Docker image(s).
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) · [Discord](https://discord.gg/3y2JKz5T25)

# Request for Contribution - Instructions

- *Fork the tested Proscenic sim into an OOMWOO package*
  - clone the tested *Proscenic M6 Pro* Gazebo sim package (`proscenic-m6pro` / [oomwoo_urdf](https://github.com/makerspet/oomwoo_urdf)) and rename it to *`oomwoo-one`* (the first OOMWOO model)
  - it's already tested with Gazebo + Nav2/SLAM — reuse it to minimize work
  - post in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) that you're working on it, and post progress
- *Adapt the URDF for OOMWOO*
  - *center the LiDAR* turret on top (the Proscenic's is offset)
  - round body, differential drive + caster; use approximate target dimensions (refine later from the 3D design)
  - keep/adjust the conventional *front semicircular bumper* with *left + right switches* — a Gazebo contact sensor publishes left/right contact events to ROS2
- *Integrate into the dev environment*
  - add the `oomwoo-one` package to the [oomwoo-install](https://github.com/makerspet/oomwoo-install) Docker image(s)
  - verify Nav2 SLAM runs (doesn't get stuck) in the Living Room world, the map saves, and Nav2 navigation on a saved map works
- *Document it (WordPress / Gutenberg post)* — an "OOMWOO software dev-environment setup & use" guide, modeled on the [Proscenic-in-Gazebo post](https://makerspet.com/blog/simulate-the-proscenic-m6-pro-robot-vacuum-in-gazebo-with-ros-2/) but for `oomwoo-one`, covering:
  - install + *Docker* setup on *Ubuntu and Windows*
  - *XLaunch* on Windows (choose *display 0*, not -1, at launch)
  - running from *Windows PowerShell*
  - launching the sim, mapping, saving a map, navigating
- *Submit* a PR to `contributions/urdf-gazebo-sim/<your-github-username>/`
  - link to the `oomwoo-one` package + the docs/blog draft
  - photos/videos of the sim running
  - announce your submission in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

Objective, measurable. Examples:
- `oomwoo-one` URDF is a *round* vacuum with a *centered LiDAR* + a front bumper (left/right switches)
- Gazebo simulation works
  - Nav2 SLAM works reliably in the Living Room world (no getting stuck)
  - map saves successfully; Nav2 navigation works on a saved map
  - bumper contact events are published to ROS2 and distinguish left vs right
- the `oomwoo-one` package *builds in the oomwoo-install Docker image*
- a *setup guide / blog post* is written (Ubuntu + Windows / XLaunch / PowerShell)
- documented and reliably reproducible by someone else
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and
a non-selected design is still a valid learning exercise and a fallback.
