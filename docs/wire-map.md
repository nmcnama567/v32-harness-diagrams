# V3.2 Receptacle Cavity Map — ordinal → real TE cavity IDs

**Date: 2026-08-22 (rev b — brake single cut line, explicit Jetson DIO set).** Companion to the 8
diagram PNGs in this directory and to
`/tmp/claude-501/internal-wiring-definition.md` (the wire tables, whose cavity IDs were ordinal).
This file records the one-time ordinal→real assignment, made 1:1 in table order per the definition
doc's convention. **Cavity IDs are REAL**, taken from the TE insert-arrangement drawings (not
indicative): the drawings show separate SKT and PIN insert views — the **PIN views** were used (all
four receptacles are P-type), and TE draws them as **rear-end (grommet) views**, which is the view a
harness builder sees when loading contacts. Face-pinout diagrams mirror this for the mating-face view.
Cavity **positions** (mm) were taken from TE's own STEP models in
`/tmp/claude-501/cad-assembly/vendor/` — counts and size classes match the drawings exactly.

## Truth sources

| Doc | Content | Where |
|---|---|---|
| TE 0425-013-1800 rev D | "Arrangements of Contact Location, HDP20/HD30, shell size 18" — numbered/lettered rear views for 18-8, 18-14, 18-20 (and 18-6, 18-21) | https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Specification+Or+Standard%7F0425-013-1800%7FD%7Fpdf%7FEnglish%7FENG_SS_0425-013-1800_D.pdf%7FHDP24-18-14PN |
| TE 0425-014-2400 rev H | Same, shell size 24 — includes 24-21 | https://www.te.com/commerce/DocumentDelivery/DDEController?Action=showdoc&DocId=Specification+Or+Standard%7F0425-014-2400%7FG%7Fpdf%7FEnglish%7FENG_SS_0425-014-2400_G.pdf%7FHD34-24-29SE |
| TE 114-151014 rev A | HD30 application spec (references the two drawings above as the contact-cavity-marking authority; sealing-plug + keying-pin install) | https://datasheet.octopart.com/HD34-24-21PE-059-TE-Connectivity-datasheet-137114240.pdf |
| TE STEP models | c-hd34-24-21pe-b-3d.stp, c-hd34-18-14pe-b-3d.stp, c-hd34-18-8pe-b-3d.stp, c-hd34-18-20pn-f1-3d.stp — cavity XY used for the face drawings | local, `/tmp/claude-501/cad-assembly/vendor/` |

Local copies of both drawings: scratchpad `te-shell18.pdf`, `te-shell24.pdf` (this session).

## VEHICLE — HD34-24-21PE (insert 24-21: 4× s12 + 17× s16, letters A–X, no I/O/Q)

Size-12 cavities are B, G (top pair) and D, E (bottom pair); all others s16.

| Ordinal | Real | Circuit | | Ordinal | Real | Circuit |
|---|---|---|---|---|---|---|
| s12-1 | **B** | BAT+ (A) | | s16-8 | **M** | JOY_CAN_L |
| s12-2 | **D** | BAT− (A) | | s16-9 | **N** | BRK_JOY |
| s12-3 | **E** | BAT+ (B) | | s16-10 | **R** | BRK_ECU |
| s12-4 | **G** | BAT− (B) | | s16-11 | **T** | SPARE_CAN_H |
| s16-1 | **A** | ESTOP_LOOP_FWD | | s16-12 | **U** | SPARE_CAN_L |
| s16-2 | **C** | ESTOP_LOOP_RET | | s16-13 | **V** | T15_KEY |
| s16-3 | **F** | SEAT_A | | s16-14 | **W** | SIG_GND/drain |
| s16-4 | **H** | SEAT_B | | s16-15…17 | **P, S, X** | spare (plugged) |
| s16-5 | **J** | ECU_CAN_H | | | | |
| s16-6 | **K** | ECU_CAN_L | | | | |
| s16-7 | **L** | JOY_CAN_H | | | | |

Mapping rule (rev a): alphabetical within each size class = table order. Rev b freed the two former
brake B-side cavities **in place** — P and S became spare (plugged) and every other rev-a contact
kept its cavity, so the rev-b ordinals no longer run strictly alphabetical past s16-9 (BRK_JOY = N,
BRK_ECU = R; the brake pair is the single cut line, one twisted pair, no returns). Happy accident
preserved: all three CAN pairs land on ring-adjacent cavities (J/K, L/M, T/U).

## ROOF — HD34-18-14PE (insert 18-14: 14× s16, letters A–P, no I/O)

| Ordinal | Real | Circuit | | Ordinal | Real | Circuit |
|---|---|---|---|---|---|---|
| 1 | **A** | STARLINK_13V | | 8 | **H** | LIDAR_CAN_L |
| 2 | **B** | STARLINK_GND | | 9 | **J** | ES_RX (always-on) |
| 3 | **C** | LIDAR_13V | | 10 | **K** | RX_STAT |
| 4 | **D** | LIDAR_GND | | 11 | **L** | RX_GND |
| 5 | **E** | BCN_13V | | 12 | **M** | SPARE_13V |
| 6 | **F** | BCN_GND | | 13 | **N** | SPARE_GND |
| 7 | **G** | LIDAR_CAN_H | | 14 | **P** | spare (plugged) |

## STEERING — HD34-18-8PE (insert 18-8: 8× s12, letters A–H)

The definition doc already used letters A–H — **identity mapping**, confirmed real: TE 18-8 letters
run A/B center pair, C/D/E top row (C right, E left in rear view), F/G/H bottom row.
A = STR_13V, B = STR_GND, C = STR_CAN_H, D = STR_CAN_L, E–H spare (plugged).

## JETSON — HD34-18-20PN (insert 18-20: 2× s16 + 18× s20, numbers 1–20)

The two size-16 cavities are **3** (left of center, rear view) and **6** (right of center); 1 = center s20.

| Ordinal | Real | Circuit | | Ordinal | Real | Circuit |
|---|---|---|---|---|---|---|
| s16-A | **3** | JET_13V | | s20-9 | **11** | GPIO_SPARE |
| s16-B | **6** | JET_GND | | s20-10 | **12** | SEAT_STATE (DIO in) |
| s20-1 | **1** | JET_CAN1_H | | s20-11 | **13** | ARM_SENSE (DIO in) |
| s20-2 | **2** | JET_CAN1_L | | s20-12 | **14** | BRAKE_SENSE (DIO in) |
| s20-3 | **4** | JET_CAN2_H | | s20-13 | **15** | IGN_SENSE (DIO in) |
| s20-4 | **5** | JET_CAN2_L | | s20-14 | **16** | SDA |
| s20-5 | **7** | DIO_PWR (FH3) | | s20-15 | **17** | SCL |
| s20-6 | **8** | DIO_GND | | s20-16 | **18** | ALERT_N |
| s20-7 | **9** | DIO_OUT_AUTONOMY | | s20-17 | **19** | V3_HOST |
| s20-8 | **10** | DIO_OUT_BRAKE | | s20-18 | **20** | SIG_GND |

Mapping rule: TE number order within each size class = table order (s20 numbers skip 3/6, which are
the s16 positions). Rev b fills all 20 cavities — nothing plugged; the DIO supply pair (7/8) rides
the power leg to J_JP 2/4, everything else the signal leg to J_JS (16/16). SEAT_EMU_SENSE has no
cavity and is dropped (survives as the R26/R18 probe stub on the interface board).

## Notes for the harness RFQ

1. **View convention:** TE arrangement views (and the internal-wiring PNGs) are rear/grommet views;
   the face-pinout PNGs are mirrored front views — both state this in their footers. External-mating-plug
   drawings must use the SKT views of the same TE sheets (mirror images of these).
2. **Board-header pins with no panel cavity:** J_RS·3 and J_SS·3 (SIG_GND/drain, CAN stub reference)
   are loaded terminals fed on the board side, not pigtail conductors — they appear as block notes on the
   internal diagrams, not as wires.
3. **Rotation/clocking:** the TE views do not show the master key; insert rotation relative to the shell
   key is fixed by the product — orient the printed cavity letters/numbers molded on the grommet at
   contact-loading time (they are molded on every HD34 rear grommet, ref 114-151014 §3.3.B).
4. Diagram set: `{vehicle,roof,steering,jetson}-{internal,pinout}.png`, 2× SVG masters alongside
   (`*.svg`, same basenames) — regenerate via scratchpad `gen2.py`.

## PANEL — kit master switch + status LED → J50 (added 2026-08-22, no HD34 involved)

Interior-only harness: panel devices on the enclosure front wall → J50 on the power board
(Micro-Fit 6 housing 43025-0600, crimps 43030-0007, all conductors 20 AWG, one wire per contact,
crimp-to-solder-lug / crimp-to-quick-connect). Diagram: `panel-switch-internal.png` (+ SVG master,
generator `gen_panel_switch.py`). J50 was XH-6 single-row; now Micro-Fit 2×3 — pin NUMBERS 1:1
(rows 1-2-3 / 4-5-6, pin 1 opposite pin 4).

| J50 pin | Circuit | Panel end | AWG | Notes |
|---|---|---|---|---|
| 1 | LED_A | LED + (Q8 quick-connect 2.8 mm) | 20 | fed from K50 coil node via R58 1k (~10 mA) — lights when kit armed |
| 2 | SW_ARM | switch lug **1** (pole-1 COM) | 20 | arms K50 via Q50 emitter-follower |
| 3 | ES_FEED | switch lug **1a** (pole-1 up-throw) | 20 | **ALWAYS HOT** ≈13 V via R92 470R whenever battery connected — does not pass through the master relay |
| 4 | PWR_SW | switch lug **2** (pole-2 COM) | 20 | LM5176 enable; R61 470k pull-up → also weakly live with kit off |
| 5 | GND | switch lug **2a** (pole-2 up-throw) | 20 | switch return |
| 6 | GND | LED − | 20 | LED return |

Switch = NKK WT22S (DPDT ON-NONE-ON): toggle **UP = ON** closes 1–1a + 2–2a; lugs 1b/2b unused.
LED = APEM Q8P1CXXHG02E (green, 2 V bare LED — no series resistor in the harness). Both PNs
pending approval per switch-sourcing.md.
