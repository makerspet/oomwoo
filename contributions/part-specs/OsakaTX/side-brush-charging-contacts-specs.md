# Side Brush Motor, Side Brushes, and Charging Contacts — Part Specs

> **Compiled:** 2026-07-16  
> **Sources:** BOM.md (upstream commits 5977b86, 61a6063, 37f0bdc), codetiger/VacuumTiger firmware source, iFixit repair guide, particleflux.codes teardown, Reddit r/Roborock teardown, AliExpress listings, SUNMON/Alibaba pogo pin guides  
> **Status:** Awaiting user review — no PR created

## Trigger

Upstream BOM.md added three new line items between Jul 14-16, 2026:
- `5977b86` "Sourced side brushes" (Jul 14)
- `61a6063` "Source side brush motor assembly" (Jul 14)
- `37f0bdc` "Sourced robot charging contacts" (Jul 16)

These are new 💻-researchable part-specs gaps. Wall sensor and carpet sensor (commits `2a71e64`, `91476ba`) were already addressed in branch `part-specs-wall-carpet-sensors-jul15`.

---

## 1. Side Brush Motor

### BOM Entry

| Type | Price | Compatibility | Notes |
|------|-------|---------------|-------|
| Fixed | $7-10 | Roborock S5, S50, S51, S52, S55, S502-00/01/02/03, S552-00, S5 Max, S6, S6 Pure, S6 MaxV, S60, S61, S65, S7, S7 MaxV, S7 Plus, S70, S75, Xiaowa/Xiaomi C10, E20, E25, E35 | Standard side brush motor |
| Extendable (FlexiArm) | $18-35 | Roborock Qrevo Master/Edge/Slim/Pro/S Pro, S8 MaxV Ultra, S8 Max Ultra, Q55 Pro, G20, G20S, V20 | Motorized extending arm |

### Motor Type — Verified by Physical Teardown

- **Type:** Brushed DC motor (confirmed by Reddit teardown — u/BinturongHoarder, Jan 2025)
  - Contains carbon brushes (coal dust found inside worn motor)
  - Sintered bronze self-lubricating bushings at both ends (not ball bearings)
  - Motor housing is not sealed; can be affected by dust ingress
  - Motor cannot be opened without destruction
  - The robot detects motor stalls via current sensing and shuts off the motor as a safety precaution
- **Construction:** Metal and PVC housing
- **Weight:** ~0.150 kg (Amazon listing for replacement motor, "Mytkoj" brand)

### Gearbox — Verified by Teardown

- **Type:** 2-stage reduction gearbox with plastic gears
  - Two white plastic gear wheels inside the gearbox housing
  - Contains grease
  - Gears and grease are generally reliable — motor failure is the common issue, not gears
- **Gear ratio:** Not directly published; AliExpress wiki claims 1:40 (S5/S5 Max), 1:45 (S6 Pure/MaxV), 1:50 (S7/MaxV) — **these values are from a retail wiki and unverified by manufacturer datasheet**
- **Mounting:** 3 screws hold gearbox assembly to chassis; 2 screws hold motor inside gearbox; motor has alignment nub fitting into 3rd hole at front

### Electrical Interface

- **Contact pads:** TP1 and TP2 on motor PCB (2-pad contact, simple DC +/−)
- **Connector:** 2-wire connection to mainboard (small JST-type connector per AliExpress wiki installation guide)
- **Operating voltage:** Not explicitly published; robot battery is 14.4V nominal (13.5-15.5V range per VacuumTiger constants). Side brush motor likely runs at battery voltage or a PWM-regulated lower voltage.
- **Speed control:** PWM via GD32 firmware

### Firmware Control (VacuumTiger — verified from source code)

- **Command:** `CMD_SIDE_BRUSH = 0x69` (confirmed in `constants.rs`)
- **Packet format:** 4-byte payload, data[4] = speed (u8, 0-100%)
- **Source:** `sangam-io/src/devices/crl200s/gd32/packet.rs` line 145: `pub fn set_side_brush(&mut self, speed: u8)`
- **Documentation:** `sangam-io/src/devices/crl200s/COMMANDS.md`: "0x69 | Side Brush | 1 byte | ✅ | 32x | HIGH | Working in SangamIO, matches AuxCtrl `packetBrushSpeed`"
- **Component ID:** `"side_brush"` in SangamIO component state (confirmed in `commands.rs` line 75)

### Compatibility

The side brush motor is shared across a wide range of Roborock models (S5 through S7 MaxV, plus Xiaomi C10/E20/E25/E35). The fixed-type motor is a standard replacement part available from $7-10. The FlexiArm extendable variant ($18-35) is a newer motorized design for premium models (Qrevo, S8 MaxV, G20S, V20) and is not directly interchangeable.

### Failure Mode (for reference)

Common failure: motor stops spinning during cleaning. Root cause is typically worn carbon brushes or seized sintered bronze bushings (not gear failure). The robot detects the stall via current sensing and disables the motor. Replacement is the standard fix — the motor is designed for easy swap (10-minute job, Phillips #2 screwdriver only).

---

## 2. Side Brushes

### BOM Entry

| Type | Price | Compatibility | Notes |
|------|-------|---------------|-------|
| 5-arm | $2-8 | Roborock S5, S50, S51, S55, S6, S60, S6 Pure | Standard 5-arm side brush |
| 3-arm | $3-9 | Roborock S8 and many other Roborock models | 3-arm design |
| 2-arm curved | $3-7 | Roborock Saros | Possibly fits many other models |

### Attachment

- Single Phillips #2 captive screw holds the side brush to the motor shaft
- Brush lifts off after unscrewing — no tools needed beyond screwdriver
- Side brush alignment matters: if not parallel to the wall, it drags and wears prematurely

---

## 3. Charging Contacts

### BOM Entry — Robot Side

| Spec | Value |
|------|-------|
| Quantity | 2 |
| Material | Nickel-plated steel strip |
| Dimensions | ~1mm wide, ~0.1mm thick, ~5cm long |
| Price | $1.50-2.50 |
| Source | Standard nickel strip (AliExpress/Amazon/eBay) |

### BOM Entry — Dock Side

| Spec | Value |
|------|-------|
| Quantity | 2 |
| Type | Gold-plated pogo pins |
| Current rating | 4A |
| Price | TODO (not yet priced in BOM) |

### Charging System Specifications

| Parameter | Value | Source |
|-----------|-------|--------|
| Dock power supply output | 20V DC, 1.2A (24W) | Amazon/AliExpress replacement adapter listings for Roborock S5 |
| Dock output at contacts | ~19.8-20V DC (when robot parked) | Reddit r/Roborock user measurement (Jun 2023) |
| Robot battery voltage | 13.5-15.5V (4S Li-ion) | VacuumTiger `constants.rs`: `BATTERY_VOLTAGE_MIN = 13.5`, `BATTERY_VOLTAGE_MAX = 15.5` |
| Nominal battery voltage | 14.4V (14.8V default in mock config) | VacuumTiger `mock/config.rs`: `default_battery_voltage() = 14.8` |
| Charging method | Contact-based (not inductive/wireless) | Standard for Roborock S-family |

### Firmware Charging Detection (VacuumTiger — verified from source code)

- **Charging flags offset:** `OFFSET_CHARGING_FLAGS = 0x07` (byte 7 in 96-byte status packet)
- **Flag bits:**
  - Bit 0 (`FLAG_DOCK_CONNECTED = 0x01`): 1 = robot is on the charging dock
  - Bit 1 (`FLAG_CHARGING = 0x02`): 1 = robot is actively charging
- **Battery voltage offset:** `OFFSET_BATTERY_VOLTAGE_RAW = 0x08` (byte 8, raw value / 10 = volts)
- **Charger power command:** `CMD_CHARGER_POWER = 0x9B` — 1 byte, Enable/Disable
- **Source:** `sangam-io/src/devices/crl200s/constants.rs`, `SENSORSTATUS.md`

### Charging Contact Design Notes

**Robot side (nickel-plated steel strip):**
- The robot uses flat spring-metal strips as charging contacts, not pogo pins
- Nickel plating provides corrosion resistance at low cost
- Strip dimensions (~1mm × 0.1mm × 5cm) are standard nickel strip stock — same material used for battery pack welding
- Spring force comes from the strip's own flex, not from a separate spring mechanism
- Contact resistance: nickel-plated contacts typically 30-50 mΩ — sufficient for 1.2A charging current

**Dock side (gold-plated pogo pins, 4A):**
- Gold plating (0.3-0.76 µm Au over Ni) ensures low contact resistance and corrosion resistance
- 4A rating provides >3× safety margin over the 1.2A charging current
- Pogo pin working stroke absorbs docking misalignment (typical: 1.5-3mm compression)
- Spring force typically 40-120 cN (40-120 gf) for robot vacuum applications
- Cycle life: 50,000-100,000+ mating cycles for quality pogo pins
- Cost: ~$0.22-0.30/unit (nickel-plated), +25-40% for gold-plated variants (at 5k qty)

**Design reference for oomwoo:**
- 2-pin configuration: V+ and GND (simplest charging, no data)
- Optional 3-4 pin: add dock detection or temperature sense
- Dock should use pogo pins (spring-loaded); robot should use flat pads (easier to clean, no debris ingress)
- Magnetic alignment optional but improves docking reliability

---

## 4. Main Brush Motor (context — already in BOM, added Jul 14)

### BOM Entry

| Type | Price | Compatibility | Notes |
|------|-------|---------------|-------|
| Main brush motor + gearbox | $7-11 | Roborock S5, S50, S51, S52, S55, S502, S552, S6; Xiaowa C10, E20, E25, E35 | Requires brush socket adapter |

### Firmware Control

- **Command:** `CMD_MAIN_BRUSH = 0x6A` (confirmed in `constants.rs`)
- **Packet format:** 4-byte payload, data[4] = speed (u8, 0-100%)
- **Source:** `sangam-io/src/devices/crl200s/gd32/packet.rs` line 134: `pub fn set_main_brush(&mut self, speed: u8)`
- **Documentation:** `COMMANDS.md`: "0x6A | Rolling Brush | 1 byte | ✅ | 32x | HIGH"
- **Component ID:** `"main_brush"` in SangamIO component state

---

## Source Verification Table

| Data Point | Source | URL/Path | Verification |
|------------|--------|----------|--------------|
| Side brush = brushed DC motor | Reddit teardown (u/BinturongHoarder, Jan 2025) | https://www.reddit.com/r/Roborock/comments/1hztkyw/just_pulled_apart_a_s5_side_brush_motor/ | Physical inspection — primary source |
| Gearbox = 2-stage plastic gears | iFixit guide + particleflux.codes teardown | https://www.ifixit.com/Guide/Roborock+S5+Series+Sidebrush+Motor+Replacement/181289, https://particleflux.codes/post/2025/roborock-s50-sidebrush-motor-replacement/ | Physical disassembly — primary source |
| Motor contact pads TP1/TP2 | particleflux.codes teardown | https://particleflux.codes/post/2025/roborock-s50-sidebrush-motor-replacement/ | Physical observation — primary source |
| CMD_SIDE_BRUSH = 0x69 | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` line 19 | Running firmware source — verified |
| Side brush speed = u8 0-100% | VacuumTiger source code | `sangam-io/src/devices/crl200s/gd32/packet.rs` line 141-149 | Running firmware source — verified |
| CMD_MAIN_BRUSH = 0x6A | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` line 20 | Running firmware source — verified |
| CMD_CHARGER_POWER = 0x9B | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` line 51 | Running firmware source — verified |
| Charging flags at offset 0x07 | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` line 62, `SENSORSTATUS.md` | Running firmware source — verified |
| FLAG_DOCK_CONNECTED = 0x01 | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` line 101 | Running firmware source — verified |
| FLAG_CHARGING = 0x02 | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` line 100 | Running firmware source — verified |
| Battery voltage 13.5-15.5V | VacuumTiger source code | `sangam-io/src/devices/crl200s/constants.rs` lines 96-97 | Running firmware source — verified |
| Dock output ~20V | Reddit user measurement + Amazon adapter listing | https://www.reddit.com/r/Roborock/comments/149zrv3/error_13_fixed/, Amazon S5 charger listing | Community measurement + retail spec |
| Dock adapter = 20V 1.2A 24W | Amazon/AliExpress replacement adapter listings | Amazon B0G5K2D84P, AliExpress 1005009410095092 | Retail product spec |
| Motor weight ~150g | Amazon listing | https://www.amazon.com/S51-S55-S4-S5-S6/dp/B0CF8L4RFM | Retail listing — secondary |
| Pogo pin 4A gold-plated specs | SUNMON guide + Alibaba guide | https://smeconn.com/how-to-choose-pogo-pin-connector-cleaning-robot-charging/, https://electronics.alibaba.com/buyingguides/spring-loaded-battery-contacts-a-practical-guide | Manufacturer guide — secondary |
| Gear ratio claims (1:40/1:45/1:50) | AliExpress wiki article | https://www.aliexpress.com/s/wiki-ssr/article/Roborock-S5-S6-S7-side-brush-motor | Retail wiki — **unverified, likely approximate** |

---

## Remaining Gaps

| Gap | Category | Notes |
|-----|----------|-------|
| Side brush motor exact voltage | 🔬 | Needs multimeter measurement on running robot or motor datasheet |
| Side brush motor RPM (no-load and under load) | 📡 | Needs tachometer or oscilloscope measurement |
| Gearbox ratio (exact tooth count) | ⚙️ | Needs disassembly and tooth count |
| Motor connector type (JST model/pitch) | 🔬 | Needs physical inspection of connector |
| Dock pogo pin model/part number | 🔬 | Needs physical inspection of dock |
| Dock-side charging contact pricing | 💻 | BOM lists as "TODO" — standard 4A gold pogo pins are ~$0.50-1.00/pair at retail |
| FlexiArm extendable motor specs | 💻 | Newer design, limited teardown data available |
