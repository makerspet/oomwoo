# Source 3D Models (STEP) for Off-the-Shelf BOM Parts (procurement)

To design printed mounts and the chassis that **fit real sourced parts**, we need accurate
3D models (**STEP**) of the off-the-shelf components in the [BOM](../../BOM.md) — the
drive-wheel assembly, the suction fan/blower (several candidate models), the caster wheel,
the side-brush motor, and more. Manufacturers rarely publish these, so the community needs
to **obtain, measure, and model** them. Every printed mount and the chassis references this
geometry — see [ARCHITECTURE.md](../../docs/ARCHITECTURE.md) §5.2 (mechanical interface
standard). Missing models block or force guesswork on the mechanical modules.

This is a great **first contribution** for anyone with CAD skills and calipers — no
robotics or programming needed, and the modules can be modeled **in parallel**.

## Priority parts (from the [BOM](../../BOM.md))

Start with the "ready now" mechanical parts:
- **Drive wheel assembly pair** (e.g. Roborock S5/S50/S55/S6/S7-family modules)
- **Caster / universal wheel** (e.g. Roomba i/j/e/500–900 caster)
- **Suction fan / blower** — model the option(s) we shortlist (e.g. Dreame L10s / Nidec /
  Roborock S8-family blowers listed in the BOM)
- **Side-brush motor**, **main-brush assembly**, **water pump**, **battery pack**, etc.

See [BOM.md](../../BOM.md) for the full list, the exact candidate models, and AliExpress
search links, plus [docs/ali_express_research.md](../../docs/ali_express_research.md) for
sourcing notes.

# Request for Contribution - Instructions

- **Pick a part** from the [BOM](../../BOM.md) and **claim it** in
  [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) or
  [Discord](https://discord.gg/3y2JKz5T25) so two people don't model the same thing. Post progress too.
- **Get an accurate model** — two paths:
  1. **Find an existing STEP** (manufacturer site, GrabCAD, etc.) and **verify it against the
     real part** (dimensions match). Fastest — but confirm it's the same model/revision.
  2. **Model it yourself**: order the exact part (AliExpress links are in the BOM), measure
     with calipers, optionally use a 3D scanner and build an accurate STEP.
- **Capture the interface-relevant geometry** (external only — internal detail is not needed):
  - Overall **bounding envelope** (so it fits the chassis space / height budget)
  - **Mounting features**: holes, bosses, clips, bolt pattern — and their exact positions
  - **Functional interfaces**: axle/shaft position + axis, wheel contact plane, fan air
    inlet/outlet, connector / wire-exit locations
  - **Mating faces** where other modules attach
  - Note the **key overall dimensions**
- **Record provenance** — the exact vendor + link + which model/revision you measured. Parts
  vary between sellers and revisions; say which one this model represents.
- **Submit a PR** to `contributions/source-3d-models/<your-github-username>/<part-name>/`:
  - the **STEP** file (primary deliverable) + native CAD source (Fusion/SolidWorks/etc.) if you modeled it
  - a **photo** of the real part (ideally next to your model / with calipers)
  - the **source link** (AliExpress/vendor) and **key dimensions**
  - notes on tolerances and how you measured
  - announce it in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)
- Iterate with review.
- TBD, expect the RFC to evolve.

(*) If you have a strong reason to model a different variant than the BOM lists, post your
rationale in [discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=) first.

## Acceptance criteria

Objective, measurable. Examples:
- Accurate **STEP** of the specified part — bounding envelope, mounting features, and
  functional interfaces match the measured real part (within a stated tolerance)
- Includes the **exact source link**, **key dimensions**, and a **photo** of the real part
  - Please make sure the model is licensed as open-source
- **Verifiable/reproducible** by someone else who buys the same part
- STEP provided (+ native CAD source if self-modeled)
- Documented well enough that a mount designer can build against it with confidence
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple attempts
are welcome and useful even if not selected — models are swappable, and a non-selected
model is still a valid reference and a fallback.
