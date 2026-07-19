# Obstacle-Detection Range Camera — VL53L7CX / VL53L7CH

> Part-specs coverage for the **"Obstacle detection range camera"** BOM entry
> added in upstream commit `d32b27d` (2026-07-18): *"Sourced obstacle avoidance
> range sensor"*, which split the prior single VL53L7CX row into a distinct
> obstacle-detection role alongside the OV5647 vision camera.
>
> BOM entry (verbatim from `BOM.md` line 62):
> | Obstacle detection range camera | 1 | $8–15 | VL53L7CX or VL53L7CH, 8x8 obstacle detection (90° FoV) | … |

This document gives the verified spec sheet for both variants, the
authoritative CH-vs-CX difference, the full LGA-16 pinout (which supersedes
the older LGA-12 / 4.4×2.4 mm figures that appear in the consolidated
`README.md` — those were copied from the unrelated VL53L5CX and are incorrect
for the L7 family), and the application context for oomwoo.

---

## 1. Why two variants in the BOM?

The BOM lists **VL53L7CX or VL53L7CH** as acceptable. Per the STMicroelectronics
datasheets (VL53L7CX DS13865 Rev 8, VL53L7CH DS14309 Rev 3, both Sept 2024) and
confirmation from ST staff on the ST Community (Anne BIGOT, ST Technical
Moderator, Oct 2025):

- The two parts are **pin-to-pin and driver compatible** (datasheet Features:
  *"Pin-to-pin compatible with VL53L5CX and VL53L7CX"* on the CH; *"Pin-to-pin
  and driver compatible with VL53L5CX"* on the CX, and the CH adds CX
  compatibility).
- The **only difference is firmware**: the **CH** additionally exposes
  **Compact Normalized Histogram (CNH)** raw per-zone histogram data (up to 128
  bins, min bin width 37 mm) for AI/ML processing, while still outputting all
  the standard processed ranging data (distance, signal amplitude, reflectance,
  ambient IR, motion indicator). The **CX** outputs the standard processed data
  only.
- Electrical, optical, mechanical, FoV, range, I²C address and package are
  identical. Either part can be soldered onto the same footprint.

**Practical guidance for oomwoo:** use the **CX** for a pure distance-threshold
obstacle detector (cheaper, simpler driver path). Choose the **CH** if you plan
to feed raw histogram bins into an on-host AI model for floor-type recognition
or clutter classification — the CH datasheet explicitly lists *"Floor sensing
for robotics and vacuum cleaners"* as a target application.

---

## 2. Common specifications (both VL53L7CX and VL53L7CH)

All figures below are taken verbatim from the two ST datasheets and cross-check
between them. Where the two datasheets differ in wording, the value is identical
numerically.

| Parameter | Value | Source |
|---|---|---|
| **Type** | ToF, 8×8 multizone (64 zones; 4×4 also selectable on CX) | DS13865 §1 / DS14309 §1 |
| **Field of view (detection)** | 90° diagonal (60° × 60° square) | DS14309 Table 2 |
| **Collector exclusion zone** | 116° diagonal (74° × 74°) | DS14309 Table 2 |
| **Maximum range** | 350 cm (varies with target reflectivity & ambient) | both datasheets |
| **Minimum range** | 2 cm | DS14309 Table 1 |
| **Frame rate** | up to 60 Hz | DS13865 Features / DS14309 Table 1 |
| **I²C address** | 0x52 (default, configurable) | both |
| **I²C speed** | up to 1 MHz (Fast-mode Plus) | both |
| **Emitter** | 940 nm invisible VCSEL, Class 1 eye-safe | both |
| **Supply — AVDD** | 2.8 V or 3.3 V | DS14309 Table 1 |
| **Supply — IOVDD** | 1.8 V, 2.8 V, or 3.3 V | DS14309 Table 1 |
| **Operating temperature** | −30 °C to +85 °C | DS14309 Table 1 |
| **Package** | Optical LGA-16, **6.4 × 3.0 × 1.6 mm** | DS14309 Table 1 / DS13865 Features |
| **Optical elements** | DOE metalens on TX and RX (square FoV) | both |
| **Receiver** | SPAD array | both |
| **Multitarget per zone** | Yes (CX: multiple targets per zone; CH: via histogram bins) | DS13865 |
| **Motion indicator** | Per zone (direction + magnitude of target motion) | both |
| **Low-power mode** | Autonomous mode with programmable distance threshold interrupt to wake host | both |
| **Cover-glass crosstalk** | Histogram compensation (CX) / CNH (CH) mitigates crosstalk beyond 60 cm | both |

### CH-only extra features (the reason to pay the premium)

| Feature | Detail |
|---|---|
| **CNH (Compact Normalized Histogram) output** | Raw per-zone histogram with signal count per bin |
| **Histogram size** | Programmable up to 128 bins |
| **Minimum bin width** | 37 mm |
| **CNH max rate via I²C** | 30 Hz |
| **Configurations** | 64 zones × 18 bins @ 15 Hz; 32 zones × 36 bins @ 15 Hz; 16 zones × 48 bins @ 25 Hz |
| **Ambient IR level** | Reported per zone |
| **Driver compatibility** | Same driver as VL53L8CH |

---

## 3. Pinout (LGA-16, identical for CX and CH)

> ⚠️ This supersedes the 8-row pinout table in the consolidated
> `contributions/part-specs/OsakaTX/README.md` §4, which listed only 8 pins and
> a 4.4 × 2.4 mm LGA-12 package. Those figures were carried over from the
> VL53L5CX and are **incorrect for the VL53L7 family**. The L7 parts are LGA-16
> in a 6.4 × 3.0 × 1.6 mm package; the table below is transcribed from
> DS14309 §2.5 Table 3 and matches DS13865.

Pin assignments use the A/B/C row + column notation from the ST datasheet
(bottom view).

| Pin | Name | Type | Function |
|---|---|---|---|
| A1 | I2C_RST | Digital in | I²C interface reset, active high. Toggle 0→1→0. Tie to GND via 47 kΩ. |
| A2 | RSVD4 | Reserved | Connect to GND |
| A3 | INT | Digital I/O | Interrupt output (open-drain, tristate default). 47 kΩ pull-up to IOVDD required. |
| A4 | IOVDD | Power | 1.8 V / 2.8 V / 3.3 V digital core & I/O supply |
| A5 | LPn | Digital in | Comms enable. 0 = disable I²C, 1 = enable. 47 kΩ pull-up to IOVDD required. Used for I²C address reconfiguration in multi-device buses. |
| A6 | RSVD1 | Reserved | Connect to GND |
| A7 | RSVD2 | Reserved | Connect to GND |
| B1 | AVDD | Power | 2.8 V or 3.3 V analog & VCSEL supply |
| B4 | THERMAL_PAD | GND | Connect to ground plane for thermal conduction (see AN5853) |
| B7 | AVDD | Power | 2.8 V or 3.3 V analog & VCSEL supply |
| C1 | GND | Ground | Ground |
| C2 | RSVD6 | Reserved | General-purpose I/O, open-drain default, 47 kΩ pull-up to IOVDD required |
| C3 | SDA | Digital I/O | I²C data, 2.2 kΩ pull-up to IOVDD required |
| C4 | SCL | Digital in | I²C clock, 2.2 kΩ pull-up to IOVDD required |
| C5 | RSVD5 | Reserved | Do not connect |
| C6 | RSVD3 | Reserved | Connect to GND |
| C7 | GND | Ground | Ground |

**Notes (from datasheet):**
- Toggling I2C_RST resets only the I²C interface, not the sensor. Full sensor
  reset follows the procedure in the user manual (UM3038 for the CX, UM3183 for the CH).
- All digital signals are driven to the IOVDD level.
- AVDD appears on two pins (B1, B7); both must be powered.
- Required external components: 47 kΩ pull-ups on INT, LPn, RSVD6; 2.2 kΩ
  pull-ups on SDA, SCL; 47 kΩ on I2C_RST to GND.

---

## 4. Application to oomwoo

The BOM positions this sensor as the **obstacle-detection range camera**,
distinct from the OV5647 vision camera (used for visual obstacle avoidance in
low light with an IR illuminator). The two are complementary:

| Sensor | Role | Output | Latency / compute |
|---|---|---|---|
| **VL53L7CX/CH** | Geometric obstacle detection — direct 8×8 distance map over 90° FoV | 64 distance + reflectance + motion values per frame, up to 60 Hz | Low — direct I²C read, no image pipeline |
| **OV5647 (vis camera)** | Semantic obstacle avoidance — recognize objects, textures, hazards via vision/ML | 5 MP MIPI CSI-2 frames | High — requires CSI-2 capture + inference |

ST's own application notes for the VL53L7 family list these robotics-relevant
use cases verbatim:
- *"Robotics applications (SLAM, wall tracking, small object detection, cliff
  prediction, floor type recognition)"* — VL53L7CX datasheet
- *"Floor sensing for robotics and vacuum cleaners"* — VL53L7CH datasheet
- *"Vacuum cleaners (three sensors can cover 180° × 60° FoV)"* — VL53L7CX datasheet

For oomwoo's single-sensor BOM, the 90° FoV covers the forward hemisphere;
combine with the 2D LiDAR (CRL-200S) for full 360° planar coverage and the
VL53L7 for the volumetric forward/downward volume (cliff prediction, low
obstacles below the LiDAR plane).

### CH vs CX recommendation for oomwoo

- **Default: VL53L7CX** — sufficient for distance-threshold obstacle avoidance,
  cheaper, simpler driver, all standard ranging data available.
- **Upgrade path: VL53L7CH** — if/when oomwoo adds an AI layer for floor-type
  recognition (carpet vs hard floor vs rug — relevant to the existing carpet
  ultrasonic sensor) or clutter classification from raw histogram shapes. Same
  footprint, so the PCB does not need to change to swap later.

---

## 5. What we still need (gaps)

These items require physical inspection of a specific carrier PCB or module and
are not in the ST datasheet:

- [ ] **Breakout/module PCB dimensions** — oomwoo will likely use a third-party
      breakout (e.g. SATEL-VL53L7, P-Nucleo-VL53L7CX1) rather than bare LGA-16;
      the carrier PCB mechanicals need to be sourced from the chosen module.
- [ ] **Cover-glass design** — the datasheet specifies a collector exclusion
      zone (74° × 74°, 116° diagonal) and recommends AN5853 for cover-glass
      design; oomwoo's chassis window geometry must respect this.
- [ ] **I²C bus integration** — confirm the STM32 I/O PCB I²C port, pull-up
      values, and whether LPn/INT are wired to GPIOs or tied. Address 0x52 must
      not collide with the IMU (0x68/0x69) or ToF sensor on the same bus.
- [ ] **Power sequencing** — AVDD and IOVDD can be independent (1.8 V IOVDD
      with 3.3 V AVDD is common on STM32 designs); confirm the I/O PCB rail
      arrangement.
- [ ] **Driver / Ultron (ST ultra-lite driver) vs full ST API** — pick one and
      document the ROS2 wrapper interface.

---

## 6. References

- VL53L7CX datasheet (DS13865 Rev 8, Sep 2024): https://www.st.com/resource/en/datasheet/vl53l7cx.pdf
- VL53L7CH datasheet (DS14309 Rev 3, Sep 2024): https://www.st.com/resource/en/datasheet/vl53l7ch.pdf
- ST Community — "Difference between the VL53L7 CH and CX variants" (Anne BIGOT, ST Technical Moderator, Oct 2025): https://community.st.com/imaging-sensors-49/difference-between-the-vl53l7-ch-and-cx-variants-157838
- SATEL-VL53L7 breakout data brief: https://www.st.com/resource/en/data_brief/satel-vl53l7.pdf
- P-Nucleo-VL53L7CX1 (eval board): https://www.st.com/en/evaluation-tools/p-nucleo-vl53l7cx1.html
- STM32duino VL53L7CX Arduino library: https://github.com/stm32duino/VL53L7CX
- UM3038 — VL53L7CX user guide (Pololu mirror): https://www.pololu.com/file/0J1993/um3038-a-guide-to-using-the-vl53l7cx-timeofflight-multizone-ranging-sensor-with-90-fov-stmicroelectronics.pdf
- UM3183 — VL53L7CH user manual (sensor reset procedure): https://www.st.com/resource/en/user_manual/um3183-vl53l7ch-user-manual-stmicroelectronics.pdf
- AN5853 — cover-glass design: https://www.st.com/resource/en/application_note/an5853.pdf

---

## 7. Correction note for the consolidated README

The existing `contributions/part-specs/OsakaTX/README.md` §4 ("VL53L7CX —
Multizone Time-of-Flight Sensor") contains two inherited errors (identified while
writing this file). They are fixed in a **separate README-correction PR**, kept
out of this branch so each stays independently mergeable:

1. **Package size** — README states `4.4 × 2.4 × 1.0 mm (LGA-12)`. The correct
   VL53L7CX package is **6.4 × 3.0 × 1.6 mm (LGA-16)** per DS13865. The
   4.4 × 2.4 × 1.0 mm LGA-12 figure is the VL53L5CX package, not the L7.
2. **Pinout** — README lists 8 pins (AVDD, GND, GPIO1, LPn, I2C_RST, SCL, SDA,
   IOVDD). The real L7 part is LGA-16 with the A1–C7 pin map in §3 above;
   there is no pin named "GPIO1" — the interrupt pin is **INT** (A3), and
   there are multiple AVDD/GND/RSVD pins.

They are documented here for the record; the actual README patch ships in that
separate PR to avoid conflicting with this obstacle-detection spec addition.
