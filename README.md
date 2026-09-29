# Darktide Tree Planner

An interactive, in-browser skill-tree **build editor** for *Warhammer 40,000: Darktide* — all seven playable classes plus the Hive Scum Stimm sub-tree, in a single self-contained page.

**▶ Play it live:** **https://lawsonmode.github.io/darktide-tree-planner/** — pick a class, build, export.

Or open any HTML file locally in a browser (no install, no server, works offline): [`index.html`](index.html) (landing), a per-class page like [`zealot.html`](zealot.html), or the all-in-one [`darktide-skill-trees.html`](darktide-skill-trees.html).

> **Applet version:** v1.2.1
> **Tree data:** Games Lantern snapshot scraped **2026-09-29**. Community data may lag a game patch.

---

## Features

- **All 8 trees** — Veteran, Zealot, Ogryn, Psyker, Arbites, Skitarii, Hive Scum, and the Hive Scum **Stimm** sub-tree.
- **Game-accurate layout** — real node positions, connections, and the in-game icon art (all embedded as data URIs, so the page is fully offline / self-contained).
- **Build like in-game** — the class node is always active and free; allocate up to **30 points** following the real connection rules (a node is only selectable once linked to something you already have).
- **Faithful rules** — one Keystone / Ability / Blitz / Aura per group (handles Arbites' two keystone groups), and you can't remove a node other allocated nodes route through.
- **Hover** any node for its full effect text; **switch classes** from the top bar.
- **Export PNG** — download your build as an image, stamped with class, points, keystone/ability/blitz/aura, and version.
- **Build codes** — share a build as a short code (`DT2.<class>.<tree fingerprint>.<build>`) and paste it back to restore it, including which class and sub-tree. A tree fingerprint prevents codes from being applied to a different node order.
- **Gear guide** — per-class panel with the current-meta top-2 melee and ranged weapons plus curio stat priorities.

## Rebuilding the data

The September 29 refresh changes talent layouts. Legacy `DT1` codes must be recreated, and the old Zealot/Psyker presets have been retired because they reference removed talents.

The tree data (positions, connections, icons, descriptions) is scraped from [Games Lantern](https://darktide.gameslantern.com) and baked into the HTML. To regenerate after a game patch:

```bash
cd build
python3 scrape.py   # scrapes all classes -> data.json (+ downloads/encodes icons)
python3 gen.py      # regenerates the combined page, per-class pages, and index.html
```

Requires Python 3. `scrape.py` fetches each class's current tree (server-rendered SVG on Games Lantern class pages) and talent effect text from its `/abilities/<slug>` page. Class pages track the live tree; saved build pages can retain an older patch's layout. The scraper stops on missing trees, talent descriptions, or icons instead of publishing incomplete data.

The scrape date is recorded in `build/data.json` and included in the generated pages. Both scripts resolve paths relative to their own location, and generated HTML is written to the repository root.

## Attribution & disclaimer

This is an **unofficial fan-made tool** and is **not affiliated with, endorsed, or sponsored by** Games Workshop or Fatshark.

- *Warhammer 40,000*, *Darktide*, all associated names, icons, and imagery are © **Games Workshop** and **Fatshark**. Game icon art embedded in this project remains the property of its respective owners and is included here solely to identify in-game talents.
- Tree layout, node connections, and talent descriptions are sourced from **[Games Lantern](https://darktide.gameslantern.com)**, a community database. Descriptions are community-maintained and may occasionally lag a game patch.

The original code in this repository (the editor engine and the scripts in `build/`) is free to use and modify. The embedded game assets are **not** covered by that and belong to their owners.
