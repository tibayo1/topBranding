# Application studies — Review 09

**DRAFT — NOT FOR PUBLICATION.** These are limited context studies for continued development of Shared Rhythm and Open Praise. They are not approved identity standards or publishing templates.

Both directions use the same layout, artwork placement boxes, neutral gray backgrounds and application copy. The actual symbol and outlined full-name lockups are embedded unchanged from the Review 09 masters. Their source paths and SHA-256 values are recorded in [manifest.json](manifest.json).

- `*-entrance-sign.svg`: a diagram of an imagined entrance wall; no actual church premises, materials, dimensions or fabrication claims.
- `*-a4-letterhead.svg`: an editable A4 page, with `[CORRESPONDENCE TEXT]` and `[CONTACT DETAILS]` placeholders. `*-letterhead-context.svg` is the separate flat page preview.
- `*-welcome-post.svg`: a hypothetical square identity post saying “Welcome”; no service details or event claims.
- `*-avatar-profile.svg`: a primary-mark crop and illustrative profile, with `[CHURCH HANDLE]` explicitly left as a placeholder. The context uses the full church name and verified Istanbul, Türkiye location. Compact compensation drawings are reserved for the separate 16–20 px tests, rather than enlarged into normal avatars.

The original authorized RCCG emblem is absent from the checkout and is not reconstructed. Textual RCCG affiliation is shown. The companion text in these studies uses outlined Instrument Sans 450, width 100 under its existing SIL Open Font License; this is a working choice, not an approved typography system.

To rebuild after the root Review 09 metadata and masters are ready:

```sh
python3 applications/build.py
```

The builder reads `../exports/development-artwork.json`, creates the eight editable applications and comparison board, then refreshes provenance in the manifest. `--provisional` exists only for layout development against preserved Review 08 artwork; a delivered manifest must have `"provisional": false`.
