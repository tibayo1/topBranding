# Larger RCCG emblem — proportion review 15

**DRAFT — NOT FOR PUBLICATION.** The RCCG emblem is now **twice its previous diameter** in both parish layouts. Its visible circle nearly matches the complete parish logo's height, including the name below the symbol.

![Both updated layouts](exports/larger-RCCG-comparison-DRAFT.png)

| Concept | Square PNG 1080×1080 | Widescreen PNG 1920×1080 | Editable square SVG |
|---|---|---|---|
| Shared Rhythm | [Download](exports/shared-rhythm-RCCG-larger-square-DRAFT.png) | [Download](exports/shared-rhythm-RCCG-larger-landscape-DRAFT.png) | [SVG](exports/shared-rhythm-RCCG-larger-square-DRAFT.svg) |
| Open Praise | [Download](exports/open-praise-RCCG-larger-square-DRAFT.png) | [Download](exports/open-praise-RCCG-larger-landscape-DRAFT.png) | [SVG](exports/open-praise-RCCG-larger-square-DRAFT.svg) |

The RCCG image grows from 180 to 360 units in the base pairing. Its visible circle is about 337.1 units tall, compared with the complete Shared Rhythm logo's 352 and Open Praise's 344.65. Both options share the same parent-emblem size. The circle aligns with the complete parish logo, including its name, and the whole pairing is recentered. The parish symbol, name, colors, internal proportions and name-below arrangement are preserved.

The complete existing RCCG reference PNG is embedded byte-for-byte, with no cropping, tracing, recoloring or regeneration. It remains the documented [236×236 parish-source reference](../../assets/rccg-emblem/references/README.md). The requested increase displays it at 396 px in square and 468 px in widescreen drafts; the seal may appear softer at these larger sizes. This scaling adds no source detail and does not make it a high-resolution production master.

This revision provides updated static PNGs and editable SVGs. The [preceding motion graphics](../rccg-motion-14/README.md) retain their earlier proportions. No final identity, palette, typography or production/publication approval is implied. AGENTS.md and identity skill files are unchanged.

Rebuild from the repository root with Python, Pillow and Playwright/Chromium:

```sh
python brand/explorations/balanced-emblem-15/source/build.py
```

[Editable layout parameters](source/layout.json) · [Source and geometry checks](exports/manifest.json)
