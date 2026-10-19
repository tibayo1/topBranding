# Shared Rhythm — optical development 09

**DRAFT — NOT FOR PUBLICATION.** No logo, palette, typeface or production rule is final.

The favored primary drawing is preserved. This work addresses one demonstrated weakness: two of its four faces join in a 16 px raster. Four faces remain visually substantial at 24 px and above; 32 px better shows the folded planes and shared interior.

The provisional small-use cut retains the four unequal faces, tallest inner-right face, open forecourt and a short second-face shoulder. Narrower planes and wider intervals keep the four faces separate at 16–20 px. Its more disconnected appearance at large sizes makes it unsuitable as a global replacement for the primary.

- [Primary symbol](primary.svg) and [white reverse](reverse.svg): provisionally use from 24 px; 32 px preferred for the spatial construction.
- [Compact symbol](compact.svg) and [white reverse](compact-reverse.svg): constrained 16–20 px uses only.
- [Primary/compact comparison](renders/primary-and-compact.png): actual native samples next to labeled 2× pixel diagnostics.
- [Initial optical comparison](renders/optical-development.png): two small-use premises, including the rejected simpler facets.
- [Metadata and findings](metadata.json).

Both black and white versions were rendered and viewed. Inkscape and Chromium both preserve four separate alpha components in the selected compact at native 16/20/24/32/64/512 px, at alpha thresholds 1, 32, 64, 128, 192 and 224. Alpha 1 includes faint antialias fringes. Results are in [Inkscape records](source/inkscape-pixel-components.json) and [Chromium records](source/chromium-pixel-components.json). These measurements establish separation on the tested whole-pixel raster setup. They do not establish that a viewer perceives a sanctuary, praise or a church, and they do not cover arbitrary subpixel placement, platform resampling or physical production.

The SVG audit finds no live type, rasters, gradients or filters. It flags the existing slightly tapered edges and unequal vertical margins; these deliberate qualities remain rather than snapping the favored drawing to a rigid grid. An audit score is not aesthetic or legal approval.

Rebuild vectors, Inkscape native renders and comparison boards with `python3 source/build.py`. Rebuild the independent Chromium pixel record with `python3 source/browser_proof.py` (Playwright and `/usr/bin/chromium`). Source paths are self-contained except for the existing repository Noto Sans font used solely in board annotations. The symbol has no font dependency.

Property/cultural-venue associations and the abstract praise reading still need human review. No actual RCCG emblem is embedded or redrawn. No production, publishing or trademark clearance is implied.
