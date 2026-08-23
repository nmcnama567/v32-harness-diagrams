# V3.2 Harness Length + Wire Gauge Sizing Pass — analysis + edit list

**Date: 2026-08-22.** Companion to `/tmp/claude-501/internal-wiring-definition.md` (rev b),
`/tmp/claude-501/board-connector-picks.md` (rev b), `/tmp/claude-501/receptacle-diagrams/wire-map.md`,
and the CAD assembly manifest (`/tmp/claude-501/cad-assembly/manifest.md`). **This file is analysis +
edit instructions only — nothing has been applied.** The applier agent executes section (c) after the
in-flight doc pass lands.

**Length spec (Niall, verbatim intent):** all external harnesses ≥5 m, EXCEPT steering ≈1.5 m, and
JETSON, which only reaches from the enclosure's JETSON receptacle up over the enclosure edge to the
Jetson on top — slack for easy install, no waste. Locked numbers used throughout:

| Harness | Finished length | Basis |
|---|---|---|
| VEHICLE | **5.0 m** | floor spec |
| ROOF | **5.0 m** | floor spec |
| STEERING | **1.5 m** | Niall's ≈1.5 m |
| JETSON | **0.7 m ± 0.1 m** | computed from CAD geometry, §5 |

**Method.** Copper per ASTM B258 solid at 20 °C (stranded GXL/TXL ≈ +2 %, absorbed by the 60 °C
factor's conservatism): 12 AWG 5.211 · 14 AWG 8.286 · 16 AWG 13.17 · 18 AWG 20.95 · 20 AWG
33.31 mΩ/m. Hot factor ×1.157 (60 °C, α = 0.00393/°C — applied to **every** run: engine bay obviously,
and black loom in Buda sun reaches 60 °C on the roof mast too). Hot values used in all tables:
12 → 6.03 · 14 → 9.59 · 16 → 15.24 · 18 → 24.24 · 20 → 38.54 mΩ/m.
Loop resistance R = 2 × (L_ext + **0.4 m internal pigtail allowance**) × r_hot (battery: 2 conductors
per pole → per-pole R halved). Connector contacts + fuse add ~10–15 mΩ on the battery pair only —
noted there, ignored elsewhere.
**Pass criteria** (rail = 13.0 V): drop ≤ 3 % (0.39 V) at **working** current for power branches;
3–5 % (0.65 V) acceptable with justification; fuse-ceiling drop shown informatively as a
delivered-voltage floor. **Battery input is exempt from the % rule** — evaluated on power loss and
the 9 V UVLO floor in the 12 V-machine cranking case (§2.1).

---

## (a) Summary verdict table

| Circuit (harness) | Verdict | AWG | Terminal PN impact |
|---|---|---|---|
| BAT+ / BAT− 2+2 (VEHICLE) | **keep — barrel ceiling** | 12 ×2/pole | none (76823-0322); crank-margin note §2.1 → Niall item N3 |
| ESTOP_LOOP_FWD/RET (VEHICLE) | keep | 18 | none (43030-0038) |
| T15_KEY (VEHICLE) | keep | 20 | none |
| SEAT, BRK pair, ECU/JOY/SPARE CAN (VEHICLE) | keep | 20 | none |
| STARLINK_13V/GND (ROOF) | **CHANGE 18 → 16** | 16 | J_RP: 2× 39-00-0039 → 2× **45750-3112** HCS |
| LIDAR_13V/GND (ROOF) | **CHANGE 18 → 16** | 16 | J_RP: 2× → 2× 45750-3112 |
| BCN_13V/GND (ROOF) | **CHANGE 18 → 16** | 16 | J_RP: 2× → 2× 45750-3112 |
| SPARE_13V/GND FH8 (ROOF) | **CHANGE 18 → 16** (barrel max — see Niall item N1) | 16 | J_RP: 2× → 2× 45750-3112 |
| ES_RX / RX_GND (ROOF) | keep | 18 | none (39-00-0039) |
| RX_STAT (ROOF) | keep | 20 | none |
| LIDAR_CAN pair (ROOF) | keep — topology note §4 | 20 | none |
| STR_13V/GND (STEERING) | keep — 1.6 % @ 9 A | 12 | none |
| STR_CAN pair (STEERING) | keep (barrel-forced) | 16 | none (45750-3112, as picked) |
| JET_13V/GND (JETSON) | keep — short harness makes it legal | 18 | none; N-seal OD check → Niall item N5 |
| DIO_PWR/GND (JETSON) | keep | 20 | none |
| All JETSON signals, J_BRG | keep | 20/22 | none |

Net: **4 circuits changed (8 conductors, all ROOF power)**. Terminal deltas: 39-00-0039 16 → **8**,
45750-3112 2 → **10** per enclosure (+$0.72). No housing, header, panel-contact, or insert changes
anywhere — the 16 AWG bump sits inside the s16 barrel (16–20 AWG) and the HCS terminal loads the
same 39-01-2120 housing and mates the same 39-28-1123 header.

---

## (b) Arithmetic

### 1. ROOF power branches — 5.0 m, the prime suspects (confirmed)

Loop length 2 × (5.0 + 0.4) = 10.8 m. R_loop: 18 AWG = 10.8 × 24.24 m = **0.262 Ω**;
16 AWG = 10.8 × 15.24 m = **0.165 Ω**. Working-current assumptions: Starlink 3.0 A (Mini-class,
~40 W — confirm hardware, Niall item N2), LiDAR 1.5 A (~20 W), beacon 1.2 A (~15 W LED), spare
undefined → judged at fuse ceiling.

| Branch | I work / fuse | AWG as-spec | R loop | V-drop work / fuse | % rail work / fuse | W work / fuse | Flag |
|---|---|---|---|---|---|---|---|
| STARLINK (FH4) | 3.0 / 5.0 A | 18 | 0.262 Ω | 0.79 / 1.31 V | **6.0 % / 10.1 %** | 2.4 / 6.5 W | **FAIL** — over 5 % at working |
| LIDAR pwr (FH7) | 1.5 / 5.0 A | 18 | 0.262 Ω | 0.39 / 1.31 V | **3.0 % / 10.1 %** | 0.6 / 6.5 W | at the 3 % line; fuse-case floor 11.7 V |
| BEACON (FH5) | 1.2 / 5.0 A | 18 | 0.262 Ω | 0.31 / 1.31 V | 2.4 % / 10.1 % | 0.4 / 6.5 W | passes working; fuse-case floor poor |
| SPARE (FH8) | — / 7.5 A | 18 | 0.262 Ω | — / 1.96 V | — / **15.1 %** | — / 14.7 W | **FAIL** — spare delivers 11.0 V at ceiling |

Same rows at **16 AWG** (the fix):

| Branch | I work / fuse | R loop | V-drop work / fuse | % rail | Delivered V at fuse | Verdict |
|---|---|---|---|---|---|---|
| STARLINK | 3.0 / 5.0 A | 0.165 Ω | 0.49 / 0.82 V | **3.8 %** / 6.3 % | 12.18 V | pass with justification: 3.8 % < 5 %; load is a wide-input converter; floor check → N2 |
| LIDAR pwr | 1.5 / 5.0 A | 0.165 Ω | 0.25 / 0.82 V | 1.9 % / 6.3 % | 12.18 V | pass |
| BEACON | 1.2 / 5.0 A | 0.165 Ω | 0.20 / 0.82 V | 1.5 % / 6.3 % | 12.18 V | pass |
| SPARE | — / 7.5 A | 0.165 Ω | — / 1.23 V | — / 9.5 % | 11.77 V | barrel ceiling — within-5 % deliverable = 0.65/0.165 = **3.9 A**; → N1 |

Why not 14 AWG: 14 AWG would give Starlink 0.31 V (2.4 %) at working — but **14 AWG does not fit an
s16 barrel (16–20 AWG)**. 16 is the ceiling on HD34-18-14PE without a panel-insert change (→ N1).
Uniform 16 AWG across all four pairs = one spool, one crimp setting, one terminal reel; +$0.72/enclosure.
Ampacity: 16 AWG GXL bundled is good for ≥10 A — the 7.5 A FH8 fuse still coordinates. Dissipation at
worst case 9.3 W over 10.8 m = 0.86 W/m — thermally trivial.

### 2. VEHICLE — 5.0 m

**2.1 Battery (2× 12 AWG per pole, F1 = 25 A).** Per-pole one-way R = 5.4 m × 6.03 / 2 = 16.3 mΩ;
**loop (both poles) = 32.6 mΩ** wire-only; fuse + 8 Mega-Fit/Deutsch contacts add ~10–15 mΩ (shown
separately, not in the wire numbers).

| Case | I | V-drop (wire) | Loss | Note |
|---|---|---|---|---|
| Working (≈230 W in at 12 V) | 20 A | 0.65 V | 13.0 W | 5.3 % of transferred power; 1.2 W/m over the 4-wire bundle — thermally fine |
| Fuse ceiling | 25 A | 0.81 V | 20.4 W | — |
| **Cranking, full load** | 26.8 A | 0.87 V | 19.5 W | battery 10.0 V → box sees **9.13 V** — 0.13 V above the 9 V UVLO |
| Cranking, shed load (~120 W) | 14.2 A | 0.46 V | — | battery threshold for UVLO-clean ≈ **9.5 V** |

Crank math (constant-power in): V_box² − V_bat·V_box + P·R/η = 0 with P = 230 W, η = 0.94,
R = 32.6 mΩ → at V_bat = 10.0 V, V_box = 9.13 V; the box stays above 9 V UVLO only while the battery
terminal stays ≥ **9.9 V** at full load (≥ 9.5 V at 120 W boot load). A hard diesel crank can dip
below that. **No gauge fix exists inside the locked barrels** — s12 contact is 12–14 AWG and
76823-0322 is a 12 AWG barrel, and 2+2 already uses all four s12 cavities. Ride-through is the
CB-001 supercap bank's job (KO_SUPERCAP provision). → Niall item N3. Practical note for the RFQ: the
battery pair benefits from being built at 5.0 m exactly — no service coil.

**2.2 The rest of VEHICLE (one line each).**
E-stop loop, 18 AWG, loop 0.262 Ω: at the ≤2 A seat-circuit class worst case 0.52 V across a switched
safety loop (series with relay coils, tens of Ω) — **confirmed 18 AWG**; realistic 0.5 A → 0.13 V.
T15_KEY, 20 AWG single-ended: ~5 mA through R91 → < 3 mV — **confirmed**.
Seat / brake pair / all 20 AWG signal + CAN conductors: bias currents < 20 mA on 0.42 Ω loop → < 9 mV,
**negligible — this one statement covers every 20 AWG signal line at every length in the system.**

### 3. STEERING — 1.5 m

Loop 2 × 1.9 = 3.8 m; 12 AWG R_loop = **22.9 mΩ**.

| Case | I | V-drop | % rail | W |
|---|---|---|---|---|
| Working | 9 A | 0.21 V | **1.6 %** | 1.9 |
| Transient | 16 A | 0.37 V | 2.8 % | — |
| Fuse (FH6 15 A ATO) | 15 A | 0.34 V | 2.6 % | — |

**12 AWG stays** — under 3 % all the way to 17 A continuous. The 1.5 m spec is load-bearing: at 5 m
this pair would run 0.59 V (4.5 %) working and 1.05 V (8.0 %) on transients. Steering CAN 16 AWG
(barrel-forced) unchanged.

### 4. CAN / signal notes

Signal-level drops: covered once in §2.2 — negligible everywhere, verified.

**Topology at the spec lengths** (guideline numbers per the NI CAN physical-layer table:
max single unterminated stub ≈ **5.5 m @ 500 kbit/s**, ≈ **11 m @ 250 kbit/s**; total bus
250 m @ 250k / 100 m @ 500k):

- **VEHICLE ECU + JOY pairs = bus segments**, not stubs — the enclosure is an in-line MITM node on
  the machine bus. 5 m adds nothing against a 100–250 m budget. No termination change; the machine
  ends stay terminated, SJ1/SJ2 on the interface board stay per the existing commissioning rule.
- **CAN-A taps are stubs**: steering 1.5 m + LiDAR 5 m (+ spare 5 m if ever used).
  At **250 kbit/s**: 5 m < 11 m single-stub limit, cumulative 6.5–11.5 m — **complies as drawn**
  (both on-board terminations per SJ1/SJ2).
  At **500 kbit/s**: the 5 m LiDAR tap is 91 % of the single-stub limit and the ensemble is out of
  comfort — **revisit the termination scheme**: populate exactly ONE 120 Ω on the interface board
  (SJ1 or SJ2) and place the second termination at the LiDAR node, turning the 5 m roof run into
  terminated trunk; steering's 1.5 m becomes the only stub (legal at 500k). Spare tap then usable
  only at 250k or as a terminated extension. Bitrate confirmation → Niall item N4.
- **JET_CAN1/2 at 0.7 m**: point-to-point, terminate both ends per existing provision — no issue.

### 5. JETSON harness — computed length spec

Geometry from `/tmp/claude-501/cad-assembly/manifest.md` (enclosure 330 × 210 × 86, lid z 86–90,
Jetson plate plane z 94, stack top z 195):

- Panel outer face y = −105 (210 deep, centered); receptacle mating faces ≈ y = −127 (22.2 mm proud —
  assembly bbox front extreme). Receptacle centerline **z = 45**, stations x ∈ {−123, −41, +41, +123};
  **group→station mapping not asserted by the CAD** — worst case carried below.
- A4AGX connector face y = **−95.1** (9.9 mm behind the panel plane — the run goes up the harness
  face, it never actually crosses the lid edge), chassis z 94–195, connector cluster est. z 110–180,
  face spans x ±149.
- HD36 plug + backshell wire exit ≈ 75 mm beyond the mating face → y ≈ −200 at z = 45.
- Path legs (Manhattan + bend allowance): double-back toward the face ~50 mm · climb Δz 105–135 mm ·
  lateral Δx 0–270 mm (worst station-to-connector offset) · connector entry ~50 mm · +~30 mm for two
  90° bends at R ≥ 60 mm (bundle: 20 conductors, Ø ≈ 12–13 mm loomed; min static bend ≈ 5× OD).
- Tip-to-tip: best ≈ 0.39 m, worst-lateral ≈ 0.58 m; + **150–200 mm service loop** (lets the lid lift
  with the Jetson attached and gives connector-unplug access).

**Spec: 0.7 m ± 0.1 m**, plug mating face → Jetson connector faces, fan-out breakout to the A4AGX
connectors in the final 150 mm, min bend radius 60 mm. If the enclosure-face freeze later pins the
JETSON station directly under the A4AGX connector cluster, trim to 0.6 m ± 0.1.

**Gauge at that length — trivial, one number:** JET_13V/GND 18 AWG, loop 2 × (0.7 + 0.4) = 2.2 m →
53 mΩ → **0.25 V (1.9 %) at the 4.6 A real draw** (0.40 V / 3.1 % at the 7.5 A fuse) — 18 AWG
confirmed. (At 5 m it would have been 1.21 V / 9.3 % — the short spec is what keeps 18 AWG legal.)
DIO_PWR/GND 20 AWG: 0.35 A × 85 mΩ = 30 mV — confirmed. All signals: §2.2.

---

## (c) EDIT LIST — for the applier agent (apply after the in-flight doc pass lands; re-locate line numbers if that pass moved them)

### C1. `/tmp/claude-501/internal-wiring-definition.md`

1. ROOF table (§a, lines 54–66): AWG cell **18 → 16** on exactly these 8 rows — cavity 1
   STARLINK_13V, 2 STARLINK_GND, 3 LIDAR_13V, 4 LIDAR_GND, 5 BCN_13V, 6 BCN_GND, 12 SPARE_13V,
   13 SPARE_GND. **Do not touch** cavity 9 ES_RX (18), 10 RX_STAT (20), 11 RX_GND (18).
2. Header roster (line 116): `J_RP Mini-Fit Jr 12 (roof branches + RX trio)` → append
   `— branch pairs 16 AWG on 45750-3112 HCS terminals, RX trio on 39-00-0039`.
3. "Current vs rating, derated" table, Roof row (line 170):
   `Mini-Fit Jr 9 A (≈7 A fully-loaded derate) | ≤71 % — fine` →
   `Mini-Fit Jr, branch pins on HCS terminals (13 A) | ≤5 A on 13 A = ≤38 %; RX trio ≪1 A — fine`.
4. RFQ addendum item 2 (line 209): after the RX-trio sentence append: `The four branch pairs
   (Starlink/LiDAR/beacon/spare) are 16 AWG GXL internal and external (5 m voltage-drop retune,
   2026-08-22; s16 barrel ceiling); board-side terminals 45750-3112 HCS.`
5. RFQ addendum, new numbered item 7 — harness lengths: `**Finished external harness lengths
   (locked):** VEHICLE 5.0 m · ROOF 5.0 m · STEERING 1.5 m · JETSON 0.7 m ±0.1 (plug face → A4AGX
   connector faces, incl. 150–200 mm service loop, fan-out breakout in final 150 mm, bend radius
   ≥60 mm — derived from enclosure CAD). ≥5 m lines quoted with a per-meter adder for install
   variance; battery pair cut at 5.0 m exactly, no service coil.`
6. Approvals queue (line 215): in the 45750-3112 mention, note quantity is now **10/enclosure**
   (8× J_RP + 2× J_SS).

### C2. `/tmp/claude-501/board-connector-picks.md`

1. Pick table, J_RP row (line 24), terminals cell: `11× 39-00-0039 · 18–24 AWG · DK 464,782 @ $0.17`
   → `3× 39-00-0039 (ES_RX/RX_GND 18 AWG, RX_STAT 20 AWG) + 8× 45750-3112 HCS · 16 AWG · DK 14,947
   @ $0.26`; Notes cell append: `Branch pairs 16 AWG per the 5 m drop analysis
   (harness-length-gauge-analysis.md). HCS loads standard Mini-Fit Jr housings — confirm the
   39-01-2120 association at order (verified family-wide via 39-01-2040).`
2. Correction #3 (line 12), parenthetical `(roof/Jetson 18 AWG legs are Mini-Fit, 39-00-0039 =
   18–24 AWG)` → `(Jetson 18 AWG legs are Mini-Fit 39-00-0039; roof branch legs went 16 AWG on
   45750-3112 HCS in the length/gauge pass; RX trio stays 39-00-0039)`.
3. Cost rollup (lines 40–41): `71× 43030-0007 ($14.20)` unchanged; `16× 39-00-0039 ($2.72)` →
   `8× 39-00-0039 ($1.36)`; `2× 45750-3112 ($0.52)` → `10× 45750-3112 ($2.60)`; Terminals total
   `$19.27` → `$19.99`; grand total `≈ $40.53` → `≈ $41.25`. Terminal count stays 97.

### C3. Diagrams — regenerate, don't hand-edit

1. Data source: scratchpad `gen_diagrams.py` (`/private/tmp/claude-501/-Users-…-My-Drive/8521ca48-…/
   scratchpad/gen_diagrams.py`) — change `"18"` → `"16"` on exactly 8 ROOF rows: lines 101–104
   (STARLINK_13V, LIDAR_13V, BCN_13V, SPARE_13V) and 107–110 (STARLINK_GND, LIDAR_GND, BCN_GND,
   SPARE_GND). **Leave** line 105 ES_RX `"18"`, line 111 RX_GND `"18"`, lines 62–63 e-stop `"18"`,
   lines 169/171 JET pwr `"18"`.
2. Regenerate via scratchpad `gen2.py`, then `receptacle-diagrams/export.sh` — only
   `roof-internal.{svg,png}` and `roof-pinout.{svg,png}` change content.
3. Verification strings (must appear in the regenerated roof SVGs, old → new):
   `STARLINK_13V (FH4 5A) · 18 AWG` → `… · 16 AWG`; `STARLINK_GND · 18 AWG` → 16;
   `LIDAR_13V (FH7 AUX 5A) · 18 AWG` → 16; `LIDAR_GND · 18 AWG` → 16;
   `BCN_13V (FH5·K53 5A) · 18 AWG` → 16; `BCN_GND · 18 AWG` → 16;
   `SPARE_13V (FH8 7.5A) · 18 AWG` → 16; `SPARE_GND · 18 AWG` → 16.
   In `roof-pinout.svg` the AWG table column: rows A/B/C/D/E/F/M/N `18` → `16`; rows J/L stay `18`,
   row K stays `20`. Strings that must remain: `ES_RX (ALWAYS-ON) · 18 AWG`, `RX_GND · 18 AWG`,
   `RX_STAT · 20 AWG`. The other six diagrams must be byte-equivalent in their label content.

### C4. `/tmp/claude-501/receptacle-diagrams/wire-map.md`

**No row changes** — the map carries circuits/cavities only, no gauges. Only if the applier bumps the
diagram set: update the header date line to note the roof 16 AWG regeneration.

### C5. `/tmp/claude-501/panel-connector-options.md` — RFQ line list (§ line 82–91) + lengths

1. Add a **Length** entry per group row (or a lengths preamble line above the table):
   VEHICLE `5.0 m`; ROOF `5.0 m`; STEERING `1.5 m`; JETSON `0.7 m ±0.1 — receptacle up the harness
   face to the A4AGX connector cluster on the lid; includes 150–200 mm service loop (lid lift-off
   with Jetson attached); fan-out breakout in final 150 mm; no excess length`. Wording for the two
   5 m lines: `5.0 m finished, plug face to machine-end termination; quote per-meter adder`.
2. ROOF row (line 89): `LED 2× 18 AWG` → `beacon 2× 16 AWG`; `spare pair 2× 18 AWG` →
   `spare pair 2× 16 AWG` (Starlink/LiDAR pwr already read 16 AWG — now all four pairs match);
   `e-stop RX 2× 18 AWG` → `e-stop RX trio: ES_RX + RX_GND 2× 18 AWG, RX_STAT 1× 20 AWG (cavities
   J/K/L)`; `LiDAR CAN 1× 18 AWG twisted pair` → `1× 20 AWG TXL twisted pair (per rev-b internal
   doc)`.
3. VEHICLE row (line 88) is stale vs rev b — harmonize: `e-stop fwd/ret 2× 14 AWG` →
   `2× 18 AWG GXL (moved to s16 cavities A/C, rev b)`; `seat 2×, joystick brake 2×, ECU brakes 2×
   16–18 AWG` → `seat 2×, brake cut pair 2× (BRK_JOY/BRK_ECU, one twisted pair, no returns) ·
   20 AWG TXL`; `ECU CAN, joystick CAN, spare CAN 3× 18 AWG TXL twisted pairs` → `… 3× 20 AWG TXL
   twisted pairs`; add `T15 key-sense 1× 20 AWG (cavity V, splice-point per machine tap)`; contact
   count `s16 ×12 (+5 plugged)` → `s16 ×13 (+3 plugged: P, S, X)`.
4. JETSON row (line 91): `s20 ×9–11 (rest plugged)` → `s20 ×18 (all used, rev b — nothing plugged)`;
   keep `pwr +/− 2× 16 AWG` (N-seal constraint; internal side stays 18 AWG — mixed gauge across the
   contact is legal, both barrels compliant, pending N5).

### C6. Notion (apply per the Notion pipeline rules; PNG re-upload per notion-image-pipeline)

1. **Internal-wiring/enclosure page** (the page section (d) of the definition doc was applied to):
   search the page for `18 AWG` — every occurrence attached to a ROOF branch circuit
   (STARLINK/LIDAR pwr/BCN/SPARE_13V/GND bullets or table cells) → `16 AWG`; occurrences for
   ES_RX/RX_GND/e-stop/JET_13V stay. Update any J_RP terminal mention to the 3× 39-00-0039 +
   8× 45750-3112 split. Add the locked-lengths bullet (same four numbers + Jetson slack wording as
   C1.5).
2. Re-upload `roof-internal.png` + `roof-pinout.png` wherever embedded (PNG-only via Chrome paste +
   source_url relay; single-attach upload IDs).
3. **Interface-board design page**: no edit now — the SJ1/SJ2 CAN-A termination change is conditional
   on Niall's N4 bitrate answer; add nothing until he rules.

---

## (d) Niall's calls — flagged, not decided

- **N1 — SPARE FH8 vs the s16 ceiling.** 16 AWG is the largest wire an s16 cavity takes; at 5 m the
  spare branch delivers 3.9 A within 5 % drop, and 11.77 V at the full 7.5 A ceiling. Options: accept
  and document the delivered-voltage curve; re-fuse FH8 7.5 → 5 A; or reserve FH8 for
  non-voltage-critical loads. Going bigger than 16 AWG means a different ROOF insert (panel connector
  change) — not proposed.
- **N2 — Starlink hardware floor.** Numbers assume Mini-class (12–48 V input, ~40 W working). At
  16 AWG the roof end sees 12.51 V working / 12.18 V at the 5 A fuse ceiling — 0.18 V above a 12 V
  floor at absolute worst case. Confirm the actual roof unit and its minimum input; if it is tighter
  than 12 V, this needs a decision (roof-side DC-DC or branch rework), not a gauge tweak.
- **N3 — Battery crank ride-through.** At 5 m the box loses ~0.9 V during a full-load crank and
  UVLOs if the 12 V battery dips below ≈9.9 V at its terminals. 2× 12 AWG per pole is the ceiling of
  both barrels (s12 contact 12–14 AWG, 76823-0322 12 AWG). Confirm the CB-001 supercap bank is sized
  for crank ride-through; if not, the alternatives (10 AWG s12 contact variants + battery-side
  terminal change, or load-shed-at-crank logic) are his call.
- **N4 — CAN-A bitrate.** 250 kbit/s: the 5 m LiDAR + 1.5 m steering stub scheme complies as drawn.
  500 kbit/s: adopt the far-end-termination scheme (one on-board 120 Ω via SJ1/SJ2, second at the
  LiDAR node). Needs the protocol sheet's number before C6.3 or any board doc changes.
- **N5 — JETSON s16 N-seal vs 18 AWG internal pigtail.** HD34-18-20PN N seals want 16 AWG-class
  insulation OD on the s16 cavities; 18 AWG GXL (~2.85 mm / 0.112″) sits at the seal-range edge.
  Have the OEM confirm seal fit, or bump the two internal JET pwr conductors to 16 AWG — which would
  force 2× 45750-3112 at J_JP pins 1/3 (drop numbers pass either way at 0.7 m).
