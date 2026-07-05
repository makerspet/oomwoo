# Part Specs — Compiled Datasheets & Specifications

> **Contributor:** OsakaTX
> **Status:** Updated July 7, 2026 — encoder, gearbox, caster, connector findings consolidated from merged PRs, codetiger/VacuumTiger firmware analysis, and verified calibrations
> **Methodology:** Web research from manufacturer datasheets, public SDKs, open-source reverse-engineering projects (codetiger/VacuumTiger, codetiger/VacuumRobot), physical inspection data from merged contributor PRs (Scowt PR #13), Aliexpress listings, and VacuumTiger firmware empirical calibration
>
> 👉 **See the companion file for detailed methodology, derivation, and cross-referencing:**
> [`vacuumtiger-verified-specs.md`](vacuumtiger-verified-specs.md)

This document compiles the electrical and mechanical specifications found for key BOM
parts. Each section covers what was found and what is still missing.

---

## 1. Drive Wheel Assembly (Roborock S-family)

### Part Identification

The Roborock S4/S5/S5-Max/S6/S7-family drive wheel module is a complete unit:
gearmotor + incremental encoder + rubber tire + suspension + wheel-drop switch.
See BOM.md for the full Aliexpress search links.

### Motor Specs (Nidec 20N704RC70 — "Motor for Wheel")

Sourced from the [Nidec Robot Cleaner Motor catalog PDF](https://file.eleecans.com/web1/M00/CC/89/o4YBAF-ZOBKAQBvyADDMAglsvTw020.pdf):

| Parameter | Value |
|---|---|
| **Rated voltage** | 14.4 V |
| **No-load speed** | 16,800 rpm |
| **No-load current** | 0.4 A |
| **Rated speed** | 13,200 rpm |
| **Rated current** | 1.4 A |
| **Maximum power** | 13.8 W |
| **Noise (SPL)** | 45 dB(A) |
| **Status** | ⚠️ "In development" per Nidec catalog — model may have changed in production |

**Note:** The actual motor used in production Roborock wheels may differ from the
catalog entry above. The wheel module includes a **gearbox** (see estimated ratio below)
that reduces this to the final wheel RPM. The encoder is mounted after the gearbox.

### Wheel Dimensions (from PR #10 — alvarosamudio's URDF, merged)

| Dimension | Value |
|---|---|
| **Wheel diameter** | 0.065 m (65 mm) |
| **Robot body diameter** | 0.33 m (330 mm) |

### Encoder

- **Type:** **Single-channel Hall-effect sensor** (pulse output) — confirmed via physical inspection by Scowt PR #13 (merged). The wheel-side 7-pin JST connector has exactly **one** encoder signal wire (blue), plus 5V (orange) and GND (brown). This is NOT a quadrature A/B encoder.
- **GD32 decoding:** The GD32F103VCT6 hardware timer performs **4× edge counting** on the single pulse train (rising + falling edges × 2 timer channels), producing effective 4× resolution.
- **Effective ticks/rev (wheel shaft):** **~911 ticks/rev** — derived from the calibrated `ticks_per_meter = 4464.0` (VacuumTiger firmware, confirmed in `encoder_sim.rs` unit test) and wheel circumference = π × 0.065 m ≈ 0.2042 m. Calculation: 4464 ticks/m × 0.2042 m/rev ≈ 911 ticks/rev.
- **PPR:** **~228 PPR** (raw encoder pulses per wheel revolution) — 911 / 4 = ~228. Consistent with a multi-pole magnetic ring encoder using ~32 poles (common standard).
- **Directional ambiguity:** The single-channel encoder alone cannot determine rotation direction. Direction is resolved by the **IMU gyro** in the navigation pipeline (VacuumTiger dhruva-slam).
- **Data format:** u16 LE wrapping counter at offsets 0x10 (left wheel) / 0x18 (right wheel) in the 96-byte GD32 status packet, streamed at 110 Hz. Confirmed from codetiger/VacuumTiger `sangam-io/src/devices/crl200s/gd32/reader.rs` and `SENSORSTATUS.md`.
- **Calibrated odometry:** `ticks_per_meter = 4464.0`, `wheel_base = 0.233 m` — empirically calibrated on real hardware and confirmed in multiple VacuumTiger source files: `sangam-io/src/devices/mock/config.rs`, `dhruva-nav/dhruva.toml`, `dhruva-slam/src/sensors/odometry/wheel_odometry.rs`, and `dhruva-nav/src/odometry.rs`.

### Gearbox Ratio

- **Estimated ratio:** **~190:1** — derived from `VELOCITY_TO_DEVICE_UNITS = 523.0` (empirically calibrated in VacuumTiger `commands.rs`) and the verified max linear speed of 0.3 m/s. At 16,800 rpm no-load motor speed with 0.065 m wheels, a ~190:1 reduction produces a max wheel speed consistent with 0.3 m/s. Confirmed consistent with the calibrated ticks/m and 911 ticks/rev at the wheel shaft.
- **Physical verification:** ❌ **Not yet confirmed via tooth counting** — requires disassembly.

### Connectors

#### Wheel Module Connector (7-pin JST, cable side)

Confirmed by Scowt PR #13 physical inspection (merged):

| Pin | Wire Color | Function |
|-----|-----------|----------|
| 1 | Grey | Limit switch (wheel-drop, NC) |
| 2 | Grey | Limit switch (wheel-drop, common) |
| 3 | Orange | Encoder VCC (+5V) |
| 4 | Blue | Encoder signal (single-channel pulse) |
| 5 | Brown | Encoder GND |
| 6 | Black | Motor power (-) |
| 7 | Red | Motor power (+) |

**Cable length:** ~250 mm (per Scowt observation).

#### Mainboard Connectors (J25/J26 — 16-pin SHD 1.0mm)

Motor power is on **separate connectors** (J24 left / J27 right, 2-pin PH 2.0mm) — NOT carried by J25/J26.

**J25 (bottom, left wheel):** Left wheel encoder (3 wires) + Dustbox power + Left cliff sensor + Left bumper
**J26 (top, right wheel):** Right wheel encoder (3 wires) + Sweeper motor power + Right cliff sensor + Right bumper

Per codetiger/VacuumRobot reverse-engineering. **Full per-pin map** requires PCB continuity tracing (multimeter). The signal groups above are established; the exact pin-to-signal assignment within each group is hypothesis.

### Motor Driver IC

- **IC:** **TMI8870** (TOLL Microelectronic) — top mark "T8870", ESOP8 package
- **Specs:** Single H-bridge, 3.6A peak, 6.8-45V, PWM with integrated current regulation
- **Pin-compatible:** With TI DRV8870
- **Confirmed via:** TMI8870 datasheet (taoic.oss-cn-hangzhou.aliyuncs.com) matching the "8870" marking on U25 on the motherboard (photographed in codetiger/VacuumRobot Component_Diagram.md)
- **Dual ICs:** Since TMI8870 is a single-channel H-bridge and the robot has two wheels, a second matching IC should exist on the motherboard (near J27 for the right wheel)

### Wheel Module Weight

- **Pair:** ~463g (0.463 kg shipped pair — AliExpress listing for original Roborock S6 wheel module)
- **Single:** ~230g (estimated from pair weight)

### What We Still Need

| Item | Status |
|---|---|
| Exact gearbox ratio via tooth counting | ❌ Needs disassembly |
| Full J25/J26 per-pin map | ❌ Needs PCB continuity tracing |
| Wheel-drop sensor exact model | ❌ Needs physical inspection |
| Cable length (exact) | ❌ Needs physical measurement |
| Motor driver IC location for right wheel | ❌ Needs PCB inspection |

### References

- [Nidec Robot Cleaner Motor Product Introduction PDF](https://file.elecfans.com/web1/M00/CC/89/o4YBAF-ZOBKAQBvyADDMAglsvTw020.pdf)
- [codetiger/VacuumRobot — Mainboard Component Diagram](https://github.com/codetiger/VacuumRobot/blob/main/Research/Motherboard/Component_Diagram.md)
- [codetiger/VacuumRobot — Connection Evidence](https://github.com/codetiger/VacuumRobot/blob/main/Research/Motherboard/Connection_Evidence.md)
- [codetiger/VacuumTiger — Custom firmware with verified calibration](https://github.com/codetiger/VacuumTiger)
- [Scowt PR #13 — Wheel module 7-pin connector physical inspection](https://github.com/makerspet/oomwoo/pull/13)
- [TMI8870 Motor Driver Datasheet](https://www.taoic.com/product/28.html)

---

## 2. Suction Fan / Blower

### Nidec 20N-series Blower Units (full assemblies)

From the [Nidec catalog PDF](https://file.elecfans.com/web1/M00/CC/89/o4YBAF-ZOBKAQBvyADDMAglsvTw020.pdf):

#### Standard Blower Units

| Parameter | 20N183L010 A | 20N704R310 / R500 | 20N704S310 | 22N709Q140 |
|---|---|---|---|---|
| Rated voltage | 12 V | 14.4 V | 14.4 V | 14.4 V |
| Rated speed | 15,000 rpm | 17,200 rpm | 15,100 rpm | 22,500 rpm |
| Rated current | 1.7 A | 2.2 A | 1.6 A | 4.5 A |
| Input power | 20 W | 31.7 W | 23 W | 64.8 W |
| Max static pressure | 1.8 kPa | 2.6 kPa | 3.0 kPa | 4.0 kPa |
| Max air volume | 0.63 m³/min | 0.78 m³/min | 0.63 m³/min | 0.99 m³/min |
| Noise | 67 dB(A) | 70 dB(A) | 68 dB(A) | 75 dB(A) |
| Fixing device | With | With | Without | Without |

#### Nidec BLDC Bare Motors (for Blower — without impeller housing)

| Parameter | 20N704K500 B | 20N704P110 A | 22N709P230 D | 35N048P010 |
|---|---|---|---|---|
| Rated voltage | 12 V | 13 V | 14.4 V | 18 V |
| No-load speed | 16,500 rpm | 23,000 rpm | 29,000 rpm | 28,800 rpm |
| No-load current | 0.4 A | 0.6 A | 0.6 A | 0.8 A |
| Rated speed | 13,500 rpm | 16,700 rpm | 24,800 rpm | 25,900 rpm |
| Rated current | 1.4 A | 1.75 A | 2.8 A | 7.1 A |
| Max power | 15.9 W | 21.2 W | 58.4 W | 74.6 W |
| Noise | 40 dB(A) | 50 dB(A) | 65 dB(A) | 60 dB(A) |

### Fan Control Interface (BLDC bare motors)

From the catalog, the Nidec Smart_20N series BLDC motors support:

| Feature | Details |
|---|---|
| **Control** | PWM input for speed control |
| **Feedback** | FG (frequency generator / tachometer) output |
| **Special** | 22N709P230 D additionally has SS (soft-start) |
| **Drive** | 3-phase BLDC — requires external driver/controller |
| **Voltage range** | 5–24 V (Smart_20N series datasheet) |
| **Mass** | 25–30 g (bare motor) |

### Driving the Fans

- The open-source [ripinteer/fan_protector](https://github.com/ripinteer/fan_protector) project is a reference for driving/protecting these BLDC blowers
- The [jniebuhr/roborock-pcb](https://github.com/jniebuhr/roborock-pcb) project has a custom PCB for driving Roborock fans (Nidec-based), including connector pinout
- Connector on the Roborock CPAP board: JST XH 3-pin 2.54mm for motor, JST XH 2-pin 2.54mm for fan

### What We Still Need

| Item | Status |
|---|---|
| Full suction-assembly-level datasheet (including impeller housing) | ❌ Missing (we have bare motor specs) |
| Specific connector model + pinout for each assembly variant | ❌ Unknown |
| Cable length(s) | ❌ Unknown |
| Signal waveforms (PWM, FG) | ❌ Unknown |
| Weight of full assembly | ❌ Unknown |

### References

- [Nidec Robot Cleaner Motor PD](https://file.elecfans.com/web1/M00/CC/89/o4YBAF-ZOBKAQBvyADDMAglsvTw020.pdf)
- [Nidec Smart_20N series product page](https://www.nidec.com/en/product/search/category/B101/M102/S100/NCJ-20N-Type-3/)
- [jniebuhr/roborock-pcb — custom PCB with pinout](https://github.com/jniebuhr/roborock-pcb)
- [ripinteer/fan_protector — BLDC driver reference](https://github.com/ripinteer/fan_protector)

---

## 3. LiDAR — 3irobotix CRL-200S / Delta-2D

### Basic Specs

| Parameter | Value |
|---|---|
| **Model** | 3irobotix CRL-200S (same platform as Delta-2D) |
| **Type** | Laser triangulation (not ToF) |
| **Range** | 0.13–8 m @ 100% reflectivity |
| **Accuracy** | < 1% @ 5m |
| **Scan rate** | 4–10 Hz (configurable via motor voltage) |
| **Points/sec** | 2–5 KHz |
| **Wavelength** | 780 nm |
| **Laser class** | Class 1 |
| **Max ambient** | 1K lux |
| **Weight** | ~175 g |
| **Retail** | ~$28–40 |
| **Life** | Estimated 1,500+ hours |
| **Power** | 0.35A idle, 0.37A ranging @ 5V (~1.75 W) + motor ~0.1A |

### Interface

| Parameter | Value |
|---|---|
| **Connector** | JST PH 2.0mm 5-pin |
| **Data** | UART 115200 baud, 8N1 |
| **Protocol** | Proprietary 3irobotix — 8-byte header + variable payload |
| **Commands** | 0xAE (health), 0xAD (measurement data) |
| **Distance multiplier** | 0.25 mm per LSB |

#### Pinout (J17 on 3irobotix CRL-200S mainboard)

| Pin | Function | Direction | Notes |
|---|---|---|---|
| 1 | Motor+ | Power | 5V for rotation |
| 2 | Motor- | Power | GND |
| 3 | TX | Output | LiDAR → MCU (UART RX) |
| 4 | RX | Input | MCU → LiDAR (UART TX) |
| 5 | GND | Power | Ground |

### Motor Control

| Parameter | Value |
|---|---|
| **Motor voltage range** | 2.2–3.8 V (for valid ranging) |
| **RPM range** | ~240–420 RPM |
| **Motor drive** | Direct voltage control (external) or H-bridge / PWM |
| **Ranging fails below** | ~2.2 V motor (below 240 RPM) |
| **Ranging fails above** | ~4.0 V motor (above 460 RPM) |
| **Angular resolution** | 0.77° at 240 RPM → 1.41° at 420 RPM |

### Data Format (from notblackmagic.com reverse engineering)

Start byte `0xAA`, followed by:
- 2-byte packet type
- Data length
- Angle + distance pairs (each 2 bytes)
- Checksum byte

### References

- [kaiaai/awesome-2d-lidars — comparison table & pinout](https://github.com/kaiaai/awesome-2d-lidars)
- [kaiaai/LDS — Arduino LiDAR library supporting CRL-200S / Delta-2D](https://github.com/kaiaai/LDS)
- [notblackmagic.com — full reverse engineering of Delta-2G (same protocol)](https://notblackmagic.com/bitsnpieces/lidar-modules/)
- [codetiger/VacuumRobot — LiDAR protocol decoding](https://github.com/codetiger/VacuumRobot)
- [3irobotix Delta-2B SDK](https://github.com/CWRU-AutonomousVehiclesLab/Delta-2B-Lidar-SDK)
- Delta-1A protocol doc (shared with 2A/2B/2G/2D): see notblackmagic.com above

---

## 4. VL53L7CX — Multizone Time-of-Flight Sensor

### Basic Specs

| Parameter | Value |
|---|---|
| **Type** | Time-of-Flight, 8×8 multizone (64 zones) |
| **Field of View** | 90° diagonal (65° × 65° typical) |
| **Range** | Up to 350 cm (varies by target reflectivity and ambient) |
| **I²C address** | 0x52 (default) — configurable |
| **I²C speed** | Up to 1 MHz (fast mode+) |
| **Supply** | 2.8 V (AVDD), 1.8 V (IOVDD) or 2.8 V (optional) |
| **Package** | 4.4 × 2.4 × 1.0 mm (LGA-12) |

### Pinout

| Pin | Name | Function |
|---|---|---|
| 1 | AVDD | Power (2.8 V) |
| 2 | GND | Ground |
| 3 | GPIO1 | Interrupt output (programmable) |
| 4 | LPn | Low power mode control |
| 5 | I2C_RST | I²C interface reset (active high) |
| 6 | SCL | I²C clock |
| 7 | SDA | I²C data |
| 8 | IOVDD | I/O voltage (1.8 V or 2.8 V) |

### Interface

- **I²C** up to 1 MHz
- Requires external pull-up resistors on SCL/SDA
- Interrupt pin (GPIO1) for data-ready signaling
- LPn pin for low-power mode control

### References

- [ST VL53L7CX Datasheet](https://www.st.com/resource/en/datasheet/vl53l7cx.pdf)
- [STM32duino VL53L7CX Arduino library](https://github.com/stm32duino/VL53L7CX)
- [UM3038 — User guide for using VL53L7CX](https://www.pololu.com/file/0J1993/um3038-a-guide-to-using-the-vl53l7cx-timeofflight-multizone-ranging-sensor-with-90-fov-stmicroelectronics.pdf)

---

## 5. IMU — MPU-6050 (common choice, architecture TBD)

### Basic Specs

| Parameter | Value |
|---|---|
| **Type** | 6-axis (3-axis gyro + 3-axis accelerometer) |
| **Gyro range** | ±250, ±500, ±1000, ±2000 °/s (programmable) |
| **Accel range** | ±2g, ±4g, ±8g, ±16g (programmable) |
| **I²C address** | 0x68 (AD0 low) or 0x69 (AD0 high) |
| **I²C speed** | Up to 400 kHz |
| **Supply** | 2.375–3.46 V |
| **Package** | 4×4×0.9 mm QFN-24 |

### Pinout (QFN-24)

| Pin | Name | Function |
|---|---|---|
| 8 | SCL | I²C clock |
| 9 | SDA | I²C data |
| 12 | AD0 | I²C address select |
| 20 | INT | Interrupt output |
| 6 | VDD | Power (2.4–3.5 V) |
| 18 | VLOGIC | Logic reference (1.8V±5% or VDD) |
| 7, 10, 13, 19, 21 | GND | Ground |

### References

- [MPU-6000/6050 Register Map & Descriptions](https://cdn.sparkfun.com/datasheets/Sensors/Accelerometers/RM-MPU-6000A.pdf)
- [MPU-6050 Product Specification v3.4](https://www.cdiweb.com/datasheets/invensense/mpu-6050_datasheet_v3%204.pdf)

---

## 6. IR Cliff / Proximity Sensors — TCRT5000 (typical)

### Basic Specs

| Parameter | Value |
|---|---|
| **Type** | Reflective optical sensor (IR LED + phototransistor) |
| **Operating voltage** | LED: 1.2–1.5 V forward (typical), Phototransistor: up to 30 V |
| **Detection range** | 0.2–15 mm (for reliable cliff detection) |
| **Output** | Phototransistor collector (open collector — needs pull-up resistor) |
| **Package** | 4-pin DIP (standard leaded package) |

### Pinout

| Pin | Name | Function |
|---|---|---|
| 1 | A (Anode) | IR LED anode |
| 2 | C (Cathode) | IR LED cathode |
| 3 | C (Collector) | Phototransistor collector (output) |
| 4 | E (Emitter) | Phototransistor emitter (GND) |

### Typical Circuit

- IR LED: driven through a current-limiting resistor (e.g., 100–220 Ω at 3.3–5 V)
- Phototransistor: collector pulled up to MCU voltage (3.3 V) via a 10–47 kΩ resistor
- Output read as analog voltage (ADC) or digital threshold (comparator)

### References

- [TCRT5000 datasheet (components101)](https://components101.com/sensors/tcrt5000-ir-sensor-pinout-datasheet)
- [TCRT5000 guide (Utmel)](https://www.utmel.com/components/tcrt5000-ir-sensor-datasheet-pinout-and-circuit?id=697)

---

## 7. Caster Wheel

**⚠️ BOM specifies a Roomba-style caster** (iRobot part #4624869, $2.50-$5 push-in ball-type). The Roborock S-family caster (50mm wheel-type, OEM #9.01.1272/1273) is a different part — verify which is selected before designing the mount.

### Roomba Caster (BOM Source)

| Spec | Value |
|---|---|
| Part number | iRobot 4624869 / RM500CSA |
| Type | Snap-in ball-type caster |
| Wheel diameter | ~25mm |
| Weight | ~30g (plastic) to ~61g (metal+plastic variant) |
| Mounting | Push-in snap-fit |
| Sensor | None (passive) |
| Compatible with | Roomba i3/4/6/8/J7/e5/6/500-900 series |
| Price | $2.50–$12.95 |
| Availability | Abundant (iRobot official, Amazon, aftermarket) |

### Roborock S-family Caster (Alternative / Other BOM Variant)

| Spec | Value |
|---|---|
| OEM part numbers | 9.01.1272 (white) / 9.01.1273 (black) — confirmed via TechPunt.nl, Roborock India |
| Type | Wheel-type caster |
| Wheel height | ~50mm |
| Base diameter | ~45mm |
| Weight | ~45–70g |
| Mounting | Clip-in/pop-in (older models) or bolted-on screw bracket (S5 Max, S6 MaxV, E4+) |
| Sensor | None (passive) |
| Price | $4–17 |

### References

- [TechPunt.nl — OEM part listing](https://www.techpunt.nl/en/robotic-vacuums/robotic-vacuum-parts/20-c2109-roborock-original-spare-parts_141225)
- [Roborock India — OEM parts](https://www.roborockindia.in/)
- [iRobot official store — part 4624869](https://store.irobot.com/)
- [Thingiverse — Roomba caster 3D printable models](https://www.thingiverse.com/)
- [Printables — Roborock caster bracket model (Uko, Jan 2021)](https://www.printables.com/)

---

## Summary of Found vs Missing

| Part | Documentation Found | Critical Gaps |
|---|---|---|
| **Drive wheel** | Motor electrical specs (Nidec 20N704RC70), wheel diameter (65mm), encoder type (single-channel Hall, ~228 PPR), gearbox ratio (~190:1), ticks/meter (4464), wheel module connector (7-pin JST with wire colors), mainboard connectors (J25/J26 16-pin SHD signal groups, J24/J27 2-pin PH motor power), motor driver IC (TMI8870), module weight (~463g pair) | ❌ Exact gearbox ratio via tooth count, ❌ full J25/J26 per-pin map, ❌ wheel-drop sensor model |
| **Suction fan** | Complete Nidec catalog specs for many models, PWM/FG control, connector types (JST XH) | ❌ Impeller housing geometry, ❌ assembly weight, ❌ cable lengths |
| **LiDAR (CRL-200S)** | ✅ Full specs, pinout, protocol, RPM/voltage relationship, power consumption | Minor: exact motor model inside, formal manufacturer datasheet |
| **VL53L7CX ToF** | ✅ Full datasheet, I²C interface, pinout, FOV, range | None — standard ST component |
| **IMU (MPU-6050)** | ✅ Full datasheet, I²C interface, pinout | None — standard InvenSense component |
| **IR cliff sensor** | ✅ TCRT5000 specs, circuit, pinout | None — standard sensor, subject to final BOM choice |
| **Caster wheel** | ✅ Roomba 4624869 specs (25mm ball-type, push-in); Roborock 9.01.1272/1273 (50mm wheel-type); both passive | ❌ Exact dimensional drawing for chosen variant; ❌ which BOM variant is selected |
