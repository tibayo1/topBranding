# Color development 10 — Shared Rhythm + Open Praise

**DRAFT — NOT FOR PUBLICATION.** Five palette families on the current two logos. No logo, exact palette, typography or publishing template is finalized.

![Five palette families on both logos](exports/palette-comparison.png)

- **[Open the five-palette comparison PNG](exports/palette-comparison.png)**
- **[Open the larger teal/navy shortlist](exports/color-shortlist.png)**
- **[Download the color review PDF](exports/color-review-10.pdf)**
- **[Interactive explorer](exports/color-explorer.html)** — download the raw HTML, then open it in a browser. It contains its artwork; no server is required. GitHub's file view displays HTML source rather than running the explorer.
- [Teal application comparison](applications/applications-teal.png) · [Navy application comparison](applications/applications-navy.png)

## The five candidates

These revisit the user's earlier palette families using the current Shared Rhythm and Open Praise artwork. The values are proposed screen colors; earlier concept rankings have not been carried forward.

| Family | Primary | Secondary | Accent | Neutral |
|---|---|---|---|---|
| Navy + gold + ivory | `#14263D` | `#946B2E` | `#C9A467` | `#F6F1E8` |
| Forest + warm gold + cream | `#1C3D32` | `#8B6838` | `#C2A069` | `#F5F0E4` |
| Deep teal + sand + soft gold | `#10494C` | `#D9CBB4` | `#B69255` | `#F6F3EC` |
| Burgundy + muted gold + stone | `#562C3B` | `#96784D` | `#C7AA7D` | `#F1EDE5` |
| Charcoal + ivory + copper | `#282C32` | `#616A74` | `#C78362` | `#F5F0E8` |

Light versions use primary ink for the symbol and full name on neutral. Large dark versions use accent ink for the symbol and neutral for the name on primary. Tiny dark versions use neutral ink for stronger separation. Secondary colors support layouts or surfaces; every swatch does not need to appear inside the logo. Shared Rhythm's four faces keep one ink so color does not substitute for its construction. Open Praise's counter stays open to the actual background.

The same frozen geometry, spacing and working type are used across palettes. Existing practical lockups retain Open Praise's 7% optical reduction, consistently in every family. No mark is enlarged or strengthened selectively to favor a color. Monochrome controls remain available.

## Provisional recommendations

**Deep teal + sand** is the strongest contemporary candidate: the dark teal gives both marks character while warm surfaces temper its coolness. Shared Rhythm feels expressive and spatial; Open Praise feels compact and confident. The gold-on-teal symbol has less contrast than ivory reverse, so use the latter for tiny applications. Sand works as a surface with teal text.

**Navy + gold + ivory** is the strongest dependable alternative: dignified, readable and effective in dark/reverse uses. Its familiar institutional and premium associations make it less distinctive by color alone. Shared Rhythm can lean toward architecture; Open Praise can lean toward a publisher or college. Full-name and church context matter.

Forest is welcoming and calm, but more quiet/heritage in character. Burgundy is warm and ceremonial, with a more solemn impression. Charcoal/copper is versatile and restrained, with weaker color recognition. These are design judgments, not audience-research results.

Shared Rhythm remains the user's preferred starting point; color does not overrule that choice or make Open Praise's T universally clear. Both continue as working directions.

## Contrast and practical limits

| Family | Primary / neutral | Accent / primary |
|---|---:|---:|
| Navy | 13.58:1 | 6.54:1 |
| Forest | 10.48:1 | 4.84:1 |
| Teal | 9.11:1 | 3.48:1 |
| Burgundy | 9.89:1 | 5.21:1 |
| Charcoal | 12.37:1 | 4.58:1 |

Body text uses primary/neutral pairings rather than pale gold on light surfaces. Accent gold on ivory and sand on porcelain are unsuitable for ordinary body copy. A logo contrast measurement is not proof that its symbolism or letters are recognizable; teal's 3.48:1 dark accent is particularly worth comparing with the clearer ivory reverse. Tiny-use cuts remain provisional at 16–20 px, and normal avatars use primary geometry.

The [official RCCG emblem manifest](../../assets/rccg-emblem/README.md) is present, but its original PNG remains absent. Actual paired-logo compatibility is untested; neither emblem colors nor artwork are recreated. The entrance is an imagined proportion diagram. Contact/handle/correspondence placeholders are explicitly labeled; no services, schedules or addresses are invented.

Gold and copper are flat screen colors, not metallic finishes. HEX is precise for this screen study; process CMYK, spot inks, paper, vinyl and physical signage need proofing after a shortlist. No production color match or legal clearance is claimed.

## Editable sources and next step

- [Palette source and color roles](source/palettes.json)
- [Current brief](source/brief.md)
- [Reusable colored SVG manifest](exports/artwork.json) and `artwork/`
- `applications/` contains the editable colored contexts and source manifest.
- `tools/` contains the artwork, explorer and delivery builders.
- [Preceding monochrome development](../identity-development-09/README.md)

Narrow the color candidates first. Then refine any remaining optical details, test the actual unmodified RCCG emblem alongside the parish identity, and proof physical materials. Teammate feedback and final brand approval follow; nothing here triggers publication or updates permanent brand instructions.

To regenerate from the repository root with the existing Python/fontTools/Pillow, Inkscape and Playwright/Chromium environment:

```sh
python brand/explorations/color-development-10/tools/build_artwork.py
python brand/explorations/color-development-10/applications/build.py
python brand/explorations/color-development-10/tools/build_explorer.py
python brand/explorations/color-development-10/tools/build_delivery.py
```

The explorer embeds outlined SVGs and uses system fonts for its interface. The shortlist's self-contained HTML embeds the unmodified Instrument Sans font together with its original copyright/OFL text. The font source and license remain in the preceding development folder. The saved PNG/PDF files provide direct viewing when chat previews fail.
