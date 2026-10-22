# Visual review — paired motion graphics 14

**DRAFT — NOT FOR PUBLICATION.** Reviewed 22 October 2026. This review concerns presentation and motion craft, not final brand or publishing approval.

Both concepts retain the complete **Tabernacle of Praise** name below their parish symbol. The RCCG reference is separate on the left, in full color on its own white panel, aligned with the parish symbol rather than the combined symbol/name height. The resulting dark teal composition is restrained and visually balanced.

## What was actually inspected

- The end-frame PNGs for both concepts and formats, including native Shared Rhythm landscape and both square compositions.
- A [360 px width comparison](phone-width-review.png). Square gives the parish name more readable size on a phone; landscape suits wider displays. The emblem's fine ring lettering is necessarily small in phone previews.
- Exact-player intermediate frames: [Shared Rhythm at 1.2 seconds, square](shared-rhythm-square-1p2s.png), [Shared Rhythm at 2.1 seconds, landscape](shared-rhythm-landscape-2p1s.png), and [Open Praise at 2.1 seconds, square](open-praise-square-2p1s.png).
- An actual H.264 frame decoded at [1.2 seconds](shared-rhythm-encoded-landscape-1p2s.png) from the frozen Shared Rhythm landscape MP4, SHA-256 `e8294bb8065dbfa85b65235b4f1bc2a9872eb81ad0bb695f2fd75b99a022dd91`.
- The six-frame Shared Rhythm storyboard and the renderer's all-frame checks.

The Shared Rhythm shoulder interval stays open in the inspected intermediate frames, including the encoded frame. All four planes remain distinct; their staggered rise reads as a gentle collective response. The name stays in the same clear lower position. Open Praise's quieter lift preserves its continuous contour and interior opening. No clipping, added symbols, excessive effects or invented church information appeared in the inspected material.

## Source checks

Parsed all four end SVGs. Each embeds the complete existing RCCG PNG byte-for-byte, with no clip path or mask. Each contains 18 outlined name glyphs spelling `TabernacleofPraise`. The authoritative embedded reference SHA-256 remains `977ee1c5a43c30d2859e31f59705da23a53e8c3e7736d1d1376e021c62703340`.

The renderer reports that all 300 lossless pre-encode frames of each format preserve the emblem and name regions, retain four separate Shared Rhythm components, and match the exact end PNG during the 6–10 second hold. This review sampled frames visually; it does not claim a separate visual inspection of every encoded frame. H.264/YUV compression is lossy.

No craft correction is required from this review. Recommend the **square version for phone sharing** and landscape for wider screens. The existing 236 px parish-source reference remains explicitly a draft asset, not the unavailable 1200 px chat upload or an approved print master. No Google upload or generation occurred.
