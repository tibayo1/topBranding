# Tabernacle of Praise — Creative Review 05

**DRAFT — NOT FOR PUBLICATION. Five developed directions; no logo, palette, type system, or official lockup is approved.**

![Five developed monochrome directions](exports/creative-review-05-overview.png)

- **[Open the interactive review](exports/tabernacle-creative-review-05.html)** — on GitHub, download the raw HTML file, then open it in your browser. Its artwork, fonts, comparisons, SVG downloads and review-note controls work offline.
- **[View the six-page review PDF](exports/tabernacle-creative-review-05.pdf)**.
- [Download the editable review package](exports/creative-review-05-editable.zip).
- [Read the current brief](source/user-brief.md) and [review conditions](source/art-direction.md).

## The five directions

| Direction | What the construction means | Critical limitation | Large drawing |
| --- | --- | --- | --- |
| A — Sacred Space / **Open Crossing** | Two faceted boundaries hold an open cruciform interior; their thresholds make the Christian gathering space open rather than sealed. | Dense and institutional; praise is less immediate than sacred space. | [A](exports/direction-a.png) |
| B — Dwelling and Expression / **Passing Shelter** | The same passing surfaces hold a shared interval and release outward: shelter becomes an expressive gesture. | Wave, bird or fabric reads sooner than dwelling; the interval needs 24 px or more. | [B](exports/direction-b.png) |
| C — Contemporary Ecclesiastical Emblem / **The Joined Roundel** | Crafted T and P initials sit within an open enclosing contour; the name and shared dwelling organize the emblem. | University, heritage and luxury associations; the ring may feel decorative. | [C](exports/direction-c.png) |
| D — Custom Typographic Identity / **Open Counter** | Six originally drawn letters and related counter openings give the full parish name a consistent, restrained character. | Editorial rather than explicitly Christian; no viable 16 px full-name avatar. | [D](exports/direction-d.png) |
| E — Cadenced Wall Reimagined / **Opening Measure** | One joined architectural mass opens through a larger shared interior and measured cuts; cadence belongs inside the dwelling. | Property, product or sculptural associations remain; fine cadence weakens at tiny sizes. | [E](exports/direction-e.png) |

The review shows **20 curated initial premises**: A4, B4, C3, D3 and E6. Each includes its visual idea and selection or rejection reason. Meaningful intermediate drawings are preserved separately. E receives the broader investigation requested in the brief; it receives the same developed presentation conditions as the other four.

## Professional assessment

C currently has the most resolved emblematic construction. D gives the clearest name recognition and avoids a separate symbol. Both warrant discussion, with C's heritage tone and D's editorial character left visible.

A communicates Christian sacred space most directly, but its weight still needs a warmth test. B is the most expressive gesture, with the least secure unaided church reading. E is a substantial replacement for the earlier skyline arrangement and should stay active; its extra development does not make it the automatic winner. The browser compares all five against the same ten questions from the brief, without numerical scores that imply a settled choice.

## What is included

The browser has equal-condition monochrome and reverse artwork, complete-name horizontal and stacked lockups, construction and negative-space breakdowns, native 64/32/24/16 px symbol tests, 320/240 px full-name tests, and hypothetical wall-sign and stationery studies. Direction D is honestly tested as a full-name wordmark rather than squeezed into a tiny symbol box. Review selections and notes remain local; downloadable review JSON explicitly records that approvals are false.

The newer repository [emblem manifest](source/rccg-emblem-manifest.md) records a user-supplied RCCG PNG, but confirms that the actual image file still needs transferring. The original file is absent from the checkout and available attachments. Pairing studies therefore use an explicit reservation. No emblem was traced, generated, recolored or merged. Actual emblem balance, color competition and publication authorization remain unverified. Application scenes are illustrative proportions, not photographs of the church's premises. No event, schedule, address, clergy or contact facts are invented.

## Editable files and provenance

- `directions/` — curated metadata, original sketches, developed SVG masters, meaningful refinements and native-size renders.
- `exports/` — 30 editable SVGs, overview and direction PNGs, PDF, standalone HTML, review data and ZIP.
- `source/` — current brief and art direction; retained Study 04 [biblical](source/research/scriptural-foundations.md) and [architectural](source/research/architecture-and-symbolism.md) research with retrieval provenance. These older research documents describe their historical round, not five approved Review 05 marks.
- `assets/` — original licensed fonts and their license notices. Source Serif 4 and Instrument Sans companion wordmarks are outlined; no font binary was modified. D draws T/P/a/e/r/f originally and uses unchanged Source Serif 4 shapes for the other letters. It is not claimed to be a wholly new typeface. Noto Sans/Serif support the review interface and earlier source specimens.
- `tools/` — reusable builders and browser validation. Preliminary SVG audit scores are geometry heuristics, not evidence of artistic quality or trademark clearance.

## Run or rebuild

Open the standalone HTML directly for review. To work on the editable browser, serve this directory with `python3 -m http.server 8767 --bind 127.0.0.1` and inspect it locally. Python 3 with fontTools and Pillow builds the outlined companion lockups; Playwright and Chromium build the PNG/PDF review and run browser checks. These are development tools, not dependencies of the downloaded standalone HTML.

From this directory, run the builders in order:

```sh
python3 tools/build_review.py
python3 tools/build_offline.py
python3 tools/build_exports.py
python3 tools/package_review.py
python3 tools/verify_review.py http://127.0.0.1:8767
```

The final validation report is a separate companion rather than a member of its own hashed ZIP. It records actual output hashes and executed checks. Browser testing establishes delivery behavior and source fidelity; congregation recognition, physical print/fabrication, actual RCCG pairing and legal clearance remain outside those tests.

This review stops for feedback. Earlier studies remain historical, and AGENTS.md and the RCCG identity skill are unchanged.
