# OOMWOO Design Document

> *Working design doc.* This accumulates research-backed design decisions before
> they're split into per-module [RFCs](../contributions) and the [RFC backlog](RFC_BACKLOG.md), and/or migrated into
> the [README](../README.md). A condensed version of §1 already lives in the
> README's [Design research](../README.md#design-research) section. Expect this to
> grow as remaining components are researched.

---

## 1. Design research — what makes vacuum users happy

We reviewed the 2025–2026 consumer robot vacuum landscape (global + China-sourceable
brands, budget → flagship) across RTINGS, VacuumWars, Reddit r/robotvacuums, and
reviewer blogs, then adversarially fact-checked the key claims. The point: copy the
solutions that correlate with happy users, skip the ones that need commercial scale.

### Suction — a sourcing problem, not an engineering one
Real-world cleaning does *not* track advertised suction (Pa). ~$500 mid-tier
models beat flagships in pickup tests. A moderate *sealed* sourced motor + a good
brush + a *tight airflow seal* matches flagship cleaning — *no custom-molded
impeller needed.* Airflow sealing (bin/fan/brush seams) matters more than raw Pa.
[(source)](https://www.thesmarthomehookup.com/the-best-300-600-robot-vacuums-they-beat-the-flagships/)

### Navigation & "never gets stuck" — the #1 user pain, hardest to replicate
Best obstacle avoidance comes from *sensor fusion* (LiDAR + a floor-level 3D-ToF
or RGB camera + AI object recognition), not any single sensor. LiDAR is structurally
*blind below its ~10 cm turret*, which is exactly why robots eat cables and socks.
The Eufy Omni S2 ($1,599) was the only model in one test to pass all 24 obstacles —
and it has the full vision stack. *Never-stuck is commercial-scale.*
- *For OOMWOO:* v1 leans on the *bumper* for low/LiDAR-invisible obstacles (this
  is already how the [clean-and-map RFC](../contributions/clean-and-map) handles it).
  Camera + AI vision avoidance is a *later / experimental* goal, not an MVP promise.
  Don't position OOMWOO as out-navigating commercial flagships; position it as an
  open platform to *experiment* with navigation and vision.
[(source)](https://vacuumwars.com/best-robot-vacuums-with-obstacle-avoidance/)

### Brush — anti-tangle is what users notice
Rubber beats bristle, and a *tapered, one-side-mounted roller* resists hair-wrap
best (hair tangling is a top complaint). Easy to 3D-print or source compatible.

### Mop — dual-spinning is the replicable sweet spot
Performance ladder: flat drag pad (worst) → *dual spinning pads* (mid) →
self-washing roller (best). But the roller mop's "better stains / less residual
water" edge was *refuted* under fact-checking — it's overstated. A 3D-printed
*dual-spinning* mop is competitive and DIY-able; *skip the self-washing roller*
(and its multifunction wash/dry dock) for now.
[(source)](https://vacuumwars.com/robot-vacuum-mop-systems/)

### Dock — basic is DIY-able, full-service is not
A *basic charging dock* is well within reach (print the housing; source contacts +
adapter + IR beacon). *Auto-empty / mop-wash / hot-dry all-in-one docks* are
commercial-scale — defer, or use an off-the-shelf corded vac for emptying.

### Cloud-free / local control — the real differentiator
[Valetudo](https://github.com/Hypfer/Valetudo) gives cloud-free MQTT/REST local
control across ~10 brands. *Dreame* is the most rootable (≈16 models) and the
safest donor to study. Cloud-free local operation is OOMWOO's positioning advantage.

### Well-loved models worth studying
Eufy Omni S2 (obstacle avoidance), Narwal Flow (roller mop), Ecovacs Deebot T90 Pro
Omni (~$499 all-rounder), Dreame X40 Ultra (dual-spinning mop; Dreame = best donor).

> *Caveats:* the top-level dimensions (suction-decoupling, sensor-fusion, mop
> ladder) are primary-source and verified. Per-model rankings are *directional*,
> from single-run reviewer tests. Rootability is *per hardware revision* —
> re-verify any specific donor unit before buying to root.

---

## 2. Print vs source strategy

*Rule of thumb: print geometry, source mechanisms and wear items.* Anything with a
gearbox, encoder, rubber compound, spring, pump, or bearing is precision you can buy
for a few dollars; anything custom-shaped that mates with the OOMWOO chassis, print.

| Component | Source or 3D print | Why / how |
|---|---|---|
| *Driving wheel assemblies* | *Source (whole module)* | Complete drive modules (gearmotor + encoder + suspension + rubber tire). 3D print at most an adapter bracket. Why? Requires advanced skill - possibly SLA for gearbox, FDM TPU tire. The #1 "don't print it" part. |
| *Universal / caster wheel* | *Print* or source wheel/ball caster. | Likely a simple passive swivel, possibly TPU. |
| *Side brush assembly* | *Hybrid* | Source brush + small gearmotor; print the mount. Fit a *common replaceable brush*. Fixed (not extendable) for v1. |
| *Main brush* | *Source / hybrid* | Tapered rubber anti-tangle roller in a *common wear-part size*; source compatible, or print core + rubber. |
| *Bumper* | *Hybrid* | Print floating shroud; source lever microswitches + return springs. |
| *Dust bin / water tank* | *Print body + source guts* | Print custom body (mates airflow); source filter (common HEPA size), gasket (or TPU print), latch spring. Water tank adds a sourced *pump + solenoid valve + tubing*. |
| *Mop lift* | *Hybrid (P2)* | Print cam/linkage; source a small *servo or geared motor*. |
| Mop disposable cloths | *Source* | Source (easier) or DIY sew. |
| Mop dryer | *Source* | Source the mop dryer. |
| *Enclosure / top shell* | *Print* | Custom cosmetic/structural; no off-the-shelf equivalent. Design for splitting to fit common print beds. |
| *Dock (basic charge)* | *Print housing + source contacts* | Source *pogo pins / spring contacts / magnets* (magnets can carry [10 A](https://xdaforums.com/t/home-made-pogo-pin-charging-dock.2019847/)) + wall adapter + IR-beacon LEDs. Plenty of [DIY precedent](https://www.instructables.com/Roamer-the-Self-Charging-Companion-Robot/). |
| *Auto-empty dock* | *3D print enclosure + source bin/fan* | Needs its own fan + bin (commercial-scale). Off-the-shelf corded vac bolted to a printed dock is the DIY path. |
| *Mop dock* | *3D print enclosure + source water tanks/hookups* | Needs its own fan + bin (commercial-scale). Off-the-shelf corded vac bolted to a printed dock is the DIY path. |
| Battery, LiDAR, motors, PCB, fasteners, bearings, gaskets | *Source* | Standard sourced parts (custom PCB + LiDAR aside). |
| Single Board Computer | *Source* | Raspberry Pi 5 4GB or better for first model. |
| Input/Output board | *Custom* | No DIY-vacuum I/O PCBs I'm aware of. I'll design a custom PCB for sensors and motor drivers. |
| Cameras, sensors, LiDAR | *Source* | Color + distance cameras for top-tier obstacle avoidance. IR cliff, side proximity sensors. Ultrasonic carpet sensor. |

*Sourcing strategy:* deliberately spec sourced wear parts (brushes, filters, wheel
modules) in *common, abundant sizes* so users buy cheap "universal" / Roomba-style
replacements anywhere. A selling feature *and* less inventory to stock.

---

## 3. Feature decisions

### 3.1 Extendable side brush — *fixed for v1*
The extendable arm (e.g. Roborock FlexiArm) is a *genuinely loved* feature — best
corner-cleaning scores and strong reviews
[(source)](https://vacuumwars.com/vacuum-wars-best-robot-vacuums/). But it's a
mechanically complex actuated mechanism. A well-placed *fixed* side brush captures
most of the corner benefit at a fraction of the complexity. Extendable is a great
*P2+ community mod*, not an MVP requirement.

### 3.2 Body shape — *round*
D-shape cleans corners/edges better, but the real-world advantage is "smaller than
most people expect," and a well-engineered round robot with good side brushes
performs as well or better in most homes
[(source)](https://www.ecovacs.com/us/blog/round-vs-square-robot-vacuum). Round wins
for a DIY/printable platform:
1. Simpler to design, print, and seal.
2. Navigates better — rotates in place, backs out the way it came (D-shape
   complicates every nav/recovery RFC).
3. Natural fit for the spinning 2D LiDAR turret.
4. Matches the round teardown reference we're porting.
5. Corners are better solved by the side brush (later extendable) than by body shape.

*Decision: round body + fixed side brush now, extendable side brush later.*

---

## 4. Compute (SBC)

*v1: Raspberry Pi 5 (4 GB).* Chosen to onboard the large Raspberry Pi community —
the biggest contributor wedge. Runs ROS2 + LiDAR SLAM + Nav2 comfortably. No on-board NPU.

- *ML vision option — Hailo AI HAT.* Add the RPi M.2 AI Kit (Hailo-8L, ~13 TOPS) for
  real-time camera obstacle detection: keeps the entire RPi ecosystem advantage *and*
  gains an NPU. *Check the board-stack height* — a vacuum is only ~10 cm tall and
  the M.2 HAT adds Z. Evaluate alternatives (Coral USB/M.2 accelerator, or lighter
  CPU-only models) against the height budget.
- *Later: Rockchip RK3588 / RK3576.* Orange Pi 5, Radxa Rock 5B, Banana Pi CM5 —
  built-in *6 TOPS NPU*, RKNN toolkit, YOLO ~65 ms/image. Cheaper and integrated, but
  driver / ROS2 / kernel maturity *lags RPi*, so it's a *later* move, not the
  community-onboarding one.

---

## 5. I/O board (custom, JLCPCB)

No off-the-shelf DIY-vacuum I/O board exists, so we design one. It carries an *MCU
running real-time firmware with a custom safety-focused serial protocol* to the SBC: the SBC
does ROS2 / SLAM / nav / vision; the board does real-time motor + sensor I/O.

*MCU:* CH32V307VCT6 (LQFP100) plus a CH32L103C8T6 companion — replacing the
STM32G473VCT6 in Nov 2026 for cost and stock. Its 144 MHz RISC-V core, timers, and ADCs
serve closed-loop motor control and the board's many current/sensor channels.
Offload the *BLDC fan to its external controller* (one PWM command plus FG feedback,
instead of in-MCU FOC) to save pins and complexity.

*LiDAR (3irobotix CRL-200S):* wires to the I/O board. The board *drives the LiDAR
motor* (MOSFET + closed-loop speed control using the LiDAR's RPM feedback) and *passes
raw LiDAR data through the MCU to the SBC* over the fast serial link. *Confirm the MCU
UART bandwidth handles the CRL-200S data rate.*

Cross-checked peripheral list (your running list + `[+]` = additions to consider):

*Sensors*
- 2D LiDAR (CRL-200S) — motor-driven + data passthrough to SBC
- IR cliff / proximity / docking
- Bumper micro-switches (+ optional optical/IR bumper)
- Wheel encoders
- Carpet ultrasonic sensor
- Color camera → *connects to the SBC's CSI/USB, not this board*
- VL53L7CX distance sensor (I²C)
- Water tank level (full/empty)
- Dust bin present / lid open-closed
- Battery level / fuel gauge
- Dock-connected / charge sense
- IMU
- `[+]` Wheel-drop / lift sensor (robot picked up) — distinct from cliff

*Motor drivers*
- Main wheels ×2
- Main brush
- Side brush(es)
- `[+]` *Mop pad spin motor(s)* — for dual-spinning pads (you listed mop *lift* but not *spin*)
- Mop lift servo
- Water pump (low-side MOSFET)
- Vacuum fan (BLDC) — via *external ESC* (recommended)
- LiDAR motor (MOSFET, closed-loop)

*Power*
- Battery connector
- Charging circuit (charge-controller IC)
- Dock contacts
- BMS interface
- Current sense (per-rail and/or per-motor for stall / tangle detection)
- DC-DC converters (5 V for SBC, 3.3 V logic, motor rails)
- Power on/off button + soft-latch power circuit
- `[+]` Protection: reverse-polarity, over-current fuse / eFuse, inrush limiting

*Audio / UI*
- Speaker amp + connector (audio in from the SBC)
- Mic placeholder
- Power / status LEDs
- Buttons (power, dock, clean)
- `[+]` Buzzer (cheap fallback if the speaker amp is deferred)

*Host link:* USB or high-speed UART between MCU and SBC, carrying the custom
framed commands and telemetry. LiDAR serial ownership/passthrough and its bandwidth
budget remain open integration decisions.

> *Scope note:* the *wash/dry dock has its own controller* (ESP32 + WiFi) for its
> pumps / heater / fan / water-level. Those are *not* on the robot I/O board.

---

## 6. Electrical / sensor BoM sketch

Rough *robot* BoM at prototype / low-qty China-sourcing prices (compresses at volume).
Excludes the dock.

| Item | Qty | ~USD | Notes |
|---|---|---|---|
| Drive wheel modules | 2 | 12–27 | sourced complete module |
| Caster wheel | 1 | 0–3 | print or ball caster |
| Suction blower (BLDC) | 1 | 8–20 | sealed sourced motor |
| Main brush + motor | 1 | 5–12 | tapered rubber roller |
| Side brush + motor | 1–2 | 3–8 | |
| Mop spin motor(s) + pads | 1–2 | 6–15 | mopping models |
| Water pump + valve + tubing | 1 | 4–10 | mopping models |
| Mop lift servo | 1 | 2–6 | mopping models |
| Battery pack (~14.8 V Li-ion) + BMS | 1 | 15–30 | safety review |
| LiDAR (CRL-200S / LDS) | 1 | 30–40 | your cost |
| VL53L7CX ToF | 1 | 8–15 | obstacle detection |
| Color camera | 1 | 5–15 | to SBC |
| IMU | 1 | 2–5 | |
| IR cliff / proximity | 3–4 | 3–8 | |
| Bumper micro-switches | 2–3 | 1–3 | |
| Ultrasonic carpet sensor | 1 | 2–5 | |
| Speaker + amp, mic, LEDs, buttons | — | 3–8 | |
| Custom I/O PCB (JLCPCB assembled, low qty) | 1 | 15–40 | |
| Wiring, connectors, fasteners, magnets, gaskets, filter | — | 12–25 | |
| Printed parts (filament) | — | 5–15 | |
| *Robot subtotal (sourced parts)* | | *~$130–270* | excludes SBC |
| Raspberry Pi 5 4 GB | 1 | ~60 | |
| Hailo AI HAT (optional, premium vision) | 1 | ~70 | |

---

## 7. Water system

*Robot:* an onboard *clean-water tank* (printed) → *solenoid diaphragm pump* (what
commercial units use) → mop head. For spinning pads, dirty water stays in the pads until
the dock washes them.

*Dock tiers (where the water complexity lives):*
- *Auto-empty:* dock fan + bin/bag suck the robot's dustbin out through a sealed port.
  The off-the-shelf-corded-vac approach works here.
- *Wash + dry:* *clean tank + dirty tank* (printed) + *two pumps* + a wash
  tray/roller + a *hot-air blower (heater + fan)*. Wash *must* include hot-air dry —
  wash-without-dry breeds mildew/odor. Needs its *own ESP32 + WiFi controller*.
- *Plumbing hookup:* offer as an *option* on the premium dock (pump + supply/drain
  lines + valve); default to tank-based (direct plumbing needs pro install). Skip exotic
  water-recycling (e.g. silver-ion distillation).
- DIY parts are cheap/common: 12 V diaphragm or peristaltic pumps, solenoid valves,
  silicone tubing, float / capacitive level sensors.

---

## 8. Budget target

*Target: ~$100–200 sourced parts + Raspberry Pi 5 4 GB*, aiming at the capability of a
mid-range ($500–600) commercial vacuum.

- *Verdict: realistic for the mechanicals + core sensors* at the low–mid end, and it
  compresses at volume. But *mopping + premium obstacle detection* (ToF + color camera
  + an NPU accelerator) are exactly the line items that push toward / past $200 — the
  Hailo HAT alone is ~$70. So $100–200 holds for a capable vacuum; "premium vision now"
  wants a +$70-ish allowance (or defer the NPU to the Rockchip generation).
- *Sanity check vs commercial:* a $500–600 LiDAR vacuum has roughly a *$120–180 FOB
  BoM at 5,000 MOQ*. Our low-qty numbers are coherent — we trade *no tooling/molds*
  (3D print) for *higher per-part cost* (no volume).
- *Set builder expectations honestly:* total DIY spend (kit + RPi 5 + LiDAR + margin)
  lands *above* a commercial unit's BoM. The value proposition is *openness, local
  control, and hackability — not beating Roborock on price.*

---

## 9. Product lineup — shared base, three dock tiers

One robot base, three dock tiers, released in order:
1. *Basic charging dock* (first release — simplest, MVP-aligned).
2. *Auto-empty dock* (dust).
3. *Auto-empty + mop-wash + hot-dry dock* (the full-service tier).

Notes:
- Mirrors how commercial brands segment (same robot, dock tiers) and fits the
  swappable-module philosophy.
- The *mop hardware (spinning pads + onboard water tank) is an add-on module* on the
  shared base — only the mopping models carry it; the base is otherwise constant.
- The *wash+dry dock is almost its own mini-product* (pumps, heater, tanks, ESP32).
  Correctly the last and hardest deliverable after the robot itself.
- Skip a wash-*only* dock — drying is mandatory (odor).

---

## 10. Obstacle detection strategy (premium hardware + community ML)

Targets the #1 user pain (getting stuck / eating cables). Strategy: *premium hardware
now, ML maturity via community contribution over time.*

- *Sensors:* *VL53L7CX* multizone ToF (8×8, *90° FoV*, ~350 cm — wider FoV than the
  L5CX's 63°, better coverage) *+ color camera.* The ToF alone detects the low / small /
  cliff objects the *LiDAR is blind to*, so v1 gets real "doesn't eat cables" value
  *before* any ML matures — de-risks the feature.
- *ML:* the *camera + model* is where the NPU matters (Hailo HAT now, Rockchip NPU
  later); real-time RGB detection won't run well on the RPi 5 CPU.
- *Community-labeled household-obstacle dataset* is a legitimately novel contribution
  track — every contributor's home is training data. Treat it as a first-class
  contribution track alongside the RFCs; it doubles as community-building.

---

## 11. Still to research / open decisions

- *Battery:* chemistry (Li-ion 3S/4S?), specific cells + BMS, charge profile — *safety review*.
- *BLDC fan ESC:* select an off-the-shelf ESC vs in-MCU drive.
- *Filter:* pick a common, abundant filter size as the interface standard.
- *Gasket sourcing* vs TPU printing for airflow seals.
- *Dock docking signal:* IR beacon protocol / fiducial / reflective marker.
- *Fastener / heat-set insert standard* (ties to ARCHITECTURE §5.2).
- *Confirm:* MCU pin budget, host-link bandwidth (including any LiDAR passthrough), Hailo stack height.
- Remaining mechanical parts not yet covered above.
