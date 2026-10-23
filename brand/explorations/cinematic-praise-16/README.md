# Shared Rhythm — a rising response

**DRAFT — NOT FOR PUBLICATION.** A fourteen-second motion film developing gathering, collective praise and the folded sanctuary form into one visual story. This develops Shared Rhythm; Open Praise remains a separate active option. No final identity or motion system is approved.

- **[Watch with original sound study](exports/shared-rhythm-cinematic-1080p-SOUND-DRAFT.mp4)**
- **[Watch the silent version](exports/shared-rhythm-cinematic-1080p-SILENT-DRAFT.mp4)**
- **[Download the film, previews and editable sources](exports/SHARED-RHYTHM-CINEMATIC-DRAFT.zip)**
- [Start here](exports/START-HERE.txt) · [Portable browser preview](preview.html)

![Shared Rhythm motion storyboard](previews/storyboard-DRAFT.png)

## The story

Individual strands suggest distinct voices. They gather around a shared open space, respond in one upward movement, then unfold into Shared Rhythm's four architectural planes. Camera movement, grazing highlights and dimensional surfaces build the reveal. The idea is **a rising response to praise**, preserving the user's phrase **“a rising reaction to praises”** as a creative interpretation of communal worship.

The film ends with a still hold from 10.5–14 seconds. That closing composition uses the exact [latest larger RCCG pairing](../balanced-emblem-15/README.md): the intact RCCG reference on its separate white panel, the parish symbol and the full two-line name below. The complete logos have comparable overall height. The wordmark and emblem are composited from the existing artwork, preserving their detail and spacing.

This film uses deterministic procedural graphics and rendering source authored for this project. It is not a Google-generated video. No image or footage from the user's uploaded film is included, and no files have been sent to Google or teammates. The motion is a design metaphor; no real parish gathering or official mission is depicted.

## Files

| File | Use |
|---|---|
| [Sound MP4](exports/shared-rhythm-cinematic-1080p-SOUND-DRAFT.mp4) | 1920×1080, 30 fps, fourteen seconds, optional original sound study |
| [Silent MP4](exports/shared-rhythm-cinematic-1080p-SILENT-DRAFT.mp4) | Same visuals without audio |
| [GIF preview](previews/shared-rhythm-cinematic-DRAFT.gif) | Quick visual review; no sound |
| [Closing PNG](exports/shared-rhythm-cinematic-end-DRAFT.png) · [SVG](exports/shared-rhythm-cinematic-end-DRAFT.svg) | Exact existing paired artwork for comparison and editing |
| [Browser preview](preview.html) | Download and open the portable file to replay the visual sequence |
| [Storyboard](previews/storyboard-DRAFT.png) | Keyframes for discussing narrative and craft |

## Editable sources and review

[Current brief](source/brief.md) · [Scene parameters](source/scene.json) · [Motion source](source/film.js) · [Renderer](source/build_film.py) · [Render checks](exports/render-checks.json) · [Sound source](audio/build_sound.py) · [Sound notes](audio/sound-notes.md) · [Sound checks](audio/sound-checks.json) · [Package manifest](exports/package-manifest.json)

The original synthesized sound study contains no existing recording, speech or choir. Technical checks cover duration, headroom and fades. It has not been auditioned by the assistant in this environment; the audio version is optional and awaits listening review. The silent version contains the same visuals.

The existing RCCG reference remains the [documented 236×236 parish-source PNG](../../assets/rccg-emblem/references/README.md), embedded byte-for-byte and enlarged for the requested proportion review. It is not the unavailable original chat upload or a high-resolution production master. Final production-asset authorization and publication approval remain open.

Rebuild from the repository root with the existing Python, Pillow, NumPy/SciPy, Playwright/Chromium and ffmpeg tools:

```sh
python brand/explorations/cinematic-praise-16/source/build_film.py
python brand/explorations/cinematic-praise-16/audio/build_sound.py
python brand/explorations/cinematic-praise-16/source/mux_sound.py
```

The package instructions document audio muxing and source dependencies. Exact hold comparisons apply before lossy H.264 encoding; encoded video does not preserve pixel-for-pixel equality. Original font/license files remain available with the source study and rebuild package. AGENTS.md and the church identity skill are unchanged.
