# Bill of Materials (BoM)

> ⚠️ **Work in progress / draft.** This is an evolving sketch, not a final BoM. The
> **first working BoM is targeted for ~mid-July**; a final, fully-costed BoM follows as
> the chassis, I/O board, and sensors settle and parts are sourced and validated.
> Prices are **prototype / low-quantity** China-sourcing estimates and compress at volume.
>
> Rationale and design decisions behind these choices live in
> [docs/design-document.md](docs/design-document.md). Interfaces live in
> [ARCHITECTURE.md](ARCHITECTURE.md).

## Budget target

**~$100–200 in sourced parts + a Raspberry Pi 5 (4 GB)**, aiming at the capability of a
mid-range ($500–600) commercial vacuum. Mopping and premium obstacle detection (ToF +
color camera + an NPU accelerator) push toward / past the top of that range; premium
vision is a clearly-priced **add-on**, not part of the base figure.

The honest framing: total DIY spend (kit + Pi 5 + LiDAR + margin) lands **above** a
commercial unit's BoM. The value is **openness, local control, and hackability — not
beating commercial vacuums on price.** (At MoQ volume, the goal is to close that gap.)

## Robot BoM (sketch)

Prototype / low-qty prices. Excludes the dock.

| Item | Qty | ~USD | Notes |
|---|---|---|---|
| Drive wheel modules | 2 | 12–27 | sourced complete module (motor + encoder + suspension + tire) |
| Caster wheel | 1 | 0–3 | print or ball caster |
| Suction blower (BLDC) | 1 | 8–20 | sealed sourced motor — sealing matters more than raw Pa |
| Main brush + motor | 1 | 5–12 | tapered rubber anti-tangle roller |
| Side brush + motor | 1–2 | 3–8 | fixed (extendable is later) |
| Mop spin motor(s) + pads | 1–2 | 6–15 | mopping models only |
| Water pump + valve + tubing | 1 | 4–10 | mopping models only |
| Mop lift servo | 1 | 2–6 | mopping models only |
| Battery pack (~14.8 V Li-ion) + BMS | 1 | 15–30 | **safety review** |
| LiDAR (3irobotix CRL-200S / LDS) | 1 | 30–40 | |
| VL53L7CX multizone ToF | 1 | 8–15 | obstacle detection (90° FoV) |
| Color camera | 1 | 5–15 | connects to the SBC |
| IMU | 1 | 2–5 | |
| IR cliff / proximity sensors | 3–4 | 3–8 | |
| Bumper micro-switches | 2–3 | 1–3 | |
| Ultrasonic carpet sensor | 1 | 2–5 | |
| Speaker + amp, mic, LEDs, buttons | — | 3–8 | |
| Custom I/O PCB (JLCPCB assembled, low qty) | 1 | 15–40 | STM32 + motor drivers + sensor front-ends |
| Wiring, connectors, fasteners, magnets, gaskets, filter | — | 12–25 | |
| Printed parts (filament) | — | 5–15 | you print these yourself |
| **Robot subtotal (sourced parts)** | | **~$130–270** | excludes SBC |
| Raspberry Pi 5 (4 GB) | 1 | ~60 | the SBC |
| Hailo AI HAT (optional, premium vision) | 1 | ~70 | NPU for camera ML |

## Dock (by tier)

Three dock tiers share one robot base, released in order:

| Tier | Adds | Rough extra parts |
|---|---|---|
| **Basic charge** (first release) | charging only | printed housing + contacts/magnets + wall adapter + IR beacon |
| **Auto-empty** | dust auto-emptying | dock fan + bin/bag + sealed port |
| **Auto-empty + wash + dry** | mop wash + hot-air dry | clean + dirty tanks, 2 pumps, heater + fan, **own ESP32 + WiFi controller** |

## Sourcing strategy

- **Print geometry, source mechanisms and wear items.** See the print-vs-source table in
  [docs/design-document.md](docs/design-document.md#2-print-vs-source-strategy).
- Spec wear parts (brushes, filters, wheel modules) in **common, abundant sizes** so
  builders can buy cheap universal replacements anywhere.
- Per-module sourcing details will land in the relevant
  [contributions/](contributions) RFCs as they mature.
