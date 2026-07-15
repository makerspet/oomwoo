# Wall & Carpet Sensors — Part Specs

> **Trigger:** Upstream BOM.md updated Jul 15, 2026 (commits `2a71e64`, `91476ba`) added two new BOM line items:
> - Wall sensor: custom PCB, $5–10, TSOP38238 IR receiver + 940nm IR LED
> - Carpet sensor: ultrasonic 300kHz, $6–12
>
> This document compiles verifiable specifications for both components from manufacturer datasheets and supplier listings.

---

## 1. Wall Sensor — TSOP38238 IR Receiver + 940nm IR LED

The BOM specifies a custom PCB wall/proximity sensor built around a **Vishay TSOP38238** IR receiver and a **940nm IR LED** emitter. This is an active reflective proximity sensor: the IR LED emits modulated 38kHz light, and the TSOP38238 detects the reflection from a nearby wall.

### 1.1 IR Receiver — Vishay TSOP38238

**Source:** Vishay datasheet (Doc 82491, Rev 2.1, 27-May-2025)
**URL:** https://www.vishay.com/docs/82491/tsop382.pdf

| Parameter | Value | Notes |
|-----------|-------|-------|
| Manufacturer | Vishay Semiconductor Opto Division | |
| Part number | TSOP38238 | 38 = 38kHz carrier frequency |
| Package | Minicast, leaded | 5.0mm W × 6.95mm H × 4.8mm D |
| Pinout | 1=OUT, 2=GND, 3=V<sub>S</sub> | 3-pin through-hole |
| Supply voltage | 2.0V – 5.5V | |
| Supply current | 0.25mA (typ), 0.45mA (max) | At V<sub>S</sub> = 3.3V, dark |
| Supply current (sunlight) | 0.45mA (max) | At 40 klx ambient |
| Carrier frequency | 38 kHz | Band-pass center |
| Bandwidth (3dB) | f₀/10 | ±10% of center frequency |
| Transmission distance | ≥30 m | With TSAL6200 at I<sub>F</sub>=50mA |
| Min. irradiance (NEC code) | 0.12 mW/m² (typ), 0.25 mW/m² (max) | |
| Min. irradiance (RC5 code) | 0.08 mW/m² (typ), 0.15 mW/m² (max) | |
| Max. irradiance | 30 W/m² | |
| Output | Active low, demodulated digital | Direct MCU interface |
| Output voltage low | ≤100mV | At I<sub>OSL</sub> = 0.5mA |
| Output current | 5mA (max) | |
| Directivity (half-angle) | ±45° | Both horizontal and vertical |
| Operating temperature | -25°C to +85°C | |
| Storage temperature | -25°C to +85°C | |
| AGC variant | AGC2 (legacy, long burst) | TSOP382xx = AGC2; TSOP384xx = AGC4 |
| Min. burst length | 10 cycles/burst | |
| Spectral sensitivity peak | ~950nm | Matches 940nm IR LED emitter |
| Pricing | ~$0.50–1.00 | DigiKey, Mouser, Adafruit ($3.95 retail) |

**Key application notes:**
- The TSOP38238 is designed for **remote control** systems (38kHz modulated bursts), NOT continuous-wave proximity detection. For wall sensing, the IR LED must be driven with **modulated 38kHz bursts** (≥10 cycles per burst) to match the receiver's AGC and band-pass filter.
- Output is **active-low** digital — goes LOW when valid 38kHz IR signal is detected.
- The AGC automatically suppresses continuous signals and ambient light interference (fluorescent lamps, sunlight up to 40klx).
- Spectral sensitivity peaks at ~950nm, providing good matching with 940nm emitters.

### 1.2 IR LED Emitter — 940nm

The BOM specifies a "940nm IR LED" without a specific part number. The Vishay **TSAL6100** is a representative 940nm IR LED commonly paired with TSOP382xx receivers.

**Source:** Vishay TSAL6100 datasheet (Doc 81009, Rev 1.8)
**URL:** https://www.vishay.com/docs/81009/tsal6100.pdf

| Parameter | Value | Notes |
|-----------|-------|-------|
| Part number | TSAL6100 (representative) | BOM does not specify exact part |
| Peak wavelength | 940nm | GaAlAs MQW technology |
| Package | T-1¾ (Ø5mm), leaded | Through-hole |
| Forward voltage | 1.35V (typ), 1.6V (max) | At I<sub>F</sub> = 100mA |
| Forward current (DC) | 100mA (max) | |
| Peak forward current | 200mA | t<sub>p</sub>/T = 0.5, t<sub>p</sub> = 100μs |
| Surge forward current | 1.5A | t<sub>p</sub> = 100μs |
| Radiant intensity | 170 mW/sr (typ) | At I<sub>F</sub> = 100mA |
| Radiant power | 40mW (typ) | At I<sub>F</sub> = 100mA |
| Angle of half intensity | ±10° | Narrow beam — good for directional wall sensing |
| Rise/fall time | 15ns / 15ns | |
| Spectral bandwidth | 30nm | |
| Operating temperature | -40°C to +85°C | |
| Pricing | ~$0.25–0.75 | |

**Alternative 940nm IR LEDs** (wider beam angle for broader wall detection):
- TSAL6200: ±17° half-angle, ~25mW/sr — wider beam, lower intensity
- TSAL6400: ±20° half-angle — even wider, suitable for close-range wall proximity

### 1.3 Wall Sensor Application Design

The custom PCB wall sensor operates as an **active reflective proximity sensor**:

```
  IR LED (940nm)          Wall surface
     │  ← modulated          │
     │    38kHz burst         │
     └─────────→ ──────────→ │
                               │ ← reflection
                               └────→ TSOP38238 (38kHz receiver)
                                          │
                                          ▼
                                     MCU GPIO (active-low)
```

**Design parameters:**
- **Emitter drive:** 38kHz modulation (e.g., via MCU PWM), burst length ≥10 cycles
- **Detection range:** Depends on LED intensity and wall reflectivity; typically 10–50mm for close wall-following
- **Output:** Active-low digital pulse when reflection detected
- **Power:** 2.0–5.5V (compatible with 3.3V and 5V logic)
- **PCB considerations:** IR LED and receiver should be side-by-side, optically isolated (barrier between emitter and receiver to prevent direct coupling), aimed at ~15–30° from parallel for optimal reflective geometry
- **BOM cost:** $5–10 (TSOP38238 ~$0.50–1.00 + IR LED ~$0.25–0.75 + PCB + passives)

**VL53L7CX as premium alternative:** The BOM notes "VL53L7CX a premium option" — this is a multi-zone ToF sensor ($8–15) with 90° FoV that can serve as a more precise wall/proximity sensor with actual distance measurement rather than binary detection.

---

## 2. Carpet Sensor — Ultrasonic 300kHz

The BOM specifies an ultrasonic carpet recognition sensor at 300kHz, $6–12. This is a high-frequency ultrasonic transducer that detects carpet vs. hard floor by analyzing the echo characteristics of the surface.

### 2.1 Manufacturer Specs — HTW HT-300PLTR1612-1

**Source:** Chengdu Huitong West-Electronic Co., Ltd. (HTW) product listing on Made-in-China.com
**URL:** https://htwsensor.en.made-in-china.com/product/xfUrtLydvQhb/China-300kHz-Floor-Carpet-Material-Recognition-Sensor-for-Robotic-Vacuum-Cleaner-Ultraosinc-Sensor-Transducer.html

| Parameter | Value | Notes |
|-----------|-------|-------|
| Model | HT-300PLTR1612-1 | HTW (Chengdu Huitong West-Electronic) |
| Working mode | Transceiver | Single element Tx/Rx |
| Nominal frequency | 290 ± 15 kHz | Listed as "300kHz" in BOM |
| Diameter | 16mm | |
| Height | 12mm | |
| Directivity | ≤ 12° | Narrow beam, focused downward |
| Capacitance | 1300pF ± 20% | |
| Target distance | 30mm | Distance to floor surface |
| Precision | ≤ 2mm | Surface detection resolution |
| Housing material | PC (polycarbonate) | |
| Probe type | Dual probe | Tx and Rx elements |
| Detection mode | Echo reflection | Bounce echo off floor surface |
| IP rating | IP67 | Waterproof |
| Working temperature | 0°C to 80°C | |
| Working humidity | ≤ 90% RH | |
| Certification | RoHS | |
| Production process | Ceramics | Piezo ceramic element |
| Wire length | 60mm | |
| Price (20-199 pcs) | $6.00/pc | Matches BOM $6–12 range |
| Price (200-1999 pcs) | $5.00/pc | |
| Price (2000-9999 pcs) | $4.00/pc | |
| HS Code | 9031809090 | |

### 2.2 Product Variants

HTW offers four variants of the 300kHz floor material recognition sensor:

| Model | Output Type | PCBA Embedded | Algorithm Pre-installed | Description |
|-------|------------|---------------|------------------------|-------------|
| HT-300PLT1612 | Analog signal | No | No | Cheapest; R&D in algorithm needed — bare transducer |
| HT-300PLT-A | Analog signal | Yes | No | Signal amplified and filtered; R&D in algorithm still needed |
| HT-300PLT-M | Digital (COM) | Yes | Yes | Time-saving; set threshold values for different floor materials |
| HT-300PLT-MIR | Digital (COM + I/O) | Yes | Yes | Default I/O mode directly outputs hard/soft floor result; switchable to COM for custom thresholds |

**For oomwoo:** The HT-300PLT-MIR variant is the most practical — it provides a direct digital I/O output indicating hard floor vs. soft floor (carpet), requiring no algorithm development. The bare transducer (HT-300PLT1612) requires significant DSP work to process echo signatures.

### 2.3 How Ultrasonic Carpet Recognition Works

The sensor mounts on the robot's underside, pointing downward at the floor surface (~30mm distance). The piezo ceramic element emits a 290kHz ultrasonic pulse and receives the echo:

- **Hard floor (tile, wood, laminate):** Strong, sharp specular reflection — high amplitude, short decay
- **Carpet (soft, absorbent):** Diffuse, attenuated reflection — lower amplitude, longer decay

The echo signature (amplitude, decay time, frequency shift) is analyzed to classify the surface. The HT-300PLT-MIR variant has this algorithm pre-installed and outputs a simple digital signal.

### 2.4 OEM Roborock Carpet Sensor Module

**Source:** AliExpress listing for Roborock original ultrasonic carpet recognition module
**URL:** https://www.aliexpress.com/i/1005007785301618.html

| Parameter | Value |
|-----------|-------|
| Compatibility | Roborock S8 Pro Ultra, S7 Max Ultra, Q Revo, S7 MaxV, S7 Pro |
| Price | $6.93 (sale) / $19.24 (list) |
| Type | Ultrasonic probe (replacement part) |
| Availability | Retail (AliExpress) |

The Roborock S7 and later models feature "Ultrasonic Carpet Recognition" — confirmed on S7, S7 MaxV, S7 Max Ultra, S8, S8+, S8 Pro Ultra, and Q Revo per Roborock's official product pages and forum. The replacement module is the same class of 300kHz transducer described above.

**BOM note:** "Low availability retail" — the BOM advises purchasing factory direct. The HTW listing (Made-in-China) provides direct manufacturer access at $3–6/pc depending on quantity.

---

## 3. Summary Table

| Component | BOM Item | Key Part | Price | Status |
|-----------|----------|----------|-------|--------|
| Wall sensor (IR proximity) | Custom PCB, $5–10 | Vishay TSOP38238 + 940nm IR LED (TSAL6100 or similar) | $5–10 | ✅ Specs found |
| Carpet sensor (ultrasonic) | Ultrasonic 300kHz, $6–12 | HTW HT-300PLTR1612-1 (or Roborock OEM module) | $3–7 (factory) / $6.93 (retail) | ✅ Specs found |

---

## 4. Sources

1. **Vishay TSOP38238 datasheet** — https://www.vishay.com/docs/82491/tsop382.pdf (Rev 2.1, 27-May-2025)
2. **Vishay TSAL6100 940nm IR LED datasheet** — https://www.vishay.com/docs/81009/tsal6100.pdf (Rev 1.8)
3. **HTW 300kHz carpet sensor (Made-in-China)** — https://htwsensor.en.made-in-china.com/product/xfUrtLydvQhb/ (Chengdu Huitong West-Electronic Co., Ltd.)
4. **Roborock OEM ultrasonic carpet recognition module (AliExpress)** — https://www.aliexpress.com/i/1005007785301618.html
5. **Roborock S7 product page (Ultrasonic Carpet Recognition)** — https://us.roborock.com/pages/roborock-s7
6. **oomwoo BOM.md** — upstream commits `2a71e64` (wall sensor) and `91476ba` (carpet sensor), Jul 15, 2026
7. **DigiKey TSOP38238** — https://www.digikey.com/en/products/detail/vishay-semiconductor-opto-division/TSOP38238/1681362
8. **Adafruit TSOP38238** — https://www.adafruit.com/product/157

---

*Compiled: 2026-07-15 by OsakaTX (autonomous contributor, part-specs module)*
