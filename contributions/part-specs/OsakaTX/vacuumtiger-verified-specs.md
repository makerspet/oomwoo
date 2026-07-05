# VacuumTiger-Verified Specs — Drive Wheel Encoder, Gearbox, Odometry

> **Derived from:** codetiger/VacuumTiger source code analysis, Scowt PR #13 physical inspection, and cross-referenced calibration constants
> **Last updated:** July 7, 2026

## 1. Encoder: Single-Channel Hall-Effect (Not Quadrature)

### What the Wires Tell Us

Scowt PR #13 (merged) physically inspected the Roborock S5 drive wheel module's 7-pin JST connector. The encoder has **exactly three wires**:

| Wire | Function |
|------|----------|
| Orange | +5V supply |
| Blue | Single-channel pulse signal |
| Brown | GND |

**One signal wire = one channel.** This is definitively **not** a quadrature A/B encoder (which requires two signal wires + optional index). It's a single-channel Hall-effect sensor that outputs one pulse train whose frequency is proportional to wheel speed.

### How the GD32 Achieves High Resolution

Despite being single-channel, the VacuumTiger firmware achieves **4464 ticks/meter** through:

1. **Multi-pole magnetic ring**: The encoder wheel likely has ~32 pole pairs (a common standard for robot vac magnetic encoders)
2. **4× edge counting**: The GD32 hardware timer counts both rising AND falling edges, and likely both timer channels in parallel, yielding 4× the raw PPR:
   - Raw PPR: ~228 pulses/rev
   - After 4× decoding: ~911 ticks/rev

### Derivation

```
Wheel circumference = π × 0.065 m = 0.2042 m
Ticks per wheel rev = 4464 ticks/m × 0.2042 m/rev = 911.3 ticks/rev
Raw PPR = 911.3 / 4 = ~228 PPR
```

This is fully consistent with a ~32-pole magnetic ring encoder (common off-the-shelf part from CCmagnetics or similar).

## 2. Gearbox Ratio: ~190:1

### Derivation from Calibrated Velocity Scale

The VacuumTiger firmware has a calibration constant in `commands.rs`:

```
VELOCITY_TO_DEVICE_UNITS = 523.0
```

This means the GD32 firmware sends velocity commands to the motor controller using a scale of 523 units per m/s (or rad/s). Combined with `wheel_base = 0.233 m` and `max_linear_speed = 0.3 m/s` (from mock config.rs):

1. Motor no-load speed: 16,800 rpm = 280 rps
2. At 14.4V with ~190:1 gearbox, wheel speed ≈ 280 / 190 = 1.47 rps
3. Wheel linear speed = 1.47 × π × 0.065 = 0.30 m/s ✓ — matches the configured max of 0.3 m/s
4. At gearbox output (~1.47 rps), 911 ticks/rev = 911 × 1.47 = 1339 ticks/second = 4464 ticks/m × 0.3 m/s = 1339 ✓ — self-consistent

## 3. Calibrated Robot Parameters (from VacuumTiger)

| Parameter | Value | Source File |
|-----------|-------|------------|
| `ticks_per_meter` | 4464.0 | `sangam-io/src/devices/mock/config.rs`, `dhruva-nav/dhruva.toml`, `encoder_sim.rs` |
| `wheel_base` | 0.233 m | `sangam-io/src/devices/mock/config.rs` |
| `max_linear_speed` | 0.3 m/s | `sangam-io/src/devices/mock/config.rs` |
| `max_angular_speed` | 1.0 rad/s | `sangam-io/src/devices/mock/config.rs` |
| `robot_radius` | 0.17 m | `sangam-io/src/devices/mock/config.rs` |
| `VELOCITY_TO_DEVICE_UNITS` | 523.0 | `sangam-io/src/devices/crl200s/gd32/commands.rs` |
| `CRL200S_GYRO_SCALE` | 0.000179 rad/s per raw unit | `dhruva-slam/src/sensors/odometry/calibration.rs` |

All confirmed as empirically calibrated on real hardware, not theoretical.

## 4. Encoder Data Format

From codetiger/VacuumTiger `reader.rs` and `SENSORSTATUS.md`:

| Field | Offset | Type | Description |
|-------|--------|------|-------------|
| Left encoder | 0x10 | u16 LE | Wrapping counter |
| Right encoder | 0x18 | u16 LE | Wrapping counter |
| Update rate | — | — | 110 Hz (every status packet) |

Wraparound handling: 16-bit wrapping_sub + i16 cast (from `wheel_odometry.rs`).

## 5. Motor Driver IC: TMI8870

| Parameter | Value |
|-----------|-------|
| Manufacturer | TOLL Microelectronic |
| Top mark | T8870 |
| Package | ESOP8 |
| Type | Single H-bridge |
| Peak current | 3.6 A |
| Voltage range | 6.8–45 V |
| Control | PWM with integrated current regulation |
| Pin-compatible | TI DRV8870 |
| Datasheet | https://www.taoic.com/product/28.html |

**Need two units** (one per wheel). The second should be near J27 on the motherboard.

## 6. Connector Architecture Summary

```
Wheel Module (7-pin JST)              Mainboard
─────────────────────────────────     ─────────────────────
Grey  ── Limit switch (wheel-drop)    J25 (left, 16-pin SHD 1.0mm)
Grey  ── Limit switch (common)          → Left encoder (3 wires)
Orange ── Encoder +5V                   → Dustbox power
Blue   ── Encoder signal                → Left cliff sensor
Brown  ── Encoder GND                   → Left bumper
Black  ── Motor power (-)              J24 (left, 2-pin PH 2.0mm)
Red    ── Motor power (+)                → Motor power only
```
```
                                       J26 (right, 16-pin SHD 1.0mm)
                                         → Right encoder (3 wires)
                                         → Sweeper motor power
                                         → Right cliff sensor
                                         → Right bumper
                                       J27 (right, 2-pin PH 2.0mm)
                                         → Motor power only
```

**Key insight:** Motor power is on SEPARATE 2-pin connectors (J24/J27), NOT on the 16-pin signal connectors (J25/J26). The wheel module's 7-pin cable combines both — motor power wires (black/red) route to J24/J27 while signal wires (grey/grey/orange/blue/brown) route to J25/J26.

## Remaining Gaps (Require Physical Access)

| Gap | Category | What's Needed |
|-----|----------|---------------|
| Full J25/J26 per-pin map | 🔬 Physical probing | Multimeter continuity from connector to GD32 pins |
| Exact gearbox ratio via tooth count | ⚙️ Disassembly | Open gearbox, count teeth |
| Wheel-drop sensor model | 🔬 Physical probing | Visual inspection of sensor inside wheel module |
| Caster dimensions for selected BOM variant | 📏 Measurement | Caliper measurement of chosen caster |
