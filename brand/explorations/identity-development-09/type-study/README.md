# Companion lettering — working study

**DRAFT — NOT FOR PUBLICATION.** No logo, font family, type weight or lockup has been approved.

[View the three-way comparison](typographic-comparison.png). Both columns use the unchanged Review 08 symbols. This isolates the lettering decision while the symbols develop separately. It introduces no third logo direction.

The full name is **Tabernacle of Praise**. All letters, including “of,” use the same size and weight within each specimen. No enlarged roof-like T, decorative connector, hidden symbol or substituted letter is used.

| Specimen | Construction | Value | Tradeoff |
| --- | --- | --- | --- |
| Open title case | Instrument Sans, weight 470, width 100; normal shaping plus small optical pair adjustments and 0.002 em tracking | Familiar word shapes; clean, contemporary and welcoming | The family remains recognizably font-based; the symbol carries the more distinctive identity |
| Measured capitals | Instrument Sans, weight 500, width 100; 0.085 em tracking with optical corrections | Deliberate spacing and a compact, more ceremonial name block | More formal; may strengthen a civic or institutional association |
| Warm serif | Source Serif 4, weight 500, optical size 24; normal shaping plus optical corrections and 0.002 em tracking | Warmth, dignity and strong reading rhythm | More literary; with Open Praise, it can accentuate heritage or editorial associations |

## Provisional working recommendations

For **Shared Rhythm**, use **Open title case** as the working control. Familiar lowercase shapes bring welcome to the angular, unequal folded surfaces and retain the clean full-name feel of the earlier praise study. The serif is a useful warmth comparison, rather than a selected system.

For **Open Praise**, begin with **Open title case** too. The emblem is already compact and assertive; the plain companion name gives it breathing room and makes the parish name immediate. **Measured capitals** is the strongest alternative if a more formal voice is desired. It needs careful assessment for a civic or institutional reading.

Using the same provisional lettering for both does not commit the future identities to the same typography. It gives a clean control while judging the two symbols. The three alternatives remain editable and available for review.

## Editable artwork

- [Title-case single line](specimens/01-open-titlecase-single-line.svg) and [two lines](specimens/01-open-titlecase-two-line.svg)
- [Capitals single line](specimens/02-measured-capitals-single-line.svg) and [two lines](specimens/02-measured-capitals-two-line.svg)
- [Serif single line](specimens/03-warm-serif-single-line.svg) and [two lines](specimens/03-warm-serif-two-line.svg)
- [Spacing, axes, glyph positions and provisional recommendations](metadata.json)
- [Editable comparison board](typographic-comparison.svg)
- [Reproducible builder](build.py)

Each wordmark uses filled glyph outlines, with each letter labeled through `data-letter`. The builder retains the original glyph contours, natural font overshoot and kerning. The additional pair adjustments are explicitly recorded in em units; no font binary or letter shape has been modified. This is **font-based companion lettering**, not a bespoke typeface or a claim of original glyph design.

The comparison fits both symbols to the same ink field and names into the same available width. All scaling is uniform. Capitals naturally have a shorter overall word-shape height; they are not vertically stretched to match lowercase. These comparison fields are not proposed minimum sizes or permanent clear-space rules.

## Font rights and reproduction

Both fonts, their exact upstream metadata and their original SIL Open Font License files are copied without changes from the verified Study 04 font assets. The builder verifies that the copied bytes match. Source Serif 4’s reserved font name rules still apply if a modified font binary is ever distributed. No modified font binary is supplied here.

- Instrument Sans: [original font](fonts/instrumentsans/InstrumentSans%5Bwdth%2Cwght%5D.ttf), [OFL](fonts/instrumentsans/OFL.txt), [metadata](fonts/instrumentsans/METADATA.pb)
- Source Serif 4: [original font](fonts/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf), [OFL](fonts/sourceserif4/OFL.txt), [metadata](fonts/sourceserif4/METADATA.pb)

Run `python3 brand/explorations/identity-development-09/type-study/build.py` from the repository root. It requires fontTools, Pillow with libraqm, and Inkscape for the comparison PNG. SVG wordmarks themselves have no font dependency. The comparison board’s explanatory captions use a system sans; the proposed parish lettering is outlined throughout.

These are draft layout studies. They establish neither trademark clearance nor team approval. Full-name minimum sizes and official RCCG pairing remain to be tested within the developed lockups.
