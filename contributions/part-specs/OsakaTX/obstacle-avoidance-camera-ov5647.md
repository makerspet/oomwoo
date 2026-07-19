# Obstacle Avoidance Camera — OmniVision OV5647

> **Contributor:** OsakaTX
> **Added:** July 18, 2026
> **BOM entry:** "Obstacle avoidance vis camera — OV5647 5M MIPI 16-pin cable, 130 deg, no IR-cut filter" (added to `BOM.md` in upstream commit `6b8f59c`, 2026-07-18)
> **Source:** The OV5647 is the sensor behind the original Raspberry Pi Camera Module 1. Specifications below are taken from the official Raspberry Pi camera documentation, which publishes the sensor-level parameters. The BOM item pairs this sensor with a wider-angle (≈130°) lens and removes the IR-cut filter for night-vision / near-IR obstacle detection.

This file complements the main `README.md` part-specs index. It documents the newly
sourced obstacle-avoidance camera so the camera has the same level of part-spec
coverage as the LiDAR, ToF, IMU, and other sensors.

---

## Sensor Identification

| Parameter | Value |
|---|---|
| **Sensor** | OmniVision OV5647 (same die as Raspberry Pi Camera Module 1) |
| **Type** | CMOS rolling-shutter image sensor |
| **Optical format** | 1/4" |
| **Still resolution** | 5 megapixels (2592 × 1944) |
| **Pixel size** | 1.4 µm × 1.4 µm |
| **Sensor image area** | 3.76 × 2.74 mm |
| **Color filter array** | Bayer RGB |
| **Output interface** | MIPI CSI-2 (2-lane D-PHY) |
| **Control bus** | I²C (SCL/SDA), typically 400 kHz |
| **Supply** | 2.8 V (AVDD, analog) + 1.8 V (DOVDD, I/O; 1.7-3.0 V range) + 1.5 V (DVDD, core, internal regulator); module-level 3.3 V via the CSI connector |

> **Note on the sensor identity:** The BOM entry names "OV5647" explicitly. The
> Raspberry Pi Camera Module 1 (the best-known OV5647 carrier) is listed in the
> official Raspberry Pi camera comparison table with the parameters reproduced
> above. The OOMWOO BOM item is **not** the stock Raspberry Pi Camera Module 1 —
> it is an AliExpress "night vision" module that uses the same OV5647 die with a
> third-party wider-angle lens and no IR-cut filter. Sensor-level specs transfer;
> lens-level specs (focal length, FoV, F-stop) do **not** and are given separately
> below from the BOM entry.

---

## Module-Level Specs (BOM Entry)

From `BOM.md` (upstream commit `6b8f59c`, 2026-07-18):

| Parameter | Value |
|---|---|
| **Sensor** | OV5647, 5 MP |
| **Cable** | 16-pin MIPI CSI-2 FPC |
| **Field of view** | ~130° (wide-angle lens, third-party) |
| **IR-cut filter** | **None** (night-vision / near-IR variant) |
| **Purpose** | Advanced obstacle avoidance |
| **Retail price** | $6–7 |
| **Search term** | "ov5647 night vision" — [AliExpress](https://www.aliexpress.us/wholesale-ov5647-night-vision.html) / [Amazon](https://www.amazon.com/s?k=ov5647+night+vision) / [eBay](https://www.ebay.com/sch/i.html?_nkw=ov5647+night+vision) |

The "no IR-cut filter" variant is the key difference from the standard Raspberry
Pi Camera Module 1: removing the IR-cut filter lets near-infrared light reach the
sensor, which is what makes these modules usable as a low-light / active-IR
obstacle camera when paired with an IR illuminator.

---

## CSI-2 Connector Pinout (16-pin FPC, 1.0 mm pitch)

> ⚠️ **Connector caveat:** The BOM entry specifies a **16-pin** cable. The
> standard Raspberry Pi CSI-2 connectors are **15-pin** (flagship Pi ≤4, CM1–CM4
> IO boards) or **22-pin** (Pi Zero, Pi 5, CM5 IO board). A 16-pin 1.0 mm FPC is
> a common third-party OV5647 module format and typically carries the same
> MIPI CSI-2 + I²C + power signals as the 15-pin Raspberry Pi connector, often
> with one pin reserved or repurposed for an on-module IR illuminator enable.
> The exact 16-pin assignment is module-vendor-specific; verify against the
> module's silkscreen before wiring. The 15-pin Raspberry Pi pinout is reproduced
> below as the reference since the signal set is identical.

### Reference: 15-pin CSI-2 connector (Raspberry Pi, Amphenol SFW15R-2STE1LF)

Direction is from the SBC's perspective. I²C lines are pulled up to 3.3 V on the
SBC side.

| Pin | Name | Description | Direction / Type |
|-----|------|-------------|------------------|
| 1 | GND | Ground | Ground |
| 2 | CAM_DN0 | D-PHY lane 0 (negative) | Input, D-PHY |
| 3 | CAM_DP0 | D-PHY lane 0 (positive) | Input, D-PHY |
| 4 | GND | Ground | Ground |
| 5 | CAM_DN1 | D-PHY lane 1 (negative) | Input, D-PHY |
| 6 | CAM_DP1 | D-PHY lane 1 (positive) | Input, D-PHY |
| 7 | GND | Ground | Ground |
| 8 | CAM_CN | D-PHY clock (negative) | Input, D-PHY |
| 9 | CAM_CP | D-PHY clock (positive) | Input, D-PHY |
| 10 | GND | Ground | Ground |
| 11 | CAM_IO0 | GPIO (typically power-enable, active high) | Bidirectional, 3.3 V |
| 12 | CAM_IO1 | GPIO (typically clock / LED) | Bidirectional, 3.3 V |
| 13 | SCL | I²C clock | Bidirectional, 3.3 V |
| 14 | SDA | I²C data | Bidirectional, 3.3 V |
| 15 | 3V3 | 3.3 V supply | Output |

**Likely 16-pin module mapping (hypothesis, verify on-silkscreen):** the 16th pin
on night-vision OV5647 modules is commonly used for an on-board IR-LED
illuminator enable (active-high) or an extra GND. Treat this as unverified until
the specific module is inspected.

### Compute Module 5 / Pi 5 (22-pin) connector

The OOMWOO BOM lists both a Raspberry Pi CM4 ≥2 GB (primary, ~$62.50) and a
CM5 ≥2 GB (~$72.50) as compute-module options. On a CM5 build, the camera
attaches through the 22-pin CSI-2 connector (Amphenol F32Q-1A7H1-11022).
It is a superset of the 15-pin connector: same lane-0/lane-1 + clock + I²C +
power signals, plus lane 2 and lane 3 pairs for 4-lane sensors. The OV5647 is a
2-lane sensor, so only the lane-0/lane-1 pins are used; the extra lanes are
no-connects. The full 22-pin pinout is in the Raspberry Pi mechanical drawings /
Product Information Portal referenced below.

---

## Host-Side Interface (OOMWOO compute module)

- **Compute module:** Raspberry Pi **CM4 or CM5 ≥2 GB** (`BOM.md` lists CM4 ≥2 GB
  as primary at ~$62.50 and CM5 ≥2 GB as the alternative at ~$72.50; the ≥4 GB
  options were dropped 2026-07-18 in commit `19ec1c2`). The CSI connector differs
  by choice: 15-pin on the CM4 IO board, 22-pin on the CM5 IO board.
- **Camera interface:** MIPI CSI-2 receiver on the compute module's SoC (BCM2711
  on CM4, BCM2712 on CM5), 2 lanes sufficient for the OV5647's peak data rate.
- **Driver:** `ov5647` in the Raspberry Pi / libcamera stack; the sensor is a
  long-supported first-party Raspberry Pi sensor.
- **Control:** I²C for sensor register configuration; `CAM_IO0` for power-enable.

---

## Why a No-IR-Cut OV5647 for Obstacle Avoidance

- The OV5647's Bayer photodiodes are sensitive into the near-IR (~1000 nm); the
  IR-cut filter on the standard Raspberry Pi Camera Module 1 blocks this band to
  produce natural color.
- Removing the IR-cut filter lets the module image in near-darkness when paired
  with a 940 nm (or 850 nm) IR illuminator — the same approach used by Roborock's
  own "Reactive AI" obstacle cameras and by commercial night-vision CSI modules.
- At ~$6–7 retail this is the cheapest obstacle-avoidance sensing option in the
  BOM, well below the VL53L7CX ToF ($8–15) and complementary to the 2D LiDAR
  (which gives range but not object classification).

---

## What We Still Need

| Item | Status |
|---|---|
| Exact 16-pin FPC pinout for the specific AliExpress module | ❌ Needs silkscreen inspection of the chosen module |
| Lens focal length / F-stop / distortion profile for the 130° variant | ❌ Vendor-specific, not in the BOM entry |
| IR illuminator: on-module vs. external, wavelength (850 vs. 940 nm), drive | ❌ Needs module inspection |
| Module PCB dimensions / mounting-hole pattern | ❌ Needs physical measurement |
| Power consumption (sensor + illuminator) | ❌ Needs measurement |
| Confirmed libcamera / `ov5647` driver compatibility with the no-IR-cut module | ❌ Needs runtime test on CM5 |

---

## References

- [Raspberry Pi camera documentation — hardware specification table](https://www.raspberrypi.com/documentation/accessories/camera.html) (CC BY-SA 4.0) — source for the sensor-level specs (resolution, optical format, pixel size, image area).
- CSI connector pinouts and Amphenol part numbers (15-pin `SFW15R-2STE1LF`, 22-pin `F32Q-1A7H1-11022`): Raspberry Pi mechanical drawings / Product Information Portal ([pip.raspberrypi.com](https://pip.raspberrypi.com)) and the CM4 IO board / Raspberry Pi 5 schematics, cross-checked against the [Arducam CSI pinout reference](https://docs.arducam.com/Raspberry-Pi-Camera/raspberry-pi-camera-pinout/).
- [OOMWOO BOM.md — obstacle avoidance camera entry](https://github.com/makerspet/oomwoo/blob/main/BOM.md) (commit `6b8f59c`, 2026-07-18).
- [OmniVision OV5647 datasheet (public mirror)](https://cdn.sparkfun.com/datasheets/Dev/RaspberryPi/ov5647_full.pdf) — full preliminary specification: power rails (AVDD 2.8 V, DOVDD 1.7-3.0 V, DVDD 1.5 V), registers, pinout.
