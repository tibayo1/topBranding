# RCCG + Tabernacle of Praise — pairing study 12

**DRAFT — NOT FOR PUBLICATION.** Both current parish options sit beside an unchanged existing RCCG emblem reference. Teal + sand remains the selected working parish palette. No final lockup or production asset is approved.

![Both paired options on light and dark](exports/paired-comparison.png)

- **[Open the paired comparison PNG](exports/paired-comparison.png)**
- **[Download the two-page review PDF](exports/pairing-review-12.pdf)**
- **[Download the PNG + paired artwork ZIP](exports/RCCG-and-Tabernacle-of-Praise-DRAFT.zip)**

The ZIP includes the standalone emblem PNG, four self-contained paired SVGs, comparison PNG, review PDF and reference-source notes. The PNG is ready to download; no ZIP creation is required from the user.

## Reference source

The image displayed in chat was not exposed to the project tools as downloadable file bytes. For this internal draft, an existing PNG was extracted unchanged from the embedded image in an RCCG parish website repository's SVG asset:

- Repository: `RCCG-WayForwardProject/rccg-wayforward`
- Commit: `b053a99345e9178e23db06ac35b9529006684480`
- Source: [public/logo.svg](https://github.com/RCCG-WayForwardProject/rccg-wayforward/blob/b053a99345e9178e23db06ac35b9529006684480/public/logo.svg)
- Native PNG: **236 × 236**, RGBA, **23,611 bytes**
- SHA-256: `977ee1c5a43c30d2859e31f59705da23a53e8c3e7736d1d1376e021c62703340`
- [Recorded reference PNG and provenance](../../assets/rccg-emblem/references/README.md)

This is a separate sourced reference, not a regenerated emblem or a claim to have recovered the exact original chat upload. The original 1200×1200 PNG/checksum in the [earlier manifest](../../assets/rccg-emblem/README.md) remains unverified. The reference's modest native resolution limits large print use; final source authorization and production suitability remain open.

## Layout tests

| Option | Light | Dark |
|---|---|---|
| Shared Rhythm | [Editable SVG](exports/shared-rhythm-light-pairing-DRAFT.svg) | [Editable SVG](exports/shared-rhythm-dark-pairing-DRAFT.svg) |
| Open Praise | [Editable SVG](exports/open-praise-light-pairing-DRAFT.svg) | [Editable SVG](exports/open-praise-dark-pairing-DRAFT.svg) |

Both use identical 960×300 test fields. The complete emblem occupies a 160×160 field at `(40,70)`; the current 680×256 parish horizontal arrangement starts at `(230,22)`. Light fields are pure white. Dark fields retain a separate white 192×192 panel around the full raster and place the ivory parish identity on teal. The emblem's source pixels, color, transparency, full image and proportions stay unchanged. No circular mask or background removal is applied.

All parish contours, name outlines and internal transforms stay exactly as in [refinement 11](../teal-refinement-11/README.md), including Open Praise's 93% symbol-height adjustment. Only the parish presentation background changes from porcelain to the common white pairing field in light examples. Gold is omitted from these formal pairing studies.

Shared Rhythm's open planes provide a lighter companion to the dense circular seal. Open Praise offers a compact alternative with a heavier contour. Both still need actual-size ring-letter reading and physical material checks before permanent dimensions can be approved.

## Rebuild and checks

```sh
python brand/explorations/rccg-pairing-12/source/build.py
```

The builder reads the recorded reference asset and frozen refinement 11 SVGs, embeds the unchanged image bytes in each paired SVG, creates the review and ZIP, and verifies the ZIP's PNG matches the source bytes. No image-generation tool or external font is used. [Manifest and source hashes](exports/pairing-manifest.json) record the embedded image and source parish artwork.
