# Roof harness and roof junction box wiring

**Date: 2026-09-01.** Truth source for `roof-harness` (machine-side harness of the enclosure ROOF
receptacle) and `roof-box-internal` (wiring inside the roof junction box). The ROOF receptacle
itself, its pigtail and its face pinout are in `internal-wiring-definition.md` and `wire-map.md`.

## Roof harness: enclosure ROOF receptacle to the box wall plugs

Cab end: TE Deutsch HD36-18-14SE plug (mates HD34-18-14PE), size-16 socket contacts. Trunk 3.5 m
cut length: 2.0 m up the rear-left ROPS leg, about 0.9 m across the roof, plus the cab tail. The box
end is a second HD36-18-14SE plug onto an HD34-18-14PE receptacle in the box wall: same parts, same
cavity letters at both ends.

| ROOF cavity | Circuit | AWG | Class | Box plug · cavity |
|---|---|---|---|---|
| A | STARLINK_13V (FH4) | 16 | PWR | A |
| B | STARLINK_GND | 16 | GND | B |
| E | BCN_13V (FH5, K53 switched) | 16 | PWR | E |
| F | BCN_GND | 16 | GND | F |
| J | ES_RX (always on) | 18 | SAFE | J |
| L | RX_GND | 18 | GND | L |
| K | RX_STAT | 18 | SAFE | K |
| C, D, G, H, M, N, P | LiDAR power, LiDAR CAN, spare pair, plugged cavity | — | — | sealed (TE 114017) |

The plug's wire-side view is the mirror of the receptacle rear view; the cavity
letters are moulded on the plug grommet.

## Inside the roof junction box

| From | To | Conductor | Length |
|---|---|---|---|
| cavity A pin | converter IN + | converter's own red input lead (supplied), crimp pin | 30 cm |
| cavity B pin | converter IN − | converter's own black input lead (supplied), crimp pin | 30 cm |
| cavity E pin | beacon cord + | beacon pigtail through the gland, uncut, crimp pin | as supplied |
| cavity F pin | beacon cord − | beacon pigtail through the gland, uncut, crimp pin | as supplied |
| cavity J pin | receiver RED (9–30 V) | receiver pigtail, 18 AWG | 0.91 m pigtail |
| cavity L pin | receiver BLACK (GND) | receiver pigtail, 18 AWG | |
| cavity K pin | receiver WHITE (E-stop output 1, sourcing) | receiver pigtail, 18 AWG | |
| — | receiver GREEN (output 2) | not used, cut back and heat-shrunk | |
| converter OUT | router 57 V barrel | converter's own output lead + barrel plug (supplied) | 98 cm |
| KVT grommet | router DISH port | Starlink cable, moulded plug, passes the Ø63.4 cut-out before the grommet closes | 15 m fixed |
| KVT grommet | router LAN port | CAT6A outdoor, moulded RJ45, to the cab switch | 10 ft |
| lid dome | receiver ANT port | dome's captive coax, connected after the dome is bolted to the lid and the receiver is on its bracket | captive |

No junction blocks and no solder: every conductor ends in a size-16 crimp pin in the receptacle rear; the beacon cord
passes through the box untapped.

## Parts

| Item | Part | Qty |
|---|---|---|
| Cab plug | TE Deutsch HD36-18-14SE | 1 |
| Socket contacts, size 16 | TE 0462-201-16141 | 7 |
| Sealing plugs, size 16 | TE 114017 | 7 |
| Box harness plug | TE HD36-18-14SE (second plug, crimp) | 1 |
| Box receptacle | TE HD34-18-14PE + panel nut 114020-90 + lock washer 114021 | 1 each |
| Receptacle pins | TE 0460-202-16141 size-16 solid pins (converter leads, beacon cord, receiver pigtail) | 7 |
| Split gland | Weidmüller Cabtite CGS M63 + SE 8-9 (dish), SE 6-7 (LAN), SE 4-5 (beacon cord), BSE blind | 1 set |
| Split gland | icotek KVT-ER 63|4 (45456) | 1 |
| Wire | 16 AWG GXL red/black (two pairs), 18 AWG TXL violet ×2 + black, braided loom | 3.5 m each |

## Design notes

FH4 is a 5 A position in the power-board fuse ladder. The Gen 3 Standard draws up to 100 W, about
7.7 A at 13 V, so FH4 moves to a 10 A fuse before this harness carries the Standard. The 16 AWG pair
and the size-16 contacts (13 A) carry that current.

The beacon pair E/F is switched by K53 on the power board (autonomy engaged), so the beacon cannot
hang off the box's own 13 V feed. It arrives on receptacle cavities E/F; the beacon cord itself comes in through the split gland
No junction blocks and no solder: every conductor ends in a size-16 crimp pin in the receptacle rear; the beacon cord
joint is a size-16 crimp pin in the receptacle rear (13 A contacts, the Starlink feed draws up to 7.7 A).

The receiver's E-stop output 1 (white) is a sourcing output that carries the receiver supply voltage
while the link is healthy and no transmitter is stopped, and it drops when a stop is pressed or the
link is lost. That output is RX_STAT into the power board's K52 link gate; output 2 (green) is unused.
