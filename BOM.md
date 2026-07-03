# Bill of Materials (work in progress)

First working BoM is targeted for **mid-July '26**

A final, fully-costed BoM is targeted for **end of August '26**

Blog post - how I'm making this BOM [How-to: Source BOM for OOMWOO Open-Source Vacuum Robot](https://makerspet.com/blog/how-to-source-bom-for-oomwoo-open-source-vacuum-robot/)

Rationale in [docs/design-document.md](docs/design-document.md).

---

## Budget target

~$200 in sourced parts + a Raspberry Pi 5 (4 GB), aiming at the capability of a
mid-range ($500–600) commercial vacuum with mopping, possibly premium obstacle detection (ToF +
color camera + an NPU accelerator).

## Robot BoM (work in progress)

Retail / low-qty prices, INCLUDES shipping, excludes tax.

| Item | Qty | ~USD | Notes | Source |
|---|---|---|---|---|
| Drive wheel assembly pair | 1 | $24-$33 | Motor + encoder + suspension + tire + cables + wheel-drop sensors | Roborock S4/5/45/50/51/52/55 Max, S7/Pro/MaxV, E4/E5/45/50/55, G10, T7S/S+, S6/60/65 Pure/MaxV, S70/75, Q5/7 [search AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-maxv-wheels.html) |
| Caster wheel | 1 | $2.50-$5 | Push-in | iRobot Roomba I3/4/6/8, J7/Plus J7 E5/6 500 600 700 800 900 [search AliExpress](https://www.aliexpress.us/w/wholesale-roomba-caster.html) |
| Suction fan | 1 | $10–23 | 6 kPa option | Dreame MSD-C-3, Nidec 20N709U020; fits Dreame L10s Prime/Pro, **L10s Ultra Gen 1** (5.3 kPa — Gen 2 is 10 kPa!), D10s Plus, X10+ (6 kPa); X20+ verify (~7 kPa?) [search AliExpress](https://www.aliexpress.us/w/wholesale-Dreame-L10s-fan.html) |
|             |   | $17–28 | 5.1-6 kPa option | Nidec 22N704W150, 20N704S980, 20N704R980L; fits Roborock S8 Pro Ultra, S7 MaxV (5.1 kPa), S8/S8+/S8 Plus (6 kPa); G20 (Q7 Max/Max+ excluded — they're 4.2 kPa, not 5-6) [search AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s8-pro-fan.html) |
|             |   | $12–24 | 10 kPa option | Roborock BL24131616; Nidec 22N704V160; fits Roborock S8 MaxV Ultra (10 kPa); G20S [search AliExpress](https://www.aliexpress.us/w/wholesale-roborock-g20s-fan.html) |
|             |   | $34–45 | 36 kPa option | Roborock Saros 20 [search AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-Saros-20-fan.html) |
|             |   | $12–25 | 2-2.5 kPa option | Nidec 20N704P200, 20N704R500, 20N704R310, 20N704P160; Xiaomi Roborock S50 S51 S55 S60 S61 S65 S5 MAX S6 E25 E35, S5, S6 Pure [search AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-fan.html) |
| Main brush | 1 | $5-$8 | Single roller, rubber and bristles | Fits Roborock S4, S4 Max, S5, S5 Max, S50/S55, S6, S6 Pure/MaxV, S60/S65, E2,E3,E4,E5, E20,E25,E35, C10, Xiaomi Mijia [search AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-brush.html) |
|            |   | $8-$12 | Anti-tangle dual roller, rubber only | Fits Roborock S8 MaxV Ultra, G20S V20, P10S Pro/Pro Plus [search AliExpress](https://www.aliexpress.us/w/wholesale-roborock-G20S-v20-brush.html) |
|            |   | $3-$5 | Single roller, rubber only | Fits Roborock S7, S70, S7+/MaxV/MaxV Plus/MaxV Ultra/Pro, Q Revo/Pro/Plus, Q5, Q5+, Q7, Q7 Max, QV 35S, T7S, T7S Plus [search AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-S7-main-brush.html) |
|            |   | $5-$10 | Anti-tangle split single roller, rubber and bristles | Fits Roborock Saros 10/10R, Saros 20, Saros 20 Sonic, S10 MaxV Ultra, S9 MaxV/MaxV Ultra, QRevo 5AE/Edge/Edge C/Edge S5A/5V1/X/Edge T/Curv/S5V/Curv S5X/P20 Pro [search AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-saros-10-main-brush.html) |
|            |   | $20-$30 | Anti-tangle hair-cutting dual roller, rubber and bristles | Fits Dreame L40s Ultra, L40 Ultra, X40, X40 Ultra, X30 Ultra, L30 Ultra, L20 Ultra, L10s Ultra/Ultra Gen 2/Pro Ultra, S10 Pro, S20, S20 Pro/Pro Plus, X10, X10+, X20 Pro, D9 Max Gen2; Mova E30 Ultra, S10 Plus, P10 Pro Ultra; Xiaomi S10+, X20 Pro, X10+, Mijia M30S/M40 [search AliExpress](https://www.aliexpress.us/w/wholesale-dreame-tricut-brush.html) |
|            |   | $7-$10 | Anti-tangle tapered dual roller, rubber and bristles | Fits Dreame X60 Max, X50 Ultra/Master/Pro Ultra, L40S Pro Ultra/Ultra; MOVA V50 Ultra [search AliExpress](https://www.aliexpress.us/w/wholesale-dreame-x50-ultra-main-brush.html) |
|            |   | $7-$10 | Anti-tangle dual roller, rubber only + rubber and bristles options| Fits Roborock Roborock S8, S8+/Pro Ultra, Q5 Pro/Pro+, Q8 Max/Max+, G20 [search AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-Q8-Max-main-brush.html) |
| Main brush motor, gearbox | 1 | TBD | TBD | |
| Side brush + motor | 1–2 | 3–8 | fixed (extendable is later) | |
| Mop spin motor(s) + pads | 1–2 | 6–15 | mopping models only | |
| Water pump + valve + tubing | 1 | 4–10 | mopping models only | |
| Mop lift servo | 1 | 2–6 | mopping models only | |
| Battery pack (~14.8 V Li-ion) + BMS | 1 | 15–30 | **safety review** | |
| LiDAR (3irobotix CRL-200S / LDS) | 1 | 30–40 | | |
| VL53L7CX multizone ToF | 1 | 8–15 | obstacle detection (90° FoV) | |
| Color camera | 1 | 5–15 | connects to the SBC | |
| IMU | 1 | 2–5 | | |
| IR cliff / proximity sensors | 3–4 | 3–8 | | |
| Bumper micro-switches | 2–3 | 1–3 | | |
| Ultrasonic carpet sensor | 1 | 2–5 | | |
| Speaker + amp, mic, LEDs, buttons | — | 3–8 | | |
| Custom I/O PCB (JLCPCB assembled, low qty) | 1 | 15–40 | STM32 + motor drivers + sensor front-ends | |
| Wiring, connectors, fasteners, magnets, gaskets, filter | — | 12–25 | | |
| Printed parts (filament) | — | 5–15 | you print these yourself | |
| **Robot subtotal (sourced parts)** | | **~$130–270** | excludes SBC | |
| Raspberry Pi 5 (4 GB) | 1 | ~60 | the SBC | |

> **⚠️ Fan sourcing caveat:** the **kPa is the fan's own rating** — verify it against the fan's
> model number / datasheet. The vacuum models are a **sourcing search aid only**: a fan listed
> as "fits vacuum X" is *not* necessarily X's original fan (lower-power replacements are sold as
> compatible for higher-suction models). Omit any model whose known suction contradicts the row.

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
