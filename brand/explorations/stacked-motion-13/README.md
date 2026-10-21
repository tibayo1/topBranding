# Name below + rising-response animation handoff 13

**DRAFT — NOT FOR PUBLICATION.** The user now prefers the complete parish name **below the symbol** for both Shared Rhythm and Open Praise. Teal + sand remains the working palette; final identity and motion approval remain open.

![Both names below their symbols, alongside RCCG](pairings/stacked-pairing-comparison.png)

- **[Download the complete updated-logo and animation kit](exports/UPDATED-LOGOS-AND-GOOGLE-ANIMATION-DRAFT.zip)**
- **[Watch the Shared Rhythm motion study](animation/shared-rhythm-rising-response-1080-DRAFT.mp4)**
- [Open the updated static comparison](pairings/stacked-pairing-comparison.png) · [PDF](pairings/stacked-pairing-review.pdf)
- [Start here](exports/START-HERE.txt)

## The description becomes the movement

Shared Rhythm preserves the user's description, **“a rising reaction to praises”**, expressed as **a rising response to praise**. Four unequal planes suggest people responding together in worship around a shared gathering space. Their rising sequence gives that idea motion; it is a visual metaphor rather than a claim of official mission or doctrine.

The eight-second study starts quietly with the planes slightly lowered. The left outer plane leads an overlapping response from the second inner plane, followed by the tallest inner-right plane and the answering lower right plane. The first two movements stay coordinated to preserve their white interval. The movement stays small and graceful. The outlines, widths and solid fill remain rigid, with one gentle settling movement. By six seconds, the exact logo is still; the last two seconds hold it. The full **Tabernacle of Praise** name stays below, stationary and readable throughout.

Open Praise has a quieter whole-symbol lift and settle, preserving its single counter contour and proposed T/P relationship. It receives the same name-below arrangement. No music, camera movement, extra symbols, pulsing bars, 3D treatment or invented church wording is added.

The supplied MP4/GIF/HTML studies are controlled motion made from the existing vector artwork. They are **not Google-generated videos**. All generative-tool uploads remain the user's choice; nothing is sent to Google automatically.

## Use with your Google animation tool

1. Open the ZIP and read `START-HERE.txt`.
2. For Shared Rhythm, upload the **landscape full-logo end PNG** from `01-upload-to-google/Shared-Rhythm/`. It already has the complete name below. Use image-to-video if your tool provides it.
3. Copy [the Shared Rhythm prompt](exports/shared-rhythm-google-prompt.txt). A matching [Open Praise prompt](exports/open-praise-google-prompt.txt) is included.
4. If the tool supports both start and end images, use the supplied lowered start and exact final image. For a single starting image, the prompt describes a gentle lift-and-return from the finished logo. Duration controls and start/end support depend on the Google tool being used.
5. Compare the result with the exact final PNG before sharing for review. Keep the word spelling, four planes or T/P counter, spacing and final position intact.

Generative video can distort lettering and shapes. The optional symbol-only images leave the name area empty; matching transparent full-canvas name overlays let you add the exact static name in a video editor. Replacing the closing hold with the supplied exact end frame is another useful correction. The [full prompt notes](animation/google-animation-prompts.md) explain this fallback.

## Direct upload images

| Logo | Landscape 1920×1080 | Square 1080×1080 |
|---|---|---|
| Shared Rhythm | [Finished PNG](animation-inputs/shared-rhythm/landscape/full-logo-end-DRAFT.png) · [Start PNG](animation-inputs/shared-rhythm/landscape/full-logo-start-DRAFT.png) | [Finished PNG](animation-inputs/shared-rhythm/square/full-logo-end-DRAFT.png) · [Start PNG](animation-inputs/shared-rhythm/square/full-logo-start-DRAFT.png) |
| Open Praise | [Finished PNG](animation-inputs/open-praise/landscape/full-logo-end-DRAFT.png) · [Start PNG](animation-inputs/open-praise/landscape/full-logo-start-DRAFT.png) | [Finished PNG](animation-inputs/open-praise/square/full-logo-end-DRAFT.png) · [Start PNG](animation-inputs/open-praise/square/full-logo-start-DRAFT.png) |

These are clean reference artwork, with draft status in filenames, metadata and accompanying review notes. No review caption is printed inside the logo. Every PNG has a matching editable SVG. [Input manifest](animation-inputs/manifest.json) records compositions and source hashes. The full logo occupies the same centered 760×779 area at both aspect ratios, retaining the exact refinement 11 paths and outlined lettering.

## Updated RCCG pairings

The [four paired SVGs, source and PDF](pairings/README.md) now put each parish name below its symbol. The RCCG emblem remains separate on the left, aligned with the parish symbol, on a white field/panel. Its full existing reference PNG stays byte-identical and is never recolored, cropped, traced or animated.

Keep the RCCG emblem **out of generative animation inputs**. If a paired animated presentation is needed, add it separately as an unchanged static overlay after generation. The current 236×236 reference's [source record](../../assets/rccg-emblem/references/README.md) remains explicit; it is not the inaccessible original 1200×1200 chat upload or an approved high-resolution production master.

## Sources and rebuild

- [Current brief](source/brief.md) · [layout preference](source/layout.json)
- [Timed storyboard](animation/storyboard.json)
- [Editable light and dark standalone SVGs](exports/shared-rhythm-name-below-light-DRAFT.svg), with both directions in `exports/`
- [Replayable motion HTML](animation/motion-preview-DRAFT.html) — download raw HTML, then open in a browser.
- [Shared Rhythm keyframes](animation/shared-rhythm-motion-contact-sheet.png)

Use the existing Python/Pillow, Inkscape, Playwright/Chromium and ffmpeg environment, from the repository root:

```sh
python brand/explorations/stacked-motion-13/source/build_inputs.py
python brand/explorations/stacked-motion-13/pairings/build.py
python brand/explorations/stacked-motion-13/animation/build_preview.py
python brand/explorations/stacked-motion-13/source/build_package.py
```

Glyphs and symbol geometry stay unchanged from refinement 11; original font/license files remain there. Rendering and final-pose checks establish file/motion consistency, not audience recognition, physical production suitability, final approval or the behavior of an external AI video service. AGENTS.md and the identity skill are unchanged.
