# V3.2 Board-Connector Pick List — FINAL (pending approval)

**Date: 2026-08-22 (rev b).** Closes the verification gaps left open in `/tmp/claude-501/internal-wiring-definition.md`. Scheme unchanged: Molex three-tier (Mega-Fit 5.7 mm / Mini-Fit Jr 4.2 mm / Micro-Fit 3.0), all board headers vertical THT (LCSC = JLC PCBA pool), crimp receptacle housings on the internal Y-split pigtail legs (Digi-Key). Genuine Molex throughout. All stock/price reads **2026-08-22**; prices are qty-1. Per the no-unapproved-substitutions rule, every PN here remains a proposal until Niall signs the approvals queue; rows that differ from the definition doc carry a **PROPOSAL** flag with the reason.

## The three corrections that matter (read first)

1. **Mega-Fit harness housings were the wrong series — both of them.** The Molex Mega-Fit family datasheet (987650-5401 Rev 9) partitions the family as: vertical headers **76829** (dual-row format, 2–12 ckt) · crimp **receptacle** housings **171692** (dual row, 2–12 ckt, female terminals 76823/172063) · crimp **plug** housings **105411** (dual row, male terminals 105417/105418, wire-to-wire only) · single-row system **200241** headers ↔ **200456** receptacles (2–8 ckt).
   - **105411-0104 is a plug housing.** It carries male terminals and mates a 171692 receptacle in wire-to-wire use; it cannot mate a 76829 header (male pins into male terminals). Disqualified.
   - **200456-1212 does not mate 76829-0002.** 200456 is the *single-row* receptacle and mates only 200241 single-row headers. 76829-0002 is a 2-circuit part in the *dual-row* housing format (one column of the dual-row shroud — catalogs listing it "1×2" blur this). Disqualified.
   - **The correct mates are 171692-0104 (4 ckt) and 171692-0102 (2 ckt)**, both deep in stock at Digi-Key, both taking the already-verified 76823-0322 12 AWG tin terminals. The datasheet confirms 171692 receptacles are compatible with all current Mega-Fit dual-row headers.
2. **The HCS terminal PN in the definition doc is the wrong gauge.** 45750-1112 is the **18–20 AWG** Mini-Fit Plus HCS female terminal (Digi-Key: 28,882 @ $0.26). The **16 AWG** part for the steering CAN pair is **45750-3112** (Digi-Key: 14,947 @ $0.26, standard stock). HCS compatibility confirmed: 45750 terminals load standard Mini-Fit Jr receptacle housings (Digi-Key associates 39-01-2040 directly with 45750-3112; Molex/Mouser: "for Mini-Fit Jr., Mini-Fit TPA and Mini-Fit BMI housings") and mate the standard 39-28 header pin — same header, different terminal, as assumed. The 13 A figure is the terminal rating with 16 AWG; here the terminal is chosen purely for its 16 AWG crimp barrel (CAN currents are negligible).
3. **18 AWG in a Micro-Fit housing needs its own terminal — and it exists.** 43030-0007 is a 20–24 AWG barrel; the 18 AWG e-stop loop wires at J_VP2 cannot legally crimp into it. The 18 AWG Micro-Fit 3.0 female terminal is **43030-0038** (tin, phosphor bronze; Molex lists it for 43025/43645/44133 receptacle housings; Digi-Key 749,392 @ $0.073, verified 2026-08-22). The loop stays 18 AWG end-to-end (Deutsch s16 barrel 16–20 AWG, Micro-Fit 3.0 carries 8.5 A with 18 AWG — loop class is ≤ 2 A); T15 at 20 AWG keeps 43030-0007. No other 18 AWG conductor lands in a Micro-Fit housing (roof/Jetson 18 AWG legs are Mini-Fit, 39-00-0039 = 18–24 AWG).

## J_SP verdict: stays Mega-Fit 2-circuit

**Keep J_SP at 76829-0002 + 171692-0102 + 76823-0322.** The 1×2 murk is resolved — the correct 2-ckt mate exists, is in production, and holds 11,182 pcs at Digi-Key — and keeping J_SP two circuits preserves the size-uniqueness between the enclosure's two high-energy power legs: a 2-ckt and a 4-ckt Mega-Fit cannot cross-mate, whereas the 2×2 fallback would put two identical Mega-Fit 4 sets on the same board (battery vs steering) with only labels between a mis-plug and 25 A on the steering branch.

## Pick table — one row per header position (11 positions)

| Position | Board | Ckts used/total | Board header (vertical THT) · LCSC · stock · $ | Mating housing · source · stock · $ | Terminals · gauge · stock | Notes |
|---|---|---|---|---|---|---|
| J_VP1 battery | PWR | 4/4 | 76829-0004 Mega-Fit 4 (2×2) · **C19170941** · 2,081 · $1.77 | **171692-0104** · Digi-Key · 7,954 · $0.72 | 4× 76823-0322 · 12 AWG · DK 32,992 @ $0.28 | **PROPOSAL: housing corrected from 105411-0104 (plug housing, not a header mate).** 2+2 poles, 12.5 A/pin at 25 A fuse ceiling |
| J_VP2 e-stop loop + T15 | PWR | 3/4 | 43045-0412 Micro-Fit 4 · C277721 · 4,668 · $0.52 | 43025-0400 · Digi-Key · 189,519 (+37.5k factory) · $0.42 | 2× **43030-0038** · 18 AWG · DK 749,392 @ $0.07; 1× 43030-0007 · 20 AWG (T15) | Pin 4 spare. Loop pins live via safety chain. **Terminal corrected: 43030-0007 is 20–24 AWG, illegal at 18 AWG** |
| J_RP roof power | PWR | 11/12 | 39-28-1123 Mini-Fit Jr 12 · C293505 · 1,140 · $0.66 | 39-01-2120 · Digi-Key · 3,079 · $0.49 | 3× 39-00-0039 (RX trio, 18–20 AWG) + 8× 45750-3112 HCS (16 AWG) · DK 14,947 @ $0.26 | Four fused branches at 16 AWG (5 m drop analysis — s16 barrel ceiling) + RX trio; pin 12 spare |
| J_SP steering | PWR | 2/2 | 76829-0002 Mega-Fit 2 (2×1) · C588521 · 365 · $1.38 | **171692-0102** · Digi-Key · 11,182 · $0.47 | 2× 76823-0322 · 12 AWG · (same reel as J_VP1) | **PROPOSAL: housing corrected from 200456-1212 (single-row family, mates 200241 headers only).** Verdict above |
| J_JP Jetson + DIO power | PWR | 4/4 | 39-28-1043 Mini-Fit Jr 4 · C293502 · 65,105 · $0.25 | 39-01-2040 · Digi-Key · 134,739 · $0.31 | 2× 39-00-0039 · 18 AWG + 2× 39-00-0039 · 20 AWG · (same reel) | 1 = JET_13V, 2 = DIO_PWR (FH3), 3 = JET_GND, 4 = DIO_GND. HCS drop-in for 18 AWG if bench runs hot is **45750-1112** (18–20 AWG, DK 28,882 @ $0.26) — the doc's PN is valid for exactly this, not for 16 AWG |
| J_BRG-P bridge | PWR | 17/20 | 43045-2012 Micro-Fit 20 · **not stocked at LCSC — GAP** · Digi-Key backfill 2,955 @ $2.88 | 43025-2000 · Digi-Key · 7,797 · $1.21 | 20× 43030-0007 · 20–22 AWG · (same reel) | **GAP: no LCSC listing exists for 43045-2012** (verified — no C-number). Board is hand-THT at JLC anyway; consign or solder the DK part. Width unique by design |
| J_VS vehicle signals | IFB | 11/16 | 43045-1612 Micro-Fit 16 · C491447 · 1,942 · $1.35 | 43025-1600 · Digi-Key · 12,104 · $0.94 | 11× 43030-0007 · 20 AWG · (same reel) | Pins 12–16 spare (brake is one cut pair on 7/8 — no returns). Same-board twin of J_JS — leg dress + labels |
| J_RS LiDAR CAN | IFB | 3/4 | 43045-0412 Micro-Fit 4 · C277721 · (shared with J_VP2) · $0.52 | 43025-0400 · Digi-Key · (shared) · $0.42 | 3× 43030-0007 · 20 AWG · (same reel) | Pin 4 spare; cross-board twin of J_VP2 — nuisance-stop worst case |
| J_SS steering CAN | IFB | 3/4 | 39-28-1043 Mini-Fit Jr 4 · C293502 · (shared with J_JP) · $0.25 | 39-01-2040 · Digi-Key · (shared) · $0.31 | 2× **45750-3112 HCS** · **16 AWG** · DK 14,947 @ $0.26; 1× 39-00-0039 · 20 AWG (SIG_GND) | **PROPOSAL: HCS terminal corrected from 45750-1112 (that PN is 18–20 AWG) to 45750-3112 (16 AWG).** Mates standard 39-28 header — verified |
| J_JS Jetson signals | IFB | 16/16 | 43045-1612 Micro-Fit 16 · C491447 · (shared with J_VS) · $1.35 | 43025-1600 · Digi-Key · (shared) · $0.94 | 16× 43030-0007 · 20 AWG · (same reel) | Full: CAN1/2 + DIO out ×2 + GPIO_SPARE + DIO in ×4 + I²C/host + SIG_GND (J12 deleted — status rides here). Stays 16-ckt; J_BRG 20 width unique |
| J_BRG-I bridge | IFB | 17/20 | 43045-2012 Micro-Fit 20 · **LCSC GAP** · Digi-Key 2,955 @ $2.88 | 43025-2000 · Digi-Key · (2nd of the pair) · $1.21 | 20× 43030-0007 · 20–22 AWG · (same reel) | Second end of the single J_BRG assembly |

## Per-enclosure cost rollup (qty-1 pricing, loaded contacts only, no attrition)

| Class | Detail | Cost |
|---|---|---|
| Board headers (11) | 2× Mega-Fit ($3.15) + 3× Mini-Fit ($1.16) + 6× Micro-Fit ($9.51, incl. 2× 43045-2012 @ DK $2.88) | **$13.82** |
| Housings (10) | 171692-0104 + 171692-0102 ($1.19) + 3× Mini-Fit ($1.11) + 5× Micro-Fit incl. 2× 20-ckt ($5.14) | **$7.44** |
| Terminals (97) | 6× 76823-0322 ($1.68) + 71× 43030-0007 ($14.20) + 2× 43030-0038 ($0.15) + 8× 39-00-0039 ($1.36) + 10× 45750-3112 ($2.60) | **$19.99** |
| **Total per enclosure** | | **≈ $41.25** |

Crimp attrition and fleet-quantity price breaks both push real cost per enclosure toward ~$35–45; order terminals in 100s.

## J50 migration (XH-6 → Micro-Fit 6) — APPLIED in schematic revision c (PROPOSAL, pending approval)

Verified 2026-08-22 (re-verified at rev-c edit time: **C234188 still 63 pcs @ $0.5454**): header **43045-0612** LCSC **C234188** (thin; Digi-Key carries the same PN as backfill, hand-THT anyway — same treatment as J_BRG); housing **43025-0600** Digi-Key **96,959** @ $0.51; 6× 43030-0007 ($1.20). Adds ≈ **$2.26**/enclosure and puts the last board-to-panel connector on latched crimp hardware in the same Micro-Fit ecosystem. **Landed in `v32-power-board-swept.kicad_sch` revision c (md5 `26db7fab0b9839e142058d3530111749`): ref J50 kept, pin map 1 LED_A / 2 SW_ARM / 3 ES_FEED / 4 PWR_SW / 5+6 GND preserved net-for-net; Micro-Fit 6 is 2×3 dual-row (rows 1-2-3 / 4-5-6) vs the old single-row XH — pin numbers map 1:1, arrangement drawn on the panel wiring diagram.** PROPOSAL like every other row — nothing ordered.

## Kit master switch + status LED (panel, wired to J50) — PROPOSAL, pending approval

| Item | PN | Source · stock · $ (2026-08-22) | Notes |
|---|---|---|---|
| Master switch | **NKK WT22S** | Digi-Key · 322 (+179 factory) · $34.08 | DPDT ON-ON (the schematic's MTS-202 role), IP67 bootless, M12×1 threaded bushing + D-hole anti-rotation flat (screw-in rule), 10 A/30 VDC, solder lugs. Panel cutout Ø12.5/11.2 flat, wall ≤4.0. REAL STEP fetched no-login via the DK-linked NKK CADENAS portal (`cad-assembly/vendor/NKK-WT22S/WT22S.stp`) |
| Status LED | **APEM Q8P1CXXHG02E** | Digi-Key · 312 · $24.21 | Green diffused dome, **2 V/20 mA bare LED — matches the R58 1k on-board drive (~10 mA)**, Ø8.13 cutout, threaded bushing, IP67. Own panel hole (Ø8.2 cut in CAD) |
| Switch runner-ups | C&K 7201TCWZGE ($23.87/250) · Carling 2M1-DP1-T6-B1-M1QE ($8.25/630) · TE 3-6437592-9 ($42.36/304) | see `/tmp/claude-501/switch-sourcing.md` | C&K: no verified no-login STEP; Carling: 1/4-40 miniature bat; TE: On-Off-On only |

Full evaluation (option a-vs-b: sealed illuminated bushing-mount switches don't exist in distribution; separate-LED wins): `/tmp/claude-501/switch-sourcing.md`.

## What changed vs the definition doc

1. **J_VP1 housing: 105411-0104 → 171692-0104** (PROPOSAL). 105411 is the Mega-Fit wire-to-wire plug housing (male terminals); it never mates a header. Datasheet-verified; terminals unchanged (76823-0322).
2. **J_SP housing: 200456-1212 → 171692-0102** (PROPOSAL). 200456 is the single-row receptacle for 200241 headers; 76829-0002 is dual-row format. J_SP stays 2-circuit — the 2×2 fallback was considered and rejected for creating an identical-pair mis-plug hazard between the two power legs on the same board.
3. **J_SS 16 AWG terminals: 45750-1112 → 45750-3112** (PROPOSAL). 45750-1112 is 18–20 AWG; it stays on the books only as the J_JP hot-bench drop-in. HCS-in-standard-housing/header compatibility confirmed.
4. **43045-2012 has no LCSC listing** (GAP, not a substitution): J_BRG headers come from Digi-Key (2,955 @ $2.88 each, 2 per enclosure) and are hand-loaded like every other header at JLC.
5. **Stock re-reads, 2026-08-22, unchanged from the definition doc:** C491447 = 1,942 · C19170941 = 2,081 · C293505 = 1,140. Nothing in either stock table has gone to zero; thinnest lines are 76829-0002 (LCSC 365) and 43045-0612 (LCSC 63).
6. Optional note: 171692-0204 (tangless TPA-capable 4-ckt, DK 20,535 @ $1.13) plus the 105415 TPA retainer is the vibration-hardened variant of the battery housing if the roller deck proves unkind; not specified today to keep the line-item count down.

**Approvals queue:** all PNs above (headers, housings, terminals incl. 43030-0038), the PROPOSAL corrections, the J_BRG Digi-Key backfill, the J50 migration, and the panel kit-master-switch set (NKK WT22S + APEM Q8P1CXXHG02E). Nothing ordered.
