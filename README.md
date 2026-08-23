# V3.2 Harness Diagrams

Generator for the Crewline V3.2 enclosure harness diagrams — nine drawings. Each of the four HD34
panel receptacles (VEHICLE, ROOF, STEERING, JETSON) gets two:

- **`<key>-internal`** — the internal Y-split pigtail: rear (wire-side) cavity view, one lane per
  conductor converging into the trunk, the Y-fork, then power-leg and signal-leg fan-out into the
  board-header housings (power board / interface board), with twisted pairs drawn as crossover
  glyphs and pin numbers at each housing entry.
- **`<key>-pinout`** — the mating-face pinout: mirrored front view with per-cavity callout leaders
  and a full cavity | circuit | AWG | dest header · pin table.

The ninth, **`panel-switch-internal`**, is the interior panel harness: kit master switch
(NKK WT22S DPDT) + status LED (APEM Q8) on the enclosure front wall → J50 on the power board —
rear-view solder-lug reference with the used/spare lug grid, six-wire fan with per-wire
circuit · AWG labels, J50 wire-entry view, and an always-hot warning box (pins 3/4 live with the
kit switched off).

SVG masters plus 2x PNG exports live in `output/` — the committed set is the delivered reference.

## Data model

One JSON file per receptacle (and one per panel device) in `data/`, plus `data/meta.json` (project
label, revision date, wire-table reference — the dates stamped on the drawings come from here,
never from the clock). Receptacle fields:

| Field | Content |
|---|---|
| `order` | sort key for generation order (vehicle 10, roof 20, steering 30, jetson 40) |
| `key`, `name`, `shell`, `arr` | file basename, display name, TE shell PN, insert arrangement line |
| `tedoc`, `stepsrc` | TE insert-arrangement drawing rev; TE STEP model the cavity XY came from |
| `cavities` | `{cavity_id: [contact_size, x_mm, y_mm]}` — rear-view (wire-side) coordinates extracted from the TE STEP models, +x right / +y up per the TE drawing orientation |
| `ordmap` | ordinal → real cavity assignment (row order = wire-table order; see `docs/wire-map.md`) |
| `wires` | rows `[cavity, circuit, awg, class, leg, header, pin, note]` — class keys the color legend (PWR/GND/CANH/CANL/SIG/SAFE), leg is `power` or `signal`, note `tw:a`/`tw:b` marks twisted-pair members |
| `spare_cavs` | cavities left unwired (drawn muted, sealed with plugs) |
| `housings` | per board header: title, board + mate PN subtitle, spare/note footer lines |

### Panel-device schema extension

`data/switch.json` carries `"kind": "panel"`, which routes it to the panel-device renderer
(`gen_switch`) instead of the receptacle pair — `kind` is the only dispatch field; receptacle files
omit it. Panel diagrams need things receptacles have no equivalent for (solder-lug maps instead of
cavity XY, a warning box), so a panel entry replaces `shell`/`arr`/`cavities`/`ordmap`/`housings`
with:

| Field | Content |
|---|---|
| `title`, `sub` | header-band title and subtitle lines |
| `switch` | lug grid: `poles` (columns, left→right), `throws` (rows, top→bottom, `""` = COM), `used_lugs`, plus the two caption notes |
| `led` | LED reference-drawing heading + note |
| `legend` | `[class, label]` rows — classes key the shared receptacle palette (PWR/SIG/GND) |
| `wires` | rows `[lug, circuit, awg, class, pin]` — straight fan, one row per J50 pin |
| `housing` | destination header box (title, sub, note) + `entry` wire-entry inset (grid size, caption notes) |
| `warning` | red always-hot box: title + body lines |
| `footer` | the two footer lines |

Output naming is shared: `<key>-internal.svg/png` (key `panel-switch`). `order` 50 places it after
the receptacles in the manifest.

Truth sources: the wire tables are `docs/internal-wiring-definition.md` (rev b, 2026-08-22); the
ordinal → real cavity mapping, TE document provenance, and the PANEL → J50 harness table are
`docs/wire-map.md`. Cavity IDs are the real TE ones from the PIN-insert rear/grommet views of TE
0425-013-1800 rev D (shell 18) and 0425-014-2400 rev H (shell 24); face-pinout drawings mirror them
for the mating-face view.

**To edit a wire**: change its row in the receptacle's `wires` (and the table in
`docs/internal-wiring-definition.md` that it transcribes), then regenerate.
**To add a receptacle**: drop one new `data/<key>.json` with a unique `order`; nothing else changes.

## Collision audit

`gen_face` places callout leaders by scanning candidate ray angles (0–80° off the radial, 2° steps)
and scoring each by its clearance to every other cavity circle (point-to-segment distance); it takes
a near-radial ray when one clears by > 13 px, else the maximum-clearance ray. After layout, two
checks run over the finished drawing:

1. **segment × segment** — every leader polyline segment pairwise against every other label's
   segments, straddle test via CCW orientation signs;
2. **leader × cavity circle** — every ray against every foreign cavity circle, flagged when the
   distance drops below the cavity radius + 2 px.

The panel-switch drawing has no callout leaders, so it runs its own overlap audit instead
(inherited from its standalone generator): every audited text extent against every horizontal wire
run, every other text extent, and every box edge (text fully inside or fully outside a box is
fine — straddling an edge is flagged).

Violations from both audits print as `XING:` lines and the run reports the combined count. The
committed set generates with **0 collision warnings**. `NUDGE` in `__main__` accepts per-cavity
angle overrides should a future data change introduce one.

## Running

```
./run.sh        # or: make
```

`make svg` regenerates the SVG masters (Python 3 stdlib only, deterministic).
`make png` rasterizes them at 2x via headless Chrome screenshot (`generators/export.sh`, driven by
`output/manifest.txt`); set `CHROME=/path/to/chrome` if the binary is not at the default macOS path.

## Reproducibility

Verified end-to-end from a clean checkout on macOS (Python 3.9, Chrome): the 9 generated SVGs are
byte-identical to the delivered reference set (the panel-switch SVG matches the standalone
generator's delivered master byte-for-byte), and repeated PNG exports are byte-identical
run-to-run (the rasterizer is deterministic on a given machine) — the committed 9-PNG set
regenerates byte-identically, and the fresh panel-switch export is byte-identical to the
originally delivered `panel-switch-internal.png`. Against the originally delivered receptacle
PNGs, 4 of 8 exports are byte-identical; the other 4 (rasterized earlier in the delivery session)
match in dimensions and were confirmed visually identical pair-by-pair, differing only in PNG
encoding. The generator itself injects nothing from the environment — the dates on the drawings
come from `data/meta.json`. The SVG masters are the ground truth; PNG byte identity holds within
any one machine + Chrome build, not across them (font rasterization).

## History

The generator merges the original two-file pipeline: `gen_diagrams.py` (data tables + SVG helpers +
first-pass drawing routines) and `gen2.py` (collision-hardened v2 drawing routines that superseded
the first pass). The v2 routines and shared helpers are what live here; the v1 drawing code was
dropped and the inline data tables moved to `data/`. The panel-switch drawing was delivered by a
third standalone script, `gen_panel_switch.py`; its drawing routine and overlap audit were folded
in as `gen_switch` with the inline data extracted to `data/switch.json`, keeping its own SVG
emitters so the output stays byte-identical to the delivered master.
