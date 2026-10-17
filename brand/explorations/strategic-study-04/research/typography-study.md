# Full-name typography study

**DRAFT — NOT FOR PUBLICATION.** Research and typographic starting points for the strategic exploration; no typeface, wordmark, or lockup has been approved.

The name is **Tabernacle of Praise**. The wordmark must be legible and memorable in its own right. The previous T/P monogram is historical work, not a requirement for this study. A new wordmark should not be judged by whether it conceals more religious symbols.

## Recommendation

Develop the symbol shortlist using two related voices: **Source Serif 4** for warmth and dignity, and **Instrument Sans** for clarity and contemporary welcome. Keep the body of the presentation in one consistent text family so changes in the logo can be judged fairly. Reserve **Bricolage Grotesque** for a genuinely developed living-wordmark proposal if its letterforms support the concept; it should not become a third arbitrary type style attached to a symbol.

This is a comparison of three type approaches, not a proposal to use three brand families together. The eventual identity should normally use no more than two families. A custom outlined wordmark can be a separate piece of artwork from the everyday text face.

## Three considered approaches

| Approach | Starting point and explicit axes | What it contributes | Risk and appropriate refinement |
| --- | --- | --- | --- |
| Humanist serif | Source Serif 4, `wght=550`, `opsz=24` | Clear distinction between letters, generous lowercase counters, moderate stroke contrast, and enough warmth to support sacred dwelling without pretending to be ancient Hebrew or biblical lettering. | May feel literary or institutional. Keep weight substantial, avoid display optical sizes with fragile fine strokes, and resist ornamental swashes. Assess lighter/heavier weight beside each actual symbol. |
| Contemporary open sans | Instrument Sans, `wght=550`, `wdth=100` | Open, direct name recognition with a calmer, more welcoming rhythm than a rigid geometric construction. A useful control for symbols with richer negative space. | The untouched face alone is not a distinctive wordmark. Refine spacing, terminal logic, and a small number of meaningful details once the symbol concept is known. Do not narrow it merely to fit a layout. |
| Crafted living wordmark | Bricolage Grotesque, `wght=550`, `wdth=100`, `opsz=24` as the initial control | Fuller lowercase forms and a stronger human irregularity offer room for deliberate letter craft. Width and optical-size axes allow genuine designed variants rather than distorted letters. | At restrained settings it is too close to Instrument Sans to justify a separate symbol concept; at exaggerated settings it risks fashionable quirk. Advance it only if the name itself carries the idea through repeated counter shapes, joined structure, or a controlled rhythm that remains readable. No automatic T/P ligature, replaced letter, or harp. |

Source Serif 4 is an especially convincing alternative to the earlier Noto Serif specimen: the complete name has a deliberate rhythm and the lowercase remains open at a modest weight. Instrument Sans is the cleaner practical starting point. The earlier Noto Sans / Noto Serif files remain usable historical controls, not approved brand typography. Their broad language coverage is useful for ordinary communications but does not, by itself, give this parish a distinctive wordmark.

## Name, hierarchy, and lockups

- Use title case for the first comparison: **Tabernacle of Praise**. It retains familiar word shapes and feels approachable. An uppercase trial may be useful for architectural lettering but must be judged independently; tracked capitals change the voice toward the monumental.
- Test the complete single-line name for horizontal arrangements. Beside a compact symbol, a two-line horizontal lockup can use **Tabernacle** above **of Praise**. A separate stacked arrangement places the symbol above those same two lines.
- Keep “of” readable. Making it a tiny decorative connector breaks the spoken name and produces an unnecessary hierarchy. A moderate size reduction can be tested later, after the equal-size control.
- The second line is naturally shorter. At identical font size it measures about 78–80% of the first line in these settings. Accept this rhythm and align intentionally; do not stretch the letters or track lowercase excessively to force an equal-width rectangle.
- Start the symbol-to-name gap near one lowercase x-height, then correct optically. This is a testing value, not a finished clear-space rule. Different silhouettes need different optical adjustments.
- Test full-name outlines at realistic widths around 240 and 320 px, at sign size, and in reverse. A complete name is not a 16 px avatar: keep the 16/24/32 px test for the symbol and report the name's own legibility separately.
- For official pairing, reserve an independent, labeled space for the unchanged authorized RCCG emblem. Do not make the local wordmark conform to a guessed emblem; verify the authorized asset before approving the relationship.

At 100 px nominal font size, with the explicit axes above and shaping enabled, measured advance widths were:

| Face | Full name | “Tabernacle” | “of Praise” | Second / first line |
| --- | ---: | ---: | ---: | ---: |
| Source Serif 4 | 911.77 px | 500.66 px | 388.70 px | 77.6% |
| Instrument Sans | 944.25 px | 519.48 px | 405.27 px | 78.0% |
| Bricolage Grotesque | 958.41 px | 518.27 px | 416.34 px | 80.3% |

These are initial shaped text advances, not final visual bounds. At 18 px, the single-line name is approximately 164–173 px wide. Equal font size is an informative first control; match optical cap height and total visual weight when comparing developed lockups.

## What custom work should earn

Before editing a letter, state the concept in one sentence and identify the real typographic opportunity. The repeated `a` and `e`, the opening `Ta`, and the `Pr`/`ra` sequence offer useful rhythm and spacing tests. A coherent terminal angle or counter shape can echo a symbol without adding a second icon. A shared stroke must preserve both letter readings. Do not claim that an arbitrary white hole represents God's presence, or that a set number of letters encodes doctrine.

For a living-wordmark concept, the useful test is whether the whole name becomes a recognizable composition while still reading immediately. A decorative cross substituted for a letter, a tiny harp inside a counter, and a stretched T that becomes a roof do not automatically make a meaningful identity. Explain the visible structure first, then the intended association and its limits.

## Technical and license verification

Downloaded 17 October 2026 from the Google Fonts repository's `ofl` directories. The files are the original unmodified variable fonts, each accompanied by its exact **SIL Open Font License 1.1** and upstream `METADATA.pb` file. All three parsed successfully in fontTools; each has GPOS positioning and GSUB substitution tables. None has a legacy `kern` table. Preserve shaping and kerning when converting words to outlines instead of simply adding `hmtx` advances.

The original variable fonts can be drawn at specified axes with fontTools `getGlyphSet(location=...)`. Use a shaping engine for glyph selection and positions, then draw with SVG paths. Chromium was used to render and inspect all three actual fonts, in single-line, stacked, uppercase, and 18 px settings. A separate Pillow/libraqm measurement verified the advances above. The temporary specimen is a research control, not a finished logo.

Tested glyph coverage includes the full parish name, `Istanbul`, `Türkiye`, `ÇçĞğİıÖöŞşÜü`, `@`, `&`, and digits 0–9; none is missing. This is a limited coverage check, not a claim to support every language used by parish members.

OFL permits use in logo artwork and embedding/distribution under its conditions. Preserve the license and copyright when distributing fonts. Source Serif 4's metadata declares the reserved name **Source**; if a modified font binary is ever redistributed, comply with the applicable reserved-name requirements. Outlined logo artwork does not require redistributing a modified font binary. These files have not been renamed, subset, or modified. This confirms font licensing, not trademark clearance for a future logo.

### Verified sources

| Family | Original source and author | Local files |
| --- | --- | --- |
| Source Serif 4 | [Adobe / Frank Grießhammer](https://github.com/adobe-fonts/source-serif), upstream source commit recorded in metadata: `b3980ade53bb3d023a0006076d05349236b309b1` | [Variable font](../assets/fonts/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf), [OFL](../assets/fonts/sourceserif4/OFL.txt), [metadata](../assets/fonts/sourceserif4/METADATA.pb) |
| Instrument Sans | [Instrument / Rodrigo Fuenzalida and Jordan Egstad](https://github.com/Instrument/instrument-sans), upstream source commit: `7fa22308a3d0c94ee2b3cd537a1196b65db34a3e` | [Variable font](../assets/fonts/instrumentsans/InstrumentSans%5Bwdth%2Cwght%5D.ttf), [OFL](../assets/fonts/instrumentsans/OFL.txt), [metadata](../assets/fonts/instrumentsans/METADATA.pb) |
| Bricolage Grotesque | [Mathieu Triay](https://github.com/ateliertriay/bricolage), upstream source commit: `84745e5b96261ae5f8c6c856e262fe78d1d6efdd` | [Variable font](../assets/fonts/bricolagegrotesque/BricolageGrotesque%5Bopsz%2Cwdth%2Cwght%5D.ttf), [OFL](../assets/fonts/bricolagegrotesque/OFL.txt), [metadata](../assets/fonts/bricolagegrotesque/METADATA.pb) |

Downloaded URLs follow `https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/<filename>`. Their exact bytes are verified by these SHA-256 checksums:

```text
97b2d4da6e3cb494b5a1e66ae176914d852ccabef49e0c02c0df25f3e39aca0b  sourceserif4/SourceSerif4[opsz,wght].ttf
b24f1812584816958afcf22e22d08e44318c5e51651e25d2438efdde389b33b1  instrumentsans/InstrumentSans[wdth,wght].ttf
413e7357809ddd12fd80a96a8a396de0e401638d4acd3cb3e37532f0472ac682  bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf
```

No typography system is selected. The next review should compare the actual shortlisted concepts with their full names in horizontal and stacked arrangements, with honest notes on what remains to be refined.

## Initial territory F drawings

These are two **initial** ideas in the broader twelve-idea study. Neither is an approved shortlist entry.

- [11 — Shared Line](../sketches/11-living-line-v1.svg): the first T becomes one common overhead line and an anchoring stem. A deliberately drawn structural T is combined with the remaining Source Serif 4 letter outlines; it is not a wholly hand-drawn typeface. The full name reads in two lines. The idea earns comparison because the dwelling structure belongs to the written name, but the heavy initial and beam can resemble a signboard or roof. It is naturally a wide identifier and has no proven compact avatar.
- [12 — Lifted Praise](../sketches/12-lifted-praise-v1.svg): a stable first line is answered by the controlled rise of the six letters in Praise. Bricolage Grotesque outlines remain upright and undistorted. The idea tests a visible movement in the name instead of a separate music icon; it risks feeling like expressive event typography and is presently the weaker enduring-identity proposition.

Both were rendered and inspected in black, reverse white, and at 480 / 240 px overall width. The full name remains readable at the inspected widths. No 16 px whole-wordmark performance is claimed. The SVG audit reports high anchor counts because these are complete twenty-character wordmarks rather than compact icons; Source Serif's curves and Bricolage's intended angled terminals must not be flattened merely to improve a heuristic score. There are no live text objects, embedded rasters, gradients, filters, or strokes in either file. The SVGs contain draft labels in title/description metadata; the review presentation must also carry a visible draft notice.

[Editable builder](../source/typography_sketches.py) reproduces both drawings from the original fonts with fontTools and Pillow/libraqm. [Sketch metadata](../sketches/typography-sketches.json) preserves the idea, construction, inner SVG, viewBox, and honest risk for the browser presentation. Save a new iteration instead of overwriting these drawings if either develops further.
