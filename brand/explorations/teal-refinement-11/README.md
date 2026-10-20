# Teal refinement 11 — two working options

**DRAFT — NOT FOR PUBLICATION.** Teal + sand is the user's selected working color direction. Both logos continue toward a later team review; final logo, type system, production colors and publication approval remain open.

![Shared Rhythm and Open Praise refined in teal](exports/two-options-teal.png)

- **[Open the refined comparison PNG](exports/two-options-teal.png)**
- **[Open the three-page review PDF](exports/two-option-review-11.pdf)**
- **[Download the vector A4 print proof](proofs/a4-print-proof.pdf)** — print at 100% / Actual size, disable fit-to-page, and measure the 50 mm calibration ruler.
- [Actual screen-size proof](proofs/screen-size-proof.png)

## What changed

**Shared Rhythm:** the favored primary silhouette is preserved exactly. Four unequal folded faces hold an open forecourt; their changing heights suggest gathering and shared praise. Its lettering, arrangements and contrast treatment receive the refinement. The separate compact drawing remains reserved for 16–20 px. Normal avatars use the primary. The architectural/cultural-venue reading remains possible; this is a spatial rhythm rather than a literal musical instrument.

**Open Praise:** the negative crossbar's two lower edges now meet at the same height, with the outer P silhouette and existing stem width retained. This steadies the counter-to-stem junction. A wider-stem trial was compared and set aside because it made the shape less compact without a clear benefit. The tiny-use candidate receives the corresponding alignment. The proposed T remains interpretive; the adjustment is a craft improvement, not an audience-recognition result.

**Full-name lettering:** Instrument Sans 470 keeps its original glyph contours. A few pair spaces are refined and the two-line baseline pitch reduces from 117 to 110 source units, making the name a more cohesive unit. “of Praise” keeps equal size and weight. A new single-line **Tabernacle of Praise** arrangement supports wider headers/signs; horizontal two-line and centered stacked arrangements remain available. No font binary is modified or new custom typeface claimed.

**Symbol balance:** the denser Open Praise symbol uses 93% of Shared Rhythm's actual ink height beside the same name scale. The new builder normalizes actual contours, fixing the earlier maximum-field approach that did not consistently produce the stated optical reduction. Each arrangement uses the same correction for both light and dark. There is no nonuniform scaling.

**Working color use:** teal `#10494C` and warm porcelain `#F6F3EC` carry the symbol and full name. Preferred dark versions use porcelain for both on teal, giving about 9.11:1 contrast. Sand `#D9CBB4` supports surfaces; soft gold `#B69255` stays a restrained flat layout accent. This favors clear small shapes over the softer gold-on-teal pairing. Physical papers, inks and materials remain to be proved.

## Editable masters

| Option | Symbol | Two-line horizontal | Stacked | New single-line |
|---|---|---|---|---|
| Shared Rhythm | [SVG](shared-rhythm/primary.svg) | [SVG](exports/shared-rhythm-horizontal-DRAFT.svg) | [SVG](exports/shared-rhythm-stacked-DRAFT.svg) | [SVG](exports/shared-rhythm-singleLine-DRAFT.svg) |
| Open Praise | [SVG](open-praise/primary.svg) | [SVG](exports/open-praise-horizontal-DRAFT.svg) | [SVG](exports/open-praise-stacked-DRAFT.svg) | [SVG](exports/open-praise-singleLine-DRAFT.svg) |

Reverse arrangements, colored symbol proofs and compact cuts are listed in [artwork.json](exports/artwork.json). All parish names are outlined paths. The original black contour sources remain transparent and editable. [Working palette](source/working-palette.json), [source brief](source/brief.md), [lettering source and comparison](lettering/README.md), [Open Praise contour comparison](open-praise/README.md) and [Shared Rhythm source notes](shared-rhythm/README.md) preserve the decisions and trials.

The review's header, entrance and avatar contexts use the same conditions for both options. The entrance is an imagined proportion study; no actual premises, services, addresses or contact information are invented. No materials are sent to teammates automatically.

## Proof status and remaining checks

The A4 file is a vector proof prepared for physical printing. It includes both symbols at actual ink heights of 8/12/18/24 mm and complete lockups at 35/50/70 mm ink widths, with one-color controls and ivory reverse. The 50 mm ruler verifies that the print driver preserved scale. Cloud renders cannot verify the resulting paper, ink spread, vinyl or fabrication; these are open physical checks rather than approved minimum-size standards.

The screen proof displays actual small renderings, including the assembled single-line arrangement at real header widths. Visible contours and separations do not prove recognition of worship, architecture or T/P. Meaning should still be assessed with the full name and church context.

The [RCCG emblem manifest](../../assets/rccg-emblem/README.md) is present, but the original PNG remains absent. Actual two-logo pairing is pending that asset. No emblem is recreated, traced, recolored or merged into the parish mark. The intended original file is `brand/assets/rccg-emblem/rccg-emblem-user-supplied.png`; verify its recorded checksum when it becomes available.

After the actual emblem and physical proof checks, the two options can be reviewed by the team. Final brand approval, any legal clearance and production-ready standards follow that feedback. AGENTS.md and the RCCG identity skill remain unchanged.

## Rebuild

Use the existing repository Python/fontTools/Pillow, Inkscape and Playwright/Chromium environment:

```sh
python brand/explorations/teal-refinement-11/lettering/build.py
python brand/explorations/teal-refinement-11/open-praise/source/build.py
python brand/explorations/teal-refinement-11/tools/build_artwork.py
python brand/explorations/teal-refinement-11/tools/build_proofs.py
python brand/explorations/teal-refinement-11/tools/build_review.py
```

The source font and original OFL remain in [development 09](../identity-development-09/type-study/README.md). Self-contained review HTML includes the original license if the font binary is embedded. Saved PNG/PDF files provide normal downloads when chat previews fail.
