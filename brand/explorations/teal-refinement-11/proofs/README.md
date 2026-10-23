# Screen and physical-size proofs

**DRAFT — NOT FOR PUBLICATION.** These inspect the current two working directions. No production minimum or material/color match is approved.

- [Actual-size A4 vector proof](a4-print-proof.pdf)
- [Editable A4 source](a4-print-proof.svg)
- [Preview of the A4 sheet](print-proof-preview.png)
- [Native screen-size proof](screen-size-proof.png)

Print the PDF at **actual size / 100%**, with Fit, Shrink and similar scaling turned off. Measure the ruler: its end ticks must be **50 mm apart**. If they are not, correct the print scaling before assessing the logos. The PNG preview is for viewing; use the PDF for printing.

The A4 sheet is exactly 210 × 297 mm and contains vector artwork, with no embedded raster images. Symbol labels measure **actual filled ink height** at 8, 12, 18 and 24 mm. Full-name lockup labels measure **the entire symbol-and-name ink width** at 35, 50 and 70 mm. Small source-canvas margins are excluded from those physical measurements. Teal/ivory, black on paper and ivory reverse provide distinct conditions to compare.

The native screen sheet instead labels **SVG viewport widths**, with no enlargement of the rendered samples. Horizontal lockups appear at 180, 240 and 320 px; the new single-line arrangement at 320 and 480 px. Symbol canvases use the primary at 24/32/40 px and the compact cut at 16/20 px. Compare the saved image at 100% zoom. The native samples are whole-pixel aligned; browser resampling and fractional placement can change their appearance.

These files have been rendered and visually inspected. **No physical print has been made or verified here.** Assess actual paper, printer, ink, vinyl and any other intended process before establishing production sizes. Rendering does not prove that viewers recognize architectural space, praise or a proposed T/P. The original RCCG emblem remains absent, so actual paired-emblem proofing is not included.

Rebuild after the final Review 11 artwork assembly:

```sh
python brand/explorations/teal-refinement-11/tools/build_proofs.py
```

The builder reads `exports/artwork.json`, preserves source contour geometry and outlines its own labels from the repository's unmodified licensed Instrument Sans font. The optional `--provisional` switch writes layout-only scratch files under `/tmp`; those are not review deliverables.
