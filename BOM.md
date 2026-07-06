# Bill of Materials (work in progress)

First working BoM is targeted for *mid-July '26*

A final, fully-costed BoM is targeted for *end of August '26*

Blog post - how I'm making this BOM [How-to: Source BOM for OOMWOO Open-Source Vacuum Robot](https://makerspet.com/blog/how-to-source-bom-for-oomwoo-open-source-vacuum-robot/)

Rationale in [docs/design-document.md](docs/design-document.md).

---

## Budget target

~$200 in sourced parts + a Raspberry Pi 5 (4 GB), aiming at the capability of a
mid-range ($500–600) commercial vacuum with mopping, possibly premium obstacle detection (ToF +
color camera + an NPU accelerator).

## Robot BoM (work in progress)

Retail / low-qty prices, INCLUDES shipping, excludes tax. Read [how I calculate BoM costs](#how-i-calculate-costs).

| Item | Qty | ~USD | Notes | Source |
|---|---|---|---|---|
| Drive wheel assembly pair | 1 | $24-$33 | Motor + encoder + suspension + tire + cables + wheel-drop sensors | Roborock S4/5/45/50/51/52/55 Max, S7/Pro/MaxV, E4/E5/45/50/55, G10, T7S/S+, S6/60/65 Pure/MaxV, S70/75, Q5/7 [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-maxv-wheels.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+maxv+wheels) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+maxv+wheels) |
| Caster wheel | 1 | $2.50-$5 | Push-in | iRobot Roomba I3/4/6/8, J7/Plus J7 E5/6 500 600 700 800 900 [AliExpress](https://www.aliexpress.us/w/wholesale-roomba-caster.html) / [Amazon](https://www.amazon.com/s?k=roomba+caster) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roomba+caster) |
| Suction fan | 1 | $10–23 | 6 kPa option | Dreame MSD-C-3, Nidec 20N709U020; fits Dreame L10s Prime/Pro, *L10s Ultra Gen 1* (5.3 kPa — Gen 2 is 10 kPa!), D10s Plus, X10+ (6 kPa); X20+ verify (~7 kPa?) [AliExpress](https://www.aliexpress.us/w/wholesale-Dreame-L10s-fan.html) / [Amazon](https://www.amazon.com/s?k=Dreame+L10s+fan) / [eBay](https://www.ebay.com/sch/i.html?_nkw=Dreame+L10s+fan) |
|             |   | $17–28 | 5.1-6 kPa option | Nidec 22N704W150, 20N704S980, 20N704R980L; fits Roborock S8 Pro Ultra, S7 MaxV (5.1 kPa), S8/S8+/S8 Plus (6 kPa); G20 (Q7 Max/Max+ excluded — they're 4.2 kPa, not 5-6) [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s8-pro-fan.html) / [Amazon](https://www.amazon.com/s?k=roborock+s8+pro+fan) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s8+pro+fan) |
|             |   | $12–24 | 10 kPa option | Roborock BL24131616; Nidec 22N704V160; fits Roborock S8 MaxV Ultra (10 kPa); G20S [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-g20s-fan.html) / [Amazon](https://www.amazon.com/s?k=roborock+g20s+fan) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+g20s+fan) |
|             |   | $34–45 | 36 kPa option | Roborock Saros 20 [AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-Saros-20-fan.html) / [Amazon](https://www.amazon.com/s?k=Roborock+Saros+20+fan) / [eBay](https://www.ebay.com/sch/i.html?_nkw=Roborock+Saros+20+fan) |
|             |   | $12–25 | 2-2.5 kPa option | Nidec 20N704P200, 20N704R500, 20N704R310, 20N704P160; Xiaomi Roborock S50 S51 S55 S60 S61 S65 S5 MAX S6 E25 E35, S5, S6 Pure [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-fan.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+fan) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+fan) |
| Main brush | 1 | $5-$8 | Single roller, rubber and bristles | Fits Roborock S4, S4 Max, S5, S5 Max, S50/S55, S6, S6 Pure/MaxV, S60/S65, E2,E3,E4,E5, E20,E25,E35, C10, Xiaomi Mijia [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-brush.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+brush) |
|            |   | $8-$12 | Anti-tangle dual roller, rubber only | Fits Roborock S8 MaxV Ultra, G20S V20, P10S Pro/Pro Plus [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-G20S-v20-brush.html) / [Amazon](https://www.amazon.com/s?k=roborock+G20S+v20+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+G20S+v20+brush) |
|            |   | $3-$5 | Single roller, rubber only | Fits Roborock S7, S70, S7+/MaxV/MaxV Plus/MaxV Ultra/Pro, Q Revo/Pro/Plus, Q5, Q5+, Q7, Q7 Max, QV 35S, T7S, T7S Plus [AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-S7-main-brush.html) / [Amazon](https://www.amazon.com/s?k=Roborock+S7+main+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=Roborock+S7+main+brush) |
|            |   | $5-$10 | Anti-tangle split single roller, rubber and bristles | Fits Roborock Saros 10/10R, Saros 20, Saros 20 Sonic, S10 MaxV Ultra, S9 MaxV/MaxV Ultra, QRevo 5AE/Edge/Edge C/Edge S5A/5V1/X/Edge T/Curv/S5V/Curv S5X/P20 Pro [AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-saros-10-main-brush.html) / [Amazon](https://www.amazon.com/s?k=Roborock+saros+10+main+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=Roborock+saros+10+main+brush) |
|            |   | $20-$30 | Anti-tangle hair-cutting dual roller, rubber and bristles | Fits Dreame L40s Ultra, L40 Ultra, X40, X40 Ultra, X30 Ultra, L30 Ultra, L20 Ultra, L10s Ultra/Ultra Gen 2/Pro Ultra, S10 Pro, S20, S20 Pro/Pro Plus, X10, X10+, X20 Pro, D9 Max Gen2; Mova E30 Ultra, S10 Plus, P10 Pro Ultra; Xiaomi S10+, X20 Pro, X10+, Mijia M30S/M40 [AliExpress](https://www.aliexpress.us/w/wholesale-dreame-tricut-brush.html) / [Amazon](https://www.amazon.com/s?k=dreame+tricut+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=dreame+tricut+brush) |
|            |   | $7-$10 | Anti-tangle tapered dual roller, rubber and bristles | Fits Dreame X60 Max, X50 Ultra/Master/Pro Ultra, L40S Pro Ultra/Ultra; MOVA V50 Ultra [AliExpress](https://www.aliexpress.us/w/wholesale-dreame-x50-ultra-main-brush.html) / [Amazon](https://www.amazon.com/s?k=dreame+x50+ultra+main+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=dreame+x50+ultra+main+brush) |
|            |   | $7-$10 | Anti-tangle dual roller, rubber only + rubber and bristles options| Fits Roborock Roborock S8, S8+/Pro Ultra, Q5 Pro/Pro+, Q8 Max/Max+, G20 [AliExpress](https://www.aliexpress.us/w/wholesale-Roborock-Q8-Max-main-brush.html) / [Amazon](https://www.amazon.com/s?k=Roborock+Q8+Max+main+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=Roborock+Q8+Max+main+brush) |
| Battery pack + BMS | 1 | $16–30 | OEM BRR-2P4S-5200, 4S2P-MMBK P2150-4S2P-XWDLS; 14.4V Li-ion, ~5200 mAh / 75 Wh in-pack BMS. | Fits Xiaomi Mijia 1/1S/1C/1T/G1, Roborock S4/S5/S5 Max/S6/S6 Pure/MaxV/S7/S7 MaxV, Q5/Q7 Max, T4/T6/T7/T60/T65, Xiaowa E20/E25/E35, C10 [AliExpress](https://www.aliexpress.us/w/wholesale-BRR-2P4S-5200-battery.html) / [Amazon](https://www.amazon.com/s?k=BRR+2P4S+5200+battery) / [eBay](https://www.ebay.com/sch/i.html?_nkw=BRR+2P4S+5200+battery) 4-pin connector B+, B−, NTC, sense (TODO verify). Safety review narrows to: 16.8 V CC/CV charge + NTC temp sense. |
| 2D LiDAR  | 1 | $16-26 | PCB mark X-WPFTB-V2.6.2, possibly Camsense | Fits Dreame L10s/Pro/Ultra/Prime, L10 Ultra, L20 Pro/Ultra, L30 Ultra, W10s/Pro, W20,  Xiaomi X10+, X30s Pro, X30 Plus/Pro/Ultra, X20 Pro, X40/Pro/Pro Plus, X10/Plus, X20/Plus, S10/Pro/Plus/Ultra, S20+ |
|           |   | $16-27 | PCB mark X-Wireless board-V1.13.3, possibly Camsense | Fits Dreame W10, F9, D9, D9 Pro/Plus/max, L10 Pro, Z10 Pro [AliExpress](https://www.aliexpress.us/w/wholesale-Dreame-L10s-lds.html) / [Amazon](https://www.amazon.com/s?k=Dreame+L10s+lds) / [eBay](https://www.ebay.com/sch/i.html?_nkw=Dreame+L10s+lds) |
|           |   | $14-32 | Xiaomi LDS02RR, LDS01RR | Fits Roborock S5/S50/51/55/S6/S7, S502-00/01/02/03, S550-00, S5 Max, S6 MaxV/Pure, S45 Max, S7 Max, Xiaomi Mi 1s [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-lds.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+lds) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+lds) |
|           |   | $13-25 | 3irobotix Delta-2A/B/G | Fits Xiaomi Mijia Mop P Pro, Mop 2S, 3C S10, S12 T12 [AliExpress](https://www.aliexpress.us/w/wholesale-xiaomi-mop-lds.html) / [Amazon](https://www.amazon.com/s?k=xiaomi+mop+lds) / [eBay](https://www.ebay.com/sch/i.html?_nkw=xiaomi+mop+lds) |
|           |   | $13-23 | Possibly LDROBOT LD14P | Fits Dreame X30 X40 Series, Xiaomi Mijia X20 Plus, Mop2 [AliExpress](https://www.aliexpress.us/w/wholesale-dreame-x30-lds.html) / [Amazon](https://www.amazon.com/s?k=dreame+x30+lds) / [eBay](https://www.ebay.com/sch/i.html?_nkw=dreame+x30+lds) |
| Main brush motor, gearbox | 1 | TBD | TBD | |
| Side brush + motor | 1–2 | 3–8 | fixed (extendable is later) | |
| Mop spin motor(s) + pads | 1–2 | 6–15 | mopping models only | |
| Water pump + valve + tubing | 1 | 4–10 | mopping models only | |
| Mop lift servo | 1 | 2–6 | mopping models only | |
| VL53L7CX multizone ToF | 1 | 8–15 | obstacle detection (90° FoV) | |
| Color camera | 1 | 5–15 | connects to the SBC | |
| IR cliff / proximity sensors | 3–4 | 3–8 | | |
| Bumper micro-switches | 2–3 | 1–3 | | |
| Ultrasonic carpet sensor | 1 | 2–5 | | |
| Speaker + amp, mic, LEDs, buttons | — | 3–8 | | |
| Custom I/O PCB | 1 | 20–40 | STM32 + motor drivers + sensor front-ends | |
| Wiring, connectors, fasteners, magnets, gaskets, filter | — | 12–25 | | |
| Printed parts (filament) | — | 5–15 | you print these yourself | |
| *Robot subtotal (sourced parts)* | | *~$130–270* | excludes SBC | |
| Raspberry Pi 5 (4 GB) | 1 | ~60 | the SBC | |

> *Fan sourcing caveat:* the *kPa is the fan's own rating* — verify it against the fan's
> model number / datasheet. The vacuum models are a *sourcing search aid only*: a fan listed
> as "fits vacuum X" is *not* necessarily X's original fan (lower-power replacements are sold as
> compatible for higher-suction models). Omit any model whose known suction contradicts the row.

## Dock (by tier)

Three dock tiers share one robot base, released in order:

| Tier | Adds | Rough extra parts |
|---|---|---|
| Basic charge (first release) | charging only | printed housing + contacts/magnets + wall adapter + IR beacon |
| Auto-empty | dust auto-emptying | dock fan + bin/bag + sealed port |
| Auto-empty + wash + dry | mop wash + hot-air dry | clean + dirty tanks, 2 pumps, heater + fan, own ESP32 + WiFi controller |

## Sourcing strategy

- Print geometry, source mechanisms and wear items. See the print-vs-source table in
  [docs/design-document.md](docs/design-document.md#2-print-vs-source-strategy).
- Spec wear parts (brushes, filters, wheel modules) in *common, abundant sizes* so
  builders can buy cheap universal replacements anywhere.
- Per-module sourcing details will land in the relevant
  [contributions/](contributions) RFCs as they mature.

## How I calculate BoM costs

Prices for vacuum cleaner aftermarket parts have a wide spread (3x max/min as a ballpark).
You can buy same part for, say, $15 or $30 or even $45.

Therefore, if you search [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-lidar.html)/eBay/Amazon
for, say, "Roborock S5 LiDAR", you will likely see offers around $30.

There will probably several pages worth of those offers. And if you dig through those pages, you will probably start
finding parts for $25.

If you are shopping on AliExpress, open a part listing and check for free coupon offers like "$2.00 off on $18.00".
That brings your $25 price down to $23. Also, check the fine print in red font saying something like "$21.43 each, ≥ 3 pieces".

That's not the end of it. The next AliExpress trick is to wait for seasonal sales and promotions. Those happen relatively often.
Sales and promotions can bring prices down even futher.

How can you get to the rock-bottom $15 price? Aftermarket parts prices depend on your search keywords.
Try searching for multiple keyword variations: "Roborock S5 LDS", "Roborock S5 LiDAR", "original laser distance lds",
"LDS02RR", "LDS02RR LiDAR", "Roborock LDS02RR", "LDS laser sensor for xiaomi Roborock" and so on. Be creative and persistent.
Try searching Google "site:aliexpress.com lds02rr" and other variations. Be creative and persistent.

Combining all these methods is how you can get the rock bottom $15 price.

I record two prices for each part in the BoM table, for example "$15-$25".
The first ($15) price is the rock bottom one that often requires a minimum purchase of 3 pieces.
The second ($25) price is what you can realistically get when purchasing 1 piece, *applying coupons* and doing *a few minutes of search*.

Why record the first price if requires a 3 pcs minimum? This is because I intend to assemble a convenient parts kit - and make it available to everyone.

Hunting dozens of parts on AliExpress/Amazon/eBay can take be onerous. AliExpress shipping from China add a couple weeks more.

Getting an all-in-one kit, quickly shipped from the US, with parts that I've shopped, pre-screened/pre-tested for you - that's what I'd like to make.
I would be purchasing parts for that "first" small quantity ($15) price. This is why I record that price.
