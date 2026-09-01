# V3.2 Internal Wiring Definition — Y-split pigtails + board headers + J_BRG

**Date: 2026-08-22 (rev b).** Companion to the panel sourcing pass (`/tmp/claude-501/panel-connector-options.md`, rev 2). Scheme per Niall: each of the four HD34 panel receptacles gets a **Y-split pigtail** — contacts crimped at the receptacle rear, forking inside the enclosure into a **power leg** ending in a connector onto the power board (CB-001) and a **signal leg** ending in a connector onto the interface board — plus **one board-to-board link, J_BRG**. All board headers **vertical** (his ruling; no right-angle shells). No splices anywhere: every conductor is crimp-to-crimp, panel contact to board-header receptacle.

Board split (locked): **POWER board** — battery in (25 A), all fused 13 V outputs (Starlink / roof LED / steering / spares / LiDAR pwr), e-stop loop + RX feed + toggle/ES_FEED, ignition T15 sense, Jetson power. **INTERFACE board** — all CANs (ECU, joystick, steering, LiDAR, Jetson CAN1/2), brakes, seat sensor, Jetson GPIO/DIO, autonomy/arm signals. Sense lines that originate on the power board but report onward (ARM_SENSE, IGN_SENSE, INA228 telemetry) ride **J_BRG**, never the panel pigtails.

## Design resolutions (the ambiguous lines, decided)

1. **Roof LED drive = switched power, power leg.** The beacon is gated on the power board (K53 between FH5 "ROOF LEDS 5 A" and the output). The wire to the roof is fused, K53-switched 13 V — a power line. The *drive logic* never leaves the boards: AUTONOMY_EN crosses J_BRG and Q54 sinks K51/K53 coils on CB-001.
2. **Spare power pairs = power leg, ladder branches.** LiDAR power consumes the AUX 5 A branch (FH7) as the census anticipated; the remaining spare pair rides the spare 7.5 A branch (FH8). Starlink = FH4, roof LED = FH5, steering = FH6 (15 A ATO), Jetson = FH2. DIO 2 A (FH3) carries two loads: the interface-board +13V_SIG rail via J_BRG 1/2 and the Syslogic DIO-bank supply (DIO_PWR/DIO_GND) via J_JP 2/4 up the Jetson power leg — combined ≤ 0.35 A (budget in the JETSON section).
3. **Kar-Tech RX is three wires, not two.** The census line "e-stop RX pwr + return" expands per the 3-wire rework: RX power feed (always-on **/ES_RX** from the safety chain, *not* the fuse ladder), RX ground, and the single status wire (RX_STAT → J53 path → R86/Q58/K52). The third wire consumes ROOF's headroom pin. Mark the ES_RX position on silks/labels: it is live with the master switch off.
4. **Ignition T15 rides a VEHICLE s16 spare.** The four-connector census never listed T15; it lands on VEHICLE cavity s16-15 → power leg → J1/R91 (KEY_IN). Single-ended, referenced to battery return.
5. **E-stop machine loop moves from s12 to s16 cavities.** Two reasons: (a) gauge chain — a size-12 solid barrel wants 12–14 AWG, but no signal-class board header accepts that; on s16 the whole run is 18 AWG, legal at both ends (s16 barrel 16–20 AWG; board-side crimp = Micro-Fit 18 AWG terminal 43030-0038 — the 20–24 AWG 43030-0007 does not take 18 AWG). Loop current is the machine seat-circuit class (≤2 A) — 18 AWG is generous. (b) It frees s12-3/s12-4 for the battery.
6. **Battery goes 2+2 now.** One 12 AWG conductor per pole would put 25 A (fuse ceiling) on a single 23 A-rated Mega-Fit pin — over nameplate. The sourcing pass's contingency ("re-pin battery 2+2 across all four size 12s") becomes the baseline: two 12 AWG conductors per pole, panel s12-1/-3 = BAT+, s12-2/-4 = BAT−, landing one wire per pin on a Mega-Fit 4 → 12.5 A/pin at the fuse ceiling, ~54 % of rating. Deutsch s12 contact count on VEHICLE unchanged (all four now used).
7. **The VEHICLE power leg lands in two housings** (the only leg that does): battery copper (Mega-Fit, 12 AWG) and the e-stop loop + T15 (Micro-Fit, 18–20 AWG) cannot share a crimp system — and the safety loop earns its own service point anyway.
8. **Legacy connectors replaced:** J5 XT60 input deleted (battery now J_VP1 — this also closes the open J2/J5 identical-XT60 mis-plug hazard: J2 remains the only XT60, bench/main-out). J51/J52/J53 XH (RX feed/loop/status) → J_RP + J_VP2. Fuse-ladder 5.08 terminals J57–J63 → J_JP/J_RP/J_SP as mapped below. On the interface board: J6/J7 (CAN), J14/J15 (aux taps), J1/J10/J12 (DIO/GPIO), J2/J3/J11 (AUT_EN/lamp/ARM), J4/J5/J8/J9/J13 (seat/brake terminals) are subsumed by J_VS/J_RS/J_SS/J_JS/J_BRG-I. J50 (panel toggle + ES_FEED, XH-6) stays a direct board-to-panel harness outside the Y-splits — recommend migrating it to Micro-Fit 6-ckt in the same sweep for latch + one crimp ecosystem. Both board schematics carry the sweep (gen_interface.py for the interface board; the swept CB-001 file for the power board).

## (a) THE TABLE — per panel connector: every wire → Y-leg → board header + pin

Cavity IDs are ordinal per insert arrangement; final Deutsch cavity letters map 1:1 at harness-drawing time from the TE insert drawings (sourcing-pass caveat stands). Wire gauges are the **internal pigtail** gauges (chosen so one conductor satisfies both its panel-contact barrel and its board-terminal crimp range).

### VEHICLE — HD34-24-21PE (4× s12 + 17× s16)

| Cavity | Circuit | AWG | Y-leg | Board header · pin |
|---|---|---|---|---|
| s12-1 | BAT+ (A) | 12 | power | PWR J_VP1 · 1 |
| s12-2 | BAT− (A) | 12 | power | PWR J_VP1 · 3 |
| s12-3 | BAT+ (B) | 12 | power | PWR J_VP1 · 2 |
| s12-4 | BAT− (B) | 12 | power | PWR J_VP1 · 4 |
| s16-1 | ESTOP_LOOP_FWD | 18 | power | PWR J_VP2 · 1 |
| s16-2 | ESTOP_LOOP_RET | 18 | power | PWR J_VP2 · 2 |
| s16-3 | SEAT_A | 20 | signal | IFB J_VS · 1 |
| s16-4 | SEAT_B | 20 | signal | IFB J_VS · 2 |
| s16-5 | ECU_CAN_H | 20 tw | signal | IFB J_VS · 3 |
| s16-6 | ECU_CAN_L | 20 tw | signal | IFB J_VS · 4 |
| s16-7 | JOY_CAN_H | 20 tw | signal | IFB J_VS · 5 |
| s16-8 | JOY_CAN_L | 20 tw | signal | IFB J_VS · 6 |
| s16-9 | BRK_JOY (BTS lever, console side of cut) | 20 tw | signal | IFB J_VS · 7 |
| s16-10 | BRK_ECU (BTS lever, ECU side of cut) | 20 tw | signal | IFB J_VS · 8 |
| s16-11 | SPARE_CAN_H | 20 tw | signal | IFB J_VS · 9 |
| s16-12 | SPARE_CAN_L | 20 tw | signal | IFB J_VS · 10 |
| s16-13 | T15_KEY (ignition sense) | 20 | power | PWR J_VP2 · 3 |
| s16-14 | SIG_GND / drain | 20 | signal | IFB J_VS · 11 |
| s16-15…17 | spare (plugged) | — | — | J_VS 12–16 spare |

**Brake is a single-ended MITM — the one exception to pair wiring.** On the BW211 the brake is one conductor (the BTS lever line, X4.B pin 9 → X5.A:14), referenced to console ground at the EBOX stud — X4.B has no ground cavity. Cutting it for the interposer yields exactly two wires, BRK_JOY (console/joystick-side end) and BRK_ECU (ECU-side end), run as one twisted pair; there is no brake return conductor, and the board-side reference is SIG_GND. The seat, by contrast, stays a true two-wire pair (floating switch across SEAT_A/B). Per-machine adaptation of the brake tap lives in the external harness, never the enclosure internals.

J_VP2 · 4 = spare. Power-board terminations: J_VP1 → input stage (F1/K-gate, was J5); J_VP2-1/2 → safety-chain loop nets (CONT_A/LOOP_B series path through K50/K52, was J52); J_VP2-3 → R91 → KEY_IN (was J1).

### ROOF — HD34-18-14PE (14× s16)

| Cavity | Circuit | AWG | Y-leg | Board header · pin |
|---|---|---|---|---|
| 1 | STARLINK_13V (FH4, 5 A) | 16 | power | PWR J_RP · 1 |
| 2 | STARLINK_GND | 16 | power | PWR J_RP · 7 |
| 3 | LIDAR_13V (FH7 AUX, 5 A) | 16 | power | PWR J_RP · 2 |
| 4 | LIDAR_GND | 16 | power | PWR J_RP · 8 |
| 5 | BCN_13V (FH5 via K53, 5 A) | 16 | power | PWR J_RP · 3 |
| 6 | BCN_GND | 16 | power | PWR J_RP · 9 |
| 7 | LIDAR_CAN_H | 20 tw | signal | IFB J_RS · 1 |
| 8 | LIDAR_CAN_L | 20 tw | signal | IFB J_RS · 2 |
| 9 | ES_RX (RX pwr, **always-on**) | 18 | power | PWR J_RP · 5 |
| 10 | RX_STAT | 20 | power | PWR J_RP · 6 |
| 11 | RX_GND | 18 | power | PWR J_RP · 11 |
| 12 | SPARE_13V (FH8, 7.5 A) | 16 | power | PWR J_RP · 4 |
| 13 | SPARE_GND | 16 | power | PWR J_RP · 10 |
| 14 | spare (plugged) | — | — | J_RP · 12 spare |

J_RS · 3 = SIG_GND/drain (bus GND reference for the CAN stub), · 4 spare. J_RP terminations: pins 1–4 = FH4/FH7/FH5(K53)/FH8 branch outputs; pin 5 = /ES_RX (safety chain, upstream of master switch — was J51); pin 6 = RX_STAT (R86/Q58 cell — was J53).

### STEERING — HD34-18-8PE (8× s12)

| Cavity | Circuit | AWG | Y-leg | Board header · pin |
|---|---|---|---|---|
| A | STR_13V (FH6 via K51, 15 A ATO) | 12 | power | PWR J_SP · 1 |
| B | STR_GND | 12 | power | PWR J_SP · 2 |
| C | STR_CAN_H | 16 tw | signal | IFB J_SS · 1 |
| D | STR_CAN_L | 16 tw | signal | IFB J_SS · 2 |
| E–H | spare (plugged) | — | — | — |

The 16 AWG CAN pair is forced by the s12 barrel (same constraint, and same 14 AWG-range crimp setting, as the external side per the sourcing pass); board end uses Mini-Fit **HCS 16 AWG terminals** — see family section. J_SS · 3 = SIG_GND, · 4 spare. Steering CAN is a CAN-A bus tap (replaces aux-tap J14/J15 duty for this node).

### JETSON — HD34-18-20PN (2× s16 + 18× s20)

| Cavity | Circuit | AWG | Y-leg | Board header · pin |
|---|---|---|---|---|
| s16-A | JET_13V (FH2, 7.5 A) | 18 | power | PWR J_JP · 1 |
| s16-B | JET_GND | 18 | power | PWR J_JP · 3 |
| s20-1 | JET_CAN1_H | 20 tw | signal | IFB J_JS · 1 |
| s20-2 | JET_CAN1_L | 20 tw | signal | IFB J_JS · 2 |
| s20-3 | JET_CAN2_H | 20 tw | signal | IFB J_JS · 3 |
| s20-4 | JET_CAN2_L | 20 tw | signal | IFB J_JS · 4 |
| s20-5 | DIO_PWR (FH3 "DIO 2 A" branch) | 20 | power | PWR J_JP · 2 |
| s20-6 | DIO_GND | 20 | power | PWR J_JP · 4 |
| s20-7 | DIO_OUT_AUTONOMY (gpiochip8 out_b1, hi = autonomy on) | 20 | signal | IFB J_JS · 5 |
| s20-8 | DIO_OUT_BRAKE (gpiochip8 out_b0, lo = brake engaged) | 20 | signal | IFB J_JS · 6 |
| s20-9 | GPIO_SPARE (third conditioning row / BRK_LINE) | 20 | signal | IFB J_JS · 7 |
| s20-10 | SEAT_STATE (DIO in) | 20 | signal | IFB J_JS · 8 |
| s20-11 | ARM_SENSE (DIO in) | 20 | signal | IFB J_JS · 14 |
| s20-12 | BRAKE_SENSE (DIO in) | 20 | signal | IFB J_JS · 15 |
| s20-13 | IGN_SENSE (DIO in) | 20 | signal | IFB J_JS · 16 |
| s20-14 | SDA | 20 | signal | IFB J_JS · 9 |
| s20-15 | SCL | 20 | signal | IFB J_JS · 10 |
| s20-16 | ALERT_N | 20 | signal | IFB J_JS · 11 |
| s20-17 | V3_HOST (Jetson 3V3 → INA228 VS) | 20 | signal | IFB J_JS · 12 |
| s20-18 | SIG_GND (CAN + I²C reference) | 20 | signal | IFB J_JS · 13 |

The DIO set is explicit. The Syslogic DIO bank (PCA9554 expanders) is galvanically isolated and needs its own supply pair: **DIO_PWR + DIO_GND, fed from FH3 ("DIO 2 A") directly up the Jetson power leg on J_JP 2/4** — J_JP runs 4/4 (1 = JET_13V, 2 = DIO_PWR, 3 = JET_GND, 4 = DIO_GND). Outputs (gpiochip8): out_b0 = DIO_OUT_BRAKE (low = brake engaged), out_b1 = DIO_OUT_AUTONOMY (high = autonomy on). Inputs (gpiochip7), allocated by priority: SEAT_STATE, ARM_SENSE, BRAKE_SENSE, IGN_SENSE. Input returns ride DIO_GND at the Jetson end; on the board side the inputs are the existing driven nets referenced to board GND, with one SIG_GND pin carrying the CAN/I²C reference.

Cavity arithmetic: 18× s20 = 2 (DIO supply pair, power leg) + 16 (signal leg: 4 CAN + 2 DIO out + 1 GPIO_SPARE + 4 DIO in + 4 I²C/host + 1 SIG_GND). Both s16s carry Jetson power. **20/20 — the shell is full**, so SEAT_EMU_SENSE (diagnostics-class) is dropped; it survives on the interface board as a probe stub only. J_JS stays **Micro-Fit 16 at exactly 16/16** (43045-1812 fallback not needed; J_BRG's 20-ckt width stays unique on the board). GPIO_SPARE keeps the third conditioning row fed — populated per the no-DNP rule, it is the BRK_LINE emulation-level provision.

FH3 "DIO 2 A" budget — two loads: the interface-board +13V_SIG rail via J_BRG 1/2 (4× G6K-2 coils ≈ 47 mA + wetting pull-ups ≈ 7 mA + panel lamp ≈ 13 mA ⇒ ≲ 0.1 A) and the Syslogic DIO bank via J_JP 2 (expander + isolated I/O class, ≤ 0.25 A). Combined worst case ≤ 0.35 A on the 2 A branch — >5× headroom.

### Header roster

**Power board (6):** J_VP1 Mega-Fit 4 (battery), J_VP2 Micro-Fit 4 (e-stop loop + T15), J_RP Mini-Fit Jr 12 (roof branches + RX trio) — branch pairs 16 AWG on 45750-3112 HCS terminals, RX trio on 39-00-0039, J_SP Mega-Fit 2 (steering), J_JP Mini-Fit Jr 4 (Jetson pwr + DIO pwr, 4/4), J_BRG-P Micro-Fit 20. Plus J50 panel harness (XH-6 today; migrate to Micro-Fit 6 recommended) and J2 XT60 bench out.
**Interface board (5):** J_VS Micro-Fit 16 (vehicle signals), J_RS Micro-Fit 4 (LiDAR CAN), J_SS Mini-Fit Jr 4 w/ HCS (steering CAN), J_JS Micro-Fit 16 (Jetson signals), J_BRG-I Micro-Fit 20.

Same-size collision audit: J_RS (Micro-Fit 4, IFB) vs J_VP2 (Micro-Fit 4, PWR) — cross-board only; worst case is loop-open = nuisance stop, no damage. J_SS vs J_JP (Mini-Fit 4) — cross-board only; label + leg dress. J_VS vs J_JS (both Micro-Fit 16, same board) — the one real same-board pair: all-signal, no damage class, machine simply won't run; mitigate with leg length dress + housing labels (same posture as the panel-side boot-color rule). J_BRG's 20-ckt width is deliberately unique so the bridge can never mate a Y-leg.

## (b) Board connector family — verticals only, and the Molex question

**Direct answer: yes, Molex is good — it is the correct default here, and the specific weak spots are known and avoidable.** The three Molex power families (Mega-Fit 5.7 mm / Mini-Fit Jr 4.2 mm / Micro-Fit 3.0) are the harness industry's lingua franca for unsealed board-to-wire: every US harness OEM already runs 5556/43030-class applicators and hand tools, Digi-Key holds terminals in the half-million class, every housing is positively latched and polarized, and — decisive for PCBA — **LCSC stocks genuine Molex vertical THT headers in depth**, which is the JLC assembly pool. No other candidate family clears all four gates at once. Weaknesses, honestly: **Mega-Fit is the thin one** (LCSC verticals: 6-ckt = 29 pcs, 8-ckt = 0 — designed around below by never using >4-ckt Mega-Fit), Mini-Fit Jr needs its HCS terminal variant above ~9 A, and same-arrangement housings have no hard keying (labels/dress, as accepted at the panel). Note the boards are JLC "SMT-only + hand THT" anyway — every header is hand-loaded, so a Digi-Key backfill of any LCSC gap never blocks assembly.

Stock snapshots **2026-08-22** (LCSC read via site, Digi-Key read via product pages):

### Board side — vertical THT headers on LCSC (JLC PCBA pool), genuine Molex

| Family | PN (vertical, THT, tin) | LCSC | Stock | $ @1 |
|---|---|---|---|---|
| Micro-Fit 3.0, 2-ckt | 43045-0212 | C293362 | 29,604 | $0.38 |
| Micro-Fit 3.0, 4-ckt | 43045-0412 | C277721 | 4,668 (+22k other-supplier) | $0.52 |
| Micro-Fit 3.0, 12-ckt | 43045-1212 | C485572 | 10,044 | $0.99 |
| Micro-Fit 3.0, 16-ckt | 43045-1612 | C491447 | 1,942 | $1.35 |
| Micro-Fit 3.0, 20-ckt | 43045-2012 | pull at BOM time | family PN, not read | ~$1.6 |
| Mini-Fit Jr, 4-ckt | 39-28-1043 | C293502 | 65,105 | $0.25 |
| Mini-Fit Jr, 12-ckt | 39-28-1123 | C293505 | 1,140 | $0.66 |
| Mega-Fit, 2-ckt (1×2) | 76829-0002 | C588521 | 365 | $1.38 |
| Mega-Fit, 4-ckt (2×2) | 76829-0004 | C19170941 | 2,081 | $1.77 |
| Mega-Fit, 6-ckt | 76829-0006 | C588522 | **29** | $1.82 |
| Mega-Fit, 8-ckt | 76829-0008 | C588523 | **0** (DK: 3,457 @ $3.65) | — |

Clone depth behind every Micro/Mini line (XFCN, Hong Cheng, HCTL, DLL, ~$0.10–0.40) — genuine specified, clones acceptable fallback for bench mules only. 76829 confirmed as the *vertical* Mega-Fit series (76825 is right-angle — several catalogs blur this).

### Harness side — receptacle housings + crimp terminals at Digi-Key

| Item | PN | DK stock 2026-08-22 | $ @1 |
|---|---|---|---|
| Micro-Fit socket terminal, 20–24 AWG tin | 43030-0007 | 507,432 (+648k factory) | $0.20 |
| Micro-Fit socket terminal, 18 AWG tin | 43030-0038 | 749,392 | $0.07 |
| Micro-Fit receptacle housing, 16-ckt | 43025-1600 | 12,104 | $0.94 |
| Micro-Fit housings 4/20-ckt | 43025-0400 / 43025-2000 | family, not individually read | ~$0.35/$1.10 |
| Mini-Fit Jr socket terminal (5556), 18–24 AWG tin | 39-00-0039 | 464,782 | $0.17 |
| Mini-Fit Jr HCS terminal, 16 AWG (13 A) | 45750-1112 | staple, not read this pass | ~$0.35 |
| Mini-Fit Jr housing, 12-ckt | 39-01-2120 | 3,079 | $0.49 |
| Mini-Fit Jr housing, 4-ckt | 39-01-2040 | family, not read | ~$0.35 |
| Mega-Fit socket terminal, 12 AWG tin | 76823-0322 | 32,992 | $0.28 |
| Mega-Fit housing, 8-ckt dual (ref) | 105411-0108 | 1,348 | $1.43 |
| Mega-Fit housing, 4-ckt dual | 105411-0104 | family (sibling verified) | ~$1.20 |
| Mega-Fit housing, 1×2 | 200456-1212 | LCSC C585463: 3,112 — **VERIFY mate** vs 76829-0002 drawing | $0.60 |

Tooling: all three families crimp with standard open-barrel tooling every OEM owns (spec tools: Molex 63819-xxxx frames); no new ecosystem.

### Current vs rating, derated

| Leg | Load | Pin rating | Result |
|---|---|---|---|
| Battery (J_VP1) | 25 A fuse ceiling / ~20 A real, 2 pins/pole | Mega-Fit 23 A | 12.5 A/pin = 54 % — clean even at Texas ambient |
| Steering (J_SP) | ~9 A working, ~16 A transient | Mega-Fit 23 A | 39 % cont / 70 % transient — fine |
| Roof branches (J_RP) | ≤5 A each, 12-ckt loaded | Mini-Fit Jr, branch pins on HCS terminals (13 A) | ≤5 A on 13 A = ≤38 %; RX trio ≪1 A — fine |
| Jetson (J_JP) | 7.5 A fuse / ≈4.6 A real | Mini-Fit Jr 9 A | 51 % real; HCS drop-in if bench runs hot |
| Signals + J_BRG | ≤2 A (13 V feed over 2 pins → 1 A/pin) | Micro-Fit 5 A | ≥60 % headroom everywhere |

### Alternates judged (and why not)

- **TE VAL-U-LOK** (4.2 mm, Mini-Fit-analog, NOT intermateable): fine parts, cheaper at DK (e.g. 1586041-8 R/A $1.10) — but **zero exact-match presence on LCSC** (checked 2026-08-22) = no JLC PCBA path, and it buys nothing Mini-Fit doesn't already give. Second-source on paper only.
- **AMP CT**: 2.0 mm, ~2 A signal-only — wrong current class for every leg here. Rejected.
- **JST VL** (6.2 mm, 10 A JST-rated): genuine JST on LCSC (B04P-VL family present) but tops out far below Mega-Fit, tiny position range, and VL crimp tooling is rare at US heavy-equipment OEMs. Niche only.

## (c) J_BRG — one cable assembly

**Micro-Fit 3.0 dual-row 20-ckt** (the historical J_BRG width, kept — and unique on both boards so it can't mate a Y-leg). Headers 43045-2012 vertical THT on both boards; assembly = 2× 43025-2000 receptacles + 40× 43030-0007, 22 AWG (13 V feed pairs 20 AWG), ~120–150 mm, built by the harness OEM with the pigtails (or 2 units hand-built). Supplies face grounds across the rows:

| Pin | Signal | Dir | Pin | Signal |
|---|---|---|---|---|
| 1 | +13V_SIG (FH3 DIO 2 A) | P→I | 11 | GND |
| 2 | +13V_SIG | P→I | 12 | GND |
| 3 | 3V3_AUX (≤50 mA, AMS1117) | P→I | 13 | GND |
| 4 | V3_HOST (Jetson 3V3 → INA228 VS) | I→P | 14 | GND |
| 5 | SDA | ↔ | 15 | GND |
| 6 | SCL | ↔ | 16 | GND |
| 7 | ALERT_N | P→I | 17 | GND |
| 8 | AUTONOMY_EN (→ Q54 → K51/K53) | I→P | 18 | ARM_SENSE (K50 pole 2/R59) |
| 9 | IGN_SENSE (Q55 open-drain) | P→I | 19 | spare |
| 10 | spare | — | 20 | spare |

Replaces the power board's J54/J56/J66/J67 XH cluster. Control + telemetry only — **no load current** (doctrine unchanged). The July 20-way list's MODE_SEL/ARMED/FAULT/LVD_OK/LOW_BATT/VON flags are OBE — as-built CB-001 exports ARM_SENSE + IGN_SENSE + I²C/ALERT; AUTONOMY_EN is the only I→P command. 7× GND preserved.

## (d) Notion internal-wiring text (applied to the page 2026-08-22)

Routing bullets rewritten to the Y-split scheme + header roster + J_BRG pin summary; diagrams left as-is; next-steps item 3 marked done; e-stop-routing open question updated to the defined s16 + J_VP2 path (residual = bench wetting-current check).

## RFQ addendum — harness OEM (supersedes matching lines in the sourcing-pass RFQ list)

**Scope add:** OEM also builds the four **internal Y-split pigtails** (receptacle side): crimp HD34 rear contacts → fork → Molex housings per the tables above. Leg lengths TBD at enclosure CAD (target: legs reach only their own board — mis-plug dressing). No splices; one conductor per contact, crimp-to-crimp.

Changes vs the original line list:
1. **VEHICLE:** battery is now **2+2** — four 12 AWG GXL conductors (BAT+ ×2 on s12-1/-3, BAT− ×2 on s12-2/-4), external harness same. **E-stop loop moves to s16-1/-2 at 18 AWG** (was s12 @ 14 AWG; board-side terminals 43030-0038). **Brake is one twisted pair, BRK_JOY/BRK_ECU on s16-9/-10** — single cut conductor, no returns (the machine references the lever line to console ground at the EBOX stud). Add **T15 key-sense on s16-13, 20 AWG** (external: splice-point per machine T15 tap, OEM to quote). 14 of 17 s16 used; s16-15…17 plugged.
2. **ROOF:** e-stop RX is **three wires** — ES_RX pwr (18 AWG), RX_STAT (20 AWG), RX_GND (18 AWG) on cavities 9/10/11. The four branch pairs (Starlink/LiDAR/beacon/spare) are 16 AWG GXL internal and external (5 m voltage-drop retune, 2026-08-22; s16 barrel ceiling); board-side terminals 45750-3112 HCS. 13 of 14 used; cavity 14 plugged.
3. **STEERING:** unchanged externally (16 AWG CAN confirmed); internal CAN pair lands in Mini-Fit HCS 16 AWG terminals (45750-1112) — OEM to confirm applicator.
4. **JETSON:** DIO set finalized — all 18 s20 positions used (DIO supply pair on the power leg + 16 signal-leg wires per the map above); nothing plugged. SEAT_EMU_SENSE has no cavity and is dropped (diagnostics-class).
5. **Molex housing/terminal line items** per the harness-side table (43025/43030 incl. 43030-0038 18 AWG, 39-01/39-00/45750, 171692/76823). Board headers are our PCBA scope, not the OEM's.
6. **J_BRG assembly:** 1× per enclosure, 20-ckt Micro-Fit double-ended per section (c).
7. **Finished external harness lengths (locked):** VEHICLE 5.0 m · ROOF 5.0 m · STEERING 1.5 m · JETSON 0.7 m ±0.1 (plug face → A4AGX connector faces, incl. 150–200 mm service loop, fan-out breakout in final 150 mm, bend radius ≥60 mm — derived from enclosure CAD). ≥5 m lines quoted with a per-meter adder for install variance; battery pair cut at 5.0 m exactly, no service coil.

**Approvals queue for Niall (per no-unapproved-substitutions — all connector PNs above are proposals, nothing ordered):** the Molex header/housing/terminal line items per the pick list (`/tmp/claude-501/board-connector-picks.md`), including 43030-0038 (18 AWG Micro-Fit terminal, e-stop loop), 171692-0104/-0102 (Mega-Fit receptacles) and 45750-3112 (16 AWG HCS — quantity now 10/enclosure: 8× J_RP + 2× J_SS); 43045-2012/43025-2000/43025-0400/39-01-2040 stock reads at order time; J50 XH→Micro-Fit migration.

## rev c (2026-08-26) — interface board rev-B pin truth + lengths + colours

- JETSON s20-9 circuit renamed: the third conditioning row is the **brake value line, DIO_OUT_BRK_VALUE** (was labelled GPIO_SPARE); J_JS pin 7 unchanged.
- JETSON s20-13 now carries **SEAT_EMU_SENSE (DIO in)** to J_JS pin 16. Ignition sense is descoped: J_BRG pin 9 is unloaded on the interface board and the T15 wire terminates at KEY_IN on the power board only. The rev-b note "SEAT_EMU_SENSE is dropped" is superseded — it took the freed cavity.
- **Leg cut lengths** stamped on every housing block: straight 2D line, receptacle station to header (positions from v32-enclosure-cad: stations x = −123/−41/+41/+123 on the front wall y = −101, boards POWER (−76,20) headers local y −61, INTERFACE (83,−10) headers local y −33), plus 2/3 of the 82 mm interior height (≈55 mm), rounded up to 10 mm. VEHICLE: J_VP1 120 / J_VP2 130 / J_VS 240. ROOF: J_RP 130 / J_RS 190. STEERING: J_SP 140 / J_SS 140. JETSON: J_JP 230 / J_JS 120. Panel switch → J50: 250.
- **Physical wire colours** locked, one per class, matching the drawing palette: PWR red, GND/returns black, CAN H yellow, CAN L green, signal white, safety chain violet. 20/18/16 AWG in UL1007/UL1015, 12 AWG battery and steering pairs in GXL red/black. ES_RX stays violet with the always-on warning label.

## rev d (2026-08-30) — ACTUAL lengths for the ceiling-hung 344 x 210 enclosure

The enclosure architecture the rev-c lengths assumed (floor-standing boards, 330 x 210 box) is superseded: the live enclosure is the 344 x 210 machined tub with BOTH boards ceiling-hung component-side down (POWER east bay at (50.5, 7.4) mounted flip-only, INTERFACE west bay at (-107, -20) mounted flip+z180), stations repacked to x = -110 / -56 / -5 / +46 on the front wall (y = -105), switch + LED at x = -145.5.

**Cut-length rule (his, 2026-08-30, replaces the 2/3-height adder):** straight plan line from the receptacle rear grommet (y = -85.3, z = 45) to the point over the board header, plus the vertical rise to that header family's entry face (board component face z = 65.4 minus family height: Mega-Fit 50.6, Mini-Fit 52.6, Micro-Fit 55.5, XH 58.4), rounded up to 10 mm.

| Leg | plan + rise | cut |
|---|---|---|
| VEHICLE pwr J_VP1 (battery 2+2, 12 AWG) | 306.7 + 5.6 | **320** |
| VEHICLE pwr J_VP2 (e-stop loop + T15) | 128.1 + 10.5 | **140** |
| VEHICLE sig J_VS | 68.3 + 10.5 | **80** |
| ROOF pwr J_RP1 | 93.0 + 7.6 | **110** |
| ROOF sig J_RS | 117.5 + 10.5 | **130** |
| STEERING pwr J_SP1 | 66.5 + 5.6 | **80** |
| STEERING sig J_SS | 138.5 + 7.6 | **150** |
| JETSON pwr J_JP1 | 141.6 + 7.6 | **150** |
| JETSON sig J_JS | 161.6 + 10.5 | **180** |
| Panel switch (z 31.5) -> J50 | 329.6 + 24.0 | **360** |
| Panel LED (z 55.5) -> J3 lamp | 113.0 + 2.9 | **120** |
| Bridge J_BRG-P <-> J_BRG-I | 93.3 + 0 | **100** |

Battery run note: J_VP1 sits at the east-bay board's far corner from the VEHICLE station, hence 320 on the 12 AWG pairs. All nine drawings regenerated with these values ("actual: straight line + vertical rise" stamped on every housing block); connector names carry the 2026-08-28 board refs (J_RP1/J_JP1/J_SP1 on the real power board).

## rev e (2026-09-01) — BASE-MOUNT lengths (supersedes rev d)

The rev-d lengths assumed the ceiling-hung boards. The live enclosure now
mounts BOTH boards component-side UP on standoffs from the 10-thick base
plate (his 2026-09-01 call — the machined ceiling pads and their JLC DFM
troubles are deleted): board slab z 16..17.6, POWER east bay (50.5, 7.4)
bench + z180 (bridge edge west), INTERFACE west bay (-107, -20) plain
bench (bridge edge east). Stations (x = -110 / -56 / -5 / +46, z 45) and
the switch/LED station (x -145.5, z 31.5 / 55.5) are unchanged.

**Cut-length rule (unchanged in form):** straight plan line from the
receptacle rear grommet (y = -85.3, z = 45) to the point over the board
header, plus the vertical drop to that header family's entry face — now
ABOVE the board (component face ~17.6 plus family height: Mega-Fit
z 32.4, Mini-Fit z 30.4, Micro-Fit z 27.4, XH z 24.5), rounded up to
10 mm. Orientation flips move several headers to different edges, so
legs change in both directions.

| Leg | plan + rise | cut (rev d) |
|---|---|---|
| VEHICLE pwr J_VP1 (battery 2+2, 12 AWG) | 265.5 + 12.6 | **280** (was 320) |
| VEHICLE pwr J_VP2 (e-stop loop + T15) | 214.8 + 17.6 | **240** (was 140 — header now on the rear edge) |
| VEHICLE sig J_VS | 74.7 + 17.6 | **100** (was 80) |
| ROOF pwr J_RP1 | 94.9 + 14.6 | **110** (unchanged) |
| ROOF sig J_RS | 83.2 + 17.6 | **110** (was 130) |
| STEERING pwr J_SP1 | 146.9 + 12.6 | **160** (was 80 — header now mid-board rear) |
| STEERING sig J_SS | 110.3 + 14.6 | **130** (was 150) |
| JETSON pwr J_JP1 | 113.8 + 14.6 | **130** (was 150) |
| JETSON sig J_JS | 180.7 + 17.6 | **200** (was 180) |
| Panel switch (z 31.5) -> J50 | 311.0 + 4.1 | **320** (was 360) |
| Panel LED feed rides in J50 (pins 3/6) | — | — |
| Lamp J3 (IFB XH) -> LED station | 74.0 + 31.0 | **110** (was 120) |
| Bridge J_BRG-P <-> J_BRG-I | 46.7 + 0 | **50** (was 100 — housings now 46.7 apart) |

All harness ends are now plugged FACE-UP on the open tray (tub off);
the receptacle pigtails tether the tub to the tray until their board-end
plugs are pulled. All nine drawings regenerated with these values.

## rev f (2026-09-01) — ceiling-standoff mount: rev-d lengths RESTORED

The base-mount excursion of rev e is reverted the same day (his call:
the boards stay on the enclosure roof). The live enclosure hangs both
boards component-side down at the SAME z as the ceiling-pad era — the
machined pad islands are replaced by F-F x18 standoffs through-bolted
from the enclosure top face (flush countersunk screws, fitted before
the Jetson) — so every world position, entry face and leg length of
rev d applies verbatim. The rev-d table is the current build table:
J_VP1 320, J_VP2 140, J_VS 80, J_RP1 110, J_RS 130, J_SP1 80, J_SS 150,
J_JP1 150, J_JS 180, switch J50 360, lamp J3 120, bridge 100. The rev-e
appendix above is design history. All nine drawings regenerated with
the restored values (footer stamped rev f).
