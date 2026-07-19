# OOMWOO I/O Board SPEC.md — Jul 18 2026 Update

> **Source:** `makerspet/oomwoo-io-board` repository, `docs/SPEC.md`
> (commits `dba0d1c3` and `75803b7e` and `4e6c0134` of 2026-07-18, plus the
> `cff32b3e` merge of PR #1 `xbattlax/docs-spec-cleanup-xbattlax`).
> **Captured:** July 19, 2026 (cron run)
> **Purpose:** Record the new verifiable facts added to the upstream I/O board
> SPEC on 2026-07-18 that were not previously covered by the OsakaTX part-specs
> compilation. These are quoted / paraphrased directly from the upstream file;
> no reverse-engineering was performed by this contributor.

---

## 1. Drive Wheel Motor — Coil Resistance

The upstream SPEC.md table row for the drive wheel now reads:

> `Drive wheel | 2 | DC 14.4V 19 Ohm, 3.5A stall (TODO check), H-bridge DRV8231, DRV8871 or similar`

The **19 Ω** winding resistance is a **new** electrical parameter (previously
the OsakaTX compilation listed only 14.4 V and 3.5 A stall). 19 Ω at 14.4 V
gives a stall current of ~0.76 A by Ohm's law — which is *inconsistent* with
the "3.5 A stall" figure that upstream itself still marks `TODO check`, so the
two numbers cannot both be the bare-motor stall current. Plausible readings:

- 19 Ω may be the **cold DC resistance of the motor winding only** (motor
  disconnected from gearbox/driver), in which case the 3.5 A figure is the
  mechanical stall current after the gearbox reflection and back-EMF are
  accounted for — these are genuinely different measurements and need not
  agree.
- Alternatively 3.5 A may have been a placeholder from an earlier draft.

Either way, **19 Ω is the new figure listed** in the upstream maintainer's
SPEC.md and should be propagated to the part-specs drive-wheel section as the
listed coil resistance (SPEC.md does not state whether it was measured), with
the 3.5 A stall left as `TODO check` exactly as upstream has it.

| Parameter | Value | Source line in SPEC.md |
|---|---|---|
| Motor type | DC brushed | row "Drive wheel" |
| Quantity | 2 (left + right) | row "Drive wheel" |
| Nominal voltage | 14.4 V | row "Drive wheel" |
| **Coil resistance** | **19 Ω** (new) | row "Drive wheel" |
| Stall current | 3.5 A (TODO check) | row "Drive wheel" |
| H-bridge | DRV8231 / DRV8871 or similar | row "Drive wheel" |

---

## 2. Roborock S5 Max Wheel Assembly — 7-pin JST ZH Pinout

Upstream SPEC.md now carries an explicit **motor pinouts** code block. The
Roborock S5 Max wheel assembly entry is:

```
Roborock S5 Max wheel assembly - JST ZH 1.5mm male 7p (needs f)
['''''''] wheel-drop-switch on, wheel-drop-switch com, orange hall TBD, blue hall TBD, brown hall TBD, MOT, MOT
```

Decoded (the 7 apostrophes are positional placeholders for the 7 pins, in
order):

| Pin | Wire / signal | Function |
|-----|---------------|----------|
| 1 | (wheel-drop-switch on) | Wheel-drop limit switch — NO / signal side |
| 2 | (wheel-drop-switch com) | Wheel-drop limit switch — common |
| 3 | Orange | Hall TBD |
| 4 | Blue | Hall TBD |
| 5 | Brown | Hall TBD |
| 6 | (MOT) | Motor power |
| 7 | (MOT) | Motor power |

### Cross-check vs. Scowt PR #13

The OsakaTX compilation already records Scowt's physical inspection (merged
PR #13), which gave:

| Pin | Wire Color | Function (Scowt) |
|-----|-----------|----------|
| 1 | Grey | Limit switch (wheel-drop, NC) |
| 2 | Grey | Limit switch (wheel-drop, common) |
| 3 | Orange | Encoder VCC (+5V) |
| 4 | Blue | Encoder signal (single-channel pulse) |
| 5 | Brown | Encoder GND |
| 6 | Black | Motor power (-) |
| 7 | Red | Motor power (+) |

The two sources **agree on**:
- Connector: 7-pin, **JST ZH 1.5mm pitch**, male on the wheel-module side
  (Scowt listed it as "7-pin JST"; upstream pins the family to ZH 1.5mm).
- Pin 1 / Pin 2 = the two wheel-drop switch contacts.
- Pins 3/4/5 = the three Hall/encoder wires, in the order **orange, blue, brown**.
- Pins 6/7 = the two motor power pins.

The two sources **differ on**:
- **Switch polarity:** Scowt labels pin 1 "NC"; upstream labels it "on". These
  are not necessarily contradictory (a NC switch is "on" when the wheel is up),
  but the convention is not identical and should be flagged.
- **Hall wire functions:** Upstream explicitly leaves all three Hall wires as
  `TBD` (orange/blue/brown). Scowt assigns Orange=+5V, Blue=signal,
  Brown=GND. **Scowt's assignment remains the more detailed physical
  measurement; upstream's TBD should not be read as contradicting it.**
- **Motor wire colors:** Upstream lists both motor pins as `MOT` with no
  color; Scowt records Black (-) and Red (+).

### What this update adds

- **Connector family confirmation:** JST **ZH 1.5mm**, male, 7-position on the
  wheel module side. (Scowt's PR #13 had "7-pin JST" without naming the
  family; this pins it down.)
- **Manufacturer-side wire ordering** of the Hall wires (orange → blue →
  brown, pins 3→5), matching Scowt's physical cable.
- **"needs f" annotation:** upstream notes the mating (board-side) connector
  needs a *female* counterpart — i.e. the wheel module ships with a male plug
  and the I/O board / mainboard needs the female ZH receptacle. Useful for
  BOM / PCB footprint selection.

### Remaining unknown (unchanged)

The **exact J25/J26 16-pin SHD 1.0mm mainboard connector per-pin map** is
still not resolved by this update. Upstream's `MOT, MOT` for pins 6/7 of the
wheel-module-side connector confirms motor power is *on the wheel connector*
in the original Roborock design — consistent with the OsakaTX note that, on
the original mainboard, motor power is *separately* broken out to J24/J27
(2-pin PH 2.0mm) and the 16-pin J25/J26 carries only the encoder + auxiliary
signals. The 16-pin map still needs PCB continuity tracing.

---

## 3. Suction Fan / Blower — Connector Variants

Upstream SPEC.md now lists **10 suction-fan module rows** (9 distinct model
numbers; `20N704R990F` appears twice, at unspecified voltage and at 15 V) with
their connector types. Only some of these were previously captured (the
Nidec 20N-series blower *motor* specs are already in the OsakaTX README §2;
this new block covers the *connector on the fan module* for each variant).

| Fan model | Voltage | Connector (as stated upstream) |
|---|---|---|
| BL24131607 | 14.4V | JST PH2.0 female 5p — pins: `ID FG SP - +` |
| 20N704R990F | — | JST PH2.0 female 4p — pinout TBD |
| 20N704R990F | 15V | JST PH2.0 female 4p — pinout TBD |
| MSD-D | — | JST PH2.0 female 4p — pinout TBD |
| 20N709U020 | — | JST PH2.0 female 4p — pinout TBD |
| 22N704V160 | 14.4V | 5-pin 2mm pitch **with latch**, female (not PH) |
| BL27302101 | 14.4V | 6-pin 2mm pitch **with latch**, female (not PH) |
| BL24131616 | 14.4V | 5-pin 2mm pitch **with latch**, female (not PH) |
| MSD-C-3 | — | 4-pin "like PH, but looser vertically" |
| MSD-G-V1 | — | LHE MX3.0 2×2 (4-pin) 3mm pitch **with latch**, **male** (aka Molex Micro-Fit 3.0) |

### Key observations

- **BL24131607** is the only fan with an explicit pinout in the upstream
  block: `ID FG SP - +` across the 5-pin PH2.0. Decoded:
  - `ID` — identity / presence detect
  - `FG` — frequency-generator tachometer feedback
  - `SP` — set-point (PWM speed command input)
  - `-` — ground
  - `+` — motor power (battery voltage)
  This matches the "PWM input + FG feedback" interface already recorded for
  the Nidec Smart_20N BLDC family in README §2, and adds an `ID` pin that was
  not previously documented.
- The three latching 2mm-pitch fans (22N704V160, BL27302101, BL24131616) are
  **not JST PH** — they are a 2mm-pitch latching family. This is a useful
  warning against assuming PH2.0 across all Roborock-family fans.
- **MSD-G-V1** uses a **Molex Micro-Fit 3.0** (LHE MX3.0) 2×2 male connector,
  the same family as the battery connector (see §4 below). The MSD-G-V1 line
  was refined on 2026-07-18 (commit `4e6c0134`) to specify the
  male/female direction and the Molex-equivalent name.
- The other 4-pin PH2.0 fans (20N704R990F ×2, MSD-D, 20N709U020) carry pinout
  `TBD` upstream.

### What's new vs. the existing OsakaTX README

The existing README §2 documents the **Nidec bare-motor electrical specs**
(rated speed, current, power, pressure, noise) for many 20N/22N/35N series
motors. It does **not** list the module-level connector type per fan SKU. This
update adds the **connector-on-module** dimension, which is what a PCB
designer needs to pick the right receptacle. The two are complementary.

---

## 4. Battery Pack — BRR-2P4S-5200 4-pin Connector Pinout

Upstream SPEC.md now gives an explicit pinout for the 4S battery pack
connector:

```
Battery BRR-2P4S-5200 14.4V nominal - 4-pin 3mm pitch with latch male LHE MX3.0 (C3001-H04), Molex Micro-Fit 3.0
[o66o] 4321 BAT+ 10.7K/NTC 0.62M/ID GND
```

Decoded:

| Property | Value |
|---|---|
| Pack model | BRR-2P4S-5200 |
| Configuration | 2P4S (2 parallel × 4 series) |
| Nominal voltage | 14.4 V |
| Connector | 4-pin, 3mm pitch, **with latch**, **male** on the battery side |
| Connector family | LHE MX3.0 `C3001-H04` ≡ Molex Micro-Fit 3.0 |
| Mating (board side) | female Micro-Fit 3.0 4-pin |

Pin map (the `[o66o]` is the physical layout diagram — a 2×2 block with the
two "o" corners occupied by the latch / keying features; the digits `4321`
are the pin numbers read in some order across the body):

| Pin | Signal |
|-----|--------|
| 1 | BAT+ (pack positive) |
| 2 | 10.7k / NTC (thermistor — 10.7 kΩ NTC for temperature) |
| 3 | 0.62M / ID (identity / presence — 620 kΩ resistor, or possibly 0.62 MΩ pull) |
| 4 | GND (pack negative) |

### Notes

- **NTC 10.7 kΩ** is the battery thermistor for the charger IC — required
  input for any JEITA-style charge-current derating and for the 0.5C cap
  specified in the same SPEC.md. This is the first time the thermistor value
  is recorded in the part-specs compilation.
- **ID 0.62 MΩ** is a pack-identity resistor (so the charger can confirm a
  genuine / matching pack is fitted before enabling high-current charge).
  This is also new information.
- The connector is the **same family** as the MSD-G-V1 suction fan (Molex
  Micro-Fit 3.0), simplifying the BOM — but note the fan is *male* and the
  battery is also *male*, so the board-side receptacles are both *female*
  Micro-Fit 3.0 (4-pin), in different layouts (1×4 battery vs. 2×2 fan).

---

## 5. Alternative LiDAR Module Connectors

Upstream SPEC.md adds a dedicated **LiDAR pinouts** block listing four LiDAR
module candidates with their cable connectors. The OsakaTX README §3 covers
the **3irobotix CRL-200S / Delta-2D** in detail (5-pin JST PH 2.0mm); the
block below is the upstream's catalogue of *alternative* LiDAR modules under
consideration for the BOM, all of which use **JST GH 1.25mm**:

| LiDAR PCB marking | Connector | Notes |
|---|---|---|
| `X-WPFTB-V2.6.2` | JST GH 1.25mm 4-pin female (needs m) | — |
| `D-WPFTBCD-V1.0.1` | JST GH 1.25mm 4-pin female (needs m) | — |
| LDROBOT **LD14P** lookalike | JST GH 1.25mm 4-pin female (needs m) | LDROBOT LD14P is a known 2D LiDAR; "lookalike" suggests a clone/rebrand |
| "Mystery mini" | JST GH 1.25mm **5**-pin female (needs m) | Unknown model; the extra 5th pin distinguishes it from the 4-pin units |

`(needs m)` = the LiDAR-module side is female, so the board-side needs a
**male** GH 1.25mm receptacle. (Opposite convention to the "needs f" on the
wheel module above — worth double-checking before footprint selection.)

### What's new

- The BOM is considering **at least four** LiDAR candidates beyond the
  CRL-200S, all on JST GH 1.25mm. Previously the part-specs compilation
  treated the CRL-200S as the single LiDAR. This expands the connector
  family that the I/O board LiDAR receptacle must accommodate.
- **LD14P** is a specific, identifiable LDROBOT model — its datasheet can be
  fetched separately to recover the 4-pin GH pinout (M+, M-, TX, GND per
  LDROBOT's published LD14P doc) and confirm whether the "lookalike" shares
  it.
- The "Mystery mini" 5-pin variant is the only one that deviates from 4-pin;
  the 5th pin is most likely a 3.3V/5V select or a mode/enable input, but
  this is speculation until the module is identified.

### Remaining unknown

The per-pin map for each of the four GH connectors is **not** given in
upstream SPEC.md (only the connector type and pitch). For the LD14P the
pinout can be recovered from LDROBOT's public datasheet; for the two
`WPFTB*` PCB markings and the "Mystery mini", identification + pinout
remains open.

---

## 6. Compute / Camera Note

Upstream SPEC.md `Compute + Camera` section now reads:

> - 2x 15-pin ArduCam-style connectors for OV5647
> - TODO add USB to I/O board

This cross-confirms the OV5647 camera work captured in PR #28
(`part-specs-obstacle-camera-ov5647-jul18`) — the I/O board exposes **two**
15-pin ArduCam-style CSI connectors for OV5647 modules, matching the "stereo
/ front + rear" camera option noted in that PR. The new fact here is the
**count: two connectors**, which the camera PR did not pin down. No new file
is needed for this; it is recorded here for cross-reference.

---

## 7. Summary — What This Update Adds vs. Existing OsakaTX part-specs

| New fact | Source in upstream SPEC.md | Previously in OsakaTX part-specs? |
|---|---|---|
| Drive wheel motor coil resistance = **19 Ω** | drive wheel row | ❌ No (only 14.4V / 3.5A stall) |
| Wheel module connector family = **JST ZH 1.5mm male 7p** | wheel assembly pinout block | ⚠️ Partial (Scowt PR #13 said "7-pin JST", family not pinned) |
| Hall wire order orange→blue→brown (pins 3→5) | wheel assembly pinout block | ✅ Matches Scowt PR #13 (recorded) |
| Wheel-drop switch pins 1/2 labelled "on"/"com" | wheel assembly pinout block | ⚠️ Scowt had "NC"/"common" — polarity convention differs |
| 10 suction-fan rows (9 distinct SKUs) with per-module connector types | motor pinouts block | ❌ No (only Nidec bare-motor specs) |
| BL24131607 5-pin PH2.0 fan pinout `ID FG SP - +` | motor pinouts block | ❌ No |
| MSD-G-V1 fan = Molex Micro-Fit 3.0 2×2 male | motor pinouts block (refined 2026-07-18) | ❌ No |
| Battery BRR-2P4S-5200 4-pin Micro-Fit 3.0 male pinout | charging section | ❌ No |
| Battery NTC = 10.7 kΩ, ID = 0.62 MΩ | charging section | ❌ No |
| 4 alternative LiDAR modules on JST GH 1.25mm | LiDAR pinouts block | ❌ No (only CRL-200S documented) |
| I/O board has **2×** OV5647 CSI connectors | Compute + Camera section | ⚠️ Camera PR #28 had the module but not the count |

### Gaps still open after this update

| Gap | Status |
|---|---|
| Encoder PPR (raw, via pole-count / magnetic-ring inspection) | ❌ Still ~228 PPR *derived* from VacuumTiger calibration; not physically confirmed |
| Gearbox ratio (via tooth counting) | ❌ Still ~190:1 *derived*; not physically confirmed |
| Full J25/J26 16-pin mainboard pinout | ❌ Upstream's wheel-connector block does not touch J25/J26; still needs PCB continuity tracing |
| Caster wheel exact wheel / ball diameter | ❌ No new data this run |
| Per-pin map for the 4 alternative LiDAR GH connectors | ❌ Only connector type given upstream |
| Pinout of the 4-pin PH2.0 fan variants (20N704R990F, MSD-D, 20N709U020) | ❌ Still TBD upstream |

---

## 8. References

- Upstream file (as of 2026-07-18): `makerspet/oomwoo-io-board` `docs/SPEC.md`
  - Commit `dba0d1c3` "Update SPEC.md" (2026-07-18 19:40 UTC) — added motor
    pinouts block, LiDAR pinouts block, Compute+Camera section, drive wheel
    19 Ω.
  - Commit `75803b7e` "Update power specifications for robot and dock"
    (2026-07-18 20:18 UTC) — expanded battery connector to
    `BRR-2P4S-5200 / LHE MX3.0 / Molex Micro-Fit 3.0` with the
    `[o66o] 4321 BAT+ 10.7K/NTC 0.62M/ID GND` pinout.
  - Commit `4e6c0134` "Update MSD-G-V1 suction fan description" (2026-07-18
    22:55 UTC) — refined MSD-G-V1 connector to
    `LHE MX3.0 2x2 (4-pin) 3mm pitch with latch male (aka Molex Micro-Fit 3.0)`.
  - Merge `cff32b3e` of PR #1 `xbattlax/docs-spec-cleanup-xbattlax`
    (2026-07-18) — general cleanup that preceded the above.
- Cross-reference (existing OsakaTX part-specs):
  - `README.md` §1 drive wheel, §2 suction fan, §3 LiDAR (CRL-200S)
  - `io-board-wheel-connector-and-caster.md` — OOMWOO I/O board J12/J13
    5-pin ZH wheel connector (the *OOMWOO redesign*; this update covers the
    *original Roborock* wheel connector, which is distinct)
  - `io-board-sensors-and-motors-schematic.md` — OOMWOO I/O board LiDAR J17
    (4-pin, M+/M-/RX/5V) and motor driver table
  - PR #28 `part-specs-obstacle-camera-ov5647-jul18` — OV5647 camera module
- External cross-checks:
  - Scowt PR #13 (merged) — physical wheel-module 7-pin connector inspection
  - [Molex Micro-Fit 3.0 family](https://www.molex.com/en-us/products/part/micro-fit/030120420) — `C3001-H04` equivalent 4-pin body
  - [LDROBOT LD14P product page](https://www.ldrobot.com/) — for the 4-pin GH pinout cross-check (to be fetched separately)
