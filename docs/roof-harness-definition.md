# Roof harness and roof junction box wiring

**Date: 2026-09-01.** Truth source for `roof-harness` (machine-side harness of the enclosure ROOF
receptacle) and `roof-box-internal` (wiring inside the roof junction box). The ROOF receptacle
itself, its pigtail and its face pinout are in `internal-wiring-definition.md` and `wire-map.md`.

## Roof harness: enclosure ROOF receptacle to the box wall plugs

Cab end: TE Deutsch HD36-18-14SE plug (mates HD34-18-14PE), size-16 socket contacts. Trunk 3.5 m
cut length: 2.0 m up the rear-left ROPS leg, about 0.9 m across the roof, plus the cab tail. The box
end is one Weipu SP21 7-pin cable plug (15 A contacts) into the SP2112/S7 wall socket.

| ROOF cavity | Circuit | AWG | Class | Plug · pin |
|---|---|---|---|---|
| A | STARLINK_13V (FH4) | 16 | PWR | SP21 · 1 |
| B | STARLINK_GND | 16 | GND | SP21 · 2 |
| E | BCN_13V (FH5, K53 switched) | 16 | PWR | SP21 · 3 |
| F | BCN_GND | 16 | GND | SP21 · 4 |
| J | ES_RX (always on) | 18 | SAFE | SP21 · 5 |
| L | RX_GND | 18 | GND | SP21 · 6 |
| K | RX_STAT | 18 | SAFE | SP21 · 7 |
| C, D, G, H, M, N, P | LiDAR power, LiDAR CAN, spare pair, plugged cavity | — | — | sealed (TE 114017) |

The plug's wire-side view is the mirror of the receptacle rear view; the cavity
letters are moulded on the plug grommet.

## Inside the roof junction box

| From | To | Conductor | Length |
|---|---|---|---|
| SP21 cup 1 | converter IN + | converter's own red input lead (supplied) | 30 cm |
| SP21 cup 2 | converter IN − | converter's own black input lead (supplied) | 30 cm |
| SP21 cup 3 | SP13 2-pin cup 1 | 18 AWG red, beacon feed pass-through | 250 mm |
| SP21 cup 4 | SP13 2-pin cup 2 | 18 AWG black, beacon return pass-through | 250 mm |
| SP21 cup 5 | receiver RED (9–30 V) | receiver pigtail, 18 AWG | 0.91 m pigtail |
| SP21 cup 6 | receiver BLACK (GND) | receiver pigtail, 18 AWG | |
| SP21 cup 7 | receiver WHITE (E-stop output 1, sourcing) | receiver pigtail, 18 AWG | |
| — | receiver GREEN (output 2) | not used, cut back and heat-shrunk | |
| converter OUT | router 57 V barrel | converter's own output lead + barrel plug (supplied) | 98 cm |
| KVT grommet | router DISH port | Starlink cable, moulded plug, passes the Ø63.4 cut-out before the grommet closes | 15 m fixed |
| KVT grommet | router LAN port | CAT6A outdoor, moulded RJ45, to the cab switch | 10 ft |
| lid dome | receiver ANT port | dome's captive coax, connected after the dome is bolted to the lid and the receiver is on its bracket | captive |

No junction blocks: the converter leads solder straight to the SP21 solder cups and the beacon feed
passes through the box untapped.

## Parts

| Item | Part | Qty |
|---|---|---|
| Cab plug | TE Deutsch HD36-18-14SE | 1 |
| Socket contacts, size 16 | TE 0462-201-16141 | 7 |
| Sealing plugs, size 16 | TE 114017 | 7 |
| Box harness plug | Weipu SP2110/P7 (cable plug, 7-pin, 15 A contacts) | 1 |
| Wall sockets | Weipu SP2112/S7 (harness), SP1312/S2 (beacon out) | 1 each |
| Beacon cord plug | Weipu SP1310/P2 | 1 |
| Split gland | icotek KVT-ER 63|4 (45456) | 1 |
| Wire | 16 AWG GXL red/black (two pairs), 18 AWG TXL violet ×2 + black, braided loom | 3.5 m each |

## Design notes

FH4 is a 5 A position in the power-board fuse ladder. The Gen 3 Standard draws up to 100 W, about
7.7 A at 13 V, so FH4 moves to a 10 A fuse before this harness carries the Standard. The 16 AWG pair
and the size-16 contacts (13 A) carry that current.

The beacon pair E/F is switched by K53 on the power board (autonomy engaged), so the beacon cannot
hang off the box's own 13 V feed. It enters the box on SP21 pins 3/4 and passes straight through to
the SP13 2-pin beacon socket. One 7-pin SP21 carries the whole harness into the box: the SP21
7-pin contacts are rated 15 A, the Starlink feed draws up to 7.7 A.

The receiver's E-stop output 1 (white) is a sourcing output that carries the receiver supply voltage
while the link is healthy and no transmitter is stopped, and it drops when a stop is pressed or the
link is lost. That output is RX_STAT into the power board's K52 link gate; output 2 (green) is unused.
