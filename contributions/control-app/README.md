# Control App & UX (design-first)

The app and UI a person actually touches to run their OOMWOO: start a clean, see
the map, set no-go zones, check on the robot, schedule. OOMWOO is *local-first and
cloud-free by design*, so the control app is too — it's a *client of the OOMWOO
ROS2 stack and Home Assistant*, not a phone-home service.

This module is *design-led*: it welcomes *designers* as much as coders. It runs in
two tracks — a *design track* that can start now, and a *build track* that follows
once the MVP scope and the robot's core behaviours settle.

> *Status — ready to start work (design track).* The robot's core (cleaning,
> navigation) is still being built, so the useful work *now* is *direction*:
> prioritise the feature set and concept the near-term control surface. Hold
> polished prototypes and the app build for far-future features until the scope and
> the robot behaviours land. Say hi in the
> [discussions](https://github.com/makerspet/oomwoo/discussions) so we can coordinate.

> *Grounding rule.* The app can only do what the robot exposes. Anchor every screen
> to a real capability in [SOFTWARE_INTERFACES.md](../../docs/SOFTWARE_INTERFACES.md)
> (and Home Assistant) and to a real user need — not to a feature that doesn't exist yet.

# Important References

- *[Valetudo](https://github.com/Hypfer/Valetudo)* — the closest existing example of
  what OOMWOO wants: a *local, cloud-free web UI* for (rooted) robot vacuums. Study
  its information architecture and interaction patterns (live map, zones, segments,
  go-to, settings) — the reference for a *privacy-respecting* control UX.
- *Consumer vacuum apps — learn from them without owning a robot.* The Roborock,
  Dreame, Ecovacs, and iRobot apps are worth studying for what works (map editing,
  room segmentation, zones / no-go, scheduling, multi-map) *and* what to avoid (ads,
  upsells, cloud lock-in, dark patterns). *You don't need to own a vacuum* — YouTube
  has plenty of *app/UI walkthroughs and reviews* demonstrating these flows (search
  e.g. "Roborock app tutorial", "Dreamehome app", "Ecovacs Home app"). Using one is
  better for real intuition, but watching is enough to learn the patterns.
- *Real user research (free)* — the OOMWOO Hacker News and Facebook threads have
  *hundreds of real users* saying what they love and hate (privacy / no-cloud,
  auto-empty, pet hair, edge cleaning, "brain-transplant my dead vacuum"). Mine these
  for genuine pain points instead of guessing.
- *Community feature-ideation board* — alfatreze's starting board:
  [Feature Ideation (Notion)](https://app.notion.com/p/Feature-Ideation-d5cd9e5c8eb840768ad98e989bbf7b70).
  A wide-net idea dump to prioritise from (a working board — decisions land in the
  project, see below).
- *[SOFTWARE_INTERFACES.md](../../docs/SOFTWARE_INTERFACES.md)* — the ROS2 topics /
  actions / state the app is a client of.
- *Home Assistant* — OOMWOO targets native HA integration; treat an HA dashboard as a
  first-class control surface, not an afterthought.
- [Project discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) · [Discord](https://discord.gg/3y2JKz5T25)

# Request for Contribution — Instructions

*Design track (start here):*

- *Prioritise the feature set* — turn the community idea dump into a clear
  *MVP / v1 / later* structure (Must / Should / Could is plenty of rigour for now),
  grounded in what the robot exposes ([SOFTWARE_INTERFACES.md](../../docs/SOFTWARE_INTERFACES.md))
  and real user pain (the HN / Facebook threads).
- *Concept the MVP control surface* — the near-term screens that map to behaviours
  we're actually building: *start / stop / pause a clean, live map, robot status
  (battery, docked, stuck / needs-attention), teleop, no-go zones / virtual walls,
  basic scheduling*. Local-first; no mandatory cloud.
- *Design system / visual language* — a small, reusable, accessible design system
  (aligned with the OOMWOO brand) so the app and future screens stay consistent.
- *Aggregate community input in the open* — working boards (Notion / Figma / FigJam /
  Penpot) are welcome for ideation, but land the *prioritised set and decisions* in a
  *GitHub Discussion* (or here in this module) so the whole community can weigh in and
  it's part of the project record, not one account.
- post progress in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)

*Build track (later):*

- Implement the app once the MVP scope + robot behaviours settle — e.g. a *local web
  UI* (à la Valetudo), a *Home Assistant dashboard*, and/or a mobile client. Build
  against [SOFTWARE_INTERFACES.md](../../docs/SOFTWARE_INTERFACES.md); contribute in
  your own repo and link it (per [CONTRIBUTING](../../docs/CONTRIBUTING.md)).

- iterate with review
- TBD, expect the RFC to evolve

## Acceptance criteria

*Design milestone:*
- A *prioritised feature set* (MVP / v1 / later), grounded in SOFTWARE_INTERFACES +
  real user pain, and *reviewed by the community* (not siloed in one board).
- *MVP control-surface concepts* (user flows + wireframes) for the near-term
  behaviours, each mapping to a real ROS2 capability.
- *Local-first* — no mandatory cloud, consistent with OOMWOO's privacy DNA.
- A starter *design system / visual language*.
- Decisions recorded *in the project*.

*Build milestone (later):*
- A working app implementing the MVP control surface against the ROS2 stack /
  Home Assistant; documented and reproducible.

- TBD, expect criteria to evolve.

The maintainer selects among compliant candidates using these criteria. Multiple
attempts are welcome and useful even if not selected — modules are swappable, and a
non-selected design is still a valid learning exercise and a fallback.
