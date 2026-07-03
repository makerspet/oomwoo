# Procure Part Specs & Datasheets for Sourced Components

We've already sourced candidate parts (see [BOM.md](../../BOM.md)). To design the I/O
board and firmware, **drive the motors and fans**, and build accurate mounts, we need each
part's detailed **electrical + mechanical specs** — pinouts, voltages, currents, encoder
PPR, torque, waveforms, etc. Vendors rarely publish these for vacuum sub-assemblies, so
contributors will **find datasheets, ask vendors, or safely reverse-engineer** them.

This is the *electrical/mechanical data* companion to
[source-3d-models](../source-3d-models) (which covers the *geometry*). No robotics
background needed — a multimeter, patience, and (for reverse-engineering) an oscilloscope go far.

Please check [BOM.md](../../BOM.md) and the [sourcing follow-along blog post](https://makerspet.com/blog/how-to-source-bom-for-oomwoo-open-source-vacuum-robot/)
for datasheets/specs already found.

## What we need, per part

### Drive wheel assembly (Roborock-family — see BOM)
- motor model; motor/assembly **datasheet** (if any)
- **encoder type + PPR** (pulses per revolution)
- **gearbox ratio**; **wheel diameter**
- rated + max motor **voltage**, **current** (no-load & stall), **torque**
- max / rated wheel **speed**
- **cable length(s)**; **connector models** (both ends); **full connector + motor pinouts**
- **wheel-drop sensor** model + pinout (these modules include one)
- signal **waveforms** (encoder channels, motor drive)
- assembly **weight**

### Suction fan / blower (several options sourced — see BOM)
- fan/motor model; **datasheet**
- rated **voltage, current, RPM**; **airflow** + **static pressure (Pa)**
- **how to drive it** — BLDC driver + control interface (PWM / tach / hall / 3-phase),
  soft-start / protection behaviour
- **connector model(s) + pinout**; cable length
- signal **waveforms**
- **weight**

### Caster / universal wheel assembly (Roomba-family — see BOM)
- model, dimensions, mounting, any embedded sensor, weight, datasheet

## Already found ✅ vs still missing ❔

**Found**
- **Fan datasheet (some options):** https://file.elecfans.com/web1/M00/CC/89/o4YBAF-ZOBKAQBvyADDMAglsvTw020.pdf
- **Nidec BLDC motors** (candidate fan motors — *bare motors, not the full suction assemblies*):
  [NCJ-20N Type-3](https://www.nidec.com/en/product/search/category/B101/M102/S100/NCJ-20N-Type-3/),
  [NCJ-20N Type-4](https://www.nidec.com/en/product/search/category/B101/M102/S100/NCJ-20N-Type-4/)
- **Driving the fans:** [ripinteer/fan_protector](https://github.com/ripinteer/fan_protector)
  — reference for driving / protecting the BLDC blower (from earlier project research)

**Still missing (help wanted)**
- Connector **pinouts** + cable lengths for wheels, fans, caster
- **Encoder type + PPR**, gearbox ratios, torque/current under load
- **Wheel-drop sensor** model + pinout
- Signal **waveforms** (encoder, motor/fan drive)
- Suction-**assembly**-level datasheets (we have some bare motors, not the assemblies)
- Weights; caster specs

## Reverse-engineering — only if specs can't be found, and SAFELY

If a spec isn't published, reverse-engineer it by opening an existing vacuum and probing.
**Safety first:**
- Don't do it unless you're qualified, experienced.
- Opening a vacuum usually **voids the warranty** and **can damage it** — accept that risk knowingly.
- **Secure / prop up the vacuum** so it can't scoot off the table or bench when the wheels or
  fan spin during testing (clamp it, or raise the wheels off the surface).
- Respect the **Li-ion battery** — don't short, pierce, or stress the pack; disconnect where sensible.
- Mind **pinch points and spinning parts** — keep fingers/hair clear of the impeller and brushes.
- Any **mains-connected** testing (e.g. a dock) — extra caution; isolate.
- Use a **multimeter + oscilloscope** to capture voltages, currents, and waveforms; trace and
  **label connector pinouts**; photograph everything.

**Legal:**
- By performing any work for this project including reverse engineering you agree to
  - wave liability, indemnify this project, the legal entity behind it (Remake AI Statutory Trust) and and its founder
  - contribute your work and results thereof, if any, as open-source, to be published under Apache 2.0 license

## Submit

A PR to `contributions/part-specs/<your-github-username>/<part>/`:
- a spec sheet (markdown table) with everything you found
- any datasheets (PDF) and source links
- photos of connectors + labelled pinouts
- waveform captures where reverse-engineered
- provenance — which vendor / model / revision the data is from
- announce it in [Project Discussions](https://github.com/makerspet/oomwoo/discussions?discussions_q=)

## Acceptance criteria

- Spec sheet for a part (or a clearly-scoped subset)
- Datasheets / links where found
  - pinouts + waveforms where reverse-engineered when appropriate
- Provenance stated (part / vendor / revision)
- Verifiable by someone else with the same part
- TBD, expect criteria to evolve

The maintainer selects among compliant candidates using these criteria. Multiple attempts
are welcome and useful even if not selected — a non-selected spec sheet is still a valid
reference and a fallback.
