# Kit master switch — sourcing (2026-08-22)

Panel master ON/OFF for the V3.2 enclosure front face. Electrical role (read from the
landed power schematic, J50 region): **two poles, logic-class** — pole 1 jumpers
ES_FEED (J50.3, /ES_RX via R92 470R) onto SW_ARM (J50.2 → R57 → Q50 BCP56-16
emitter-follower → K50 master-relay coil); pole 2 grounds PWR_SW (J50.4, R61 470k
pull-up to VCAP_IN, Q53 gate) to enable the LM5176. Switched current ≪ 100 mA at
~13 V — the 25 A path lives in K50, never in the switch. The schematic's own note at
(397.5, 66.0) reads "PANEL: MTS-202 DPDT + STATUS LED" — the circuit was drawn for a
**DPDT ON-ON** toggle (task brief said SPST/SPDT; the as-built circuit needs two
poles, so DPDT ON-ON wired as a two-pole ON/OFF is the correct class; flagged, not
silently changed). Status LED is a separate 2-wire circuit: LED_A (J50.1, fed from
the K50 coil node through R58 1k — a **bare-LED ~10 mA drive**) + GND return.

## Option (a) vs (b)

- **(b) sealed illuminated switch merging the LED — REJECTED.** Digi-Key toggle
  category, Illuminated + IP67 + threaded bushing: zero live parts (checked
  2026-08-22; the only IP67 bushing-mount toggles in distribution are all
  Non-Illuminated — NKK M/WT, C&K 7000, Carling 2M, TE AW, Honeywell NT). IP67
  illuminated switches exist only as anti-vandal pushbuttons (wrong actuation — a
  master switch must show its state by lever position) and snap-in rockers (violates
  the screw-in mounting rule). Lamp-drive would also mismatch: integrated 12/24 V
  lamps carry internal resistors, and behind R58 1k they run at roughly half
  brightness; the board drive is designed for a bare LED.
- **(a) plain sealed DPDT toggle + separate sealed panel LED — SELECTED.**

## Selected switch — NKK WT22S (PROPOSAL, pending Niall's approval)

DPDT ON-NONE-ON, solder lug. Digi-Key 360-3379-ND, **322 in stock + 179 factory,
$34.08 qty-1 / $29.41 qty-10** (verified 2026-08-22).

Why this one: it is the exact function the schematic note asks for (MTS-202-class
DPDT ON-ON, wired common+one-side as a two-pole ON/OFF); the switch itself is IP67
at the front panel **without a boot** (inner + outer nitrile seals, epoxy-sealed
base — nothing to tear off on a roller deck; NKK boots stay available as an
option); the M12 × 1 chrome-brass bushing is a true threaded-bushing mount
(screw-in rule) with a **flatted bushing + D-hole anti-rotation**; the 17.5 mm
chrome bat is glove-friendly; contacts are rated 10 A @ 30 VDC — two orders above
the coil/logic load, and NKK's interlocked-contactor mechanism is specified to
break light welds at low-current use; −30…+70 °C; max panel 4.0 mm = exactly the
enclosure wall. And it clears the hard gate: real manufacturer STEP, no login (below).

- Datasheet: https://www.nkkswitches.com/pdf/WT.pdf (saved `/tmp/claude-501/switch/WT-datasheet.pdf`)
- Panel cutout: **Ø12.5 mm D-hole, flat truncating to 11.2 mm** (flat-to-opposite-arc), panel ≤ 4.0 mm
- Standard hardware, supplied: AT503M chrome-brass hex face nut (≈Ø16 × 2.4), internal-tooth lockwasher, AT401P nitrile O-ring (Ø17.5 × 1.5, behind-flange panel seal)
- Behind-panel: solder-lug body (rear IP60; lives inside the IP66+ enclosure — acceptable; wire-lead WT22L is the IP67-rear variant if ever needed)

### STEP provenance (hard requirement — satisfied)

Digi-Key product page → "WT22S CAD" (manufacturer model link) →
`nkkswitches.com/distributor-landing-page/?part_no=WT22S&vendor=digikey` → NKK's
embedded CADENAS portal (nkkswitches-dist-embedded.partcommunity.com). Configured
WT22S (poles 2 / circuit 2 / terminals S), generated STEP AP214, downloaded with
**no login** (guest session; cookie banner = Reject all).
File: `/tmp/claude-501/cad-assembly/vendor/NKK-WT22S/WT22S.stp` (284 KB, ISO-10303-21
AP214, CADENAS/PARTsolutions export, license CC BY-ND 4.0)
Zip sha256: `3704c23f9bcc32fc64f5cea6748c8431bc95d3b77c6e1d1c75123f7e07038434`

## Runner-ups (all in stock 2026-08-22, all DPDT unless noted)

| PN | Mfr | Price | Stock | Why not first |
|---|---|---|---|---|
| 7201TCWZGE | C&K | $23.87 | 250 | ON-ON, 15/32-32, IP67, solder lug — solid second; STEP only via login-gated aggregators (unverified no-login path), smaller stock, 5 A contacts |
| 2M1-DP1-T6-B1-M1QE | Carling | $8.25 | 630 | ON-ON IP67 but **miniature 1/4-40 bushing** — sub-mini bat, poor glove access, thin panel engagement |
| 3-6437592-9 | TE ALCOSWITCH AW | $42.36 | 304 | M12 IP67 20 A, STEP guaranteed via TE DocumentDelivery — but stocked variant is **ON-OFF-ON** (3-position; a dead third position on a master switch invites mis-sets) |
| 2NT1-7 / 2NT1-50 | Honeywell NT | $40+ | 105/60 | IP67/68 15/32 — stocked variants are Mom-Off-Mom / On-On-Mom (momentary; wrong function) |

## Status LED — separate panel indicator (option a follow-up line)

**APEM Q8P1CXXHG02E** (PROPOSAL): green diffused domed LED indicator, **2 V / 20 mA
bare LED — matches the R58 1k on-board drive exactly** (≈10 mA at the ~12.3 V coil
node; integrated-resistor 12/24 V indicators would be dim behind R58), Ø8.13 mm
(0.32") round cutout, threaded-bushing mount with nut, IP67, 2.8 mm quick-connects.
Digi-Key **312 in stock, $24.21** (verified 2026-08-22). Green = "kit armed",
consistent with on-board DS1 GREEN.
→ **Follow-up line: the LED needs its own Ø8.2 panel hole** (cut in CAD this round,
holder modeled as [PH] simplified geometry; APEM CAD model fetch = follow-up).

## Approvals queue addition

WT22S switch, Q8P1CXXHG02E indicator, J50 migration hardware (43045-0612 header /
43025-0600 housing / 43030-0007 terminals) — proposals only, nothing ordered.
