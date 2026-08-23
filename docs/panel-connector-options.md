# V3.2 Enclosure Panel Connector Sourcing Pass — rev 2 (screw-in + harness-OEM rulings)

**Date: 2026-08-22.** Baseline: four external panel-mount connectors per the enclosure-architecture pivot (Jetson on lid via Syslogic flange brackets; GPS SMA + FAKRA go direct to the Jetson, out of scope). Two rulings from Niall replace rev 1's ground rules:

1. **Panel mounting must be proper screw-in** — jam-nut or bolted metal flange, torqued to spec. No welding, no loose thermoplastic clip flanges. This kills the DT/DTM/DTP L012 flange set as the primary (welded-on thermoplastic flanges — demoted to prototype option at the bottom).
2. **Harnesses are externally manufactured by harness OEMs.** The rev 1 hard requirement ("every connector bought WITH a ready-made mating pigtail") **drops entirely**. What matters instead is **harness-house friendliness**: families every heavy-equipment loom shop crimps daily, with documented contacts and tooling. This also removes rev 1's 12-position ceiling — shells are now picked on merit, and hybrid power+signal inserts are back on the table.

Prices/stock checked live on Digi-Key **2026-08-22**.

## The census (from the 2026-08-21 pivot; mirrors the Notion "Connectors & Integration" channel census)

| Group | Contents | Positions | Class |
|---|---|---|---|
| VEHICLE | battery 25 A + return, seat sensor, e-stop fwd+ret, ECU CAN, joystick CAN, joystick brake, ECU brakes, spare CANs | 2 pwr + ~12 sig | mixed 25 A + signal |
| ROOF | Starlink 5 A, e-stop RX pwr+ret, LiDAR pwr (may consume a spare fused port), LiDAR CAN, LED, 2 spare pwr pairs | ~14 | 5 A |
| STEERING | pwr pair + CAN pair | 4–6 | 10 A (15 A ATO fuse per the late steering ruling) |
| JETSON | pwr pair, 2 CAN pairs, DIO, serviced GPIO; mates UP to lid, short jumper | est. 12–16 | mostly signal, pwr ≤7.5 A fuse |

## The new primary: Deutsch HD30 (HD34 receptacles), metal shell, jam-nut mount

The HD30/HDP20 series is TE Deutsch's heavy-duty circular family for truck/bus/off-highway: HD30 = **aluminum shell**, HDP20 = the same connector in composite thermoplastic. Both are bayonet quick-connect, environmentally sealed (Digi-Key lists HD30 as IP67, −55…+125 °C), rear-insert/rear-release, contact sizes 4–20. Verified against the TE/LADD technical manual (HD30 & HDP20 series, pp. 70–80):

- **Mounting style (verified): single-hole bulkhead, rear jam nut + lockwasher, torqued.** Digi-Key attribute on every HD34: "Bulkhead – Front Side Nut". Metal panel nuts: **114020-90** (18 shell, $4.11, 2,280 DK stock) and **112263-90** (24 shell, $6.03, 7,682 stock); lockwashers 114021 / 112264. Torque spec (HD30 metal): **18 shell 260–280 in·lb, 24 shell 350–375 in·lb**. This is exactly ruling #1 — no clips, no welding, a torqued metal interface.
- **Panel cutout (verified): D-hole** (flat stops rotation). 18 shell: Ø1.507" (38.28 mm), flat across 1.442" (36.63 mm). 24 shell: Ø1.696" (43.08 mm), flat across 1.632" (41.45 mm). Panel range .0625–.1875"; Deutsch sells D-hole punches (18-D-PUNCH / 24-D-PUNCH) for up to .078" steel.
- **Flange-to-panel sealing is a catalog part, not RTV**: neoprene panel gaskets **16-04978** (18 shell, $0.99 DK) and **16-04477** (24 shell, $0.78 DK).
- **Harness-house friendliness: top of the class.** Same Deutsch rear-release contact system as DT (solid 0460/0462 contacts crimp in the HDT-48-00 every Deutsch shop owns; stamped 1060/1062 run on the bench dies loom shops already have). HD30 is a CAT/ag/construction staple, LADD-distributed, fully documented. Any heavy-equipment harness OEM quotes this without blinking.
- Channel note: Digi-Key's HD30 depth is thin-ish and a couple of listings are marked "Discontinued at DigiKey" (not at TE) — fleet volume should flow through LADD/TTI or simply through the harness OEM's own supply, which is the point of ruling #2. DK is fine for bench quantities today (numbers below).

## Group-by-group (all receptacles HD34 = pins; harness OEM builds the HD36 socket plugs)

### VEHICLE — one shell, no split: **HD34-24-21PE** (24 shell, 21 pos: 4× size 12 + 17× size 16)

Rev 1 split VEHICLE only because no mixed 25 A + signal shell had a shelf pigtail. With harness OEMs building the mating side, the hybrid insert is legal again, and 24-21 swallows the whole census in one D-hole:

- **HD34-24-21PE** — Digi-Key 1508-HD34-24-21PE(-ND), **$23.30 @1, 200 in stock, Active** (2026-08-22). E (extra-thin-wall) wire seals: size 12 cavities take .097–.158" insulation (12–14 AWG GXL), size 16 take .053–.120" (16–20 AWG) — so CAN pairs run on normal 18–20 AWG twisted without seal games. The plain PN-seal listing (HD34-24-21PN, $21.21, 103 stock) is the one marked "Discontinued at DigiKey"; the PE is Active and the right grommet anyway.
- Packing: battery + / − on 2× size 12 (25 A rating at the 25 A class — if bench logging shows sustained >20 A, re-pin battery as 2+2 across all four size 12s and move e-stop to size 16 spares; zero hardware change), e-stop fwd/ret on the other 2× size 12, then seat (2), ECU CAN (2), joystick CAN (2), joystick brake (2), ECU brakes (2), spare CAN (2) = 12 of 17 size 16 — **5 signal spares**, which rev 1's DT-12 had none of.
- **24-19 is deliberately excluded from the whole enclosure face**: the BOMAG X34 MITM plug already in the fleet (HD36-24-19SN-059) is the same 24-19 arrangement — keeping 24-19 off the box makes the machine-harness plug physically unable to land on any enclosure receptacle.
- Mounting/cutout: 24-shell D-hole (Ø1.696"/flat 1.632"), nut 112263-90 @ 350–375 in·lb, gasket 16-04477.
- Mating plug for the OEM: HD36-24-21SE ($26.74, 58 DK stock — spot-checked Active).

### ROOF — **HD34-18-14PE** (18 shell, 14× size 16)

- **HD34-18-14PE** — Digi-Key, **$34.73 @1, 57 in stock, Active** (2026-08-22). **Thin stock — this line first on any order.** (HD34-18-14PN: $22.72, 0 stock, 13-wk lead; -PT also 0 — the PE is the one actually on the shelf, and E seals suit the 18–20 AWG roof branches.)
- Packing: Starlink (2), e-stop RX (2), LiDAR CAN (2), LED (2), LiDAR pwr on spare pair #1 (2), spare pair (2) = 12, + 1 more pair of headroom = 14. 13 A contacts loaf on 5 A branches; even the max census fits with a spare pair.
- Mounting/cutout: 18-shell D-hole (Ø1.507"/flat 1.442"), nut 114020-90 @ 260–280 in·lb, gasket 16-04978.

### STEERING — **HD34-18-8PE** (18 shell, 8× size 12) — the 13 A contact flag dies here

- **HD34-18-8PE** — Digi-Key, **$21.48 @1, 192 in stock, Active** (2026-08-22).
- Packing: pwr pair + CAN pair on size 12 contacts = **25 A continuous rating vs the ~9 A working / ~16 A transient census — the rev 1 "re-rule risk" flag on 13 A size 16 contacts is closed**, with 4 spare cavities. One spec note for the OEM: size 12 crimp barrels take 12–14 AWG, and the E-seal grommet seals .097–.158" insulation — so the CAN stub runs as a **16 AWG GXL twisted pair** (fits barrel via 14 AWG-range crimp setting and seals fine; electrically a non-issue on a short stub). If Niall prefers stock 18/20 AWG CAN wire, the alternative is 18-14PE with the power doubled 2+2 — but that duplicates ROOF's arrangement (mis-mate) and reopens the current-margin story; not recommended.
- Mounting/cutout: 18-shell D-hole, nut 114020-90, gasket 16-04978.

### JETSON — **HD34-18-20PN** (18 shell, 20 pos: 2× size 16 + 18× size 20) — GPIO no longer needs disciplining

- **HD34-18-20PN** — Digi-Key, **$28.85 @1, 181 in stock, Active** (2026-08-22). N seals: size 20 takes .040–.095" (20–22 AWG TXL/GXL), size 16 takes 16 AWG for the power pair.
- Packing: pwr pair on the 2× size 16 (13 A vs ≤7.5 A fuse), CAN1 (2), CAN2 (2), DIO (2–3), serviced GPIO (3–4) on size 20 (7.5 A) = 9–11 of 18 — the census 12–16 estimate fits whole, **rev 1's "serviced-GPIO count is the knob" constraint is gone**.
- Mounting/cutout: 18-shell D-hole, nut 114020-90, gasket 16-04978.

### Mis-mate matrix and exposure polarity

Three different 18-shell inserts (18-8 / 18-14 / 18-20) + one 24-shell (24-21): the 24 shell can't couple to 18s at all; within the 18 shell, different insert arrangements cannot seat — pins bottom against the mismatched socket-insert face before the bayonet locks. That's geometry, not a formal keying feature, so keep boot-color + label discipline; if a hard-keyed same-arrangement pair is ever needed, Deutsch sells reverse-keyed inserts (the "-91"-style reverse arrangements) as a catalog option. 24-19 excluded face-wide (X34 collision, above). All receptacles carry pins: the battery's live side arrives on the harness plug's recessed sockets (correct exposure); roof/steering/jetson receptacles present recessed, fused pins when unmated — same acceptable posture as rev 1.

## Alternates

**Amphenol AHDP (DuraMate) — the cheaper 1:1, with known stock gaps.** Same insert arrangements, bayonet, and single-hole front-side-nut bulkhead mount; IP67/IP69K; **shell is thermoplastic** (it clones the HDP20 side of the family, not the metal HD30 — still a proper torqued jam nut, but not metal, and plastic-shell torque is the lower HDP20-class spec). Roughly half the Deutsch price. Verified 2026-08-22, receptacle (AHDP04) pin variants per our four arrangements: 24-21: PR-SRA $11.91/457, PN-WTA $13.30/34; 18-14: PR-WTA $10.83/153, PN-SRA $9.94/110; 18-08: PR-SRA $10.71/331, PN-WTA $11.54/249 (+800 factory); 18-20: PN-WTA $11.75/260, PR-SRA $12.87/219. Gaps are real but variant-level, not family-level (e.g. 18-20PR-WTA 0 DK / marketplace-only, 18-08PN-SRA 0, 24-21PR-BRA 0). Suffixes: N/R = normal / reduced (thin-wall) wire seal; -WTA/-SRA/-BRA/-STA = factory rear-adapter style — pick with the harness OEM per backshell choice. Verdict: keep as the cost-down second source; contacts are the same size system, so the OEM's tooling story is unchanged.

**Souriau (Eaton) UTS — the screw-in industrial fallback.** UTS7-prefix = **jam-nut receptacle** (single round hole, e.g. Ø0.87" for the size 14 shell, rear jam nut) — the mounting passes ruling #1, but the shell is honest **plastic** (thermoplastic, IP68/69K), and the contact system is Trim Trio, not Deutsch — different crimp tooling (M317 etc.), less muscle-memory at heavy-equipment loom shops. Reference part re-checked 2026-08-22: **UTS71419P** (size 14 shell, 19× size 20 pos): $12.87, **0 stock at Digi-Key, 17-week lead** (Active; rev 1 mislabeled this PN square-flange — it is the jam-nut style). Only reached for if both Deutsch and Amphenol channels fail simultaneously.

**Split-VEHICLE option (kept on file, not recommended):** if bench data ever demands more battery margin than a 25 A size 12 pair, the studied **24-9 power insert** — **HD34-24-9PN**, $25.87 @1, **174 in stock, Active** (2026-08-22); 1× size 4 (100 A) + 2× size 8 (60 A) + 6× size 12 — takes battery on size 8 contacts with 2.4× headroom, paired with HD34-18-14 for signals. Costs a second D-hole, a second harness drop, and the size 4/8 contact + tooling adders; the 2+2 re-pin inside 24-21 covers the same concern for free, so this stays a documented fallback.

## Recommended set (four connectors — VEHICLE un-splits)

| # | Group | Panel receptacle | $ / stock (DK, 2026-08-22) | Mount | Cutout (D-hole) | Mating plug (OEM buys) |
|---|---|---|---|---|---|---|
| 1 | VEHICLE | HD34-24-21PE (4× s12 + 17× s16) | $23.30 / 200 | jam nut 112263-90, 350–375 in·lb, gasket 16-04477 | Ø1.696" / flat 1.632" | HD36-24-21SE ($26.74 / 58) |
| 2 | ROOF | HD34-18-14PE (14× s16) | $34.73 / **57** | jam nut 114020-90, 260–280 in·lb, gasket 16-04978 | Ø1.507" / flat 1.442" | HD36-18-14SE |
| 3 | STEERING | HD34-18-8PE (8× s12) | $21.48 / 192 | jam nut 114020-90, 260–280 in·lb, gasket 16-04978 | Ø1.507" / flat 1.442" | HD36-18-8SE |
| 4 | JETSON | HD34-18-20PN (2× s16 + 18× s20) | $28.85 / 181 | jam nut 114020-90, 260–280 in·lb, gasket 16-04978 | Ø1.507" / flat 1.442" | HD36-18-20SN |

**Per-enclosure cost (our side): receptacles $108.36 + jam nuts $18.36 (1× 112263-90, 3× 114020-90) + lockwashers ~$8 (112264 ×1, 114021 ×3 — est., unverified) + gaskets $3.75 + receptacle pin contacts ~$25–32 (solid nickel: s12 0460-204-12141 $0.82/35,920 stock; s16 0460-202-16141 $0.43/34,177; s20 0460-202-20141 $0.43/70,399; stamped 1060-series for volume) + cavity sealing plugs ~$5 ≈ $170–175/enclosure** — the same money as the DT set's $185, in torqued aluminum instead of clip-on plastic. Harness-side connector content (inside the OEM quote): 4 plugs ≈ $110–120 + socket contacts ≈ $25 + backshells/boots (WHDS-18/24 or -059-style clamp, HD30-xxBT boots) ≈ $30–50 → ≈ $180/kit before OEM labor.

## RFQ-ready line list for the harness OEM (per group; wire circuits per the census above / Notion wiring-page census)

Common to all groups — solid contacts (HDT-48-00-crimpable), nickel: pins 0460-204-12141 (s12) / 0460-202-16141 (s16) / 0460-202-20141 (s20); sockets 0462-203-12141 (s12) / 0462-201-16141 (s16) / 0462-201-20141 (s20). Stamped equivalents for volume: 1060-xx / 1062-xx series. Unused cavities: Deutsch sealing plugs per contact size (final plug PNs with the OEM). Receptacle side ships loose-piece with the enclosure loom; plug side is the OEM's harness end.

| Group | Connector set | Contacts (qty) | Wire list |
|---|---|---|---|
| VEHICLE | Recept HD34-24-21PE + nut 112263-90 + LW 112264 + gasket 16-04477; plug HD36-24-21SE + backshell/boot | s12 pins+sockets ×4; s16 ×12 (+5 cavities plugged) | batt +/− 2× 12 AWG GXL; e-stop fwd/ret 2× 14 AWG; seat 2×, joystick brake 2×, ECU brakes 2× 16–18 AWG; ECU CAN, joystick CAN, spare CAN 3× 18 AWG TXL twisted pairs |
| ROOF | Recept HD34-18-14PE + nut 114020-90 + LW 114021 + gasket 16-04978; plug HD36-18-14SE + backshell/boot | s16 ×14 (12–14 used) | Starlink pwr 2× 16 AWG; LiDAR pwr 2× 16 AWG; e-stop RX 2× 18 AWG; LED 2× 18 AWG; LiDAR CAN 1× 18 AWG twisted pair; spare pair 2× 18 AWG |
| STEERING | Recept HD34-18-8PE + nut 114020-90 + LW 114021 + gasket 16-04978; plug HD36-18-8SE + backshell/boot | s12 ×4 (+4 plugged) | pwr +/− 2× 12 AWG GXL; CAN 1× **16 AWG** GXL twisted pair (seal/barrel constraint, flagged above) |
| JETSON | Recept HD34-18-20PN + nut 114020-90 + LW 114021 + gasket 16-04978; plug HD36-18-20SN + backshell/boot | s16 ×2; s20 ×9–11 (rest plugged) | pwr +/− 2× 16 AWG; CAN1, CAN2 2× 20 AWG TXL twisted pairs; DIO 2–3×, serviced GPIO 3–4× 20–22 AWG TXL; far end lands on the Syslogic box's own connector faces (OEM terminates per Jetson pigtail spec) |

## Demoted: Deutsch DT/DTM/DTP shelf-pigtail set (prototype/bench-mule option only)

Rev 1's pick survives as the fast-prototype path — factory-crimped pigtails are shelf items and the three shell sizes can't intermate — but **the L012 receptacle flanges are welded-on thermoplastic two-ear clips, not a torqued metal interface: they fail ruling #1 for fleet enclosures.** Stock/prices as verified 2026-08-21: DTP04-4P-L012 $12.70/1,635 + DTP06-4S-PT12 pigtail $24.99/380; DT04-12PA-L012 $9.65/2,890 + DT06-12SA-PT $26.99/235; DT04-12PB-L012 $9.14/1,388 + DT06-12SB-PT $26.99/31; DT04-4P-L012 $5.21/4,956 + DT06-4S-PT $11.99/706; DTM04-12PA-L012 $10.76/534 + DTM06-12SA-PT20 $24.99/348 (≈$185/enclosure). Use freely on bench mules and the first CAD-check enclosure; do not fleet it.

## Bench-trial order list (2 sets, ~$450 + shipping, all Digi-Key)

Receptacles ×2 each: HD34-24-21PE, **HD34-18-14PE (57 in stock — this line first)**, HD34-18-8PE, HD34-18-20PN (≈$217). Hardware ×2 sets: 112263-90, 114020-90 ×3, lockwashers 112264/114021, gaskets 16-04477/16-04978 ×3 (≈$60). One mating plug each for fit/mate check: HD36-24-21SE, HD36-18-14SE, HD36-18-8SE, HD36-18-20SN (≈$110). Contacts: s12 pins/sockets ×30, s16 ×80, s20 ×40 solid nickel (≈$65). Per [[no-unapproved-substitutions]]: proposal list for Niall's approval, nothing ordered.

Open items: (1) D-hole dims + torque callouts go into the enclosure-face freeze (punch vs. mill per panel material); (2) OEM RFQ out with the line list above — ask them to confirm the 16 AWG steering-CAN stub or propose their standard; (3) HD34-18-14PE restock risk — 57 units on 2026-08-22; (4) battery 2+2 re-pin decision after bench current logging; (5) closed: steering-contact current flag (size 12 = 25 A), JETSON GPIO-count discipline (18 signal cavities).
