# OOMWOO I/O Board Wheel Connector & Caster Wheel Specs

> **Derived from:** oomwoo-io-board KiCad reference schematic (committed Jul 12, 2026),
> oomwoo-io-board SPEC.md (updated Jul 14, 2026), AlieksieievYurii/vacuum-cleaner motherboard schematic,
> and commercial replacement part listings.
> **Last updated:** July 17, 2026

## 1. OOMWOO I/O Board Wheel Motor Connector (from KiCad reference schematic)

The `makerspet/oomwoo-io-board` repository contains a KiCad conversion of the reference
RK3562 + STM32G070 schematic (committed Jul 12, 2026). The wheel motor sub-sheet
(`WHEEL-MOTORs .kicad_sch`) reveals the OOMWOO design's connector architecture.

### Connector: J12 / J13 — 5-pin JST ZH 1.5mm

| Property | Value |
|----------|-------|
| Reference designators | J12 (left wheel), J13 (right wheel) |
| Connector type | JST ZH 1.5mm pitch, SMD, 5-position |
| Footprint (KiCad) | `CONN-SMD_5P-P1.50_ZX-ZH1.5-5PWT` |
| Value label | "WHEEL-MOTOR-RIGHT" (both labeled RIGHT — likely a copy-paste artifact; J12 = left, J13 = right) |

### Pin Assignments (inferred from net labels)

The schematic uses a **5-pin connector** with the following net connections:

| Pin | Net Label | Function |
|-----|-----------|----------|
| 1 | `WHEEL-M-LEFT-IN1` / `WHEEL-M-RIGHT-IN1` | Motor driver IN1 (PWM/dir) |
| 2 | `WHEEL-M-LEFT-IN2` / `WHEEL-M-RIGHT-IN2` | Motor driver IN2 (PWM/dir) |
| 3 | `WHEEL-M-LEFT-ENCODE-A` / `WHEEL-M-RIGHT-ENCODE-A` | Encoder signal A (single-channel) |
| 4 | `VCC-5V-WHEEL` | +5V supply for encoder |
| 5 | GND | Ground |

> ⚠️ **Note:** The connector has only **5 pins** (not 6 or 7 as in the original Roborock design).
> Motor power is NOT on this connector — it goes through the DRV8870 H-bridge on the I/O board.
> The connector carries only: motor driver logic signals (IN1/IN2), encoder signal, +5V, and GND.
> The "ENCODE-A" net label (missing the trailing 'R') appears to be a typo in the original Altium design.

### Motor Driver: DRV8870DDAR

| Property | Value |
|----------|-------|
| IC | DRV8870DDAR (TI DRV8870) |
| Package | HSOP-8 with exposed pad |
| KiCad footprint | `HSOP-8_L5.0-W4.0-P1.27-LS6.2-BL-EP` |
| Quantity | 2 (one per wheel) |

### Key Design Differences vs. Original Roborock S5

| Feature | Roborock S5 (original) | OOMWOO I/O board (reference) |
|---------|------------------------|------------------------------|
| Connector | 7-pin JST (wheel module) | 5-pin JST ZH 1.5mm |
| Motor power | On connector (red/black wires) | Via on-board DRV8870 H-bridge |
| Encoder | Single-channel Hall (3 wires) | Single-channel (ENCODE-A) |
| Wheel-drop | Limit switch (2 grey wires) | Separate wheel-drop GPIOs |
| Pitch | 2.0mm (PH) or 1.0mm (SHD) | 1.5mm (ZH) |

The OOMWOO I/O board design **eliminates** the motor power pins from the wheel connector
by placing the H-bridge on the board itself. The connector only carries logic-level signals.

---

## 2. OOMWOO I/O Board Motor Specification (from SPEC.md)

The `oomwoo-io-board/docs/SPEC.md` (updated Jul 14, 2026) provides the following:

| Parameter | Value |
|-----------|-------|
| Motor type | DC brushed |
| Quantity | 2 (left + right drive wheels) |
| Voltage | 14.4V nominal (4S battery: 12V–16.8V) |
| Stall current | 3.5A (TODO — needs verification) |
| H-bridge | DRV8231, DRV8871, or similar |
| Power source | Direct from 4S battery (no DC-DC converter) |

> The SPEC.md notes the stall current as "TODO check" — this is not yet verified.

---

## 3. AlieksieievYurii DIY Vacuum Motherboard — Alternative Pinout

The `AlieksieievYurii/vacuum-cleaner` project (a separate DIY vacuum, not Roborock-based)
provides a motherboard schematic with a **6-pin JST PH2.0** drive wheel connector.
The oomwoo io-pcb README references this as a cross-check source.

### 6-Pin JST PH2.0 Pinout

| Pin | Signal | Description |
|-----|--------|-------------|
| 1 | MOT+ | Motor power positive |
| 2 | MOT- | Motor power negative |
| 3 | HALL_SPEED | Hall sensor — speed pulse |
| 4 | HALL_DIR | Hall sensor — direction |
| 5 | +5V | Encoder supply |
| 6 | GND | Ground |

### Key Observation: Dual Hall Signals

This design uses **two Hall sensor signals** (HALL_SPEED + HALL_DIR), which implies a
**quadrature-style** encoder with two channels — unlike the Roborock S5 which has only
a single-channel encoder (confirmed by Scowt's physical inspection in PR #13).

The net labels in the AlieksieievYurii schematic:
- `hs-lw-s` = Hall Sensor (speed) of Left Wheel
- `hs-lw-d` = Hall Sensor (direction) of Left Wheel
- `hs-rw-s` = Hall Sensor (speed) of Right Wheel
- `hs-rw-d` = Hall Sensor (direction) of Right Wheel

Motor driver: **TA6586** (dual H-bridge, different from DRV8870/TMI8870)

> **Conclusion:** The Roborock S5 and the AlieksieievYurii DIY vacuum use different encoder
> architectures. The Roborock S5 is single-channel (speed only); the AlieksieievYurii design
> is dual-channel (speed + direction). OOMWOO's reference I/O board follows the single-channel
> approach, consistent with the Roborock S5 donor parts.

---

## 4. Caster Wheel Specifications

### OEM Part Identification

| Parameter | Value | Source |
|-----------|-------|--------|
| OEM part number | HA00021 | DHgate listing (Mi Robot Roborock S50/S51) |
| Compatibility | Roborock S4, S5, S5 Max, S55 Max, S65, S65 Pure, S65 MAXV, S6, S6 Pure, S6 MaxV, S7, S70, S75, E4 | Amazon WYZBEN listing |
| Material | ABS plastic (wheel), nylon housing | AliExpress listing |

### Dimensions (from replacement part listings)

| Dimension | Value | Notes |
|-----------|-------|-------|
| Overall size | ~46mm × ~52mm | Amazon WYZBEN: "Approx. 1.8'' (46mm) × 2'' (52mm)" |
| Mounting | Snap-in, no tools required | iFixit guide confirms: "pull up to remove, snap in to install" |
| Mounting type | Plate mount (snap-in friction fit) | Amazon product specs |

### Compatibility Notes

- The caster wheel is a **snap-in assembly** — no screws, no tools. It pops out by pulling
  upward and snaps back into the chassis.
- Compatible across the entire Roborock S-series (S4–S7) and E4, making it widely available.
- The wheel is an **omnidirectional caster** (ball-style or roller-style), not a simple wheel.

### Sources

- [Amazon WYZBEN 2-pack](https://www.amazon.com/WYZBEN-Casters-Replacement-Compatible-Roborock/dp/B0D54CYM1P) — dimensions: ~46mm × ~52mm
- [iFixit S5 caster replacement guide](https://www.ifixit.com/Guide/Roborock+S5+Omnidirectional+Wheel+Assembly+Replacement/167879) — snap-in removal/installation
- [AliExpress OEM caster](https://www.aliexpress.com/item/1005002334092463.html) — ABS plastic, model S5/S50
- [DHgate HA00021 listing](https://www.dhgate.com/goods/996622453.html) — OEM part number

### Remaining Unknowns

| Gap | What's Needed |
|-----|---------------|
| Exact wheel diameter | Caliper measurement of OEM part |
| Ball/roller diameter | Disassembly and measurement |
| Mounting hole dimensions | Chassis-side measurement |
| Weight | Scale measurement |
| Material durometer | Shore hardness test |

---

## 5. Updated Remaining Gaps

| Gap | Status | Notes |
|-----|--------|-------|
| Encoder PPR | ✅ Derived (~228 raw PPR, 4464 ticks/m) | From VacuumTiger calibration — confirmed stable |
| Gearbox ratio | ✅ Derived (~190:1) | From VacuumTiger velocity scale — confirmed stable |
| Full J25/J26 pinout | ⚠️ Partially resolved | OOMWOO I/O board uses 5-pin ZH, not 16-pin SHD. Original Roborock J25/J26 still needs physical probing. |
| Caster wheel specs | ⚠️ Partially resolved | OEM part number (HA00021), dimensions (~46×52mm), snap-in mount confirmed. Exact wheel diameter and ball size still need caliper measurement. |
| OOMWOO connector design | ✅ New | 5-pin JST ZH 1.5mm, DRV8870 on-board, single-channel encoder |
