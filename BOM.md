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
| Drive wheel assembly pair | 1 | $24-$33 | Motor + encoder + suspension + tire + cables + wheel-drop sensors | Roborock S4 Max, S45 Max, S5 Max, S50 Max, S55 Max, S6 MaxV, S6 Pure, S65 Pure, S65 MaxV, S7, S7 Pro, S7 MaxV, S7 Max Ultra, S70, S75, E4, E45, E5, E50, E55, G10, T7, T7S, Q5, Q7, Q7 Max, and Q Revo [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-maxv-wheels.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+maxv+wheels) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+maxv+wheels) |
|                           |   | $24-$33 | Motor + encoder + suspension + tire + cables + wheel-drop sensors | Roborock S5, S50, S51, S52, S55, S502, and the budget C10, E20, E25 and E35 [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-wheels.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+wheels) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+wheels) |
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
| Compute Module | 1 | $95 | Raspberry Pi CM4 ≥4 GB | CM4104000 [PiShop](https://www.pishop.us/product/raspberry-pi-compute-module-4-wireless-4gb-lite-cm4104000/) [Newark](https://www.newark.com/raspberry-pi/cm4104000/rpi-compute-module-4-lite-4gb/dp/86AH2101) [DigiKey](https://www.digikey.com/en/products/detail/raspberry-pi/SC0671/13530944) CM4104008 [Newark](https://www.newark.com/raspberry-pi/cm4104008/rpi-module-4-4gb-ram-8gb-emmc/dp/86AH2103) CM4104016 CM4104032 |
|                |   | $72.50 | Raspberry Pi CM5 ≥4 GB | CM5102000 [PiShop](https://www.pishop.us/product/raspberry-pi-compute-module-5-wireless-4gb-ram-lite-cm5104000/) [Newark](https://www.newark.com/raspberry-pi/cm5104000/som-rpi-compute-mod-5-lite-2gb/dp/20AM3783) [DigiKey](https://www.digikey.com/en/products/detail/raspberry-pi/SC1592/25805568) CM5102016 CM5102032 CM5104064 |
|                |   | $62.50*  | Raspberry Pi CM4 ≥2 GB | *if software fits CM4102000 [PiShop](https://www.pishop.us/product/raspberry-pi-compute-module-4-wireless-2gb-lite-cm4102000/) [Newark](https://www.digikey.com/en/products/detail/raspberry-pi/SC0667/13530921) [DigiKey](https://www.newark.com/raspberry-pi/cm4102000/rpi-compute-module-4-lite-2gb/dp/86AH2093) CM4102008 CM4102016 CM4102032 |
|                |   | $72.50* | Raspberry Pi CM5 ≥2 GB | *if software fits CM5102000 [PiShop](https://www.pishop.us/product/raspberry-pi-compute-module-5-wireless-2gb-ram-lite-cm5102000/) [Newark](https://www.newark.com/raspberry-pi/cm5102000/som-rpi-compute-mod-5-lite-2gb/dp/20AM3775) [DigiKey](https://www.digikey.com/en/products/detail/raspberry-pi/SC1586/25805584) CM5102016 CM5102032 CM5104064 |
| Cliff sensors | 4 | $1.50-2.50 ea | 4x cliff + 2x bumper w/cables bundle | iRobot Roomba 500 600 700 800 528 552 564 595 560 570 610 615 620 625 630 650 [AliExpress](https://www.aliexpress.us/w/wholesale-irobot-roomba-500-cliff.html) / [Amazon](https://www.amazon.com/s?k=irobot+roomba+500+cliff) / [eBay](https://www.ebay.com/sch/i.html?_nkw=irobot+roomba+500+cliff) |
| Bumper switches | 2 | $0 | Included in cliff sensors bundle | |
| Main brush motor, gearbox | 1 | $7-11 | Requires brush socket adapter | Fits Roborock S5, S50, S51, S52, 55 502-00/01/02/03**S552-00, S6; Xiaowa C10, E20, E25, E35 [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-main-brush-motor.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+main+brush+motor) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+main+brush+motor) |
| Side brush | 1 | $2-8 | 5-arm | Used in Roborock S5, S50, S51, S55, S6, S60, S6 Pure; fits many other Roborock models [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-side-brush.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+side+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+side+brush) |
|            |   | $3-9 | 3-arm | Used in Roborock S8; fits many other Roborock models [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s8-side-brush.html) / [Amazon](https://www.amazon.com/s?k=roborock+s8+side+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s8+side+brush) |
|            |   | $3-7 | 2-arm curved | Used in Roborock Saros; possibly fits many other Roborock models [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-saros-side-brush.html) / [Amazon](https://www.amazon.com/s?k=roborock+saros+side+brush) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+saros+side+brush) |
| Side brush motor | 1 | $7-10 | Fixed | Fits Roborock S5, S50, S51, S52, S55, S502-00/01/02/03** S552-00, S5 Max, S6, S6 Pure, S6 MaxV, S60, S61, S65, S7, S7 MaxV, S7 Plus, S70, S75, Xiaowa/Xiaomi C10 E20 E25 E35 [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-s5-side-brush-motor.html) / [Amazon](https://www.amazon.com/s?k=roborock+s5+side+brush+motor) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+s5+side+brush+motor) |
|                  |   | $18-35 | Extendable | FlexiArm fits Roborock Qrevo Master, Qrevo Edge, Qrevo Slim, Qrevo Pro, Qrevo S Pro, S8 MaxV Ultra, S8 Max Ultra, Q55 Pro, G20, G20S, V20 [AliExpress](https://www.aliexpress.us/w/wholesale-roborock-qrevo-side-brush-motor.html) / [Amazon](https://www.amazon.com/s?k=roborock+qrevo+side+brush+motor) / [eBay](https://www.ebay.com/sch/i.html?_nkw=roborock+qrevo+side+brush+motor) |
| Mop spin motor(s) + pads | 1–2 | 6–15 | mopping models only | |
| Water pump + valve + tubing | 1 | 4–10 | mopping models only | |
| Mop lift servo | 1 | 2–6 | mopping models only | |
| VL53L7CX multizone ToF | 1 | 8–15 | obstacle detection (90° FoV) | |
| Color camera | 1 | 5–15 | connects to the SBC | |
| Side proximity sensors | 3–4 | 3–8 | | |
| Ultrasonic carpet sensor | 1 | 2–5 | | |
| LiDAR tower bumper sensor | 2 | TODO | Microswitches | |
| Speaker + amp, mic, LEDs, buttons | — | 3–8 | | |
| Custom I/O PCB | 1 | 20–40 | STM32 + motor drivers + sensor front-ends | |
| Wiring, connectors, fasteners, magnets, gaskets, filter | — | 12–25 | | |
| Printed parts (filament) | — | 5–15 | you print these yourself | |
| *Robot subtotal (sourced parts)* | | *~$130–270* | excludes SBC | |

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
The first ($15) price is the rock bottom one that often requires a minimum purchase of 3 pieces - what I'd (or anyone) be paying putting together an OOMWOO all-parts-included convenience kit.
The second ($25) price is what you can realistically get when purchasing 1 piece, *applying coupons* and doing *a few minutes of search*.

Why record the first price if requires a 3 pcs minimum? This is because I intend to assemble a convenient parts kit - and make it available to everyone.
